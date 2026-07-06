import reflex as rx
from frontend.state import State
from frontend.components.layout import page_shell


def section_card(*content, border_color="#ececE5", **props):
    return rx.box(
        *content,
        background="white", border=f"0.5px solid {border_color}",
        border_radius="12px", padding="1.5rem", width="100%",
        **props,
    )


def search_tab():
    return section_card(
        rx.heading("Salary check", size="4", color="#1a1a1a", margin_bottom="4px"),
        rx.text("Search for an employee by name.", font_size="13px", color="#8a8a85", margin_bottom="16px"),
        rx.hstack(
            rx.input(
                placeholder="Employee name",
                value=State.search_query,
                on_change=State.set_search_query,
                background="#faf9f6", border="0.5px solid #e5e3dc",
                width="100%",
            ),
            rx.button(
                "Search", on_click=State.search_employees,
                background="#7F77DD", color="white", font_weight="500",
                _hover={"background": "#8f88e5"},
            ),
            spacing="3", width="100%", margin_bottom="16px",
        ),
        rx.cond(
            State.search_error != "",
            rx.text(State.search_error, color="#d64545", font_size="13px", margin_bottom="10px"),
        ),
        rx.cond(
            State.search_results.length() > 0,
            rx.box(
                rx.foreach(
                    State.search_results,
                    lambda rec: rx.hstack(
                        rx.text(rec["employee_name"], width="200px", font_size="13px", color="#1a1a1a"),
                        rx.text(rec["job_title"], width="240px", font_size="13px", color="#6b6b66"),
                        rx.text(rec["year"].to_string(), width="70px", font_size="13px", color="#6b6b66"),
                        rx.text(rec["total_pay_display"], font_size="13px", color="#7F77DD", font_weight="500"),
                        padding="10px 4px",
                        border_bottom="0.5px solid #f2f1eb",
                        width="100%",
                    ),
                ),
                width="100%",
            ),
        ),
        margin_bottom="20px",
    )


def add_employee_tab():
    return section_card(
        rx.heading("Add employee", size="4", color="#1a1a1a", margin_bottom="4px"),
        rx.text("Writes a new employee straight into the live database.", font_size="13px", color="#8a8a85", margin_bottom="16px"),
        rx.hstack(
            rx.input(placeholder="Full name", value=State.new_emp_full_name, on_change=State.set_new_emp_full_name, background="#faf9f6", border="0.5px solid #e5e3dc"),
            rx.input(placeholder="Job title", value=State.new_emp_job_title, on_change=State.set_new_emp_job_title, background="#faf9f6", border="0.5px solid #e5e3dc"),
            rx.input(placeholder="Year", value=State.new_emp_year, on_change=State.set_new_emp_year, background="#faf9f6", border="0.5px solid #e5e3dc", width="110px"),
            spacing="3", width="100%", margin_bottom="12px",
        ),
        rx.hstack(
            rx.input(placeholder="Base pay", value=State.new_emp_base_pay, on_change=State.set_new_emp_base_pay, background="#faf9f6", border="0.5px solid #e5e3dc"),
            rx.input(placeholder="Overtime pay", value=State.new_emp_overtime_pay, on_change=State.set_new_emp_overtime_pay, background="#faf9f6", border="0.5px solid #e5e3dc"),
            rx.input(placeholder="Other pay", value=State.new_emp_other_pay, on_change=State.set_new_emp_other_pay, background="#faf9f6", border="0.5px solid #e5e3dc"),
            rx.input(placeholder="Benefits", value=State.new_emp_benefits, on_change=State.set_new_emp_benefits, background="#faf9f6", border="0.5px solid #e5e3dc"),
            spacing="3", width="100%", margin_bottom="16px",
        ),
        rx.button("Add employee", on_click=State.add_employee, background="#5DCAA5", color="white", font_weight="500", _hover={"background": "#4fb894"}),
        rx.cond(State.new_emp_error != "", rx.text(State.new_emp_error, color="#d64545", font_size="13px", margin_top="12px")),
        rx.cond(State.new_emp_result != "", rx.text(State.new_emp_result, color="#3d9b7a", font_weight="500", font_size="13px", margin_top="12px")),
        margin_bottom="20px",
    )


def delete_employee_tab():
    return section_card(
        rx.heading("Remove employee", size="4", color="#c23b3b", margin_bottom="4px"),
        rx.text(
            "Permanently deletes this employee's account and salary record. This cannot be undone.",
            font_size="13px", color="#8a8a85", margin_bottom="16px",
        ),
        rx.hstack(
            rx.input(
                placeholder="Employee ID",
                value=State.delete_emp_id,
                on_change=State.set_delete_emp_id,
                background="#faf9f6", border="0.5px solid #e5e3dc",
            ),
            rx.button(
                "Delete employee", on_click=State.delete_employee,
                background="#e05a5a", color="white", font_weight="500",
                _hover={"background": "#cc4f4f"},
            ),
            spacing="3", width="100%",
        ),
        rx.cond(State.delete_emp_error != "", rx.text(State.delete_emp_error, color="#d64545", font_size="13px", margin_top="12px")),
        rx.cond(State.delete_emp_result != "", rx.text(State.delete_emp_result, color="#3d9b7a", font_weight="500", font_size="13px", margin_top="12px")),
        border_color="#f5d5d5",
    )


def employees():
    return page_shell(
        rx.heading("Employees", size="6", color="#1a1a1a", margin_bottom="4px"),
        rx.text("Search, add, and remove employee records.", color="#8a8a85", font_size="14px", margin_bottom="24px"),
        search_tab(),
        add_employee_tab(),
        delete_employee_tab(),
    )
