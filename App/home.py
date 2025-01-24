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

from frames.invoices_frame import create_add_sale_frame, create_sales_frame
from frames.invoice_details_frame import frame_principal
# from frames.login_frame import create_login_frame
from tkinter import messagebox
import pymysql
import bcrypt
import os
def connect_db():
    try:
        global connect
        global my_cursor
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        print('Connected to the database')
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
# === Fonction de Connexion ===
justify = 'left'
entry_widgets = []  # List to store all entry widgets
label_widgets = []  # List to store all entry widgets

def direction(dir):
    global justify
    if dir == 'Ar':
        justify = 'right'
    else:
        justify = 'left'
    update_entry_justification()

def update_entry_justification():
    for entry in entry_widgets:
        if entry.winfo_exists():
            entry.configure(justify=justify)

# for entries
def create_entry(parent,width=400):
    entry = ctk.CTkEntry(parent, justify=justify,font=("Arial", 14), fg_color='#fff',
                         border_width=1, border_color='#ddd', corner_radius=8, width=width)
    entry.pack(ipady=10 , padx=20)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text,wid=200):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text, width=wid)
    label_widgets.append(label)
    return label

logged = False
user_logged = None
class App(ctk.CTk):
    def __init__(self, user=None):
        super().__init__()
        self.title("Product Management")
        self.geometry("1000x700")

        # Create a container for the navbar
        self.navbar1 = ctk.CTkFrame(self, fg_color="#333", corner_radius=0)
        self.navbar = ctk.CTkFrame(self, fg_color="#333", corner_radius=0)

        # Create a container for all pages
        self.container = ctk.CTkFrame(self, fg_color="white")

        # Store pages (frames) in a dictionary
        self.frames = {}

        # Initialize the navigation bar
        self.create_navbar()
        self.create_navbar1()

        # Initialize and show the appropriate frame
        self.init_frames()
        self.user_data = user if user else {}
        print("User Data: ", self.user_data)
        self.show_frame("Login")
    def init_frames(self):
        """Initialize and store all frames/pages."""
        self.frames["Login"] = create_login_frame(self.container, self)

    def init_frames1(self,user=None,):
        """Initialize and store all frames/pages."""
        self.frames["Home"] = create_home_frame(self.container)
        self.frames["Products"] = create_products_frame(self.container,user)
        self.frames["Categories"] = create_categories_frame(self.container,user)
        self.frames["Suppliers"] = create_suppliers_frame(self.container,user)
        self.frames["Inventory"] = create_inventory_frame(self.container,user)
        self.frames["Customers"] = create_customers_frame(self.container,user)
        self.frames["Users"] = create_users_frame(self.container,user)
        self.frames["Sales"] = create_sales_frame(self.container,user,)
        
        self.frames["AddProduct"] = create_add_product_frame(self.container)
        self.frames["AddProductCategory"] = create_add_category_frame(self.container)
        self.frames["AddSupplier"] = create_add_supplier_frame(self.container)
        self.frames["AddCustomer"] = create_add_customer_frame(self.container)
        self.frames["AddUser"] = create_add_user_frame(self.container)
        self.frames["AddSale"] = create_add_sale_frame(self.container,user)
        self.frames['SaleItems'] = frame_principal(self.container)
        

        
        # Pack all frames but hide them initially
        for frame in self.frames.values():
            frame.pack(fill="both", expand=True)
            frame.pack_forget()

    def show_frame(self, frame_name):
        """Switch to the frame with the given name."""
        for name, frame in self.frames.items():
            if name == frame_name:
                if name == "AddProduct" or name == "AddProductCategory" or name == "AddSupplier" or name == "AddCustomer":
                    frame.pack(fill="both", expand=True, padx=400, pady=10, ipady=100)
                elif name == "AddUser" or name=="AddSale" or name == "Login":
                    frame.pack(fill="x", expand=True, padx=400, pady=10, ipady=50)
                else:
                    frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

    def login(self, user):
        
        # supprimer tous les frames
        self.navbar1.pack_forget()
        self.navbar.pack_forget()
        self.container.pack_forget()
        
        # pack all frames necessaries
        self.user_data = load_user_data().get('user')
        self.init_frames1(user=self.user_data)
        self.navbar.pack(side="top", fill="x")
        self.container.pack(fill="both", expand=True)
        self.show_frame("Home")
        # print(f"Login status: {self.user_data}")



    def create_navbar1(self):
        button_style = {"font": ("Arial", 16), "fg_color": "#333", "text_color": "white", "hover_color": "#333"}
        # logo button
        logo_btn = ctk.CTkButton(self.navbar1, text="Easy", **button_style,width=140,anchor='w')
        logo_btn.pack(side="right", padx=1, pady=5)

        
    def create_navbar(self):
        button_style = {"font": ("Arial", 16), "fg_color": "#333", "text_color": "white", "hover_color": "#333"}
        # logo button
        logo_btn = ctk.CTkButton(self.navbar, text="Easy", **button_style,width=140,anchor='w')
        logo_btn.pack(side="right", padx=1, pady=5)

        # Home button
        self.home_btn = ctk.CTkButton(self.navbar, text="الرئيسية", command=lambda: self.show_frame("Home"), **button_style,width=90)
        print('Im Logged in: ',load_user_data().get('logged_in'))
        self.home_btn.pack(side="right", padx=1, pady=5)


        # Products dropdown
        products_dropdown = self.create_dropdown(self.navbar,'المنتجات', [
            ("عرض المنتجات", lambda: self.show_frame("Products")),
            ("إضافة منتج", lambda: self.show_frame("AddProduct"))
        ])
        products_dropdown.pack(side="right", padx=1, pady=5)

        # Categories dropdown
        categories_dropdown = self.create_dropdown(self.navbar,'الاقسام', [
            ("عرض الفئات", lambda: self.show_frame("Categories")),
            ("إضافة فئة", lambda: self.show_frame("AddProductCategory"))
        ])
        categories_dropdown.pack(side="right", padx=1, pady=5)

        # Inventory button
        inventory_btn = ctk.CTkButton(self.navbar, text="المخزون", command=lambda: self.show_frame("Inventory"), **button_style,width=50)
        inventory_btn.pack(side="right", padx=1, pady=5)

        # Sales button
        sale_dropdown = self.create_dropdown(self.navbar,'المبيعات', [
            ("عرض المبيعات", lambda: self.show_frame("Sales")),
            ("إضافة الفاتورة", lambda: self.show_frame("AddSale"))
        ])
        sale_dropdown.pack(side="right", padx=1, pady=5)
        # sales_btn = ctk.CTkButton(self.navbar, text="المبيعات", command=lambda: self.show_frame("Sales"), **button_style,width=50)
        # sales_btn.pack(side="right", padx=1, pady=5)

        # Customers dropdown
        customer_dropdown = self.create_dropdown(self.navbar,'العملاء', [
            ("عرض العملاء", lambda: self.show_frame("Customers")),
            ("إضافة عميل", lambda: self.show_frame("AddCustomer"))
        ])
        customer_dropdown.pack(side="right", padx=1, pady=5)

        # Suppliers dropdown
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
            try:
                self.navbar.pack_forget()
                self.container.pack_forget()
                # self.navbar1.pack_forget()
                
                self.navbar1.pack(side="top", fill="x")
                # self.create_navbar1()        
                self.container.pack(fill="both", expand=True)
                
                os.remove('user_data.json')  # Supprimer le fichier pour déconnecter l'utilisateur
            except FileNotFoundError:
                pass  # Si le fichier n'existe pas, ignorer l'erreur
            self.show_frame("Login") # Assuming the login script has a main() function to launch the login window


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


