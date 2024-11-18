import customtkinter as ctk
from ingredientes import IngredientesVentana
from menus import MenusVentana
from clientes import ClientesVentana
from pedidos import PedidosVentana

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante")
        self.geometry("1000x600")

        self.lista_ingredientes = []
        self.lista_pedido = []
        self.lista_clientes = []
        self.lista_pedidos = []


        # Crear pestañas
        tabview = ctk.CTkTabview(self, width=600, height=500)
        tabview.pack(padx=20, pady=20)
        
        tab_clientes = tabview.add("Clientes")
        tab_pedidos = tabview.add("Pedidos")
        tab_ingredientes = tabview.add("Ingredientes")
        tab_menus = tabview.add("Menús")
        
        ClientesVentana(tab_clientes, self.lista_clientes)
        PedidosVentana(tab_pedidos, self.lista_pedidos, self.lista_clientes)
        IngredientesVentana(tab_ingredientes, self.lista_ingredientes)
        MenusVentana(tab_menus, self.lista_ingredientes, self.lista_pedido)

if __name__ == "__main__":
    app = App()
    app.mainloop()
