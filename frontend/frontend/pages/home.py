import reflex as rx

FONT = "'Space Grotesk', sans-serif"

NETWORK_SVG = """
<svg width="100%" height="600" viewBox="0 0 680 600" style="position:absolute; top:0; left:0; pointer-events:none;" aria-hidden="true">
  <defs>
    <radialGradient id="glow1" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#7F77DD" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#7F77DD" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#5DCAA5" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#5DCAA5" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <circle cx="520" cy="90" r="190" fill="url(#glow1)" class="glow-orb-a"/>
  <circle cx="120" cy="440" r="170" fill="url(#glow2)" class="glow-orb-b"/>
  <g opacity="0.55" class="net-cluster">
    <circle cx="430" cy="60" r="3" fill="#AFA9EC"/>
    <circle cx="510" cy="40" r="2" fill="#5DCAA5"/>
    <circle cx="480" cy="110" r="2.5" fill="#AFA9EC"/>
    <circle cx="570" cy="90" r="2" fill="#5DCAA5"/>
    <circle cx="560" cy="150" r="3" fill="#AFA9EC"/>
    <circle cx="620" cy="60" r="2" fill="#5DCAA5"/>
    <circle cx="640" cy="140" r="2.5" fill="#AFA9EC"/>
    <circle cx="500" cy="170" r="2" fill="#5DCAA5"/>
    <line x1="430" y1="60" x2="510" y2="40" stroke="#AFA9EC" stroke-width="0.6"/>
    <line x1="510" y1="40" x2="480" y2="110" stroke="#5DCAA5" stroke-width="0.6"/>
    <line x1="480" y1="110" x2="570" y2="90" stroke="#AFA9EC" stroke-width="0.6"/>
    <line x1="570" y1="90" x2="560" y2="150" stroke="#5DCAA5" stroke-width="0.6"/>
    <line x1="570" y1="90" x2="620" y2="60" stroke="#AFA9EC" stroke-width="0.6"/>
    <line x1="620" y1="60" x2="640" y2="140" stroke="#5DCAA5" stroke-width="0.6"/>
    <line x1="560" y1="150" x2="640" y2="140" stroke="#AFA9EC" stroke-width="0.6"/>
    <line x1="480" y1="110" x2="500" y2="170" stroke="#5DCAA5" stroke-width="0.6"/>
    <line x1="560" y1="150" x2="500" y2="170" stroke="#AFA9EC" stroke-width="0.6"/>
  </g>
  <g opacity="0.4" class="net-cluster-b">
    <circle cx="60" cy="380" r="2.5" fill="#5DCAA5"/>
    <circle cx="130" cy="350" r="2" fill="#AFA9EC"/>
    <circle cx="100" cy="440" r="3" fill="#5DCAA5"/>
    <circle cx="180" cy="420" r="2" fill="#AFA9EC"/>
    <circle cx="50" cy="470" r="2" fill="#5DCAA5"/>
    <line x1="60" y1="380" x2="130" y2="350" stroke="#5DCAA5" stroke-width="0.6"/>
    <line x1="130" y1="350" x2="100" y2="440" stroke="#AFA9EC" stroke-width="0.6"/>
    <line x1="100" y1="440" x2="180" y2="420" stroke="#5DCAA5" stroke-width="0.6"/>
    <line x1="100" y1="440" x2="50" y2="470" stroke="#AFA9EC" stroke-width="0.6"/>
  </g>
</svg>
<style>
@keyframes drift-a {
  0%, 100% { transform: translate(0px, 0px); }
  50% { transform: translate(-12px, 10px); }
}
@keyframes drift-b {
  0%, 100% { transform: translate(0px, 0px); }
  50% { transform: translate(10px, -14px); }
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
.glow-orb-a { animation: drift-a 9s ease-in-out infinite; }
.glow-orb-b { animation: drift-b 11s ease-in-out infinite; }
.net-cluster circle, .net-cluster-b circle { animation: pulse-dot 3.5s ease-in-out infinite; }
</style>
"""

SPARKLINE_SVG = """
<svg width="100%" height="60" viewBox="0 0 240 60" preserveAspectRatio="none">
  <polyline points="0,45 60,38 120,35 180,20 240,8" fill="none" stroke="#7F77DD" stroke-width="2"/>
  <polygon points="0,45 60,38 120,35 180,20 240,8 240,60 0,60" fill="#7F77DD" opacity="0.12"/>
</svg>
"""


