import customtkinter as ctk
from tkinter import ttk

class MenusVentana(ctk.CTkFrame):
    def __init__(self, master, lista_ingredientes, lista_pedido):
        super().__init__(master)
        self.lista_ingredientes = lista_ingredientes
        self.lista_pedido = lista_pedido
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.configurar_ventana()

    def configurar_ventana(self):
        # Frame para los menús
        self.tarjetas_frame = ctk.CTkFrame(self)
        self.tarjetas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para el pedido
        self.pedido_frame = ctk.CTkFrame(self, fg_color="#3C3C3C")
        self.pedido_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview del pedido
        self.tree_pedido = ttk.Treeview(self.pedido_frame, columns=("Nombre", "Cantidad", "Precio"), show="headings")
        self.tree_pedido.heading("Nombre", text="Nombre del Menú")
        self.tree_pedido.heading("Cantidad", text="Cantidad")
        self.tree_pedido.heading("Precio", text="Precio Unitario")
        self.tree_pedido.pack(expand=True, fill="both", padx=10, pady=10)

        # Total y botones
        self.total_label = ctk.CTkLabel(self.pedido_frame, text="Total: $0.00")
        self.total_label.pack(side="left", padx=10, pady=10)

        boton_eliminar_menu = ctk.CTkButton(self.pedido_frame, text="Eliminar Menú", command=self.eliminar_menu)
        boton_eliminar_menu.pack(side="left", padx=10, pady=10)

    def eliminar_menu(self):
        seleccion = self.tree_pedido.selection()
        if not seleccion:
            return

        for item in seleccion:
            self.tree_pedido.delete(item)
