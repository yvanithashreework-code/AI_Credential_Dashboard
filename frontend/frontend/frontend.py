import reflex as rx
from frontend.state import State
from frontend.pages.home import home
from frontend.pages.login import login
from frontend.pages.signup import signup
from frontend.pages.overview import overview
from frontend.pages.predict import predict
from frontend.pages.analysis import analysis
from frontend.pages.employees import employees


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&display=swap",
    ],
)

app.add_page(home, route="/")
app.add_page(login, route="/login")
app.add_page(signup, route="/signup")

app.add_page(overview, route="/overview", on_load=State.load_dashboard)
app.add_page(predict, route="/predict", on_load=State.require_login)
app.add_page(analysis, route="/analysis", on_load=State.load_analytics)
app.add_page(employees, route="/employees", on_load=State.require_admin)
