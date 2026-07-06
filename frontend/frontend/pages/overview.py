import reflex as rx
from frontend.state import State
from frontend.components.layout import page_shell


def stat_card(label, value, value_color="#1a1a1a"):
    return rx.box(
        rx.text(label, font_size="12px", color="#8a8a85", margin_bottom="6px"),
        rx.text(value, font_size="24px", font_weight="600", color=value_color),
        background="#faf9f6",
        border="0.5px solid #ececE5",
        border_radius="12px",
        padding="1.1rem 1.25rem",
        width="100%",
    )


def employee_overview():
    record = State.my_latest_record
    return rx.vstack(
        rx.heading(
            "Welcome back" + rx.cond(State.user_full_name != "", ", " + State.user_full_name, ""),
            size="6", color="#1a1a1a", margin_bottom="4px",
        ),
        rx.text(
            record["job_title"], color="#8a8a85", font_size="14px", margin_bottom="24px",
        ),
        rx.grid(
            stat_card("Base pay", record["base_pay_display"]),
            stat_card("Overtime pay", record["overtime_pay_display"]),
            stat_card("Total pay", record["total_pay_display"], "#7F77DD"),
            columns="3", spacing="4", width="100%",
        ),
        rx.box(
            rx.hstack(
                rx.icon("sparkles", size=16, color="#7F77DD"),
                rx.text(
                    "Want to see how your pay compares or estimate future earnings?",
                    font_size="13px", color="#5a5a55",
                ),
                spacing="2", align="center",
            ),
            rx.link(
                "Go to Predict \u2192", href="/predict",
                color="#7F77DD", font_size="13px", font_weight="500", margin_top="8px",
            ),
            background="#f5f4fb", border="0.5px solid #e5e3f7",
            border_radius="10px", padding="1rem 1.25rem", margin_top="24px",
        ),
        width="100%", align="start",
    )


def admin_overview():
    return rx.vstack(
        rx.heading("Overview", size="6", color="#1a1a1a", margin_bottom="4px"),
        rx.text("Live snapshot of all employee records", color="#8a8a85", font_size="14px", margin_bottom="24px"),
        rx.grid(
            stat_card("Total employees", State.salary_total_count.to_string(), "#1a1a1a"),
            stat_card("Top earners shown", State.salary_records.length().to_string()),
            columns="2", spacing="4", width="100%", margin_bottom="28px",
        ),
        rx.heading("Top earners", size="4", color="#1a1a1a", margin_bottom="12px"),
        rx.box(
            rx.hstack(
                rx.text("Name", width="220px", font_size="12px", color="#8a8a85", font_weight="500"),
                rx.text("Job title", width="280px", font_size="12px", color="#8a8a85", font_weight="500"),
                rx.text("Year", width="80px", font_size="12px", color="#8a8a85", font_weight="500"),
                rx.text("Total pay", font_size="12px", color="#8a8a85", font_weight="500"),
                padding="10px 14px",
                border_bottom="0.5px solid #ececE5",
                width="100%",
            ),
            rx.foreach(
                State.salary_records,
                lambda rec: rx.hstack(
                    rx.text(rec["employee_name"], width="220px", font_size="13px", color="#1a1a1a"),
                    rx.text(rec["job_title"], width="280px", font_size="13px", color="#6b6b66"),
                    rx.text(rec["year"].to_string(), width="80px", font_size="13px", color="#6b6b66"),
                    rx.text(rec["total_pay_display"], font_size="13px", color="#7F77DD", font_weight="500"),
                    padding="10px 14px",
                    border_bottom="0.5px solid #f2f1eb",
                    width="100%",
                    _hover={"background": "#faf9f6"},
                ),
            ),
            background="white",
            border="0.5px solid #ececE5",
            border_radius="12px",
            width="100%",
            overflow="hidden",
        ),
        width="100%", align="start",
    )


def overview():
    return page_shell(
        rx.cond(
            State.dashboard_loading,
            rx.text("Loading...", color="#8a8a85"),
            rx.cond(
                State.dashboard_error != "",
                rx.text(State.dashboard_error, color="#d64545"),
                rx.cond(State.is_admin, admin_overview(), employee_overview()),
            ),
        ),
    )
