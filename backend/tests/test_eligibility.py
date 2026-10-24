import pytest


@pytest.mark.asyncio
async def test_get_scheme_eligibility_questions(client):
    response = await client.get("/schemes/raitha-siri/eligibility")
    assert response.status_code == 200
    data = response.json()
    assert data["scheme_id"] == "raitha-siri"
    assert len(data["questions"]) > 0
    first_q = data["questions"][0]
    assert "question_en" in first_q
    assert "question_kn" in first_q
    assert "question_type" in first_q


@pytest.mark.asyncio
async def test_check_eligibility_qualified(client):
    payload = {
        "answers": {
            "is_karnataka_resident": True,
            "owns_agricultural_land": True,
            "cultivates_millets": True,
            "age": 42,
        }
    }
    response = await client.post("/schemes/raitha-siri/check-eligibility", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "eligible"
    assert "Likely Eligible" in data["status_title_en"]
    assert len(data["document_checklist"]) > 0
    assert len(data["next_steps_en"]) > 0
    assert "preliminary" in data["preliminary_notice_en"].lower()


@pytest.mark.asyncio
async def test_check_eligibility_not_qualified(client):
    # Non-Karnataka resident and does not own land
    payload = {
        "answers": {
            "is_karnataka_resident": False,
            "owns_agricultural_land": False,
            "cultivates_millets": False,
            "age": 42,
        }
    }
    response = await client.post("/schemes/raitha-siri/check-eligibility", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "not_eligible"
    assert len(data["missing_requirements"]) > 0
    assert len(data["reasons_en"]) > 0


@pytest.mark.asyncio
async def test_check_eligibility_missing_mandatory_answers(client):
    # Missing mandatory answers entirely
    payload = {
        "answers": {}
    }
    response = await client.post("/schemes/raitha-siri/check-eligibility", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "more_info_required"
    assert "More Information Required" in data["status_title_en"]
