import reflex as rx

def history():
    return rx.box(
        rx.vstack(
            # Top Navigation Bar
            rx.hstack(
                rx.heading("History", size="7", color="cyan"),
                rx.spacer(),
                rx.button("Dashboard", color_scheme="blue", size="2", href="/dashboard"),
                padding="2",
                border_bottom="1px solid rgba(255,255,255,0.1)",
            ),

            rx.box(height="20px"),

            # Activity Log Card
            rx.card(
                rx.vstack(
                    rx.heading("Activity Log", size="5", color="cyan"),

                    # Table Header
                    rx.hstack(
                        rx.text("Timestamp", weight="bold", color="white"),
                        rx.text("Action", weight="bold", color="white"),
                        rx.text("Status", weight="bold", color="white"),
                        rx.text("Details", weight="bold", color="white"),
                        spacing="8",
                    ),

                    rx.divider(),

                    # Row 1
                    rx.hstack(
                        rx.text("2026-07-03 14:22", color="gray"),
                        rx.text("API Call", color="gray"),
                        rx.text("Success", color="green"),
                        rx.text("Fetched model usage", color="gray"),
                        spacing="8",
                    ),

                    # Row 2
                    rx.hstack(
                        rx.text("2026-07-03 13:10", color="gray"),
                        rx.text("Prediction", color="gray"),
                        rx.text("Success", color="green"),
                        rx.text("Risk Score: Low", color="gray"),
                        spacing="8",
                    ),

                    # Row 3
                    rx.hstack(
                        rx.text("2026-07-03 11:45", color="gray"),
                        rx.text("Credential Update", color="gray"),
                        rx.text("Success", color="green"),
                        rx.text("Key rotated", color="gray"),
                        spacing="8",
                    ),

                    # Row 4
                    rx.hstack(
                        rx.text("2026-07-02 19:30", color="gray"),
                        rx.text("API Call", color="gray"),
                        rx.text("Failed", color="red"),
                        rx.text("Rate limit exceeded", color="gray"),
                        spacing="8",
                    ),

                    spacing="4",
                ),
                padding="4",
                background_color="rgba(255,255,255,0.05)",
                border_radius="lg",
            ),

            spacing="6",
        ),
        height="100vh",
        background_color="black",
        padding="4",
    )
