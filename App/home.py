import tkinter as tk
import customtkinter as ctk
from tkinter import Menu
import json
from tkinter import messagebox, filedialog
from datetime import datetime
from frames.home_frame import create_home_frame
from frames.products_frame import create_products_frame
from frames.categories_frame import create_categories_frame
from frames.add_product_frame import create_add_product_frame
from frames.add_category_frame import create_add_category_frame
from frames.add_supplier_frame import create_add_supplier_frame

from frames.suppliers_frame import create_suppliers_frame
from frames.inventory_frame import create_warehouses_frame
from frames.add_inventory import create_add_warehouse_frame

from frames.customers_frame import create_customers_frame
from frames.add_customer_frame import create_add_customer_frame
from frames.users_frame import create_users_frame
from frames.add_user_frame import create_add_user_frame
from frames.invoices_frame import  create_sales_frame
from frames.new_invoice import create_add_sale_frame
# from frames.login_frame import create_login_frame
from tkinter import messagebox
import pymysql
import bcrypt
import os
from PIL import Image, ImageTk

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
def create_entry(parent,width=400,show=''):
    entry = ctk.CTkEntry(parent, justify=justify,font=("Arial", 14), fg_color='#fff',
                        border_width=1, border_color='#ddd', corner_radius=2, width=width,show= show)
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
    def __init__(self, user=None,accept=False):
        super().__init__()
        self.title("Product Management")
        self.geometry("1000x700")
        
        
        # methode to change


        # Create a container for the navbar
        self.navbar = ctk.CTkFrame(self, fg_color="#333", corner_radius=0)

        # Create a container for all pages
        self.container = ctk.CTkFrame(self, fg_color="white")

        # Store pages (frames) in a dictionary
        self.frames = {}
        self.logged_in = False  # État initial : non connecté

        # Initialize the navigation bar
        self.create_navbar(logged_in=False)  # Créer la navbar avec l'état déconnecté
        self.navbar.pack(side="top", fill="x")  # Afficher la navbar

        # Initialize and show the appropriate frame
        self.init_frames()
        self.user_data = user if user else {}
        print("User Data: ", self.user_data)
        self.show_frame("Login") if accept else self.show_frame("Verify") 
        
    def update_theme(self):
        # change the theme
        theme = ctk.get_appearance_mode() 
        if theme == 'Dark':
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark") 
        
    def init_frames(self):
        """Initialize and store all frames/pages."""
        self.frames["Verify"] = create_verify_frame(self.container, self)
        self.frames["Login"] = create_login_frame(self.container, self)
        self.frames["Home"] = create_home_frame(self.container)
        self.frames["Products"] = create_products_frame(self.container)
        self.frames["Categories"] = create_categories_frame(self.container)
        self.frames["Suppliers"] = create_suppliers_frame(self.container)
        self.frames["Inventory"] = create_warehouses_frame(self.container)
        self.frames["Customers"] = create_customers_frame(self.container)
        self.frames["Users"] = create_users_frame(self.container)
        self.frames["Sales"] = create_sales_frame(self.container)
        
        self.frames["AddProduct"] = create_add_product_frame(self.container)
        self.frames["AddProductCategory"] = create_add_category_frame(self.container)
        self.frames["AddSupplier"] = create_add_supplier_frame(self.container)
        self.frames["AddCustomer"] = create_add_customer_frame(self.container)
        self.frames["AddUser"] = create_add_user_frame(self.container)
        self.frames["AddSale"] = create_add_sale_frame(self.container)
        self.frames['AddInventory'] = create_add_warehouse_frame(self.container)

        # Pack all frames but hide them initially
        for frame in self.frames.values():
            frame.pack(fill="both", expand=True)
            frame.pack_forget()


    def show_frame(self, frame_name, user=None):
        """Switch to the frame with the given name."""
        for name, frame in self.frames.items():
            if name == frame_name:
                if name == "AddProduct" or name == "AddProductCategory" or name == "AddSupplier" or name == "AddCustomer":
                    frame.pack(fill="both", expand=True, padx=400, pady=10, ipady=100)
                elif name == "AddUser" or name == "Login" or name == "AddInventory":
                    frame.pack(fill="x", expand=True, padx=400, pady=10, ipady=50)
                elif name == "Home" or name == "Verify":
                    frame.pack(fill="both", expand=True)
                else:
                    # Si la frame a une méthode `set_user`, on l'appelle pour mettre à jour l'utilisateur
                    if hasattr(frame, 'set_user'):
                        frame.set_user(user)
                    frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

    def login(self, user):
        self.user_data = user
        self.logged_in = True  # Mettre à jour l'état de connexion
        
        # Reconstruire la navbar pour afficher les boutons supplémentaires
        self.navbar.pack_forget()  # Supprimer l'ancienne navbar
        self.container.pack_forget()
        self.create_navbar(logged_in=True, user=user)  # Recréer la navbar avec l'état connecté
        self.navbar.pack(side="top", fill="x")  
        self.container.pack(fill="both", expand=True)
        
        # Afficher la frame "Home" avec l'utilisateur
        self.show_frame("Home", user=user)

    def create_navbar(self, logged_in=False, user=None):
        # Supprimer tous les widgets existants dans la navbar
        for widget in self.navbar.winfo_children():
            widget.destroy()

        button_style = {"font": ("Arial", 16), "fg_color": "#333", "text_color": "white", "hover_color": "#333"}
        
        
        theme = ctk.get_appearance_mode() 
        if theme == 'light':
            image_path = os.path.join(os.path.dirname(__file__), "frames/images", "sun.png") 
            image = ctk.CTkImage(light_image=Image.open(image_path), size=(30, 30),)
        else:
            image_path = os.path.join(os.path.dirname(__file__), "frames/images", "moon.png")
            image = ctk.CTkImage(light_image=Image.open(image_path), size=(30, 30),)

        theme_button = ctk.CTkButton(self.navbar,text='',fg_color='transparent',hover=False, command=self.update_theme,width=10,height=10,corner_radius=50)
        theme_button.pack(pady=10, side="right", fill="x")
        # logo button
        logo_btn = ctk.CTkButton(self.navbar, text="Easy", **button_style, width=140, anchor='w')
        logo_btn.pack(side="right", padx=1, pady=5)

        if logged_in:
            # Home button
            self.home_btn = ctk.CTkButton(self.navbar, text="الرئيسية", command=lambda: self.show_frame("Home", user=user), **button_style, width=90)
            self.home_btn.pack(side="right", padx=1, pady=5)

            # Products dropdown
            products_dropdown = self.create_dropdown(self.navbar, 'المنتجات', [
                ("عرض المنتجات", lambda: self.show_frame("Products", user=user)),
                ("إضافة منتج", lambda: self.show_frame("AddProduct"))
            ])
            products_dropdown.pack(side="right", padx=1, pady=5)


            # Categories dropdown
            categories_dropdown = self.create_dropdown(self.navbar, 'الاقسام', [
                ("عرض الفئات", lambda: self.show_frame("Categories", user=user)),
                ("إضافة فئة", lambda: self.show_frame("AddProductCategory"))
            ])
            categories_dropdown.pack(side="right", padx=1, pady=5)

            # Inventory dropdown
            inventory_dropdown = self.create_dropdown(self.navbar, 'المخازن', [
                ("عرض المخازن", lambda: self.show_frame("Inventory", user=user)),
                ("إضافة مخزن", lambda: self.show_frame("AddInventory"))
            ])
            inventory_dropdown.pack(side="right", padx=1, pady=5)

            # Sales dropdown
            sale_dropdown = self.create_dropdown(self.navbar, 'المبيعات', [
                ("عرض الفواتير", lambda: self.show_frame("Sales", user=user)),
                ("إضافة فاتورة", lambda: self.show_frame("AddSale"))
            ])
            sale_dropdown.pack(side="right", padx=1, pady=5)

            # Customers dropdown
            customer_dropdown = self.create_dropdown(self.navbar, 'العملاء', [
                ("عرض العملاء", lambda: self.show_frame("Customers", user=user)),
                ("إضافة عميل", lambda: self.show_frame("AddCustomer"))
            ])
            customer_dropdown.pack(side="right", padx=1, pady=5)

            # Suppliers dropdown
            supplier_dropdown = self.create_dropdown(self.navbar, 'الموردين', [
                (" قائمة الموردين", lambda: self.show_frame("Suppliers", user=user)),
                ("إضافة مورد", lambda: self.show_frame("AddSupplier"))
            ])
            supplier_dropdown.pack(side="right", padx=1, pady=5)

            # Users dropdown
            user_dropdown = self.create_dropdown(self.navbar, 'المستخدمين', [
                ("عرض المستخدمين", lambda: self.show_frame("Users", user=user)),
                ("إضافة مستخدم", lambda: self.show_frame("AddUser"))
            ])
            user_dropdown.pack(side="right", padx=1, pady=5)

            # settings
            settings_dropdown = self.create_dropdown(self.navbar, 'الاعدادات', [
                ("النسخ الاحتياطي", lambda: export_to_sql())
            ])
            settings_dropdown.pack(side="right", padx=1, pady=5)


            # Logout button
            logout_btn = ctk.CTkButton(self.navbar, text="تسجيل الخروج", command=lambda: self.logout(), **button_style, width=90)
            logout_btn.pack(side="left", padx=1, pady=5)

    def logout(self):
        self.logged_in = False  # Mettre à jour l'état de connexion
        
        # Reconstruire la navbar pour afficher uniquement le bouton "Easy"
        self.navbar.pack_forget()  # Supprimer l'ancienne navbar
        self.container.pack_forget()
        self.create_navbar(logged_in=False)  # Recréer la navbar avec l'état connecté
        self.navbar.pack(side="top", fill="x")  
        self.container.pack(fill="both", expand=True)
        
        self.show_frame("Login")  # Afficher la frame "Login"
    def create_dropdown(self, parent, name, options):
        # Créez un StringVar pour stocker la valeur actuelle du menu déroulant
        default = tk.StringVar(value=name)
        
        # Fonction pour mettre à jour le texte du menu déroulant
        def on_select(value):
            # Trouvez l'option sélectionnée
            selected_option = [option[0] for option in options].index(value)
            # Exécutez la commande associée à l'option
            options[selected_option][1]()
            # Mettez à jour le StringVar pour refléter la sélection actuelle
            default.set(name)
        
        # Créez le menu déroulant avec le StringVar
        dropdown = ctk.CTkOptionMenu(parent, 
            text_color="#fff", dropdown_fg_color="#fff", fg_color='#333',
            font=("Arial", 14), dropdown_font=("Arial", 14), width=90,
            button_color="#333", dropdown_hover_color="#fff", button_hover_color='#333',
            values=[option[0] for option in options], anchor='e',
            variable=default,
            command=on_select)
        
        return dropdown
