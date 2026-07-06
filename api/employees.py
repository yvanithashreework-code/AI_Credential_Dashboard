from django.db.models import Max
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response

from api.permissions import IsAdmin
from api.models import VanpreSalary
from credentials.models import User

DEFAULT_EMPLOYEE_PASSWORD = "Welcome@123"


class AddEmployeeView(APIView):
    """
    Admin-only. Creates a new employee: a User account (for login) plus
    their first VanpreSalary record. This is the "form" data-entry path --
    every field submitted here is written straight to AWS RDS immediately,
    the same way the bulk CSV import works, just one record at a time.
    """
    permission_classes = [IsAdmin]

    REQUIRED_FIELDS = ["full_name", "job_title", "base_pay", "overtime_pay", "other_pay", "benefits", "year"]

    def post(self, request):
        missing = [f for f in self.REQUIRED_FIELDS if request.data.get(f) in (None, "")]
        if missing:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing)}"}, status=400
            )

        try:
            full_name = str(request.data["full_name"]).strip()
            job_title = str(request.data["job_title"]).strip()
            base_pay = float(request.data["base_pay"])
            overtime_pay = float(request.data["overtime_pay"])
            other_pay = float(request.data["other_pay"])
            benefits = float(request.data["benefits"])
            year = int(request.data["year"])
        except (ValueError, TypeError):
            return Response({"error": "Pay fields and year must be valid numbers"}, status=400)

        # Auto-assign the next available employee_id -- avoids collisions
        # and matches how the CSV import treats each row as one employee.
        max_id = User.objects.aggregate(Max("employee_id"))["employee_id__max"] or 0
        new_employee_id = max_id + 1

        email = f"user_{new_employee_id}@vanpre.com"

        user = User.objects.create(
            employee_id=new_employee_id,
            email=email,
            full_name=full_name,
            role="employee",
            password=make_password(DEFAULT_EMPLOYEE_PASSWORD),
        )

        total_pay = base_pay + overtime_pay + other_pay
        total_pay_benefits = total_pay + benefits

        salary_record = VanpreSalary.objects.create(
            user=user,
            employee_id=new_employee_id,
            employee_name=full_name,
            job_title=job_title,
            base_pay=base_pay,
            overtime_pay=overtime_pay,
            other_pay=other_pay,
            benefits=benefits,
            total_pay=total_pay,
            total_pay_benefits=total_pay_benefits,
            year=year,
            agency="San Francisco",
            status="",
        )

        return Response({
            "employee_id": new_employee_id,
            "email": email,
            "default_password": DEFAULT_EMPLOYEE_PASSWORD,
            "full_name": full_name,
            "job_title": job_title,
            "total_pay": total_pay,
        }, status=201)
