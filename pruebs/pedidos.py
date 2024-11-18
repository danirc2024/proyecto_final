import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from datetime import datetime

class PedidosVentana(ctk.CTkFrame):
    def __init__(self, master, lista_pedidos, lista_clientes):
        super().__init__(master)
        self.lista_pedidos = lista_pedidos
        self.lista_clientes = lista_clientes
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.configurar_ventana()

    def configurar_ventana(self):
        # Frame para crear y mostrar pedidos
        frame_formulario = ctk.CTkFrame(self)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_lista = ctk.CTkFrame(self)
        frame_lista.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario de pedidos
        ctk.CTkLabel(frame_formulario, text="Cliente: ").pack(pady=5)
        self.combo_cliente = ctk.CTkComboBox(frame_formulario, values=[cliente["nombre"] for cliente in self.lista_clientes])
        self.combo_cliente.pack(pady=5)

        ctk.CTkLabel(frame_formulario, text="Descripción: ").pack(pady=5)
        self.entry_descripcion = ctk.CTkEntry(frame_formulario)
        self.entry_descripcion.pack(pady=5)

        ctk.CTkLabel(frame_formulario, text="Total: ").pack(pady=5)
        self.entry_total = ctk.CTkEntry(frame_formulario)
        self.entry_total.pack(pady=5)

        ctk.CTkButton(frame_formulario, text="Crear Pedido", command=self.crear_pedido).pack(pady=10)
        ctk.CTkButton(frame_formulario, text="Eliminar Pedido", command=self.eliminar_pedido).pack(pady=10)

        # Lista de pedidos
        self.tree = ttk.Treeview(frame_lista, columns=("Cliente", "Descripción", "Total", "Fecha"), show="headings")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def crear_pedido(self):
        cliente = self.combo_cliente.get()
        descripcion = self.entry_descripcion.get()
        total = self.entry_total.get()

        if not cliente or not descripcion or not total.isdigit():
            CTkMessagebox(title="Error", message="Complete todos los campos correctamente.", icon="warning")
            return

        pedido = {
            "cliente": cliente,
            "descripcion": descripcion,
            "total": int(total),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.lista_pedidos.append(pedido)
        self.actualizar_lista()
    

    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for pedido in self.lista_pedidos:
            self.tree.insert("", "end", values=(pedido["cliente"], pedido["descripcion"], pedido["total"], pedido["fecha"]))

    def eliminar_pedido(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un cliente para eliminar.", icon="warning")
            return

        for item in seleccion:
            nombre = self.tree.item(item, "values")[0]
            self.lista_pedidos = [ing for ing in self.lista_pedidos if ing["cliente"] != nombre]
            self.tree.delete(item)
        self.actualizar_lista()
