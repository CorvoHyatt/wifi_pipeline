# 🌐 API de Puntos WiFi CDMX

Esta API proporciona acceso a los puntos de acceso WiFi de la Ciudad de México. Se ha desarrollado utilizando **FastAPI**, **SQLAlchemy**, **PostgreSQL**, y **GraphQL**.

## 🚀 Características

- **GraphQL API** para consultas flexibles.
- **Base de datos PostgreSQL** para almacenamiento eficiente.
- **Importación automática de datos** desde un archivo CSV.
- **Manejo de errores robusto** para operaciones de base de datos y consultas.
- **Pruebas unitarias** con `pytest` y `httpx`.

---

## 📦 Requisitos

- **Docker** y **Docker Compose** instalados.

## 🚧 Configuración del Entorno

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/CorvoHyatt/wifi_pipeline
   cd api-wifi
   ```

2. Configurar variables de entorno en un archivo `.env`:

   ```env
   DATABASE_URL=postgresql+asyncpg://wifi_user:wifi_pass@db:5432/wifi_db
   ```

3. Asegúrate de que el archivo `puntos_wifi_cdmx.csv` está ubicado en `app/puntos_wifi_cdmx.csv`.

## 🚩 Ejecución del Proyecto

Iniciar la aplicación usando Docker Compose:

```bash
docker-compose up --build
```

Esto:

- Iniciará la API en `http://localhost:8000`
- Inicializará la base de datos.
- Importará los datos desde el CSV automáticamente.

## 🔍 Exploración de la API

Visita [http://localhost:8000/graphql](http://localhost:8000/graphql) para acceder a la consola de GraphQL.

### Ejemplos de Consultas:

1. **Obtener Puntos WiFi:**

   ```graphql
   query {
     puntosWifi(limit: 5, offset: 0) {
       id
       programa
       latitud
       longitud
     }
   }
   ```

2. **Buscar por ID:**

   ```graphql
   query {
     puntosWifiPorId(id: "TEST001") {
       id
       programa
       colonia
     }
   }
   ```

3. **Filtrar por Colonia:**

   ```graphql
   query {
     puntosWifiPorColonia(colonia: "Centro") {
       id
       alcaldia
     }
   }
   ```

4. **Puntos Cercanos:**
   ```graphql
   query {
     puntosWifiCercanos(lat: 19.4326, lon: -99.1332, limit: 10) {
       id
       programa
       latitud
       longitud
     }
   }
   ```

## 🐞 Manejo de Errores

- **Errores de Base de Datos:** Manejo de `OperationalError` y `SQLAlchemyError`.
- **Errores de Archivo:** Control de `FileNotFoundError` para el archivo CSV.
- **Validaciones de Parámetros:** Verificación de latitud y longitud inválidas en consultas.

## 💪 Pruebas Unitarias

Las pruebas están escritas usando `pytest`, `pytest-asyncio` y `httpx`.

### Ejecución de Pruebas:

```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from tests
```

### Estructura de las Pruebas:

- **API:** Pruebas de la raíz de la API.
- **Base de Datos:** Verificación de conexión e inserción de datos.
- **GraphQL:** Pruebas de queries básicas y avanzadas.

## 🌌 Futuras Mejoras

- Implementación de paginación avanzada.
- Autenticación y autorización.
- Deploy en un entorno en la nube.

## 📄 Licencia

Este proyecto está bajo la [MIT License](LICENSE).

## ✨ Autor

- **Desarrollador:** [Tu Nombre]
- **Contacto:** tu-email@ejemplo.com
