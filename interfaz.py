# --- Importaciones de Módulos ---
import tkinter as tk
from tkinter import ttk, messagebox # ttk para widgets modernos, messagebox para pop-ups
import csv
import os
from collections import Counter # Para contar países por continente en estadísticas

# --- Variables Globales ---
# Estas variables deben ser globales para ser accesibles desde diferentes funciones

estado_orden = {}     # Un diccionario para recordar el estado de orden (asc/desc) de cada columna
dataset_paises = []     # La "Lista Maestra". Se carga 1 vez desde el CSV y NUNCA se modifica.
dataset_mostrado = [] # La "Lista de Vista". Es la que se muestra en la tabla y se modifica (filtra, ordena).

# --- Widgets Globales ---
# Se definen como None y se asignan en 'iniciar_interfaz'
campo_busqueda = None
tree = None             # El widget de la tabla (Treeview)
combo_ordenar = None
combo_filtrar = None 
ventana = None          # La ventana principal de la aplicación

# Variables para los widgets de filtro por rango
campo_min_poblacion = None 
campo_max_poblacion = None 
campo_min_superficie = None 
campo_max_superficie = None

# --- Funciones de Datos y Lógica ---

def cargar_datos_en_memoria(archivo_csv):
    """
    Lee el archivo CSV especificado y lo carga en una lista de diccionarios.
    También convierte los campos de población y área a números para eficiencia.
    """
    dataset = []
    try:
        if not os.path.exists(archivo_csv): raise FileNotFoundError
        
        with open(archivo_csv, mode='r', encoding='utf-8') as archivo:
            lector_csv = csv.DictReader(archivo)
            for fila in lector_csv:
                dataset.append(fila)
        
        # --- Conversión de eficiencia ---
        # Convertimos los campos numéricos UNA SOLA VEZ al cargar.
        # Esto evita tener que convertirlos en CADA ordenamiento o CADA cálculo de estadísticas.
        # Los guardamos en nuevas claves (ej. 'poblacion_num') para no perder el original (texto).
        for pais in dataset:
            try: 
                pais['poblacion_num'] = int(pais.get('poblacion', 0))
            except: 
                pais['poblacion_num'] = 0 # Valor por defecto si falla
            try: 
                pais['area_num'] = int(pais.get('area', 0))
            except: 
                pais['area_num'] = 0 # Valor por defecto si falla

        return dataset
    
    except FileNotFoundError: 
        messagebox.showerror("Error", f"No se encontró el archivo de datos:\n{archivo_csv}")
        return None
    except Exception as e: 
        messagebox.showerror("Error", f"Ocurrió un error al leer el archivo: {e}")
        return None

def mostrar_datos_en_treeview(dataset, columnas):
    """
    Limpia el Treeview (la tabla) y lo rellena con los datos del 'dataset' proporcionado.
    """
    # Borra todos los elementos actuales de la tabla
    tree.delete(*tree.get_children()) 
    if not dataset: return # Si no hay datos, no hagas nada
    
    # Itera sobre el dataset (que es una lista de diccionarios)
    for fila_dict in dataset:
        # Crea una lista de valores en el orden correcto de las columnas
        valores = [fila_dict.get(col, '') for col in columnas]
        # Inserta la fila en la tabla
        tree.insert("", "end", values=valores)

def ordenar_columna(col, dataset_local, columnas):
    """
    Ordena la lista 'dataset_local' (que es 'dataset_mostrado') por la columna 'col'.
    Alterna entre ascendente y descendente.
    """
    global estado_orden
    
    # Revisa el estado de orden actual para esa columna (default: False = ascendente)
    es_descendente = estado_orden.get(col, False)
    # Invierte el estado para el próximo clic y lo guarda
    estado_orden = {col: not es_descendente}
    
    def clave_orden(item):
        """Función interna para decirle a .sort() CÓMO ordenar."""
        
        # --- Ordenamiento eficiente ---
        # Si la columna es población o área, usa los campos numéricos
        # que ya convertimos en 'cargar_datos_en_memoria'.
        if col == 'poblacion': 
            return item.get('poblacion_num', 0)
        elif col == 'area': 
            return item.get('area_num', 0)
        
        # Para texto (Nombre, Continente), ordena alfabéticamente en minúsculas
        valor = item.get(col, '')
        return str(valor).lower()
        
    # Ordena la lista 'dataset_mostrado' "in-place" (la modifica directamente)
    dataset_local.sort(key=clave_orden, reverse=es_descendente) 
    
    # Actualiza la tabla con la lista ya ordenada
    mostrar_datos_en_treeview(dataset_local, columnas)

