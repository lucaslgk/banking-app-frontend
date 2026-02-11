"""Base layout component with navigation."""

import reflex as rx
from ..state.app_state import AppState


def navbar() -> rx.Component:
    """Create navigation bar component."""
    return rx.box(
        rx.cond(
            AppState.is_loading,
            rx.progress(is_indeterminate=True, width="100%", position="fixed", top="0", z_index="9999", color_scheme="indigo"),
        ),
        rx.hstack(
            # Logo and title
            rx.hstack(
                rx.icon("credit-card", color="white", size=28),
                rx.heading("Banking App", size="6", color="white", font_weight="bold"),
                spacing="3",
                align_items="center",
            ),
            rx.spacer(),
            # Navigation links
            rx.hstack(
                rx.link(
                    rx.text("Dashboard", color="white", font_weight="500"),
                    href="/",
                    padding="0.5em 1em",
                    border_radius="6px",
                    _hover={"bg": "rgba(255,255,255,0.1)"},
                ),
                rx.link(
                    rx.text("Transactions", color="white", font_weight="500"),
                    href="/transactions",
                    padding="0.5em 1em",
                    border_radius="6px",
                    _hover={"bg": "rgba(255,255,255,0.1)"},
                ),
                rx.link(
                    rx.text("Customers", color="white", font_weight="500"),
                    href="/customers",
                    padding="0.5em 1em",
                    border_radius="6px",
                    _hover={"bg": "rgba(255,255,255,0.1)"},
                ),
                rx.link(
                    rx.text("Fraud Detection", color="white", font_weight="500"),
                    href="/fraud",
                    padding="0.5em 1em",
                    border_radius="6px",
                    _hover={"bg": "rgba(255,255,255,0.1)"},
                ),
                spacing="4",
            ),
            width="100%",
            padding="1em 2em",
            align_items="center",
        ),
        background="#1a365d",  # Navy Blue
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        position="sticky",
        top="0",
        z_index="1000",
        border_bottom="1px solid rgba(255,255,255,0.1)",
    )


def footer() -> rx.Component:
    """Create footer component."""
    return rx.box(
        rx.center(
            rx.text(
                "Banking Transactions API Frontend © 2026 | Powered by Reflex",
                color="gray.600",
                font_size="0.9em",
            ),
        ),
        padding="2em",
        background="white",
        border_top="1px solid",
        border_color="gray.200",
        margin_top="auto",
    )


def base_layout(*children, **props) -> rx.Component:
    """Base layout wrapper for all pages.
    
    Args:
        *children: Page content components
        **props: Additional properties to pass to the root component (e.g. on_mount)
        
    Returns:
        Complete page layout with navbar and footer
    """
    return rx.box(
        navbar(),
        rx.box(
            *children,
            padding="2em",
            min_height="calc(100vh - 200px)",
            background="gray.50",
        ),
        footer(),
        display="flex",
        flex_direction="column",
        min_height="100vh",
        **props,
    )
