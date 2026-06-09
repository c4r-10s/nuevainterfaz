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
            "descripcion": descripcion,
            "calificacion": 0.0,
            "estado": "No Revisado",
            "fecha_revision": "",
            "archivo": archivo,
            "obs_asesor": ""  # Campo compartido con Tutores
        }
        self.array_dinamico.append(nuevo_registro)

    def modificar_registro(self, id_evidencia, id_estudiante, nombre_estudiante, nombre_evidencia, fecha_carga, descripcion, archivo):
        for registro in self.array_dinamico:
            if registro["IDevidencia"] == id_evidencia:
                registro["IDestudiante"] = id_estudiante
                registro["NombreEstudiante"] = nombre_estudiante
                registro["NombreEvidencia"] = nombre_evidencia
                registro["FechadeCarga"] = fecha_carga
                registro["descripcion"] = descripcion
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


# =========================================================================
# CLASE DIRECTOR (Herencia, Arrays Dinámicos y Control de Estudiantes/Grupos)
# =========================================================================
class Director(Evidencias):
    def __init__(self):
        super().__init__()
        self.colegios = []
        self.profesores = []
        self.grupos_estudiantes = []
        self.preguntas = []
        self.estudiantes_global = []
        self.reuniones_global = [] # Array dinámico para las reuniones

    # Métodos para gestionar reuniones
    def guardar_reunion(self, fecha, id_est, tema, observaciones):
        nueva_reunion = {
            "fecha": fecha,
            "id_estudiante": id_est,
            "tema": tema,
            "observaciones": observaciones
        }
        self.reuniones_global.append(nueva_reunion)

    def obtener_reuniones(self):
        return self.reuniones_global

    # NUEVO: Método para verificar si el estudiante existe en el sistema
    def existe_estudiante(self, id_estudiante):
        # Verifica en los alumnos registrados globales (por el director)
        en_global = any(e["id"] == id_estudiante for e in self.estudiantes_global)
        # Verifica en las evidencias ya subidas (por la pestaña estudiantes)
        en_evidencias = any(reg["IDestudiante"] == id_estudiante for reg in self.array_dinamico)
        return en_global or en_evidencias

    def guardar_estudiante(self, id_est, nombre, grupo, modo_edit):
        if modo_edit:
            for e in self.estudiantes_global:
                if e["id"] == id_est:
                    e["nombre"] = nombre
                    e["grupo"] = grupo
                    return True
        else:
            if any(e["id"] == id_est for e in self.estudiantes_global): return False
            self.estudiantes_global.append({"id": id_est, "nombre": nombre, "grupo": grupo})
            return True

    def eliminar_estudiante(self, id_est):
        self.estudiantes_global = [e for e in self.estudiantes_global if e["id"] != id_est]

    def obtener_estudiantes_por_grupo(self, grupo):
        return [e for e in self.estudiantes_global if e["grupo"] == grupo]

    def guardar_colegio(self, id_col, nombre, direccion, modo_edit):
        if modo_edit:
            for c in self.colegios:
                if c["id"] == id_col:
                    c["nombre"] = nombre
                    c["direccion"] = direccion
                    return True
        else:
            if any(c["id"] == id_col for c in self.colegios): return False
            self.colegios.append({"id": id_col, "nombre": nombre, "direccion": direccion})
            return True

    def eliminar_colegio(self, id_col):
        self.colegios = [c for c in self.colegios if c["id"] != id_col]

    def guardar_profesor(self, id_prof, nombre, especialidad, modo_edit):
        if modo_edit:
            for p in self.profesores:
                if p["id"] == id_prof:
                    p["nombre"] = nombre
                    p["especialidad"] = especialidad
                    return True
        else:
            if any(p["id"] == id_prof for p in self.profesores): return False
            self.profesores.append({"id": id_prof, "nombre": nombre, "especialidad": especialidad})
            return True

    def eliminar_profesor(self, id_prof):
        self.profesores = [p for p in self.profesores if p["id"] != id_prof]

    def guardar_grupo(self, id_grup, letra_grup, id_prof, modo_edit):
        if modo_edit:
            for g in self.grupos_estudiantes:
                if g["id"] == id_grup:
                    g["letra"] = letra_grup
                    g["id_profesor"] = id_prof
                    return True
        else:
            if any(g["id"] == id_grup for g in self.grupos_estudiantes): return False
            self.grupos_estudiantes.append({"id": id_grup, "letra": letra_grup, "id_profesor": id_prof})
            return True

    def eliminar_grupo(self, id_grup):
        self.grupos_estudiantes = [g for g in self.grupos_estudiantes if g["id"] != id_grup]

    def guardar_pregunta(self, id_pre, enunciado, id_evidencia, modo_edit):
        if modo_edit:
            for p in self.preguntas:
                if p["id"] == id_pre:
                    p["enunciado"] = enunciado
                    p["id_evidencia"] = id_evidencia
                    return True
        else:
            if any(p["id"] == id_pre for p in self.preguntas): return False
            self.preguntas.append({"id": id_pre, "enunciado": enunciado, "id_evidencia": id_evidencia})
            return True

    def eliminar_pregunta(self, id_pre):
        self.preguntas = [p for p in self.preguntas if p["id"] != id_pre]


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

