"""Transactions page."""

import reflex as rx
from ..components.layout import base_layout
from ..state.app_state import AppState


def transactions() -> rx.Component:
    """Transactions page with filtering and pagination."""
    return base_layout(
        rx.vstack(
            # Page header
            rx.heading("Transactions", size="8", margin_bottom="0.5em"),
            rx.text(
                "Browse and filter banking transactions",
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
            
            # Filters
            rx.box(
                rx.vstack(
                    rx.heading("Filters", size="5", margin_bottom="1em"),
                    rx.grid(
                        rx.vstack(
                            rx.text("Transaction Type", font_weight="bold", font_size="0.9em"),
                            rx.select(
                                ["All", "Swipe Transaction", "Chip Transaction", "Online Transaction"],
                                placeholder="Select type",
                                value=AppState.filter_use_chip,
                                on_change=AppState.set_filter_use_chip,
                            ),
                            align_items="flex-start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Fraud Status", font_weight="bold", font_size="0.9em"),
                            rx.select(
                                ["All", "Fraudulent", "Legitimate"],
                                placeholder="Select status",
                                on_change=AppState.set_filter_is_fraud,
                            ),
                            align_items="flex-start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Min Amount", font_weight="bold", font_size="0.9em"),
                            rx.input(
                                placeholder="0.00",
                                type="number",
                                value=AppState.filter_min_amount,
                                on_change=AppState.set_filter_min_amount,
                            ),
                            align_items="flex-start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Max Amount", font_weight="bold", font_size="0.9em"),
                            rx.input(
                                placeholder="10000.00",
                                type="number",
                                value=AppState.filter_max_amount,
                                on_change=AppState.set_filter_max_amount,
                            ),
                            align_items="flex-start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Merchant State", font_weight="bold", font_size="0.9em"),
                            rx.input(
                                placeholder="e.g., CA",
                                value=AppState.filter_merchant_state,
                                on_change=AppState.set_filter_merchant_state,
                            ),
                            align_items="flex-start",
                            spacing="1",
                        ),
                        columns="5",
                        spacing="4",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            "Apply Filters",
                            on_click=AppState.load_transactions,
                            color_scheme="blue",
                        ),
                        rx.button(
                            "Reset",
                            on_click=[AppState.reset_filters, AppState.load_transactions],
                            variant="outline",
                        ),
                        spacing="2",
                    ),
                    spacing="3",
                ),
                padding="1.5em",
                background="white",
                border_radius="12px",
                border="1px solid",
                border_color="gray.200",
                box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                margin_bottom="2em",
            ),
            
            # Loading spinner
            rx.cond(
                AppState.is_loading,
                rx.center(
                    rx.spinner(size="3"),
                    padding="2em",
                ),
            ),
            
            # Transactions table
            rx.cond(
                ~AppState.is_loading & (AppState.transactions.length() > 0),
                rx.vstack(
                    rx.box(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID"),
                                    rx.table.column_header_cell("Date"),
                                    rx.table.column_header_cell("Customer"),
                                    rx.table.column_header_cell("Amount"),
                                    rx.table.column_header_cell("Type"),
                                    rx.table.column_header_cell("Merchant"),
                                    rx.table.column_header_cell("State"),
                                    rx.table.column_header_cell("Fraud"),
                                ),
                            ),
                            rx.table.body(
                                rx.foreach(
                                    AppState.transactions,
                                    lambda txn: rx.table.row(
                                        rx.table.cell(
                                            rx.text(
                                                txn.id[:8] + "...",
                                                font_size="0.85em",
                                                color="gray.600",
                                            )
                                        ),
                                        rx.table.cell(txn.date),
                                        rx.table.cell(txn.client_id),
                                        rx.table.cell(
                                            rx.text(
                                                f"${txn.amount:.2f}",
                                                font_weight="bold",
                                                color=rx.cond(
                                                    txn.amount < 0,
                                                    "red.600",
                                                    "green.600",
                                                ),
                                            )
                                        ),
                                        rx.table.cell(
                                            rx.badge(
                                                txn.use_chip,
                                                color_scheme="blue",
                                                variant="soft",
                                            )
                                        ),
                                        rx.table.cell(
                                            rx.text(
                                                txn.merchant_city,
                                                font_size="0.85em",
                                            )
                                        ),
                                        rx.table.cell(
                                            txn.merchant_state
                                        ),
                                        rx.table.cell(
                                            rx.cond(
                                                txn.isFraud == 1,
                                                rx.badge("Fraud", color_scheme="red"),
                                                rx.badge("Safe", color_scheme="green"),
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
                        border_color="gray.200",
                        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                        overflow_x="auto",
                    ),
                    
                    # Pagination
                    rx.hstack(
                        rx.text(
                            f"Page {AppState.current_page} | Total: {AppState.total_transactions} transactions",
                            color="gray.600",
                        ),
                        rx.spacer(),
                        rx.hstack(
                            rx.button(
                                rx.cond(
                                    AppState.is_loading,
                                    rx.spinner(size="1", color="gray"),
                                    rx.text("Previous"),
                                ),
                                on_click=AppState.prev_page,
                                disabled=AppState.current_page == 1,
                                variant="outline",
                            ),
                            rx.button(
                                rx.cond(
                                    AppState.is_loading,
                                    rx.spinner(size="1", color="gray"),
                                    rx.text("Next"),
                                ),
                                on_click=AppState.next_page,
                                disabled=AppState.current_page * AppState.items_per_page >= AppState.total_transactions,
                                variant="outline",
                            ),
                            spacing="2",
                        ),
                        width="100%",
                        padding="1em",
                    ),
                    
                    width="100%",
                    spacing="4",
                ),
            ),
            
            # Empty state
            rx.cond(
                ~AppState.is_loading & (AppState.transactions.length() == 0),
                rx.center(
                    rx.vstack(
                        rx.icon("file-text", size=64, color="gray"),
                        rx.heading("No transactions found", size="6"),
                        rx.text("Try adjusting your filters", color="gray.600"),
                        spacing="2",
                    ),
                    padding="4em",
                ),
            ),
            
            width="100%",
            spacing="4",
        ),
        on_mount=AppState.load_transactions,
    )
