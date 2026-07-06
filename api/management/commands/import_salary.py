import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from credentials.models import User
from api.models import VanpreSalary


def safe_float(value, default=0.0):
    """Convert value to float, handling NaN/None/bad strings safely."""
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (ValueError, TypeError):
        return default


class Command(BaseCommand):
    help = "Import salary CSV into database using fast bulk operations"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to CSV file")
        parser.add_argument(
            "--batch-size", type=int, default=5000,
            help="Number of rows per bulk_create batch (default: 5000)"
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        batch_size = kwargs["batch_size"]

        self.stdout.write(self.style.SUCCESS("Reading CSV file..."))
        df = pd.read_csv(file_path, low_memory=False)

        # Drop rows with no usable Id -- can't create a user/record without one
        df = df[df["Id"].notna()]
        df["Id"] = df["Id"].astype(int)

        # ---------------------------------------------------------
        # STEP 1: Build unique employees and bulk_create Users
        # ---------------------------------------------------------
        self.stdout.write("Preparing unique employee list...")

        unique_employees = df.drop_duplicates(subset="Id")[["Id", "EmployeeName"]]

        existing_ids = set(
            User.objects.filter(
                employee_id__in=unique_employees["Id"].tolist()
            ).values_list("employee_id", flat=True)
        )

        new_users = [
            User(
                employee_id=int(row["Id"]),
                email=f"user_{int(row['Id'])}@vanpre.com",
                full_name=str(row["EmployeeName"]).strip(),
                role="employee",
            )
            for _, row in unique_employees.iterrows()
            if int(row["Id"]) not in existing_ids
        ]

        self.stdout.write(f"Creating {len(new_users)} new user records...")
        with transaction.atomic():
            User.objects.bulk_create(new_users, batch_size=batch_size, ignore_conflicts=True)

        # ---------------------------------------------------------
        # STEP 2: Build employee_id -> user_id lookup in ONE query
        # ---------------------------------------------------------
        self.stdout.write("Building employee_id -> user_id map...")
        id_to_user_id = dict(
            User.objects.filter(
                employee_id__in=df["Id"].unique().tolist()
            ).values_list("employee_id", "id")
        )

        # ---------------------------------------------------------
        # STEP 3: Build VanpreSalary objects, skipping employee_ids that
        # already have a salary record (makes this script safe to
        # re-run on an updated CSV -- e.g. one with a few new hires added
        # -- without duplicating the employees that were already imported)
        # ---------------------------------------------------------
        self.stdout.write("Checking for already-imported salary records...")
        existing_salary_ids = set(
            VanpreSalary.objects.filter(
                employee_id__in=df["Id"].unique().tolist()
            ).values_list("employee_id", flat=True)
        )

        self.stdout.write("Preparing salary records...")

        salary_objects = []
        skipped = 0
        already_imported = 0

        for _, row in df.iterrows():
            employee_id = int(row["Id"])

            if employee_id in existing_salary_ids:
                already_imported += 1
                continue

            user_id = id_to_user_id.get(employee_id)

            if user_id is None:
                skipped += 1
                continue

            try:
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
            except Exception as e:
                skipped += 1
                self.stdout.write(self.style.WARNING(f"Skipped row (Id={employee_id}): {e}"))

        self.stdout.write(f"Bulk inserting {len(salary_objects)} NEW salary records "
                           f"in batches of {batch_size} "
                           f"({already_imported} rows already existed and were skipped)...")

        with transaction.atomic():
            VanpreSalary.objects.bulk_create(salary_objects, batch_size=batch_size)

        self.stdout.write(self.style.SUCCESS(
            f"Import completed! Inserted: {len(salary_objects)}, "
            f"Already imported (skipped): {already_imported}, Errors (skipped): {skipped}"
        ))