LETRAS_GRUPOS = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
gestor_evidencias = Director()
ruta_archivo = ""
modo_edicion = False
id_seleccionado = None
id_evidencia_asesor_sel = None

# ==========================================
# FUNCIONES DE UI - NAVEGACIÓN ENTRE VISTAS
# ==========================================
def mostrar_submenu(menu):
    frame_estudiantes.place_forget()
    frame_tutores.place_forget()
    frame_asesores.place_forget()
    frame_director_menu.place_forget()
    frame_ver_grupos_menu.place_forget()

    if menu == "estudiantes":
        frame_estudiantes.place(x=40, y=85)
        lbl_ruta.config(text="Estudiantes > Gestión de Evidencias")
        volver_al_menu_principal()  
    elif menu == "tutores":
        frame_tutores.place(x=40, y=165)
        lbl_ruta.config(text="Tutores Académicos")
    elif menu == "asesores":
        frame_asesores.place(x=40, y=245)
        lbl_ruta.config(text="Asesores Pedagógicos")
        ir_a_asesores_pedagogicos()
    elif menu == "director":
        frame_director_menu.place(x=40, y=365)
        lbl_ruta.config(text="Director > Panel de Control General")
        ir_a_panel_director()
    elif menu == "ver_grupos":
        frame_ver_grupos_menu.place(x=40, y=445)
        lbl_ruta.config(text="Consulta > Estudiantes por Grupo")
        ir_a_vista_grupos()

def ir_a_revision_evidencias():
    ocultar_todos_los_paneles()
    frame_revision.place(x=275, y=80)
    refrescar_tabla_revision()

def ir_a_asesores_pedagogicos():
    ocultar_todos_los_paneles()
    frame_asesores_panel.place(x=275, y=80)
    limpiar_campos_asesor()
    refrescar_tabla_asesores()

def ir_a_reuniones_asesor():
    ocultar_todos_los_paneles()
    frame_reuniones_panel.place(x=275, y=80)
    limpiar_campos_reunion()
    refrescar_tabla_reuniones()

def volver_al_menu_principal():
    ocultar_todos_los_paneles()
    frame_principal.place(x=275, y=80)
    refrescar_tabla()

def ir_a_panel_director():
    ocultar_todos_los_paneles()
    frame_director.place(x=275, y=80)
    actualizar_combos_director()
    refrescar_tablas_director()

def ir_a_vista_grupos():
    ocultar_todos_los_paneles()
    frame_ver_grupos.place(x=275, y=80)
    combo_filtro_letra.set("")
    tabla_filtro_grupos.delete(*tabla_filtro_grupos.get_children())

def ocultar_todos_los_paneles():
    frame_principal.place_forget()
    frame_revision.place_forget()
    frame_asesores_panel.place_forget()
    frame_reuniones_panel.place_forget()
    frame_director.place_forget()
    frame_ver_grupos.place_forget()

def salir():
    if messagebox.askyesno("Salir", "¿Desea salir del sistema?"):
        ventana.destroy()

