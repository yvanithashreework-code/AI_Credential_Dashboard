from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("employees", views.employees, name="employees"),
]
