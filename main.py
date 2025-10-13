from generarPaises import obtener_y_guardar_paises

def procesar_todos_los_continentes():

    # 1. Definimos todos los continentes.
    continentes = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania', 'Antarctic']
    
    # 2. Definimos la carpeta donde se va a alojar.
    carpeta_salida = "Continentes"

    # 3. Recorremos la lista por continentes.
    print("Iniciando la descarga de países por continente...")
    
    for continente in continentes:
        print(" ")
        print(f"--- Procesando {continente} ---")
        
        # 4. Construimos la URL y el nombre del archivo dinámicamente.
        url = f"https://restcountries.com/v3.1/region/{continente}"
        nombre_archivo = f"{continente}.csv"
        
        # 5. Llamamos a la función importada con los datos de este continente.
        obtener_y_guardar_paises(url, nombre_archivo, carpeta_salida)
        print(" ")
    print("\n¡Proceso completado!")

if __name__ == "__main__":
    procesar_todos_los_continentes()