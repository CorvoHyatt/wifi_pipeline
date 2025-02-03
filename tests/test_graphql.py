import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
@pytest.mark.asyncio
async def test_puntos_wifi_query():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/graphql", json={"query": "{ puntosWifi { id programa } }"})
        assert response.status_code == 200
        assert "data" in response.json()


@pytest.mark.asyncio
async def test_punto_wifi_por_id():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/graphql", json={"query": '{ puntosWifiPorId(id: "TEST001") { id programa } }'})
        assert response.status_code == 200
        assert "data" in response.json()


@pytest.mark.asyncio
async def test_puntos_wifi_por_colonia():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/graphql", json={"query": '{ puntosWifiPorColonia(colonia: "Test Colonia") { id programa } }'})
        assert response.status_code == 200
        assert "data" in response.json()
