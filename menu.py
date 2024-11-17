from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import customtkinter as ctk
import tkinter as tk
from PIL import Image
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from datetime import datetime
import re

class Ingreso_Ingredientes:
    def __init__(self, nombre_ingrediente, cantidad):
        self.nombre = nombre_ingrediente
        self.cantidad = cantidad

class MenuItem:
    def __init__(self, nombre, ingredientes, icono_menu=None, precio=0):
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.icono_menu = icono_menu
        self.precio = precio
        self.cantidad = 0  # Añadido para almacenar la cantidad

class PestañasPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante")
        self.geometry("1000x600")
        self.tabview = ctk.CTkTabview(self, width=600, height=500)
        self.tabview.pack(padx=20, pady=20)

        self.lista_Ingredientes = []  # Lista para almacenar los ingredientes ingresados
        self.pedido = []  # Lista para almacenar el pedido actual

        self.crear_pestanas()

    def crear_pestanas(self):
        self.tab1 = self.tabview.add("Ingreso De Ingredientes")
        self.tab2 = self.tabview.add("Pedido")
        self.configurar_pestana1()
        self.configurar_pestana2()

    def configurar_pestana1(self):
        # Frame para ingresar ingredientes
        Window1 = ctk.CTkFrame(self.tab1)
        Window1.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario de ingredientes
        label_nombre_ingred = ctk.CTkLabel(Window1, text="Nombre Ingrediente: ")
        label_nombre_ingred.pack(pady=5)
        self.entry_nombre_ingred = ctk.CTkEntry(Window1)
        self.entry_nombre_ingred.pack(pady=5)

        label_cantidad_ingred = ctk.CTkLabel(Window1, text="Cantidad: ")
        label_cantidad_ingred.pack(pady=5)
        self.entry_cantidad_ingred = ctk.CTkEntry(Window1)
        self.entry_cantidad_ingred.pack(pady=5)

        # Botón para ingresar ingrediente
        self.boton_ingresar = ctk.CTkButton(Window1, text="Ingresar Ingrediente", command=self.ingresar_Ingrediente)
        self.boton_ingresar.pack(pady=10)

        # Botón para eliminar ingrediente
        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white", command=self.eliminar_Ingrediente)
        self.boton_eliminar.pack(pady=10)

        # Treeview para mostrar los ingredientes ingresados
        self.tree = ttk.Treeview(frame_treeview, columns=("Nombre", "Cantidad"), show="headings")
        self.tree.heading("Nombre", text="Nombre Ingrediente")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Botón para generar menú
        self.boton_generar_menu = ctk.CTkButton(Window1, text="Generar Menú", command=self.generar_menu)
        self.boton_generar_menu.pack(side="bottom", pady=10)

    def validar_Ingrediente(self, nombre, cantidad):
        # Validar que el nombre contenga solo letras y que la cantidad sea un número positivo
        if not re.match(r"^[a-zA-Z\s]+$", nombre):
            CTkMessagebox(title="Error de Validación", message="El nombre del ingrediente debe contener solo letras y espacios.", icon="warning")
            return False
        if not cantidad.isdigit() or int(cantidad) <= 0:
            CTkMessagebox(title="Error de Validación", message="La cantidad debe contener solo números enteros positivos.", icon="warning")
            return False

        # Validar cantidad contra el stock
        ingrediente_en_stock = next((item for item in self.lista_Ingredientes if item.nombre == nombre), None)
        if ingrediente_en_stock and int(cantidad) > ingrediente_en_stock.cantidad:
            CTkMessagebox(title="Error de Validación", message=f"No hay suficiente stock para '{nombre}'. Solo quedan {ingrediente_en_stock.cantidad}.", icon="warning")
            return False

        return True


    def ingresar_Ingrediente(self):
        nombre = self.entry_nombre_ingred.get()
        cantidad = self.entry_cantidad_ingred.get()

        if not self.validar_Ingrediente(nombre, cantidad):
            return

        nuevo_ingrediente = Ingreso_Ingredientes(nombre, int(cantidad))

        # Buscar si el ingrediente ya existe en la lista
        for ing in self.lista_Ingredientes:
            if ing.nombre == nombre:
                ing.cantidad += nuevo_ingrediente.cantidad
                self.actualizar_treeview()
                return

        self.lista_Ingredientes.append(nuevo_ingrediente)
        self.actualizar_treeview()

    def generar_menu(self):
    # Definir los menús disponibles
        menu1 = MenuItem("Papas Fritas", [Ingreso_Ingredientes("papas", 5)], "icono_papas_fritas_64x64.png", 500)
        menu2 = MenuItem("Pepsi", [Ingreso_Ingredientes("bebida", 1)], "icono_cola_64x64.png", 1100)
        menu3 = MenuItem("Completo", [Ingreso_Ingredientes("vianesa", 1), Ingreso_Ingredientes("pan de completo", 1), Ingreso_Ingredientes("tomate", 1), Ingreso_Ingredientes("palta", 1)], "icono_hot_dog_sin_texto_64x64.png", 1800)
        menu4 = MenuItem("Hamburguesa", [Ingreso_Ingredientes("pan de hamburguesa", 1), Ingreso_Ingredientes("lamina de queso", 1), Ingreso_Ingredientes("churrasco de carne", 1)], "icono_hamburguesa_negra_64x64.png", 3500)

        menus_disponibles = []
        for menu_item in [menu1, menu2, menu3, menu4]:
            ingredientes_faltantes = []
            for ingrediente in menu_item.ingredientes:
                ingrediente_en_stock = next((item for item in self.lista_Ingredientes if item.nombre == ingrediente.nombre), None)
                if not ingrediente_en_stock or ingrediente_en_stock.cantidad < ingrediente.cantidad:
                    ingredientes_faltantes.append(ingrediente.nombre)

            if not ingredientes_faltantes:
                menus_disponibles.append(menu_item)
            else:
                mensaje_faltantes = ', '.join(ingredientes_faltantes)
                CTkMessagebox(title="Ingredientes Faltantes", message=f"Faltan los siguientes ingredientes para '{menu_item.nombre}': {mensaje_faltantes}", icon="warning")

        if menus_disponibles:
            # Limpiar las tarjetas existentes
            for widget in self.tarjetas_frame.winfo_children():
                widget.destroy()

            for menu_item in menus_disponibles:
                self.crear_tarjeta(menu_item)
            CTkMessagebox(title="Menú Generado", message="Menús generados correctamente.", icon="info")
        else:
            CTkMessagebox(title="Sin Menú", message="No hay menús que se puedan generar con los ingredientes disponibles.", icon="info")

    def actualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for ingrediente in self.lista_Ingredientes:
            self.tree.insert("", "end", values=(ingrediente.nombre, ingrediente.cantidad))

    def eliminar_Ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un ingrediente para eliminar.", icon="warning")
            return

        for item in seleccion:
            ingrediente_nombre = self.tree.item(item, "values")[0]
            self.lista_Ingredientes = [ing for ing in self.lista_Ingredientes if ing.nombre != ingrediente_nombre]
            self.tree.delete(item)

        self.actualizar_treeview()

    def configurar_pestana2(self):
        # Frame para mostrar las tarjetas de menú
        self.tarjetas_frame = ctk.CTkFrame(self.tab2)
        self.tarjetas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para mostrar el pedido
        self.pedido_frame = ctk.CTkFrame(self.tab2, fg_color="#3C3C3C")
        self.pedido_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview para el pedido
        self.tree_pedido = ttk.Treeview(self.pedido_frame, columns=("Nombre", "Cantidad", "Precio"), show="headings")
        self.tree_pedido.heading("Nombre", text="Nombre del Menú")
        self.tree_pedido.heading("Cantidad", text="Cantidad")
        self.tree_pedido.heading("Precio", text="Precio Unitario")
        self.tree_pedido.pack(expand=True, fill="both", padx=10, pady=10)

        # Total y botones
        self.total_label = ctk.CTkLabel(self.pedido_frame, text="Total: $0.00")
        self.total_label.pack(side="left", padx=10, pady=10)

        self.boton_eliminar_menu = ctk.CTkButton(self.pedido_frame, text="Eliminar Menú", command=self.eliminar_menu)
        self.boton_eliminar_menu.pack(side="left", padx=10, pady=10)

        self.boton_generar_boleta = ctk.CTkButton(self.pedido_frame, text="Generar Boleta", command=self.generar_boleta)
        self.boton_generar_boleta.pack(side="left", padx=10, pady=10)

    def crear_tarjeta(self, menu_item):
    # Ajustar el tamaño del frame según sea necesario
        frame_menu = ctk.CTkFrame(self.tarjetas_frame, width=250, height=250)  # Tamaño ajustado
        frame_menu.pack(side="left", padx=10, pady=10)

        # Imagen del menú
        if menu_item.icono_menu:
            img = Image.open(menu_item.icono_menu)
            img = img.resize((200, 150), Image.LANCZOS)  # Tamaño ajustado para la imagen
            photo = ctk.CTkImage(img)
            label_imagen = ctk.CTkLabel(frame_menu, image=photo, text="")  # Eliminar texto del label
            label_imagen.image = photo  # Necesario para evitar que la imagen sea recolectada por el GC

            # Agregar el evento de clic a la imagen
            label_imagen.bind("<Button-1>", lambda e, mi=menu_item: self.agregar_al_pedido(mi))
            label_imagen.pack()

        # Nombre del producto
        label_nombre = ctk.CTkLabel(frame_menu, text=menu_item.nombre, font=("Arial", 12, "bold"))
        label_nombre.pack(pady=5)

    def agregar_al_pedido(self, menu_item):
    # Verificar si el menú ya está en el pedido
        for item in self.tree_pedido.get_children():
            if self.tree_pedido.item(item, "values")[0] == menu_item.nombre:
                # Convertir la cantidad actual a entero para sumar el nuevo valor
                cantidad_actual = int(self.tree_pedido.item(item, "values")[1])
                self.tree_pedido.item(item, values=(menu_item.nombre, cantidad_actual + 1, menu_item.precio))
                
                # Actualizar self.pedido
                for pedido_item in self.pedido:
                    if pedido_item.nombre == menu_item.nombre:
                        pedido_item.cantidad += 1
                        break
                
                self.calcular_total()
                return

        # Si no está en el pedido, añadirlo
        self.tree_pedido.insert("", "end", values=(menu_item.nombre, 1, menu_item.precio))
        
        # Actualizar self.pedido
        self.pedido.append(MenuItem(menu_item.nombre, menu_item.ingredientes, menu_item.icono_menu, menu_item.precio))
        self.pedido[-1].cantidad = 1
        
        self.calcular_total()

    def eliminar_menu(self):
        seleccion = self.tree_pedido.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un menú para eliminar.", icon="warning")
            return

        for item in seleccion:
            menu_nombre = self.tree_pedido.item(item, "values")[0]
            self.tree_pedido.delete(item)

            # Actualizar self.pedido
            self.pedido = [pedido_item for pedido_item in self.pedido if pedido_item.nombre != menu_nombre]

        self.calcular_total()

    def calcular_total(self):
        total = sum(float(self.tree_pedido.item(item, "values")[2]) * int(self.tree_pedido.item(item, "values")[1]) for item in self.tree_pedido.get_children())
        self.total_label.configure(text=f"Total: ${total:.2f}")


    #utiliza el ReportLab para generar la boleta, si no lo tienen es una extencion [ pip install ReportLab ]
    def generar_boleta(self):
        if not self.pedido:
            CTkMessagebox(title="Error", message="No hay elementos en el pedido para generar una boleta.", icon="warning")
            return

        total_precio = sum(menu_item.precio * menu_item.cantidad for menu_item in self.pedido)
        # Crear el documento PDF
        nombre_archivo = "boleta.pdf"
        pdf = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        elementos = []
        estilos = getSampleStyleSheet()
        
        # Título de la boleta
        titulo = Paragraph("Boleta de Pedido", estilos['Title'])
        elementos.append(titulo)
        elementos.append(Spacer(1, 12))  # Espacio después del título

        # Fecha de la boleta
        fecha = Paragraph(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", estilos['Normal'])
        elementos.append(fecha)
        elementos.append(Spacer(1, 12))  # Espacio después de la fecha

        # Tabla de contenido del pedido
        datos = [["Nombre del Menú", "Cantidad", "Precio Unitario", "Total"]]
        total_pedido = 0
        
        for item in self.pedido:
            nombre = item.nombre  # Acceder al atributo 'nombre' del objeto item
            cantidad = item.cantidad  # Acceder al atributo 'cantidad' del objeto item
            precio = item.precio  # Acceder al atributo 'precio' del objeto item
            total = precio * cantidad
            datos.append([nombre, cantidad, f"${precio:.2f}", f"${total:.2f}"])
            total_pedido += total

        # Agregar fila con el total final
        datos.append(["", "", "Total", f"${total_pedido:.2f}"])

        # Crear la tabla en ReportLab
        tabla = Table(datos)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elementos.append(tabla)
        elementos.append(Spacer(1, 12))  # Espacio después de la tabla

        # Generar el PDF
        pdf.build(elementos)
        CTkMessagebox(title="Boleta Generada", message=f"La boleta se ha generado correctamente como '{nombre_archivo}'.", icon="info")


if __name__ == "__main__":
    app = PestañasPrincipal()
    app.mainloop()


    #rial rial rial rial rial 0.1------------