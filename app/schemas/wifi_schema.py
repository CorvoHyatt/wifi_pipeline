import strawberry
from typing import List, Optional
from app.services.wifi_service import (
    obtener_puntos_wifi,
    obtener_puntos_wifi_por_id,
    obtener_puntos_wifi_por_colonia,
    obtener_puntos_wifi_cercanos
)

@strawberry.type
class WifiPointType:
    uuid: str
    id: str
    programa: str
    fecha_instalacion: Optional[str]
    latitud: float
    longitud: float
    colonia: Optional[str]
    alcaldia: Optional[str]

@strawberry.type
class Query:

    @strawberry.field
    async def puntos_wifi(self, limit: int = 10, offset: int = 0) -> List[WifiPointType]:
        puntos = await obtener_puntos_wifi(limit, offset)
        return [WifiPointType(**p.to_dict()) for p in puntos]

    @strawberry.field
    async def puntos_wifi_por_id(self, id: str) -> List[WifiPointType]:
        puntos = await obtener_puntos_wifi_por_id(id)
        return [WifiPointType(**p.to_dict()) for p in puntos]

    @strawberry.field
    async def puntos_wifi_por_colonia(self, colonia: str, limit: int = 10, offset: int = 0) -> List[WifiPointType]:
        puntos = await obtener_puntos_wifi_por_colonia(colonia, limit, offset)
        return [WifiPointType(**p.to_dict()) for p in puntos]

    @strawberry.field
    async def puntos_wifi_cercanos(self, lat: float, lon: float, limit: int = 10) -> List[WifiPointType]:
        puntos = await obtener_puntos_wifi_cercanos(lat, lon, limit)
        return [WifiPointType(**p.to_dict()) for p in puntos]

schema = strawberry.Schema(Query)