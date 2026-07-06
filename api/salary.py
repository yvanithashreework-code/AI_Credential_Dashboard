from rest_framework.views import APIView
from rest_framework.response import Response
from api.permissions import IsAdmin, IsEmployee
from api.models import VanpreSalary
from api.serializers import VanpreSalarySerializer


class AdminSalaryView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        salaries = VanpreSalary.objects.all().order_by("-year", "-total_pay")

        # Exact employee_id lookup -- used by the admin "salary check" search
        employee_id = request.GET.get("employee_id")
        if employee_id:
            try:
                salaries = salaries.filter(employee_id=int(employee_id))
            except ValueError:
                pass

        # Partial job title / name search
        search = request.GET.get("search")
        if search:
            salaries = salaries.filter(employee_name__icontains=search)

        total_count = salaries.count()

        # Support an optional ?limit= param so the frontend doesn't have to
        # pull all 148K+ records just to render a summary table. Defaults
        # to returning everything if not specified, but the frontend should
        # always pass a limit for dashboard views.
        limit = request.GET.get("limit")
        if limit:
            try:
                limit = int(limit)
                salaries = salaries[:limit]
            except ValueError:
                pass

        serializer = VanpreSalarySerializer(salaries, many=True)
        return Response({
            "count": total_count,
            "returned": len(serializer.data),
            "results": serializer.data
        })


class EmployeeSalaryView(APIView):
    permission_classes = [IsEmployee]

    def get(self, request):
        salaries = VanpreSalary.objects.filter(
            employee_id=request.user.employee_id
        ).order_by("-year")

        if not salaries.exists():
            return Response(
                {"detail": "No salary records found for this employee"},
                status=404
            )

        serializer = VanpreSalarySerializer(salaries, many=True)
        return Response({
            "count": salaries.count(),
            "results": serializer.data
        })
