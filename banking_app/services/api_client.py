"""API Client for Banking Transactions API."""

import httpx
from typing import Optional, Dict, Any, List


class APIClient:
    """Client for interacting with Banking Transactions API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize API client.
        
        Args:
            base_url: Base URL of the API (default: http://localhost:8000)
        """
        self.base_url = base_url
        self.timeout = 30.0
    
    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request to API.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            JSON response as dictionary
            
        Raises:
            httpx.HTTPError: If request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
    
    async def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request to API.
        
        Args:
            endpoint: API endpoint path
            data: JSON data to send
            
        Returns:
            JSON response as dictionary
            
        Raises:
            httpx.HTTPError: If request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
    
    async def _delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request to API.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            JSON response as dictionary
            
        Raises:
            httpx.HTTPError: If request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.delete(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            return response.json()
    
    # ===== TRANSACTIONS (8 routes) =====
    
    async def get_transactions(
        self,
        page: int = 1,
        limit: int = 50,
        use_chip: Optional[str] = None,
        is_fraud: Optional[int] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        merchant_state: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get paginated list of transactions.
        
        Args:
            page: Page number (default: 1)
            limit: Items per page (default: 50, max: 100)
            use_chip: Filter by transaction method
            is_fraud: Filter by fraud status (0 or 1)
            min_amount: Minimum transaction amount
            max_amount: Maximum transaction amount
            merchant_state: Filter by merchant state
            
        Returns:
            TransactionList with pagination info
        """
        params = {"page": page, "limit": limit}
        if use_chip:
            params["use_chip"] = use_chip
        if is_fraud is not None:
            params["isFraud"] = is_fraud
        if min_amount is not None:
            params["min_amount"] = min_amount
        if max_amount is not None:
            params["max_amount"] = max_amount
        if merchant_state:
            params["merchant_state"] = merchant_state
        
        return await self._get("/api/transactions", params)
    
    async def get_transaction_types(self) -> List[str]:
        """Get list of available transaction types.
        
        Returns:
            List of transaction types (e.g., ['Swipe Transaction', 'Chip Transaction', 'Online Transaction'])
        """
        return await self._get("/api/transactions/types")
    
    async def get_recent_transactions(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get N most recent transactions.
        
        Args:
            n: Number of recent transactions (default: 10, max: 100)
            
        Returns:
            List of recent transactions
        """
        return await self._get("/api/transactions/recent", {"n": n})
    
    async def search_transactions(
        self,
        criteria: Dict[str, Any],
        page: int = 1,
        limit: int = 50
    ) -> Dict[str, Any]:
        """Search transactions with multiple criteria.
        
        Args:
            criteria: Search criteria dictionary
            page: Page number
            limit: Items per page
            
        Returns:
            TransactionList with matching transactions
        """
        params = {"page": page, "limit": limit}
        return await self._post("/api/transactions/search", criteria)
    
    async def get_transactions_by_customer(
        self,
        customer_id: int,
        page: int = 1,
        limit: int = 50
    ) -> Dict[str, Any]:
        """Get transactions by a specific customer.
        
        Args:
            customer_id: Customer identifier
            page: Page number
            limit: Items per page
            
        Returns:
            TransactionList for this customer
        """
        params = {"page": page, "limit": limit}
        return await self._get(f"/api/transactions/by-customer/{customer_id}", params)
    
    async def get_transactions_to_customer(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get transactions received by a customer.
        
        Note: Returns empty list for this dataset (no customer-to-customer transactions).
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            List of transactions (empty for this dataset)
        """
        return await self._get(f"/api/transactions/to-customer/{customer_id}")
    
    async def get_transaction_by_id(self, transaction_id: str) -> Dict[str, Any]:
        """Get transaction details by ID.
        
        Args:
            transaction_id: Transaction identifier
            
        Returns:
            Transaction details
        """
        return await self._get(f"/api/transactions/{transaction_id}")
    
    async def delete_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """Delete a transaction (test mode only).
        
        Args:
            transaction_id: Transaction identifier
            
        Returns:
            Status message
        """
        return await self._delete(f"/api/transactions/{transaction_id}")
    
    # ===== CUSTOMERS (3 routes) =====
    
    async def get_customers(self, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        """Get paginated list of customers.
        
        Args:
            page: Page number
            limit: Items per page
            
        Returns:
            CustomerList with pagination info
        """
        return await self._get("/api/customers", {"page": page, "limit": limit})
    
    async def get_top_customers(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get top customers by transaction volume.
        
        Args:
            n: Number of top customers (default: 10, max: 100)
            
        Returns:
            List of top customers
        """
        return await self._get("/api/customers/top", {"n": n})
    
    async def get_customer_profile(self, customer_id: int) -> Dict[str, Any]:
        """Get customer profile with transaction summary.
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            Customer profile with stats
        """
        return await self._get(f"/api/customers/{customer_id}")
    
    # ===== STATS (4 routes) =====
    
    async def get_stats_overview(self) -> Dict[str, Any]:
        """Get overall statistics of the dataset.
        
        Returns:
            Overall statistics including total transactions, fraud rate, etc.
        """
        return await self._get("/api/stats/overview")
    
    async def get_amount_distribution(self, bins: int = 10) -> Dict[str, Any]:
        """Get distribution of transaction amounts.
        
        Args:
            bins: Number of histogram bins (default: 10, range: 5-50)
            
        Returns:
            Distribution with bin labels and counts
        """
        return await self._get("/api/stats/amount-distribution", {"bins": bins})
    
    async def get_stats_by_type(self) -> List[Dict[str, Any]]:
        """Get statistics grouped by transaction type.
        
        Returns:
            List of statistics for each transaction type
        """
        return await self._get("/api/stats/by-type")
    
    async def get_daily_stats(self, limit: int = 30) -> List[Dict[str, Any]]:
        """Get statistics grouped by day.
        
        Args:
            limit: Maximum number of days to return (default: 30, 0 for all)
            
        Returns:
            List of daily statistics
        """
        return await self._get("/api/stats/daily", {"limit": limit})
    
    # ===== FRAUD (3 routes) =====
    
    async def get_fraud_summary(self) -> Dict[str, Any]:
        """Get fraud detection summary.
        
        Returns:
            Summary of fraud statistics
        """
        return await self._get("/api/fraud/summary")
    
    async def get_fraud_by_type(self) -> List[Dict[str, Any]]:
        """Get fraud statistics by transaction type.
        
        Returns:
            List of fraud rates and counts for each transaction type
        """
        return await self._get("/api/fraud/by-type")
    
    async def predict_fraud(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict if a transaction is fraudulent.
        
        Args:
            data: Transaction data (amount, use_chip, merchant_state, mcc)
            
        Returns:
            Prediction result with fraud probability
        """
        return await self._post("/api/fraud/predict", data)
    
    # ===== SYSTEM (2 routes) =====
    
    async def get_health(self) -> Dict[str, Any]:
        """Check system health status.
        
        Returns:
            System health information
        """
        return await self._get("/api/system/health")
    
    async def get_metadata(self) -> Dict[str, Any]:
        """Get system metadata.
        
        Returns:
            System metadata including version, endpoint count, etc.
        """
        return await self._get("/api/system/metadata")
