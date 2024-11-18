import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import re

class IngredientesVentana(ctk.CTkFrame):
    def __init__(self, master, lista_ingredientes):
        super().__init__(master)
        self.lista_ingredientes = lista_ingredientes
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.configurar_ventana()

    def configurar_ventana(self):
        # Frame para ingresar ingredientes
        Window1 = ctk.CTkFrame(self)
        Window1.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self)
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
        boton_ingresar = ctk.CTkButton(Window1, text="Ingresar Ingrediente", command=self.ingresar_ingrediente)
        boton_ingresar.pack(pady=10)

        # Botón para eliminar ingrediente
        boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", command=self.eliminar_ingrediente)
        boton_eliminar.pack(pady=10)

        # Treeview para mostrar los ingredientes ingresados
        self.tree = ttk.Treeview(frame_treeview, columns=("Nombre", "Cantidad"), show="headings")
        self.tree.heading("Nombre", text="Nombre Ingrediente")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def ingresar_ingrediente(self):
        nombre = self.entry_nombre_ingred.get()
        cantidad = self.entry_cantidad_ingred.get()

        if not self.validar_ingrediente(nombre, cantidad):
            return

        # Buscar si el ingrediente ya existe
        for ing in self.lista_ingredientes:
            if ing["nombre"] == nombre:
                ing["cantidad"] += int(cantidad)
                self.actualizar_treeview()
                return

        # Si no existe, agregar nuevo
        self.lista_ingredientes.append({"nombre": nombre, "cantidad": int(cantidad)})
        self.actualizar_treeview()

    def validar_ingrediente(self, nombre, cantidad):
        if not re.match(r"^[a-zA-Z\s]+$", nombre):
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras.", icon="warning")
            return False
        if not cantidad.isdigit() or int(cantidad) <= 0:
            CTkMessagebox(title="Error de Validación", message="La cantidad debe ser un número positivo.", icon="warning")
            return False
        return True

    def actualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for ing in self.lista_ingredientes:
            self.tree.insert("", "end", values=(ing["nombre"], ing["cantidad"]))

    def eliminar_ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un ingrediente para eliminar.", icon="warning")
            return

        for item in seleccion:
            nombre = self.tree.item(item, "values")[0]
            self.lista_ingredientes = [ing for ing in self.lista_ingredientes if ing["nombre"] != nombre]
            self.tree.delete(item)

        self.actualizar_treeview()
