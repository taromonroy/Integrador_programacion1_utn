![UTN](https://upload.wikimedia.org/wikipedia/commons/6/67/UTN_logo.jpg)

**Proyecto Integrador - Programación I (2025)**
-------
**Integrantes del proyecto:**
- Lautaro Monroy
- Benjamin Cajales
-------
**Descripcion:**

Trabajo integrador Programación I sobre gestión de datos de paises en Python:
- Filtros
- Ordenamientos
- Estadisticas
-------
**Instrucciones para ejecutar Docker**
- 1- construir la imagen
  
```python docker build -t mi-app-tkinter:1.0 .```
- 2- ejecutar el contenedor 

*Linux*

Necesitás conectar manualmente el contenedor al servidor gráfico (X11) de tu sistema

```python docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix mi-app-tkinter ```

Qué hacér: Añadís -v /tmp/.X11-unix... para compartir el "cable" de video

*windows*

Docker Desktop lo hace por vos automáticamente gracias a la tecnología WSLg

```python docker run -it --rm -e DISPLAY=$DISPLAY mi-app-tkinter ```

Qué hacér: Solo pasás la dirección de la pantalla (-e DISPLAY). El "cable" se conecta por arte de magia.

-------
**Actividades**
| Funcionalidades minimas del sistema             | Realizado      |
|-------------------------------------------------|----------------|
| Buscar un pais (coincidencia parcial o exacta)  | 🚧 En Progreso |
| Filtrar paises                                  | 🚧 En Progreso |
| Ordenar paises                                  | 🚧 En Progreso |
| Mostrar estadisticas                            | 🚧 En Progreso |