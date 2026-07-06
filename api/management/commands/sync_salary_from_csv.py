"""
sync_salary_from_csv.py

Makes the database match the CSV EXACTLY: adds employees present in the
CSV but missing from the database, and DELETES employees present in the
database but missing from the CSV (e.g. because their row was removed).

SAFETY: this defaults to a DRY RUN. It will only show you what it WOULD
do. Nothing is added or deleted until you re-run it with --confirm.

Usage:
    python manage.py sync_salary_from_csv salary.csv              # dry run
    python manage.py sync_salary_from_csv salary.csv --confirm     # actually applies changes
"""

import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import transaction
from credentials.models import User
from api.models import VanpreSalary

DEFAULT_EMPLOYEE_PASSWORD = "Welcome@123"


def safe_float(value, default=0.0):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (ValueError, TypeError):
        return default


class Command(BaseCommand):
    help = "Sync the database to exactly match a CSV file, including deletions. Dry-run by default."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to CSV file")
        parser.add_argument(
            "--confirm", action="store_true",
            help="Actually apply changes. Without this flag, only a preview is shown."
        )
        parser.add_argument(
            "--batch-size", type=int, default=5000,
            help="Batch size for bulk operations (default: 5000)"
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        confirm = kwargs["confirm"]
        batch_size = kwargs["batch_size"]

        self.stdout.write(self.style.SUCCESS("Reading CSV file..."))
        df = pd.read_csv(file_path, low_memory=False)
        df = df[df["Id"].notna()]
        df["Id"] = df["Id"].astype(int)

        csv_ids = set(df["Id"].tolist())
        db_ids = set(
            User.objects.filter(role="employee").values_list("employee_id", flat=True)
        )

        to_add_ids = csv_ids - db_ids
        to_delete_ids = db_ids - csv_ids

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=== SYNC PREVIEW ==="))
        self.stdout.write(f"Employees in CSV:      {len(csv_ids)}")
        self.stdout.write(f"Employees in database: {len(db_ids)}")
        self.stdout.write(f"Would ADD:             {len(to_add_ids)}")
        self.stdout.write(f"Would DELETE:          {len(to_delete_ids)}")
        self.stdout.write("")

        if to_delete_ids:
            sample_to_delete = User.objects.filter(
                employee_id__in=list(to_delete_ids)[:10]
            ).values_list("employee_id", "full_name")
            self.stdout.write(self.style.WARNING(
                f"Sample of employees that would be DELETED (showing up to 10):"
            ))
            for emp_id, name in sample_to_delete:
                self.stdout.write(f"  - #{emp_id}: {name}")
            self.stdout.write("")

        if not confirm:
            self.stdout.write(self.style.WARNING(
                "DRY RUN ONLY -- no changes were made. "
                "Re-run with --confirm to actually apply these changes."
            ))
            return

        # ---------------------------------------------------------
        # Apply additions
        # ---------------------------------------------------------
        if to_add_ids:
            self.stdout.write(f"Adding {len(to_add_ids)} new employees...")
            new_rows = df[df["Id"].isin(to_add_ids)].drop_duplicates(subset="Id")

            hashed_password = make_password(DEFAULT_EMPLOYEE_PASSWORD)
            new_users = [
                User(
                    employee_id=int(row["Id"]),
                    email=f"user_{int(row['Id'])}@vanpre.com",
                    full_name=str(row["EmployeeName"]).strip(),
                    role="employee",
                    password=hashed_password,
                )
                for _, row in new_rows.iterrows()
            ]
            with transaction.atomic():
                User.objects.bulk_create(new_users, batch_size=batch_size, ignore_conflicts=True)

            id_to_user_id = dict(
                User.objects.filter(employee_id__in=to_add_ids).values_list("employee_id", "id")
            )

            salary_objects = []
            for _, row in df[df["Id"].isin(to_add_ids)].iterrows():
                employee_id = int(row["Id"])
                user_id = id_to_user_id.get(employee_id)
                if user_id is None:
                    continue
                salary_objects.append(VanpreSalary(
                    user_id=user_id,
                    employee_id=employee_id,
                    employee_name=str(row["EmployeeName"]).strip(),
                    job_title=str(row["JobTitle"]).strip(),
                    base_pay=safe_float(row.get("BasePay")),
                    overtime_pay=safe_float(row.get("OvertimePay")),
                    other_pay=safe_float(row.get("OtherPay")),
                    benefits=safe_float(row.get("Benefits")),
                    total_pay=safe_float(row.get("TotalPay")),
                    total_pay_benefits=safe_float(row.get("TotalPayBenefits")),
                    year=int(row["Year"]),
                    notes=str(row.get("Notes", "")) if pd.notna(row.get("Notes")) else "",
                    agency=str(row.get("Agency", "")).strip(),
                    status=str(row.get("Status", "")) if pd.notna(row.get("Status")) else "",
                ))
            with transaction.atomic():
                VanpreSalary.objects.bulk_create(salary_objects, batch_size=batch_size)

        # ---------------------------------------------------------
        # Apply deletions (VanpreSalary rows cascade-delete automatically
        # via the ForeignKey's on_delete=CASCADE when the User is deleted)
        # ---------------------------------------------------------
        if to_delete_ids:
            self.stdout.write(f"Deleting {len(to_delete_ids)} employees no longer in the CSV...")
            with transaction.atomic():
                User.objects.filter(employee_id__in=to_delete_ids).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Sync complete! Added: {len(to_add_ids)}, Deleted: {len(to_delete_ids)}"
        ))