def export_to_sql():
    try:
        # Demander à l'utilisateur de choisir un répertoire
        backup_dir = filedialog.askdirectory(title="اختر مجلد لحفظ النسخة الاحتياطية")
        
        if not backup_dir:  # Si l'utilisateur annule
            return
        
        # Générer un nom de fichier unique basé sur la date et l'heure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{backup_dir}/backup_{timestamp}.sql"  # Chemin complet du fichier
        
        # Connexion à la base de données
        connect = pymysql.connect(
            host='localhost',
            user='root',
            password='Azerty2024',
            database='easy_db'
        )
        cursor = connect.cursor()
        
        # Ouvrir le fichier SQL en mode écriture
        with open(backup_file, 'w', encoding='utf-8') as f:
            # Récupérer la liste des tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            # Exporter chaque table
            for table in tables:
                table_name = table[0]
                
                # Récupérer la structure de la table
                cursor.execute(f"SHOW CREATE TABLE {table_name}")
                create_table = cursor.fetchone()[1]
                
                # Écrire la commande CREATE TABLE dans le fichier
                f.write(f"-- Structure de la table {table_name}\n")
                f.write(f"{create_table};\n\n")
                
                # Récupérer les données de la table
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                if rows:
                    # Écrire les commandes INSERT INTO dans le fichier
                    f.write(f"-- Données de la table {table_name}\n")
                    for row in rows:
                        # Convertir les valeurs en chaînes de caractères
                        values = ", ".join([f"'{str(value)}'" if value is not None else "NULL" for value in row])
                        f.write(f"INSERT INTO {table_name} VALUES ({values});\n")
                    f.write("\n")
        
        # Fermer la connexion à la base de données
        connect.close()
        
        # Afficher un message de succès
        messagebox.showinfo('نجاح في التصدير', f'تم تصدير قاعدة البيانات بنجاح في "{backup_file}".')
    except Exception as e:
        # Gérer les exceptions
        messagebox.showerror("خطأ", f"حدث خطأ غير متوقع: {str(e)}")
        
 
