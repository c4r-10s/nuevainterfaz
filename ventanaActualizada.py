import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os

# ==========================================
# CLASE EVIDENCIAS (Manejo del Array Dinámico)
# ==========================================
class Evidencias:
    def __init__(self):
        self.array_dinamico = []
        self.contador_id = 1

    # Crear / Incluir un registro (Mantiene los campos ocultos listos para el profesor)
    def incluir_evidencia(self, nombre, fecha_carga, descripcion, archivo):
        nuevo_registro = {
            "IDevidencia": self.contador_id,
            "NombreEvidencia": nombre,
            "FechadeCarga": fecha_carga,
            "Descripcion": descripcion,
            "calificacion": "",        # Queda oculto y vacío para el profesor
            "estado": "No Revisado",   # Queda oculto como 'No Revisado' para el profesor
            "fecha_revision": "",      # Queda oculto y vacío para el profesor
            "archivo": archivo
        }
        self.array_dinamico.append(nuevo_registro)
        self.contador_id += 1

    # Modificar / Editar un registro (El alumno solo altera sus campos, respeta lo del profesor)
    def modificar_registro(self, id_evidencia, nombre, fecha_carga, descripcion, archivo):
        for registro in self.array_dinamico:
            if registro["IDevidencia"] == id_evidencia:
                registro["NombreEvidencia"] = nombre
                registro["FechadeCarga"] = fecha_carga
                registro["Descripcion"] = descripcion
                # NOTA: calificacion, estado y fecha_revision NO se tocan para no borrar lo del profesor
                registro["archivo"] = archivo
                break

    # Guardar un registro (Decide si incluye o modifica)
    def guardar_registro(self, modo_edicion, id_evidencia, nombre, fecha_carga, desc, archivo):
        if modo_edicion:
            self.modificar_registro(id_evidencia, nombre, fecha_carga, desc, archivo)
        else:
            self.incluir_evidencia(nombre, fecha_carga, desc, archivo)

    # Eliminar un registro
    def eliminar_registro(self, id_evidencia):
        self.array_dinamico = [reg for reg in self.array_dinamico if reg["IDevidencia"] != id_evidencia]

    # Obtener todos los registros para la rejilla
    def obtener_todos(self):
        return self.array_dinamico


# =========================
# CONFIGURACIÓN PRINCIPAL
# =========================
ventana = tk.Tk()
ventana.title("Sistema de Evidencias - Vista Estudiante")

ancho = 950
alto = 700

pantalla_ancho = ventana.winfo_screenwidth()
pantalla_alto = ventana.winfo_screenheight()

x = int((pantalla_ancho / 2) - (ancho / 2))
y = int((pantalla_alto / 2) - (alto / 2))

ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
ventana.configure(bg="white")
ventana.resizable(False, False)

# =========================
# VARIABLES GLOBALES UI
# =========================
gestor_evidencias = Evidencias()
ruta_archivo = ""
modo_edicion = False
id_seleccionado = None

# =========================
# FUNCIONES DE UI
# =========================

def mostrar_submenu(menu):
    frame_estudiantes.place_forget()
    frame_tutores.place_forget()
    frame_asesores.place_forget()

    if menu == "estudiantes":
        frame_estudiantes.place(x=40, y=85)
        lbl_ruta.config(text="Estudiantes > Gestión de Evidencias")
    elif menu == "tutores":
        frame_tutores.place(x=40, y=165)
        lbl_ruta.config(text="Tutores Académicos")
    elif menu == "asesores":
        frame_asesores.place(x=40, y=255)
        lbl_ruta.config(text="Asesores Pedagógicos > Observaciones")

def salir():
    if messagebox.askyesno("Salir", "¿Desea salir del sistema?"):
        ventana.destroy()

def refrescar_tabla():
    tabla.delete(*tabla.get_children())
    for reg in gestor_evidencias.obtener_todos():
        tabla.insert("", "end", values=(
            reg["IDevidencia"],
            reg["NombreEvidencia"],
            reg["FechadeCarga"],
            reg["Descripcion"],
            reg["calificacion"],
            reg["estado"],
            reg["fecha_revision"],
            reg["archivo"]
        ))

def nueva_evidencia():
    global ruta_archivo, modo_edicion, id_seleccionado

    modo_edicion = False  
    id_seleccionado = None

    # Habilitar campos del alumno
    entry_nombre.config(state="normal")
    txt_descripcion.config(state="normal")
    btn_cargar.config(state="normal")

    # Limpiar controles
    entry_nombre.delete(0, tk.END)
    txt_descripcion.delete("1.0", tk.END)

    # Fecha de Carga automática del día de hoy
    entry_fecha_carga.config(state="normal")
    entry_fecha_carga.delete(0, tk.END)
    entry_fecha_carga.insert(0, datetime.now().strftime("%d/%m/%Y"))
    entry_fecha_carga.config(state="readonly")

    ruta_archivo = ""
    lbl_archivo.config(text="Sin archivo")

