from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAdmin
from api.models import PredictionRequest
from api import ml_utils


class SalaryPredictView(APIView):
    """
    Predicts expected total pay for a given job title + year.
    Available to both employees (for themselves) and admins (for anyone).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        job_title = request.data.get("job_title")
        year = request.data.get("year")

        if not job_title or not year:
            return Response(
                {"error": "job_title and year are required"}, status=400
            )

        try:
            year = int(year)
        except (ValueError, TypeError):
            return Response({"error": "year must be a number"}, status=400)

        try:
            result = ml_utils.predict_salary(job_title, year)
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=503)

        PredictionRequest.objects.create(
            input_data={"job_title": job_title, "year": year, "model": "salary_regressor"},
            prediction_result=result,
        )

        return Response(result)


class SalaryBandPredictView(APIView):
    """
    Predicts a Low/Mid/High pay band for a given job title + year.
    Available to both employees and admins.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        job_title = request.data.get("job_title")
        year = request.data.get("year")

        if not job_title or not year:
            return Response(
                {"error": "job_title and year are required"}, status=400
            )

        try:
            year = int(year)
        except (ValueError, TypeError):
            return Response({"error": "year must be a number"}, status=400)

        try:
            result = ml_utils.predict_salary_band(job_title, year)
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=503)

        PredictionRequest.objects.create(
            input_data={"job_title": job_title, "year": year, "model": "salary_band_classifier"},
            prediction_result=result,
        )

        return Response(result)


class AnomalyPredictView(APIView):
    """
    Flags whether a pay record looks unusual. ADMIN ONLY -- this checks
    one employee's data against patterns across the whole company, which
    isn't appropriate for an employee to run on themselves or others.
    """
    permission_classes = [IsAdmin]

    def post(self, request):
        required_fields = ["job_title", "base_pay", "overtime_pay", "other_pay", "total_pay", "year"]
        missing = [f for f in required_fields if request.data.get(f) is None]

        if missing:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing)}"}, status=400
            )

        try:
            job_title = request.data["job_title"]
            base_pay = float(request.data["base_pay"])
            overtime_pay = float(request.data["overtime_pay"])
            other_pay = float(request.data["other_pay"])
            total_pay = float(request.data["total_pay"])
            year = int(request.data["year"])
        except (ValueError, TypeError):
            return Response({"error": "Numeric fields must be valid numbers"}, status=400)

        try:
            result = ml_utils.predict_anomaly(
                job_title, base_pay, overtime_pay, other_pay, total_pay, year
            )
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=503)

        PredictionRequest.objects.create(
            input_data={**request.data, "model": "anomaly_detector"},
            prediction_result=result,
        )

        return Response(result)
