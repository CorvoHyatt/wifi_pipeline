from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.schemas.wifi_schema import schema
from app.init_db import init_db
from app.data_importer import main as importar_datos  # Importar la función principal del importador

app = FastAPI()

# Inicializar la base de datos y cargar datos al iniciar la aplicación
@app.on_event("startup")
async def startup_event():
    await init_db()          # Crear tablas si no existen
    await importar_datos()   # Importar los datos del CSV automáticamente

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": "API de Puntos WiFi - Visita /graphql para la consola de GraphQL"}
