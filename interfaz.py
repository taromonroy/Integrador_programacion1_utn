import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# --- Variables Globales ---
# Las listas y los widgets de control deben ser globales para que las funciones los usen.
dataset_paises = []     # La lista maestra de todos los países
dataset_mostrado = []   # La lista que se está mostrando actualmente (resultado de los filtros)
tree = None
campo_busqueda = None
combo_filtrar = None
campo_min_poblacion = None
campo_max_poblacion = None
campo_min_superficie = None
campo_max_superficie = None
ventana = None 

# --- Funciones de Datos y Lógica (ESENCIALES para tu parte) ---

def cargar_datos_en_memoria(archivo_csv):
    """Carga y pre-procesa los datos, convirtiendo población y área a números."""
    dataset = []
    try:
        if not os.path.exists(archivo_csv): raise FileNotFoundError
        with open(archivo_csv, mode='r', encoding='utf-8') as archivo:
            lector_csv = csv.DictReader(archivo)
            for fila in lector_csv: dataset.append(fila)
        
        for pais in dataset:
            try: 
                pais['poblacion_num'] = int(pais.get('poblacion', 0))
            except: 
                pais['poblacion_num'] = 0 
            try: 
                pais['area_num'] = int(pais.get('area', 0))
            except: 
                pais['area_num'] = 0 
        return dataset
    except FileNotFoundError: 
        messagebox.showerror("Error", f"No se encontró el archivo de datos:\n{archivo_csv}")
        return None
    except Exception as e: 
        messagebox.showerror("Error", f"Ocurrió un error al leer el archivo: {e}")
        return None

def mostrar_datos_en_treeview(dataset, columnas):
    """Actualiza el Treeview con los datos filtrados."""
    global tree
    tree.delete(*tree.get_children())
    if not dataset: return
    for fila_dict in dataset:
        valores = [fila_dict.get(col, '') for col in columnas]
        tree.insert("", "end", values=valores)

def _obtener_valor_numerico(entrada_widget, default_val=None):
    """Intenta obtener un valor ENTERO de un Entry, manejando errores y cadenas vacías."""
    try:
        valor_str = entrada_widget.get().strip().replace('.', '').replace(',', '')
        if not valor_str: 
            return default_val
        return int(float(valor_str))
    except ValueError:
        # Solo muestra advertencia si el campo NO está vacío y tiene un valor inválido
        if entrada_widget.get().strip():
             messagebox.showwarning("Entrada Inválida", "Por favor, introduce solo números ENTEROS válidos para los filtros de Población/Superficie.")
        return default_val
    except AttributeError: 
        return default_val

# --- FUNCIÓN CENTRAL DE FILTRADO Y BÚSQUEDA ---
def actualizar_vista():
    """
    Aplica los filtros de búsqueda por nombre, continente y rangos numéricos.
    Este es el núcleo de tu entrega.
    """
    global dataset_mostrado, dataset_paises
    global combo_filtrar, campo_busqueda, campo_min_poblacion, campo_max_poblacion
    global campo_min_superficie, campo_max_superficie

    # 1. Obtener valores de los controles
    filtro_continente = combo_filtrar.get() if combo_filtrar else "Todos"
    termino_busqueda = campo_busqueda.get().lower() if campo_busqueda else ""

    # Usamos un valor máximo muy grande si el campo está vacío, para simular infinito.
    min_pob = _obtener_valor_numerico(campo_min_poblacion, default_val=0)
    max_pob = _obtener_valor_numerico(campo_max_poblacion, default_val=999999999999999) 
    min_area = _obtener_valor_numerico(campo_min_superficie, default_val=0)
    max_area = _obtener_valor_numerico(campo_max_superficie, default_val=999999999999999)

    # 2. Empezar SIEMPRE desde la lista maestra
    lista_temporal = dataset_paises[:]

    # 3. Aplicar filtro de continente
    if filtro_continente != "Todos":
        lista_temporal = [
            pais for pais in lista_temporal 
            if pais.get('continente') == filtro_continente
        ]

    # 4. Aplicar filtro de búsqueda por nombre
    if termino_busqueda:
        lista_temporal = [
            pais for pais in lista_temporal 
            if termino_busqueda in pais.get('nombre_comun_es', '').lower()
        ]

    # 5. Aplicar filtro de POBLACIÓN por rango
    if min_pob is not None and max_pob is not None:
        lista_temporal = [
            pais for pais in lista_temporal 
            if min_pob <= pais['poblacion_num'] <= max_pob
        ]

    # 6. Aplicar filtro de SUPERFICIE por rango
    if min_area is not None and max_area is not None:
        lista_temporal = [
            pais for pais in lista_temporal 
            if min_area <= pais['area_num'] <= max_area
        ]

    # 7. Actualizar la lista de vista
    dataset_mostrado = lista_temporal

    # 8. Mostrar en la GUI
    columnas_visibles = ["nombre_comun_es", "poblacion", "area", "continente"]
    mostrar_datos_en_treeview(dataset_mostrado, columnas_visibles)

# Funciones wrapper para los botones
def realizar_busqueda():
    """Llamada directa desde el botón de búsqueda."""
    actualizar_vista()
    
