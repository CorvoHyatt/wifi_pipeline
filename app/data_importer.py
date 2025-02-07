import csv
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert
from app.models.wifi import WifiPoint
from app.models.control import ImportControl
from app.database import get_db
from dotenv import load_dotenv
import logging
import os

logger = logging.getLogger(__name__)
load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")

def leer_csv(file_path):
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]
    except FileNotFoundError:
        logger.error(f"❌ No se encontró el archivo CSV en la ruta especificada: {file_path}")
        return []
    except Exception as e:
        logger.error(f"❌ Error al leer el archivo CSV: {str(e)}")
        return []

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

async def importar_datos(session: AsyncSession, datos):
    try:
        # Verificar si los datos ya han sido importados
        result = await session.execute(select(ImportControl).where(ImportControl.id == True))
        control = result.scalar()

        if control and control.imported:
            logger.info("Los datos ya han sido importados previamente.")
            return

        registros = [r for r in map(transformar_fila, datos) if r is not None]
        await session.execute(insert(WifiPoint),registros)
        await session.commit()

        # Marcar los datos como importados
        if not control:
            control = ImportControl(id=True, imported=True)
            session.add(control)
        else:
            control.imported = True
        await session.commit()

        logger.info(f"✅ Se importaron {len(registros)} registros correctamente.")

    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Error al insertar datos en la base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado durante la importación: {str(e)}")

async def main():
    datos = leer_csv(CSV_FILE)
    if datos:
        async for session in get_db():
            await importar_datos(session, datos)
    else:
        logger.warning("No se encontraron datos para importar.")