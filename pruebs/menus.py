import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox


class MenusVentana(ctk.CTkFrame):
    def __init__(self, master, lista_ingredientes, lista_menus):
        super().__init__(master)
        self.lista_ingredientes = lista_ingredientes  # Ingredientes disponibles
        self.lista_menus = lista_menus  # Menús creados
        self.ingredientes_seleccionados = []  # Ingredientes seleccionados para un menú
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.configurar_ventana()

    def configurar_ventana(self):
        # Frame izquierdo para creación de menús
        frame_formulario = ctk.CTkFrame(self)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame derecho para lista de menús creados
        frame_lista = ctk.CTkFrame(self)
        frame_lista.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario para crear un menú
        ctk.CTkLabel(frame_formulario, text="Nombre del Menú:").pack(pady=5)
        self.entry_nombre_menu = ctk.CTkEntry(frame_formulario)
        self.entry_nombre_menu.pack(pady=5)

        ctk.CTkLabel(frame_formulario, text="Descripción:").pack(pady=5)
        self.entry_descripcion_menu = ctk.CTkEntry(frame_formulario)
        self.entry_descripcion_menu.pack(pady=5)

        ctk.CTkLabel(frame_formulario, text="Ingredientes Disponibles:").pack(pady=5)
        self.combo_ingredientes = ctk.CTkComboBox(
            frame_formulario,
            values=[f"{ing['nombre']} ({ing['cantidad']} disponibles)" for ing in self.lista_ingredientes],
        )
        self.combo_ingredientes.pack(pady=5)

        ctk.CTkLabel(frame_formulario, text="Cantidad Requerida:").pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.pack(pady=5)

        ctk.CTkButton(frame_formulario, text="Agregar Ingrediente", command=self.agregar_ingrediente).pack(pady=10)
        ctk.CTkButton(frame_formulario, text="Crear Menú", command=self.crear_menu).pack(pady=10)

        # Treeview para ingredientes seleccionados
        ctk.CTkLabel(frame_formulario, text="Ingredientes Seleccionados:").pack(pady=5)
        self.tree_ingredientes = ttk.Treeview(
            frame_formulario, columns=("Nombre", "Cantidad"), show="headings"
        )
        self.tree_ingredientes.heading("Nombre", text="Nombre")
        self.tree_ingredientes.heading("Cantidad", text="Cantidad")
        self.tree_ingredientes.pack(expand=True, fill="both", padx=10, pady=10)

        # Lista de menús creados
        ctk.CTkLabel(frame_lista, text="Menús Creados:").pack(pady=5)
        self.tree_menus = ttk.Treeview(
            frame_lista, columns=("Nombre", "Descripción"), show="headings"
        )
        self.tree_menus.heading("Nombre", text="Nombre")
        self.tree_menus.heading("Descripción", text="Descripción")
        self.tree_menus.pack(expand=True, fill="both", padx=10, pady=10)

    def agregar_ingrediente(self):
        # Obtener los valores seleccionados
        seleccion = self.combo_ingredientes.get()
        if not seleccion:
            CTkMessagebox(title="Error", message="Seleccione un ingrediente.", icon="warning")
            return

        nombre = seleccion.split(" (")[0]  # Extraer el nombre del ingrediente
        cantidad = self.entry_cantidad.get()

        if not cantidad.isdigit() or int(cantidad) <= 0:
            CTkMessagebox(title="Error", message="Ingrese una cantidad válida.", icon="warning")
            return

        cantidad = int(cantidad)

        # Verificar disponibilidad
        ingrediente = next((ing for ing in self.lista_ingredientes if ing["nombre"] == nombre), None)
        if not ingrediente or cantidad > ingrediente["cantidad"]:
            CTkMessagebox(title="Error", message="Cantidad no disponible.", icon="warning")
            return

        # Agregar ingrediente a la lista seleccionada
        self.ingredientes_seleccionados.append({"nombre": nombre, "cantidad": cantidad})
        self.actualizar_tree_ingredientes()

    def actualizar_tree_ingredientes(self):
        # Limpiar el Treeview
        for item in self.tree_ingredientes.get_children():
            self.tree_ingredientes.delete(item)

        # Agregar los ingredientes seleccionados
        for ing in self.ingredientes_seleccionados:
            self.tree_ingredientes.insert("", "end", values=(ing["nombre"], ing["cantidad"]))

    def crear_menu(self):
        nombre = self.entry_nombre_menu.get()
        descripcion = self.entry_descripcion_menu.get()

        if not nombre or not descripcion:
            CTkMessagebox(title="Error", message="Complete todos los campos del menú.", icon="warning")
            return

        if not self.ingredientes_seleccionados:
            CTkMessagebox(title="Error", message="Agregue al menos un ingrediente.", icon="warning")
            return

        # Guardar menú en la lista
        nuevo_menu = {
            "nombre": nombre,
            "descripcion": descripcion,
            "ingredientes": self.ingredientes_seleccionados.copy(),
        }
        self.lista_menus.append(nuevo_menu)

        # Actualizar Treeview de menús
        self.tree_menus.insert("", "end", values=(nombre, descripcion))

        # Limpiar formulario
        self.entry_nombre_menu.delete(0, "end")
        self.entry_descripcion_menu.delete(0, "end")
        self.ingredientes_seleccionados.clear()
        self.actualizar_tree_ingredientes()

        CTkMessagebox(title="Éxito", message="Menú creado correctamente.", icon="info")
