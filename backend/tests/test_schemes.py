import pytest


@pytest.mark.asyncio
async def test_list_schemes_all(client):
    response = await client.get("/schemes")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] > 0
    assert len(data["items"]) > 0
    first_scheme = data["items"][0]
    assert "name_en" in first_scheme
    assert "name_kn" in first_scheme
    assert "category" in first_scheme


@pytest.mark.asyncio
async def test_filter_schemes_by_category(client):
    response = await client.get("/schemes?category=farmers")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    for item in data["items"]:
        assert item["category"] == "farmers"


@pytest.mark.asyncio
async def test_search_schemes_by_query(client):
    response = await client.get("/schemes?query=Millet")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("millet" in s["name_en"].lower() or "millet" in s["short_description_en"].lower() for s in data["items"])


@pytest.mark.asyncio
async def test_scheme_pagination(client):
    response = await client.get("/schemes?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["items"]) <= 2
    assert data["total_pages"] >= 2


@pytest.mark.asyncio
async def test_get_scheme_by_id_success(client):
    response = await client.get("/schemes/raitha-siri")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "raitha-siri"
    assert "Raitha Siri" in data["name_en"]
    assert len(data["benefits_en"]) > 0
    assert len(data["required_documents"]) > 0


@pytest.mark.asyncio
async def test_get_scheme_not_found(client):
    response = await client.get("/schemes/non-existent-scheme-999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_scheme_documents(client):
    response = await client.get("/schemes/gruha-lakshmi/documents")
    assert response.status_code == 200
    docs = response.json()
    assert isinstance(docs, list)
    assert len(docs) > 0
    assert any("aadhaar" in d["id"].lower() or "ration" in d["id"].lower() for d in docs)