import json

def save_user_data(user_data):
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

def load_user_data():
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'logged_in': False}  # Si le fichier n'existe pas, l'utilisateur n'est pas connecté
    
# === Création de la fenêtre de connexion ===
def create_login_frame(root,app):
    # Création du frame
    app.navbar1.pack(side="top", fill="x")
    app.container.pack_forget()
    app.container.pack(fill="both", expand=True)
    login_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    login_frame.pack(padx=400,pady=100,ipady=30,)
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(login_frame,fg_color='transparent')
    btns_frame.pack( ipady=10 , padx=20, pady=10,fill='x')
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black'
    ,command=lambda:direction('Fr')).pack(pady=1,side='left')
    
    # label for login 
    log =  ctk.CTkLabel(btns_frame,text="تسجيل الدخول",  bg_color='#fff', font=("Arial", 16,'bold'), anchor='center',width= 310).pack(pady=1,padx=1,side='left')
    
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black'
    ,command=lambda:direction('Ar')).pack(pady=1,side='right')
    # name 
    create_label(login_frame,"اسم المستخدم").pack(ipady=10 ,pady=10, padx=20,fill='x')
    username_entry = create_entry(login_frame)
    
    
    # password_hash
    create_label(login_frame,"كلمة المرور").pack(ipady=10 ,pady=10, padx=20,fill='x')
    password_entry = create_entry(login_frame)
    # show='*'
    
    # global logged 
    def login_action():
        username = username_entry.get()
        password = password_entry.get()

        # Vérification des champs vides
        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        # Connexion à la base de données
        try:
            connect_db()
            my_cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = my_cursor.fetchone()

            # Vérification de l'existence de l'utilisateur et du mot de passe
            if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
                # Connexion réussie
                user_data = {'user': [user[1],user[2],user[4]], 'logged_in': True}  # Créez un dictionnaire pour stocker les données de l'utilisateur
                save_user_data(user_data)  # Enregistrez les données dans un fichier JSON
                messagebox.showinfo("Succès", f"Bienvenue {username}!")
                username_entry.delete(0,tk.END)
                password_entry.delete(0,tk.END)
                app.login(user)
            else:
                messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")    
    add_button = ctk.CTkButton(
        login_frame,
        font=font_arial_title,
        text="تسجيل الدخول",
        width=400,
        command=login_action,
    )
    add_button.pack(pady=20,padx=20,ipady=10)# Fonction pour afficher la fenêtre de mise à jour

    return login_frame

app = App()
# login_frame = create_login_frame(app.container, app)
app.mainloop()
