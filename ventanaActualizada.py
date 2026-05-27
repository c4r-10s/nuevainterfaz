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

    def existe_id(self, id_evidencia):
        return any(reg["IDevidencia"] == id_evidencia for reg in self.array_dinamico)

    def incluir_evidencia(self, id_evidencia, id_estudiante, nombre_estudiante, nombre_evidencia, fecha_carga, descripcion, archivo):
        nuevo_registro = {
            "IDevidencia": id_evidencia,
            "IDestudiante": id_estudiante,
            "NombreEstudiante": nombre_estudiante,
            "NombreEvidencia": nombre_evidencia,
            "FechadeCarga": fecha_carga,
            "Descripcion": descripcion,
            "calificacion": 0.0,
            "estado": "No Revisado",
            "fecha_revision": "",
            "archivo": archivo,
            "obs_asesor": ""
        }
        self.array_dinamico.append(nuevo_registro)

    def modificar_registro(self, id_evidencia, id_estudiante, nombre_estudiante, nombre_evidencia, fecha_carga, descripcion, archivo):
        for registro in self.array_dinamico:
            if registro["IDevidencia"] == id_evidencia:
                registro["IDestudiante"] = id_estudiante
                registro["NombreEstudiante"] = nombre_estudiante
                registro["NombreEvidencia"] = nombre_evidencia
                registro["FechadeCarga"] = fecha_carga
                registro["Descripcion"] = descripcion
                registro["archivo"] = archivo
                break

    def guardar_registro(self, modo_edicion, id_evidencia, id_estudiante, nombre_estudiante, nombre_evidencia, fecha_carga, desc, archivo):
        if modo_edicion:
            self.modificar_registro(id_evidencia, id_estudiante, nombre_estudiante, nombre_evidencia, fecha_carga, desc, archivo)
        else:
            self.incluir_evidencia(id_evidencia, id_estudiante, nombre_estudiante, nombre_evidencia, fecha_carga, desc, archivo)

    def eliminar_registro(self, id_evidencia):
        self.array_dinamico = [reg for reg in self.array_dinamico if reg["IDevidencia"] != id_evidencia]

    def obtener_todos(self):
        return self.array_dinamico


# ==========================================
# CONFIGURACIÓN PRINCIPAL (TAMAÑO 1080x720)
# ==========================================
ventana = tk.Tk()
ventana.title("Sistema de Evidencias - Entorno Académico")

ancho = 1080
alto = 720

pantalla_ancho = ventana.winfo_screenwidth()
pantalla_alto = ventana.winfo_screenheight()

x = int((pantalla_ancho / 2) - (ancho / 2))
y = int((pantalla_alto / 2) - (alto / 2))

ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
ventana.configure(bg="white")
ventana.resizable(False, False)

# Variables Globales
gestor_evidencias = Evidencias()
ruta_archivo = ""
modo_edicion = False
id_seleccionado = None

# ==========================================
# FUNCIONES DE UI - NAVEGACIÓN ENTRE VISTAS
# ==========================================
def mostrar_submenu(menu):
    frame_estudiantes.place_forget()
    frame_tutores.place_forget()
    frame_asesores.place_forget()

    if menu == "estudiantes":
        frame_estudiantes.place(x=40, y=85)
        lbl_ruta.config(text="Estudiantes > Gestión de Evidencias")
        volver_al_menu_principal()  
    elif menu == "tutores":
        frame_tutores.place(x=40, y=165)
        lbl_ruta.config(text="Tutores Académicos")
    elif menu == "asesores":
        frame_asesores.place(x=40, y=255)
        lbl_ruta.config(text="Asesores Pedagógicos")

def ir_a_revision_evidencias():
    frame_principal.place_forget()
    frame_revision.place(x=275, y=80)
    refrescar_tabla_revision()

def volver_al_menu_principal():
    frame_revision.place_forget()
    frame_principal.place(x=275, y=80)
    refrescar_tabla()

def salir():
    if messagebox.askyesno("Salir", "¿Desea salir del sistema?"):
        ventana.destroy()