# === Création de la fenêtre de connexion ===
def create_login_frame(root,app):
    # Création du frame
    app.navbar.pack(side="top", fill="x")
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
    password_entry = create_entry(login_frame,show='*')
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
                messagebox.showinfo('نجاح', f' {username} مرحبا بك')
                username_entry.delete(0,tk.END)
                password_entry.delete(0,tk.END)
                app.login(user)
            else:
                messagebox.showerror("خطأ", " اسم المستخدم او كلمة المرور غير صحيحة")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ : {str(e)}")    
    add_button = ctk.CTkButton(
        login_frame,
        font=font_arial_title,
        text="تسجيل الدخول",
        width=400,
        command=login_action,corner_radius=2
    )
    add_button.pack(pady=20,padx=20,ipady=10)# Fonction pour afficher la fenêtre de mise à jour

    return login_frame

    
import hashlib
import uuid
def verify_license(entered_code):
    """Vérifie si la licence est valide."""
    try:
        # Récupérer l'adresse MAC de la machine
        mac_address = '-'.join(('%012X' % uuid.getnode())[i:i+2] for i in range(0, 12, 2))
        print("mac_address", mac_address)
        
        # Connexion à la base de données
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        cursor = connect.cursor()
        
        # Récupérer la clé de licence correspondante
            # my_cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        cursor.execute("SELECT * FROM licenses WHERE mac_address = %s and license_key = %s", (mac_address,entered_code))
        result = cursor.fetchone()
        
        if result:
            print("Ok")
            # Ajouter l'adresse MAC à la table mac
            cursor.execute("INSERT INTO mac (mac_address) VALUES (%s)", (mac_address,))
            # connect.commit()
            # delete l'adresse mac sur table licenses
            cursor.execute("DELETE FROM licenses WHERE mac_address = %s and license_key = %s", (mac_address, entered_code))
            
            connect.commit()
            return True
        else:
            messagebox.showerror("Licence non trouvée", "Aucune licence trouvée pour cette machine.")
            return False
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la vérification de la licence : {str(e)}")
        return False
    finally:
        connect.close()

