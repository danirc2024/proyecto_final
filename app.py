
import customtkinter as ctk
import tkinter as tk
from PIL import Image
from tkinter import messagebox,ttk
from CTkMessagebox import CTkMessagebox
from datetime import datetime
import re
from crud.cliente_crud import ClienteCRUD
from database import get_session, engine, Base
from crud.ingrediente_crud import IngredienteCRUD
from crud.pedidos_crud import PedidoCRUD
from crud.menu_crud import MenuCRUD

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


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
        self.configurar_pestana_pedidos()
        # Pestaña de ClienteS
        self.tab_clientes = self.tabview.add("Clientes")
        self.crear_formulario_cliente(self.tab_clientes)
        self.configurar_pestana1()
        self.configurar_pestana_menus()
        self.configurar_pestana_panel_compra()
        self.cargar_ingredientes()
        self.configurar_pestana_graficos()

    def configurar_pestana1(self):
        # Frame para ingresar ingredientes
        Window1 = ctk.CTkFrame(self.tab1)
        Window1.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario de ingredientes
        ctk.CTkLabel(Window1, text="Tipo de Ingrediente: ").pack(pady=5)
        self.combobox_tipo_ingrediente = ttk.Combobox(Window1, state="readonly")
        self.combobox_tipo_ingrediente["values"] = ["masa", "bebestible", "vegetal", "carne"]
        self.combobox_tipo_ingrediente.pack(pady=5)
        
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
        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white", command=self.eliminar_ingrediente)
        self.boton_eliminar.pack(pady=10)

        # Treeview para mostrar los ingredientes ingresados
        self.tree = ttk.Treeview(frame_treeview, columns=("ID", "Nombre", "Cantidad", "Tipo"), show="headings")
        self.tree.heading("ID", text="ID Ingrediente")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)


        # Botón para generar menú

    def configurar_pestana_menus(self):
        """Configura la pestaña de gestión de menús."""
        # Frame principal de la pestaña
        self.tab_menus = ctk.CTkFrame(self.tabview.add("Menús"))
        self.tab_menus.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame superior para el formulario de creación
        frame_formulario = ctk.CTkFrame(self.tab_menus)
        frame_formulario.pack(fill="x", padx=10, pady=10)

        # Nombre del menú
        ctk.CTkLabel(frame_formulario, text="Nombre del Menú").grid(row=0, column=0, padx=10, pady=5)
        self.entry_menu_nombre = ctk.CTkEntry(frame_formulario, placeholder_text="Ingrese el nombre del menú")
        self.entry_menu_nombre.grid(row=0, column=1, padx=10, pady=5)

        # Descripción del menú
        ctk.CTkLabel(frame_formulario, text="Descripción").grid(row=1, column=0, padx=10, pady=5)
        self.entry_menu_descripcion = ctk.CTkEntry(frame_formulario, placeholder_text="Ingrese una descripción")
        self.entry_menu_descripcion.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(frame_formulario, text="Precio").grid(row=3, column=0, padx=10, pady=5)
        self.entry_menu_precio = ctk.CTkEntry(frame_formulario, placeholder_text="Ingrese el precio del menú")
        self.entry_menu_precio.grid(row=3, column=1, padx=10, pady=5)

        # Selección de ingredientes
        ctk.CTkLabel(frame_formulario, text="Ingredientes Disponibles").grid(row=2, column=0, padx=10, pady=5)
        self.combobox_ingredientes = ttk.Combobox(frame_formulario, state="readonly")
        self.combobox_ingredientes.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame_formulario, text="Cantidad").grid(row=2, column=2, padx=10, pady=5)
        self.entry_cantidad_ingrediente = ctk.CTkEntry(frame_formulario, placeholder_text="Cantidad requerida")
        self.entry_cantidad_ingrediente.grid(row=2, column=3, padx=10, pady=5)

        # Botón para añadir ingredientes al menú
        ctk.CTkButton(frame_formulario, text="Añadir Ingrediente", command=self.agregar_ingrediente_menu).grid(row=2, column=4, padx=10, pady=5)

        # Frame para mostrar los ingredientes añadidos
        self.tree_ingredientes_menu = ttk.Treeview(self.tab_menus, columns=("Ingrediente", "Cantidad"), show="headings")
        self.tree_ingredientes_menu.heading("Ingrediente", text="Ingrediente")
        self.tree_ingredientes_menu.heading("Cantidad", text="Cantidad")
        self.tree_ingredientes_menu.pack(fill="both", padx=10, pady=10)

        # Botones para crear y eliminar menús
        frame_botones = ctk.CTkFrame(self.tab_menus)
        frame_botones.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(frame_botones, text="Crear Menú", command=self.crear_menu).pack(side="left", padx=5)
        ctk.CTkButton(frame_botones, text="Eliminar Menú", command=self.eliminar_menu).pack(side="left", padx=5)

        # Treeview para mostrar menús existentes
        self.tree_menus = ttk.Treeview(self.tab_menus, columns=("ID", "Nombre", "Descripción", "Precio"), show="headings")
        self.tree_menus.heading("ID", text="ID Menú")
        self.tree_menus.heading("Nombre", text="Nombre")
        self.tree_menus.heading("Descripción", text="Descripción")
        self.tree_menus.heading("Precio", text="Precio")
        self.tree_menus.pack(fill="both", padx=10, pady=10)

        # Cargar ingredientes disponibles y menús existentes al iniciar
        self.cargar_ingredientes_disponibles()
        self.cargar_menus()

    def validar_Ingrediente(self, nombre, cantidad, tipo):
        if not re.match(r"^[a-zA-Z\s]+$", nombre):
            CTkMessagebox(title="Error de Validación", message="El nombre del ingrediente debe contener solo letras y espacios.", icon="warning")
            return False
        if not cantidad.isdigit() or int(cantidad) <= 0:
            CTkMessagebox(title="Error de Validación", message="La cantidad debe contener solo números enteros positivos.", icon="warning")
            return False
        if tipo not in ["masa", "bebestible", "vegetal", "carne"]:
            CTkMessagebox(title="Error de Validación", message="Seleccione un tipo válido de ingrediente.", icon="warning")
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
        tipo = self.combobox_tipo_ingrediente.get()

        if not self.validar_Ingrediente(nombre, cantidad, tipo):
            return

        db = next(get_session())
        ingrediente = IngredienteCRUD.agregar_ingrediente(db, nombre, int(cantidad), tipo)
        db.close()

        if ingrediente:
            self.cargar_ingredientes()
            self.actualizar_combobox_ingredientes()
            CTkMessagebox(title="Éxito", message="Ingrediente agregado correctamente.")
        else:
            CTkMessagebox(title="Error", message="No se pudo agregar el ingrediente.")

    def crear_menu(self):
        """Crea un menú en la base de datos."""
        nombre = self.entry_menu_nombre.get()
        descripcion = self.entry_menu_descripcion.get()
        precio = self.entry_menu_precio.get()
        ingredientes_requeridos = self.obtener_ingredientes_requeridos()

        if not nombre or not descripcion or not precio or not ingredientes_requeridos:
            CTkMessagebox(title="Error", message="Por favor, completa todos los campos y selecciona ingredientes.", icon="warning")
            return

        if not precio.replace('.', '', 1).isdigit() or float(precio) <= 0:
            CTkMessagebox(title="Error", message="El precio debe ser un número positivo.", icon="warning")
            return

        db = next(get_session())
        menu = MenuCRUD.crear_menu(db, nombre, descripcion, ingredientes_requeridos, float(precio))
        db.close()

        if menu:
            CTkMessagebox(title="Éxito", message="Menú creado correctamente.")
            self.actualizar_combobox_menus()
            self.cargar_menus()  # Actualizar la vista
        else:
            CTkMessagebox(title="Error", message="No se pudo crear el menú. Verifica los ingredientes disponibles.")


    def cargar_ingredientes(self):
        """Carga los ingredientes desde la base de datos en el Treeview."""
        db = next(get_session())
        ingredientes = IngredienteCRUD.leer_ingredientes(db)
        db.close()

        # Limpiar el Treeview antes de recargar
        self.tree.delete(*self.tree.get_children())

        # Insertar ingredientes en el Treeview
        for ingrediente in ingredientes:
            self.tree.insert("", "end", values=(ingrediente.ID_ingrediente, ingrediente.Nombre, ingrediente.Cantidad, ingrediente.Tipo))

    def eliminar_ingrediente(self):
        """Elimina el ingrediente seleccionado en el Treeview."""
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor, selecciona un ingrediente para eliminar.", icon="warning")
            return

        id_ingrediente = self.tree.item(seleccion[0], "values")[0]  # ID del ingrediente
        db = next(get_session())
        ingrediente_eliminado = IngredienteCRUD.eliminar_ingrediente(db, id_ingrediente)
        db.close()

        if ingrediente_eliminado:
            CTkMessagebox(title="Éxito", message="Ingrediente eliminado correctamente.")
            self.cargar_ingredientes()  # Recargar el Treeview
        else:
            CTkMessagebox(title="Error", message="No se pudo eliminar el ingrediente.")
            
    def cargar_ingredientes_disponibles(self):
        """Carga los ingredientes disponibles en la base de datos al combobox."""
        db = next(get_session())
        ingredientes = IngredienteCRUD.leer_ingredientes(db)
        db.close()

        self.combobox_ingredientes["values"] = [ingrediente.Nombre for ingrediente in ingredientes]
    
    def agregar_ingrediente_menu(self):
        """Añade un ingrediente al menú temporalmente (Treeview de ingredientes del menú)."""
        ingrediente = self.combobox_ingredientes.get()
        cantidad = self.entry_cantidad_ingrediente.get()

        if not ingrediente or not cantidad.isdigit() or int(cantidad) <= 0:
            CTkMessagebox(title="Error", message="Seleccione un ingrediente y asegúrese de que la cantidad sea válida.", icon="warning")
            return

        self.tree_ingredientes_menu.insert("", "end", values=(ingrediente, cantidad))
        self.entry_cantidad_ingrediente.delete(0, "end")


    def obtener_ingredientes_requeridos(self):
        """Obtiene la lista de ingredientes y cantidades seleccionados para el menú."""
        ingredientes = []
        for item in self.tree_ingredientes_menu.get_children():
            valores = self.tree_ingredientes_menu.item(item, "values")
            ingredientes.append({"nombre": valores[0], "cantidad": int(valores[1])})
        return ingredientes

    def crear_formulario_cliente(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de clientes."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre = ctk.CTkEntry(frame_superior)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Email").grid(row=0, column=2, pady=10, padx=10)
        self.entry_email = ctk.CTkEntry(frame_superior)
        self.entry_email.grid(row=0, column=3, pady=10, padx=10)

        # Botones alineados horizontalmente en el frame superior
        self.btn_crear_cliente = ctk.CTkButton(frame_superior, text="Crear Cliente", command=self.crear_cliente)
        self.btn_crear_cliente.grid(row=1, column=0, pady=10, padx=10)

        self.btn_actualizar_cliente = ctk.CTkButton(frame_superior, text="Actualizar Cliente", command=self.actualizar_cliente)
        self.btn_actualizar_cliente.grid(row=1, column=1, pady=10, padx=10)

        self.btn_eliminar_cliente = ctk.CTkButton(frame_superior, text="Eliminar Cliente", command=self.eliminar_cliente)
        self.btn_eliminar_cliente.grid(row=1, column=2, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los clientes
        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("Email", "Nombre"), show="headings")
        self.treeview_clientes.heading("Email", text="Email")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)

        self.cargar_clientes()

    # Método para actualizar los correos electrónicos en el Combobox
    # def actualizar_emails_combobox(self):
    #     """Llena el Combobox con los emails de los clientes."""
    #     db = next(get_session())
    #     emails = [cliente.email for cliente in ClienteCRUD.leer_clientes(db)]
    #     self.combobox_cliente_email['values'] = emails
    #     db.close()

    # Métodos CRUD para Clientes
    def cargar_clientes(self):
        db = next(get_session())
        self.treeview_clientes.delete(*self.treeview_clientes.get_children())
        clientes = ClienteCRUD.leer_clientes(db)
        for cliente in clientes:
            self.treeview_clientes.insert("", "end", values=(cliente.email, cliente.nombre))
        db.close()

    def crear_cliente(self):
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        if nombre and email :
            db = next(get_session())
            cliente = ClienteCRUD.crear_cliente(db, nombre, email)
            if cliente:
                messagebox.showinfo("Éxito", "Cliente creado correctamente.")
                self.actualizar_combobox_clientes()
                self.cargar_clientes()
                #self.actualizar_emails_combobox()   Actualizar el Combobox con el nuevo email
            else:
                messagebox.showwarning("Error", "El cliente ya existe.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")

    def actualizar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un cliente.")
            return
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()

        if not nombre.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un nombre.")
            return
        if not email.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un email.")
            return 
        
        email_viejo = self.treeview_clientes.item(selected_item)["values"][0]
        nombre = self.entry_nombre.get()
        if nombre:
            db = next(get_session())
            cliente_actualizado = ClienteCRUD.actualizar_cliente(db, email_viejo, nombre,email)
            if cliente_actualizado:
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
                self.cargar_clientes()
            else:
                messagebox.showwarning("Error", "No se pudo actualizar el cliente.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese el nombre.")

    def eliminar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un cliente.")
            return
        email = self.treeview_clientes.item(selected_item)["values"][0]
        db = next(get_session())
        ClienteCRUD.borrar_cliente(db, email)
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        self.cargar_clientes()
        #self.actualizar_emails_combobox()   Actualizar el Combobox después de eliminar
        db.close()
        
        
    
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

    def eliminar_menu(self):
        seleccion = self.tree_menus.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor, selecciona un menú para eliminar.", icon="warning")
            return

        id_menu = self.tree_menus.item(seleccion[0], "values")[0]
        db = next(get_session())
        menu_eliminado = MenuCRUD.eliminar_menu(db, id_menu)
        db.close()

        if menu_eliminado:
            CTkMessagebox(title="Éxito", message="Menú eliminado correctamente.")
            self.cargar_menus()  # Actualizar la vista
        else:
            CTkMessagebox(title="Error", message="No se pudo eliminar el menú.")
            
    def cargar_menus(self):
        """Carga los menús desde la base de datos en el Treeview."""
        db = next(get_session())
        menus = MenuCRUD.leer_menus(db)
        db.close()

        self.tree_menus.delete(*self.tree_menus.get_children())

        for menu in menus:
            self.tree_menus.insert("", "end", values=(menu.ID_menu, menu.Nombre, menu.Descripcion, f"${menu.Precio}"))


    def calcular_total(self):
        menu_seleccionado = self.combobox_menus.get()
        cantidad = self.entry_cantidad.get()

        if not menu_seleccionado or not cantidad.isdigit() or int(cantidad) <= 0:
            CTkMessagebox(title="Error", message="Selecciona un menú y una cantidad válida.", icon="warning")
            return

        db = next(get_session())
        menu = MenuCRUD.leer_menu_por_nombre(db, menu_seleccionado)
        db.close()

        if menu:
            total = int(cantidad) * menu.Precio
            self.label_total.configure(text=f"Total: ${total:.2f}")
        else:
            CTkMessagebox(title="Error", message="No se encontró el menú seleccionado.", icon="warning")



    #utiliza el ReportLab para generar la boleta, si no lo tienen es una extencion [ pip install ReportLab ]
        
    def configurar_pestana_pedidos(self):
        # Crear un Frame para contener la tabla y los botones
        frame_pedidos = ctk.CTkFrame(self.tabview.add("Pedidos"))
        frame_pedidos.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview para mostrar los pedidos
        self.treeview_pedidos = ttk.Treeview(frame_pedidos, columns=("ID", "Correo Cliente", "Menú", "Cantidad", "Total", "Fecha"), show="headings")
        self.treeview_pedidos.heading("ID", text="ID Pedido")
        self.treeview_pedidos.heading("Correo Cliente", text="Correo Cliente")
        self.treeview_pedidos.heading("Menú", text="Menú")
        self.treeview_pedidos.heading("Cantidad", text="Cantidad")
        self.treeview_pedidos.heading("Total", text="Total")
        self.treeview_pedidos.heading("Fecha", text="Fecha")
        self.treeview_pedidos.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones para gestionar pedidos
        frame_botones = ctk.CTkFrame(frame_pedidos)
        frame_botones.pack(fill="x", pady=10)

        ctk.CTkButton(frame_botones, text="Cargar Pedidos", command=self.cargar_pedidos).pack(side="left", padx=5)
        ctk.CTkButton(frame_botones, text="Eliminar Pedido", command=self.eliminar_pedido).pack(side="left", padx=5)
        self.cargar_pedidos()

    def cargar_pedidos(self):
        """Carga los pedidos en el Treeview desde la base de datos."""
        db = next(get_session())
        pedidos = PedidoCRUD.leer_pedidos(db)
        db.close()

        self.treeview_pedidos.delete(*self.treeview_pedidos.get_children())  # Limpiar el Treeview

        for pedido in pedidos:
            self.treeview_pedidos.insert("", "end", values=(
                pedido.ID_pedido,
                pedido.Correo_cliente,
                pedido.Menu,
                pedido.Cantidad,
                f"${pedido.Total:.2f}",
                pedido.Fecha.strftime("%d-%m-%y %H:%M:%S")
            ))


    def eliminar_pedido(self):
        """Elimina el pedido seleccionado en el Treeview."""
        seleccion = self.treeview_pedidos.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor, selecciona un pedido para eliminar.", icon="warning")
            return

        id_pedido = self.treeview_pedidos.item(seleccion[0], "values")[0]
        db = next(get_session())
        pedido_eliminado = PedidoCRUD.borrar_pedido(db, id_pedido)
        db.close()

        if pedido_eliminado:
            CTkMessagebox(title="Éxito", message="Pedido eliminado correctamente.")
            self.cargar_pedidos()  # Recargar el Treeview
        else:
            CTkMessagebox(title="Error", message="No se pudo eliminar el pedido.")

        
    
    def configurar_pestana_panel_compra(self):
        """Configura la pestaña de Panel de Compra."""
        # Crear el Frame principal de la pestaña
        self.tab_panel_compra = ctk.CTkFrame(self.tabview.add("Panel de Compra"))
        self.tab_panel_compra.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame superior para seleccionar cliente y menú
        frame_seleccion = ctk.CTkFrame(self.tab_panel_compra)
        frame_seleccion.pack(fill="x", padx=10, pady=10)

        # Selección de cliente
        ctk.CTkLabel(frame_seleccion, text="Cliente").grid(row=0, column=0, padx=10, pady=5)
        self.combobox_clientes = ttk.Combobox(frame_seleccion, state="readonly")
        self.combobox_clientes.grid(row=0, column=1, padx=10, pady=5)

        # Selección de menú
        ctk.CTkLabel(frame_seleccion, text="Menú").grid(row=1, column=0, padx=10, pady=5)
        self.combobox_menus = ttk.Combobox(frame_seleccion, state="readonly")
        self.combobox_menus.grid(row=1, column=1, padx=10, pady=5)

        # Selección de cantidad
        ctk.CTkLabel(frame_seleccion, text="Cantidad").grid(row=2, column=0, padx=10, pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_seleccion)
        self.entry_cantidad.grid(row=2, column=1, padx=10, pady=5)

        # Botón para calcular el total
        ctk.CTkButton(frame_seleccion, text="Calcular Total", command=self.calcular_total).grid(row=3, column=0, padx=10, pady=5)

        # Mostrar el total
        self.label_total = ctk.CTkLabel(frame_seleccion, text="Total: $0.00")
        self.label_total.grid(row=3, column=1, padx=10, pady=5)

        # Botón para registrar el pedido
        ctk.CTkButton(self.tab_panel_compra, text="Registrar Pedido", command=self.registrar_pedido).pack(pady=10)
        ctk.CTkButton(self.tab_panel_compra, text="Generar Boleta", command=self.generar_boleta).pack(pady=10)


        # Treeview para mostrar pedidos
        self.tree_pedidos = ttk.Treeview(self.tab_panel_compra, columns=("ID", "Cliente", "Menú", "Cantidad", "Total", "Fecha"), show="headings")
        self.tree_pedidos.heading("ID", text="ID Pedido")
        self.tree_pedidos.heading("Cliente", text="Cliente")
        self.tree_pedidos.heading("Menú", text="Menú")
        self.tree_pedidos.heading("Cantidad", text="Cantidad")
        self.tree_pedidos.heading("Total", text="Total")
        self.tree_pedidos.heading("Fecha", text="Fecha")
        self.tree_pedidos.pack(fill="both", padx=10, pady=10)

        # Cargar datos iniciales
        self.cargar_clientesotes()
        self.cargar_menusotes()
        self.cargar_pedidotes()
    


    def registrar_pedido(self):
        cliente = self.combobox_clientes.get()
        menu = self.combobox_menus.get()
        cantidad = self.entry_cantidad.get()
        total_text = self.label_total.cget("text").replace("Total: $", "")

        if not cliente or not menu or not cantidad.isdigit() or float(total_text) <= 0:
            CTkMessagebox(title="Error", message="Completa todos los campos correctamente.", icon="warning")
            return

        db = next(get_session())
        pedido = PedidoCRUD.crear_pedido(db, cliente, menu, int(cantidad), float(total_text))
        db.close()

        if pedido:
            CTkMessagebox(title="Éxito", message="Pedido registrado correctamente.")
            self.cargar_pedidos()
        else:
            CTkMessagebox(title="Error", message="No se pudo registrar el pedido.")
        self.cargar_pedidotes()
            
    def cargar_clientesotes(self):
        db = next(get_session())
        clientes = ClienteCRUD.leer_clientes(db)
        db.close()
        self.combobox_clientes["values"] = [cliente.email for cliente in clientes]

    def cargar_menusotes(self):
        db = next(get_session())
        menus = MenuCRUD.leer_menus(db)
        db.close()
        self.combobox_menus["values"] = [menu.Nombre for menu in menus]

    def cargar_pedidotes(self):
        db = next(get_session())
        pedidos = PedidoCRUD.leer_pedidos(db)
        db.close()
        self.tree_pedidos.delete(*self.tree_pedidos.get_children())

        for pedido in pedidos:
            self.tree_pedidos.insert("", "end", values=(pedido.ID_pedido, pedido.Correo_cliente, pedido.Menu, pedido.Cantidad, f"${pedido.Total:.2f}", pedido.Fecha.strftime("%Y-%m-%d %H:%M:%S")))
 
    def actualizar_combobox_ingredientes(self):
        """Recarga los ingredientes disponibles en el Combobox."""
        db = next(get_session())
        ingredientes = IngredienteCRUD.leer_ingredientes(db)
        db.close()

        self.combobox_ingredientes["values"] = [ingrediente.Nombre for ingrediente in ingredientes]

 
    def actualizar_combobox_menus(self):
        """Recarga los menús disponibles en el Combobox."""
        db = next(get_session())
        menus = MenuCRUD.leer_menus(db)
        db.close()
        self.combobox_menus["values"] = [menu.Nombre for menu in menus]
    
    def actualizar_combobox_clientes(self):
        db = next(get_session())
        clientes = ClienteCRUD.leer_clientes(db)
        db.close()

        self.combobox_clientes["values"] = [cliente.email for cliente in clientes]
        
    def generar_boleta(self):
        """Genera una boleta en PDF para el pedido seleccionado en el Treeview."""
        # Obtener el pedido seleccionado
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor, selecciona un pedido para generar la boleta.", icon="warning")
            return
        valores = self.treeview_pedidos.item(seleccion[0], "values")  # Cambiar a [0]
        ID, correo_cliente, menu, cantidad, total, fecha = valores


        # Crear el documento PDF
        nombre_archivo = "boleta.pdf"
        pdf = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        elementos = []
        estilos = getSampleStyleSheet()

        # Título de la boleta
        titulo = Paragraph("Boleta de Pedido", estilos['Title'])
        elementos.append(titulo)
        elementos.append(Spacer(1, 12))  # Espacio después del título

        # Información del cliente y la fecha
        info_cliente = Paragraph(f"Cliente: {correo_cliente}", estilos['Normal'])
        elementos.append(info_cliente)
        elementos.append(Spacer(1, 12))  # Espacio después del cliente

        fecha_pedido = Paragraph(f"Fecha: {fecha}", estilos['Normal'])
        elementos.append(fecha_pedido)
        elementos.append(Spacer(1, 12))  # Espacio después de la fecha

        # Tabla del pedido
        datos = [["Menú", "Cantidad", "Precio Unitario", "Total"]]
        precio_unitario = float(total.strip('$')) / int(cantidad)  # Convertir texto de total a float
        datos.append([menu, cantidad, f"${precio_unitario:.2f}", total])

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

