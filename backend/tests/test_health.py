import pytest


@pytest.mark.asyncio
async def test_health_check_returns_healthy(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "RuralConnect Karnataka" in data["service"]
    assert "database" in data
    assert data["database"]["status"] == "connected"
