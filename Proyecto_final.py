import tkinter as tk
from tkinter import messagebox
import random

def generar_tablero():
    # Obtiene los valores ingresados por el usuario
    n = int(entry.get())
    if n < 3:
        messagebox.showerror("Error", "El tamaño del tablero debe ser mayor o igual a 3")
        return
    jugador1 = entry_jugador1.get()
    jugador2 = entry_jugador2.get()
    participaciones = int(entry_participaciones.get())

    # Cierra la ventana actual
    ventana.destroy()

    tablero = [[random.randint(0, 11) for _ in range(n)] for _ in range(n)]
    puntajes = {1: 0, 2: 0}
    turno = 1
    participacion_actual = 0.5

    def mostrar_respuestas(opciones):
        # Elimina los botones de respuesta existentes
        for widget in frame_botones.grid_slaves():
            widget.destroy()

        # Crea los botones de respuesta
        for i, opcion in enumerate(opciones):
            boton_respuesta = tk.Button(frame_botones, text=str(opcion), width=5, height=2,
                                        command=lambda opcion=opcion: verificar_respuesta(opcion, opciones))
            boton_respuesta.grid(row=i, column=0)

    def verificar_respuesta(respuesta, opciones):
        nonlocal turno, participacion_actual  # Permite acceder a las variables del ámbito exterior
        # Verifica la respuesta seleccionada por el jugador
        if respuesta == opciones[3]:
            puntajes[turno] += 3
            label_puntaje.config(text=f"{jugador1}: {puntajes[1]} puntos    {jugador2}: {puntajes[2]} puntos")
        
        # Cambia de turno
        turno = 2 if turno == 1 else 1
        label_turno.config(text=f"Turno: {turno}")

        # Vuelve a ocultar los números y las respuestas
        for i in range(n):
            for j in range(n):
                botones[i][j].config(text="")
        for widget in frame_botones.grid_slaves():
            widget.destroy()

        # Reinicia el cronómetro
        reiniciar_cronometro()

        # Verifica si se han completado todas las participaciones
        if participacion_actual == participaciones:
            mostrar_ganador()
        else:
            participacion_actual += 0.5

    def revelar_numero(i, j):
        # Verifica si el número ya está revelado
        if botones[i][j].cget('text') != "":
            return
        
        # Inicia el cronómetro si no está en marcha
        if not cronometro_activo.get():
            iniciar_cronometro()

        # Actualiza el texto del botón con el número correspondiente
        botones[i][j].config(text=str(tablero[i][j]))
        botones[i][j].config(state=tk.DISABLED)  # Desactiva el botón

        # Revela los números vecinos
        for x in range(max(0, i-1), min(n, i+2)):
            for y in range(max(0, j-1), min(n, j+2)):
                botones[x][y].config(text=str(tablero[x][y]))

        # Calcula la sumatoria y genera las opciones de respuesta
        vecinos = [tablero[x][y] for x in range(max(0, i-1), min(n, i+2)) for y in range(max(0, j-1), min(n, j+2)) if (x, y) != (i, j)]
        sumatoria = sum(vecinos)
        multiplicacion = sumatoria * tablero[i][j]
        opciones = [random.randint(0, 1000) for _ in range(3)] + [multiplicacion]

        # Selecciona aleatoriamente la posición del botón con la respuesta correcta
        posicion_respuesta_correcta = random.choice(range(4))

        # Elimina los botones de respuesta existentes
        for widget in frame_botones.grid_slaves():
            widget.destroy()

        # Crea los botones de respuesta
        for i, opcion in enumerate(opciones):
            if i == posicion_respuesta_correcta:
                # Crea el botón con la respuesta correcta
                boton_respuesta = tk.Button(frame_botones, text=str(opcion), width=5, height=2,
                                            command=lambda opcion=opcion: verificar_respuesta(opcion, opciones))
            else:
                # Crea los botones con las otras opciones
                boton_respuesta = tk.Button(frame_botones, text=str(opcion), width=5, height=2,
                                            command=lambda opcion=opcion: verificar_respuesta(opcion, opciones))
            boton_respuesta.grid(row=i, column=0)


    # Crea una nueva ventana para el juego
    ventana_juego = tk.Tk()
    ventana_juego.title("Juego de Matríz Arirmetica")
    botones = []
    for i in range(n):
        fila = []
        for j in range(n):
            # Crea un botón con una función de clic asociada
            boton = tk.Button(ventana_juego, text="", width=5, height=2,
                              command=lambda i=i, j=j: revelar_numero(i, j))
            boton.grid(row=i, column=j)
            fila.append(boton)
        botones.append(fila)

    frame_botones = tk.Frame(ventana_juego)
    frame_botones.grid(row=n, column=0, columnspan=n)

    label_turno = tk.Label(ventana_juego, text=f"Turno: {turno}")
    label_turno.grid(row=n+1, column=0, columnspan=n)

    label_puntaje = tk.Label(ventana_juego, text=f"{jugador1}: {puntajes[1]} puntos    {jugador2}: {puntajes[2]} puntos")
    label_puntaje.grid(row=n+2, column=0, columnspan=n)

    cronometro = tk.IntVar()
    cronometro_activo = tk.BooleanVar()
    cronometro.set(25)
    cronometro_activo.set(False)
    label_cronometro = tk.Label(ventana_juego, text="Tiempo restante: 25 segundos")
    label_cronometro.grid(row=n+3, column=0, columnspan=n)

    def iniciar_cronometro():
        cronometro_activo.set(True)
        actualizar_cronometro()

    def actualizar_cronometro():
        if cronometro_activo.get():
            tiempo_restante = cronometro.get()
            tiempo_restante -= 1
            cronometro.set(tiempo_restante)
            label_cronometro.config(text=f"Tiempo restante: {tiempo_restante} segundos")

            if tiempo_restante == 0:
                nonlocal turno
                turno = 2 if turno == 1 else 1
                label_turno.config(text=f"Turno: {turno}")
                reiniciar_cronometro()

                # Vuelve a ocultar los números y las respuestas
                for i in range(n):
                    for j in range(n):
                        botones[i][j].config(text="")
                for widget in frame_botones.grid_slaves():
                    widget.destroy()

                # Verifica si se han completado todas las participaciones
                if participacion_actual == participaciones:
                    mostrar_ganador()
                else:
                    participacion_actual += 1

            ventana_juego.after(1000, actualizar_cronometro)

    def reiniciar_cronometro():
        cronometro.set(25)
        cronometro_activo.set(False)
        label_cronometro.config(text="Tiempo restante: 25 segundos")

    def mostrar_ganador():
        ganador = jugador1 if puntajes[1] > puntajes[2] else jugador2 if puntajes[2] > puntajes[1] else "... Wow, el resultado es un empate, felicidades a ambos jugadores"
        messagebox.showinfo("Juego Terminado", f"El ganador es {ganador}!")

    ventana_juego.mainloop()


# Crea la ventana principal
ventana = tk.Tk()
ventana.title("Menu de inicio")
ventana.geometry("500x500")

# Etiqueta y campo de entrada para el tamaño del tablero
label = tk.Label(ventana, text="Tamaño del tablero:")
label.pack()
entry = tk.Entry(ventana)
entry.pack()

# Etiqueta y campo de entrada para el nombre de los jugadores
label_jugador1 = tk.Label(ventana, text="Nombre del jugador 1:")
label_jugador1.pack()
entry_jugador1 = tk.Entry(ventana)
entry_jugador1.pack()

label_jugador2 = tk.Label(ventana, text="Nombre del jugador 2:")
label_jugador2.pack()
entry_jugador2 = tk.Entry(ventana)
entry_jugador2.pack()

# Etiqueta y campo de entrada para la cantidad de participaciones
label_participaciones = tk.Label(ventana, text="Cantidad de participaciones:")
label_participaciones.pack()
entry_participaciones = tk.Entry(ventana)
entry_participaciones.pack()

# Botón para generar el tablero
boton_generar = tk.Button(ventana, text="Generar Tablero", command=generar_tablero)
boton_generar.pack()

# Ejecuta el bucle de eventos de la ventana principal
ventana.mainloop()