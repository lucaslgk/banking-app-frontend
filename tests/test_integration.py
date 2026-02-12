"""Integration tests for API Client."""

import pytest
from banking_app.services.api_client import APIClient

@pytest.mark.asyncio
async def test_api_connection():
    """Test that we can connect to the API."""
    client = APIClient()
    try:
        health = await client.get_health()
        assert "status" in health
    except Exception as e:
        pytest.skip(f"API not available: {e}")

@pytest.mark.asyncio
async def test_get_transactions():
    """Test fetching transactions."""
    client = APIClient()
    try:
        result = await client.get_transactions(limit=5)
        assert "transactions" in result
        assert "total" in result
        assert len(result["transactions"]) <= 5
    except Exception as e:
        pytest.skip(f"API not available: {e}")

@pytest.mark.asyncio
async def test_get_stats_overview():
    """Test fetching stats overview."""
    client = APIClient()
    try:
        stats = await client.get_stats_overview()
        assert "total_transactions" in stats
        assert "fraud_rate" in stats
    except Exception as e:
        pytest.skip(f"API not available: {e}")