# ==========================================
# GESTIÓN TABLA ESTUDIANTE
# ==========================================
def refrescar_tabla():
    tabla.delete(*tabla.get_children())
    for reg in gestor_evidencias.obtener_todos():
        tabla.insert("", "end", values=(
            reg["IDevidencia"], reg["NombreEvidencia"], reg["FechadeCarga"],
            reg["Descripcion"], reg["calificacion"], reg["estado"],
            reg["fecha_revision"], reg["archivo"], reg["IDestudiante"], reg["NombreEstudiante"]
        ))

def nueva_evidencia():
    global ruta_archivo, modo_edicion, id_seleccionado
    modo_edicion = False  
    id_seleccionado = None

    entry_id_estudiante.config(state="normal")
    entry_nombre_estudiante.config(state="normal")
    entry_id.config(state="normal")
    entry_nombre.config(state="normal")
    txt_descripcion.config(state="normal")
    btn_cargar.config(state="normal")

    entry_id_estudiante.delete(0, tk.END)
    entry_nombre_estudiante.delete(0, tk.END)
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    txt_descripcion.delete("1.0", tk.END)

    entry_fecha_carga.config(state="normal")
    entry_fecha_carga.delete(0, tk.END)
    entry_fecha_carga.insert(0, datetime.now().strftime("%d/%m/%Y"))
    entry_fecha_carga.config(state="readonly")

    ruta_archivo = ""
    lbl_archivo.config(text="Sin archivo")

    if tabla.selection():
        tabla.selection_remove(tabla.selection())

def cargar_archivo():
    global ruta_archivo
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos permitidos", "*.pdf;*.doc;*.docx;*.xls;*.xlsx;*.pptx"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        ruta_archivo = archivo
        lbl_archivo.config(text=os.path.basename(archivo))

def aceptar():
    global ruta_archivo, modo_edicion, id_seleccionado

    id_est_texto = entry_id_estudiante.get().strip()
    nom_est = entry_nombre_estudiante.get().strip()
    id_texto = entry_id.get().strip()
    nombre_evid = entry_nombre.get().strip()
    fecha_carga = entry_fecha_carga.get()
    descripcion = txt_descripcion.get("1.0", tk.END).strip()

    if not id_est_texto or not nom_est or not id_texto or not nombre_evid or not descripcion or not ruta_archivo:
        messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos requeridos.")
        return

    try:
        id_est_num = int(id_est_texto)
        if id_est_num <= 0: raise ValueError
    except ValueError:
        messagebox.showwarning("ID Estudiante Inválido", "El ID del Estudiante debe ser un número entero positivo.")
        return

    try:
        id_ingresado = int(id_texto)
        if id_ingresado <= 0: raise ValueError
    except ValueError:
        messagebox.showwarning("ID Evidencia Inválido", "El ID de la Evidencia debe ser un número entero positivo.")
        return

    if not modo_edicion:
        if gestor_evidencias.existe_id(id_ingresado):
            messagebox.showwarning("ID Duplicado", f"El ID de evidencia {id_ingresado} ya existe.")
            return
    else:
        id_ingresado = id_seleccionado

    gestor_evidencias.guardar_registro(modo_edicion, id_ingresado, id_est_num, nom_est, nombre_evid, fecha_carga, descripcion, ruta_archivo)
    messagebox.showinfo("Correcto", "Evidencia guardada exitosamente.")
    refrescar_tabla()
    nueva_evidencia()

def eliminar():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un registro para eliminar.")
        return
    if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este registro?"):
        datos = tabla.item(seleccionado)["values"]
        gestor_evidencias.eliminar_registro(int(datos[0]))
        refrescar_tabla()
        nueva_evidencia()

def modificar():
    global modo_edicion
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un registro para modificar.")
        return
    entry_id_estudiante.config(state="normal")
    entry_nombre_estudiante.config(state="normal")
    entry_id.config(state="disabled")
    entry_nombre.config(state="normal")
    txt_descripcion.config(state="normal")
    btn_cargar.config(state="normal")
    modo_edicion = True

