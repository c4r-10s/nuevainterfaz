import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os

# =========================
# CONFIGURACIÓN PRINCIPAL
# =========================

ventana = tk.Tk()
ventana.title("Sistema de Evidencias")

# Tamaño ventana
ancho = 900
alto = 700

# Centrar ventana
pantalla_ancho = ventana.winfo_screenwidth()
pantalla_alto = ventana.winfo_screenheight()

x = int((pantalla_ancho / 2) - (ancho / 2))
y = int((pantalla_alto / 2) - (alto / 2))

ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
ventana.configure(bg="white")
ventana.resizable(False, False)

# =========================
# VARIABLES
# =========================

ruta_archivo = ""
contador_id = 1
modo_edicion = False

# =========================
# FUNCIONES
# =========================

def mostrar_submenu(menu):

    # OCULTAR TODOS
    frame_estudiantes.place_forget()
    frame_tutores.place_forget()
    frame_asesores.place_forget()

    # MOSTRAR SOLO EL SELECCIONADO
    if menu == "estudiantes":

        frame_estudiantes.place(x=40, y=85)

        lbl_ruta.config(
            text="Estudiantes > Gestión de Evidencias"
        )

    elif menu == "tutores":

        frame_tutores.place(x=40, y=165)

        lbl_ruta.config(
            text="Tutores Académicos"
        )

    elif menu == "asesores":

        frame_asesores.place(x=40, y=255)

        lbl_ruta.config(
            text="Asesores Pedagógicos > Observaciones"
        )


def salir():

    respuesta = messagebox.askyesno(
        "Salir",
        "¿Desea salir del sistema?"
    )

    if respuesta:
        ventana.destroy()


def nueva_evidencia():

    global ruta_archivo

    combo_tipo.set("")

    entry_nombre.delete(0, tk.END)

    txt_descripcion.delete("1.0", tk.END)

    entry_fecha.config(state="normal")

    entry_fecha.delete(0, tk.END)

    entry_fecha.insert(
        0,
        datetime.now().strftime("%d/%m/%Y")
    )

    entry_fecha.config(state="readonly")

    ruta_archivo = ""

    lbl_archivo.config(text="Sin archivo")


def cargar_archivo():

    global ruta_archivo

    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[
            ("Archivos permitidos", "*.pdf *.doc *.docx *.xls *.xlsx")
        ]
    )

    if archivo:

        tipo = combo_tipo.get()

        if tipo == "":
            messagebox.showwarning("Atención", "Selecciona primero el tipo de evidencia")
            return

        if not validar_archivo(tipo, archivo):
            messagebox.showerror(
                "Archivo inválido",
                f"El archivo no corresponde al tipo seleccionado: {tipo}"
            )
            return

        ruta_archivo = archivo
        lbl_archivo.config(text=os.path.basename(archivo))


def aceptar():

    global contador_id
    global ruta_archivo

    tipo = combo_tipo.get()
    nombre = entry_nombre.get()
    fecha = entry_fecha.get()
    descripcion = txt_descripcion.get("1.0", tk.END).strip()

    # VALIDACIÓN COMPLETA
    if tipo == "" or nombre.strip() == "" or descripcion == "" or ruta_archivo == "":
        messagebox.showwarning(
            "Campos incompletos",
            "Debes completar todos los campos y cargar un archivo"
        )
        return

    tabla.insert(
        "",
        "end",
        values=(
            contador_id,
            nombre,
            tipo,
            fecha,
            descripcion,
            ruta_archivo
        )
    )

    contador_id += 1

    messagebox.showinfo("Correcto", "Evidencia registrada correctamente")

    nueva_evidencia()

def eliminar():

    seleccionado = tabla.selection()

    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un registro")
        return

    confirmar1 = messagebox.askyesno(
        "Confirmar eliminación",
        "¿Seguro que deseas eliminar este registro?"
    )

    if not confirmar1:
        return

    confirmar2 = messagebox.askyesno(
        "Confirmación final",
        "Esta acción no se puede deshacer. ¿Deseas continuar?"
    )

    if confirmar2:
        tabla.delete(seleccionado)
        messagebox.showinfo("Eliminado", "Registro eliminado correctamente")


def cargar_datos(event):

    seleccionado = tabla.selection()

    if seleccionado:

        datos = tabla.item(seleccionado)["values"]

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, datos[1])

        combo_tipo.set(datos[2])

        entry_fecha.config(state="normal")

        entry_fecha.delete(0, tk.END)

        entry_fecha.insert(0, datos[3])

        entry_fecha.config(state="readonly")

        txt_descripcion.delete("1.0", tk.END)

        txt_descripcion.insert("1.0", datos[4])

        lbl_archivo.config(
            text=os.path.basename(str(datos[5]))
        )

def bloquear_campos(estado):

    if estado:
        entry_nombre.config(state="normal")
        txt_descripcion.config(state="normal")
        combo_tipo.config(state="readonly")
    else:
        entry_nombre.config(state="disabled")
        txt_descripcion.config(state="disabled")
        combo_tipo.config(state="readonly")
    
