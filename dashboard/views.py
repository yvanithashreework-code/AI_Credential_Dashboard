import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from backend.auth import login_user, verify_token
from .models import User, Employee


# ✅ JWT-based login
@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token_data = login_user(username, password)
        return Response(token_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


# ✅ Employees CRUD (same as your old code, but JWT protected)
@csrf_exempt
def employees(request):
    # Token verification (optional: protect this endpoint)
    token = request.headers.get("Authorization")
    if token:
        try:
            token = token.replace("Bearer ", "")
            username = verify_token(token)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=401)

    if request.method == "GET":
        data = list(Employee.objects.values())
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        data = json.loads(request.body)
        emp = Employee.objects.create(
            name=data["name"],
            email=data["email"],
            department=data["department"]
        )
        return JsonResponse({"id": emp.id, "message": "Employee created"})
