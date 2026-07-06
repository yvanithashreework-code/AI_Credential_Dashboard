"""
state.py

Shared application state for the Reflex frontend. Holds the logged-in
user's JWT token and profile info, and talks to the Django REST API.

IMPORTANT: change API_BASE_URL to your deployed backend URL once this
moves off localhost.
"""

import reflex as rx
import requests

API_BASE_URL = "http://127.0.0.1:8000/api"


class State(rx.State):
    # Auth / session
    access_token: str = ""
    refresh_token: str = ""
    user_email: str = ""
    user_full_name: str = ""
    user_role: str = ""
    user_employee_id: str = ""

    # Login form inputs
    login_email: str = ""
    login_password: str = ""
    login_error: str = ""

    # Dashboard data
    salary_records: list[dict] = []
    salary_total_count: int = 0
    dashboard_error: str = ""
    dashboard_loading: bool = False

    # Analytics (admin only)
    analytics_loading: bool = False
    analytics_error: str = ""
    analytics_total_employees: int = 0
    analytics_avg_total_pay: float = 0.0
    analytics_distinct_job_titles: int = 0
    analytics_anomaly_count: int = 0
    analytics_avg_pay_by_year: list[dict] = []
    analytics_top_job_titles: list[dict] = []
    analytics_band_distribution: list[dict] = []

    # Predict page model selector (admin can choose; employee always uses "salary")
    predict_model: str = "salary"

    # Prediction form
    predict_job_title: str = ""
    predict_year: str = "2026"
    predict_result: str = ""
    predict_error: str = ""

    # Anomaly check form (admin only)
    anomaly_job_title: str = ""
    anomaly_base_pay: str = ""
    anomaly_overtime_pay: str = ""
    anomaly_other_pay: str = ""
    anomaly_total_pay: str = ""
    anomaly_year: str = "2026"
    anomaly_result: str = ""
    anomaly_error: str = ""

    # Add employee form (admin only)
    new_emp_full_name: str = ""
    new_emp_job_title: str = ""
    new_emp_base_pay: str = ""
    new_emp_overtime_pay: str = ""
    new_emp_other_pay: str = ""
    new_emp_benefits: str = ""
    new_emp_year: str = "2026"
    new_emp_result: str = ""
    new_emp_error: str = ""

    # Delete employee form (admin only)
    delete_emp_id: str = ""
    delete_emp_result: str = ""
    delete_emp_error: str = ""

    # Employee search / salary check (admin only)
    search_query: str = ""
    search_results: list[dict] = []
    search_loading: bool = False
    search_error: str = ""

    @rx.var
    def is_logged_in(self) -> bool:
        return self.access_token != ""

    @rx.var
    def is_admin(self) -> bool:
        return self.user_role == "admin"

    @rx.var
    def model_name(self) -> str:
        return "Salary band classifier" if self.predict_model == "band" else "Salary regressor"

    @rx.var
    def model_type(self) -> str:
        return "Classification \u00b7 Random Forest" if self.predict_model == "band" else "Regression \u00b7 Random Forest"

    @rx.var
    def model_what(self) -> str:
        if self.predict_model == "band":
            return ("Predicts whether a role falls into a Low, Mid, or High pay band, "
                    "based on percentile cutoffs from the actual dataset.")
        return "Estimates the expected total pay for a given job title and year."

    @rx.var
    def model_accuracy(self) -> str:
        if self.predict_model == "band":
            return "65% accuracy (vs. 33% random guessing across 3 classes)"
        return "R\u00b2 = 0.53 on held-out test data"

    @rx.var
    def model_features(self) -> str:
        return "Job title (frequency-encoded), year"

    @rx.var
    def model_note(self) -> str:
        if self.predict_model == "band":
            return ("Bands are data-driven, not fixed dollar amounts \u2014 they reflect "
                    "this dataset's own pay distribution.")
        return ("Job title and year alone explain about half of pay variation. The rest "
                "depends on individual factors this dataset doesn't capture "
                "(seniority, performance, tenure).")

    @rx.var
    def my_latest_record(self) -> dict:
        """Convenience accessor for the employee's own (single) salary record."""
        if self.salary_records:
            return self.salary_records[0]
        return {}

    def set_login_email(self, value: str):
        self.login_email = value

    def set_login_password(self, value: str):
        self.login_password = value

    def set_predict_job_title(self, value: str):
        self.predict_job_title = value

    def set_predict_year(self, value: str):
        self.predict_year = value

    def set_predict_model(self, value: str):
        self.predict_model = value
        self.predict_result = ""
        self.predict_error = ""

    def set_anomaly_job_title(self, value: str):
        self.anomaly_job_title = value

    def set_anomaly_base_pay(self, value: str):
        self.anomaly_base_pay = value

    def set_anomaly_overtime_pay(self, value: str):
        self.anomaly_overtime_pay = value

    def set_anomaly_other_pay(self, value: str):
        self.anomaly_other_pay = value

    def set_anomaly_total_pay(self, value: str):
        self.anomaly_total_pay = value

    def set_anomaly_year(self, value: str):
        self.anomaly_year = value

    def set_new_emp_full_name(self, value: str):
        self.new_emp_full_name = value

    def set_new_emp_job_title(self, value: str):
        self.new_emp_job_title = value

    def set_new_emp_base_pay(self, value: str):
        self.new_emp_base_pay = value

    def set_new_emp_overtime_pay(self, value: str):
        self.new_emp_overtime_pay = value

    def set_new_emp_other_pay(self, value: str):
        self.new_emp_other_pay = value

    def set_new_emp_benefits(self, value: str):
        self.new_emp_benefits = value

    def set_new_emp_year(self, value: str):
        self.new_emp_year = value

    def set_delete_emp_id(self, value: str):
        self.delete_emp_id = value

    def set_search_query(self, value: str):
        self.search_query = value

    def login(self):
        """Call the Django login endpoint and store the returned token + user info."""
        self.login_error = ""

        if not self.login_email or not self.login_password:
            self.login_error = "Enter your email and password."
            return

        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/login/",
                json={"email": self.login_email, "password": self.login_password},
                timeout=10,
            )
        except requests.exceptions.ConnectionError:
            self.login_error = "Couldn't reach the server. Is the Django backend running?"
            return

        if response.status_code != 200:
            self.login_error = "Invalid email or password."
            return

        data = response.json()
        self.access_token = data["access"]
        self.refresh_token = data["refresh"]
        self.user_email = data["user"]["email"]
        self.user_full_name = data["user"]["full_name"] or ""
        self.user_role = data["user"]["role"]
        self.user_employee_id = str(data["user"]["employee_id"] or "")

        # Clear the password from state once logged in -- no reason to keep it around
        self.login_password = ""

        return rx.redirect("/overview")

    def logout(self):
        self.access_token = ""
        self.refresh_token = ""
        self.user_email = ""
        self.user_full_name = ""
        self.user_role = ""
        self.user_employee_id = ""
        self.salary_records = []
        self.predict_job_title = ""
        self.predict_year = "2026"
        self.predict_result = ""
        self.predict_error = ""
        self.anomaly_job_title = ""
        self.anomaly_base_pay = ""
        self.anomaly_overtime_pay = ""
        self.anomaly_other_pay = ""
        self.anomaly_total_pay = ""
        self.anomaly_year = "2026"
        self.anomaly_result = ""
        self.anomaly_error = ""
        self.new_emp_full_name = ""
        self.new_emp_job_title = ""
        self.new_emp_base_pay = ""
        self.new_emp_overtime_pay = ""
        self.new_emp_other_pay = ""
        self.new_emp_benefits = ""
        self.new_emp_year = "2026"
        self.new_emp_result = ""
        self.new_emp_error = ""
        return rx.redirect("/login")

    def auth_headers(self) -> dict:
        """Helper for other state methods to attach the JWT to API calls."""
        return {"Authorization": f"Bearer {self.access_token}"}

    def require_login(self):
        if not self.is_logged_in:
            return rx.redirect("/login")

    def require_admin(self):
        if not self.is_logged_in:
            return rx.redirect("/login")
        if not self.is_admin:
            return rx.redirect("/overview")

    def load_dashboard(self):
        """
        Called when the dashboard page loads. Redirects to /login if not
        authenticated, otherwise fetches the appropriate data for the
        user's role (own record for employees, top earners for admins).
        """
        if not self.is_logged_in:
            return rx.redirect("/login")

        self.dashboard_error = ""
        self.dashboard_loading = True

        try:
            if self.is_admin:
                response = requests.get(
                    f"{API_BASE_URL}/salary/admin/",
                    headers=self.auth_headers(),
                    params={"limit": 20},
                    timeout=15,
                )
            else:
                response = requests.get(
                    f"{API_BASE_URL}/salary/employee/",
                    headers=self.auth_headers(),
                    timeout=15,
                )
        except requests.exceptions.ConnectionError:
            self.dashboard_error = "Couldn't reach the server."
            self.dashboard_loading = False
            return

        self.dashboard_loading = False

        if response.status_code == 401:
            # Token expired or invalid -- send back to login
            return self.logout()

        if response.status_code != 200:
            self.dashboard_error = "Couldn't load salary data."
            return

        data = response.json()
        results = data.get("results", [])

        # Add pre-formatted currency strings so pages can display
        # $167,411.19 instead of raw floats like 167411.19
        for rec in results:
            for field in ["base_pay", "overtime_pay", "other_pay", "total_pay", "total_pay_benefits"]:
                if field in rec and rec[field] is not None:
                    rec[f"{field}_display"] = f"${rec[field]:,.2f}"

        self.salary_records = results
        self.salary_total_count = data.get("count", 0)

    def load_analytics(self):
        """Admin-only. Fetches dataset-wide stats for the Analysis & trends page."""
        if not self.is_logged_in:
            return rx.redirect("/login")
        if not self.is_admin:
            return rx.redirect("/overview")

        self.analytics_error = ""
        self.analytics_loading = True

        try:
            response = requests.get(
                f"{API_BASE_URL}/analytics/admin/",
                headers=self.auth_headers(),
                timeout=30,
            )
        except requests.exceptions.ConnectionError:
            self.analytics_error = "Couldn't reach the server."
            self.analytics_loading = False
            return

        self.analytics_loading = False

        if response.status_code == 401:
            return self.logout()

        if response.status_code != 200:
            self.analytics_error = "Couldn't load analytics."
            return

        data = response.json()
        self.analytics_total_employees = data.get("total_employees", 0)
        self.analytics_avg_total_pay = data.get("avg_total_pay", 0.0)
        self.analytics_distinct_job_titles = data.get("distinct_job_titles", 0)
        self.analytics_anomaly_count = data.get("anomaly_count") or 0
        self.analytics_avg_pay_by_year = data.get("avg_pay_by_year", [])
        self.analytics_top_job_titles = data.get("top_job_titles_by_avg_pay", [])

        band_dist = data.get("band_distribution")
        if band_dist:
            self.analytics_band_distribution = [
                {"name": "Low", "value": band_dist.get("Low", 0)},
                {"name": "Mid", "value": band_dist.get("Mid", 0)},
                {"name": "High", "value": band_dist.get("High", 0)},
            ]

    def run_salary_prediction(self):
        """Calls the salary regressor or band classifier, based on predict_model."""
        self.predict_error = ""
        self.predict_result = ""

        if not self.predict_job_title or not self.predict_year:
            self.predict_error = "Enter a job title and year."
            return

        try:
            year = int(self.predict_year)
        except ValueError:
            self.predict_error = "Year must be a number."
            return

        endpoint = "predict/band/" if self.predict_model == "band" else "predict/salary/"

        try:
            response = requests.post(
                f"{API_BASE_URL}/{endpoint}",
                headers=self.auth_headers(),
                json={"job_title": self.predict_job_title, "year": year},
                timeout=15,
            )
        except requests.exceptions.ConnectionError:
            self.predict_error = "Couldn't reach the server."
            return

        if response.status_code != 200:
            self.predict_error = "Prediction failed. Try a different job title."
            return

        data = response.json()
        if self.predict_model == "band":
            band = data.get("predicted_band", "Unknown")
            confidence = data.get("confidence", {})
            conf_pct = confidence.get(band, 0) * 100
            self.predict_result = f"{band} pay band ({conf_pct:.0f}% confidence)"
        else:
            predicted = data.get("predicted_total_pay", 0)
            self.predict_result = f"${predicted:,.2f}"

    def run_anomaly_check(self):
        """Calls the admin-only anomaly detection endpoint with the form's pay data."""
        self.anomaly_error = ""
        self.anomaly_result = ""

        required = [
            self.anomaly_job_title, self.anomaly_base_pay, self.anomaly_overtime_pay,
            self.anomaly_other_pay, self.anomaly_total_pay, self.anomaly_year
        ]
        if not all(required):
            self.anomaly_error = "Fill in all fields."
            return

        try:
            payload = {
                "job_title": self.anomaly_job_title,
                "base_pay": float(self.anomaly_base_pay),
                "overtime_pay": float(self.anomaly_overtime_pay),
                "other_pay": float(self.anomaly_other_pay),
                "total_pay": float(self.anomaly_total_pay),
                "year": int(self.anomaly_year),
            }
        except ValueError:
            self.anomaly_error = "Pay fields and year must be numbers."
            return

        try:
            response = requests.post(
                f"{API_BASE_URL}/predict/anomaly/",
                headers=self.auth_headers(),
                json=payload,
                timeout=15,
            )
        except requests.exceptions.ConnectionError:
            self.anomaly_error = "Couldn't reach the server."
            return

        if response.status_code == 403:
            self.anomaly_error = "Admin access required."
            return

        if response.status_code != 200:
            self.anomaly_error = "Check failed. Verify the inputs."
            return

        data = response.json()
        if data.get("is_anomaly"):
            self.anomaly_result = f"Flagged as unusual (score: {data.get('anomaly_score')})"
        else:
            self.anomaly_result = f"Looks normal (score: {data.get('anomaly_score')})"

    def add_employee(self):
        """Submits the new-employee form. Writes straight to AWS RDS via the API."""
        self.new_emp_error = ""
        self.new_emp_result = ""

        required = [
            self.new_emp_full_name, self.new_emp_job_title, self.new_emp_base_pay,
            self.new_emp_overtime_pay, self.new_emp_other_pay, self.new_emp_benefits,
            self.new_emp_year
        ]
        if not all(required):
            self.new_emp_error = "Fill in all fields."
            return

        try:
            payload = {
                "full_name": self.new_emp_full_name,
                "job_title": self.new_emp_job_title,
                "base_pay": float(self.new_emp_base_pay),
                "overtime_pay": float(self.new_emp_overtime_pay),
                "other_pay": float(self.new_emp_other_pay),
                "benefits": float(self.new_emp_benefits),
                "year": int(self.new_emp_year),
            }
        except ValueError:
            self.new_emp_error = "Pay fields and year must be numbers."
            return

        try:
            response = requests.post(
                f"{API_BASE_URL}/employees/add/",
                headers=self.auth_headers(),
                json=payload,
                timeout=15,
            )
        except requests.exceptions.ConnectionError:
            self.new_emp_error = "Couldn't reach the server."
            return

        if response.status_code == 403:
            self.new_emp_error = "Admin access required."
            return

        if response.status_code != 201:
            self.new_emp_error = "Couldn't add employee. Check the inputs."
            return

        data = response.json()
        self.new_emp_result = (
            f"Added employee #{data['employee_id']} ({data['email']}, "
            f"password: {data['default_password']})"
        )

        # Clear the form
        self.new_emp_full_name = ""
        self.new_emp_job_title = ""
        self.new_emp_base_pay = ""
        self.new_emp_overtime_pay = ""
        self.new_emp_other_pay = ""
        self.new_emp_benefits = ""
        self.new_emp_year = "2026"

        # Refresh the dashboard so the new total count and (if they rank
        # high enough) the new employee show up immediately
        self.load_dashboard()

        # Keep an active search in sync too
        if self.search_query:
            self.search_employees()

    def delete_employee(self):
        """Deletes an employee by ID. Writes straight to AWS RDS via the API."""
        self.delete_emp_error = ""
        self.delete_emp_result = ""

        if not self.delete_emp_id:
            self.delete_emp_error = "Enter an employee ID."
            return

        try:
            emp_id = int(self.delete_emp_id)
        except ValueError:
            self.delete_emp_error = "Employee ID must be a number."
            return

        try:
            response = requests.delete(
                f"{API_BASE_URL}/employees/delete/{emp_id}/",
                headers=self.auth_headers(),
                timeout=15,
            )
        except requests.exceptions.ConnectionError:
            self.delete_emp_error = "Couldn't reach the server."
            return

        if response.status_code == 403:
            self.delete_emp_error = "Admin access required."
            return

        if response.status_code == 404:
            self.delete_emp_error = f"No employee found with ID {emp_id}."
            return

        if response.status_code != 200:
            self.delete_emp_error = "Couldn't delete employee."
            return

        data = response.json()
        self.delete_emp_result = data.get("message", "Employee deleted.")
        self.delete_emp_id = ""

        # Refresh the dashboard so the count and table update immediately
        self.load_dashboard()

        # If a search was active, refresh it too so the deleted employee
        # disappears from the visible list right away instead of looking
        # like the deletion didn't work
        if self.search_query:
            self.search_employees()

    def search_employees(self):
        """Admin-only. Searches employees by name for the salary check tab."""
        self.search_error = ""
        self.search_results = []

        if not self.search_query:
            self.search_error = "Enter a name to search."
            return

        self.search_loading = True

        try:
            response = requests.get(
                f"{API_BASE_URL}/salary/admin/",
                headers=self.auth_headers(),
                params={"search": self.search_query, "limit": 25},
                timeout=15,
            )
        except requests.exceptions.ConnectionError:
            self.search_error = "Couldn't reach the server."
            self.search_loading = False
            return

        self.search_loading = False

        if response.status_code != 200:
            self.search_error = "Search failed."
            return

        data = response.json()
        results = data.get("results", [])
        for rec in results:
            for field in ["base_pay", "overtime_pay", "other_pay", "total_pay", "total_pay_benefits"]:
                if field in rec and rec[field] is not None:
                    rec[f"{field}_display"] = f"${rec[field]:,.2f}"

        self.search_results = results
        if not results:
            self.search_error = f"No employees found matching '{self.search_query}'."        # Refresh the dashboard so the count and table update immediately
        self.load_dashboard()
