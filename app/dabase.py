from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Ahora la URL de la base de datos se obtiene de las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Configuración del motor de la base de datos
engine = create_async_engine(DATABASE_URL, echo=True)

# Sesión de base de datos
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión en los endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
