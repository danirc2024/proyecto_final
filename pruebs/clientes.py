import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

class ClientesVentana(ctk.CTkFrame):
    def __init__(self, master, lista_clientes):
        super().__init__(master)
        self.lista_clientes = lista_clientes
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.configurar_ventana()

    def configurar_ventana(self):
        # Frame para clientes
        frame_formulario = ctk.CTkFrame(self)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_lista = ctk.CTkFrame(self)
        frame_lista.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        

        # Formulario de cliente
        ctk.CTkLabel(frame_formulario, text="Nombre Cliente: ").pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        ctk.CTkLabel(frame_formulario, text="Correo Electrónico: ").pack(pady=5)
        self.entry_correo = ctk.CTkEntry(frame_formulario)
        self.entry_correo.pack(pady=5)

        ctk.CTkButton(frame_formulario, text="Agregar Cliente", command=self.agregar_cliente).pack(pady=10)
        ctk.CTkButton(frame_formulario, text="Eliminar Cliente", command=self.eliminar_cliente).pack(pady=10)

        # Lista de clientes
        self.tree = ttk.Treeview(frame_lista, columns=("Nombre", "Correo"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Correo", text="Correo Electrónico")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def agregar_cliente(self):
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()

        # Validar que no haya duplicados
        if any(cliente["correo"] == correo for cliente in self.lista_clientes):
            CTkMessagebox(title="Error", message="El correo ya está registrado.", icon="warning")
            return

        self.lista_clientes.append({"nombre": nombre, "correo": correo})
        self.actualizar_lista()

    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for cliente in self.lista_clientes:
            self.tree.insert("", "end", values=(cliente["nombre"], cliente["correo"]))
            
    def eliminar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un cliente para eliminar.", icon="warning")
            return

        for item in seleccion:
            nombre = self.tree.item(item, "values")[0]
            self.lista_clientes = [ing for ing in self.lista_clientes if ing["nombre"] != nombre]
            self.tree.delete(item)

        self.actualizar_lista()
