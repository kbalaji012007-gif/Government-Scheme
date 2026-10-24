import pytest
import uuid


@pytest.mark.asyncio
async def test_register_and_login_flow(client):
    unique_email = f"citizen_{uuid.uuid4().hex[:8]}@test.ruralconnect.karnataka.gov.in"
    reg_payload = {
        "email": unique_email,
        "password": "StrongSecretPassword123!",
        "full_name": "Siddaramaiah Pujar",
        "preferred_language": "kn",
    }

    # 1. Register
    reg_resp = await client.post("/auth/register", json=reg_payload)
    assert reg_resp.status_code == 200
    reg_data = reg_resp.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == unique_email.lower()
    token = reg_data["access_token"]

    # 2. Get profile /auth/me with Bearer token
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = await client.get("/auth/me", headers=headers)
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["email"] == unique_email.lower()
    assert me_data["full_name"] == "Siddaramaiah Pujar"

    # 3. Login with credentials
    login_payload = {
        "email": unique_email,
        "password": "StrongSecretPassword123!",
    }
    login_resp = await client.post("/auth/login", json=login_payload)
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()


@pytest.mark.asyncio
async def test_duplicate_registration_rejected(client):
    unique_email = f"dup_{uuid.uuid4().hex[:8]}@test.karnataka.gov.in"
    payload = {
        "email": unique_email,
        "password": "Password123!",
        "full_name": "Test Citizen",
        "preferred_language": "en",
    }
    # First registration
    resp1 = await client.post("/auth/register", json=payload)
    assert resp1.status_code == 200

    # Duplicate registration
    resp2 = await client.post("/auth/register", json=payload)
    assert resp2.status_code == 400
    assert "already exists" in resp2.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_invalid_password_rejected(client):
    login_payload = {
        "email": "citizen@ruralconnect.karnataka.gov.in",
        "password": "CompletelyWrongPassword123",
    }
    resp = await client.post("/auth/login", json=login_payload)
    assert resp.status_code == 401
    assert "invalid email or password" in resp.json()["detail"].lower()