def nav_bar():
    return rx.hstack(
        rx.spacer(),
        rx.button(
            "Log in",
            on_click=rx.redirect("/login"),
            background="#f5f5f3", color="#0a0a0c", font_family=FONT,
            font_weight="500", font_size="13px", padding="9px 20px",
            _hover={"background": "#e0e0dc"},
        ),
        width="100%",
        margin_bottom="20px",
        position="relative",
        z_index="1",
    )


def stat(value, label):
    return rx.vstack(
        rx.text(value, font_size="21px", font_weight="600", color="#f5f5f3", font_family=FONT),
        rx.text(label, font_size="12px", color="#79796f"),
        spacing="1", align="start",
    )


def hero():
    return rx.grid(
        rx.vstack(
            rx.image(
                src="/logo_full_v2.png",
                height="110px",
                margin_bottom="32px",
            ),
            rx.hstack(
                rx.icon("cloud", size=13, color="#CECBF6"),
                rx.text("Live on AWS RDS", font_size="12px", color="#CECBF6"),
                spacing="2", align="center",
                background="rgba(127,119,221,0.15)", padding="5px 12px",
                border_radius="20px", margin_bottom="22px",
            ),
            rx.heading(
                "Salary intelligence,",
                rx.html("<br/>"),
                "built on live data",
                font_size="38px", font_weight="600", color="#f5f5f3",
                line_height="1.15", letter_spacing="-0.5px",
                font_family=FONT, margin_bottom="18px",
            ),
            rx.text(
                "Predict pay, catch anomalies, and manage your workforce, "
                "all backed by machine learning and a real-time AWS database.",
                font_size="15px", color="#a3a39e", line_height="1.65",
                max_width="400px", margin_bottom="30px",
            ),
            rx.hstack(
                rx.button(
                    "Log in", on_click=rx.redirect("/login"),
                    background="#7F77DD", color="#0a0a0c", font_weight="500",
                    font_family=FONT, _hover={"background": "#8f88e5"},
                ),
                rx.button(
                    "Sign up", on_click=rx.redirect("/signup"),
                    background="transparent", color="#f5f5f3",
                    border="0.5px solid rgba(255,255,255,0.2)", font_family=FONT,
                    _hover={"background": "rgba(255,255,255,0.05)"},
                ),
                spacing="3", margin_bottom="38px",
            ),
            rx.hstack(
                stat("148,654", "records"),
                stat("3", "ML models"),
                stat("Live", "database"),
                spacing="7",
            ),
            align="start",
        ),
        rx.box(
            rx.text("ADMIN OVERVIEW", font_size="11px", color="#79796f",
                     letter_spacing="0.5px", margin_bottom="14px"),
            rx.grid(
                rx.box(
                    rx.text("Avg pay", font_size="11px", color="#79796f"),
                    rx.text("$93,909", font_size="17px", font_weight="600",
                            color="#f5f5f3", font_family=FONT, margin_top="2px"),
                    background="#1c1c1f", border_radius="8px", padding="10px 12px",
                ),
                rx.box(
                    rx.text("Anomalies", font_size="11px", color="#79796f"),
                    rx.text("2,966", font_size="17px", font_weight="600",
                            color="#F0997B", font_family=FONT, margin_top="2px"),
                    background="#1c1c1f", border_radius="8px", padding="10px 12px",
                ),
                columns="2", spacing="2", margin_bottom="16px", width="100%",
            ),
            rx.html(SPARKLINE_SVG),
            background="rgba(21,21,23,0.85)",
            border="0.5px solid rgba(255,255,255,0.08)",
            border_radius="12px", padding="1.25rem",
            _hover={"border": "0.5px solid rgba(127,119,221,0.4)"},
            transition="border 0.3s ease",
        ),
        columns="2", spacing="6", width="100%",
        align="center",
        position="relative", z_index="1",
    )