def cargar_datos(event):
    global ruta_archivo, modo_edicion, id_seleccionado
    seleccionado = tabla.selection()
    if seleccionado:
        modo_edicion = False 
        datos = tabla.item(seleccionado)["values"]
        id_seleccionado = int(datos[0])

        entry_id.config(state="normal")
        entry_nombre.config(state="normal")
        txt_descripcion.config(state="normal")
        entry_fecha_carga.config(state="normal")
        entry_id_estudiante.config(state="normal")
        entry_nombre_estudiante.config(state="normal")

        entry_id.delete(0, tk.END)
        entry_id.insert(0, datos[0])
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, datos[1])
        entry_fecha_carga.delete(0, tk.END)
        entry_fecha_carga.insert(0, datos[2])
        txt_descripcion.delete("1.0", tk.END)
        txt_descripcion.insert("1.0", datos[3])
        entry_id_estudiante.delete(0, tk.END)
        entry_id_estudiante.insert(0, datos[8])
        entry_nombre_estudiante.delete(0, tk.END)
        entry_nombre_estudiante.insert(0, datos[9])

        ruta_archivo = datos[7]
        lbl_archivo.config(text=os.path.basename(str(datos[7])))

        entry_id.config(state="disabled")
        entry_nombre.config(state="disabled")
        txt_descripcion.config(state="disabled")
        entry_fecha_carga.config(state="readonly")
        entry_id_estudiante.config(state="disabled")
        entry_nombre_estudiante.config(state="disabled")
        btn_cargar.config(state="disabled")


# ==========================================
# SECCIÓN: VISTA TUTOR (REVISAR EVIDENCIAS)
# ==========================================
def refrescar_tabla_revision():
    tabla_revision.delete(*tabla_revision.get_children())
    for reg in gestor_evidencias.obtener_todos():
        tabla_revision.insert("", "end", values=(
            reg.get("IDestudiante", "N/A"),
            reg["IDevidencia"],
            reg["archivo"],
            reg.get("obs_asesor", "Sin observaciones"),
            reg["calificacion"],
            reg["estado"],
            reg["fecha_revision"]
        ))

def abrir_ventana_evaluacion(event):
    seleccion = tabla_revision.selection()
    if not seleccion:
        return
    
    valores = tabla_revision.item(seleccion)["values"]
    id_est = valores[0]
    id_evid = valores[1]
    path_arch = valores[2]
    obs_asesor = valores[3]
    nota_actual = valores[4]
    estado_actual = valores[5]

    nombre_est_actual = f"Estudiante {id_est}"
    for reg in gestor_evidencias.obtener_todos():
        if reg["IDevidencia"] == id_evid:
            nombre_est_actual = reg.get("NombreEstudiante", f"Estudiante {id_est}")
            break

    pop = tk.Toplevel(ventana)
    pop.title("Evaluación de Evidencia")
    pop.geometry("450x450")
    pop.configure(bg="white")
    pop.resizable(False, False)
    pop.grab_set() 

    # --- CAMPO BLOQUEADO (Nombre del Estudiante) ---
    tk.Label(pop, text="Nombre Estudiante:", font=("Arial", 9, "bold"), bg="white").place(x=30, y=30)
    entry_pop_nombre = tk.Entry(pop, width=30)
    entry_pop_nombre.insert(0, nombre_est_actual)
    entry_pop_nombre.config(state="disabled") # Se cambia a deshabilitado
    entry_pop_nombre.place(x=180, y=30)

    # --- CAMPO BLOQUEADO (ID del Estudiante) ---
    tk.Label(pop, text="ID Estudiante:", font=("Arial", 9, "bold"), bg="white").place(x=30, y=70)
    entry_pop_id = tk.Entry(pop, width=30)
    entry_pop_id.insert(0, id_est)
    entry_pop_id.config(state="disabled") # Se cambia a deshabilitado
    entry_pop_id.place(x=180, y=70)

    # --- CAMPO BLOQUEADO (Ruta del Archivo) ---
    tk.Label(pop, text="Path del Archivo:", font=("Arial", 9, "bold"), bg="white").place(x=30, y=110)
    entry_pop_path = tk.Entry(pop, width=30)
    entry_pop_path.insert(0, path_arch)
    entry_pop_path.config(state="disabled") 
    entry_pop_path.place(x=180, y=110)

    def abrir_archivo_sistema():
        if os.path.exists(path_arch):
            try:
                os.startfile(path_arch)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")
        else:
            messagebox.showwarning("Archivo no encontrado", f"El archivo local no existe o la ruta es ficticia:\n{path_arch}")

    btn_pop_ver = tk.Button(pop, text="VER", font=("Arial", 8, "bold"), command=abrir_archivo_sistema)
    btn_pop_ver.place(x=380, y=107)

    # --- CAMPO HABILITADO (Observaciones) ---
    tk.Label(pop, text="Observaciones:", font=("Arial", 9, "bold"), bg="white").place(x=30, y=150)
    entry_pop_obs = tk.Entry(pop, width=35)
    entry_pop_obs.insert(0, obs_asesor)
    entry_pop_obs.place(x=180, y=150)

    # --- CAMPO HABILITADO (Nota) ---
    tk.Label(pop, text="Nota (0.0 a 5.0):", font=("Arial", 9, "bold"), bg="white").place(x=30, y=190)
    entry_pop_nota = tk.Entry(pop, width=10)
    entry_pop_nota.insert(0, nota_actual)
    entry_pop_nota.place(x=180, y=190)

    # --- CAMPO HABILITADO (Estado) ---
    tk.Label(pop, text="Estado:", font=("Arial", 9, "bold"), bg="white").place(x=30, y=230)
    combo_pop_estado = ttk.Combobox(pop, values=["Revisado"], state="readonly", width=15)
    combo_pop_estado.set("Revisado" if estado_actual == "Revisado" else "")
    combo_pop_estado.place(x=180, y=230)

    def guardar_evaluacion():
        nuevas_obs = entry_pop_obs.get().strip()
        estado_seleccionado = combo_pop_estado.get()

        if estado_seleccionado != "Revisado":
            messagebox.showwarning("Estado obligatorio", "Debe establecer el estado como 'Revisado' obligatoriamente.")
            return

        try:
            nota_num = float(entry_pop_nota.get())
            if not (0.0 <= nota_num <= 5.0):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error de entrada", "La nota debe ser un número decimal entre 0.0 y 5.0 (Ej: 4.5).")
            return

        for reg in gestor_evidencias.obtener_todos():
            if reg["IDevidencia"] == id_evid:
                reg["obs_asesor"] = nuevas_obs
                reg["calificacion"] = nota_num
                reg["estado"] = estado_seleccionado
                reg["fecha_revision"] = datetime.now().strftime("%d/%m/%Y")
                break
        
        messagebox.showinfo("Éxito", "Evaluación actualizada correctamente.")
        refrescar_tabla_revision()
        pop.destroy()

    btn_pop_cancelar = tk.Button(pop, text="Cancelar", width=12, command=pop.destroy)
    btn_pop_cancelar.place(x=40, y=360)

    btn_pop_aceptar = tk.Button(pop, text="Aceptar", width=12, bg="#d9f2d9", command=guardar_evaluacion)
    btn_pop_aceptar.place(x=300, y=360)


