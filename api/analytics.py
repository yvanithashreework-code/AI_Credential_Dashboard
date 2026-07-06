import pandas as pd
from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response

from api.permissions import IsAdmin
from api.models import VanpreSalary
from api import ml_utils


class AdminAnalyticsView(APIView):
    """
    Admin-only. Returns aggregated, dataset-wide statistics for the
    Analysis & Trends page: overall KPIs, pay trend by year, top-paid
    job titles, salary band distribution, and a live anomaly count
    computed by running the anomaly detector over every record.
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        total_employees = VanpreSalary.objects.count()
        avg_total_pay = VanpreSalary.objects.aggregate(avg=Avg("total_pay"))["avg"] or 0
        distinct_job_titles = VanpreSalary.objects.values("job_title").distinct().count()

        avg_pay_by_year = list(
            VanpreSalary.objects.values("year")
            .annotate(avg_total_pay=Avg("total_pay"), count=Count("id"))
            .order_by("year")
        )

        # Only consider job titles with a meaningful sample size (50+
        # records) so a single rare, highly-paid title doesn't dominate
        # the "top paid roles" list.
        top_job_titles = list(
            VanpreSalary.objects.values("job_title")
            .annotate(avg_total_pay=Avg("total_pay"), count=Count("id"))
            .filter(count__gte=50)
            .order_by("-avg_total_pay")[:10]
        )

        band_distribution = None
        try:
            band_bundle = ml_utils.get_salary_band_classifier()
            cutoffs = band_bundle["band_cutoffs"]
            low_count = VanpreSalary.objects.filter(total_pay__lte=cutoffs["low"]).count()
            high_count = VanpreSalary.objects.filter(total_pay__gt=cutoffs["high"]).count()
            mid_count = total_employees - low_count - high_count
            band_distribution = {"Low": low_count, "Mid": mid_count, "High": high_count}
        except FileNotFoundError:
            pass

        anomaly_count = None
        try:
            anomaly_bundle = ml_utils.get_anomaly_detector()
            model = anomaly_bundle["model"]
            freq_map = anomaly_bundle["job_title_freq_map"]

            records = VanpreSalary.objects.all().values(
                "job_title", "base_pay", "overtime_pay", "other_pay", "total_pay", "year"
            )
            df = pd.DataFrame.from_records(records)
            if not df.empty:
                df["job_title_norm"] = df["job_title"].str.strip().str.upper()
                fallback = freq_map.get("OTHER", min(freq_map.values()) if freq_map else 0.0)
                df["job_title_freq"] = df["job_title_norm"].map(freq_map).fillna(fallback)
                features = df[["job_title_freq", "base_pay", "overtime_pay", "other_pay", "total_pay", "year"]]
                predictions = model.predict(features)
                anomaly_count = int((predictions == -1).sum())
        except FileNotFoundError:
            pass

        return Response({
            "total_employees": total_employees,
            "avg_total_pay": round(avg_total_pay, 2),
            "distinct_job_titles": distinct_job_titles,
            "anomaly_count": anomaly_count,
            "avg_pay_by_year": avg_pay_by_year,
            "top_job_titles_by_avg_pay": top_job_titles,
            "band_distribution": band_distribution,
        })
