import tkinter as tk
import customtkinter as ctk
from tkinter import Menu
from frames.home_frame import create_home_frame
from frames.products_frame import create_products_frame
from frames.categories_frame import create_categories_frame
from frames.add_product_frame import create_add_product_frame
from frames.add_category_frame import create_add_category_frame
from frames.add_supplier_frame import create_add_supplier_frame

from frames.suppliers_frame import create_suppliers_frame
from frames.inventory_frame import create_inventory_frame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Product Management")
        self.geometry("1200x800")
        # Create a container for all pages
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.pack(fill="both", expand=True)

        # Store pages (frames) in a dictionary
        self.frames = {}

        # Initialize the navigation bar
        self.create_navbar()

        # Initialize and show the home page
        self.init_frames()
        self.show_frame("Home")

    def init_frames(self):
        """Initialize and store all frames/pages."""
        self.frames["Home"] = create_home_frame(self.container)
        self.frames["Products"] = create_products_frame(self.container)
        self.frames["Categories"] = create_categories_frame(self.container)
        self.frames["AddProduct"] = create_add_product_frame(self.container)
        self.frames["AddProductCategory"] = create_add_category_frame(self.container)
        self.frames["AddSupplier"] = create_add_supplier_frame(self.container)
        self.frames["Suppliers"] = create_suppliers_frame(self.container)
        self.frames["Inventory"] = create_inventory_frame(self.container)

        # Pack all frames but hide them initially
        for frame in self.frames.values():
            frame.pack(fill="both", expand=True)
            frame.pack_forget()

    def show_frame(self, frame_name):
        """Switch to the frame with the given name."""
        for name, frame in self.frames.items():
            # print(name)
            if name == frame_name:
                if name == "AddProduct" or name == "AddProductCategory" or name == "AddSupplier" :
                    frame.pack(fill="both", expand=True,padx=400,pady=10,ipady=100)
                else:
                    frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

    def create_navbar(self):
        """Create a navigation bar for switching between pages."""
        # Create a top-level menu
        nav_style = {"font": ("Arial", 28), "bg": "#333", "fg": "white"}
        navbar = Menu(self, tearoff=0, **nav_style)
        self.config(menu=navbar)

        # Styling parameters
        submenu_style = {"font": ("Arial", 15), "activebackground": "#fff", "bg": "#fff", "fg": "black",
                        "activeborderwidth": 3,"activeforeground": "black"}

        # Define individual menus
        empty_menu = Menu(navbar, tearoff=0, **submenu_style)
        navbar.add_cascade(label="                                                                                                                                                                                                                                                                                                     ", menu=empty_menu)
        # empty_menu.add_command(label="                              ", command=lambda: self.show_frame("Home"))

        inventory_menu = Menu(navbar, tearoff=0, **submenu_style)
        navbar.add_cascade(label="المخزون", menu=inventory_menu)
        inventory_menu.add_command(label="إدارة المخزون", command=lambda: self.show_frame("Inventory"))        


        suppliers_menu = Menu(navbar, tearoff=0, **submenu_style)
        navbar.add_cascade(label="الموردين", menu=suppliers_menu)
        suppliers_menu.add_command(label="عرض الموردين", command=lambda: self.show_frame("Suppliers"))
        suppliers_menu.add_command(label="إضافة مورد", command=lambda: self.show_frame("AddSupplier"))

        categories_menu = Menu(navbar, tearoff=0, **submenu_style)
        navbar.add_cascade(label="الفئات", menu=categories_menu)
        categories_menu.add_command(label="عرض الفئات", command=lambda: self.show_frame("Categories"))
        categories_menu.add_command(label="إضافة فئة", command=lambda: self.show_frame("AddProductCategory"))

        products_menu = Menu(navbar, tearoff=0, **submenu_style)
        navbar.add_cascade(label="المنتجات", menu=products_menu)
        products_menu.add_command(label="عرض المنتجات", command=lambda: self.show_frame("Products"))
        products_menu.add_command(label="إضافة منتج", command=lambda: self.show_frame("AddProduct"))

        home_menu = Menu(navbar, tearoff=0, **submenu_style, )
        navbar.add_cascade(label="الرئيسية", menu=home_menu)
        home_menu.add_command(label="الرئيسية", command=lambda: self.show_frame("Home"))


        # Align the items to the right in the menu bar
        # self.tk.call("tk", "menu", "configure", navbar, "-postcommand", f"menubar_right {str(navbar)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
