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

from frames.customers_frame import create_customers_frame
from frames.add_customer_frame import create_add_customer_frame
from frames.users_frame import create_users_frame
from frames.add_user_frame import create_add_user_frame

class App(ctk.CTk):
    def __init__(self,user):
        super().__init__()
        self.title("Product Management")
        self.geometry("1000x700")
        print('User', user)
        
        # Create a container for the navbar
        self.navbar = ctk.CTkFrame(self, fg_color="#333",corner_radius=0)
        self.navbar.pack(side="top", fill="x")
        
        # Create a container for all pages
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.pack(fill="both", expand=True)

        # Store pages (frames) in a dictionary
        self.frames = {}

        # Initialize the navigation bar
        self.create_navbar()

        # Initialize and show the home page
        self.init_frames(user)
        self.show_frame("Products")

    def init_frames(self,user=None):
        """Initialize and store all frames/pages."""
        self.frames["Home"] = create_home_frame(self.container)
        self.frames["Products"] = create_products_frame(self.container,user)
        self.frames["Categories"] = create_categories_frame(self.container)
        self.frames["AddProduct"] = create_add_product_frame(self.container)
        self.frames["AddProductCategory"] = create_add_category_frame(self.container)
        self.frames["AddSupplier"] = create_add_supplier_frame(self.container)
        self.frames["Suppliers"] = create_suppliers_frame(self.container)
        self.frames["Inventory"] = create_inventory_frame(self.container)
        self.frames["Customers"] = create_customers_frame(self.container)
        self.frames["AddCustomer"] = create_add_customer_frame(self.container)
        self.frames["Users"] = create_users_frame(self.container)
        self.frames["AddUser"] = create_add_user_frame(self.container)  
        
        # Pack all frames but hide them initially
        for frame in self.frames.values():
            frame.pack(fill="both", expand=True)
            frame.pack_forget()


    def show_frame(self, frame_name):
        """Switch to the frame with the given name."""
        for name, frame in self.frames.items():
            # print(name)
            if name == frame_name:
                if name == "AddProduct" or name == "AddProductCategory" or name == "AddSupplier" or name == "AddCustomer":
                    frame.pack(fill="both", expand=True,padx=400,pady=10,ipady=100)
                elif name == "AddUser" :
                    frame.pack(fill="x", expand=True, padx=400, pady=10, ipady=50)
                else:
                    frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()



    def create_navbar(self):
        """Create a navigation bar for switching between pages."""
        button_style = {"font": ("Arial", 16), "fg_color": "#333", "text_color": "white", "hover_color": "#333"}
        # logo button
        inventory_btn = ctk.CTkButton(self.navbar, text="Easy",  **button_style,width=140,anchor='w')
        inventory_btn.pack(side="right", padx=1, pady=5)
                
        # Home button
        home_btn = ctk.CTkButton(self.navbar, text="الرئيسية", command=lambda: self.show_frame("Home"), **button_style,width=90)
        home_btn.pack(side="right", padx=1, pady=5)

        # Products dropdown
        # products_btn = ctk.CTkButton(self.navbar, text="المنتجات", **button_style,width=90)
        # products_btn.pack(side="right", padx=1, pady=5)
        products_dropdown = self.create_dropdown(self.navbar,'المنتجات', [
            ("عرض المنتجات", lambda: self.show_frame("Products")),
            ("إضافة منتج", lambda: self.show_frame("AddProduct"))
        ])
        products_dropdown.pack(side="right", padx=1, pady=5)

        # Categories dropdown        
        # products_btn = ctk.CTkButton(self.navbar, text="الاقسام", **button_style,width=90)
        # products_btn.pack(side="right", padx=1, pady=5)
        categories_dropdown = self.create_dropdown(self.navbar,'الاقسام', [
            ("عرض الفئات", lambda: self.show_frame("Categories")),
            ("إضافة فئة", lambda: self.show_frame("AddProductCategory"))
        ])
        categories_dropdown.pack(side="right", padx=1, pady=5)


        # Inventory button
        inventory_btn = ctk.CTkButton(self.navbar, text="المخزون", command=lambda: self.show_frame("Inventory"), **button_style,width=50)
        inventory_btn.pack(side="right", padx=1, pady=5)
        
        # Inventory button
        inventory_btn = ctk.CTkButton(self.navbar, text="المبيعات",  **button_style,width=50)
        inventory_btn.pack(side="right", padx=1, pady=5)


        # Customers dropdown
        # products_btn = ctk.CTkButton(self.navbar, text="العملاء", **button_style,width=90)
        # products_btn.pack(side="right", padx=1, pady=5)
        customer_dropdown = self.create_dropdown(self.navbar,'العملاء', [
            ("عرض العملاء", lambda: self.show_frame("Customers")),
            ("إضافة عميل", lambda: self.show_frame("AddCustomer"))
        ])
        customer_dropdown.pack(side="right", padx=1, pady=5)
        
        # Suppliers dropdown
        # products_btn = ctk.CTkButton(self.navbar, text="الموردين", **button_style,width=90)
        # products_btn.pack(side="right", padx=1, pady=5)
        supplier_dropdown = self.create_dropdown(self.navbar,'الموردين', [
            (" قائمة الموردين", lambda: self.show_frame("Suppliers")),
            ("إضافة مورد", lambda: self.show_frame("AddSupplier"))
        ])
        supplier_dropdown.pack(side="right", padx=1, pady=5)
        
        # Users dropdown
        user_dropdown = self.create_dropdown(self.navbar,'المستخدمين', [
            ("عرض المستخدمين", lambda: self.show_frame("Users")),
            ("إضافة مستخدم", lambda: self.show_frame("AddUser"))
        ])
        user_dropdown.pack(side="right", padx=1, pady=5)
        
        # settings
        settings_btn = ctk.CTkButton(self.navbar, text="الاعدادات",  **button_style,width=60)
        settings_btn.pack(side="right", padx=1, pady=5)
        
        
        # Logout button
        logout_btn = ctk.CTkButton(self.navbar, text="تسجيل الخروج", command=lambda: logout(self), **button_style,width=90)
        logout_btn.pack(side="left", padx=1, pady=5)
        def logout(self):
            """
            Logout the user and show the login window while closing the current application window.
            """
            import login  # Import the login module
            self.destroy()  # Close the current window
            login.launch_login_window()  # Assuming the login script has a main() function to launch the login window


    def create_dropdown(self, parent, name,options):
        default = tk.StringVar(value=name)
        dropdown = ctk.CTkOptionMenu(parent, 
            text_color="#fff",dropdown_fg_color="#fff",fg_color='#333',
            font=("Arial", 14),dropdown_font=("Arial", 14),width=90,
            button_color="#333",dropdown_hover_color="#fff",button_hover_color='#333',
            values=[option[0] for option in options],anchor='e',
            variable=default,
            command=lambda value: options[[option[0] for option in options].index(value)][1]())
        return dropdown

# if __name__ == "__main__":
# app = App()
# app.mainloop()

def launch_main_window(user):
    app = App(user=user)
    print("Launching", user)
    app.mainloop()

