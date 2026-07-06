import reflex as rx
from frontend.state import State

FONT = "'Space Grotesk', sans-serif"


def nav_item(icon, label, href, active_route):
    is_active = State.router.page.path == active_route
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=16),
            rx.text(label, font_size="13px"),
            spacing="3", align="center",
            padding="9px 14px",
            border_radius="8px",
            width="100%",
            color=rx.cond(is_active, "#1a1a1a", "#6b6b66"),
            background=rx.cond(is_active, "#f0efe9", "transparent"),
            font_weight=rx.cond(is_active, "500", "400"),
            _hover={"background": "#f6f5f0"},
            transition="all 0.15s ease",
        ),
        href=href,
        width="100%",
        underline="none",
    )


def sidebar():
    return rx.vstack(
        rx.hstack(
            rx.image(src="/logo_icon_v2.png", width="26px", height="26px", object_fit="contain"),
            rx.text("Vanpre", font_weight="600", font_size="15px", color="#1a1a1a"),
            spacing="2", align="center",
            padding="0 14px", margin_bottom="28px",
        ),
        nav_item("layout-dashboard", "Overview", "/overview", "/overview"),
        rx.cond(
            State.is_admin,
            nav_item("bar-chart-3", "Analysis & trends", "/analysis", "/analysis"),
        ),
        nav_item("sparkles", "Predict", "/predict", "/predict"),
        rx.cond(
            State.is_admin,
            nav_item("users", "Employees", "/employees", "/employees"),
        ),
        rx.spacer(),
        rx.box(
            rx.hstack(
                rx.box(
                    rx.text(
                        rx.cond(State.user_full_name != "", State.user_full_name, State.user_email),
                        font_size="12px", font_weight="500", color="#1a1a1a",
                    ),
                    rx.text(State.user_role, font_size="11px", color="#9a9a94", text_transform="capitalize"),
                ),
                spacing="2", align="center", padding="0 14px", margin_bottom="10px",
            ),
        ),
        width="220px",
        height="100vh",
        padding="20px 12px",
        background="#fafaf7",
        border_right="0.5px solid #ececE5",
        position="fixed",
        left="0", top="0",
        font_family=FONT,
        spacing="1",
        align="start",
    )


def page_shell(*content):
    return rx.hstack(
        sidebar(),
        rx.box(
            rx.hstack(
                rx.spacer(),
                rx.button(
                    rx.icon("log-out", size=14),
                    "Log out",
                    on_click=State.logout,
                    background="transparent", color="#6b6b66",
                    border="0.5px solid #e5e3dc", font_family=FONT,
                    font_size="13px", _hover={"background": "#f6f5f0"},
                ),
                width="100%", padding="20px 32px 0",
            ),
            rx.box(
                *content,
                padding="12px 32px 40px",
                width="100%",
            ),
            margin_left="220px",
            width="calc(100% - 220px)",
            min_height="100vh",
            background="white",
        ),
        width="100%",
        align="start",
        font_family=FONT,
        background="white",
    )
