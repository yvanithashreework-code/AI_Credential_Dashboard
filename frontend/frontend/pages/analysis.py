import reflex as rx
from frontend.state import State
from frontend.components.layout import page_shell

BAND_COLORS = ["#F0997B", "#7F77DD", "#5DCAA5"]


def kpi(label, value, color="#1a1a1a"):
    return rx.box(
        rx.text(label, font_size="12px", color="#8a8a85", margin_bottom="6px"),
        rx.text(value, font_size="22px", font_weight="600", color=color),
        background="#faf9f6", border="0.5px solid #ececE5",
        border_radius="12px", padding="1rem 1.25rem", width="100%",
    )


def chart_card(title, chart):
    return rx.box(
        rx.text(title, font_size="13px", font_weight="500", color="#1a1a1a", margin_bottom="16px"),
        chart,
        background="white", border="0.5px solid #ececE5",
        border_radius="12px", padding="1.25rem", width="100%",
    )


def pay_trend_chart():
    return rx.recharts.line_chart(
        rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#f0efe9"),
        rx.recharts.x_axis(data_key="year", stroke="#a3a39e", font_size=12),
        rx.recharts.y_axis(stroke="#a3a39e", font_size=12),
        rx.recharts.line(
            data_key="avg_total_pay", stroke="#7F77DD", stroke_width=2.5, dot=False,
        ),
        rx.recharts.graphing_tooltip(),
        data=State.analytics_avg_pay_by_year,
        width="100%", height=260,
    )


def top_titles_chart():
    return rx.recharts.bar_chart(
        rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#f0efe9"),
        rx.recharts.x_axis(type_="number", stroke="#a3a39e", font_size=11),
        rx.recharts.y_axis(data_key="job_title", type_="category", width=180, stroke="#a3a39e", font_size=11),
        rx.recharts.bar(data_key="avg_total_pay", fill="#5DCAA5", radius=[0, 6, 6, 0]),
        rx.recharts.graphing_tooltip(),
        data=State.analytics_top_job_titles,
        layout="vertical",
        width="100%", height=340,
    )


def band_pie_chart():
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=State.analytics_band_distribution,
            data_key="value", name_key="name",
            cx="50%", cy="50%", inner_radius=55, outer_radius=85,
            fill="#7F77DD",
            *[rx.recharts.cell(fill=BAND_COLORS[i]) for i in range(3)],
        ),
        rx.recharts.graphing_tooltip(),
        rx.recharts.legend(),
        width="100%", height=260,
    )


def analysis():
    return page_shell(
        rx.heading("Analysis & trends", size="6", color="#1a1a1a", margin_bottom="4px"),
        rx.text("Dataset-wide statistics computed live from AWS RDS.", color="#8a8a85", font_size="14px", margin_bottom="24px"),
        rx.cond(
            State.analytics_loading,
            rx.text("Crunching the numbers...", color="#8a8a85"),
            rx.cond(
                State.analytics_error != "",
                rx.text(State.analytics_error, color="#d64545"),
                rx.vstack(
                    rx.grid(
                        kpi("Total employees", State.analytics_total_employees.to_string()),
                        kpi("Average total pay", "$" + State.analytics_avg_total_pay.to_string()),
                        kpi("Distinct job titles", State.analytics_distinct_job_titles.to_string()),
                        kpi("Anomalies flagged", State.analytics_anomaly_count.to_string(), "#F0997B"),
                        columns="4", spacing="4", width="100%", margin_bottom="24px",
                    ),
                    rx.grid(
                        chart_card("Average pay by year", pay_trend_chart()),
                        chart_card("Pay band distribution", band_pie_chart()),
                        columns="2", spacing="4", width="100%", margin_bottom="24px",
                    ),
                    chart_card("Top-paid job titles (min. 50 records)", top_titles_chart()),
                    width="100%", spacing="4",
                ),
            ),
        ),
    )
