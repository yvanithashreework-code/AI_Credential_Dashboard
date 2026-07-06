from rest_framework.views import APIView
from rest_framework.response import Response

from api.permissions import IsAdmin
from api.models import VanpreSalary
from credentials.models import User


class DeleteEmployeeView(APIView):
    """
    Admin-only. Deletes an employee's User account and all their
    VanpreSalary records from AWS RDS, identified by employee_id.
    """
    permission_classes = [IsAdmin]

    def delete(self, request, employee_id):
        try:
            user = User.objects.get(employee_id=employee_id, role="employee")
        except User.DoesNotExist:
            return Response({"error": f"No employee found with ID {employee_id}"}, status=404)

        deleted_salary_count, _ = VanpreSalary.objects.filter(employee_id=employee_id).delete()
        full_name = user.full_name
        user.delete()

        return Response({
            "message": f"Deleted employee #{employee_id} ({full_name})",
            "salary_records_deleted": deleted_salary_count,
        })
