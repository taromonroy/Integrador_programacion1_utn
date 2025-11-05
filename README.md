![UTN](https://upload.wikimedia.org/wikipedia/commons/6/67/UTN_logo.jpg)

**Proyecto Integrador - Programación I (2025)**
-------
# Visor de Datos de Países

Una aplicación de escritorio en Python para explorar, filtrar y analizar datos de países del mundo, construida con Tkinter y desplegable con Docker.

## Descripción del Proyecto

Este proyecto es una aplicación de escritorio completa, desarrollada en Python, que funciona como un visor interactivo de datos de países.

La aplicación se conecta a la API pública `restcountries.com` para descargar y procesar datos. Durante este proceso, enriquece la información añadiendo la columna `continente` (basada en la región de la API) y consolida todo en un archivo CSV maestro (`Continentes/Todos.csv`).

La interfaz gráfica, construida con **Tkinter**, permite al usuario:
* Visualizar los datos en una tabla limpia.
* Realizar **filtros combinados** (por nombre, continente, rangos de población y superficie).
* **Validar entradas** de usuario para evitar errores (ej. no permite números negativos).
* **Ordenar** los datos por cualquier columna (ascendente o descendente).
* Ver una ventana emergente con **estadísticas globales** (promedios, máximos, conteo, etc.).

El proyecto también incluye un `Dockerfile` para una fácil portabilidad y despliegue.

## 🖱️ Instrucciones de Uso

Tienes dos métodos principales para ejecutar la aplicación:

### A. Ejecución Local (Python)

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
    cd tu-repositorio
    ```
2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  **Instalar dependencias:**
    El único requisito es `requests`.
    ```bash
    pip install -r requirements.txt
    ```
4.  **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```
    *Nota: La primera vez que se ejecute, el script `main.py` detectará que `Todos.csv` no existe, por lo que descargará los datos de la API. Esto puede tardar unos segundos. Las siguientes ejecuciones serán **instantáneas** gracias a la lógica de caché.*

### B. Ejecución con Docker

El `Dockerfile` está configurado para ejecutar la aplicación en un contenedor.

1.  **Construir la imagen de Docker:**
    ```bash
    docker build -t visor-paises .
    ```
2.  **Ejecutar el contenedor (Linux/macOS):**
    * Necesitarás compartir tu X server para que la GUI de Tkinter se muestre desde el contenedor.
    ```bash
    # Permite a Docker conectarse a tu pantalla local
    xhost +local:docker
    
    # Ejecuta el contenedor
    docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix visor-paises
    ```
    *(La configuración para Windows puede requerir un X Server como VcXsrv o XQuartz en macOS).*

## 📸 Características y Funcionalidad

La interfaz principal permite una exploración de datos fluida.

### Filtros Combinados (Entrada)
El panel izquierdo permite al usuario aplicar múltiples filtros que funcionan en conjunto:
* **Por Nombre:** Búsqueda de texto libre.
* **Por Continente:** Un menú desplegable.
* **Por Rango:** Campos de "mínimo" y "máximo" para Población y Superficie, con validación de errores.



### Tabla de Datos (Salida)
La tabla principal se actualiza en tiempo real basado en los filtros aplicados. El usuario puede hacer clic en los botones de "Ordenar" para reorganizar la vista actual.

### Ventana de Estadísticas
Al presionar "Mostrar Estadísticas", la aplicación calcula y muestra un resumen de **todos** los datos (no solo los filtrados):
* País más y menos poblado.
* Promedio de población y superficie.
* Conteo de países por continente.


## 🗃️ Dataset Base (`Todos.csv`)

El archivo `Continentes/Todos.csv` es el dataset maestro que utiliza la aplicación. **No necesitas descargarlo manualmente**, ya que se genera automáticamente por el script `main.py` durante la primera ejecución.

Este archivo consolida los datos de todos los continentes y añade las siguientes columnas clave que se usan en la aplicación:
* `nombre_comun_es`: Nombre común en español.
* `poblacion`: Población.
* `area`: Superficie.
* `continente`: Continente (columna añadida durante el procesamiento).

La aplicación interna luego crea versiones numéricas (`poblacion_num`, `area_num`) en memoria para que los filtros y ordenamientos sean eficientes.
## 📹 Video Explicativo
Link: https://youtu.be/hclPgxYFY6g

## 👥 Integrantes

Este proyecto fue desarrollado por:

* **Benjamin Cajales**
* **Lautaro Monroy** 
