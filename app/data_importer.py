import csv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from app.models.wifi import WifiPoint
from app.database import get_db
import asyncio
import logging

# Configuración del registro de errores
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CSV_FILE = "app/puntos_wifi_cdmx.csv"

# Función para leer el CSV
def leer_csv(archivo):
    try:
        with open(archivo, encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        logger.error(f"El archivo '{archivo}' no se encontró.")
        return []
    except Exception as e:
        logger.error(f"Error al leer el archivo CSV: {str(e)}")
        return []

# Transformar cada fila del CSV en un diccionario listo para la BD
def transformar_fila(fila):
    try:
        latitud = float(fila["latitud"]) if fila["latitud"] not in ("NA", "", None) else None
        longitud = float(fila["longitud"]) if fila["longitud"] not in ("NA", "", None) else None

        if latitud is None or longitud is None:
            raise ValueError("Coordenadas inválidas (latitud/longitud faltantes).")

        return {
            "id": fila["id"],
            "programa": fila["programa"],
            "fecha_instalacion": fila["fecha_instalacion"] if fila["fecha_instalacion"] != "NA" else None,
            "latitud": latitud,
            "longitud": longitud,
            "colonia": fila["colonia"] or None,
            "alcaldia": fila["alcaldia"] or None
        }
    except (ValueError, KeyError) as e:
        logger.warning(f"Fila inválida: {fila} - Error: {str(e)}")
        return None  # Ignorar filas con errores

# Importar los datos de forma asincrónica
async def importar_datos(session: AsyncSession, datos):
    try:
        registros = [r for r in map(transformar_fila, datos) if r is not None]  # Filtrar registros válidos

        if not registros:
            logger.warning("No hay registros válidos para importar.")
            return

        await session.execute(insert(WifiPoint), registros)
        await session.commit()

        logger.info(f"✅ Se importaron los registros correctamente.")

    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Error al insertar datos en la base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado durante la importación: {str(e)}")

# Orquestador principal
async def main():
    datos = leer_csv(CSV_FILE)
    if datos:
        async for session in get_db():
            await importar_datos(session, datos)
    else:
        logger.warning("No se encontraron datos para importar.")

if __name__ == "__main__":
    asyncio.run(main())
