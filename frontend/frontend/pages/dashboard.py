import reflex as rx
from frontend.state import State


def predict_panel():
    return rx.box(
        rx.vstack(
            rx.heading("Predict expected pay", size="5", color="cyan"),
            rx.hstack(
                rx.input(
                    placeholder="Job title",
                    value=State.predict_job_title,
                    on_change=State.set_predict_job_title,
                    width="100%",
                ),
                rx.input(
                    placeholder="Year",
                    value=State.predict_year,
                    on_change=State.set_predict_year,
                    width="120px",
                ),
                rx.button("Predict", color_scheme="blue", on_click=State.run_salary_prediction),
                spacing="3",
                width="100%",
            ),
            rx.cond(
                State.predict_error != "",
                rx.text(State.predict_error, color="red", size="2"),
            ),
            rx.cond(
                State.predict_result != "",
                rx.text(
                    "Expected total pay: " + State.predict_result,
                    color="cyan",
                    weight="bold",
                    size="4",
                ),
            ),
            spacing="4",
            align="stretch",
        ),
        background_color="rgba(255,255,255,0.05)",
        border_radius="lg",
        padding="4",
        width="100%",
    )


def employee_content():
    record = State.my_latest_record
    return rx.vstack(
        rx.hstack(
            rx.card(
                rx.vstack(
                    rx.text("Base pay", color="gray", size="2"),
                    rx.heading(record["base_pay"].to_string(), size="6", color="cyan"),
                ),
                width="33%",
            ),
            rx.card(
                rx.vstack(
                    rx.text("Overtime pay", color="gray", size="2"),
                    rx.heading(record["overtime_pay"].to_string(), size="6", color="cyan"),
                ),
                width="33%",
            ),
            rx.card(
                rx.vstack(
                    rx.text("Total pay", color="gray", size="2"),
                    rx.heading(record["total_pay"].to_string(), size="6", color="cyan"),
                ),
                width="33%",
            ),
            spacing="4",
            width="100%",
        ),
        rx.box(height="20px"),
        predict_panel(),
        spacing="4",
        width="100%",
    )


def anomaly_panel():
    return rx.box(
        rx.vstack(
            rx.heading("Check for unusual pay", size="5", color="amber"),
            rx.text(
                "Admin only. Flags whether a pay record looks statistically unusual.",
                color="gray",
                size="2",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Job title",
                    value=State.anomaly_job_title,
                    on_change=State.set_anomaly_job_title,
                ),
                rx.input(
                    placeholder="Year",
                    value=State.anomaly_year,
                    on_change=State.set_anomaly_year,
                    width="100px",
                ),
                spacing="3",
                width="100%",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Base pay",
                    value=State.anomaly_base_pay,
                    on_change=State.set_anomaly_base_pay,
                ),
                rx.input(
                    placeholder="Overtime pay",
                    value=State.anomaly_overtime_pay,
                    on_change=State.set_anomaly_overtime_pay,
                ),
                rx.input(
                    placeholder="Other pay",
                    value=State.anomaly_other_pay,
                    on_change=State.set_anomaly_other_pay,
                ),
                rx.input(
                    placeholder="Total pay",
                    value=State.anomaly_total_pay,
                    on_change=State.set_anomaly_total_pay,
                ),
                spacing="3",
                width="100%",
            ),
            rx.button("Check", color_scheme="amber", on_click=State.run_anomaly_check),
            rx.cond(
                State.anomaly_error != "",
                rx.text(State.anomaly_error, color="red", size="2"),
            ),
            rx.cond(
                State.anomaly_result != "",
                rx.text(State.anomaly_result, color="amber", weight="bold", size="4"),
            ),
            spacing="4",
            align="stretch",
        ),
        background_color="rgba(255,255,255,0.05)",
        border_radius="lg",
        padding="4",
        width="100%",
    )


