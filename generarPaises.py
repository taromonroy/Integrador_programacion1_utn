# --- Importaciones de Módulos ---
import requests  # Para realizar peticiones HTTP a la API
import csv       # Para leer y escribir archivos CSV
import os        # Para interactuar con el sistema operativo (crear carpetas, revisar archivos)

def obtener_y_guardar_paises(url, nombre_archivo, carpeta_salida):
    """
    Obtiene datos de la API y los guarda en un CSV dentro de una carpeta específica.
    """
    # --- 1. Preparación del Directorio ---
    
    # Comprueba si la carpeta de salida (ej. "Continentes") no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida) # Si no existe, la crea
        print(f"Carpeta '{carpeta_salida}' creada exitosamente.")

    # Une la ruta de la carpeta y el nombre del archivo (ej. "Continentes/Africa.csv")
    ruta_completa_archivo = os.path.join(carpeta_salida, nombre_archivo)
    
    print(f"Obteniendo datos desde {url}...")
    
    # --- 2. Petición a la API y Manejo de Errores ---
    try:
        # Realiza la petición GET a la URL
        response = requests.get(url) 
        # Si la respuesta es un error (ej. 404, 500), lanza una excepción
        response.raise_for_status()
        
        # Convierte la respuesta JSON (texto) en una lista de diccionarios de Python
        paises = response.json()
        print(f"Se encontraron {len(paises)} territorios. Procesando...")

        # --- 3. Escritura del Archivo CSV ---
        
        # Abre el archivo en modo escritura ('w').
        # newline='' y encoding='utf-8' son buenas prácticas para CSV.
        with open(ruta_completa_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
            
            # Define los nombres de las columnas que queremos en nuestro CSV
            campos = ['nombre_comun_es', 'nombre_oficial_es', 'capital', 'region', 'poblacion', 'area']
            
            # Crea un "escritor" que entiende de diccionarios
            escritor = csv.DictWriter(archivo_csv, fieldnames=campos)
            
            # Escribe la primera fila (la cabecera) con los nombres de los campos
            escritor.writeheader()
            
            # Itera sobre cada país (que es un diccionario) en la lista obtenida de la API
            for pais in paises:
                # Escribe una fila en el CSV
                escritor.writerow({
                    # --- 4. Extracción Segura de Datos ---
                    # Esta es una forma muy segura de acceder a datos anidados.
                    # pais.get('translations', {}) -> Obtiene 'translations' o un dict vacío {} si no existe.
                    # .get('spa', {}) -> Obtiene 'spa' o un dict vacío {} si no existe.
                    # .get('common', 'N/A') -> Obtiene 'common' o 'N/A' si no existe.
                    'nombre_comun_es': pais.get('translations', {}).get('spa', {}).get('common', 'N/A'),
                    'nombre_oficial_es': pais.get('translations', {}).get('spa', {}).get('official', 'N/A'),
                    
                    # La capital puede ser una lista (ej. Sudáfrica). .join() la convierte en un string.
                    # Si no hay capital, .get() devuelve ['N/A'] y .join() convierte eso en 'N/A'.
                    'capital': ', '.join(pais.get('capital', ['N/A'])),
                    
                    'region': pais.get('region', 'N/A'),
                    'poblacion': int(pais.get('population', 0)), #onvierte una población en int
                    'area': int(pais.get('area', 0.0)) # Convierte el área a entero
                })
        print(f"¡Éxito! Los datos han sido guardados en el archivo '{ruta_completa_archivo}'.")
    
    # Maneja errores específicos de la librería 'requests' (ej. no hay internet)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
    # Captura cualquier otro error inesperado
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


def unir_csvs_en_uno(carpeta_entrada, archivo_salida):
    """
    Busca todos los archivos .csv en una carpeta, les añade una columna 'continente',
    y los une en un único archivo.
    """
    
    # Obtiene solo el nombre del archivo de salida (ej. "Todos.csv")
    nombre_archivo_salida = os.path.basename(archivo_salida)
    
    # --- 1. Encontrar los archivos a unir ---
    # Crea una lista de todos los archivos en la 'carpeta_entrada'
    # que cumplan DOS condiciones:
    # 1. Terminan en '.csv'
    # 2. NO son el archivo de salida (para no unir "Todos.csv" consigo mismo)
    archivos_csv_a_unir = [
        f for f in os.listdir(carpeta_entrada)
        if f.endswith('.csv') and f != nombre_archivo_salida
    ]

    if not archivos_csv_a_unir:
        print("No se encontraron archivos de continentes para unir.")
        return # Termina la función si no hay nada que hacer

    print(f"\nUniendo {len(archivos_csv_a_unir)} archivos en '{archivo_salida}'...")
    
    # --- 2. Escribir el archivo CSV unificado ---
    
    # Abre el archivo de salida (ej. "Continentes/Todos.csv") en modo escritura
    with open(archivo_salida, 'w', newline='', encoding='utf-8') as f_salida:
        # Usamos csv.writer (simple) porque vamos a manejar filas como listas
        escritor = csv.writer(f_salida)
        
        # --- 3. Escribir la Cabecera ---
        # Solo necesitamos leer la cabecera del PRIMER archivo (ej. "Africa.csv")
        primer_archivo = os.path.join(carpeta_entrada, archivos_csv_a_unir[0])
        
        with open(primer_archivo, 'r', encoding='utf-8') as f_entrada:
            lector = csv.reader(f_entrada) # Lector simple
            cabecera = next(lector) # Lee la primera línea (la cabecera)
            
            # --- ENRIQUECIMIENTO DE DATOS 1 ---
            # Añade la nueva columna "continente" a la lista de cabeceras
            cabecera.append('continente')
            
            # Escribe la cabecera modificada en el archivo de salida
            escritor.writerow(cabecera)
        
        # --- 4. Procesar y unir todos los archivos ---
        
        # Ahora iteramos sobre TODOS los archivos (incluido el primero)
        for nombre_archivo in archivos_csv_a_unir:
            print(f"  - Procesando y añadiendo: {nombre_archivo}")
            
            # --- ENRIQUECIMIENTO DE DATOS 2 (La parte inteligente) ---
            # Extrae el nombre del continente a partir del nombre del archivo
            # ej. "Europe.csv" -> "Europe"
            continente = nombre_archivo.replace('.csv', '')
            
            ruta_completa = os.path.join(carpeta_entrada, nombre_archivo)
            
            with open(ruta_completa, 'r', encoding='utf-8') as f_entrada:
                lector = csv.reader(f_entrada)
                next(lector) # ¡Importante! Salta la cabecera de este archivo
                
                # Itera sobre cada fila de datos
                for fila in lector:
                    # Añade el nombre del continente al final de la fila
                    fila.append(continente)
                    # Escribe la fila completa en el archivo de salida
                    escritor.writerow(fila)
                    
    print(f"¡Éxito! Archivo '{archivo_salida}' creado correctamente con la columna 'continente'.")