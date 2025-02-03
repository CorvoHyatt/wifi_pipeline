from fastapi import FastAPI, HTTPException
from strawberry.fastapi import GraphQLRouter
from app.schemas.wifi_schema import schema
from app.init_db import init_db
from app.data_importer import main as importar_datos  # Importar la función principal del importador
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from contextlib import asynccontextmanager
import logging

# Configuración del registro de errores
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("🚀 Iniciando la aplicación y configurando la base de datos...")
        await init_db()          # Crear tablas si no existen
        logger.info("✅ Base de datos inicializada correctamente.")
        
        await importar_datos()   # Importar los datos del CSV automáticamente
        logger.info("📊 Datos importados exitosamente.")
        
    except OperationalError as e:
        logger.critical(f"❌ Error de conexión a la base de datos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos.")
    except SQLAlchemyError as e:
        logger.critical(f"⚠️ Error en la base de datos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos.")
    except FileNotFoundError as e:
        logger.critical(f"📂 Archivo CSV no encontrado: {str(e)}")
        raise HTTPException(status_code=500, detail="Archivo CSV no encontrado.")
    except Exception as e:
        logger.critical(f"⚠️ Error inesperado durante el inicio de la aplicación: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado al iniciar la aplicación.")

    yield  # Continúa con la ejecución de la aplicación

# Inicializar la aplicación con el ciclo de vida personalizado
app = FastAPI(lifespan=lifespan)

# Enrutador GraphQL
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Ruta raíz para pruebas rápidas
@app.get("/")
def read_root():
    return {"message": "🌐 API de Puntos WiFi - Visita /graphql para la consola de GraphQL"}
