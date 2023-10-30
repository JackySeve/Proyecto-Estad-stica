import tkinter as tk
from tkinter import Toplevel, messagebox
from tkinter.ttk import Combobox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import json
import statistics
import numpy as np
import matplotlib.pyplot as plt

# Crear un diccionario para almacenar las gráficas por fecha
graficas_por_fecha = {}

# Crear una lista para rastrear los movimientos (ingresos y retiros)
movimientos = []

# Función para generar y almacenar una gráfica para la fecha actual
def generar_y_almacenar_grafica():
    fecha_actual = datetime.date.today().isoformat()  # Obtiene la fecha actual (en formato YYYY-MM-DD)
    
    # Verifica si la fecha ya tiene una gráfica asociada
    if fecha_actual not in graficas_por_fecha:
        # Genera una nueva gráfica
        fig = Figure(figsize=(6, 4), dpi=100)
        plot = fig.add_subplot(111)
        # Personaliza la gráfica según tus necesidades
        # ...
        
        # Almacena la gráfica en el diccionario
        graficas_por_fecha[fecha_actual] = fig

# Función para mostrar una gráfica seleccionada
def mostrar_grafica_seleccionada():
    fecha_seleccionada = combobox_fecha.get()
    if not fecha_seleccionada:
        messagebox.showwarning("Advertencia", "No has seleccionado un día para revisar su gráfica.")
    else:
        if fecha_seleccionada in graficas_por_fecha:
            # Obtén la gráfica correspondiente
            figura = graficas_por_fecha[fecha_seleccionada]
            ventana_grafica = Toplevel(ventana)
            ventana_grafica.title(f"Gráfica del {fecha_seleccionada}")
            canvas = FigureCanvasTkAgg(figura, master=ventana_grafica)
            canvas.get_tk_widget().pack()

# Función para registrar movimientos (ingresos y retiros)
def registrar_movimiento(descripcion, ventana_movimientos_text):
    fecha_actual = datetime.date.today().isoformat()
    hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
    movimiento = {
        "fecha": fecha_actual,
        "hora": hora_actual,
        "descripcion": descripcion,
    }
    movimientos.append(movimiento)
    
    # Actualiza el registro de movimientos en la ventana de movimientos
    ventana_movimientos_text.insert(tk.END, f"{fecha_actual} {hora_actual}: {descripcion}\n")
    
    # Guarda los movimientos después de agregar uno nuevo
    guardar_movimientos()

def guardar_movimientos():
    with open('movimientos.json', 'w') as archivo:
        json.dump(movimientos, archivo)

# Función para disminuir el valor y registrar el movimiento
def disminuir_valor(valor, label, total_label, ventana_movimientos_text):
    valor_actual = valor.get()
    if valor_actual > 0:
        valor.set(valor_actual - 1)
        label.config(text=str(valor.get()))
        actualizar_total(total_label)
        registrar_movimiento(f"Retiro de {label.cget('text')}", ventana_movimientos_text)

# Función para mostrar los movimientos en una nueva ventana
def mostrar_movimientos():
    ventana_movimientos = Toplevel(ventana)
    ventana_movimientos.title("Registro de Movimientos")
    text = tk.Text(ventana_movimientos, height=15, width=40)
    text.pack()

    # Cargar los movimientos desde el archivo JSON
    movimientos_cargados = cargar_movimientos()
    
    # Agregar los movimientos al Text
    for movimiento in movimientos_cargados:
        fecha = movimiento['fecha']
        hora = movimiento['hora']
        descripcion = movimiento['descripcion']
        text.insert(tk.END, f"{fecha} {hora}: {descripcion}\n")

