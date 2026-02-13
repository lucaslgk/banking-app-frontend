"""Dashboard page."""

import reflex as rx
from ..components.layout import base_layout
from ..components.stat_card import stat_card
from ..state.app_state import AppState


def dashboard() -> rx.Component:
    """Dashboard page with overview statistics."""
    return base_layout(
        rx.vstack(
            # Page header
            rx.heading("Dashboard", size="8", margin_bottom="0.5em"),
            rx.text(
                "Overview of banking transactions and system status",
                color="gray.600",
                margin_bottom="2em",
            ),
            
            # Error message
            rx.cond(
                AppState.error_message != "",
                rx.callout(
                    AppState.error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                    margin_bottom="1em",
                ),
            ),
            
            # Loading spinner
            rx.cond(
                AppState.is_loading,
                rx.center(
                    rx.spinner(size="3"),
                    padding="2em",
                ),
            ),
            
            # Statistics cards
            rx.cond(
                ~AppState.is_loading & (AppState.stats_overview != {}),
                rx.vstack(
                    rx.heading("Statistics Overview", size="6", margin_bottom="1em"),
                    rx.grid(
                        stat_card(
                            "Total Transactions",
                            AppState.stats_overview.get("total_transactions", 0).to(str),
                            "credit-card",
                            "blue",
                        ),
                        stat_card(
                            "Total Amount",
                            f"${AppState.stats_overview.get('total_amount', 0).to(float):,.2f}",
                            "dollar-sign",
                            "green",
                        ),
                        stat_card(
                            "Fraud Rate",
                            f"{(AppState.stats_overview.get('fraud_rate', 0).to(float) * 100):.2f}%",
                            "alert-triangle",
                            "red",
                        ),
                        stat_card(
                            "Average Amount",
                            f"${AppState.stats_overview.get('avg_amount', 0).to(float):,.2f}",
                            "bar-chart-2",
                            "purple",
                        ),
                        columns="4",
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    margin_bottom="2em",
                ),
            ),
            
            # Recent transactions
            rx.cond(
                ~AppState.is_loading & (AppState.recent_transactions.length() > 0),
                rx.vstack(
                    rx.heading("Recent Transactions", size="6", margin_bottom="1em"),
                    rx.box(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID"),
                                    rx.table.column_header_cell("Date"),
                                    rx.table.column_header_cell("Customer"),
                                    rx.table.column_header_cell("Amount"),
                                    rx.table.column_header_cell("Type"),
                                    rx.table.column_header_cell("Fraud"),
                                ),
                            ),
                            rx.table.body(
                                rx.foreach(
                                    AppState.recent_transactions,
                                    lambda txn: rx.table.row(
                                        rx.table.cell(txn.id),
                                        rx.table.cell(txn.date),
                                        rx.table.cell(txn.client_id),
                                        rx.table.cell(f"${txn.amount:.2f}"),
                                        rx.table.cell(txn.use_chip),
                                        rx.table.cell(
                                            rx.cond(
                                                txn.isFraud == 1,
                                                rx.badge("Yes", color_scheme="red"),
                                                rx.badge("No", color_scheme="green"),
                                            )
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        background="white",
                        padding="1.5em",
                        border_radius="12px",
                        border="1px solid",
                        border_color="gray.100",
                        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                    ),
                    width="100%",
                    margin_bottom="2em",
                ),
            ),
            
            # System status
            rx.cond(
                ~AppState.is_loading & (AppState.system_health != {}),
                rx.vstack(
                    rx.heading("System Status", size="6", margin_bottom="1em"),
                    rx.grid(
                        rx.box(
                            rx.vstack(
                                rx.text("API Health", font_weight="bold", color="gray.700"),
                                rx.badge(
                                    AppState.system_health.get("status", "unknown"),
                                    color_scheme="green",
                                    font_size="1.2em",
                                ),
                                spacing="2",
                            ),
                            padding="1.5em",
                            background="white",
                            border_radius="12px",
                            border="1px solid",
                            border_color="gray.100",
                            box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("API Version", font_weight="bold", color="gray.700"),
                                rx.text(
                                    AppState.system_metadata.get("version", "1.0.0"),
                                    font_size="1.2em",
                                    color="gray.800",
                                ),
                                spacing="2",
                            ),
                            padding="1.5em",
                            background="white",
                            border_radius="12px",
                            border="1px solid",
                            border_color="gray.100",
                            box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Total Endpoints", font_weight="bold", color="gray.700"),
                                rx.text(
                                    "20",
                                    font_size="1.2em",
                                    color="gray.800",
                                ),
                                spacing="2",
                            ),
                            padding="1.5em",
                            background="white",
                            border_radius="12px",
                            border="1px solid",
                            border_color="gray.100",
                            box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                        ),
                        columns="3",
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                ),
            ),
            
            width="100%",
            spacing="4",
        ),
        on_mount=AppState.load_dashboard_data,
    )
