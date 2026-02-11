"""Reusable stat card component."""

import reflex as rx


def stat_card(title: str, value: str, icon_name: str = "activity", color: str = "blue") -> rx.Component:
    """Create a statistic card component.
    
    Args:
        title: Card title/label
        value: Main value to display
        icon_name: Lucide icon name
        color: Color scheme (blue, green, red, orange, purple, indigo)
        
    Returns:
        Reflex component for stat card
    """
    color_map = {
        "blue": "blue",
        "green": "green",
        "red": "red",
        "orange": "orange",
        "purple": "purple",
        "indigo": "indigo",
    }
    
    accent_color = color_map.get(color, "blue")
    
    return rx.box(
        rx.hstack(
            rx.center(
                rx.icon(icon_name, size=24),
                width="3em",
                height="3em",
                border_radius="full",
                bg=rx.color(accent_color, 3),
                color=rx.color(accent_color, 11),
            ),
            rx.vstack(
                rx.text(title, font_size="0.875em", color="gray.500", font_weight="500"),
                rx.text(value, font_size="1.5em", font_weight="bold", color="gray.900"),
                spacing="1",
                align_items="flex-start",
            ),
            spacing="4",
            align_items="center",
        ),
        padding="1.5em",
        border_radius="12px",
        background="white",
        border="1px solid",
        border_color="gray.100",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
            "border_color": rx.color(accent_color, 5),
        },
        transition="all 0.2s ease",
    )
