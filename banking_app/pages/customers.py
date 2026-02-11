"""Customers page."""

import reflex as rx
from ..components.layout import base_layout
from ..components.stat_card import stat_card
from ..state.app_state import AppState


def customers() -> rx.Component:
    """Customers page with top customers and profiles."""
    return base_layout(
        rx.vstack(
            # Page header
            rx.heading("Customers", size="8", margin_bottom="0.5em"),
            rx.text(
                "View customer profiles and top performers",
                color="gray.600",
                margin_bottom="2em",
            ),
            
            # Stats Cards
            rx.grid(
                stat_card(
                    "Total Customers",
                    AppState.total_customers.to(str),
                    "users",
                    "blue",
                ),
                stat_card(
                    "Avg Transaction",
                    f"${AppState.stats_overview.get('avg_amount', 0).to(float):,.2f}",
                    "credit-card",
                    "green",
                ),
                stat_card(
                    "Total Volume",
                    f"${AppState.stats_overview.get('total_amount', 0).to(float):,.0f}",
                    "dollar-sign",
                    "purple",
                ),
                columns="3",
                spacing="4",
                width="100%",
                margin_bottom="2em",
            ),

            # Search Bar
            rx.hstack(
                rx.input(
                    placeholder="Search by Customer ID...",
                    value=AppState.search_customer_id,
                    on_change=AppState.set_search_customer_id,
                    width="300px",
                ),
                rx.button(
                    rx.cond(
                        AppState.is_loading,
                        rx.spinner(size="1", color="white"),
                        rx.text("Search"),
                    ),
                    on_click=AppState.search_customer,
                    color_scheme="blue",
                ),
                rx.spacer(),
                width="100%",
                margin_bottom="1em",
            ),
            
            # Loading spinner
            rx.cond(
                AppState.is_loading,
                rx.center(
                    rx.spinner(size="3"),
                    padding="2em",
                ),
            ),
            
            # Customer Profile (if loaded from search)
            rx.cond(
                AppState.customer_profile,
                rx.vstack(
                    rx.heading(f"Customer Profile: {AppState.customer_profile['id']}", size="6"),
                    rx.button("Close Profile", on_click=lambda: AppState.set_customer_profile(None), variant="outline"),
                    # Add more profile details here if needed, or rely on a separate view/modal if implied
                    # For now, let's keep it simple and focus on the list table
                    rx.text("Profile loaded. (Implement detailed view here or navigate)", color="gray.500"),
                    margin_bottom="2em",
                    padding="1em",
                    border="1px solid #ddd",
                    border_radius="8px",
                ),
            ),

            # All Customers Table
            rx.cond(
                ~AppState.is_loading & (AppState.customers.length() > 0),
                rx.vstack(
                    rx.box(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("Customer ID"),
                                    rx.table.column_header_cell("Total Transactions"),
                                    rx.table.column_header_cell("Total Amount"),
                                    rx.table.column_header_cell("Avg Amount"),
                                    rx.table.column_header_cell("Fraud Count"),
                                    rx.table.column_header_cell("Actions"),
                                ),
                            ),
                            rx.table.body(
                                rx.foreach(
                                    AppState.customers,
                                    lambda customer: rx.table.row(
                                        rx.table.cell(
                                            rx.hstack(
                                                rx.icon("user", size=16),
                                                rx.text(customer.id, font_weight="bold"),
                                                spacing="2",
                                                align_items="center",
                                            )
                                        ),
                                        rx.table.cell(customer.transactions_count),
                                        rx.table.cell(
                                            rx.text(
                                                f"${customer.total_amount:.2f}",
                                                color="green.600",
                                                font_weight="500",
                                            )
                                        ),
                                        rx.table.cell(f"${customer.avg_amount:.2f}"),
                                        rx.table.cell(
                                            rx.cond(
                                                customer.fraud_count > 0,
                                                rx.badge(
                                                    customer.fraud_count.to(str),
                                                    color_scheme="red",
                                                ),
                                                rx.text("0", color="gray.500"),
                                            )
                                        ),
                                        rx.table.cell(
                                            rx.button(
                                                "View Profile",
                                                on_click=lambda: AppState.load_customer_profile(customer.id.to(str)),
                                                size="1",
                                                variant="soft",
                                            )
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        background="white",
                        padding="0", # Remove padding to make table flush or keep small
                        border_radius="12px",
                        border="1px solid",
                        border_color="gray.200",
                        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                        overflow_x="hidden", # Prevent double scrollbars
                        overflow="hidden", 
                        width="100%",
                    ),
                    
                    # Pagination for customers
                    rx.hstack(
                        rx.text(
                            f"Page {AppState.customers_page} | Total: {AppState.total_customers} customers",
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
                                on_click=AppState.prev_customers_page,
                                disabled=AppState.customers_page == 1,
                                variant="outline",
                            ),
                            rx.button(
                                rx.cond(
                                    AppState.is_loading,
                                    rx.spinner(size="1", color="gray"),
                                    rx.text("Next"),
                                ),
                                on_click=AppState.next_customers_page,
                                disabled=AppState.customers_page * AppState.items_per_page >= AppState.total_customers,
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
        ),
        on_mount=[AppState.load_top_customers, AppState.load_customers],
    )