def cargar_archivo():
    global ruta_archivo
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos permitidos", "*.pdf;*.doc;*.docx;*.xls;*.xlsx"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        ruta_archivo = archivo
        lbl_archivo.config(text=os.path.basename(archivo))

def aceptar():
    global ruta_archivo, modo_edicion, id_seleccionado

    nombre = entry_nombre.get().strip()
    fecha_carga = entry_fecha_carga.get()
    descripcion = txt_descripcion.get("1.0", tk.END).strip()

    seleccionado = tabla.selection()
    if seleccionado and not modo_edicion:
        messagebox.showwarning("Atención", "Este registro ya existe en la rejilla. Presiona 'Modificar' si deseas editarlo.")
        return

    if not nombre or not descripcion or not ruta_archivo:
        messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos requeridos (Nombre, Descripción, Archivo).")
        return

    # Enviamos los datos al gestor (los campos de profesor se administran internamente)
    gestor_evidencias.guardar_registro(
        modo_edicion, id_seleccionado, nombre, fecha_carga, descripcion, ruta_archivo
    )
    
    if modo_edicion:
        messagebox.showinfo("Correcto", "Evidencia modificada correctamente.")
    else:
        messagebox.showinfo("Correcto", "Evidencia registrada correctamente.")

    refrescar_tabla()
    nueva_evidencia()

def eliminar():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un registro de la rejilla para eliminar.")
        return

    if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este registro?"):
        datos = tabla.item(seleccionado)["values"]
        id_evid = int(datos[0])
        
        gestor_evidencias.eliminar_registro(id_evid)
        refrescar_tabla()
        messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")
        nueva_evidencia()

def modificar():
    global modo_edicion
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un registro de la rejilla para modificar.")
        return

    # Habilitamos únicamente los campos que el alumno tiene permitido alterar
    entry_nombre.config(state="normal")
    txt_descripcion.config(state="normal")
    btn_cargar.config(state="normal")
    
    modo_edicion = True
    messagebox.showinfo("Modo Edición", "Campos habilitados. Puedes modificar los datos de tu entrega.")

def cargar_datos(event):
    global ruta_archivo, modo_edicion, id_seleccionado
    seleccionado = tabla.selection()

    if seleccionado:
        modo_edicion = False 
        datos = tabla.item(seleccionado)["values"]
        id_seleccionado = int(datos[0])

        # Habilitar temporalmente para volcar los datos
        entry_nombre.config(state="normal")
        txt_descripcion.config(state="normal")
        entry_fecha_carga.config(state="normal")

        # Inserción de textos correspondientes
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, datos[1])

        entry_fecha_carga.delete(0, tk.END)
        entry_fecha_carga.insert(0, datos[2])

        txt_descripcion.delete("1.0", tk.END)
        txt_descripcion.insert("1.0", datos[3])

        ruta_archivo = datos[7]
        lbl_archivo.config(text=os.path.basename(str(datos[7])))

        # Congelar los controles en modo lectura rápida
        entry_nombre.config(state="disabled")
        txt_descripcion.config(state="disabled")
        entry_fecha_carga.config(state="readonly")
        btn_cargar.config(state="disabled")


# =========================
# DISEÑO DE LA INTERFAZ
# =========================

frame_superior = tk.Frame(ventana, width=876, height=60, bd=1, relief="solid", bg="white")
frame_superior.place(x=24, y=10)

try:
    imagen_logo = tk.PhotoImage(file=r"C:\Users\SALA-2\Downloads\Programacion\logoudi.png")
    lbl_logo = tk.Label(frame_superior, image=imagen_logo, bg="white")
    lbl_logo.image = imagen_logo
    lbl_logo.place(x=100, y=0)
except Exception:
    lbl_logo = tk.Label(frame_superior, text="LOGO", bg="#D9D9D9", font=("Arial", 12, "bold"))
    lbl_logo.place(x=200, y=10)

lbl_titulo = tk.Label(frame_superior, text="Software ING", font=("Arial", 18, "bold"), bg="white")
lbl_titulo.place(x=400, y=15)

# PANEL IZQUIERDO (MENÚ)
frame_menu = tk.Frame(ventana, width=230, height=600, bd=1, relief="solid", bg="white")
frame_menu.place(x=25, y=80)

lbl_menu = tk.Label(frame_menu, text="Menú", font=("Arial", 11, "bold"), bg="white")
lbl_menu.place(x=15, y=15)

btn_estudiantes = tk.Button(frame_menu, text="Estudiantes", bd=0, bg="white", anchor="w", command=lambda: mostrar_submenu("estudiantes"))
btn_estudiantes.place(x=20, y=60)

btn_tutores = tk.Button(frame_menu, text="Tutores Académicos", bd=0, bg="white", anchor="w", command=lambda: mostrar_submenu("tutores"))
btn_tutores.place(x=20, y=140)