def mostrar_histograma_informe():
    datos = gestor_evidencias.obtener_todos()
    if not datos:
        messagebox.showwarning("Sin datos", "No existen evidencias para graficar un informe.")
        return

    v_grafico = tk.Toplevel(ventana)
    v_grafico.title("Informe: Histograma Histórico de Notas")
    v_grafico.geometry("600x450")
    v_grafico.configure(bg="white")

    tk.Label(v_grafico, text="Histograma de Rendimiento Académico", font=("Arial", 12, "bold"), bg="white").pack(pady=10)

    canvas = tk.Canvas(v_grafico, width=520, height=340, bg="#f9f9f9", bd=1, relief="solid")
    canvas.pack(pady=5)

    canvas.create_line(50, 20, 50, 300, width=2)   
    canvas.create_line(50, 300, 500, 300, width=2) 

    for i in range(6):
        y_pos = 300 - (i * 50)
        canvas.create_line(45, y_pos, 50, y_pos)
        canvas.create_text(30, y_pos, text=str(float(i)), font=("Arial", 8))
    canvas.create_text(20, 15, text="Nota (Y)", font=("Arial", 8, "bold"), anchor="w")

    ancho_barra = 40
    espacio = 30
    x_inicial = 70

    for index, reg in enumerate(datos):
        nota = reg.get("calificacion", 0.0)
        id_est = reg.get("IDestudiante", "N/A")

        altura_barra = int(nota * 50)
        y_top = 300 - altura_barra

        x1 = x_inicial + (index * (ancho_barra + espacio))
        y1 = y_top
        x2 = x1 + ancho_barra
        y2 = 300

        canvas.create_rectangle(x1, y1, x2, y2, fill="#4a90e2", outline="#2a60a0")
        canvas.create_text(x1 + 20, y1 - 10, text=str(nota), font=("Arial", 8, "bold"))
        canvas.create_text(x1 + 20, 315, text=f"ID:{id_est}", font=("Arial", 8), angle=45)

    canvas.create_text(480, 325, text="Estudiante (X)", font=("Arial", 8, "bold"), anchor="e")