def create_verify_frame(parent, app):
    """Crée la frame d'accueil avec la vérification de licence."""
    verify_frame = ctk.CTkFrame(parent, fg_color="white")

    # Titre
    title_label = ctk.CTkLabel(verify_frame, text="Page d'Accueil", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

    # Champ pour entrer le code de licence
    license_label = ctk.CTkLabel(verify_frame, text="Entrez le code de licence :", font=("Arial", 16))
    license_label.pack(pady=10)

    license_entry = ctk.CTkEntry(verify_frame,font=("Arial", 14), fg_color='#fff',
                        border_width=1, border_color='#ddd', corner_radius=2, width=300)
    license_entry.pack(pady=10,ipady=10)

    # Bouton pour vérifier la licence
    def on_verify_license():
        entered_code = license_entry.get().strip()
        if verify_license(entered_code):
            messagebox.showinfo("Succès", "Licence valide. Vous pouvez maintenant vous connecter.")
            app.show_frame("Login")  # Afficher la frame de connexion
        else:
            messagebox.showerror("Erreur", "Code de licence invalide.")

    verify_button = ctk.CTkButton(verify_frame, text="Vérifier la licence",fg_color='#222',hover=False,
        width=300,font=("Arial", 16,'bold'), command=on_verify_license,corner_radius=2)
    verify_button.pack(pady=20,padx=30,ipady=10)

    return verify_frame



if __name__ == "__main__":
    # Récupérer l'adresse MAC de la machine
    mac_address = '-'.join(('%012X' % uuid.getnode())[i:i+2] for i in range(0, 12, 2))
    print("mac_address", mac_address)
    connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
    cursor = connect.cursor()
    
    # Récupérer la clé de licence correspondante
        # my_cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    cursor.execute("SELECT * FROM mac WHERE mac_address = %s", (mac_address))
    result = cursor.fetchone()
    
    if result:
    # if verify_license():
        app = App(accept= True)
        app.mainloop()
    else:
        app = App(accept= False)
        app.mainloop()