def ordenar_desde_controles():
    """
    Función que se llama al presionar el botón "Ordenar".
    Lee el valor del Combobox y llama a 'ordenar_columna'.
    """
    # Mapea el texto del Combobox (ej. "Nombre") al nombre real de la columna (ej. "nombre_comun_es")
    mapa_columnas = {"Nombre": "nombre_comun_es", "Población": "poblacion", "Superficie": "area", "Continente": "continente"}
    
    opcion_elegida = combo_ordenar.get()
    if not opcion_elegida: 
        messagebox.showwarning("Aviso", "Por favor, selecciona un criterio para ordenar.")
        return
        
    columna_a_ordenar = mapa_columnas[opcion_elegida]
    columnas_visibles = list(mapa_columnas.values())
    
    # Llama a la función de ordenamiento, pasándole la lista que se está mostrando
    ordenar_columna(columna_a_ordenar, dataset_mostrado, columnas_visibles)

def mostrar_ventana_estadisticas():
    """
    Calcula estadísticas a partir de la "Lista Maestra" (dataset_paises)
    y las muestra en una nueva ventana emergente (Toplevel).
    """
    if not dataset_paises: 
        messagebox.showinfo("Estadísticas", "No hay datos cargados.")
        return
        
    try:
        # --- CORRECCIÓN CLAVE ---
        # El bucle 'for' que convertía a float FUE ELIMINADO.
        # Ya no es necesario convertir aquí, porque 'cargar_datos_en_memoria'
        # ya creó los campos 'poblacion_num' y 'area_num' (como int).
        
        # Usamos los campos _num (que son enteros) para todos los cálculos.
        # Se usa 'dataset_paises' para que las estadísticas sean SIEMPRE globales.
        pais_max_pob = max(dataset_paises, key=lambda p: p['poblacion_num']); 
        pais_min_pob = min(dataset_paises, key=lambda p: p['poblacion_num'])
        total_paises = len(dataset_paises)
        promedio_poblacion = sum(p['poblacion_num'] for p in dataset_paises) / total_paises
        promedio_superficie = sum(p['area_num'] for p in dataset_paises) / total_paises
        # Counter crea un diccionario contando cuántas veces aparece cada continente
        conteo_continentes = Counter(p['continente'] for p in dataset_paises)

    except (ValueError, TypeError) as e: 
        messagebox.showerror("Error de Datos", f"No se pudieron calcular las estadísticas.\nError: {e}")
        return
    
    # --- Creación de la Ventana Emergente ---
    ventana_stats = tk.Toplevel(ventana) # 'Toplevel' es una ventana hija
    ventana_stats.title("Estadísticas Globales")
    ventana_stats.geometry("525x400")
    ventana_stats.resizable(False, False)
    
    frame_stats = ttk.Frame(ventana_stats, padding="10")
    frame_stats.pack(fill="both", expand=True)
    
    ttk.Label(frame_stats, text="Estadísticas de Países", font=("Helvetica", 14, "bold")).pack(pady=(0,10))
    frame_resultados = ttk.Frame(frame_stats); frame_resultados.pack(fill="x")
    
    # Función interna para no repetir código al crear líneas de texto
    def crear_linea_stat(parent, etiqueta, valor):
        ttk.Label(parent, text=etiqueta, font=("Helvetica", 10, "bold")).grid(row=parent.grid_size()[1], column=0, sticky="w", pady=2)
        ttk.Label(parent, text=valor).grid(row=parent.grid_size()[1]-1, column=1, sticky="w", padx=5)
    
    # Se añaden las estadísticas al frame (usando .format() para los números)
    crear_linea_stat(frame_resultados, "País más poblado:", f"{pais_max_pob['nombre_comun_es']} ({pais_max_pob['poblacion_num']:,.0f})".replace(',', '.'))
    crear_linea_stat(frame_resultados, "País menos poblado:", f"{pais_min_pob['nombre_comun_es']} ({pais_min_pob['poblacion_num']:,.0f})".replace(',', '.'))
    crear_linea_stat(frame_resultados, "Promedio de población:", f"{promedio_poblacion:,.0f}".replace(',', '.'))
    crear_linea_stat(frame_resultados, "Promedio de superficie:", f"{promedio_superficie:,.2f} km²".replace(',', '.'))
    
    ttk.Separator(frame_stats, orient='horizontal').pack(fill='x', pady=10)
    
    ttk.Label(frame_stats, text="Países por Continente", font=("Helvetica", 12, "bold")).pack()
    frame_continentes = ttk.Frame(frame_stats); frame_continentes.pack(fill="x", pady=5)
    for continente, cantidad in sorted(conteo_continentes.items()): 
        crear_linea_stat(frame_continentes, f"{continente}:", str(cantidad))
        
    ttk.Button(frame_stats, text="Cerrar", command=ventana_stats.destroy).pack(side="bottom", pady=10)