def modificar():

    global modo_edicion
    global ruta_archivo

    seleccionado = tabla.selection()

    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un registro")
        return

    # ESTO ACTIVA EDICION
    if not modo_edicion:

        datos = tabla.item(seleccionado)["values"]

        entry_nombre.config(state="normal")
        txt_descripcion.config(state="normal")
        combo_tipo.config(state="readonly")

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, datos[1])

        combo_tipo.set(datos[2])

        entry_fecha.config(state="normal")
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, datos[3])
        entry_fecha.config(state="readonly")

        txt_descripcion.delete("1.0", tk.END)
        txt_descripcion.insert("1.0", datos[4])

        ruta_archivo = datos[5]
        lbl_archivo.config(text=os.path.basename(str(datos[5])))

        bloquear_campos(True)

        modo_edicion = True

        messagebox.showinfo("Edición", "Ahora puedes modificar los campos")

        return

    # GUARDAR CAMBIOS
    tipo = combo_tipo.get()
    nombre = entry_nombre.get()
    fecha = entry_fecha.get()
    descripcion = txt_descripcion.get("1.0", tk.END).strip()

    if tipo == "" or nombre.strip() == "" or descripcion == "" or ruta_archivo == "":
        messagebox.showwarning("Campos incompletos", "Completa todos los campos")
        return

    valores_actuales = tabla.item(seleccionado)["values"]

    tabla.item(
        seleccionado,
        values=(
            valores_actuales[0],
            nombre,
            tipo,
            fecha,
            descripcion,
            ruta_archivo
        )
    )

    bloquear_campos(False)
    modo_edicion = False

    messagebox.showinfo("Correcto", "Registro actualizado")
    
def validar_archivo(tipo, archivo):

    if archivo == "":
        return False

    archivo = archivo.lower()

    if tipo == "PDF":
        return archivo.endswith(".pdf")

    elif tipo == "Word":
        return archivo.endswith(".doc") or archivo.endswith(".docx")

    elif tipo == "Excel":
        return archivo.endswith(".xls") or archivo.endswith(".xlsx")

    return False
# =========================
# ENCABEZADO
# =========================

frame_superior = tk.Frame(
    ventana,
    width=850,
    height=60,
    bd=1,
    relief="solid",
    bg="white"
)

frame_superior.place(x=25, y=10)

# =========================
# LOGO
# =========================

ruta_logo = r"C:\Users\SALA-2\Desktop\logo (2).png"

try:

    imagen_logo = tk.PhotoImage(file=ruta_logo)

    lbl_logo = tk.Label(
        frame_superior,
        image=imagen_logo,
        bg="white"
    )

    lbl_logo.image = imagen_logo

    lbl_logo.place(x=50, y=-20)

except Exception as e:

    print("ERROR LOGO:", e)

    lbl_logo = tk.Label(
        frame_superior,
        text="LOGO",
        bg="#D9D9D9",
        font=("Arial", 12, "bold")
    )

    lbl_logo.place(x=10, y=10)

# TÍTULO

lbl_titulo = tk.Label(
    frame_superior,
    text="Software Carlos",
    font=("Arial", 18, "bold"),
    bg="white"
)

lbl_titulo.place(x=400, y=15)

# =========================
# PANEL IZQUIERDO
# =========================

frame_menu = tk.Frame(
    ventana,
    width=230,
    height=520,
    bd=1,
    relief="solid",
    bg="white"
)

frame_menu.place(x=25, y=80)

lbl_menu = tk.Label(
    frame_menu,
    text="Menú",
    font=("Arial", 11, "bold"),
    bg="white"
)

lbl_menu.place(x=15, y=15)

# BOTONES PRINCIPALES

btn_estudiantes = tk.Button(
    frame_menu,
    text="Estudiantes",
    bd=0,
    bg="white",
    anchor="w",
    command=lambda: mostrar_submenu("estudiantes")
)

btn_estudiantes.place(x=20, y=60)

btn_tutores = tk.Button(
    frame_menu,
    text="Tutores Académicos",
    bd=0,
    bg="white",
    anchor="w",
    command=lambda: mostrar_submenu("tutores")
)

btn_tutores.place(x=20, y=140)

btn_asesores = tk.Button(
    frame_menu,
    text="Asesores Pedagógicos",
    bd=0,
    bg="white",
    anchor="w",
    command=lambda: mostrar_submenu("asesores")
)

btn_asesores.place(x=20, y=230)

# =========================
# SUBMENÚS
# =========================

frame_estudiantes = tk.Frame(
    frame_menu,
    bg="white"
)

tk.Label(
    frame_estudiantes,
    text="└ Gestión de Evidencias",
    bg="white"
).pack(anchor="w")

frame_tutores = tk.Frame(
    frame_menu,
    bg="white"
)

tk.Label(
    frame_tutores,
    text="└ Subir Preguntas",
    bg="white"
).pack(anchor="w")

tk.Label(
    frame_tutores,
    text="└ Revisar Evidencias",
    bg="white"
).pack(anchor="w")

