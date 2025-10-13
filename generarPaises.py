import requests
import csv
import os

def obtener_y_guardar_paises(url, nombre_archivo, carpeta_salida):
    """
    Obtiene datos de la API y los guarda en un CSV dentro de una carpeta específica.
    """
    #verifica si la carpeta existe, si no existe la crea para almacenar los .csv de los paises
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
        print(f"Carpeta '{carpeta_salida}' creada exitosamente.")

    # Creamos la ruta completa del archivo 
    ruta_completa_archivo = os.path.join(carpeta_salida, nombre_archivo)
    
    print(f"Obteniendo datos desde {url}...")
    
    try:
        #envia una solicitud HTTP GET a la url
        response = requests.get(url) 

        #verifica que la solicitud fue exitosa
        response.raise_for_status()
        
        #convierte el cuerpo de la respuesta HTTP de la api a formato JSON
        paises = response.json()
        print(f"Se encontraron {len(paises)} territorios. Procesando...")

        #Abre el archivo CSV 
        # Usamos la variable con la ruta completa para guardar el archivo
        with open(ruta_completa_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
            #Define las columnas que tendra el CSV y un objeto DictWriter
            campos = ['nombre_comun', 'nombre_oficial', 'capital', 'region', 'poblacion', 'area']
            escritor = csv.DictWriter(archivo_csv, fieldnames=campos)
            escritor.writeheader()
            
            #recorre la lista de diccionarios de paises obtenida de la api
            for pais in paises:
                #crea un diccionario con los elementos de la api
                escritor.writerow({
                    'nombre_comun': pais.get('name', {}).get('common', 'N/A'),
                    'nombre_oficial': pais.get('name', {}).get('official', 'N/A'),
                    'capital': ', '.join(pais.get('capital', ['N/A'])),
                    'region': pais.get('region', 'N/A'),
                    'poblacion': pais.get('population', 0),
                    'area': pais.get('area', 0.0)
                })
        print(f"¡Éxito! Los datos han sido guardados en el archivo '{ruta_completa_archivo}'.")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")