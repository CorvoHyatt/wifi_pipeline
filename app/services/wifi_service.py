# app/services/wifi_service.py
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.models.wifi import WifiPoint
from math import radians, sin, cos, sqrt, atan2

# Función para calcular la distancia Haversine
def calcular_distancia(lat1, lon1, lat2, lon2):
	R = 6371  # Radio de la Tierra en km
	dlat = radians(lat2 - lat1)
	dlon = radians(lon2 - lon1)
	a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	return R * c

# Servicio para obtener puntos WiFi con paginación
async def obtener_puntos_wifi(limit: int = 10, offset: int = 0):
	try:
		if limit < 0 or offset < 0:
			raise ValueError("Los parámetros 'limit' y 'offset' deben ser mayores o iguales a 0.")

		async for session in get_db():
			result = await session.execute(
				select(WifiPoint).offset(offset).limit(limit)
			)
			return result.scalars().all()
	except (ValueError, SQLAlchemyError) as e:
		raise Exception(f"Error al obtener los puntos WiFi: {str(e)}")

# Servicio para obtener puntos WiFi por ID
async def obtener_puntos_wifi_por_id(id: str):
	try:
		if not id:
			raise ValueError("El parámetro 'id' no puede estar vacío.")
		async for session in get_db():
			result = await session.execute(
				select(WifiPoint).where(WifiPoint.id.ilike(f"%{id}%"))
			)
			return result.scalars().all()
	except (ValueError, SQLAlchemyError) as e:
				raise Exception(f"Error al buscar el punto WiFi por ID: {str(e)}")

# Servicio para obtener puntos WiFi por colonia con paginación
async def obtener_puntos_wifi_por_colonia(colonia: str, limit: int = 10, offset: int = 0):
	try:
		if not colonia:
			raise ValueError("El parámetro 'colonia' no puede estar vacío.")
		if limit < 0 or offset < 0:
			raise ValueError("Los parámetros 'limit' y 'offset' deben ser mayores o iguales a 0.")
            
		
		async for session in get_db():
			result = await session.execute(
				select(WifiPoint)
				.where(WifiPoint.colonia.ilike(f"%{colonia}%"))
				.offset(offset)
				.limit(limit)
			)
			return result.scalars().all()
	except (ValueError, SQLAlchemyError) as e:
		raise Exception(f"Error al buscar puntos WiFi por colonia: {str(e)}")

# Servicio para obtener puntos WiFi cercanos
async def obtener_puntos_wifi_cercanos(lat: float, lon: float, limit: int = 10):
	try:
		if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
			raise ValueError("Las coordenadas de latitud y longitud no son válidas.")

		async for session in get_db():
			result = await session.execute(select(WifiPoint))
			puntos = result.scalars().all()

			puntos_validos = [p for p in puntos if p.latitud is not None and p.longitud is not None]
			puntos_ordenados = sorted(
				puntos_validos,
				key=lambda p: calcular_distancia(lat, lon, p.latitud, p.longitud)
			)
			return puntos_ordenados[:limit]
	except (ValueError, SQLAlchemyError) as e:
		raise Exception(f"Error al obtener puntos WiFi cercanos: {str(e)}")