# ==========================================
# CONSTRUCCIÓN INTERFAZ GRÁFICA GENERAL
# ==========================================

frame_superior = tk.Frame(ventana, width=1032, height=60, bd=1, relief="solid", bg="white")
frame_superior.place(x=24, y=10)

try:
    imagen_logo = tk.PhotoImage(file=r"C:\Users\SALA-2\Downloads\Programacion\logoudi.png")
    lbl_logo = tk.Label(frame_superior, image=imagen_logo, bg="white")
    lbl_logo.image = imagen_logo
    lbl_logo.place(x=100, y=0)
except Exception:
    lbl_logo = tk.Label(frame_superior, text="LOGO", bg="#D9D9D9", font=("Arial", 12, "bold"))
    lbl_logo.place(x=150, y=10)

lbl_titulo = tk.Label(frame_superior, text="Software ING", font=("Arial", 18, "bold"), bg="white")
lbl_titulo.place(x=460, y=15)

frame_menu = tk.Frame(ventana, width=230, height=620, bd=1, relief="solid", bg="white")
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
btn_sub_revisar = tk.Button(frame_tutores, text="└ Revisar Evidencias", bg="white", bd=0, activebackground="white", command=ir_a_revision_evidencias)
btn_sub_revisar.pack(anchor="w")

frame_asesores = tk.Frame(frame_menu, bg="white")
tk.Label(frame_asesores, text="└ Observaciones", bg="white").pack(anchor="w")

btn_salir = tk.Button(frame_menu, text="Salir", width=15, command=salir)
btn_salir.place(x=20, y=570)


# ==========================================
# ENTIDADES ASOCIADAS AL PANEL DERECHO 1: ESTUDIANTES
# ==========================================
frame_principal = tk.Frame(ventana, width=780, height=620, bd=1, relief="solid", bg="white")
frame_principal.place(x=275, y=80)

lbl_ruta = tk.Label(frame_principal, text="Inicio", font=("Arial", 11, "bold"), bg="white", fg="blue")
lbl_ruta.place(x=15, y=15)

tk.Label(frame_principal, text="ID Estudiante:", bg="white", font=("Arial", 9, "bold")).place(x=20, y=40)
entry_id_estudiante = tk.Entry(frame_principal, width=25)
entry_id_estudiante.place(x=140, y=40)

tk.Label(frame_principal, text="Nombre Estudiante:", bg="white", font=("Arial", 9, "bold")).place(x=20, y=75)
entry_nombre_estudiante = tk.Entry(frame_principal, width=25)
entry_nombre_estudiante.place(x=140, y=75)

tk.Label(frame_principal, text="ID Evidencia:", bg="white", font=("Arial", 9, "bold")).place(x=360, y=40)
entry_id = tk.Entry(frame_principal, width=25)
entry_id.place(x=500, y=40)

tk.Label(frame_principal, text="Nombre Evidencia:", bg="white", font=("Arial", 9, "bold")).place(x=360, y=75)
entry_nombre = tk.Entry(frame_principal, width=25)
entry_nombre.place(x=500, y=75)

tk.Label(frame_principal, text="Fecha Carga:", bg="white", font=("Arial", 9, "bold")).place(x=360, y=110)
entry_fecha_carga = tk.Entry(frame_principal, width=25)
entry_fecha_carga.place(x=500, y=110)

tk.Label(frame_principal, text="Descripción:", bg="white", font=("Arial", 9, "bold")).place(x=360, y=145)
txt_descripcion = tk.Text(frame_principal, width=23, height=2)
txt_descripcion.place(x=500, y=145)

btn_cargar = tk.Button(frame_principal, text="Cargar archivo", command=cargar_archivo)
btn_cargar.place(x=360, y=195)

lbl_archivo = tk.Label(frame_principal, text="Sin archivo", bg="white", fg="blue")
lbl_archivo.place(x=500, y=198)

# Rejilla Estudiantes
columnas = ("id", "nombre", "fecha", "descripcion", "calif", "estado", "frevision", "archivo", "id_est", "nom_est")
tabla = ttk.Treeview(frame_principal, columns=columnas, show="headings", height=14)

