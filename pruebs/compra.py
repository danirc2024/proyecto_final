import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from fpdf import FPDF
from datetime import datetime


class CompraVentana(ctk.CTkFrame):
    def __init__(self, master, lista_clientes, lista_menus, lista_pedidos):
        super().__init__(master)
        self.lista_clientes = lista_clientes  # Clientes registrados
        self.lista_menus = lista_menus  # Menús creados
        self.lista_pedidos = lista_pedidos  # Pedidos realizados
        self.pedido_actual = []  # Menús seleccionados para el pedido actual
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.configurar_ventana()

    def configurar_ventana(self):
        # Frame para selección de cliente y menús
        frame_seleccion = ctk.CTkFrame(self)
        frame_seleccion.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame para detalle del pedido
        frame_detalle = ctk.CTkFrame(self)
        frame_detalle.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Selección de cliente
        ctk.CTkLabel(frame_seleccion, text="Seleccionar Cliente:").pack(pady=5)
        self.combo_cliente = ctk.CTkComboBox(
            frame_seleccion, values=[cliente["nombre"] for cliente in self.lista_clientes]
        )
        self.combo_cliente.pack(pady=5)

        # Selección de menú
        ctk.CTkLabel(frame_seleccion, text="Seleccionar Menú:").pack(pady=5)
        self.combo_menu = ctk.CTkComboBox(
            frame_seleccion, values=[menu["nombre"] for menu in self.lista_menus]
        )
        self.combo_menu.pack(pady=5)

        ctk.CTkLabel(frame_seleccion, text="Cantidad:").pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_seleccion)
        self.entry_cantidad.pack(pady=5)

        ctk.CTkButton(frame_seleccion, text="Agregar al Pedido", command=self.agregar_al_pedido).pack(pady=10)

        # Treeview para detalle del pedido
        ctk.CTkLabel(frame_detalle, text="Detalle del Pedido:").pack(pady=5)
        self.tree_pedido = ttk.Treeview(
            frame_detalle, columns=("Menú", "Cantidad", "Precio Unitario", "Subtotal"), show="headings"
        )
        self.tree_pedido.heading("Menú", text="Menú")
        self.tree_pedido.heading("Cantidad", text="Cantidad")
        self.tree_pedido.heading("Precio Unitario", text="Precio Unitario")
        self.tree_pedido.heading("Subtotal", text="Subtotal")
        self.tree_pedido.pack(expand=True, fill="both", padx=10, pady=10)

        # Total y botones
        self.label_total = ctk.CTkLabel(frame_detalle, text="Total: $0.00", font=("Arial", 16))
        self.label_total.pack(pady=10)

        ctk.CTkButton(frame_detalle, text="Generar Boleta", command=self.generar_boleta).pack(pady=5)

    def agregar_al_pedido(self):
        cliente = self.combo_cliente.get()
        menu = self.combo_menu.get()
        cantidad = self.entry_cantidad.get()

        if not cliente or not menu or not cantidad.isdigit() or int(cantidad) <= 0:
            CTkMessagebox(title="Error", message="Complete todos los campos correctamente.", icon="warning")
            return

        cantidad = int(cantidad)
        menu_seleccionado = next((m for m in self.lista_menus if m["nombre"] == menu), None)

        if not menu_seleccionado:
            CTkMessagebox(title="Error", message="El menú seleccionado no existe.", icon="warning")
            return

        # Calcular subtotal
        precio_unitario = sum(ing["cantidad"] * 100 for ing in menu_seleccionado["ingredientes"])  # Ejemplo: precio ficticio
        subtotal = precio_unitario * cantidad

        # Agregar al pedido actual
        self.pedido_actual.append({"menu": menu, "cantidad": cantidad, "precio": precio_unitario, "subtotal": subtotal})
        self.actualizar_treeview()
        self.calcular_total()

    def actualizar_treeview(self):
        # Limpiar Treeview
        for item in self.tree_pedido.get_children():
            self.tree_pedido.delete(item)

        # Rellenar Treeview con datos del pedido actual
        for item in self.pedido_actual:
            self.tree_pedido.insert(
                "", "end", values=(item["menu"], item["cantidad"], f"${item['precio']:.2f}", f"${item['subtotal']:.2f}")
            )

    def calcular_total(self):
        total = sum(item["subtotal"] for item in self.pedido_actual)
        self.label_total.configure(text=f"Total: ${total:.2f}")

    def generar_boleta(self):
        if not self.pedido_actual:
            CTkMessagebox(title="Error", message="No hay elementos en el pedido para generar la boleta.", icon="warning")
            return

        cliente = self.combo_cliente.get()
        total = sum(item["subtotal"] for item in self.pedido_actual)

        # Generar PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Boleta Restaurante - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
        pdf.ln(10)

        for item in self.pedido_actual:
            pdf.cell(200, 10, txt=f"{item['menu']} - Cantidad: {item['cantidad']} - Subtotal: ${item['subtotal']:.2f}", ln=True)

        pdf.cell(200, 10, txt=f"Total: ${total:.2f}", ln=True)

        nombre_archivo = "boleta_actual.pdf"
        pdf.output(nombre_archivo)

        # Guardar pedido en memoria
        self.lista_pedidos.append({"cliente": cliente, "detalle": self.pedido_actual.copy(), "total": total, "fecha": datetime.now()})

        CTkMessagebox(title="Éxito", message=f"Boleta generada: {nombre_archivo}", icon="info")
        self.pedido_actual.clear()
        self.actualizar_treeview()
        self.calcular_total()