def actualizar_vista():
    """
    Función unificada que filtra y busca desde la lista maestra.
    Actualiza 'dataset_mostrado' con el resultado.
    """
    global dataset_mostrado

    # 1. Obtener valores de los controles
    filtro_continente = combo_filtrar.get()
    termino_busqueda = campo_busqueda.get().lower()

    # 2. Obtener valores numéricos
    min_pob = _obtener_valor_numerico(campo_min_poblacion, default_val=0)
    max_pob = _obtener_valor_numerico(campo_max_poblacion, default_val=999999999999999) 
    min_area = _obtener_valor_numerico(campo_min_superficie, default_val=0)
    max_area = _obtener_valor_numerico(campo_max_superficie, default_val=999999999999999)

    # --- ¡VALIDACIÓN AÑADIDA! ---
    # Si CUALQUIERA de los campos numéricos tuvo un error (y devolvió None),
    # detenemos el filtrado. El usuario ya vio el messagebox.
    if min_pob is None or max_pob is None or min_area is None or max_area is None:
        return # Detener la función aquí, no hacer nada.
    # --- FIN DE LA VALIDACIÓN ---

    # 3. Empezar SIEMPRE desde la lista maestra
    lista_temporal = dataset_paises[:]

    # 4. Aplicar filtro de continente (si no es "Todos")
    if filtro_continente != "Todos":
        lista_temporal = [
            pais for pais in lista_temporal 
            if pais['continente'] == filtro_continente
        ]

    # 5. Aplicar filtro de búsqueda (si hay término)
    if termino_busqueda:
        lista_temporal = [
            pais for pais in lista_temporal 
            if termino_busqueda in pais['nombre_comun_es'].lower()
        ]

    # 6. Aplicar filtro de POBLACIÓN
    # (Ya no se necesita 'if min_pob is not None' porque nos aseguramos de que no sea None)
    lista_temporal = [
        pais for pais in lista_temporal 
        if min_pob <= pais['poblacion_num'] <= max_pob 
    ]

    # 7. Aplicar filtro de SUPERFICIE
    lista_temporal = [
        pais for pais in lista_temporal 
        if min_area <= pais['area_num'] <= max_area
    ]

    # 8. Actualizar la lista de vista
    dataset_mostrado = lista_temporal

    # 9. Mostrar en la GUI (sin re-ordenar)
    columnas_visibles = ["nombre_comun_es", "poblacion", "area", "continente"]
    mostrar_datos_en_treeview(dataset_mostrado, columnas_visibles)

    # 10. (Opcional) Mostrar "no hay resultados"
    if not dataset_mostrado and termino_busqueda:
        messagebox.showinfo("Búsqueda", f"No se encontraron países con el término '{termino_busqueda}'.")

def resetear_vista():
    """
    Limpia TODOS los controles de filtro y resetea la vista
    para mostrar todos los países, ordenados por nombre.
    """
    global dataset_mostrado 
    
    # 1. Limpia todos los widgets de entrada
    campo_busqueda.delete(0, tk.END)
    combo_ordenar.set("Nombre")
    combo_filtrar.set("Todos") 
    campo_min_poblacion.delete(0, tk.END)
    campo_max_poblacion.delete(0, tk.END)
    campo_min_superficie.delete(0, tk.END)
    campo_max_superficie.delete(0, tk.END)
    
    # 2. Llama a la función unificada.
    # Como todos los campos están vacíos/en "Todos", mostrará la lista completa.
    actualizar_vista()
    
    # 3. Aplica el orden por defecto (Nombre) a la vista reseteada.
    columnas_visibles = ["nombre_comun_es", "poblacion", "area", "continente"]
    ordenar_columna("nombre_comun_es", dataset_mostrado, columnas_visibles)

