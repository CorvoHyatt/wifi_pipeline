import csv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.models.wifi import WifiPoint
from app.database import get_db
import asyncio

CSV_FILE = "puntos_wifi_cdmx.csv"

# Función para leer el CSV
def leer_csv(archivo):
    with open(archivo, encoding='utf-8') as f:
        return list(csv.DictReader(f))

# Transformar cada fila del CSV en un diccionario listo para la BD
def transformar_fila(fila):
    return {
        "id": fila["id"],
        "programa": fila["programa"],
        "fecha_instalacion": fila["fecha_instalacion"] if fila["fecha_instalacion"] != "NA" else None,
        "latitud": float(fila["latitud"]),
        "longitud": float(fila["longitud"]),
        "colonia": fila["colonia"] or None,
        "alcaldia": fila["alcaldia"] or None
    }

# Importar los datos de forma asincrónica
async def importar_datos(session: AsyncSession, datos):
    # Transformar y filtrar datos válidos
    registros = list(map(transformar_fila, datos))

    # Insertar en la base de datos en lotes
    await session.execute(insert(WifiPoint), registros)
    await session.commit()

# Orquestador principal
async def main():
    datos = leer_csv(CSV_FILE)
    async for session in get_db():
        await importar_datos(session, datos)

if __name__ == "__main__":
    asyncio.run(main())