tk.Label(
    frame_tutores,
    text="└ Informes",
    bg="white"
).pack(anchor="w")

frame_asesores = tk.Frame(
    frame_menu,
    bg="white"
)

tk.Label(
    frame_asesores,
    text="└ Observaciones",
    bg="white"
).pack(anchor="w")

# BOTÓN SALIR

btn_salir = tk.Button(
    frame_menu,
    text="Salir",
    width=15,
    command=salir
)

btn_salir.place(x=20, y=470)

# =========================
# PANEL DERECHO
# =========================

frame_principal = tk.Frame(
    ventana,
    width=570,
    height=520,
    bd=1,
    relief="solid",
    bg="white"
)

frame_principal.place(x=280, y=80)

# RUTA ACTUAL

lbl_ruta = tk.Label(
    frame_principal,
    text="Inicio",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="blue"
)

lbl_ruta.place(x=15, y=15)

# =========================
# LISTA IZQUIERDA
# =========================

combo_lista = ttk.Combobox(
    frame_principal,
    values=[
        "Lista 1",
        "Lista 2",
        "Lista 3"
    ],
    width=15
)

combo_lista.place(x=15, y=65)

listbox = tk.Listbox(
    frame_principal,
    width=20,
    height=4
)

listbox.place(x=15, y=95)

listbox.insert(tk.END, "xxxx")
listbox.insert(tk.END, "yyyy")

# =========================
# FORMULARIO
# =========================

tk.Label(
    frame_principal,
    text="Tipo",
    bg="white",
    font=("Arial", 9, "bold")
).place(x=230, y=65)

combo_tipo = ttk.Combobox(
    frame_principal,
    values=[
        "PDF",
        "Word",
        "Excel"
    ],
    width=20
)

combo_tipo.place(x=335, y=65)

tk.Label(
    frame_principal,
    text="Nombre Evidencia",
    bg="white",
    font=("Arial", 9, "bold")
).place(x=230, y=100)

entry_nombre = tk.Entry(
    frame_principal,
    width=25
)

entry_nombre.place(x=335, y=100)

tk.Label(
    frame_principal,
    text="Fecha",
    bg="white",
    font=("Arial", 9, "bold")
).place(x=230, y=135)

entry_fecha = tk.Entry(
    frame_principal,
    width=25
)

entry_fecha.place(x=335, y=135)

tk.Label(
    frame_principal,
    text="Descripción",
    bg="white",
    font=("Arial", 9, "bold")
).place(x=230, y=170)

txt_descripcion = tk.Text(
    frame_principal,
    width=22,
    height=3
)

txt_descripcion.place(x=335, y=170)

btn_cargar = tk.Button(
    frame_principal,
    text="Cargar evidencia",
    command=cargar_archivo
)

btn_cargar.place(x=230, y=200)

lbl_archivo = tk.Label(
    frame_principal,
    text="Sin archivo",
    bg="white",
    fg="blue"
)

lbl_archivo.place(x=360, y=203)

# =========================
# TABLA
# =========================

columnas = (
    "id",
    "nombre",
    "tipo",
    "fecha",
    "descripcion",
    "archivo"
)

tabla = ttk.Treeview(
    frame_principal,
    columns=columnas,
    show="headings",
    height=8
)

tabla.heading("id", text="Id Evidencia")
tabla.heading("nombre", text="Nom. Evidencia")
tabla.heading("tipo", text="Tipo")
tabla.heading("fecha", text="Fecha")
tabla.heading("descripcion", text="Descripción")
tabla.heading("archivo", text="Archivo")

tabla.column("id", width=70)
tabla.column("nombre", width=120)
tabla.column("tipo", width=80)
tabla.column("fecha", width=90)
tabla.column("descripcion", width=120)
tabla.column("archivo", width=140)

tabla.place(x=15, y=250)

tabla.bind(
    "<<TreeviewSelect>>",
    cargar_datos
)

# =========================
# BOTONES INFERIORES
# =========================

btn_cancelar = tk.Button(
    frame_principal,
    text="Cancelar",
    width=10,
    command=nueva_evidencia
)

btn_cancelar.place(x=15, y=460)

btn_nuevo = tk.Button(
    frame_principal,
    text="Nueva Evidencia",
    width=15,
    command=nueva_evidencia
)

btn_nuevo.place(x=105, y=460)

btn_modificar = tk.Button(
    frame_principal,
    text="Modificar",
    width=10,
    command=modificar
)

btn_modificar.place(x=245, y=460)

btn_eliminar = tk.Button(
    frame_principal,
    text="Eliminar",
    width=10,
    command=eliminar
)

btn_eliminar.place(x=335, y=460)

btn_aceptar = tk.Button(
    frame_principal,
    text="Aceptar",
    width=10,
    command=aceptar
)

btn_aceptar.place(x=450, y=460)

# =========================
# FECHA AUTOMÁTICA
# =========================

entry_fecha.insert(
    0,
    datetime.now().strftime("%d/%m/%Y")
)

entry_fecha.config(state="readonly")

bloquear_campos(False)

ventana.mainloop()