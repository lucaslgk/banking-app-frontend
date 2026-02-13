"""Fraud detection page."""

import reflex as rx
from ..components.layout import base_layout
from ..components.stat_card import stat_card
from ..state.app_state import AppState


class FraudState(rx.State):
    """State for fraud prediction form."""

    pred_amount: str = ""
    pred_use_chip: str = "Swipe Transaction"
    pred_merchant_state: str = ""
    pred_mcc: str = ""

    def set_pred_amount(self, value: str):
        """Set prediction amount."""
        self.pred_amount = value

    def set_pred_use_chip(self, value: str):
        """Set prediction transaction type."""
        self.pred_use_chip = value

    def set_pred_merchant_state(self, value: str):
        """Set prediction merchant state."""
        self.pred_merchant_state = value

    def set_pred_mcc(self, value: str):
        """Set prediction MCC."""
        self.pred_mcc = value

    def clear_form(self):
        """Clear all form fields."""
        self.pred_amount = ""
        self.pred_use_chip = "Swipe Transaction"
        self.pred_merchant_state = ""
        self.pred_mcc = ""

    async def submit_prediction(self):
        """Submit fraud prediction with proper async handling."""
        # Validate inputs
        if not self.pred_amount:
            app_state = await self.get_state(AppState)
            app_state.error_message = "Please enter an amount"
            return

        if not self.pred_mcc:
            app_state = await self.get_state(AppState)
            app_state.error_message = "Please enter a MCC code"
            return

        if not self.pred_merchant_state:
            app_state = await self.get_state(AppState)
            app_state.error_message = "Please enter a merchant state"
            return

        try:
            amount = float(self.pred_amount)
            mcc = int(self.pred_mcc)

            # Get AppState and call predict_fraud
            app_state = await self.get_state(AppState)
            await app_state.predict_fraud(
                amount=amount,
                use_chip=self.pred_use_chip,
                merchant_state=self.pred_merchant_state,
                mcc=mcc,
            )
        except ValueError:
            app_state = await self.get_state(AppState)
            app_state.error_message = "Invalid input: Amount must be a number and MCC must be an integer"


