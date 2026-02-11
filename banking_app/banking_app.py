"""Banking App - Frontend for Banking Transactions API."""

import reflex as rx
# from .pages.dashboard import dashboard
# from .pages.transactions import transactions
# from .pages.customers import customers
# from .pages.fraud import fraud


# Create the Reflex app
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="indigo",
        radius="large",
    ),
)

# Add routes
# app.add_page(dashboard, route="/", title="Dashboard - Banking App")
# app.add_page(transactions, route="/transactions", title="Transactions - Banking App")
# app.add_page(customers, route="/customers", title="Customers - Banking App")
# app.add_page(fraud, route="/fraud", title="Fraud Detection - Banking App")

# Temporary placeholder route
def index():
    return rx.text("Backend Core Initialized. Pages coming soon.")

app.add_page(index, route="/")
