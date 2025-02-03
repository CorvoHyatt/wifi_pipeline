import strawberry
from typing import List, Optional
from sqlalchemy.future import select
from app.database import get_db
from app.models.wifi import WifiPoint
from math import radians, sin, cos, sqrt, atan2


# Tipo GraphQL para los puntos WiFi
@strawberry.type
class WifiPointType:
    uuid: str  # ✅ Se añadió este campo
    id: str
    programa: str
    fecha_instalacion: Optional[str]
    latitud: float
    longitud: float
    colonia: Optional[str]
    alcaldia: Optional[str]


# Distancia Haversine para calcular proximidad entre coordenadas
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# Query principal de GraphQL
@strawberry.type
class Query:

    # 1. Listar puntos WiFi (paginado)
    @strawberry.field
    async def puntos_wifi(self, limit: int = 10, offset: int = 0) -> List[WifiPointType]:
        async for session in get_db():
            result = await session.execute(
                select(WifiPoint).offset(offset).limit(limit)
            )
            return [WifiPointType(**row.to_dict()) for row in result.scalars().all()]

    # 2. Consultar puntos WiFi por ID
    @strawberry.field
    async def puntos_wifi_por_id(self, id: str) -> List[WifiPointType]:
        async for session in get_db():
            result = await session.execute(
                select(WifiPoint).where(WifiPoint.id.ilike(f"%{id}%"))
            )
            puntos = result.scalars().all()
            return [WifiPointType(**p.to_dict()) for p in puntos]

    # 3. Listar puntos WiFi por colonia (paginado)
    @strawberry.field
    async def puntos_wifi_por_colonia(self, colonia: str, limit: int = 10, offset: int = 0) -> List[WifiPointType]:
        async for session in get_db():
            result = await session.execute(
                select(WifiPoint)
                .where(WifiPoint.colonia.ilike(f"%{colonia}%"))
                .offset(offset)
                .limit(limit)
            )
            return [WifiPointType(**row.to_dict()) for row in result.scalars().all()]

    # 4. Listar puntos WiFi ordenados por proximidad
    @strawberry.field
    async def puntos_wifi_cercanos(self, lat: float, lon: float, limit: int = 10) -> List[WifiPointType]:
        async for session in get_db():
            result = await session.execute(select(WifiPoint))
            puntos = result.scalars().all()
            puntos_validos = [p for p in puntos if p.latitud is not None and p.longitud is not None]
            puntos_ordenados = sorted(
                puntos_validos,
                key=lambda p: calcular_distancia(lat, lon, p.latitud, p.longitud)
            )

            return [WifiPointType(**p.to_dict()) for p in puntos_ordenados[:limit]]


# Definición del esquema
schema = strawberry.Schema(Query)
