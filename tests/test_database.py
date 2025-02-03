import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.wifi import WifiPoint
import uuid

@pytest.mark.asyncio
async def test_database_connection():
    async for session in get_db():
        assert isinstance(session, AsyncSession)

@pytest.mark.asyncio
async def test_insert_wifi_point():
    async for session in get_db():
        test_point = WifiPoint(
            uuid=str(uuid.uuid4()),
            id="TEST001",
            programa="TEST",
            fecha_instalacion=None,
            latitud=19.4326,
            longitud=-99.1332,
            colonia="Test Colonia",
            alcaldia="Test Alcaldía"
        )

        session.add(test_point)
        await session.commit()

        result = await session.get(WifiPoint, (test_point.uuid, test_point.id))
        assert result is not None
        assert result.id == "TEST001"

        # Limpiar después de la prueba
        await session.delete(result)
        await session.commit()
