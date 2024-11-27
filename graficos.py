from collections import defaultdict, Counter
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def mostrar_grafico(fig, canvas_holder):
    """
    Muestra el gráfico generado en el canvas_holder de la interfaz.
    Si ya hay un gráfico, lo destruye antes de mostrar el nuevo.
    """
    # Si ya hay un gráfico, destruirlo
    if canvas_holder.get("canvas"):
        canvas_holder["canvas"].get_tk_widget().destroy()

    # Crear y mostrar el gráfico
    canvas_holder["canvas"] = FigureCanvasTkAgg(fig, master=canvas_holder["master"])
    canvas_holder["canvas"].draw()
    canvas_holder["canvas"].get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

# Función para obtener ventas por rango (diarias, semanales, mensuales, anuales)
def obtener_ventas_por_fecha(pedidos, rango: str):
    """
    Obtiene las ventas organizadas por hora, día, mes o año desde la lista de pedidos.
    """
    # Inicializar valores predeterminados
    if rango == "diarias":
        ventas = {f"{hora:02d}:00": 0 for hora in range(24)}  # Horas del día
    elif rango == "semanales":
        ventas = {dia: 0 for dia in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}  # Días de la semana
    elif rango == "mensuales":
        ventas = {mes: 0 for mes in ["January", "February", "March", "April", "May", "June",
                                     "July", "August", "September", "October", "November", "December"]}  # Meses
    elif rango == "anuales":
        ventas = {f"Q{i}": 0 for i in range(1, 5)}  # Trimestres del año
    else:
        raise ValueError("Rango no válido. Use: 'diarias', 'semanales', 'mensuales' o 'anuales'.")

    # Agregar ventas reales
    for pedido in pedidos:
        if rango == "diarias":
            clave = pedido.Fecha.strftime("%H:00")
        elif rango == "semanales":
            clave = pedido.Fecha.strftime("%A")
        elif rango == "mensuales":
            clave = pedido.Fecha.strftime("%B")
        elif rango == "anuales":
            mes = pedido.Fecha.month
            if mes <= 3:
                clave = "Q1"
            elif mes <= 6:
                clave = "Q2"
            elif mes <= 9:
                clave = "Q3"
            else:
                clave = "Q4"
        ventas[clave] += pedido.Total

    return dict(sorted(ventas.items()))


# Gráfico de ventas por rango
def generar_grafico_ventas(pedidos, rango, canvas_holder):
    """
    Genera y muestra un gráfico de ventas basado en el rango especificado.
    """
    ventas = obtener_ventas_por_fecha(pedidos, rango)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(ventas.keys(), ventas.values(), color="skyblue")
    ax.set_title(f"Ventas {rango.capitalize()}")
    ax.set_xlabel("Rango")
    ax.set_ylabel("Total Ventas ($)")
    ax.tick_params(axis='x', rotation=45)

    mostrar_grafico(fig, canvas_holder)


# Ingredientes más usados
def obtener_ingredientes_mas_usados(menus):
    """
    Obtiene los ingredientes más usados desde la lista de menús.
    """
    ingredientes = []
    for menu in menus:
        for ingrediente in menu.Ingredientes:
            if isinstance(ingrediente, dict) and "nombre" in ingrediente:
                ingredientes.append(ingrediente["nombre"])
            elif isinstance(ingrediente, str):
                ingredientes.append(ingrediente)

    return Counter(ingredientes).most_common(5)


def generar_grafico_ingredientes(menus, canvas_holder):
    """
    Genera y muestra un gráfico de los ingredientes más usados.
    """
    ingredientes_mas_usados = obtener_ingredientes_mas_usados(menus)

    if not ingredientes_mas_usados:
        ingredientes_mas_usados = [("Sin datos", 0)]

    ingredientes, cantidades = zip(*ingredientes_mas_usados)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(ingredientes, cantidades, color="purple")
    ax.set_title("Ingredientes Más Usados")
    ax.set_xlabel("Ingrediente")
    ax.set_ylabel("Cantidad Usada")
    ax.tick_params(axis='x', rotation=45)

    mostrar_grafico(fig, canvas_holder)


# Menús más vendidos
def obtener_menus_mas_vendidos(pedidos, limite=5):
    """
    Obtiene los menús más vendidos desde la lista de pedidos.
    """
    menu_ventas = Counter(pedido.Menu for pedido in pedidos)
    return menu_ventas.most_common(limite)


def generar_grafico_menus(pedidos, canvas_holder):
    """
    Genera y muestra un gráfico de los menús más vendidos.
    """
    menus_mas_vendidos = obtener_menus_mas_vendidos(pedidos)

    if not menus_mas_vendidos:
        menus_mas_vendidos = [("Sin datos", 0)]

    nombres, cantidades = zip(*menus_mas_vendidos)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(nombres, cantidades, color="orange")
    ax.set_title("Menús Más Vendidos")
    ax.set_xlabel("Menús")
    ax.set_ylabel("Cantidad Vendida")
    ax.tick_params(axis='x', rotation=45)

    mostrar_grafico(fig, canvas_holder)
