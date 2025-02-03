# 📱 WiFi CDMX Data Pipeline

Este proyecto es un **data pipeline** diseñado para procesar y exponer información sobre los puntos de acceso WiFi en la Ciudad de México. La API está construida con **FastAPI**, **GraphQL** (Strawberry), y utiliza **PostgreSQL** para el almacenamiento de datos. Todo el entorno se gestiona con **Docker** y **Docker Compose**.

## 🚀 Características

- Procesamiento de datos de puntos WiFi desde un archivo CSV.
- Almacenamiento en una base de datos PostgreSQL.
- API GraphQL para consultas flexibles.
- Consultas optimizadas por proximidad geográfica utilizando la fórmula de Haversine.

---

## 👤 Estructura del Proyecto

```
wifi_pipeline/
├── app/
│   ├── models/              # Definición de modelos de la base de datos
│   ├── schemas/             # Esquema de GraphQL
│   ├── database.py          # Configuración de la base de datos
│   ├── data_importer.py     # Script para importar datos desde CSV
│   └── main.py              # Configuración principal de FastAPI
├── puntos_wifi_cdmx.csv     # Dataset de puntos WiFi
├── Dockerfile               # Imagen de la API
├── docker-compose.yml       # Orquestación de contenedores
└── requirements.txt         # Dependencias del proyecto
```

---

## ⚙️ Configuración y Ejecución

### 1️⃣ Prerrequisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 2️⃣ Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/wifi_pipeline.git
cd wifi_pipeline
```

### 3️⃣ Configurar Variables de Entorno

Asegúrate de tener un archivo `.env` (o variables configuradas en `docker-compose.yml`):

```env
POSTGRES_USER=wifi_user
POSTGRES_PASSWORD=wifi_pass
POSTGRES_DB=wifi_db
```

### 4️⃣ Construir y Ejecutar el Proyecto

```bash
docker-compose up --build
```

Esto inicializará:

- **PostgreSQL** en `localhost:5432`
- **API GraphQL** en `http://localhost:8000/graphql`

---

## 📃 API GraphQL

Accede a la interfaz de GraphQL (GraphQL Playground) en:

```
http://localhost:8000/graphql
```

### 📍 Ejemplos de Consultas

#### 1️⃣ Obtener Puntos WiFi (paginado)

```graphql
query {
  puntosWifi(limit: 5, offset: 0) {
    uuid
    id
    programa
    latitud
    longitud
    colonia
    alcaldia
  }
}
```

#### 2️⃣ Buscar por ID

```graphql
query {
  puntoWifiPorId(id: "AICMT1-GW001") {
    uuid
    programa
    latitud
    longitud
    alcaldia
  }
}
```

#### 3️⃣ Puntos WiFi por Colonia

```graphql
query {
  puntosWifiPorColonia(colonia: "CENTRO", limit: 5) {
    id
    programa
    colonia
    alcaldia
  }
}
```

#### 4️⃣ Puntos WiFi Cercanos

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

---

## 📝 Consideraciones Técnicas

- Los datos inválidos (latitud/longitud `null` o incorrectos) son filtrados automáticamente.
- Se utiliza la fórmula de Haversine para cálculos de proximidad geográfica.
- El contenedor de la base de datos PostgreSQL se inicializa automáticamente con la estructura y datos.

---

## 🙋‍♂️ Tecnologías Utilizadas

- **Python 3.10**
- **FastAPI** + **Strawberry GraphQL**
- **PostgreSQL** + **SQLAlchemy (Async)**
- **Docker** & **Docker Compose**

---

## 🙋‍♂️ Contribuciones

Las contribuciones son bienvenidas. Puedes abrir un _pull request_ o reportar problemas a través de _issues_.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.
