# --- Importaciones ---
import os  # Para interactuar con el sistema operativo (comprobar si existen archivos, unir rutas)
import interfaz  # Importa el archivo de la interfaz gráfica (interfaz.py)

# Importa SÓLO las dos funciones que necesitamos del archivo 'generarPaises.py'
from generarPaises import obtener_y_guardar_paises, unir_csvs_en_uno

def procesar_todos_los_continentes():
    """
    Esta función se encarga de descargar los datos de la API para CADA continente
    y guardarlos en archivos CSV separados (ej. Africa.csv, Europe.csv).
    """
    # Lista de regiones a descargar desde la API
    continentes = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania', 'Antarctic']
    carpeta_salida = "Continentes" # Dónde se guardarán los CSVs
    
    print("--- INICIANDO PROCESO DE DESCARGA DE DATOS ---")
    
    # Itera sobre cada continente de la lista
    for continente in continentes:
        print(f"\nProcesando {continente}...")
        # Define la URL de la API para ese continente
        url = f"https://restcountries.com/v3.1/region/{continente}"
        # Define el nombre del archivo (ej. "Africa.csv")
        nombre_archivo = f"{continente}.csv"
        # Llama a la función importada para hacer la descarga y guardado
        obtener_y_guardar_paises(url, nombre_archivo, carpeta_salida)
        
    print("\n--- ¡PROCESO DE DESCARGA COMPLETADO! ---")

# --- Punto de Entrada Principal ---
# Este bloque de código se ejecuta SÓLO cuando corres 'python main.py'
if __name__ == "__main__":
    
    # --- Definición de Rutas ---
    carpeta_continentes = "Continentes"
    nombre_archivo_final = "Todos.csv"
    # Crea la ruta completa al archivo que la interfaz usará (ej. "Continentes/Todos.csv")
    ruta_archivo_final = os.path.join(carpeta_continentes, nombre_archivo_final)
    
    # --- LÓGICA DE CACHÉ (Modificación Clave) ---
    
    # Comprueba si el archivo 'Todos.csv' NO existe en la carpeta 'Continentes'
    if not os.path.exists(ruta_archivo_final):
        # Si no existe, ejecuta el proceso de descarga y unión
        print(f"No se encontró el archivo '{ruta_archivo_final}'.")
        
        # PASO 1: Llama a la función para descargar todos los CSV individuales
        procesar_todos_los_continentes()
        
        # PASO 2: Llama a la función para unirlos en 'Todos.csv'
        unir_csvs_en_uno(carpeta_continentes, ruta_archivo_final)
        
        print("\n--- ¡Archivos de datos generados! ---")
    else:
        # Si el archivo 'Todos.csv' YA existe, se salta los pasos 1 y 2.
        # Esto hace que la app inicie instantáneamente en usos futuros.
        print(f"Cargando datos existentes desde '{ruta_archivo_final}'...")
    
    # --- PASO FINAL (Se ejecuta siempre) ---
    
    # Lanza la aplicación gráfica llamando a la función principal de 'interfaz.py'
    print("Iniciando interfaz gráfica...")
    interfaz.iniciar_interfaz()