tabla.heading("id", text="ID Evid.")
tabla.heading("nombre", text="Nombre Evid.")
tabla.heading("fecha", text="F. Carga")
tabla.heading("descripcion", text="Descripción")
tabla.heading("calif", text="Calif.")
tabla.heading("estado", text="Estado")
tabla.heading("frevision", text="F. Rev")
tabla.heading("archivo", text="Archivo")

tabla.column("id", width=60, anchor="center")
tabla.column("nombre", width=110)
tabla.column("fecha", width=80, anchor="center")
tabla.column("descripcion", width=130)
tabla.column("calif", width=45, anchor="center")
tabla.column("estado", width=85, anchor="center")
tabla.column("frevision", width=80, anchor="center")
tabla.column("archivo", width=140)

tabla.place(x=15, y=240)
tabla.bind("<<TreeviewSelect>>", cargar_datos)

btn_cancelar = tk.Button(frame_principal, text="Cancelar", width=12, command=nueva_evidencia)
btn_cancelar.place(x=15, y=570)

btn_nuevo = tk.Button(frame_principal, text="Nueva Evidencia", width=15, command=nueva_evidencia)
btn_nuevo.place(x=125, y=570)

btn_modificar = tk.Button(frame_principal, text="Modificar", width=12, command=modificar)
btn_modificar.place(x=350, y=570)

btn_eliminar = tk.Button(frame_principal, text="Eliminar", width=12, command=eliminar)
btn_eliminar.place(x=460, y=570)

btn_aceptar = tk.Button(frame_principal, text="Aceptar", width=15, bg="#ffffff", command=aceptar)
btn_aceptar.place(x=640, y=570)


# ==========================================
# ENTIDADES ASOCIADAS AL PANEL DERECHO 2: REVISIÓN DE EVIDENCIAS
# ==========================================
frame_revision = tk.Frame(ventana, width=780, height=620, bd=1, relief="solid", bg="white")

lbl_sub1 = tk.Label(frame_revision, text="Tutor Académico", font=("Arial", 14, "bold"), bg="white", fg="#333333")
lbl_sub1.place(x=15, y=15)

lbl_sub2 = tk.Label(frame_revision, text="Revisión de Evidencias", font=("Arial", 11, "italic"), bg="white", fg="#666666")
lbl_sub2.place(x=15, y=45)

columnas_rev = ("id_est", "id_evid", "path_arch", "obs_ase", "nota", "estado", "f_rev")
tabla_revision = ttk.Treeview(frame_revision, columns=columnas_rev, show="headings", height=18)

tabla_revision.heading("id_est", text="ID Estudiante")
tabla_revision.heading("id_evid", text="ID Evidencia")
tabla_revision.heading("path_arch", text="Path Archivo")
tabla_revision.heading("obs_ase", text="Obs. Asesor")
tabla_revision.heading("nota", text="Nota (0-5)")
tabla_revision.heading("estado", text="Estado")
tabla_revision.heading("f_rev", text="F. Revisión")

tabla_revision.column("id_est", width=95, anchor="center")
tabla_revision.column("id_evid", width=85, anchor="center")
tabla_revision.column("path_arch", width=160, anchor="w")
tabla_revision.column("obs_ase", width=140, anchor="w")
tabla_revision.column("nota", width=65, anchor="center")
tabla_revision.column("estado", width=100, anchor="center")
tabla_revision.column("f_rev", width=100, anchor="center")

tabla_revision.place(x=15, y=90)
tabla_revision.bind("<Double-1>", abrir_ventana_evaluacion)
tabla_revision.bind("<<TreeviewSelect>>", abrir_ventana_evaluacion)

btn_informe = tk.Button(frame_revision, text="Informe", width=15, font=("Arial", 10, "bold"), command=mostrar_histograma_informe)
btn_informe.place(x=15, y=550)

btn_salir_revision = tk.Button(frame_revision, text="Salir", width=15, font=("Arial", 10, "bold"), command=volver_al_menu_principal)
btn_salir_revision.place(x=630, y=550)


# ==========================================
# INICIALIZACIÓN POR DEFECTO
# ==========================================
nueva_evidencia() 
refrescar_tabla()

ventana.mainloop()
