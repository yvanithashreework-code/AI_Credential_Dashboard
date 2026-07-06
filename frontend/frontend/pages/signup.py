import reflex as rx

def signup():
    return rx.center(
        rx.vstack(
            rx.heading("Create Your Account", size="7", color="cyan"),
            rx.text("Join the AI Credential Dashboard", color="gray"),
            rx.input(placeholder="Full Name", name="name"),
            rx.input(placeholder="Email", name="email"),
            rx.input(placeholder="Password", type="password", name="password"),
            rx.input(placeholder="Confirm Password", type="password", name="confirm_password"),
            rx.button("Sign Up", color_scheme="blue", size="3"),
            rx.link("Already have an account? Login", href="/login"),
            spacing="4",
        ),
        height="100vh",
        background_color="black",
    )
