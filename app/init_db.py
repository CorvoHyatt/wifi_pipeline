import asyncio
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from app.database import engine, Base
from app.models.wifi import WifiPoint  # Importar el modelo para que SQLAlchemy lo registre
from app.models.control import ImportControl  # Importar el modelo de control de importación
import logging

# Configuración del registro de errores
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def crear_tablas():
    """Crea las tablas definidas en los modelos."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Tablas creadas correctamente.")

async def init_db():
    """Inicializa la base de datos."""
    try:
        logger.info("🚀 Iniciando la inicialización de la base de datos...")
        await crear_tablas()
        logger.info("✅ Inicialización de la base de datos ejecutada correctamente.")
    
    except OperationalError as e:
        logger.error(f"❌ Error de conexión a la base de datos: {str(e)}")
    except SQLAlchemyError as e:
        logger.error(f"⚠️ Error al inicializar la base de datos con SQLAlchemy: {str(e)}")
    except Exception as e:
        logger.error(f"⚠️ Error inesperado durante la inicialización de la base de datos: {str(e)}")

if __name__ == "__main__":
    asyncio.run(init_db())