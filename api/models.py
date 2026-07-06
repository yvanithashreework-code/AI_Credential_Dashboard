from django.db import models
from django.conf import settings

class PredictionRequest(models.Model):
    input_data = models.JSONField()
    prediction_result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PredictionRequest {self.id}"


class VanpreSalary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="salary_records"
    )

    employee_id = models.IntegerField()                     # Id
    employee_name = models.CharField(max_length=255)        # EmployeeName
    job_title = models.CharField(max_length=255)            # JobTitle

    base_pay = models.FloatField()                          # BasePay
    overtime_pay = models.FloatField()                      # OvertimePay
    other_pay = models.FloatField()                         # OtherPay
    benefits = models.FloatField()                          # Benefits

    total_pay = models.FloatField()                         # TotalPay
    total_pay_benefits = models.FloatField()                # TotalPayBenefits

    year = models.IntegerField()                            # Year
    notes = models.TextField(null=True, blank=True)         # Notes
    agency = models.CharField(max_length=255)               # Agency
    status = models.CharField(max_length=255, null=True, blank=True)  # Status

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vanpre_salary"
        ordering = ["-year", "-total_pay"]

    def __str__(self):
        return f"{self.employee_name} - {self.year}"