def cargar_movimientos():
    try:
        with open('movimientos.json', 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

# Llama a cargar_movimientos al inicio para cargar los movimientos anteriores
movimientos = cargar_movimientos()

# Función para actualizar el total y mostrar la gráfica
def incrementar_valor(valor, label, total_label, ventana_movimientos_text):
    valor_actual = valor.get()
    valor.set(valor_actual + 1)
    label.config(text=str(valor.get()))
    actualizar_total(total_label)
    registrar_movimiento(f"Ingreso de {label.cget('text')} monedas", ventana_movimientos_text)

# Función para actualizar el total
def actualizar_total(total_label):
    total = (valor_50.get() * 50) + (valor_100.get() * 100) + (valor_200.get() * 200) + (valor_500.get() * 500) + (valor_1000.get() * 1000)
    total_label.config(text="Total: $" + str(total))

# Función para guardar el diccionario en un archivo JSON
def guardar_diccionario(diccionario):
    with open('monedas.json', 'w') as archivo:
        json.dump(diccionario, archivo)

# Función para cargar el diccionario desde un archivo JSON
def cargar_diccionario():
    try:
        with open('monedas.json', 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}

# Crear una lista con las denominaciones y sus valores en pesos
denominaciones_valores = {
    50: 50,
    100: 100,
    200: 200,
    500: 500,
    1000: 1000
}

# Función para mostrar estadísticas descriptivas
def mostrar_estadisticas(avanzadas=False):
    valores = [valor_50.get(), valor_100.get(), valor_200.get(), valor_500.get(), valor_1000.get()]
    
    if all(valor == 0 for valor in valores):
        messagebox.showinfo("No hay datos", "No has ingresado monedas aún, así que no hay datos para mostrar estadísticas.")
    else:
        # Convierte las cantidades de monedas a valores monetarios
        valores_monetarios = [cantidades * denominaciones_valores[d] for cantidades, d in zip(valores, denominaciones_valores)]

        media = statistics.mean(valores_monetarios)
        mediana = statistics.median(valores_monetarios)
        desviacion_estandar = statistics.stdev(valores_monetarios)
        moda = statistics.mode(valores_monetarios)
        suma = sum(valores_monetarios)
        varianza = statistics.variance(valores_monetarios)
        cuartiles = np.percentile(valores_monetarios, [25, 50, 75])
        coeficiente_de_variacion = (desviacion_estandar / media) * 100

        mensaje = f"Media: ${media:.2f}\nMediana: ${mediana:.2f}\nModa: ${moda:.2f}\nSuma: ${suma:.2f}\nVarianza: ${varianza:.2f}\n"
        mensaje += f"Cuartiles (25% - 50% - 75%): ${cuartiles[0]:.2f} - ${cuartiles[1]:.2f} - ${cuartiles[2]:.2f}\nCoeficiente de Variación: {coeficiente_de_variacion:.2f}%"

        if avanzadas:
            # Corrección: Calcular el rango
            rango = max(valores_monetarios) - min(valores_monetarios)

            # Nueva adición: Calcula el rango intercuartil (IQR)
            iqr = cuartiles[2] - cuartiles[0]

            # Nueva adición: Detecta valores atípicos usando el método IQR
            outlier_threshold = 1.5
            lower_bound = cuartiles[0] - outlier_threshold * iqr
            upper_bound = cuartiles[2] + outlier_threshold * iqr
            outliers = [valor for valor in valores_monetarios if valor < lower_bound or valor > upper_bound]

            mensaje += f"\nRango: ${rango:.2f}\nIQR (Rango Intercuartil): ${iqr:.2f}\nValores Atípicos: {', '.join(map(str, outliers))}"

        ventana_estadisticas = Toplevel(ventana)
        ventana_estadisticas.title("Estadísticas Descriptivas")
        etiqueta_estadisticas = tk.Label(ventana_estadisticas, text=mensaje)
        etiqueta_estadisticas.pack()

def mostrar_histograma():
    denominaciones = ['50', '100', '200', '500', '1000']
    cantidades = [valor_50.get(), valor_100.get(), valor_200.get(), valor_500.get(), valor_1000.get()]
    
    plt.bar(denominaciones, cantidades)
    plt.xlabel('Denominación de Moneda')
    plt.ylabel('Cantidad')
    plt.title('Distribución de Monedas por Denominación')
    plt.show()

def calcular_falta_para_meta():
    ahorro_actual = (valor_50.get() * 50) + (valor_100.get() * 100) + (valor_200.get() * 200) + (valor_500.get() * 500) + (valor_1000.get() * 1000)
    
    if ahorro_actual >= meta_ahorro.get():
        diferencia = ahorro_actual - meta_ahorro.get()
        messagebox.showinfo("Meta de Ahorro", f"Felicidades, has superado tu meta de ahorro por ${diferencia:.2f}!")
    else:
        falta_para_meta = meta_ahorro.get() - ahorro_actual
        messagebox.showinfo("Meta de Ahorro", f"Falta ${falta_para_meta:.2f} para alcanzar tu meta de ahorro.")

# Crear una lista para rastrear el ahorro diario con el tiempo
ahorro_diario = []

def actualizar_tendencia():
    fecha_actual = datetime.datetime.today().strftime('%Y-%m-%d')
    ahorro_actual = (valor_50.get() * 50) + (valor_100.get() * 100) + (valor_200.get() * 200) + (valor_500.get() * 500) + (valor_1000.get() * 1000)
    ahorro_diario.append((fecha_actual, ahorro_actual))
    guardar_tendencia()  # Llama a la función para guardar la tendencia

def mostrar_tendencia():
    fechas = [fecha for fecha, _ in ahorro_diario]
    ahorros = [ahorro for _, ahorro in ahorro_diario]
    
    plt.plot(fechas, ahorros, marker='o', linestyle='-')
    plt.xlabel('Fecha')
    plt.ylabel('Ahorro Acumulado')
    plt.title('Tendencia de Ahorro con el Tiempo')
    plt.xticks(rotation=45)
    plt.show()

def guardar_tendencia():
    with open('tendencia.json', 'w') as archivo:
        json.dump(ahorro_diario, archivo)

# Crear una ventana principal
ventana = tk.Tk()
ventana.title("Monedas Acumuladas")

# Crear una ventana de movimientos
ventana_movimientos = Toplevel(ventana)
ventana_movimientos.title("Registro de Movimientos")
ventana_movimientos_text = tk.Text(ventana_movimientos, height=15, width=40)
ventana_movimientos_text.pack()

# Crea una variable de meta de ahorro y establece un valor inicial
meta_ahorro = tk.DoubleVar()
meta_ahorro.set(1000)

# Obtener el tamaño de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Definir el ancho y alto de la ventana
ancho_ventana = 390  # Ajusta el ancho según tus necesidades
alto_ventana = 390  # Ajusta el alto según tus necesidades

# Calcular las coordenadas para centrar la ventana
x = (ancho_pantalla - ancho_ventana) // 2
y = (alto_pantalla - alto_ventana) // 2

# Establecer el tamaño y la posición de la ventana
ventana.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')

# Cargar el diccionario de monedas desde el archivo JSON
diccionario_monedas = cargar_diccionario()

# Definir las variables para los valores
valor_50 = tk.IntVar()
valor_100 = tk.IntVar()
valor_200 = tk.IntVar()
valor_500 = tk.IntVar()
valor_1000 = tk.IntVar()

# Inicializar los valores de acuerdo al diccionario
valor_50.set(diccionario_monedas.get('50', 0))
valor_100.set(diccionario_monedas.get('100', 0))
valor_200.set(diccionario_monedas.get('200', 0))
valor_500.set(diccionario_monedas.get('500', 0))
valor_1000.set(diccionario_monedas.get('1000', 0))

# Crear una etiqueta para mostrar el total
total_label = tk.Label(ventana, text="Total: $0")

# Actualizar el total al iniciar la aplicación
actualizar_total(total_label)

# Crear las etiquetas y las entradas de texto
etiqueta_50 = tk.Label(ventana, text="50")
entrada_50 = tk.Label(ventana, textvariable=valor_50)

etiqueta_100 = tk.Label(ventana, text="100")
entrada_100 = tk.Label(ventana, textvariable=valor_100)

etiqueta_200 = tk.Label(ventana, text="200")
entrada_200 = tk.Label(ventana, textvariable=valor_200)

etiqueta_500 = tk.Label(ventana, text="500")
entrada_500 = tk.Label(ventana, textvariable=valor_500)

etiqueta_1000 = tk.Label(ventana, text="1000")
entrada_1000 = tk.Label(ventana, textvariable=valor_1000)

boton_50 = tk.Button(ventana, text="+", command=lambda: incrementar_valor(valor_50, entrada_50, total_label, ventana_movimientos_text))
boton_100 = tk.Button(ventana, text="+", command=lambda: incrementar_valor(valor_100, entrada_100, total_label, ventana_movimientos_text))
boton_200 = tk.Button(ventana, text="+", command=lambda: incrementar_valor(valor_200, entrada_200, total_label, ventana_movimientos_text))
boton_500 = tk.Button(ventana, text="+", command=lambda: incrementar_valor(valor_500, entrada_500, total_label, ventana_movimientos_text))
boton_1000 = tk.Button(ventana, text="+", command=lambda: incrementar_valor(valor_1000, entrada_1000, total_label, ventana_movimientos_text))

# Agregar botones para disminuir las monedas
boton_disminuir_50 = tk.Button(ventana, text="-", command=lambda: disminuir_valor(valor_50, entrada_50, total_label, ventana_movimientos_text))
boton_disminuir_100 = tk.Button(ventana, text="-", command=lambda: disminuir_valor(valor_100, entrada_100, total_label, ventana_movimientos_text))
boton_disminuir_200 = tk.Button(ventana, text="-", command=lambda: disminuir_valor(valor_200, entrada_200, total_label,ventana_movimientos_text))
boton_disminuir_500 = tk.Button(ventana, text="-", command=lambda: disminuir_valor(valor_500, entrada_500, total_label, ventana_movimientos_text))
boton_disminuir_1000 = tk.Button(ventana, text="-", command=lambda: disminuir_valor(valor_1000, entrada_1000, total_label, ventana_movimientos_text))

# Colocar los botones de disminución junto a los de incremento
boton_disminuir_50.grid(row=0, column=3)
boton_disminuir_100.grid(row=1, column=3)
boton_disminuir_200.grid(row=2, column=3)
boton_disminuir_500.grid(row=3, column=3)
boton_disminuir_1000.grid(row=4, column=3)

# Colocar las etiquetas y las entradas de texto en la ventana
etiqueta_50.grid(row=0, column=0, sticky="e")
entrada_50.grid(row=0, column=1)
boton_50.grid(row=0, column=2)

etiqueta_100.grid(row=1, column=0, sticky="e")
entrada_100.grid(row=1, column=1)
boton_100.grid(row=1, column=2)

etiqueta_200.grid(row=2, column=0, sticky="e")
entrada_200.grid(row=2, column=1)
boton_200.grid(row=2, column=2)

etiqueta_500.grid(row=3, column=0, sticky="e")
entrada_500.grid(row=3, column=1)
boton_500.grid(row=3, column=2)

etiqueta_1000.grid(row=4, column=0, sticky="e")
entrada_1000.grid(row=4, column=1)
boton_1000.grid(row=4, column=2)

total_label.grid(row=5, column=0, columnspan=3, sticky="n")

# Crear un botón para mostrar estadísticas descriptivas
boton_estadisticas_avanzadas = tk.Button(ventana, text="Mostrar Estadísticas Avanzadas", command=lambda: mostrar_estadisticas(avanzadas=True))
boton_estadisticas_avanzadas.grid(row=7, column=0, columnspan=3, sticky="n")

# Crear un menú desplegable para seleccionar la fecha
fechas_disponibles = list(graficas_por_fecha.keys())
combobox_fecha = Combobox(ventana, values=fechas_disponibles)
combobox_fecha.grid(row=8, column=0, columnspan=3, sticky="n")

# Crear un botón para mostrar la gráfica seleccionada
boton_mostrar_grafica = tk.Button(ventana, text="Mostrar Gráfica Seleccionada", command=mostrar_grafica_seleccionada)
boton_mostrar_grafica.grid(row=9, column=0, columnspan=3, sticky="n")

boton_histograma = tk.Button(ventana, text="Mostrar Histograma", command=mostrar_histograma)
boton_histograma.grid(row=10, column=0, columnspan=3, sticky="n")

etiqueta_meta = tk.Label(ventana, text="Meta de Ahorro: $")
etiqueta_meta.grid(row=11, column=0)
entrada_meta = tk.Entry(ventana, textvariable=meta_ahorro)
entrada_meta.grid(row=11, column=1)
boton_meta = tk.Button(ventana, text="Calcular Falta para Meta", command=calcular_falta_para_meta)
boton_meta.grid(row=11, column=2)

boton_actualizar_tendencia = tk.Button(ventana, text="Actualizar Tendencia", command=actualizar_tendencia)
boton_actualizar_tendencia.grid(row=12, column=0, columnspan=3, sticky="n")

boton_tendencia = tk.Button(ventana, text="Mostrar Tendencia", command=mostrar_tendencia)
boton_tendencia.grid(row=13, column=0, columnspan=3, sticky="n")

# Crear un botón para abrir la ventana de movimientos
boton_movimientos = tk.Button(ventana, text="Ver Movimientos", command=mostrar_movimientos)
boton_movimientos.grid(row=14, column=0, columnspan=3, sticky="n")

# Cargar la tendencia desde el archivo JSON
try:
    with open('tendencia.json', 'r') as archivo:
        ahorro_diario = json.load(archivo)
except FileNotFoundError:
    ahorro_diario = []

# Generar y almacenar automáticamente una gráfica para la fecha actual al iniciar la aplicación
generar_y_almacenar_grafica()

# Función para guardar los valores al cerrar la ventana
def guardar_valores_al_cerrar():
    diccionario_monedas['50'] = valor_50.get()
    diccionario_monedas['100'] = valor_100.get()
    diccionario_monedas['200'] = valor_200.get()
    diccionario_monedas['500'] = valor_500.get()
    diccionario_monedas['1000'] = valor_1000.get()
    diccionario_monedas['total'] = total_label.cget("text")
    guardar_diccionario(diccionario_monedas)
    ventana.destroy()

# Configurar la función para guardar los valores al cerrar la ventana
ventana.protocol("WM_DELETE_WINDOW", guardar_valores_al_cerrar)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()