def fraud() -> rx.Component:
    """Fraud detection page with summary and prediction."""
    return base_layout(
        rx.vstack(
            # Page header
            rx.heading("Fraud Detection", size="8", margin_bottom="0.5em"),
            rx.text(
                "Monitor fraud statistics and predict fraudulent transactions",
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

            # Fraud summary stats
            rx.cond(
                ~AppState.is_loading & (AppState.fraud_summary != {}),
                rx.vstack(
                    rx.heading("Fraud Summary", size="6", margin_bottom="1em"),
                    rx.grid(
                        stat_card(
                            "Total Frauds",
                            AppState.fraud_summary.get("total_frauds", 0).to(str),
                            "alert-octagon",
                            "red",
                        ),
                        stat_card(
                            "Fraud Rate",
                            f"{(AppState.fraud_summary.get('fraud_rate', 0).to(float) * 100):.2f}%",
                            "activity",
                            "orange",
                        ),
                        stat_card(
                            "Total Fraud Amount",
                            f"${AppState.fraud_summary.get('total_fraud_amount', 0).to(float):,.2f}",
                            "dollar-sign",
                            "purple",
                        ),
                        columns="3",
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    margin_bottom="2em",
                ),
            ),

            # Fraud by type
            rx.cond(
                ~AppState.is_loading & (AppState.fraud_by_type.length() > 0),
                rx.vstack(
                    rx.heading("Fraud by Transaction Type", size="6", margin_bottom="1em"),
                    rx.box(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("Transaction Type"),
                                    rx.table.column_header_cell("Total Transactions"),
                                    rx.table.column_header_cell("Fraud Count"),
                                    rx.table.column_header_cell("Fraud Rate"),
                                ),
                            ),
                            rx.table.body(
                                rx.foreach(
                                    AppState.fraud_by_type,
                                    lambda item: rx.table.row(
                                        rx.table.cell(
                                            rx.badge(
                                                item.type,
                                                color_scheme="blue",
                                                variant="soft",
                                            )
                                        ),
                                        rx.table.cell(item.total_count),
                                        rx.table.cell(
                                            rx.text(
                                                item.fraud_count.to(str),
                                                font_weight="bold",
                                                color="red.600",
                                            )
                                        ),
                                        rx.table.cell(
                                            rx.badge(
                                                f"{(item.fraud_rate * 100):.2f}%",
                                                color_scheme=rx.cond(
                                                    item.fraud_rate > 0.05,
                                                    "red",
                                                    "green",
                                                ),
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
                    ),
                    width="100%",
                    margin_bottom="2em",
                ),
            ),

            # Fraud prediction form
            rx.vstack(
                rx.heading("Fraud Prediction", size="6", margin_bottom="1em"),
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Enter transaction details to predict fraud probability",
                            color="gray.600",
                            margin_bottom="1em",
                        ),

                        rx.grid(
                            rx.vstack(
                                rx.text("Amount", font_weight="bold", font_size="0.9em"),
                                rx.input(
                                    placeholder="100.00",
                                    type="number",
                                    value=FraudState.pred_amount,
                                    on_change=FraudState.set_pred_amount,
                                ),
                                align_items="flex-start",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Transaction Type", font_weight="bold", font_size="0.9em"),
                                rx.select(
                                    ["Swipe Transaction", "Chip Transaction", "Online Transaction"],
                                    value=FraudState.pred_use_chip,
                                    on_change=FraudState.set_pred_use_chip,
                                ),
                                align_items="flex-start",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Merchant State", font_weight="bold", font_size="0.9em"),
                                rx.select(
                                    AppState.merchant_states,
                                    placeholder="Select State",
                                    value=FraudState.pred_merchant_state,
                                    on_change=FraudState.set_pred_merchant_state,
                                ),
                                align_items="flex-start",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("MCC (Merchant Category Code)", font_weight="bold", font_size="0.9em"),
                                rx.select(
                                    AppState.mcc_codes,
                                    placeholder="Select MCC",
                                    value=FraudState.pred_mcc,
                                    on_change=FraudState.set_pred_mcc,
                                ),
                                align_items="flex-start",
                                spacing="1",
                            ),
                            columns="4",
                            spacing="4",
                            width="100%",
                        ),

                        rx.hstack(
                            rx.button(
                                rx.cond(
                                    AppState.is_loading,
                                    rx.spinner(size="1", color="white"),
                                    rx.text("Analyze Transaction"),
                                ),
                                on_click=FraudState.submit_prediction,
                                color_scheme="purple",
                                size="3",
                                width="200px",
                            ),
                            rx.button(
                                "Clear",
                                on_click=FraudState.clear_form,
                                variant="outline",
                                size="3",
                            ),
                            spacing="3",
                        ),

                        # Prediction result
                        rx.cond(
                            AppState.fraud_prediction != {},
                            rx.box(
                                rx.vstack(
                                    rx.heading("Prediction Result", size="5", margin_bottom="1em"),
                                    rx.hstack(
                                        rx.vstack(
                                            rx.text("Fraud Classification", font_weight="bold"),
                                            rx.cond(
                                                AppState.fraud_prediction.get("isFraud", False),
                                                rx.badge("FRAUDULENT", color_scheme="red", font_size="1.5em"),
                                                rx.badge("LEGITIMATE", color_scheme="green", font_size="1.5em"),
                                            ),
                                            align_items="center",
                                            spacing="2",
                                        ),
                                        rx.spacer(),
                                        rx.vstack(
                                            rx.text("Fraud Probability", font_weight="bold"),
                                            rx.text(
                                                f"{(AppState.fraud_prediction.get('probability', 0).to(float) * 100):.1f}%",
                                                font_size="2em",
                                                font_weight="bold",
                                                color=rx.cond(
                                                    AppState.fraud_prediction.get("probability", 0).to(float) > 0.5,
                                                    "red.600",
                                                    "green.600",
                                                ),
                                            ),
                                            align_items="center",
                                            spacing="2",
                                        ),
                                        width="100%",
                                        spacing="4",
                                    ),
                                    spacing="3",
                                ),
                                padding="1.5em",
                                background="gray.50",
                                border_radius="8px",
                                border="2px solid",
                                border_color=rx.cond(
                                    AppState.fraud_prediction.get("isFraud", False),
                                    "red.300",
                                    "green.300",
                                ),
                                margin_top="1em",
                            ),
                        ),

                        spacing="4",
                    ),
                    padding="1.5em",
                    background="white",
                    border_radius="12px",
                    border="1px solid",
                    border_color="gray.200",
                    box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                ),
                width="100%",
            ),

            width="100%",
            spacing="4",
        ),
        on_mount=AppState.load_fraud_data,
    )