btn_asesores = tk.Button(frame_menu, text="Asesores Pedagógicos", bd=0, bg="white", anchor="w", command=lambda: mostrar_submenu("asesores"))
btn_asesores.place(x=20, y=230)

frame_estudiantes = tk.Frame(frame_menu, bg="white")
tk.Label(frame_estudiantes, text="└ Gestión de Evidencias", bg="white").pack(anchor="w")

frame_tutores = tk.Frame(frame_menu, bg="white")
tk.Label(frame_tutores, text="└ Subir Preguntas", bg="white").pack(anchor="w")
tk.Label(frame_tutores, text="└ Revisar Evidencias", bg="white").pack(anchor="w")
tk.Label(frame_tutores, text="└ Informes", bg="white").pack(anchor="w")

frame_asesores = tk.Frame(frame_menu, bg="white")
tk.Label(frame_asesores, text="└ Observaciones", bg="white").pack(anchor="w")

btn_salir = tk.Button(frame_menu, text="Salir", width=15, command=salir)
btn_salir.place(x=20, y=550)

# PANEL DERECHO (PRINCIPAL)
frame_principal = tk.Frame(ventana, width=620, height=600, bd=1, relief="solid", bg="white")
frame_principal.place(x=280, y=80)

lbl_ruta = tk.Label(frame_principal, text="Inicio", font=("Arial", 11, "bold"), bg="white", fg="blue")
lbl_ruta.place(x=15, y=15)

# ===================================================
# FORMULARIO DE EVIDENCIAS (REORGANIZADO HACIA ARRIBA)
# ===================================================

tk.Label(frame_principal, text="Nombre Evidencia:", bg="white", font=("Arial", 9, "bold")).place(x=230, y=65)
entry_nombre = tk.Entry(frame_principal, width=30)
entry_nombre.place(x=360, y=65)

tk.Label(frame_principal, text="Fecha Carga:", bg="white", font=("Arial", 9, "bold")).place(x=230, y=100)
entry_fecha_carga = tk.Entry(frame_principal, width=30)
entry_fecha_carga.place(x=360, y=100)

tk.Label(frame_principal, text="Descripción:", bg="white", font=("Arial", 9, "bold")).place(x=230, y=135)
txt_descripcion = tk.Text(frame_principal, width=28, height=2)
txt_descripcion.place(x=360, y=135)

# Subimos el botón de carga de archivo y su etiqueta para cubrir el espacio vacío
btn_cargar = tk.Button(frame_principal, text="Cargar archivo", command=cargar_archivo)
btn_cargar.place(x=230, y=190)

lbl_archivo = tk.Label(frame_principal, text="Sin archivo", bg="white", fg="blue")
lbl_archivo.place(x=360, y=193)

# ===================================================
# REJILLA O GRILLA VISUAL (SUBIDA Y AMPLIADA EN ALTURA)
# ===================================================

columnas = ("id", "nombre", "fecha", "descripcion", "calif", "estado", "frevision", "archivo")
# Subimos la tabla a y=240 e incrementamos height=13 para aprovechar el espacio ganado
tabla = ttk.Treeview(frame_principal, columns=columnas, show="headings", height=13)

tabla.heading("id", text="ID")
tabla.heading("nombre", text="Nombre")
tabla.heading("fecha", text="F. Carga")
tabla.heading("descripcion", text="Descripción")
tabla.heading("calif", text="Calif.")
tabla.heading("estado", text="Estado")
tabla.heading("frevision", text="F. Rev")
tabla.heading("archivo", text="Archivo")

tabla.column("id", width=30, anchor="center")
tabla.column("nombre", width=100)
tabla.column("fecha", width=70, anchor="center")
tabla.column("descripcion", width=110)
tabla.column("calif", width=40, anchor="center")
tabla.column("estado", width=70, anchor="center")
tabla.column("frevision", width=70, anchor="center")
tabla.column("archivo", width=90)

tabla.place(x=15, y=240)
tabla.bind("<<TreeviewSelect>>", cargar_datos)

# =========================
# BOTONES DE ACCIÓN (RUD)
# =========================

btn_cancelar = tk.Button(frame_principal, text="Cancelar", width=10, command=nueva_evidencia)
btn_cancelar.place(x=15, y=550)

btn_nuevo = tk.Button(frame_principal, text="Nueva Evidencia", width=15, command=nueva_evidencia)
btn_nuevo.place(x=105, y=550)

btn_modificar = tk.Button(frame_principal, text="Modificar", width=10, command=modificar)
btn_modificar.place(x=245, y=550)

btn_eliminar = tk.Button(frame_principal, text="Eliminar", width=10, command=eliminar)
btn_eliminar.place(x=335, y=550)

btn_aceptar = tk.Button(frame_principal, text="Aceptar", width=12, bg="#ffffff", command=aceptar)
btn_aceptar.place(x=450, y=550)

# =========================
# INICIALIZACIÓN DE LA UI
# =========================
nueva_evidencia() 

ventana.mainloop()