def feature_card(icon, icon_bg, icon_color, title, description):
    return rx.vstack(
        rx.box(
            rx.icon(icon, size=17, color=icon_color),
            width="34px", height="34px", border_radius="8px",
            background=icon_bg, display="flex",
            align_items="center", justify_content="center",
            margin_bottom="12px",
        ),
        rx.text(title, font_weight="500", font_size="14px", color="#f5f5f3"),
        rx.text(description, font_size="13px", color="#a3a39e", line_height="1.5"),
        align="start",
        background="rgba(21,21,23,0.85)",
        border="0.5px solid rgba(255,255,255,0.08)",
        border_radius="12px", padding="1.25rem",
        _hover={
            "border": "0.5px solid rgba(255,255,255,0.2)",
            "transform": "translateY(-2px)",
        },
        transition="all 0.25s ease",
        width="100%",
    )


def feature_grid():
    return rx.grid(
        feature_card(
            "trending-up", "rgba(127,119,221,0.15)", "#AFA9EC",
            "Predict salaries",
            "Estimate expected pay by role and year using a trained regression model.",
        ),
        feature_card(
            "triangle-alert", "rgba(93,202,165,0.15)", "#5DCAA5",
            "Detect anomalies",
            "Flag pay records that look statistically unusual, automatically.",
        ),
        feature_card(
            "users", "rgba(240,153,123,0.15)", "#F0997B",
            "Manage employees",
            "Add, remove, and review records live, no spreadsheets required.",
        ),
        columns="3", spacing="4", width="100%",
        margin_top="52px", position="relative", z_index="1",
    )


def how_it_works():
    steps = [
        ("log-in", "Sign in", "Employees and admins share one secure login."),
        ("layout-dashboard", "View your data", "See real pay records pulled live from AWS."),
        ("sparkles", "Get predictions", "Run trained ML models on any role or record."),
    ]
    return rx.vstack(
        rx.text("How it works", font_size="12px", color="#79796f",
                letter_spacing="1px", margin_bottom="20px"),
        rx.hstack(
            *[
                rx.hstack(
                    rx.vstack(
                        rx.box(
                            rx.icon(icon, size=16, color="#f5f5f3"),
                            width="32px", height="32px", border_radius="50%",
                            background="rgba(255,255,255,0.06)",
                            border="0.5px solid rgba(255,255,255,0.15)",
                            display="flex", align_items="center", justify_content="center",
                        ),
                        rx.text(title, font_size="13px", font_weight="500", color="#f5f5f3"),
                        rx.text(desc, font_size="12px", color="#79796f",
                                text_align="center", max_width="140px"),
                        align="center", spacing="2",
                    ),
                    rx.cond(
                        i < 2,
                        rx.icon("arrow-right", size=14, color="#3a3a38"),
                        rx.fragment(),
                    ),
                    spacing="5", align="center",
                )
                for i, (icon, title, desc) in enumerate(steps)
            ],
            spacing="5", justify="center", width="100%",
        ),
        margin_top="60px", position="relative", z_index="1", align="center",
        padding_top="40px", border_top="0.5px solid rgba(255,255,255,0.06)",
    )


def footer():
    return rx.hstack(
        rx.hstack(
            rx.box(width="6px", height="6px", border_radius="50%", background="#5DCAA5"),
            rx.text("All systems operational", font_size="12px", color="#79796f"),
            spacing="2", align="center",
        ),
        rx.spacer(),
        rx.text(
            "Built with Django, PostgreSQL on AWS RDS, and scikit-learn",
            font_size="12px", color="#4a4a48",
        ),
        width="100%", margin_top="40px", padding_top="20px",
        border_top="0.5px solid rgba(255,255,255,0.06)",
        position="relative", z_index="1",
    )


def home():
    return rx.box(
        rx.box(
            rx.hstack(
                rx.box(width="10px", height="10px", border_radius="50%", background="#E24B4A"),
                rx.box(width="10px", height="10px", border_radius="50%", background="#EF9F27"),
                rx.box(width="10px", height="10px", border_radius="50%", background="#1D9E75"),
                rx.spacer(),
                rx.text("vanpre.ai", font_size="12px", color="#7a7a7a"),
                rx.spacer(),
                width="100%", padding="10px 16px", align="center",
            ),
            background="#1a1a1a",
        ),
        rx.box(
            rx.html(NETWORK_SVG),
            nav_bar(),
            hero(),
            feature_grid(),
            how_it_works(),
            footer(),
            background="#0a0a0c",
            padding="2.5rem 2.5rem 2rem",
            position="relative",
            overflow="hidden",
            font_family=FONT,
        ),
        min_height="100vh",
    )
