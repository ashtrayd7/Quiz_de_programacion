import tkinter as tk
from tkinter import messagebox
import random

todas_las_preguntas = []
preguntas_seleccionadas = []

indice_actual = 0
puntaje = 0
nombre_jugador = ""

def cargar_banco_preguntas():
    global todas_las_preguntas, preguntas_seleccionadas
    
    try:
        with open("preguntas.csv", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")
                if len(partes) == 2:
                    todas_las_preguntas.append((partes[0], partes[1]))
                    
    
        if len(todas_las_preguntas) < 5:
            messagebox.showerror("Error de Datos", "El archivo debe contener al menos 5 preguntas.")
            exit()
        preguntas_seleccionadas = random.sample(todas_las_preguntas, 5)
        
    except FileNotFoundError:
        messagebox.showerror("Error Crítico", "No se encontró el archivo 'preguntas.csv'.")
        exit()

def ir_a_pantalla_juego():
    global nombre_jugador
    nombre = entrada_nombre.get().strip()
    
    if nombre == "":
        messagebox.showwarning("Atención", "Por favor, introduce tu nombre.")
        return
        
    nombre_jugador = nombre
    frame_inicio.pack_forget()
    frame_juego.pack(pady=20)
    
    mostrar_pregunta_actual()

def mostrar_pregunta_actual():
    global indice_actual

    frase, correcta = preguntas_seleccionadas[indice_actual]
    lbl_frase.config(text=frase, font=("Times New Roman", 14), fg="#0a0a0a")
    lbl_puntaje.config(text=f"Jugador: {nombre_jugador}  |  Puntaje: {puntaje}")

    entrada_respuesta.delete(0, tk.END)
    listbox_opciones.selection_clear(0, tk.END)

    opciones_listbox = [correcta, "Madrid", "Lope de Vega", "Cervantes", "Góngora"]
    opciones_listbox = list(set(opciones_listbox))
    random.shuffle(opciones_listbox)
    
    listbox_opciones.delete(0, tk.END)
    for opcion in opciones_listbox:
        listbox_opciones.insert(tk.END, opcion)

def validar_respuesta():
    global indice_actual, puntaje
    
    frase, correcta = preguntas_seleccionadas[indice_actual]
    
    texto_entry = entrada_respuesta.get().strip()

    seleccion_listbox = listbox_opciones.curselection()
    texto_listbox = listbox_opciones.get(seleccion_listbox[0]) if seleccion_listbox else ""

    usó_entry = False
    respuesta_usuario = ""
    
    if texto_entry != "":
        respuesta_usuario = texto_entry
        usó_entry = True
    elif texto_listbox != "":
        respuesta_usuario = texto_listbox
    else:
        messagebox.showwarning("Atención", "Escribe una respuesta o selecciona una del Listbox.")
        return
    
    if respuesta_usuario.strip().lower() == correcta.strip().lower():
        # REQUISITO: 10 pts si es por Entry, 5 pts si es por Listbox
        if usó_entry:
            puntaje += 10
            messagebox.showinfo("¡Correcto!", "¡Excelente! Escribiste la respuesta correcta (+10 puntos).")
        else:
            puntaje += 5
            messagebox.showinfo("¡Correcto!", "¡Bien! Seleccionaste la respuesta de la lista (+5 puntos).")
    else:
        messagebox.showerror("Incorrecto", f"Respuesta incorrecta. La opción correcta era: {correcta}")

    indice_actual += 1
    if indice_actual < 5:
        mostrar_pregunta_actual()
    else:
        mostrar_pantalla_resultados()

def mostrar_pantalla_resultados():
    frame_juego.pack_forget()
    frame_resultados.pack(pady=20)
    
    lbl_final.config(text=f"¡Juego Terminado, {nombre_jugador}!\nTu puntaje final es: {puntaje} puntos.")
    messagebox.showinfo("Resultados", f"Fin del juego.\nPuntaje Total: {puntaje} pts.")

def salir_juego():
    ventana.destroy()
cargar_banco_preguntas()

ventana = tk.Tk()
ventana.title("Quiz de Literatura Española")
ventana.geometry("500x400")
frame_inicio = tk.Frame(ventana)
frame_inicio.pack(pady=40)

lbl_bienvenida = tk.Label(frame_inicio, text="Bienvenido al Quiz de Literatura", font=("Arial", 14, "bold"))
lbl_bienvenida.pack(pady=10)

lbl_nom = tk.Label(frame_inicio, text="Introduce tu nombre:")
lbl_nom.pack(pady=5)

entrada_nombre = tk.Entry(frame_inicio, font=("Arial", 11), justify="center")
entrada_nombre.pack(pady=5)

btn_iniciar = tk.Button(frame_inicio, text="Comenzar Juego", command=ir_a_pantalla_juego, bg="#4CAF50", fg="white")
btn_iniciar.pack(pady=15)

frame_juego = tk.Frame(ventana)

lbl_puntaje = tk.Label(frame_juego, text="", font=("Arial", 10, "italic"))
lbl_puntaje.grid(row=0, column=0, columnspan=2, pady=5)

lbl_frase = tk.Label(frame_juego, text="") # Se configura dinámicamente en Times New Roman
lbl_frase.grid(row=1, column=0, columnspan=2, pady=15)

lbl_opcion1 = tk.Label(frame_juego, text="Opción A: Escribe la palabra:")
lbl_opcion1.grid(row=2, column=0, sticky="w", padx=10)

entrada_respuesta = tk.Entry(frame_juego, font=("Arial", 11))
entrada_respuesta.grid(row=2, column=1, pady=5, padx=10)

lbl_opcion2 = tk.Label(frame_juego, text="Opción B: Selecciona de la lista:")
lbl_opcion2.grid(row=3, column=0, sticky="nw", padx=10, pady=5)

listbox_opciones = tk.Listbox(frame_juego, height=5, font=("Arial", 10))
listbox_opciones.grid(row=3, column=1, pady=5, padx=10, sticky="w")

btn_validar = tk.Button(frame_juego, text="Validar Respuesta", command=validar_respuesta, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
btn_validar.grid(row=4, column=0, columnspan=2, pady=20)

frame_resultados = tk.Frame(ventana)

lbl_res_titulo = tk.Label(frame_resultados, text="Puntaje y Respuestas", font=("Arial", 14, "bold"))
lbl_res_titulo.pack(pady=10)

lbl_final = tk.Label(frame_resultados, text="", font=("Arial", 12))
lbl_final.pack(pady=15)

btn_salir = tk.Button(frame_resultados, text="Cerrar Quiz", command=salir_juego, bg="#f44336", fg="white")
btn_salir.pack(pady=10)


ventana.mainloop()