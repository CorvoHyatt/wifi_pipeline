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
from typing import Generator, List, Dict, Any, Optional

logger = logging.getLogger(__name__)
load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")
BATCH_SIZE = 1000  # Tamaño del lote

def leer_csv(file_path: str) -> Generator[Dict[str, str], None, None]:
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row
    except FileNotFoundError:
        logger.error(f"❌ No se encontró el archivo CSV en la ruta especificada: {file_path}")
    except Exception as e:
        logger.error(f"❌ Error al leer el archivo CSV: {str(e)}")

def transformar_fila(fila: Dict[str, str]) -> Optional[Dict[str, Any]]:
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

async def async_batch_generator(data: Generator[Dict[str, str], None, None], batch_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    batch = []
    for item in data:
        transformed_item = transformar_fila(item)
        if transformed_item is not None:
            batch.append(transformed_item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

# app/data_importer.py

async def importar_datos(session: AsyncSession, datos: Generator[Dict[str, str], None, None]) -> None:
    try:
        # Verificar si los datos ya han sido importados
        result = await session.execute(select(ImportControl).where(ImportControl.id == True))
        control = result.scalar()

        if control and control.imported:
            logger.info("Los datos ya han sido importados previamente.")
            return

        async for batch in async_batch_generator(datos, BATCH_SIZE):
            await session.execute(insert(WifiPoint), batch)
            await session.commit()

        # Marcar los datos como importados
        if not control:
            control = ImportControl(id=True, imported=True)
            session.add(control)
        else:
            control.imported = True
        await session.commit()

        logger.info("✅ Se importaron los registros correctamente.")

    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Error al insertar datos en la base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado durante la importación: {str(e)}")

async def main() -> None:
    datos = leer_csv(CSV_FILE)
    async for session in get_db():
        await importar_datos(session, datos)