def _obtener_valor_numerico(entrada_widget, default_val=None):
    """
    Intenta obtener un valor ENTERO POSITIVO de un Entry.
    Devuelve 'default_val' si está vacío.
    Devuelve el número si es válido.
    Devuelve 'None' si hay un error (texto o negativo).
    """
    try:
        valor_str = entrada_widget.get().strip().replace('.', '').replace(',', '')
        if not valor_str: 
            return default_val # Campo vacío, usa el default (0 o infinito)
        
        valor_int = int(valor_str)
        
        if valor_int < 0:
            messagebox.showwarning("Valor Inválido", "No se permiten números negativos en los filtros de rango.")
            return None # <--- CAMBIO CLAVE: Señala un error
            
        return valor_int # Número válido
        
    except ValueError:
        messagebox.showwarning("Entrada Inválida", "Por favor, introduce solo números ENTEROS válidos para los filtros.")
        return None # <--- CAMBIO CLAVE: Señala un error
    except AttributeError: 
        return None # <--- CAMBIO CLAVE: Señala un error

# --- FUNCIÓN PRINCIPAL DE LA INTERFAZ ---

def iniciar_interfaz():
    """
    Crea, configura y ejecuta la interfaz gráfica principal (GUI).
    """
    # Declara qué variables globales se van a asignar/modificar dentro de esta función
    global dataset_paises, dataset_mostrado, combo_ordenar, tree, ventana, campo_busqueda, combo_filtrar
    global campo_min_poblacion, campo_max_poblacion
    global campo_min_superficie, campo_max_superficie

    # 1. Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Visor de Datos de Países")
    ventana.geometry("1000x800") # Aumentado para los nuevos filtros

    # 2. Cargar los datos
    ruta_csv = os.path.join("Continentes", "Todos.csv")
    dataset_paises = cargar_datos_en_memoria(ruta_csv)
    if dataset_paises is None: 
        dataset_paises = []
    
    # 3. Inicializar la lista de vista (al inicio, es una copia de la maestra)
    dataset_mostrado = dataset_paises[:] 

    # --- 4. Configurar Paneles de Layout ---
    # Un panel a la izquierda para controles, y uno a la derecha para la tabla
    frame_izquierda = ttk.Frame(ventana, width=200)
    frame_derecha = ttk.Frame(ventana)
    
    # fill="y" hace que el panel izquierdo ocupe toda la altura
    frame_izquierda.pack(side="left", fill="y", padx=10, pady=10)
    # fill="both" y expand=True hace que el panel derecho ocupe el resto del espacio
    frame_derecha.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # --- 5. Panel Izquierdo (Controles) ---
    ttk.Label(frame_izquierda, text="Menú", font=("Helvetica", 12, "bold")).pack(pady=10)
    
    ttk.Button(frame_izquierda, text="Resetear Vista", command=resetear_vista).pack(fill="x", pady=5)
    ttk.Separator(frame_izquierda, orient='horizontal').pack(fill='x', pady=10)
    
    # --- Bloque de Filtros (Unificado) ---
    ttk.Label(frame_izquierda, text="Filtros", font=("Helvetica", 10, "bold")).pack(pady=(5,0))

    # Filtro por Nombre
    ttk.Label(frame_izquierda, text="Por Nombre:").pack(pady=(5,0))
    campo_busqueda = ttk.Entry(frame_izquierda)
    campo_busqueda.pack(fill="x", padx=5)

    # Filtro por Continente
    ttk.Label(frame_izquierda, text="Por Continentes: ").pack(pady=(5,0))
    opciones_paises = ["Todos","Africa","Americas","Asia","Europe","Oceania", "Antarctic"]
    combo_filtrar = ttk.Combobox(frame_izquierda, values= opciones_paises, state= "readonly");  
    combo_filtrar.pack(fill="x", padx=5)
    combo_filtrar.set(opciones_paises[0]) # Default: "Todos"
    
    # Filtro por Rango de Población
    ttk.Label(frame_izquierda, text="Por Rango de Población", font=("Helvetica", 10, "bold")).pack(pady=(5,0))
    ttk.Label(frame_izquierda, text="(Mínimo / Máximo):").pack(pady=(5,0))
    frame_poblacion = ttk.Frame(frame_izquierda); frame_poblacion.pack(fill="x", padx=5)
    campo_min_poblacion = ttk.Entry(frame_poblacion, width=10); campo_min_poblacion.pack(side="left", fill="x", expand=True)
    ttk.Label(frame_poblacion, text=" / ").pack(side="left")
    campo_max_poblacion = ttk.Entry(frame_poblacion, width=10); campo_max_poblacion.pack(side="left", fill="x", expand=True)
    
    # Filtro por Rango de Superficie
    ttk.Label(frame_izquierda, text="Por Rango de Superficie", font=("Helvetica", 10, "bold")).pack(pady=(5,0))
    ttk.Label(frame_izquierda, text="(Mínimo / Máximo km²):").pack(pady=(5,0))
    frame_superficie = ttk.Frame(frame_izquierda); frame_superficie.pack(fill="x", padx=5)
    campo_min_superficie = ttk.Entry(frame_superficie, width=10); campo_min_superficie.pack(side="left", fill="x", expand=True)
    ttk.Label(frame_superficie, text=" / ").pack(side="left")
    campo_max_superficie = ttk.Entry(frame_superficie, width=10); campo_max_superficie.pack(side="left", fill="x", expand=True)
    
    # Botón Único para aplicar TODOS los filtros
    ttk.Button(frame_izquierda, text="Aplicar Filtros", command=actualizar_vista).pack(pady=5)
    ttk.Separator(frame_izquierda, orient='horizontal').pack(fill='x', pady=10)

    # --- Bloque de Ordenamiento ---
    ttk.Label(frame_izquierda, text="Ordenar por:").pack(pady=(5,0))
    opciones_orden = ["Nombre", "Población", "Superficie"]
    combo_ordenar = ttk.Combobox(frame_izquierda, values=opciones_orden, state="readonly"); combo_ordenar.pack(fill="x", padx=5); combo_ordenar.set(opciones_orden[0])
    ttk.Button(frame_izquierda, text="Ordenar (Asc/Desc)", command=ordenar_desde_controles).pack(pady=5)
    ttk.Separator(frame_izquierda, orient='horizontal').pack(fill='x', pady=10)
    
    # --- Bloque de Estadísticas ---
    ttk.Button(frame_izquierda, text="Mostrar Estadísticas", command=mostrar_ventana_estadisticas).pack(fill="x", pady=5)
    
    # --- 6. Panel Derecho (Tabla de datos) ---
    ttk.Label(frame_derecha, text="Países", font=("Helvetica", 12, "bold")).pack(pady=(0, 5))
    
    # Define las columnas que se mostrarán y sus títulos
    columnas_a_mostrar = {"nombre_comun_es": "Nombre", "poblacion": "Población", "area": "Superficie", "continente": "Continente"}
    nombres_internos_columnas = list(columnas_a_mostrar.keys()) # Lista de los nombres internos
    
    # Crea el widget Treeview
    tree = ttk.Treeview(frame_derecha, columns=nombres_internos_columnas, show="headings")
    
    # Configura las cabeceras (títulos)
    for internal_name, display_name in columnas_a_mostrar.items(): 
        tree.heading(internal_name, text=display_name)
        tree.column(internal_name, width=150, anchor='center')
        
    # Añade barras de scroll
    vsb = ttk.Scrollbar(frame_derecha, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_derecha, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # Empaqueta los scrollbars y la tabla
    vsb.pack(side='right', fill='y')
    hsb.pack(side='bottom', fill='x')
    tree.pack(side='left', fill='both', expand=True)
    
    # --- 7. Carga Inicial de Datos ---
    if dataset_mostrado:
        # Muestra todos los datos al inicio
        mostrar_datos_en_treeview(dataset_mostrado, nombres_internos_columnas)
        # Ordena la vista inicial por nombre
        ordenar_columna("nombre_comun_es", dataset_mostrado, nombres_internos_columnas)

    # --- 8. Iniciar el bucle de la aplicación ---
    # Esta línea mantiene la ventana abierta y escuchando eventos (clics, etc.)
    ventana.mainloop()

# --- Punto de Entrada del Script ---
# Este bloque solo se ejecuta si corres este archivo directamente (ej. python interfaz.py)
if __name__ == "__main__":
    iniciar_interfaz()