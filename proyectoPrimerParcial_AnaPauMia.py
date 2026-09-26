
import tkinter as tk
from tkinter import ttk
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#FUNCIONES

def f(t, y):
    ecuacion = ent_ecuacion.get()
    return eval(ecuacion, {"t": t, "y": y, "math": math})


def resolver(event=None):

    ejercicio = opcion.get()

    t0 = float(ent_t0.get())
    tf = float(ent_tf.get())
    h = float(ent_h.get())

    tiempos = []
    euler = []
    rk4 = []

    if ejercicio == "Dinámica poblacional":

        y0 = float(ent_y0.get())

        t = t0
        ye = y0
        yr = y0

        while t <= tf + 0.0001:

            tiempos.append(t)
            euler.append(ye)
            rk4.append(yr)

            ye_nuevo = ye + h*f(t, ye)

            k1 = f(t, yr)
            k2 = f(t+h/2, yr+h*k1/2)
            k3 = f(t+h/2, yr+h*k2/2)
            k4 = f(t+h, yr+h*k3)

            yr = yr + h*(k1+2*k2+2*k3+k4)/6
            ye = ye_nuevo
            t = t+h

    else:

        q = float(ent_y0.get())
        i = float(ent_i0.get())

        qr = q
        ir = i
        t = t0

        L = 1
        R = 5
        C = 0.2
        V = 10

        while t <= tf + 0.0001:

            tiempos.append(t)
            euler.append(q)
            rk4.append(qr)

            q_nuevo = q + h*i
            i_nuevo = i + h*((V-R*i-q/C)/L)

            def sistema(q, i):
                return i, (V-R*i-q/C)/L

            k1q, k1i = sistema(qr, ir)
            k2q, k2i = sistema(
                qr+h*k1q/2,
                ir+h*k1i/2
            )
            k3q, k3i = sistema(
                qr+h*k2q/2,
                ir+h*k2i/2
            )
            k4q, k4i = sistema(
                qr+h*k3q,
                ir+h*k3i
            )

            qr = qr + h*(k1q+2*k2q+2*k3q+k4q)/6
            ir = ir + h*(k1i+2*k2i+2*k3i+k4i)/6

            q = q_nuevo
            i = i_nuevo
            t = t+h

    for fila in tabla.get_children():
        tabla.delete(fila)

    for n in range(len(tiempos)):
        tabla.insert(
            "",
            "end",
            values=(
                n,
                round(tiempos[n], 3),
                round(euler[n], 6),
                round(rk4[n], 6)
            )
        )

    grafica.clear()

    grafica.plot(
        tiempos,
        euler,
        "o-",
        label="Euler"
    )

    grafica.plot(
        tiempos,
        rk4,
        "s-",
        label="RK4"
    )

    grafica.set_title("Comparación de los métodos")
    grafica.set_xlabel("Tiempo")

    if ejercicio == "Circuito RLC":
        grafica.set_ylabel("Carga q(t)")
    else:
        grafica.set_ylabel("y(t)")

    grafica.grid()
    grafica.legend()

    canvas.draw()


#CAMBIO DE EJERCICIO

def cambiar(event=None):

    if opcion.get() == "Dinámica poblacional":

        ent_ecuacion.delete(0, tk.END)
        ent_ecuacion.insert(
            0,
            "y*math.cos(t)-0.2*y**2"
        )

        ent_y0.delete(0, tk.END)
        ent_y0.insert(0, "2")

        ent_t0.delete(0, tk.END)
        ent_t0.insert(0, "0")

        ent_tf.delete(0, tk.END)
        ent_tf.insert(0, "10")

        ent_h.delete(0, tk.END)
        ent_h.insert(0, "0.5")

        lbl_y0.config(text="Condición inicial y(0):")

        lbl_i0.grid_remove()
        ent_i0.grid_remove()

    else:

        ent_ecuacion.delete(0, tk.END)
        ent_ecuacion.insert(
            0,
            "Lq'' + Rq' + (1/C)q = V(t)"
        )

        ent_y0.delete(0, tk.END)
        ent_y0.insert(0, "0")

        ent_i0.delete(0, tk.END)
        ent_i0.insert(0, "0")

        ent_t0.delete(0, tk.END)
        ent_t0.insert(0, "0")

        ent_tf.delete(0, tk.END)
        ent_tf.insert(0, "2")

        ent_h.delete(0, tk.END)
        ent_h.insert(0, "0.1")

        lbl_y0.config(text="Carga inicial q(0):")

        lbl_i0.grid()
        ent_i0.grid()


