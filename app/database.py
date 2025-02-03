from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from dotenv import load_dotenv
import os
import logging

# Configuración del registro de errores
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Leer la URL de la base de datos desde la variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Validación de la URL de la base de datos
if not DATABASE_URL:
    logger.critical("❌ DATABASE_URL no está configurada correctamente en el archivo .env.")
    raise ValueError("DATABASE_URL no está configurada correctamente.")

# Debug: Verificar qué URL está usando la aplicación
logger.info(f"Conectando a la base de datos: {DATABASE_URL}")

# Configuración del motor de la base de datos
try:
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    Base = declarative_base()
except SQLAlchemyError as e:
    logger.critical(f"❌ Error al configurar el motor de la base de datos: {str(e)}")
    raise

# Función para obtener una sesión de la base de datos
async def get_db():
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except OperationalError as e:
        logger.error(f"⚠️ Error de conexión a la base de datos: {str(e)}")
        raise
    except SQLAlchemyError as e:
        logger.error(f"⚠️ Error inesperado con SQLAlchemy: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"⚠️ Error inesperado al obtener la sesión de la base de datos: {str(e)}")
        raise
