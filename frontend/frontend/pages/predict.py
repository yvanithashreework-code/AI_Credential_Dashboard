import reflex as rx
from frontend.state import State
from frontend.components.layout import page_shell


def model_description_card():
    return rx.box(
        rx.text("About this model", font_size="12px", color="#8a8a85", margin_bottom="14px", letter_spacing="0.3px"),
        rx.heading(State.model_name, size="4", color="#1a1a1a", margin_bottom="4px"),
        rx.text(State.model_type, font_size="12px", color="#7F77DD", margin_bottom="16px"),
        rx.vstack(
            rx.box(
                rx.text("WHAT IT DOES", font_size="10px", color="#a3a39e", letter_spacing="0.5px", margin_bottom="4px"),
                rx.text(State.model_what, font_size="13px", color="#3a3a38", line_height="1.5"),
            ),
            rx.box(
                rx.text("ACCURACY", font_size="10px", color="#a3a39e", letter_spacing="0.5px", margin_bottom="4px"),
                rx.text(State.model_accuracy, font_size="13px", color="#3a3a38"),
            ),
            rx.box(
                rx.text("INPUT FEATURES", font_size="10px", color="#a3a39e", letter_spacing="0.5px", margin_bottom="4px"),
                rx.text(State.model_features, font_size="13px", color="#3a3a38"),
            ),
            rx.box(
                rx.hstack(
                    rx.icon("info", size=13, color="#a3a39e"),
                    rx.text(State.model_note, font_size="12px", color="#8a8a85", line_height="1.5"),
                    spacing="2", align="start",
                ),
                background="#faf9f6", border_radius="8px", padding="10px 12px", margin_top="6px",
            ),
            spacing="4", align="start",
        ),
        background="white",
        border="0.5px solid #ececE5",
        border_radius="12px",
        padding="1.5rem",
        width="100%",
    )


def prediction_form():
    return rx.box(
        rx.heading("Predict", size="5", color="#1a1a1a", margin_bottom="4px"),
        rx.text("Estimate pay for any job title and year.", font_size="13px", color="#8a8a85", margin_bottom="20px"),
        rx.cond(
            State.is_admin,
            rx.hstack(
                rx.button(
                    "Salary amount",
                    on_click=lambda: State.set_predict_model("salary"),
                    background=rx.cond(State.predict_model == "salary", "#7F77DD", "transparent"),
                    color=rx.cond(State.predict_model == "salary", "white", "#6b6b66"),
                    border="0.5px solid #ececE5", font_size="13px",
                ),
                rx.button(
                    "Pay band",
                    on_click=lambda: State.set_predict_model("band"),
                    background=rx.cond(State.predict_model == "band", "#7F77DD", "transparent"),
                    color=rx.cond(State.predict_model == "band", "white", "#6b6b66"),
                    border="0.5px solid #ececE5", font_size="13px",
                ),
                spacing="2", margin_bottom="20px",
            ),
        ),
        rx.text("Job title", font_size="12px", color="#5a5a55", margin_bottom="6px"),
        rx.input(
            placeholder="e.g. POLICE OFFICER 3",
            value=State.predict_job_title,
            on_change=State.set_predict_job_title,
            background="#faf9f6", border="0.5px solid #e5e3dc",
            width="100%", margin_bottom="16px",
        ),
        rx.text("Year", font_size="12px", color="#5a5a55", margin_bottom="6px"),
        rx.input(
            value=State.predict_year,
            on_change=State.set_predict_year,
            background="#faf9f6", border="0.5px solid #e5e3dc",
            width="150px", margin_bottom="22px",
        ),
        rx.button(
            "Run prediction",
            on_click=State.run_salary_prediction,
            background="#7F77DD", color="white", font_weight="500",
            _hover={"background": "#8f88e5"},
        ),
        rx.cond(
            State.predict_error != "",
            rx.text(State.predict_error, color="#d64545", font_size="13px", margin_top="14px"),
        ),
        rx.cond(
            State.predict_result != "",
            rx.box(
                rx.text("Result", font_size="11px", color="#8a8a85", margin_bottom="4px"),
                rx.text(State.predict_result, font_size="22px", font_weight="600", color="#7F77DD"),
                background="#f5f4fb", border="0.5px solid #e5e3f7",
                border_radius="10px", padding="14px 18px", margin_top="18px",
            ),
        ),
        background="white",
        border="0.5px solid #ececE5",
        border_radius="12px",
        padding="1.5rem",
        width="100%",
    )


def predict():
    return page_shell(
        rx.heading("Predict", size="6", color="#1a1a1a", margin_bottom="4px"),
        rx.text("Run trained ML models against any job title and year.", color="#8a8a85", font_size="14px", margin_bottom="24px"),
        rx.grid(
            prediction_form(),
            model_description_card(),
            columns="2", spacing="5", width="100%",
        ),
    )
