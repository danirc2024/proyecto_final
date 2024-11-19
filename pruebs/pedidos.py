import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox


class PedidosVentana(ctk.CTkFrame):
    def __init__(self, master, lista_pedidos, lista_clientes):
        super().__init__(master)
        self.lista_pedidos = lista_pedidos  # Pedidos realizados
        self.lista_clientes = lista_clientes  # Clientes registrados
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.configurar_ventana()

    def configurar_ventana(self):
        # Frame para lista de pedidos
        frame_lista = ctk.CTkFrame(self)
        frame_lista.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame para detalles del pedido
        frame_detalle = ctk.CTkFrame(self)
        frame_detalle.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Lista de pedidos
        ctk.CTkLabel(frame_lista, text="Pedidos Realizados:").pack(pady=5)
        self.tree_pedidos = ttk.Treeview(
            frame_lista, columns=("Cliente", "Fecha", "Total"), show="headings"
        )
        self.tree_pedidos.heading("Cliente", text="Cliente")
        self.tree_pedidos.heading("Fecha", text="Fecha")
        self.tree_pedidos.heading("Total", text="Total")
        self.tree_pedidos.pack(expand=True, fill="both", padx=10, pady=10)

        # Botón para eliminar pedido
        ctk.CTkButton(frame_lista, text="Eliminar Pedido", command=self.eliminar_pedido).pack(pady=10)

        # Filtro por cliente
        ctk.CTkLabel(frame_lista, text="Filtrar por Cliente:").pack(pady=5)
        self.combo_cliente = ctk.CTkComboBox(
            frame_lista, values=[cliente["nombre"] for cliente in self.lista_clientes], command=self.filtrar_pedidos
        )
        self.combo_cliente.pack(pady=5)

        # Detalle del pedido seleccionado
        ctk.CTkLabel(frame_detalle, text="Detalle del Pedido:").pack(pady=5)
        self.tree_detalle = ttk.Treeview(
            frame_detalle, columns=("Menú", "Cantidad", "Subtotal"), show="headings"
        )
        self.tree_detalle.heading("Menú", text="Menú")
        self.tree_detalle.heading("Cantidad", text="Cantidad")
        self.tree_detalle.heading("Subtotal", text="Subtotal")
        self.tree_detalle.pack(expand=True, fill="both", padx=10, pady=10)

        # Botón para mostrar detalle
        ctk.CTkButton(frame_detalle, text="Ver Detalle", command=self.mostrar_detalle).pack(pady=10)

        self.actualizar_treeview()

    def actualizar_treeview(self):
        # Limpiar Treeview de pedidos
        for item in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(item)

        # Agregar los pedidos a la lista
        for pedido in self.lista_pedidos:
            self.tree_pedidos.insert("", "end", values=(pedido["cliente"], pedido["fecha"], f"${pedido['total']:.2f}"))

    def filtrar_pedidos(self, cliente):
        # Filtrar pedidos por cliente seleccionado
        self.tree_pedidos.delete(*self.tree_pedidos.get_children())

        for pedido in self.lista_pedidos:
            if pedido["cliente"] == cliente:
                self.tree_pedidos.insert("", "end", values=(pedido["cliente"], pedido["fecha"], f"${pedido['total']:.2f}"))

    def mostrar_detalle(self):
        # Obtener el pedido seleccionado
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Seleccione un pedido para ver los detalles.", icon="warning")
            return

        # Obtener datos del pedido
        cliente, fecha, total = self.tree_pedidos.item(seleccion[0])["values"]
        pedido = next((p for p in self.lista_pedidos if p["cliente"] == cliente and p["fecha"] == fecha), None)

        if not pedido:
            CTkMessagebox(title="Error", message="Pedido no encontrado.", icon="warning")
            return

        # Mostrar detalle
        self.tree_detalle.delete(*self.tree_detalle.get_children())
        for item in pedido["detalle"]:
            self.tree_detalle.insert(
                "", "end", values=(item["menu"], item["cantidad"], f"${item['subtotal']:.2f}")
            )

    def eliminar_pedido(self):
        # Obtener el pedido seleccionado
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Seleccione un pedido para eliminar.", icon="warning")
            return

        # Obtener datos del pedido
        cliente, fecha, total = self.tree_pedidos.item(seleccion[0])["values"]
        self.lista_pedidos = [
            p for p in self.lista_pedidos if not (p["cliente"] == cliente and p["fecha"] == fecha)
        ]
        self.actualizar_treeview()

        CTkMessagebox(title="Éxito", message="Pedido eliminado correctamente.", icon="info")
