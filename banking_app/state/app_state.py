"""Application State Management."""

import reflex as rx
from typing import List, Dict, Any, Optional
import asyncio
from ..services.api_client import APIClient
from ..models import Transaction, Customer, FraudStat, DailyStat, TypeStat

# Initialize API client outside of State class to avoid serialization issues
api_client = APIClient()


class AppState(rx.State):
    """Main application state."""
    
    # Loading states
    is_loading: bool = False
    error_message: str = ""
    
    # Dashboard data
    stats_overview: Dict[str, Any] = {}
    recent_transactions: List[Transaction] = []
    system_health: Dict[str, Any] = {}
    system_metadata: Dict[str, Any] = {}
    
    # Transactions data
    transactions: List[Transaction] = []
    transaction_types: List[str] = []
    total_transactions: int = 0
    current_page: int = 1
    items_per_page: int = 50
    
    # Filters
    filter_use_chip: str = ""
    filter_is_fraud: Optional[int] = None
    filter_min_amount: str = ""
    filter_max_amount: str = ""
    filter_merchant_state: str = ""
    
    # Customers data
    customers: List[Customer] = []
    top_customers: List[Customer] = []
    customer_profile: Dict[str, Any] = {}
    total_customers: int = 0
    customers_page: int = 1
    
    # Fraud data
    fraud_summary: Dict[str, Any] = {}
    fraud_by_type: List[FraudStat] = []
    fraud_prediction: Dict[str, Any] = {}
    
    # Stats data
    amount_distribution: Dict[str, Any] = {}
    stats_by_type: List[TypeStat] = []
    daily_stats: List[DailyStat] = []
    
    async def load_dashboard_data(self):
        """Load all data for dashboard page."""
        self.is_loading = True
        self.error_message = ""
        try:
            # Load stats overview, recent transactions, and system info
            self.stats_overview = await api_client.get_stats_overview()
            recent_data = await api_client.get_recent_transactions(10)
            self.recent_transactions = [Transaction(**item) for item in recent_data]
            self.system_health = await api_client.get_health()
            self.system_metadata = await api_client.get_metadata()
        except Exception as e:
            self.error_message = f"Error loading dashboard: {str(e)}"
        finally:
            self.is_loading = False
    
    async def load_transactions(self):
        """Load transactions with current filters."""
        self.is_loading = True
        self.error_message = ""
        try:
            # Parse filter values
            min_amt = float(self.filter_min_amount) if self.filter_min_amount else None
            max_amt = float(self.filter_max_amount) if self.filter_max_amount else None
            
            result = await api_client.get_transactions(
                page=self.current_page,
                limit=self.items_per_page,
                use_chip=self.filter_use_chip if self.filter_use_chip else None,
                is_fraud=self.filter_is_fraud,
                min_amount=min_amt,
                max_amount=max_amt,
                merchant_state=self.filter_merchant_state if self.filter_merchant_state else None
            )
            self.transactions = [Transaction(**item) for item in result.get("transactions", [])]
            self.total_transactions = result.get("total", 0)
        except Exception as e:
            self.error_message = f"Error loading transactions: {str(e)}"
        finally:
            self.is_loading = False
    
    async def load_transaction_types(self):
        """Load available transaction types."""
        try:
            self.transaction_types = await api_client.get_transaction_types()
        except Exception as e:
            self.error_message = f"Error loading transaction types: {str(e)}"
    
    async def next_page(self):
        """Go to next page of transactions."""
        total_pages = (self.total_transactions + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            await self.load_transactions()
    
    async def prev_page(self):
        """Go to previous page of transactions."""
        if self.current_page > 1:
            self.current_page -= 1
            await self.load_transactions()
    
    def set_filter_is_fraud(self, value: str):
        """Set fraud filter from dropdown value.
        
        Args:
            value: The selected value ("Fraudulent", "Legitimate", "All")
        """
        if value == "Fraudulent":
            self.filter_is_fraud = 1
        elif value == "Legitimate":
            self.filter_is_fraud = 0
        else:
            self.filter_is_fraud = None
            
    def reset_filters(self):
        """Reset all transaction filters."""
        self.filter_use_chip = ""
        self.filter_is_fraud = None
        self.filter_min_amount = ""
        self.filter_max_amount = ""
        self.filter_merchant_state = ""
        self.current_page = 1
    
    async def load_customers(self):
        """Load customers list."""
        self.is_loading = True
        self.error_message = ""
        try:
            result = await api_client.get_customers(
                page=self.customers_page,
                limit=self.items_per_page
            )
            raw_customers = result.get("customers", [])
            customers_data = []

            # Check if we got a list of IDs (int) instead of objects
            if raw_customers and isinstance(raw_customers[0], int):
                # Fetch details for each customer in parallel
                tasks = [api_client.get_customer_profile(cid) for cid in raw_customers]
                customers_data = await asyncio.gather(*tasks)
            else:
                customers_data = raw_customers

            # Calculate avg_amount if missing
            for item in customers_data:
                if "avg_amount" not in item:
                    count = item.get("transactions_count", 0)
                    total = item.get("total_amount", 0.0)
                    item["avg_amount"] = total / count if count > 0 else 0.0

            self.customers = [Customer(**item) for item in customers_data]
            self.total_customers = result.get("total", 0)
        except Exception as e:
            self.error_message = f"Error loading customers: {str(e)}"
        finally:
            self.is_loading = False

    async def next_customers_page(self):
        """Go to next page of customers."""
        total_pages = (self.total_customers + self.items_per_page - 1) // self.items_per_page
        if self.customers_page < total_pages:
            self.customers_page += 1
            await self.load_customers()
    
    async def prev_customers_page(self):
        """Go to previous page of customers."""
        if self.customers_page > 1:
            self.customers_page -= 1
            await self.load_customers()
    
    async def load_top_customers(self):
        """Load top customers."""
        try:
            top_data = await api_client.get_top_customers(10)
            
            # Check if we got a list of IDs (int) instead of objects
            if top_data and isinstance(top_data[0], int):
                tasks = [api_client.get_customer_profile(cid) for cid in top_data]
                top_data = await asyncio.gather(*tasks)
                
            # Calculate avg_amount if missing
            for item in top_data:
                if "avg_amount" not in item:
                    count = item.get("transactions_count", 0)
                    total = item.get("total_amount", 0.0)
                    item["avg_amount"] = total / count if count > 0 else 0.0
                    
            self.top_customers = [Customer(**item) for item in top_data]
        except Exception as e:
            self.error_message = f"Error loading top customers: {str(e)}"
    
    
    # Customer Search
    search_customer_id: str = ""

    async def search_customer(self):
        """Search for a customer by ID."""
        if not self.search_customer_id:
            return
            
        self.is_loading = True
        self.error_message = ""
        try:
            # check if ID is valid integer
            try:
                customer_id = int(self.search_customer_id)
            except ValueError:
                self.error_message = "Customer ID must be a number"
                return

            # Direct lookup
            profile = await api_client.get_customer_profile(customer_id)
            if profile:
                self.customer_profile = profile
                # Navigate to profile page (handled by UI returning the component, 
                # but here we just load data. In Reflex we might need to redirect or show modal.
                # For now, let's assume the UI will show the profile if customer_profile is set
                # or we can redirect if using routing.)
                # Actually, the current UI shows profile in a separate page/view? 
                # The Plan said "Go to Customer ID". 
                # Let's just load it. The UI likely renders a profile view if selected.
                # Wait, the current UI has `load_customer_profile` which sets `self.customer_profile`.
                # If we reuse that, we are good.
            else:
                self.error_message = f"Customer {self.search_customer_id} not found"
        except Exception as e:
            self.error_message = f"Error searching customer: {str(e)}"
        finally:
            self.is_loading = False

    async def load_customer_profile(self, customer_id: str):
        """Load customer profile by ID."""
        self.is_loading = True
        self.error_message = ""
        try:
            self.customer_profile = await api_client.get_customer_profile(customer_id)
        except Exception as e:
            self.error_message = f"Error loading customer profile: {str(e)}"
        finally:
            self.is_loading = False
    
    async def load_fraud_data(self):
        """Load fraud detection data."""
        self.is_loading = True
        self.error_message = ""
        try:
            self.fraud_summary = await api_client.get_fraud_summary()
            fraud_data = await api_client.get_fraud_by_type()
            self.fraud_by_type = [FraudStat(**item) for item in fraud_data]
        except Exception as e:
            self.error_message = f"Error loading fraud data: {str(e)}"
        finally:
            self.is_loading = False
    
    async def predict_fraud(self, amount: float, use_chip: str, merchant_state: str, mcc: int):
        """Predict fraud for given transaction data."""
        self.is_loading = True
        self.error_message = ""
        try:
            data = {
                "amount": amount,
                "use_chip": use_chip,
                "merchant_state": merchant_state,
                "mcc": mcc
            }
            self.fraud_prediction = await api_client.predict_fraud(data)
        except Exception as e:
            self.error_message = f"Error predicting fraud: {str(e)}"
        finally:
            self.is_loading = False
    
    async def load_stats_data(self):
        """Load statistical data."""
        self.is_loading = True
        self.error_message = ""
        try:
            self.amount_distribution = await api_client.get_amount_distribution(10)
            stats_data = await api_client.get_stats_by_type()
            self.stats_by_type = [TypeStat(**item) for item in stats_data]
            daily_data = await api_client.get_daily_stats(30)
            self.daily_stats = [DailyStat(**item) for item in daily_data]
        except Exception as e:
            self.error_message = f"Error loading stats: {str(e)}"
        finally:
            self.is_loading = False
