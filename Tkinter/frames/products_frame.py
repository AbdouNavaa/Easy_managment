import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pymysql
import pandas as pd
import os
from PIL import Image, ImageTk

def export_to_excel():
    connect_db()
    query = "SELECT * FROM product"
    df = pd.read_sql(query, connect)
    df.to_excel('products.xlsx', index=False)
    messagebox.showinfo("Exportation réussie", "Les données ont été exportées avec succès dans 'products.xlsx'.")


# Fonction pour afficher la fenêtre de mise à jour
def open_update_window(product, update_callback):
    update_window = ctk.CTkToplevel(fg_color='#fff')
    # update_window.pack()
    update_window.title("تعديل ")
    

    print("Product", product)
    prod = fetch_product(product[0])
    print("Product with id", prod)
        # Créer un conteneur scrollable
    canvas = ctk.CTkCanvas(update_window, width=800, height=930)
    canvas.pack( fill="both", expand=True)

    # Créer un scrollbar
    # scrollbar = ctk.CTkScrollbar(update_window, command=canvas.yview)
    # scrollbar.pack(side="right", fill="y")

    # Configurer le canvas pour utiliser le scrollbar
    # canvas.configure(yscrollcommand=scrollbar.set)

    # Créer un frame pour contenir les champs du formulaire
    frame = ctk.CTkFrame(canvas, fg_color='#fff',)
    canvas.create_window((0,0), window=frame, anchor="center", width=799, )
    frame.columnconfigure((0,1,2), weight=1, uniform='a')
    # Champ pour le nom du produit
    ctk.CTkLabel(frame,anchor='e', text="المنتج اسم").grid(row = 0, column = 2, ipady=10 , pady=(30,2), padx=20,)
    name_entry = ctk.CTkEntry(frame, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    name_entry.insert(0, prod[1])  # Pré-remplir avec la valeur actuelle
    name_entry.grid(row = 0, column = 0, ipady=10 ,pady=(30,2), padx=20,columnspan=2)

    ctk.CTkLabel(frame,anchor='e', text="المنتج وصف").grid(row = 1, column = 2, ipady=10 , pady=2, padx=20,)
    desc_entry = ctk.CTkEntry(frame, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    desc_entry.insert(0, prod[2])  # Pré-remplir avec la valeur actuelle
    desc_entry.grid(row = 1, column = 0, ipady=10 , pady=2, padx=20, columnspan=2)

    # Champ pour le prix du produit
    ctk.CTkLabel(frame,anchor='e', text="  السعر").grid(row = 2, column = 2, ipady=10 , pady=2, padx=20,)
    price_entry = ctk.CTkEntry(frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    price_entry.insert(0, str(prod[3]))  # Pré-remplir avec la valeur actuelle
    price_entry.grid(row = 3, column = 2, ipady=10 , pady=2, padx=20, )

    ctk.CTkLabel(frame,anchor='e', text="الشراء سعر ").grid(row = 2, column = 1, ipady=10 , pady=2, padx=20,)
    before_price_entry = ctk.CTkEntry(frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    before_price_entry.insert(0, str(prod[4]))  # Pré-remplir avec la valeur actuelle
    before_price_entry.grid(row = 3, column = 1, ipady=10 , pady=2, padx=20, )
    
    # selling price
    ctk.CTkLabel(frame,anchor='e', text=" السعر البيع ").grid(row = 2, column = 0, ipady=10 , pady=2, padx=20,)
    selling_price_entry = ctk.CTkEntry(frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    selling_price_entry.insert(0, str(prod[11]))  # Pré-remplir avec la valeur actuelle
    selling_price_entry.grid(row = 3, column = 0, ipady=10 , pady=2, padx=20, )    
    # category
    connect_db()
    list_of_categories = []
    fetch_drop('product_categories',categories, list_of_categories)

    ctk.CTkLabel(frame,anchor='e', text="القسم",).grid(row = 4, column = 2, ipady=10 , pady=2, padx=20,)
    prod_categ_default = f"{prod[5]}-{product[2]}"

    # Créez une variable Tkinter StringVar
    prod_categ = tk.StringVar(value=prod_categ_default)
    print(prod_categ)
    category_entry = ctk.CTkOptionMenu(
        frame,values=list_of_categories,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        variable=prod_categ,
    )
    # category_entry.insert(0, str(prod[5]))  # Pré-remplir avec la valeur actuelle
    category_entry.grid(row = 5, column = 2, ipady=10 , pady=2, padx=20, )
    
    
    # supplier
    list_of_suppliers = []
    fetch_drop('suppliers',suppliers, list_of_suppliers)
    ctk.CTkLabel(frame,anchor='e', text=" المورد ",).grid(row = 4, column = 1, ipady=10 , pady=2, padx=20,)
    prod_supplier_default = prod[6]

    # Créez une variable Tkinter StringVar
    prod_supplier = tk.StringVar(value=prod_supplier_default)
    supplier_entry = ctk.CTkOptionMenu(
        frame,values=list_of_suppliers,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        variable=prod_supplier
    )
    # supplier_entry.insert(0, str(prod[6]))  # Pré-remplir avec la valeur actuelle
    supplier_entry.grid(row = 5, column = 1, ipady=10 , pady=2, padx=20, )
    
    
    # warehouse
    list_of_warehouses = []
    fetch_drop('warehouses',warehouses, list_of_warehouses)
    ctk.CTkLabel(frame,anchor='e', text="المخزن ").grid(row = 4, column = 0, ipady=10 , pady=2, padx=20,)
    prod_warehouse_default = f"{prod[8]}-{product[4]}"

    # Créez une variable Tkinter StringVar
    prod_warehouse = tk.StringVar(value=prod_warehouse_default)
    warehouse_entry = ctk.CTkOptionMenu(
        frame,values=list_of_warehouses,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        variable=prod_warehouse
    )
    warehouse_entry.grid(row = 5, column = 0, ipady=10 , pady=2, padx=20, )
    # created at
    ctk.CTkLabel(frame,anchor='e', text=" التاريخ التسجيل ").grid(row = 6, column = 2, ipady=10 , pady=2, padx=20,)
    created_at_entry = ctk.CTkEntry(frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    created_at_entry.insert(0, str(prod[7]))  # Pré-remplir avec la valeur actuelle
    created_at_entry.grid(row = 7, column = 1, ipady=10 , pady=2, padx=20, columnspan=2)
    
    # code
    ctk.CTkLabel(frame,anchor='e', text="الكود ").grid(row = 6, column = 0, ipady=10 , pady=2, padx=20,)
    code_entry = ctk.CTkEntry(frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    code_entry.insert(0, str(prod[9]))  # Pré-remplir avec la valeur actuelle
    code_entry.grid(row = 7, column = 0, ipady=10 , pady=2, padx=20, )
    
    # unit
    ctk.CTkLabel(frame,anchor='e', text="الوحدة ").grid(row = 8, column = 0, ipady=10 , pady=2, padx=20,)
    unit_entry = ctk.CTkEntry(frame,font=("times new roman", 14),   
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    unit_entry.insert(0, str(prod[10]))  # Pré-remplir avec la valeur actuelle
    unit_entry.grid(row = 9, column = 0, ipady=10 , pady=2, padx=20, )
    

    
    # quantity

    ctk.CTkLabel(frame,anchor='e', text=" الكمية ").grid(row = 8, column = 2, ipady=10 , pady=2, padx=20,)
    qty_entry = ctk.CTkEntry(frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    qty_entry.insert(0, str(prod[12]))  # Pré-remplir avec la valeur actuelle
    qty_entry.grid(row = 9, column = 1, ipady=10 , pady=2, padx=20, columnspan=2)
    
    # min quantity
    ctk.CTkLabel(frame,anchor='e', text="الادنى الحد").grid(row = 10, column = 2, ipady=10 , pady=2, padx=20,)
    min_qty_entry = ctk.CTkEntry(frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    min_qty_entry.insert(0, str(prod[13]))  # Pré-remplir avec la valeur actuelle
    min_qty_entry.grid(row = 11, column = 1, ipady=10 , pady=2, padx=20, columnspan=2)
    
    # active
    ctk.CTkLabel(frame,anchor='e', text=" الحالة ").grid(row = 10, column = 0, ipady=10 , pady=2, padx=20,)
    active_entry = ctk.CTkEntry(frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)    
    active_entry.insert(0, str(prod[14]))  # Pré-remplir avec la valeur actuelle
    active_entry.grid(row = 11, column = 0, ipady=10 , pady=2, padx=20, )
    # Bouton pour sauvegarder les modifications
    def save_changes():
        product_name = name_entry.get()
        product_description = desc_entry.get()
        product_price = float(price_entry.get())
        price_before = float(before_price_entry.get())
        product_category = category_entry.get()[0]
        product_supplier = supplier_entry.get()[0]
        product_warehouse = warehouse_entry.get()[0]
        product_code = code_entry.get()
        product_unit = int(unit_entry.get())
        product_selling_price = float(selling_price_entry.get())
        product_min_qty = float(min_qty_entry.get())
        product_active = int(active_entry.get())
        created_at = created_at_entry.get()
        quantity = qty_entry.get()
        product_id = prod[0]
        
        
        try:
            connect_db()
            
            query = '''
            UPDATE products SET
            name=%s, description=%s, price=%s, purchase_price=%s, quantity=%s,  code=%s,  selling_price=%s, min_quantity=%s, is_active=%s, created_at=%s ,
            category_id=%s, supplier_id =%s, warehouse_id =%s
            WHERE id=%s'''
            
            my_cursor.execute(query, (product_name, product_description, product_price, price_before, quantity, 
                                    product_code,  product_selling_price, product_min_qty, product_active, created_at,
                                    product_category, product_supplier, product_warehouse, product_id))
            connect.commit()
        except ValueError:
            messagebox.showerror("Error", "Invalid price value!")
            return

        # product[1] = new_name
        # product[2] = new_desc
        # product[3] = new_price
        # product[4] = new_price_before
        # product[5] = new_supplier
        # product[6] = new_qty
        messagebox.showinfo("Success", "Product updated successfully!")
        frame.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(frame, text="التغييرات حفظ", command=save_changes).grid(row=14, column=0, columnspan=3, ipady=10, pady=10, padx=20, sticky="news")
        # Mettre à jour la taille du frame pour qu'il soit visible dans le canvas
    frame.update_idletasks( )
    canvas.configure(scrollregion=canvas.bbox("all"))


# Connection settings
def connect_db():
    try:
        global connect
        global my_cursor
        global categories
        global warehouses
        global suppliers
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        categories = connect.cursor()
        warehouses = connect.cursor()
        suppliers = connect.cursor()
        print('Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))


# Function to fetch products with pagination
def fetch_products(limit=10, offset=0):
    connect_db()
    query = f'''
    SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location
    FROM products p JOIN product_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id LIMIT {limit} OFFSET {offset}'''
    
    ''' p.is_active,p.purchase_price,p.created_at,p.code,p.unit_id,p.selling_price,p.min_quantity'''
    
    my_cursor.execute(query)
    return my_cursor.fetchall()

def fetch_product(prod_id):
    connect_db()
    query = f'''
    SELECT *
    FROM products  WHERE id = %s'''
    
    ''' '''
    
    my_cursor.execute(query, (prod_id,))
    result = my_cursor.fetchone()
    print('Prod with Id', result)
    return result

def delete_product(product_id, update_callback):
    connect_db()
    try:
        query = f"DELETE FROM products WHERE id = {product_id}"
        my_cursor.execute(query)
        connect.commit()
        messagebox.showinfo('Success', 'Product deleted successfully')
        
        # Appel de la fonction pour actualiser les données
        update_callback()
    except Exception as e:
        messagebox.showerror('Error', str(e))

# Variable globale pour stocker les résultats de recherche
search_results = []
offset = 0
# Function to show products as a styled table with pagination
def show_products_table(parent, limit=10):
    
    def load_page(page_num):
        nonlocal offset
        offset = (page_num - 1) * limit
        update_table()

    def update_table():
        global search_results
        print("SR: ", search_results)
        # Si des résultats de recherche existent, les utiliser   
        if search_results:
            # Si les résultats de recherche sont non vides, appliquer le limit et offset
            data = search_results[offset:offset+limit]
        else:
            # Sinon, récupérer les données avec le limit et offset par défaut
            data = fetch_products(limit, offset)
        
        # Rest of the code...
        # print("data: " , data)
        # Vider les données actuelles du tableau
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Calculer le numéro de départ pour cette page
        start_number = offset + 1

        # Afficher les nouvelles données
        for row_index, row in enumerate(data):
            row1 = row
            row = row[::-1]  # Inverser les données pour l'affichage
            for col_index, value in enumerate(row):
                font_arial = ('Arial',12,)
                label = ctk.CTkLabel(
                    data_frame,
                    text=value,
                    font=font_arial,
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                label1 = ctk.CTkLabel(
                    data_frame,
                    text=start_number + row_index,
                    font=font_arial,
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                label1.grid(row=row_index, column=7, sticky="nsew", padx=5, pady=5)
                
                label.grid(row=row_index, column=col_index + 1, sticky="nsew", padx=5, pady=5)

            font_arial_btn = ('Arial',14,'bold')

            # Ajouter les boutons Modifier et Supprimer
            buttons_frame = ctk.CTkFrame(data_frame, width=100, height=40, fg_color="#fff")
            buttons_frame.grid(row=row_index, column=0, sticky="nsew", padx=5, pady=5)
            update_button = ctk.CTkButton(
                buttons_frame, text="تعديل", fg_color="#0f7",
                font=font_arial_btn,
                width=62, text_color='#000',
                command=lambda row=row: open_update_window(row[::-1], update_table)
            )
            update_button.grid(row=0, column=1)
            delete_button = ctk.CTkButton(
                buttons_frame, text="حذف", fg_color="#f03",
                font=font_arial_btn,
                width=62,
                command=lambda row=row: delete_product(row[::-1][0], update_table)
            )
            delete_button.grid(row=0, column=0, padx=5)
    
    offset = 0

    # Search Frame
    search_frame(parent, lambda: update_table(),offset)  # Appelle `update_table` comme callback
    
    columns = ('رقم القطعة ', 'اسم المنتج ', 'القسم', 'السعر', ' المخزون', 'الحد الادنى', 'الموقع','الاجراءات')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="#fff",border_width=1,border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((0, 1, 2,3, 4, 5, 6,7), weight=1, uniform='a')
    font_arial = ('Arial',14,'bold')

    # Add column headings
    for col_index, col_name in enumerate(columns):
        label = ctk.CTkLabel(
            header_frame,
            text=col_name,
            font=font_arial,
            text_color="black",
            fg_color="#fff",
            corner_radius=1,
            width=100
        )
        label.grid(row=0, column=col_index, sticky="nsew", padx=5, pady=5)

    # Data Frame
    data_frame = ctk.CTkFrame(parent, corner_radius=2,  fg_color="#fff",border_width=1,border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform='a')

    # Pagination Controls
    nav_frame = ctk.CTkFrame(parent, corner_radius=2,  fg_color="#fff",border_width=1,border_color="#f0f0f0")
    nav_frame.pack(fill='x', pady=10,padx=20, ipady=10)
    back_image_path = os.path.join(os.path.dirname(__file__), "images", "back.png")
    back_image = ctk.CTkImage(light_image=Image.open(back_image_path), size=(10, 10),)

    prev_button = ctk.CTkButton(
        nav_frame,
        image=back_image,
        font=font_arial,
        fg_color="transparent",
        hover_color="#f0f0f0",
        text_color="#333",
        text="السابق",
        command=lambda: load_page(max(1, (offset // limit))),
        state="normal" ,
        width=40
    )
    prev_button.pack(side="left", padx=5,)


    next_image_path = os.path.join(os.path.dirname(__file__), "images", "forward.png")
    next_image = ctk.CTkImage(light_image=Image.open(next_image_path), size=(10, 10),)
    next_button = ctk.CTkButton(
        nav_frame,
        font=font_arial,
        fg_color="transparent",
        hover_color="#f0f0f0",
        text_color="#333",
        text="التالي",
        image=next_image,
        compound="right",
        width=40,
        command=lambda: load_page((offset // limit) + 2)
    )
    next_button.pack(side="right", padx=5)

    update_table()
def search_frame(parent, refresh_callback,offset):
    """Crée une barre de recherche avec options."""
    search_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white")
    search_frame.pack(fill='x', padx=20, pady=5)

    # search_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')

    font_arial = ('Arial',18,)
    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="إبحث عن منتج ",
        fg_color="white",
        bg_color="white",
        border_color="#e5e3e0",
        border_width=1,
        width=300,
        corner_radius=0,
        font=font_arial,
        justify="right"
    )
    search_entry.pack(side="right",  pady=5, ipadx=5, ipady=5)
    
    search_image_path = os.path.join(os.path.dirname(__file__), "images", "search.png")
    
    s_image = ctk.CTkImage(light_image=Image.open(search_image_path), size=(24, 20),)
    search_button = ctk.CTkButton(
        search_frame,
        image=s_image,
        fg_color="#fff",
        hover_color="#f0f0f0",
        text_color="#333",
        corner_radius=0,border_width=1,border_color="#e5e3e0",
        text="",width=24,
        font=font_arial,
        # height=22,
        command=lambda: search(search_entry.get(),refresh_callback)
    )
    search_button.pack(side="right", padx=(100,0), pady=5, ipadx=5, ipady=5)

        # Option Menus
    connect_db()
    myList = []
    fetch_all('product_categories',categories, myList)
    optionmenu_var = ctk.StringVar(value="كل الاقسام")
    optionmenu = ctk.CTkOptionMenu(
        search_frame,
        values=myList,
        text_color="#333",
        dropdown_fg_color="#fff",
        button_color="white",
        fg_color="white",
        dropdown_hover_color="#f0f0f0",
        variable=optionmenu_var,
        font=font_arial,
        command=lambda value: search_by_category(value,refresh_callback)
    )
    optionmenu.pack(side="right", padx=5, pady=5, ipadx=5, ipady=5)


    list_of_howarehouses = []
    fetch_all('warehouses',warehouses,list_of_howarehouses)
    inventory_var = ctk.StringVar(value="المخزون")
    inventoryMenu = ctk.CTkOptionMenu(
        search_frame,
        values=list_of_howarehouses,
        text_color="#333",
        dropdown_fg_color="#fff",
        button_color="white",
        fg_color="white",font=font_arial,
        dropdown_hover_color="#f0f0f0",
        variable=inventory_var,
        command=lambda value: search_by_warehouses(value,refresh_callback)
    )
    inventoryMenu.pack(side="right", padx=5, pady=5, ipadx=5, ipady=5)
    image_path = os.path.join(os.path.dirname(__file__), "images", "refresh.png")
    
    image = ctk.CTkImage(light_image=Image.open(image_path), size=(20, 20),)

    refresh_button = ctk.CTkButton(
        search_frame,
        image=image,
        text="تحديث",
        fg_color="#fff",
        hover_color="#f0f0f0",
        font=font_arial,
        width=40,
        text_color="#333",
        command=lambda: refresh(refresh_callback),compound="left"
    )
    refresh_button.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5)
def refresh(refresh_callback):
    global search_results  # Déclarer `search_results` comme global
    search_results = []
    # Appeler la fonction de rafraîchissement pour afficher les données à partir de la base de données
    refresh_callback()
def search(query,refresh_callback):
    global search_results  # Déclarer `search_results` comme global
    print("Searching:", query)
    if not query:
        messagebox.showinfo("Warning", "Search input is empty!")
        search_results = []  # Vider les résultats si la recherche est vide
    else:
        connect_db()
        sql_query = '''
        SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location
        FROM products p JOIN product_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id 
        WHERE p.name = %s OR c.name = %s OR w.name = %s OR w.location = %s
        LIMIT 10
        '''
        # query = f'SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location FROM products p JOIN product_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id LIMIT {limit} OFFSET {offset}'
        
        my_cursor.execute(sql_query, (query, query,query,query))
        search_results = my_cursor.fetchall()  # Récupérer les résultats
        refresh_callback()  # Appeler la fonction de rafraîchissement pour afficher les nouvelles données

    print(search_results)  # Afficher les résultats pour déboguer

def search_by_category(query, refresh_callback, ):
    global search_results  # Déclarer `search_results` comme global
    print("Searching by category:", query)
    if not query:
        messagebox.showinfo("Warning", "Search input is empty!")
        search_results = []  # Vider les résultats si la recherche est vide
    else:
        connect_db()
        sql_query = '''
        SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location
        FROM products p JOIN product_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id 
        WHERE c.name = %s 
        LIMIT 10
        '''
        my_cursor.execute(sql_query, (query,))
        # search_results = my_cursor.fetchall()  # Récupérer les résultats
        search_results = my_cursor.fetchall()
        if not search_results:
            messagebox.showinfo("Warning", "No products found with this category!")

        else:
            messagebox.showinfo("success", f"{len(search_results)} products found successfully!")
        refresh_callback()  # Appeler la fonction de rafraîchissement pour afficher les nouvelles données

def search_by_warehouses(query, refresh_callback, ):
    global search_results  # Déclarer `search_results` comme global
    print("Searching by warehouses:", query)
    if not query:
        messagebox.showinfo("Warning", "Search input is empty!")
        search_results = []  # Vider les résultats si la recherche est vide
    else:
        connect_db()
        sql_query = f'SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location FROM products p JOIN product_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id  WHERE w.name = %s  '
        my_cursor.execute(sql_query, (query,))
        search_results = my_cursor.fetchall()  # Récupérer les résultats
        
        if not search_results:
            messagebox.showinfo("Warning", "No products found with this warehouse!")

        else:
            messagebox.showinfo("success", f"{len(search_results)} products found successfully!")
        refresh_callback()  # Appeler la fonction de rafraîchissement pour afficher les nouvelles données
# add Prod
def add_product():
    root.destroy()
    import add_product_frame
def fetch_all(table_name,total_variable,myList):
    query = f'SELECT * FROM {table_name}'
    total_variable.execute(query)
    # print('ffdfd:', total_variable.fetchall())
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        print(variable[1])
        myList.append(variable[1])
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    print(myList)
    return myList  # Retourner 0 si aucun résultat n'est trouvé   

def fetch_drop(table_name,total_variable,myList):
    query = f'SELECT * FROM {table_name}'
    total_variable.execute(query)
    # print('ffdfd:', total_variable.fetchall())
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        print(variable[1])
        myList.append(f'{variable[0]}-{variable[1]}')
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    print(myList)
    return myList  # Retourner 0 si aucun résultat n'est trouvé   


def show_title_frame(parent, ):
    
    # Table headers

    # Header frame
    title_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="transparent",)
    title_frame.pack(fill='x', padx=20, pady=5,)
    # title_frame.configure(direction="rtl")
    
    # title_frame.configure('tag-right', justify='right')
    # title_frame.insert('end', 'text ' * 10, 'tag-right')
    title_frame.columnconfigure((0, 1, 2,3, 4, 5, 6), weight=1, uniform='a',)
    # title_frame.columns = 
    # title_frame.columns[::-1]
    font_arial_title = ('Arial',20,'bold')
    font_arial = ('Arial',12,)

    title_label = ctk.CTkLabel(
        master=title_frame,
        text="ادارة المنتجات",
        font=font_arial_title,
        # text_color="#0066cc"
        # compound="right"
    )
    title_label.pack(side="right")
    
    # add 3 button 
    # add_product_button = ctk.CTkButton(
    #     master=title_frame,
    #     text="اضافة منتج",
    #     font=font_arial,
    #     fg_color="#2498f5",
    #     text_color="#333",
    #     hover_color="#f0f0f0",
    #     corner_radius=5,
    #     command=add_product
    # )
    # # add_product_button.pack(pady=10,anchor="e",padx=(10,40),)

    # add_product_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    # add 3 button 
    export_button = ctk.CTkButton(
        master=title_frame,
        text=" Excel تصدير إلى ",
        font=font_arial,
        fg_color="#3eecfa",
        text_color="#333",
        hover_color="#f0f0f0",
        corner_radius=5,
        command=export_to_excel
    )
    # export_button.pack(pady=10,anchor="e",padx=(10,40),)

    import_button = ctk.CTkButton(
        master=title_frame,
        text=" Excel استيراد من ",
        font=font_arial,
        fg_color="#09d666",
        text_color="#333",
        hover_color="#f0f0f0",
        corner_radius=5,
        command=lambda: messagebox.showinfo("ا��افة منتج", "يمكنك ا��افة منتج ��ديد من خلال هذه الخا��ية")
    )
    # import_button.pack(pady=10,anchor="e",padx=(10,40),)

    # import_button.grid(row=0, column=1, sticky="e", padx=5, pady=5)
    import_button.pack(side="left",padx=5)
    export_button.pack(side="left")


    
    

# Function to create the products frame
def create_products_frame(root):
    products_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

    show_title_frame(products_frame)
    # search_frame(products_frame)

    show_products_table(products_frame)
    return products_frame


window = ctk.CTk(fg_color="#fff")
window.title('customtkinter app')
window.geometry('1200x550')
window.state('zoomed')

products_frame = create_products_frame(window)
products_frame.pack(fill='both', expand=True)

# run
window.mainloop()