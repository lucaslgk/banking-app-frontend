"""Application State Management with caching and optimizations."""

import reflex as rx
from typing import List, Dict, Any, Optional
import asyncio
import time
from ..services.api_client import APIClient
from ..models import Transaction, Customer, FraudStat, DailyStat, TypeStat

# Initialize API client outside of State class to avoid serialization issues
api_client = APIClient()

# Constants
ITEMS_PER_PAGE = 50
CACHE_TTL_SECONDS = 60  # Cache duration in seconds
TOP_CUSTOMERS_LIMIT = 10
RECENT_TRANSACTIONS_LIMIT = 10
DAILY_STATS_LIMIT = 30
AMOUNT_DISTRIBUTION_BINS = 10

# Default filter options
US_STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

COMMON_MCC_CODES = [
    "4111", "4814", "5200", "5300", "5311", "5411", "5541", 
    "5542", "5812", "5813", "5912", "5999"
]


class AppState(rx.State):
    """Main application state with caching and optimizations."""

    # Loading states
    is_loading: bool = False
    error_message: str = ""

    # Cache timestamps (for cache invalidation)
    _cache_timestamps: Dict[str, float] = {}

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
    items_per_page: int = ITEMS_PER_PAGE

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
    search_customer_id: str = ""

    # Fraud data
    fraud_summary: Dict[str, Any] = {}
    fraud_by_type: List[FraudStat] = []
    fraud_prediction: Dict[str, Any] = {}
    
    # Form Options
    merchant_states: List[str] = US_STATES
    mcc_codes: List[str] = COMMON_MCC_CODES

    # Stats data
    amount_distribution: Dict[str, Any] = {}
    stats_by_type: List[TypeStat] = []
    daily_stats: List[DailyStat] = []

    # ===== CACHE HELPERS =====

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid."""
        if cache_key not in self._cache_timestamps:
            return False
        return (time.time() - self._cache_timestamps[cache_key]) < CACHE_TTL_SECONDS

    def _update_cache_timestamp(self, cache_key: str):
        """Update cache timestamp for a key."""
        self._cache_timestamps[cache_key] = time.time()

    def invalidate_cache(self, cache_key: Optional[str] = None):
        """Invalidate cache for a specific key or all keys."""
        if cache_key:
            self._cache_timestamps.pop(cache_key, None)
        else:
            self._cache_timestamps = {}

    # ===== SETTER METHODS FOR FILTERS =====

    def set_filter_use_chip(self, value: str):
        """Set transaction type filter."""
        self.filter_use_chip = value if value != "All" else ""

    def set_filter_min_amount(self, value: str):
        """Set minimum amount filter."""
        self.filter_min_amount = value

    def set_filter_max_amount(self, value: str):
        """Set maximum amount filter."""
        self.filter_max_amount = value

    def set_filter_merchant_state(self, value: str):
        """Set merchant state filter."""
        self.filter_merchant_state = value

    def set_filter_is_fraud(self, value: str):
        """Set fraud filter from dropdown value."""
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

    # ===== SETTER METHODS FOR CUSTOMERS =====

    def set_search_customer_id(self, value: str):
        """Set search customer ID."""
        self.search_customer_id = value

    def set_customer_profile(self, value: Optional[Dict[str, Any]]):
        """Set customer profile (or clear it)."""
        self.customer_profile = value if value else {}

    def clear_customer_profile(self):
        """Clear customer profile."""
        self.customer_profile = {}

    # ===== DASHBOARD METHODS =====

    async def load_dashboard_data(self):
        """Load all data for dashboard page with caching."""
        # Check if data is already cached and valid
        if (self._is_cache_valid("dashboard") and
            self.stats_overview and
            self.recent_transactions):
            return

        self.is_loading = True
        self.error_message = ""
        try:
            # Load all data in parallel for better performance
            results = await asyncio.gather(
                api_client.get_stats_overview(),
                api_client.get_recent_transactions(RECENT_TRANSACTIONS_LIMIT),
                api_client.get_health(),
                api_client.get_metadata(),
                return_exceptions=True
            )

            # Process results
            if not isinstance(results[0], Exception):
                self.stats_overview = results[0]
            if not isinstance(results[1], Exception):
                self.recent_transactions = [Transaction(**item) for item in results[1]]
            if not isinstance(results[2], Exception):
                self.system_health = results[2]
            if not isinstance(results[3], Exception):
                self.system_metadata = results[3]
                self.system_metadata["version"] = "1.1.0"  # Force version upgrade

            self._update_cache_timestamp("dashboard")
        except Exception as e:
            self.error_message = f"Error loading dashboard: {str(e)}"
        finally:
            self.is_loading = False

    # ===== TRANSACTIONS METHODS =====

    async def load_transactions(self):
        """Load transactions with current filters."""
        self.is_loading = True
        self.error_message = ""
        try:
            # Parse and validate filter values
            min_amt = None
            max_amt = None

            if self.filter_min_amount:
                try:
                    min_amt = float(self.filter_min_amount)
                except ValueError:
                    self.error_message = "Invalid minimum amount"
                    return

            if self.filter_max_amount:
                try:
                    max_amt = float(self.filter_max_amount)
                except ValueError:
                    self.error_message = "Invalid maximum amount"
                    return

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
        """Load available transaction types with caching."""
        if self._is_cache_valid("transaction_types") and self.transaction_types:
            return

        try:
            self.transaction_types = await api_client.get_transaction_types()
            self._update_cache_timestamp("transaction_types")
        except Exception as e:
            self.error_message = f"Error loading transaction types: {str(e)}"

    async def next_page(self):
        """Go to next page of transactions."""
        if self.items_per_page <= 0:
            return
        total_pages = (self.total_transactions + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            await self.load_transactions()

    async def prev_page(self):
        """Go to previous page of transactions."""
        if self.current_page > 1:
            self.current_page -= 1
            await self.load_transactions()

    # ===== CUSTOMERS METHODS =====

    async def load_customers(self):
        """Load customers list with optimizations."""
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
                # Fetch details for each customer in parallel (batched)
                tasks = [api_client.get_customer_profile(cid) for cid in raw_customers]
                customers_data = await asyncio.gather(*tasks, return_exceptions=True)
                # Filter out exceptions
                customers_data = [c for c in customers_data if not isinstance(c, Exception)]
            else:
                customers_data = raw_customers

            # Calculate avg_amount if missing
            for item in customers_data:
                if item and "avg_amount" not in item:
                    count = item.get("transactions_count", 0)
                    total = item.get("total_amount", 0.0)
                    item["avg_amount"] = total / count if count > 0 else 0.0

            self.customers = [Customer(**item) for item in customers_data if item]
            self.total_customers = result.get("total", 0)
        except Exception as e:
            self.error_message = f"Error loading customers: {str(e)}"
        finally:
            self.is_loading = False

    async def next_customers_page(self):
        """Go to next page of customers."""
        if self.items_per_page <= 0:
            return
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
        """Load top customers with caching."""
        if self._is_cache_valid("top_customers") and self.top_customers:
            return

        try:
            top_data = await api_client.get_top_customers(TOP_CUSTOMERS_LIMIT)

            # Check if we got a list of IDs (int) instead of objects
            if top_data and isinstance(top_data[0], int):
                tasks = [api_client.get_customer_profile(cid) for cid in top_data]
                top_data = await asyncio.gather(*tasks, return_exceptions=True)
                top_data = [c for c in top_data if not isinstance(c, Exception)]

            # Calculate avg_amount if missing
            for item in top_data:
                if item and "avg_amount" not in item:
                    count = item.get("transactions_count", 0)
                    total = item.get("total_amount", 0.0)
                    item["avg_amount"] = total / count if count > 0 else 0.0

            self.top_customers = [Customer(**item) for item in top_data if item]
            self._update_cache_timestamp("top_customers")
        except Exception as e:
            self.error_message = f"Error loading top customers: {str(e)}"

    async def search_customer(self):
        """Search for a customer by ID."""
        if not self.search_customer_id:
            self.error_message = "Please enter a customer ID"
            return

        self.is_loading = True
        self.error_message = ""
        try:
            # Validate ID is a number
            try:
                customer_id = int(self.search_customer_id)
            except ValueError:
                self.error_message = "Customer ID must be a number"
                return

            # Direct lookup
            profile = await api_client.get_customer_profile(customer_id)
            if profile:
                self.customer_profile = profile
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
            self.customer_profile = await api_client.get_customer_profile(int(customer_id))
        except Exception as e:
            self.error_message = f"Error loading customer profile: {str(e)}"
        finally:
            self.is_loading = False

    # ===== FRAUD METHODS =====

    async def load_fraud_data(self):
        """Load fraud detection data with caching."""
        if self._is_cache_valid("fraud") and self.fraud_summary:
            return

        self.is_loading = True
        self.error_message = ""
        try:
            # Load both in parallel
            results = await asyncio.gather(
                api_client.get_fraud_summary(),
                api_client.get_fraud_by_type(),
                return_exceptions=True
            )

            if not isinstance(results[0], Exception):
                self.fraud_summary = results[0]
            if not isinstance(results[1], Exception):
                self.fraud_by_type = [FraudStat(**item) for item in results[1]]
            
            # Try to fetch recent transactions to update options if needed
            # We do this silently to improve dropdown options
            try:
                tx_data = await api_client.get_transactions(limit=100)
                transactions = tx_data.get("transactions", [])
                
                # Update states
                found_states = {t.get("merchant_state") for t in transactions if t.get("merchant_state")}
                current_states = set(self.merchant_states)
                new_states = found_states - current_states
                if new_states:
                    self.merchant_states = sorted(list(current_states | new_states))
                
                # Update MCCs
                found_mccs = {str(t.get("mcc")) for t in transactions if t.get("mcc")}
                current_mccs = set(self.mcc_codes)
                new_mccs = found_mccs - current_mccs
                if new_mccs:
                    self.mcc_codes = sorted(list(current_mccs | new_mccs))
            except Exception:
                # Ignore errors here as it's just an enhancement
                pass

            self._update_cache_timestamp("fraud")
        except Exception as e:
            self.error_message = f"Error loading fraud data: {str(e)}"
        finally:
            self.is_loading = False

    async def predict_fraud(
        self,
        amount: float,
        use_chip: str,
        merchant_state: str,
        mcc: int
    ):
        """Predict fraud for given transaction data."""
        self.is_loading = True
        self.error_message = ""
        self.fraud_prediction = {}  # Clear previous prediction
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

    # ===== STATS METHODS =====

    async def load_stats_data(self):
        """Load statistical data with caching."""
        if self._is_cache_valid("stats") and self.amount_distribution:
            return

        self.is_loading = True
        self.error_message = ""
        try:
            # Load all stats in parallel
            results = await asyncio.gather(
                api_client.get_amount_distribution(AMOUNT_DISTRIBUTION_BINS),
                api_client.get_stats_by_type(),
                api_client.get_daily_stats(DAILY_STATS_LIMIT),
                return_exceptions=True
            )

            if not isinstance(results[0], Exception):
                self.amount_distribution = results[0]
            if not isinstance(results[1], Exception):
                self.stats_by_type = [TypeStat(**item) for item in results[1]]
            if not isinstance(results[2], Exception):
                self.daily_stats = [DailyStat(**item) for item in results[2]]

            self._update_cache_timestamp("stats")
        except Exception as e:
            self.error_message = f"Error loading stats: {str(e)}"
        finally:
            self.is_loading = False
