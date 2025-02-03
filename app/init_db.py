import asyncio
from app.database import engine, Base
from app.models.wifi import WifiPoint  # Importar el modelo para que SQLAlchemy lo registre

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Crea las tablas definidas en los modelos
    print("✅ Base de datos inicializada correctamente.")

if __name__ == "__main__":
    asyncio.run(init_db())