def resetear_vista_busqueda():
    """Resetea solo los campos de búsqueda y filtro."""
    global campo_busqueda, combo_filtrar
    global campo_min_poblacion, campo_max_poblacion, campo_min_superficie, campo_max_superficie
    
    campo_busqueda.delete(0, tk.END)
    combo_filtrar.set("Todos")
    campo_min_poblacion.delete(0, tk.END)
    campo_max_poblacion.delete(0, tk.END)
    campo_min_superficie.delete(0, tk.END)
    campo_max_superficie.delete(0, tk.END)
    
    actualizar_vista()

# --- FUNCIÓN PRINCIPAL DE LA INTERFAZ ---
def iniciar_interfaz():
    """Crea y ejecuta la interfaz gráfica con solo la funcionalidad de Búsqueda/Filtro."""
    global dataset_paises, dataset_mostrado, tree, ventana
    global campo_busqueda, combo_filtrar, campo_min_poblacion, campo_max_poblacion
    global campo_min_superficie, campo_max_superficie

    ventana = tk.Tk()
    ventana.title("Módulo de Búsqueda y Filtros de Países")
    ventana.geometry("800x600")

    # 1. Carga de datos
    
    ruta_csv = os.path.join("Continentes", "Todos.csv")
    dataset_paises = cargar_datos_en_memoria(ruta_csv)
    if dataset_paises is None: dataset_paises = []
    dataset_mostrado = dataset_paises[:] 

    # --- Paneles ---
    frame_controles = ttk.Frame(ventana, width=200)
    frame_tabla = ttk.Frame(ventana)
    frame_controles.pack(side="left", fill="y", padx=10, pady=10)
    frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # --- Controles de Búsqueda y Filtros (Tu parte) ---
    ttk.Label(frame_controles, text="Filtros de Búsqueda", font=("Helvetica", 12, "bold")).pack(pady=10)
    
    # 1. Búsqueda por Nombre
    ttk.Label(frame_controles, text="Buscar por Nombre:").pack(pady=(5,0))
    campo_busqueda = ttk.Entry(frame_controles)
    campo_busqueda.pack(fill="x", padx=5)
    ttk.Button(frame_controles, text="Buscar", command=realizar_busqueda).pack(pady=5)
    ttk.Separator(frame_controles, orient='horizontal').pack(fill='x', pady=10)

    # 2. Filtro por Continente
    ttk.Label(frame_controles, text="Filtro por Continentes: ").pack(pady=(5,0))
    opciones_paises = ["Todos","Africa","Americas","Asia","Europe","Oceania", "Antarctic"]
    combo_filtrar = ttk.Combobox(frame_controles, values= opciones_paises, state= "readonly")
    combo_filtrar.pack(fill="x", padx=5)
    combo_filtrar.set(opciones_paises[0]) 

    # 3. Filtro por Rango de Población
    ttk.Label(frame_controles, text="Por Rango de Pobalción").pack(pady=(10,0))
    frame_poblacion = ttk.Frame(frame_controles); frame_poblacion.pack(fill="x", padx=5)
    campo_min_poblacion = ttk.Entry(frame_poblacion, width=10); campo_min_poblacion.pack(side="left", fill="x", expand=True)
    ttk.Label(frame_poblacion, text=" / ").pack(side="left")
    campo_max_poblacion = ttk.Entry(frame_poblacion, width=10); campo_max_poblacion.pack(side="left", fill="x", expand=True)
    
    # 4. Filtro por Rango de Superficie
    ttk.Label(frame_controles, text="Por Rango de Superficie").pack(pady=(10,0))
    frame_superficie = ttk.Frame(frame_controles); frame_superficie.pack(fill="x", padx=5)
    campo_min_superficie = ttk.Entry(frame_superficie, width=10); campo_min_superficie.pack(side="left", fill="x", expand=True)
    ttk.Label(frame_superficie, text=" / ").pack(side="left")
    campo_max_superficie = ttk.Entry(frame_superficie, width=10); campo_max_superficie.pack(side="left", fill="x", expand=True)
    
    # Boton de Aplicar Filtros Unificado
    ttk.Button(frame_controles, text="Aplicar Filtros", command=actualizar_vista).pack(pady=10, fill="x")
    ttk.Button(frame_controles, text="Resetear Filtros", command=resetear_vista_busqueda).pack(pady=5, fill="x")
    
    ttk.Separator(frame_controles, orient='horizontal').pack(fill='x', pady=10)

    # --- Panel Derecho (Tabla de datos) ---
    ttk.Label(frame_tabla, text="Resultados de Búsqueda", font=("Helvetica", 12, "bold")).pack(pady=(0, 5))
    columnas_a_mostrar = {"nombre_comun_es": "Nombre", "poblacion": "Población", "area": "Superficie", "continente": "Continente"}
    nombres_internos_columnas = list(columnas_a_mostrar.keys())
    
    tree = ttk.Treeview(frame_tabla, columns=nombres_internos_columnas, show="headings")
    for internal_name, display_name in columnas_a_mostrar.items(): 
        tree.heading(internal_name, text=display_name)
        tree.column(internal_name, width=150, anchor='center')
        
    vsb = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    vsb.pack(side='right', fill='y')
    hsb.pack(side='bottom', fill='x')
    tree.pack(side='left', fill='both', expand=True)
    
    # Muestra los datos iniciales
    if dataset_mostrado:
        mostrar_datos_en_treeview(dataset_mostrado, nombres_internos_columnas)

    ventana.mainloop()

if __name__ == "__main__":
    # Esto permite ejecutar solo tu archivo para probar la funcionalidad
    iniciar_interfaz()