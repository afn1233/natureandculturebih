# test_main.py - Unit tests for NatureAndCultureBiH API
# Uses the real PostgreSQL database running in Docker

import pytest
from httpx import AsyncClient, ASGITransport
from main import app
import uuid

@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def test_user(client):
    email = f"test_{uuid.uuid4()}@example.com"
    response = await client.post("/auth/login", json={"email": email})
    return response.json()


# ── Health Check ──────────────────────────────────────────

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ── Auth Tests ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_login_creates_new_user(client):
    email = f"new_{uuid.uuid4()}@example.com"
    response = await client.post("/auth/login", json={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert "id" in data


@pytest.mark.asyncio
async def test_login_returns_existing_user(client):
    email = f"existing_{uuid.uuid4()}@example.com"
    first = await client.post("/auth/login", json={"email": email})
    second = await client.post("/auth/login", json={"email": email})
    assert first.json()["id"] == second.json()["id"]


@pytest.mark.asyncio
async def test_login_invalid_email(client):
    response = await client.post("/auth/login", json={"email": "notanemail"})
    assert response.status_code == 422


# ── Links Tests ───────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_links_empty(client, test_user):
    response = await client.get("/links", headers={"X-User-Id": test_user["id"]})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_link(client, test_user):
    response = await client.post(
        "/links",
        headers={"X-User-Id": test_user["id"]},
        json={"title": "Stari Most", "url": "https://example.com/stari-most", "description": "Famous bridge"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Stari Most"
    assert data["url"] == "https://example.com/stari-most"


@pytest.mark.asyncio
async def test_get_links_after_create(client, test_user):
    await client.post(
        "/links",
        headers={"X-User-Id": test_user["id"]},
        json={"title": "Kravice", "url": "https://example.com/kravice", "description": "Waterfalls"}
    )
    response = await client.get("/links", headers={"X-User-Id": test_user["id"]})
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_update_link(client, test_user):
    create = await client.post(
        "/links",
        headers={"X-User-Id": test_user["id"]},
        json={"title": "Old Title", "url": "https://example.com", "description": "Old"}
    )
    link_id = create.json()["id"]
    response = await client.put(
        f"/links/{link_id}",
        headers={"X-User-Id": test_user["id"]},
        json={"title": "New Title"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


@pytest.mark.asyncio
async def test_delete_link(client, test_user):
    create = await client.post(
        "/links",
        headers={"X-User-Id": test_user["id"]},
        json={"title": "To Delete", "url": "https://example.com/delete", "description": ""}
    )
    link_id = create.json()["id"]
    response = await client.delete(
        f"/links/{link_id}",
        headers={"X-User-Id": test_user["id"]}
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_nonexistent_link(client, test_user):
    fake_id = str(uuid.uuid4())
    response = await client.delete(
        f"/links/{fake_id}",
        headers={"X-User-Id": test_user["id"]}
    )
    assert response.status_code == 404


# ── Webhook Tests ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_webhook_weather(client, test_user):
    create = await client.post(
        "/links",
        headers={"X-User-Id": test_user["id"]},
        json={"title": "Mostar", "url": "https://example.com/mostar", "description": "City"}
    )
    link_id = create.json()["id"]
    response = await client.post(
        "/webhook/weather",
        json={"link_id": link_id, "weather_data": {"temperature": 25, "description": "Sunny"}}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_webhook_invalid_link(client):
    response = await client.post(
        "/webhook/weather",
        json={"link_id": str(uuid.uuid4()), "weather_data": {"temperature": 20}}
    )
    assert response.status_code == 404


# ── MCP Tests ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_mcp_stats(client, test_user):
    response = await client.get(f"/mcp/stats?user_id={test_user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert "total_links" in data
    assert "total_weather_updates" in data


@pytest.mark.asyncio
async def test_mcp_stats_with_links(client, test_user):
    await client.post(
        "/links",
        headers={"X-User-Id": test_user["id"]},
        json={"title": "Sarajevo", "url": "https://example.com/sarajevo", "description": "Capital"}
    )
    response = await client.get(f"/mcp/stats?user_id={test_user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_links"] >= 1
    assert data["most_recent_link"] is not None
