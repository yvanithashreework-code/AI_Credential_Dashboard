from rest_framework import serializers
from .models import PredictionRequest, VanpreSalary

class PredictionRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for ML prediction requests.
    Ensures input_data is valid JSON and prediction is optional.
    """

    class Meta:
        model = PredictionRequest
        fields = ["id", "input_data", "prediction_result", "created_at"]
        read_only_fields = ["id", "prediction_result", "created_at"]


class VanpreSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = VanpreSalary
        fields = [
            "id",
            "employee_id",
            "employee_name",
            "job_title",
            "base_pay",
            "overtime_pay",
            "other_pay",
            "benefits",
            "total_pay",
            "total_pay_benefits",
            "year",
            "agency",
            "status",
        ]
