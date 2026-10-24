import pytest


@pytest.mark.asyncio
async def test_list_service_centers(client):
    response = await client.get("/centers")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] > 0
    assert len(data["districts"]) > 0
    first_center = data["items"][0]
    assert "name_en" in first_center
    assert "address_en" in first_center
    assert "district" in first_center


@pytest.mark.asyncio
async def test_filter_centers_by_district(client):
    response = await client.get("/centers?district=Davanagere")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    for center in data["items"]:
        assert center["district"].lower() == "davanagere"


@pytest.mark.asyncio
async def test_get_center_by_id(client):
    response = await client.get("/centers/grama-one-hebbalu-davangere")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "grama-one-hebbalu-davangere"
    assert "Hebbalu" in data["name_en"]
    assert len(data["services_offered_en"]) > 0


@pytest.mark.asyncio
async def test_center_not_found(client):
    response = await client.get("/centers/non-existent-center-888")
    assert response.status_code == 404