# ==========================================
# GESTIÓN TABLA ESTUDIANTE (ENTREGA EVIDENCIAS)
# ==========================================
def refrescar_tabla():
    tabla.delete(*tabla.get_children())
    for reg in gestor_evidencias.obtener_todos():
        tabla.insert("", "end", values=(
            reg["IDevidencia"], reg["NombreEvidencia"], reg["FechadeCarga"],
            reg["descripcion"], reg["calificacion"], reg["estado"],
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
    if not seleccion: return
    
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
    pop.title("Evaluación de Evidencia - Tutor")
    pop.geometry("450x450")
    pop.configure(bg="white")
    pop.resizable(False, False)
    pop.grab_set() 

    tk.Label(pop, text="Nombre Estudiante:", font=("Arial", 9, "bold"), bg="white").place(x=30, y=30)
    entry_pop_nombre = tk.Entry(pop, width=30)
    entry_pop_nombre.insert(0, nombre_est_actual)
    entry_pop_nombre.config(state="disabled") 
    entry_pop_nombre.place(x=180, y=30)

    tk.Label(pop, text="ID Estudiante:", font=("Arial", 9, "bold"), bg="white").place(x=30, y=70)
    entry_pop_id = tk.Entry(pop, width=30)
    entry_pop_id.insert(0, id_est)
    entry_pop_id.config(state="disabled") 
    entry_pop_id.place(x=180, y=70)

    tk.Label(pop, text="Path del Archivo:", font=("Arial", 9, "bold"), bg="white").place(x=30, y=110)
    entry_pop_path = tk.Entry(pop, width=30)
    entry_pop_path.insert(0, path_arch)
    entry_pop_path.config(state="disabled") 
    entry_pop_path.place(x=180, y=110)

    def abrir_archivo_sistema():
        if os.path.exists(path_arch):
            try: os.startfile(path_arch)
            except Exception as e: messagebox.showerror("Error", f"No se pudo abrir:\n{e}")
        else: messagebox.showwarning("Archivo local no encontrado", f"Ruta:\n{path_arch}")

    btn_pop_ver = tk.Button(pop, text="VER", font=("Arial", 8, "bold"), command=abrir_archivo_sistema)
    btn_pop_ver.place(x=380, y=107)

    tk.Label(pop, text="Obs. Asesor (Lectura):", font=("Arial", 9, "bold"), bg="white").place(x=30, y=150)
    entry_pop_obs = tk.Entry(pop, width=35)
    entry_pop_obs.insert(0, obs_asesor)
    entry_pop_obs.config(state="disabled")
    entry_pop_obs.place(x=180, y=150)

    tk.Label(pop, text="Nota (0.0 a 5.0):", font=("Arial", 9, "bold"), bg="white").place(x=30, y=190)
    entry_pop_nota = tk.Entry(pop, width=10)
    entry_pop_nota.insert(0, nota_actual)
    entry_pop_nota.place(x=180, y=190)

    tk.Label(pop, text="Estado:", font=("Arial", 9, "bold"), bg="white").place(x=30, y=230)
    combo_pop_estado = ttk.Combobox(pop, values=["Revisado"], state="readonly", width=15)
    combo_pop_estado.set("Revisado" if estado_actual == "Revisado" else "")
    combo_pop_estado.place(x=180, y=230)

    def guardar_evaluacion():
        estado_seleccionado = combo_pop_estado.get()
        if estado_seleccionado != "Revisado":
            messagebox.showwarning("Estado obligatorio", "Debe establecer el estado como 'Revisado'.")
            return
        try:
            nota_num = float(entry_pop_nota.get())
            if not (0.0 <= nota_num <= 5.0): raise ValueError
        except ValueError:
            messagebox.showerror("Error de entrada", "La nota debe ser un número decimal entre 0.0 y 5.0.")
            return

        for reg in gestor_evidencias.obtener_todos():
            if reg["IDevidencia"] == id_evid:
                reg["calificacion"] = nota_num
                reg["estado"] = estado_seleccionado
                reg["fecha_revision"] = datetime.now().strftime("%d/%m/%Y")
                break
        
        messagebox.showinfo("Éxito", "Evaluación del Tutor guardada.")
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

    ancho_barra = 40
    espacio = 30
    x_inicial = 70

    for index, reg in enumerate(datos):
        nota = reg.get("calificacion", 0.0)
        id_est = reg.get("IDestudiante", "N/A")
        altura_barra = int(nota * 50)
        y_top = 300 - altura_barra
        x1 = x_inicial + (index * (ancho_barra + espacio))
        canvas.create_rectangle(x1, y_top, x1 + ancho_barra, 300, fill="#4a90e2", outline="#2a60a0")
        canvas.create_text(x1 + 20, y_top - 10, text=str(nota), font=("Arial", 8, "bold"))
        canvas.create_text(x1 + 20, 315, text=f"ID:{id_est}", font=("Arial", 8), angle=45)


# =========================================================================
# ASESORES PEDAGÓGICOS: SECCIÓN CON CUADRO RECTANGULAR INTEGRADO BAJO LA REJILLA
# =========================================================================
def refrescar_tabla_asesores():
    tabla_asesores.delete(*tabla_asesores.get_children())
    for reg in gestor_evidencias.obtener_todos():
        tabla_asesores.insert("", "end", values=(
            reg["IDevidencia"],
            reg["IDestudiante"],
            reg["NombreEstudiante"],
            reg["NombreEvidencia"],
            reg.get("obs_asesor", "")
        ))

def cargar_observacion_al_seleccionar(event):
    global id_evidencia_asesor_sel
    seleccion = tabla_asesores.selection()
    if seleccion:
        valores = tabla_asesores.item(seleccion)["values"]
        id_evidencia_asesor_sel = valores[0]
        obs_actual = valores[4]
        
        txt_obs_directo.delete("1.0", tk.END)
        txt_obs_directo.insert("1.0", obs_actual)

def guardar_observacion_directa():
    global id_evidencia_asesor_sel
    if id_evidencia_asesor_sel is None:
        messagebox.showwarning("Atención", "Por favor seleccione un estudiante de la rejilla superior.")
        return
    
    nueva_obs = txt_obs_directo.get("1.0", tk.END).strip()
    
    for reg in gestor_evidencias.obtener_todos():
        if reg["IDevidencia"] == id_evidencia_asesor_sel:
            reg["obs_asesor"] = nueva_obs
            break
            
    messagebox.showinfo("Guardado", "Observación registrada correctamente. Disponible para el Tutor Académico.")
    refrescar_tabla_asesores()
    limpiar_campos_asesor()

def limpiar_campos_asesor():
    txt_obs_directo.delete("1.0", tk.END)

def salir_y_volver_al_inicio():
    global id_evidencia_asesor_sel
    id_evidencia_asesor_sel = None
    limpiar_campos_asesor()
    if tabla_asesores.selection():
        tabla_asesores.selection_remove(tabla_asesores.selection())
    
    mostrar_submenu("estudiantes")


# =========================================================================
# GESTIÓN DE REUNIONES (ASESORES PEDAGÓGICOS) - MODIFICADO CON VALIDACIÓN
# =========================================================================
def refrescar_tabla_reuniones():
    tabla_reuniones.delete(*tabla_reuniones.get_children())
    for reun in gestor_evidencias.obtener_reuniones():
        tabla_reuniones.insert("", "end", values=(
            reun["fecha"],
            reun["id_estudiante"],
            reun["tema"],
            reun["observaciones"]
        ))

def guardar_nueva_reunion():
    fecha = ent_reun_fecha.get().strip()
    id_est = ent_reun_id_est.get().strip()
    tema = ent_reun_tema.get().strip()
    obs = txt_reun_obs.get("1.0", tk.END).strip()

    if not fecha or not id_est or not tema or not obs:
        messagebox.showwarning("Campos incompletos", "Por favor complete todos los campos de la reunión.")
        return

    try:
        id_est_num = int(id_est)
        if id_est_num <= 0: raise ValueError
    except ValueError:
        messagebox.showwarning("ID Estudiante Inválido", "El ID del Estudiante debe ser un número entero positivo.")
        return

    # MODIFICACIÓN CRÍTICA: Validar si el estudiante existe en el sistema
    if not gestor_evidencias.existe_estudiante(id_est_num):
        messagebox.showerror(
            "Estudiante no encontrado", 
            f"El ID Estudiante {id_est_num} no se encuentra registrado en el sistema.\n"
            "Debe ser ingresado previamente en la pestaña de estudiantes o por el director."
        )
        return

    gestor_evidencias.guardar_reunion(fecha, id_est_num, tema, obs)
    messagebox.showinfo("Éxito", "Reunión almacenada correctamente.")
    refrescar_tabla_reuniones()
    limpiar_campos_reunion()

def limpiar_campos_reunion():
    ent_reun_fecha.delete(0, tk.END)
    ent_reun_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
    ent_reun_id_est.delete(0, tk.END)
    ent_reun_tema.delete(0, tk.END)
    txt_reun_obs.delete("1.0", tk.END)


# ==========================================
# CONSTRUCCIÓN INTERFAZ GRÁFICA GENERAL
# ==========================================
frame_superior = tk.Frame(ventana, width=1032, height=60, bd=1, relief="solid", bg="white")
frame_superior.place(x=24, y=10)

try:
    imagen_logo = tk.PhotoImage(file=r"C:\Users\SALA-2\Downloads\Programacion\logoudi2.png")
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
btn_asesores.place(x=20, y=220)

btn_director = tk.Button(frame_menu, text="Director General", bd=0, bg="white", font=("Arial", 10, "bold"), fg="darkred", anchor="w", command=lambda: mostrar_submenu("director"))
btn_director.place(x=20, y=330)

btn_ver_grupos = tk.Button(frame_menu, text="Ver por Grupos", bd=0, bg="white", font=("Arial", 10, "bold"), fg="blue", anchor="w", command=lambda: mostrar_submenu("ver_grupos"))
btn_ver_grupos.place(x=20, y=410)

frame_estudiantes = tk.Frame(frame_menu, bg="white")
tk.Label(frame_estudiantes, text="└ Gestión de Evidencias", bg="white").pack(anchor="w")

frame_tutores = tk.Frame(frame_menu, bg="white")
btn_sub_revisar = tk.Button(frame_tutores, text="└ Revisar Evidencias", bg="white", bd=0, command=ir_a_revision_evidencias)
btn_sub_revisar.pack(anchor="w")

frame_asesores = tk.Frame(frame_menu, bg="white")
btn_sub_obs = tk.Button(frame_asesores, text="└ Evaluar Campo Obs.", bg="white", bd=0, command=ir_a_asesores_pedagogicos)
btn_sub_obs.pack(anchor="w")
btn_sub_reuniones = tk.Button(frame_asesores, text="└ Reuniones", bg="white", bd=0, command=ir_a_reuniones_asesor)
btn_sub_reuniones.pack(anchor="w")

frame_director_menu = tk.Frame(frame_menu, bg="white")
tk.Label(frame_director_menu, text="└ Panel Global CRUD", fg="darkred", bg="white").pack(anchor="w")

frame_ver_grupos_menu = tk.Frame(frame_menu, bg="white")
tk.Label(frame_ver_grupos_menu, text="└ Consulta A - Z", fg="blue", bg="white").pack(anchor="w")

btn_salir = tk.Button(frame_menu, text="Salir App", width=15, command=salir)
btn_salir.place(x=20, y=570)


# ==========================================
# PANEL DERECHO 1: ESTUDIANTES
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
# PANEL DERECHO 2: REVISIÓN DE EVIDENCIAS (TUTORES)
# ==========================================
frame_revision = tk.Frame(ventana, width=780, height=620, bd=1, relief="solid", bg="white")

lbl_sub1 = tk.Label(frame_revision, text="Tutor Académico", font=("Arial", 14, "bold"), bg="white", fg="#333333")
lbl_sub1.place(x=15, y=15)

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

btn_informe = tk.Button(frame_revision, text="Informe", width=15, font=("Arial", 10, "bold"), command=mostrar_histograma_informe)
btn_informe.place(x=15, y=550)


# =========================================================================
# PANEL DERECHO 3: ASESORES PEDAGÓGICOS
# =========================================================================
frame_asesores_panel = tk.Frame(ventana, width=780, height=620, bd=1, relief="solid", bg="white")

lbl_as_tit = tk.Label(frame_asesores_panel, text="Panel de Asesores Pedagógicos", font=("Arial", 14, "bold"), bg="white", fg="#4a90e2")
lbl_as_tit.place(x=15, y=12)

columnas_as = ("id_evid", "id_est", "nom_est", "nom_evid", "obs_asesor")
tabla_asesores = ttk.Treeview(frame_asesores_panel, columns=columnas_as, show="headings", height=11)

tabla_asesores.heading("id_evid", text="ID Evidencia")
tabla_asesores.heading("id_est", text="ID Estudiante")
tabla_asesores.heading("nom_est", text="Nombre Estudiante")
tabla_asesores.heading("nom_evid", text="Evidencia")
tabla_asesores.heading("obs_asesor", text="Obs. Asesor (Destino Tutor)")

tabla_asesores.column("id_evid", width=80, anchor="center")
tabla_asesores.column("id_est", width=90, anchor="center")
tabla_asesores.column("nom_est", width=170)
tabla_asesores.column("nom_evid", width=150)
tabla_asesores.column("obs_asesor", width=250)
tabla_asesores.place(x=15, y=45)

tabla_asesores.bind("<<TreeviewSelect>>", cargar_observacion_al_seleccionar)

lbl_obs_titulo = tk.Label(frame_asesores_panel, text="Observaciones", font=("Arial", 11, "bold"), bg="white", fg="#333333")
lbl_obs_titulo.place(x=15, y=320)

txt_obs_directo = tk.Text(frame_asesores_panel, width=91, height=9, bd=1, relief="solid", font=("Arial", 10))
txt_obs_directo.place(x=15, y=345)

btn_as_salir = tk.Button(frame_asesores_panel, text="Salir", width=15, font=("Arial", 10), command=salir_y_volver_al_inicio)
btn_as_salir.place(x=15, y=530)

btn_as_guardar = tk.Button(frame_asesores_panel, text="Guardar", width=15, font=("Arial", 10, "bold"), command=guardar_observacion_directa)
btn_as_guardar.place(x=160, y=530)

btn_as_limpiar = tk.Button(frame_asesores_panel, text="Limpiar", width=15, font=("Arial", 10), command=limpiar_campos_asesor)
btn_as_limpiar.place(x=305, y=530)


# =========================================================================
# PANEL DERECHO 3.5: GESTIÓN DE REUNIONES (ASESOR PEDAGÓGICO)
# =========================================================================
frame_reuniones_panel = tk.Frame(ventana, width=780, height=620, bd=1, relief="solid", bg="white")

lbl_reun_tit = tk.Label(frame_reuniones_panel, text="Registro de Reuniones", font=("Arial", 14, "bold"), bg="white", fg="#4a90e2")
lbl_reun_tit.place(x=15, y=12)

# Formulario de Entrada
tk.Label(frame_reuniones_panel, text="Fecha (DD/MM/AAAA):", bg="white", font=("Arial", 9, "bold")).place(x=15, y=50)
ent_reun_fecha = tk.Entry(frame_reuniones_panel, width=15)
ent_reun_fecha.place(x=160, y=50)

tk.Label(frame_reuniones_panel, text="ID Estudiante:", bg="white", font=("Arial", 9, "bold")).place(x=15, y=85)
ent_reun_id_est = tk.Entry(frame_reuniones_panel, width=15)
ent_reun_id_est.place(x=160, y=85)

tk.Label(frame_reuniones_panel, text="Tema de Reunión:", bg="white", font=("Arial", 9, "bold")).place(x=300, y=50)
ent_reun_tema = tk.Entry(frame_reuniones_panel, width=45)
ent_reun_tema.place(x=430, y=50)

tk.Label(frame_reuniones_panel, text="Observaciones:", bg="white", font=("Arial", 9, "bold")).place(x=300, y=85)
txt_reun_obs = tk.Text(frame_reuniones_panel, width=40, height=3, bd=1, relief="solid", font=("Arial", 9))
txt_reun_obs.place(x=430, y=85)

# Botones de Acción
btn_reun_guardar = tk.Button(frame_reuniones_panel, text="Guardar Reunión", font=("Arial", 9, "bold"), bg="#4a90e2", fg="white", command=guardar_nueva_reunion)
btn_reun_guardar.place(x=15, y=130)

btn_reun_limpiar = tk.Button(frame_reuniones_panel, text="Limpiar", font=("Arial", 9), command=limpiar_campos_reunion)
btn_reun_limpiar.place(x=150, y=130)

# Rejilla (Treeview) para mostrar registros guardados
columnas_reun = ("fecha", "id_est", "tema", "observaciones")
tabla_reuniones = ttk.Treeview(frame_reuniones_panel, columns=columnas_reun, show="headings", height=15)

tabla_reuniones.heading("fecha", text="Fecha")
tabla_reuniones.heading("id_est", text="ID Estudiante")
tabla_reuniones.heading("tema", text="Tema de la Reunión")
tabla_reuniones.heading("observaciones", text="Observaciones del Asesor")

tabla_reuniones.column("fecha", width=100, anchor="center")
tabla_reuniones.column("id_est", width=100, anchor="center")
tabla_reuniones.column("tema", width=220, anchor="w")
tabla_reuniones.column("observaciones", width=320, anchor="w")
tabla_reuniones.place(x=15, y=180)


# ==========================================
# PANEL DERECHO 4: INTERFAZ DEL DIRECTOR
# ==========================================
frame_director = tk.Frame(ventana, width=780, height=620, bd=1, relief="solid", bg="#fcfcfc")

notebook = ttk.Notebook(frame_director, width=750, height=540)
notebook.place(x=15, y=45)

tab_estudiantes_dir = tk.Frame(notebook, bg="white")
tab_colegios = tk.Frame(notebook, bg="white")
tab_profesores = tk.Frame(notebook, bg="white")
tab_grupos = tk.Frame(notebook, bg="white")
tab_preguntas = tk.Frame(notebook, bg="white")

notebook.add(tab_estudiantes_dir, text="1. Registrar Estudiantes")
notebook.add(tab_colegios, text="2. Colegios")
notebook.add(tab_profesores, text="3. Profesores")
notebook.add(tab_grupos, text="4. Grupos a Profesores")
notebook.add(tab_preguntas, text="5. Subir Preguntas")

edit_est_d = False

def refrescar_tablas_director():
    tabla_est_dir.delete(*tabla_est_dir.get_children())
    for e in gestor_evidencias.estudiantes_global:
        tabla_est_dir.insert("", "end", values=(e["id"], e["nombre"], e["grupo"]))
    tabla_col.delete(*tabla_col.get_children())
    for c in gestor_evidencias.colegios:
        tabla_col.insert("", "end", values=(c["id"], c["nombre"], c["direccion"]))
    tabla_prof.delete(*tabla_prof.get_children())
    for p in gestor_evidencias.profesores:
        tabla_prof.insert("", "end", values=(p["id"], p["nombre"], p["especialidad"]))
    tabla_grup.delete(*tabla_grup.get_children())
    for g in gestor_evidencias.grupos_estudiantes:
        tabla_grup.insert("", "end", values=(g["id"], g["letra"], g["id_profesor"]))
    tabla_pre.delete(*tabla_pre.get_children())
    for pr in gestor_evidencias.preguntas:
        tabla_pre.insert("", "end", values=(pr["id"], pr["enunciado"], pr["id_evidencia"]))

def actualizar_combos_director():
    list_profs = [f"{p['id']} - {p['nombre']}" for p in gestor_evidencias.profesores]
    combo_grup_prof.config(values=list_profs)
    list_evid = [str(reg["IDevidencia"]) for reg in gestor_evidencias.obtener_todos()]
    combo_pre_evid.config(values=list_evid)

def limpiar_estudiante_dir():
    global edit_est_d
    edit_est_d = False
    ent_est_id.config(state="normal")
    ent_est_id.delete(0, tk.END)
    ent_est_nom.delete(0, tk.END)
    combo_est_grupo.set("")

def accion_guardar_estudiante():
    try:
        id_e = int(ent_est_id.get().strip())
        nom = ent_est_nom.get().strip()
        grup = combo_est_grupo.get()
        if not nom or not grup: raise Exception
        res = gestor_evidencias.guardar_estudiante(id_e, nom, grup, edit_est_d)
        if res:
            messagebox.showinfo("Éxito", "Estudiante registrado.")
            refrescar_tablas_director()
            limpiar_estudiante_dir()
        else: messagebox.showwarning("Error", "ID duplicado.")
    except: messagebox.showwarning("Error", "Campos inválidos.")

def cargar_estudiante_dir(event):
    global edit_est_d
    sel = tabla_est_dir.selection()
    if sel:
        datos = tabla_est_dir.item(sel)["values"]
        limpiar_estudiante_dir()
        ent_est_id.insert(0, datos[0])
        ent_est_id.config(state="disabled")
        ent_est_nom.insert(0, datos[1])
        combo_est_grupo.set(datos[2])
        edit_est_d = True

tk.Label(tab_estudiantes_dir, text="ID Estudiante:", bg="white", font=("Arial", 9, "bold")).place(x=20, y=20)
ent_est_id = tk.Entry(tab_estudiantes_dir, width=15)
ent_est_id.place(x=140, y=20)
tk.Label(tab_estudiantes_dir, text="Nombre Completo:", bg="white", font=("Arial", 9, "bold")).place(x=20, y=55)
ent_est_nom = tk.Entry(tab_estudiantes_dir, width=30)
ent_est_nom.place(x=140, y=55)
tk.Label(tab_estudiantes_dir, text="Grupo (A-Z):", bg="white", font=("Arial", 9, "bold")).place(x=20, y=90)
combo_est_grupo = ttk.Combobox(tab_estudiantes_dir, values=LETRAS_GRUPOS, state="readonly", width=10)
combo_est_grupo.place(x=140, y=90)
tk.Button(tab_estudiantes_dir, text="Guardar", command=accion_guardar_estudiante).place(x=140, y=130)

tabla_est_dir = ttk.Treeview(tab_estudiantes_dir, columns=("id", "nom", "grup"), show="headings", height=12)
tabla_est_dir.heading("id", text="ID Estudiante"); tabla_est_dir.heading("nom", text="Nombre del Alumno"); tabla_est_dir.heading("grup", text="Grupo Asignado")
tabla_est_dir.column("id", width=120, anchor="center"); tabla_est_dir.column("nom", width=350); tabla_est_dir.column("grup", width=150, anchor="center")
tabla_est_dir.place(x=20, y=180)
tabla_est_dir.bind("<<TreeviewSelect>>", cargar_estudiante_dir)

def accion_guardar_colegio():
    try:
        id_c = int(ent_col_id.get().strip())
        nom = ent_col_nom.get().strip()
        dir_c = ent_col_dir.get().strip()
        if gestor_evidencias.guardar_colegio(id_c, nom, dir_c, False): refrescar_tablas_director()
    except: pass

tk.Label(tab_colegios, text="ID Colegio:", bg="white").place(x=20, y=20)
ent_col_id = tk.Entry(tab_colegios, width=15)
ent_col_id.place(x=120, y=20)
tk.Label(tab_colegios, text="Nombre:", bg="white").place(x=20, y=55)
ent_col_nom = tk.Entry(tab_colegios, width=30)
ent_col_nom.place(x=120, y=55)
tk.Label(tab_colegios, text="Dirección:", bg="white").place(x=20, y=90)
ent_col_dir = tk.Entry(tab_colegios, width=30)
ent_col_dir.place(x=120, y=90)
tk.Button(tab_colegios, text="Guardar", command=accion_guardar_colegio).place(x=120, y=130)
tabla_col = ttk.Treeview(tab_colegios, columns=("id", "nom", "dir"), show="headings", height=12)
tabla_col.heading("id", text="ID"); tabla_col.heading("nom", text="Colegio"); tabla_col.heading("dir", text="Dirección")
tabla_col.place(x=20, y=180)

def accion_guardar_profesor():
    try:
        id_p = int(ent_prof_id.get().strip())
        nom = ent_prof_nom.get().strip()
        esp = ent_prof_esp.get().strip()
        if gestor_evidencias.guardar_profesor(id_p, nom, esp, False):
            refrescar_tablas_director(); actualizar_combos_director()
    except: pass

tk.Label(tab_profesores, text="ID Profesor:", bg="white").place(x=20, y=20)
ent_prof_id = tk.Entry(tab_profesores, width=15)
ent_prof_id.place(x=120, y=20)
tk.Label(tab_profesores, text="Nombre:", bg="white").place(x=20, y=55)
ent_prof_nom = tk.Entry(tab_profesores, width=30)
ent_prof_nom.place(x=120, y=55)
tk.Label(tab_profesores, text="Especialidad:", bg="white").place(x=20, y=90)
ent_prof_esp = tk.Entry(tab_profesores, width=30)
ent_prof_esp.place(x=120, y=90)
tk.Button(tab_profesores, text="Guardar", command=accion_guardar_profesor).place(x=120, y=130)
tabla_prof = ttk.Treeview(tab_profesores, columns=("id", "nom", "esp"), show="headings", height=12)
tabla_prof.heading("id", text="ID"); tabla_prof.heading("nom", text="Profesor"); tabla_prof.heading("esp", text="Especialidad")
tabla_prof.place(x=20, y=180)

def accion_guardar_grupo():
    try:
        id_g = int(ent_grup_id.get().strip())
        letra = combo_grup_letra.get()
        prof_sel = combo_grup_prof.get()
        id_p = int(prof_sel.split(" - ")[0]) if prof_sel else 0
        if gestor_evidencias.guardar_grupo(id_g, letra, id_p, False): refrescar_tablas_director()
    except: pass

tk.Label(tab_grupos, text="ID Registro:", bg="white").place(x=20, y=20)
ent_grup_id = tk.Entry(tab_grupos, width=15)
ent_grup_id.place(x=140, y=20)
tk.Label(tab_grupos, text="Letra Grupo:", bg="white").place(x=20, y=55)
combo_grup_letra = ttk.Combobox(tab_grupos, values=LETRAS_GRUPOS, state="readonly", width=12)
combo_grup_letra.place(x=140, y=55)
tk.Label(tab_grupos, text="Profesor:", bg="white").place(x=20, y=90)
combo_grup_prof = ttk.Combobox(tab_grupos, state="readonly", width=30)
combo_grup_prof.place(x=140, y=90)
tk.Button(tab_grupos, text="Asignar", command=accion_guardar_grupo).place(x=140, y=130)
tabla_grup = ttk.Treeview(tab_grupos, columns=("id", "letra", "prof"), show="headings", height=11)
tabla_grup.heading("id", text="ID Reg"); tabla_grup.heading("letra", text="Grupo"); tabla_grup.heading("prof", text="ID Profesor")
tabla_grup.place(x=20, y=185)

tk.Label(tab_preguntas, text="ID Pregunta:", bg="white").place(x=20, y=20)
ent_pre_id = tk.Entry(tab_preguntas, width=15)
ent_pre_id.place(x=150, y=20)
tk.Label(tab_preguntas, text="Enunciado:", bg="white").place(x=20, y=55)
ent_pre_enun = tk.Entry(tab_preguntas, width=50)
ent_pre_enun.place(x=150, y=55)
tk.Label(tab_preguntas, text="ID Evidencia:", bg="white").place(x=20, y=90)
combo_pre_evid = ttk.Combobox(tab_preguntas, state="readonly", width=15)
combo_pre_evid.place(x=150, y=90)
tabla_pre = ttk.Treeview(tab_preguntas, columns=("id", "enun", "evid"), show="headings", height=12)
tabla_pre.heading("id", text="ID"); tabla_pre.heading("enun", text="Pregunta"); tabla_pre.heading("evid", text="Evidencia")
tabla_pre.place(x=20, y=180)


# ==========================================
# PANEL DERECHO 5: VISUALIZAR GRUPOS
# ==========================================
frame_ver_grupos = tk.Frame(ventana, width=780, height=620, bd=1, relief="solid", bg="white")
lbl_tit_filtro = tk.Label(frame_ver_grupos, text="CONSULTA DE GRUPOS INSTITUCIONALES", font=("Arial", 14, "bold"), bg="white", fg="blue")
lbl_tit_filtro.place(x=15, y=15)

def filtrar_estudiantes_por_letra(event):
    letra_seleccionada = combo_filtro_letra.get()
    tabla_filtro_grupos.delete(*tabla_filtro_grupos.get_children())
    lista_alumnos = gestor_evidencias.obtener_estudiantes_por_grupo(letra_seleccionada)
    for alum in lista_alumnos:
        tabla_filtro_grupos.insert("", "end", values=(alum["id"], alum["nombre"], f"Grupo {alum['grupo']}"))

combo_filtro_letra = ttk.Combobox(frame_ver_grupos, values=LETRAS_GRUPOS, state="readonly", font=("Arial", 11, "bold"), width=8)
combo_filtro_letra.place(x=260, y=58)
combo_filtro_letra.bind("<<ComboboxSelected>>", filtrar_estudiantes_por_letra)

tabla_filtro_grupos = ttk.Treeview(frame_ver_grupos, columns=("id", "nom", "grup"), show="headings", height=20)
tabla_filtro_grupos.heading("id", text="ID Estudiante"); tabla_filtro_grupos.heading("nom", text="Nombre Completo"); tabla_filtro_grupos.heading("grup", text="Grupo")
tabla_filtro_grupos.column("id", width=150, anchor="center"); tabla_filtro_grupos.column("nom", width=420); tabla_filtro_grupos.column("grup", width=160, anchor="center")
tabla_filtro_grupos.place(x=15, y=110)

# Inicialización por defecto
nueva_evidencia() 
refrescar_tabla()
ventana.mainloop()