# INTERFZ

ventana = tk.Tk()

ventana.title("Proyecto - Métodos Numéricos RK4, EULER")
ventana.geometry("900x720")


tk.Label(
    ventana,
    text="Resolución Numérica de Ecuaciones Diferenciales",
    font=("Arial", 18, "bold")
).pack(pady=10)


tk.Label(
    ventana,
    text="Método de Euler y Runge-Kutta de 4to Orden",
    font=("Arial", 11)
).pack()


datos = tk.Frame(ventana)
datos.pack(pady=15)


tk.Label(
    datos,
    text="Ejercicio:"
).grid(row=0, column=0, padx=10, pady=4)


opcion = ttk.Combobox(
    datos,
    values=[
        "Dinámica poblacional",
        "Circuito RLC"
    ],
    state="readonly",
    width=25
)

opcion.grid(row=0, column=1)
opcion.current(0)
opcion.bind("<<ComboboxSelected>>", cambiar)


tk.Label(
    datos,
    text="Ecuación:"
).grid(row=1, column=0, padx=10, pady=4)


ent_ecuacion = tk.Entry(
    datos,
    width=35
)

ent_ecuacion.grid(row=1, column=1)


lbl_y0 = tk.Label(
    datos,
    text="Condición inicial y(0):"
)

lbl_y0.grid(row=2, column=0, pady=4)


ent_y0 = tk.Entry(datos)
ent_y0.grid(row=2, column=1)


lbl_i0 = tk.Label(
    datos,
    text="Corriente inicial i(0):"
)

lbl_i0.grid(row=3, column=0, pady=4)


ent_i0 = tk.Entry(datos)
ent_i0.grid(row=3, column=1)


tk.Label(
    datos,
    text="Tiempo inicial:"
).grid(row=4, column=0, pady=4)

ent_t0 = tk.Entry(datos)
ent_t0.grid(row=4, column=1)


tk.Label(
    datos,
    text="Tiempo final:"
).grid(row=5, column=0, pady=4)

ent_tf = tk.Entry(datos)
ent_tf.grid(row=5, column=1)


tk.Label(
    datos,
    text="Tamaño de paso h:"
).grid(row=6, column=0, pady=4)

ent_h = tk.Entry(datos)
ent_h.grid(row=6, column=1)

ent_h.bind("<Return>", resolver)


tk.Label(
    ventana,
    text="Ingresa los datos y presiona Enter en el tamaño de paso",
    font=("Arial", 9)
).pack()


#TABLA

tabla = ttk.Treeview(
    ventana,
    columns=("n", "t", "Euler", "RK4"),
    show="headings",
    height=7
)

tabla.heading("n", text="n")
tabla.heading("t", text="Tiempo")
tabla.heading("Euler", text="Euler")
tabla.heading("RK4", text="RK4")

tabla.column("n", width=60, anchor="center")
tabla.column("t", width=100, anchor="center")
tabla.column("Euler", width=150, anchor="center")
tabla.column("RK4", width=150, anchor="center")

tabla.pack(pady=10)


#GRAFICA

figura = Figure(figsize=(6, 3))
grafica = figura.add_subplot(111)

canvas = FigureCanvasTkAgg(
    figura,
    master=ventana
)

canvas.get_tk_widget().pack()


#inicio

cambiar()

ventana.mainloop()