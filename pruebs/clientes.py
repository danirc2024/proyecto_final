import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox


class ClientesVentana(ctk.CTkFrame):
    def __init__(self, master, lista_clientes):
        super().__init__(master)
        self.lista_clientes = lista_clientes  # Lista de clientes registrados
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.configurar_ventana()

    def configurar_ventana(self):
        # Frame para formulario de cliente
        frame_formulario = ctk.CTkFrame(self)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame para lista de clientes
        frame_lista = ctk.CTkFrame(self)
        frame_lista.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario de cliente
        ctk.CTkLabel(frame_formulario, text="Nombre del Cliente:").pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        ctk.CTkLabel(frame_formulario, text="Correo Electrónico:").pack(pady=5)
        self.entry_correo = ctk.CTkEntry(frame_formulario)
        self.entry_correo.pack(pady=5)

        ctk.CTkButton(frame_formulario, text="Registrar Cliente", command=self.agregar_cliente).pack(pady=10)

        # Lista de clientes
        ctk.CTkLabel(frame_lista, text="Clientes Registrados:").pack(pady=5)
        self.tree = ttk.Treeview(frame_lista, columns=("Nombre", "Correo"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Correo", text="Correo Electrónico")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Botones de acciones
        ctk.CTkButton(frame_lista, text="Actualizar Cliente", command=self.actualizar_cliente).pack(pady=5)
        ctk.CTkButton(frame_lista, text="Eliminar Cliente", command=self.eliminar_cliente).pack(pady=5)

    def agregar_cliente(self):
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()

        # Validar entrada
        if not nombre or not correo:
            CTkMessagebox(title="Error", message="Complete todos los campos.", icon="warning")
            return

        if not self.validar_correo(correo):
            CTkMessagebox(title="Error", message="El correo ya está registrado.", icon="warning")
            return

        # Agregar cliente a la lista
        self.lista_clientes.append({"nombre": nombre, "correo": correo})
        self.actualizar_treeview()
        self.entry_nombre.delete(0, "end")
        self.entry_correo.delete(0, "end")

        CTkMessagebox(title="Éxito", message="Cliente registrado correctamente.", icon="info")

    def validar_correo(self, correo):
        # Verificar si el correo ya existe en la lista
        return not any(cliente["correo"] == correo for cliente in self.lista_clientes)

    def actualizar_treeview(self):
        # Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Rellenar Treeview
        for cliente in self.lista_clientes:
            self.tree.insert("", "end", values=(cliente["nombre"], cliente["correo"]))

    def actualizar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Seleccione un cliente para actualizar.", icon="warning")
            return

        # Obtener datos seleccionados
        item = self.tree.item(seleccion[0])
        nombre_anterior, correo_anterior = item["values"]

        # Actualizar datos
        nuevo_nombre = self.entry_nombre.get()
        nuevo_correo = self.entry_correo.get()

        if not nuevo_nombre or not nuevo_correo:
            CTkMessagebox(title="Error", message="Complete todos los campos.", icon="warning")
            return

        if nuevo_correo != correo_anterior and not self.validar_correo(nuevo_correo):
            CTkMessagebox(title="Error", message="El nuevo correo ya está registrado.", icon="warning")
            return

        # Actualizar en la lista
        for cliente in self.lista_clientes:
            if cliente["correo"] == correo_anterior:
                cliente["nombre"] = nuevo_nombre
                cliente["correo"] = nuevo_correo
                break

        self.actualizar_treeview()
        self.entry_nombre.delete(0, "end")
        self.entry_correo.delete(0, "end")

        CTkMessagebox(title="Éxito", message="Cliente actualizado correctamente.", icon="info")

    def eliminar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Seleccione un cliente para eliminar.", icon="warning")
            return

        # Obtener correo del cliente a eliminar
        correo = self.tree.item(seleccion[0])["values"][1]

        # Eliminar de la lista
        self.lista_clientes = [cliente for cliente in self.lista_clientes if cliente["correo"] != correo]
        self.actualizar_treeview()

        CTkMessagebox(title="Éxito", message="Cliente eliminado correctamente.", icon="info")