def add_employee_panel():
    return rx.box(
        rx.vstack(
            rx.heading("Add employee", size="5", color="green"),
            rx.text(
                "Writes a new employee straight into the live database.",
                color="gray",
                size="2",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Full name",
                    value=State.new_emp_full_name,
                    on_change=State.set_new_emp_full_name,
                ),
                rx.input(
                    placeholder="Job title",
                    value=State.new_emp_job_title,
                    on_change=State.set_new_emp_job_title,
                ),
                rx.input(
                    placeholder="Year",
                    value=State.new_emp_year,
                    on_change=State.set_new_emp_year,
                    width="100px",
                ),
                spacing="3",
                width="100%",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Base pay",
                    value=State.new_emp_base_pay,
                    on_change=State.set_new_emp_base_pay,
                ),
                rx.input(
                    placeholder="Overtime pay",
                    value=State.new_emp_overtime_pay,
                    on_change=State.set_new_emp_overtime_pay,
                ),
                rx.input(
                    placeholder="Other pay",
                    value=State.new_emp_other_pay,
                    on_change=State.set_new_emp_other_pay,
                ),
                rx.input(
                    placeholder="Benefits",
                    value=State.new_emp_benefits,
                    on_change=State.set_new_emp_benefits,
                ),
                spacing="3",
                width="100%",
            ),
            rx.button("Add employee", color_scheme="green", on_click=State.add_employee),
            rx.cond(
                State.new_emp_error != "",
                rx.text(State.new_emp_error, color="red", size="2"),
            ),
            rx.cond(
                State.new_emp_result != "",
                rx.text(State.new_emp_result, color="green", weight="bold", size="3"),
            ),
            spacing="4",
            align="stretch",
        ),
        background_color="rgba(255,255,255,0.05)",
        border_radius="lg",
        padding="4",
        width="100%",
    )


def delete_employee_panel():
    return rx.box(
        rx.vstack(
            rx.heading("Remove employee", size="5", color="red"),
            rx.text(
                "Permanently deletes this employee's account and salary record from the live database. This cannot be undone.",
                color="gray",
                size="2",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Employee ID",
                    value=State.delete_emp_id,
                    on_change=State.set_delete_emp_id,
                ),
                rx.button("Delete employee", color_scheme="red", on_click=State.delete_employee),
                spacing="3",
                width="100%",
            ),
            rx.cond(
                State.delete_emp_error != "",
                rx.text(State.delete_emp_error, color="red", size="2"),
            ),
            rx.cond(
                State.delete_emp_result != "",
                rx.text(State.delete_emp_result, color="green", weight="bold", size="3"),
            ),
            spacing="4",
            align="stretch",
        ),
        background_color="rgba(255,255,255,0.05)",
        border_radius="lg",
        padding="4",
        width="100%",
        border="1px solid rgba(255,0,0,0.3)",
    )


def admin_content():
    return rx.vstack(
        rx.card(
            rx.vstack(
                rx.text("Total employee records", color="gray", size="2"),
                rx.heading(State.salary_total_count.to_string(), size="7", color="cyan"),
            ),
            width="100%",
        ),
        rx.box(height="20px"),
        rx.heading("Top earners", size="5", color="cyan"),
        rx.box(
            rx.foreach(
                State.salary_records,
                lambda rec: rx.hstack(
                    rx.text(rec["employee_name"], width="200px", color="white"),
                    rx.text(rec["job_title"], width="250px", color="gray"),
                    rx.text(rec["year"].to_string(), width="80px", color="gray"),
                    rx.text(rec["total_pay"].to_string(), color="cyan"),
                    padding_y="2",
                    border_bottom="1px solid rgba(255,255,255,0.1)",
                    width="100%",
                ),
            ),
            width="100%",
        ),
        rx.box(height="20px"),
        predict_panel(),
        rx.box(height="20px"),
        anomaly_panel(),
        rx.box(height="20px"),
        add_employee_panel(),
        rx.box(height="20px"),
        delete_employee_panel(),
        spacing="4",
        width="100%",
    )


def dashboard():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Salary dashboard", size="7", color="cyan"),
                rx.spacer(),
                rx.button("Logout", color_scheme="red", size="2", on_click=State.logout),
                padding="2",
                border_bottom="1px solid rgba(255,255,255,0.1)",
                width="100%",
            ),
            rx.cond(
                State.dashboard_loading,
                rx.text("Loading...", color="gray"),
            ),
            rx.cond(
                State.dashboard_error != "",
                rx.text(State.dashboard_error, color="red"),
            ),
            rx.cond(
                State.is_admin,
                admin_content(),
                employee_content(),
            ),
            spacing="6",
            width="100%",
        ),
        min_height="100vh",
        background_color="black",
        padding="4",
    )
