from django.urls import path
from .auth import LoginView, RefreshView
from .salary import AdminSalaryView, EmployeeSalaryView
from .predictions import SalaryPredictView, SalaryBandPredictView, AnomalyPredictView
from .employees import AddEmployeeView
from .employee_delete import DeleteEmployeeView
from .analytics import AdminAnalyticsView

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", RefreshView.as_view(), name="token_refresh"),

    path("salary/admin/", AdminSalaryView.as_view(), name="salary_admin"),
    path("salary/employee/", EmployeeSalaryView.as_view(), name="salary_employee"),

    path("predict/salary/", SalaryPredictView.as_view(), name="predict_salary"),
    path("predict/band/", SalaryBandPredictView.as_view(), name="predict_band"),
    path("predict/anomaly/", AnomalyPredictView.as_view(), name="predict_anomaly"),

    path("employees/add/", AddEmployeeView.as_view(), name="add_employee"),
    path("employees/delete/<int:employee_id>/", DeleteEmployeeView.as_view(), name="delete_employee"),

    path("analytics/admin/", AdminAnalyticsView.as_view(), name="admin_analytics"),
]
