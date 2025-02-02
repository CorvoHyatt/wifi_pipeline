import csv
from functools import reduce

CSV_FILE = "puntos_wifi_cdmx.csv"

# Leer CSV
def leer_csv(archivo):
    with open(archivo, encoding='utf-8') as f:
        return list(csv.DictReader(f))

# Verificar nombres de columnas y ejemplos de datos
def analizar_datos(datos, n=5):
    if not datos:
        return "No hay datos disponibles."

    # Mostrar columnas exactas
    columnas = list(datos[0].keys())
    print(f"Columnas detectadas: {columnas}\n")

    # Mostrar algunas filas de ejemplo
    print("Primeros registros del dataset:")
    for fila in datos[:n]:
        print(fila)

# Intentar filtrar registros con coordenadas válidas
def filtrar_validos(datos):
    return list(filter(lambda x: x.get('latitud') and x.get('longitud'), datos))

# Resumen del análisis
def resumen(datos):
    registros_totales = len(datos)
    registros_validos = len(filtrar_validos(datos))

    return {
        "Total de registros": registros_totales,
        "Registros con coordenadas": registros_validos,
    }

# Ejecutar análisis
if __name__ == "__main__":
    datos = leer_csv(CSV_FILE)
    analizar_datos(datos)
    print("\nResumen de coordenadas:")
    print(resumen(datos))
