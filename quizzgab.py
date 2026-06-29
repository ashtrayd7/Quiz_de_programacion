import tkinter as tk
from tkinter import messagebox
import random

class MiQuizLiteratura:
    def __init__(self, ventana_principal):
        self.ventana = ventana_principal
        self.ventana.title("Quiz de Literatura Española")
        self.ventana.geometry("500x420")
        
        self.lista_todas_preguntas = []
        self.preguntas_de_la_ronda = []
        self.indice_pregunta_actual = 0
        self.puntaje_jugador = 0
        self.vidas_restantes = 3
        self.nombre_usuario = ""
        
        try:
            with open("preguntas.csv", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    partes_linea = linea.strip().split(",")
                    if len(partes_linea) == 2: 
                        self.lista_todas_preguntas.append((partes_linea[0], partes_linea[1]))
            if len(self.lista_todas_preguntas) < 5:
                messagebox.showerror("Error de Datos", "El archivo debe contener al menos 5 preguntas.")
                self.ventana.destroy()
                exit()
            self.preguntas_de_la_ronda = random.sample(self.lista_todas_preguntas, 5)
        except FileNotFoundError:
            messagebox.showerror("Error Crítico", "No se encontró el archivo 'preguntas.csv'.")
            self.ventana.destroy()
            exit()
            
        self.pantalla_inicio = tk.Frame(self.ventana)
        self.pantalla_juego = tk.Frame(self.ventana)
        self.pantalla_resultados = tk.Frame(self.ventana)
        
        titulo_bienvenida = tk.Label(self.pantalla_inicio, text="Bienvenido al Quiz de Literatura", font=("Arial", 14, "bold"))
        titulo_bienvenida.pack(pady=10)
        subtitulo_nombre = tk.Label(self.pantalla_inicio, text="Introduce tu nombre:")
        subtitulo_nombre.pack(pady=5)
        self.caja_texto_nombre = tk.Entry(self.pantalla_inicio, font=("Arial", 11), justify="center")
        self.caja_texto_nombre.pack(pady=5)
        boton_comenzar = tk.Button(self.pantalla_inicio, text="Comenzar Juego", command=self.iniciar_juego, bg="#4CAF50", fg="white")
        boton_comenzar.pack(pady=15)
        
        self.etiqueta_estado = tk.Label(self.pantalla_juego, text="", font=("Arial", 10, "italic"))
        self.etiqueta_estado.grid(row=0, column=0, columnspan=2, pady=5)
        self.etiqueta_frase_pregunta = tk.Label(self.pantalla_juego, text="") 
        self.etiqueta_frase_pregunta.grid(row=1, column=0, columnspan=2, pady=15)
        lbl_instruccion_escribir = tk.Label(self.pantalla_juego, text="Opción A: Escribe la palabra:")
        lbl_instruccion_escribir.grid(row=2, column=0, sticky="w", padx=10)
        self.caja_texto_respuesta = tk.Entry(self.pantalla_juego, font=("Arial", 11))
        self.caja_texto_respuesta.grid(row=2, column=1, pady=5, padx=10)
        lbl_instruccion_lista = tk.Label(self.pantalla_juego, text="Opción B: Selecciona de la lista:")
        lbl_instruccion_lista.grid(row=3, column=0, sticky="nw", padx=10, pady=5)
        self.lista_opciones_ui = tk.Listbox(self.pantalla_juego, height=5, font=("Arial", 10))
        self.lista_opciones_ui.grid(row=3, column=1, pady=5, padx=10, sticky="w")
        boton_validar = tk.Button(self.pantalla_juego, text="Validar Respuesta", command=self.comprobar_respuesta, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        boton_validar.grid(row=4, column=0, columnspan=2, pady=20)
        
        titulo_resultados = tk.Label(self.pantalla_resultados, text="Puntaje y Respuestas", font=("Arial", 14, "bold"))
        titulo_resultados.pack(pady=10)
        self.etiqueta_resumen_final = tk.Label(self.pantalla_resultados, text="", font=("Arial", 12))
        self.etiqueta_resumen_final.pack(pady=15)
        boton_salir = tk.Button(self.pantalla_resultados, text="Cerrar Quiz", command=self.ventana.destroy, bg="#f44336", fg="white")
        boton_salir.pack(pady=10)
        
        self.pantalla_inicio.pack(pady=40)

    def iniciar_juego(self):
        self.nombre_usuario = self.caja_texto_nombre.get().strip()
        if self.nombre_usuario == "":
            messagebox.showwarning("Atención", "Por favor, introduce tu nombre.")
            return
        self.pantalla_inicio.pack_forget()
        self.pantalla_juego.pack(pady=20)
        self.cargar_siguiente_pregunta()

    def cargar_siguiente_pregunta(self):
        frase_incompleta, respuesta_correcta = self.preguntas_de_la_ronda[self.indice_pregunta_actual]
        self.etiqueta_frase_pregunta.config(text=frase_incompleta, font=("Times New Roman", 14), fg="#0a0a0a")
        self.etiqueta_estado.config(text=f"Jugador: {self.nombre_usuario}  |  Puntaje: {self.puntaje_jugador}  |  Vidas: {self.vidas_restantes}")
        self.caja_texto_respuesta.delete(0, tk.END)
        self.lista_opciones_ui.selection_clear(0, tk.END)
        
        opciones_mezcladas = [respuesta_correcta, "Madrid", "Lope de Vega", "Cervantes", "Góngora"]
        opciones_mezcladas = list(set(opciones_mezcladas)) 
        random.shuffle(opciones_mezcladas)
        
        self.lista_opciones_ui.delete(0, tk.END)
        for opcion in opciones_mezcladas: 
            self.lista_opciones_ui.insert(tk.END, opcion)

    def comprobar_respuesta(self):
        frase_incompleta, respuesta_correcta = self.preguntas_de_la_ronda[self.indice_pregunta_actual]
        texto_de_la_caja = self.caja_texto_respuesta.get().strip()
        seleccion_lista = self.lista_opciones_ui.curselection()
        texto_de_la_lista = self.lista_opciones_ui.get(seleccion_lista[0]) if seleccion_lista else ""
        
        usuario_escribio = False
        respuesta_final_usuario = ""
        
        if texto_de_la_caja != "":
            respuesta_final_usuario = texto_de_la_caja
            usuario_escribio = True
        elif texto_de_la_lista != "":
            respuesta_final_usuario = texto_de_la_lista
        else:
            messagebox.showwarning("Atención", "Escribe una respuesta o selecciona una de la lista.")
            return
            
        if respuesta_final_usuario.strip().lower() == respuesta_correcta.strip().lower():
            if usuario_escribio:
                self.puntaje_jugador += 10
                messagebox.showinfo("¡Correcto!", "¡Excelente! Escribiste la respuesta correcta (+10 puntos).")
            else:
                self.puntaje_jugador += 5
                messagebox.showinfo("¡Correcto!", "¡Bien! Seleccionaste la respuesta de la lista (+5 puntos).")
            self.indice_pregunta_actual += 1
        else:
            self.vidas_restantes -= 1
            messagebox.showerror("Incorrecto", f"Respuesta incorrecta. La opción correcta era: {respuesta_correcta}")
            if self.vidas_restantes <= 0:
                self.finalizar_juego()
                return
            self.indice_pregunta_actual += 1
            
        if self.indice_pregunta_actual < 5: 
            self.cargar_siguiente_pregunta()
        else: 
            self.finalizar_juego()

    def finalizar_juego(self):
        self.pantalla_juego.pack_forget()
        self.pantalla_resultados.pack(pady=20)
        motivo_fin = "Te quedaste sin vidas." if self.vidas_restantes <= 0 else "Completaste las preguntas disponibles."
        self.etiqueta_resumen_final.config(text=f"¡Juego Terminado!\nMotivo: {motivo_fin}\nJugador: {self.nombre_usuario}\nPuntaje final: {self.puntaje_jugador} puntos.")
        messagebox.showinfo("Resultados", f"Fin del juego.\nPuntaje Total: {self.puntaje_jugador} pts.")

if __name__ == "__main__":
    raiz = tk.Tk()
    aplicacion = MiQuizLiteratura(raiz)
    raiz.mainloop()