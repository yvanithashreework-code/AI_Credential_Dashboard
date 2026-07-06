import reflex as rx
from frontend.state import State

FONT = "'Space Grotesk', sans-serif"

CORNER_NETWORK_SVG = """
<svg width="100%" height="100%" viewBox="0 0 700 520" style="position:absolute; top:0; left:0; pointer-events:none;" aria-hidden="true">
  <defs>
    <radialGradient id="softglowA" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#7F77DD" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#7F77DD" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="softglowB" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#5DCAA5" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#5DCAA5" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <circle cx="620" cy="70" r="210" fill="url(#softglowA)" class="drift-a"/>
  <circle cx="70" cy="450" r="190" fill="url(#softglowB)" class="drift-b"/>
  <g opacity="0.5">
    <circle cx="80" cy="70" r="3" fill="#B7B2EE"/>
    <circle cx="160" cy="40" r="2" fill="#9FDFC9"/>
    <circle cx="130" cy="120" r="2.5" fill="#B7B2EE"/>
    <line x1="80" y1="70" x2="160" y2="40" stroke="#B7B2EE" stroke-width="0.6"/>
    <line x1="160" y1="40" x2="130" y2="120" stroke="#9FDFC9" stroke-width="0.6"/>
    <circle cx="610" cy="450" r="3" fill="#9FDFC9"/>
    <circle cx="660" cy="490" r="2" fill="#B7B2EE"/>
    <circle cx="570" cy="490" r="2.5" fill="#9FDFC9"/>
    <line x1="610" y1="450" x2="660" y2="490" stroke="#9FDFC9" stroke-width="0.6"/>
    <line x1="610" y1="450" x2="570" y2="490" stroke="#B7B2EE" stroke-width="0.6"/>
  </g>
</svg>
<style>
@keyframes drift-a { 0%, 100% { transform: translate(0,0); } 50% { transform: translate(-10px, 8px); } }
@keyframes drift-b { 0%, 100% { transform: translate(0,0); } 50% { transform: translate(8px, -10px); } }
.drift-a { animation: drift-a 10s ease-in-out infinite; }
.drift-b { animation: drift-b 12s ease-in-out infinite; }
</style>
"""


def login():
    return rx.box(
        rx.html(CORNER_NETWORK_SVG),
        rx.center(
            rx.vstack(
                rx.hstack(
                    rx.image(src="/logo_icon_v2.png", width="30px", height="30px", object_fit="contain"),
                    rx.text("Vanpre", font_weight="600", font_size="17px", color="#1a1a1a"),
                    spacing="2", align="center", margin_bottom="32px",
                ),
                rx.box(
                    rx.heading(
                        "Welcome back",
                        font_size="22px", font_weight="600", color="#1a1a1a",
                        text_align="center", margin_bottom="6px",
                    ),
                    rx.text(
                        "Sign in to your salary dashboard",
                        font_size="13px", color="#8a8a85",
                        text_align="center", margin_bottom="28px",
                    ),
                    rx.text("Email", font_size="12px", color="#5a5a55", margin_bottom="6px"),
                    rx.input(
                        placeholder="name@vanpre.com",
                        value=State.login_email,
                        on_change=State.set_login_email,
                        background="#faf9f6", border="0.5px solid #e5e3dc",
                        width="100%", margin_bottom="16px",
                        _focus={"border": "0.5px solid #7F77DD"},
                    ),
                    rx.text("Password", font_size="12px", color="#5a5a55", margin_bottom="6px"),
                    rx.input(
                        placeholder="Enter your password",
                        type="password",
                        value=State.login_password,
                        on_change=State.set_login_password,
                        background="#faf9f6", border="0.5px solid #e5e3dc",
                        width="100%", margin_bottom="22px",
                        _focus={"border": "0.5px solid #7F77DD"},
                    ),
                    rx.cond(
                        State.login_error != "",
                        rx.text(
                            State.login_error, color="#d64545", size="2",
                            text_align="center", margin_bottom="14px",
                        ),
                    ),
                    rx.button(
                        "Sign in",
                        on_click=State.login,
                        width="100%", background="#7F77DD", color="white",
                        font_family=FONT, font_weight="500", padding="11px",
                        _hover={"background": "#8f88e5"},
                    ),
                    rx.text(
                        "No account? ",
                        rx.link("Sign up", href="/signup", color="#7F77DD", font_weight="500"),
                        font_size="12px", color="#8a8a85",
                        text_align="center", margin_top="18px",
                    ),
                    background="white",
                    border="0.5px solid #eceae4",
                    border_radius="14px",
                    padding="2.25rem 2rem",
                    width="360px",
                    box_shadow="0 1px 2px rgba(0,0,0,0.03)",
                ),
                rx.text(
                    "Employee and admin accounts use the same sign-in",
                    font_size="11px", color="#b0b0aa", margin_top="24px",
                ),
                rx.link("Back to Home", href="/", color="#8a8a85", font_size="12px", margin_top="8px"),
                align="center",
            ),
            width="100%", min_height="100vh",
        ),
        background="#ffffff",
        min_height="100vh",
        position="relative",
        overflow="hidden",
        font_family=FONT,
    )
