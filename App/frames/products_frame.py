import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pymysql
import pandas as pd
import os
from PIL import Image, ImageTk

def export_to_excel():
    connect_db()
    query = "SELECT * FROM products"
    df = pd.read_sql(query, connect)
    df.to_excel('products.xlsx', index=False)
    messagebox.showinfo('نجاح في التصدير', ' لقد تم تصدير البيانات بنجاح في "products.xlsx".')

from tkinter import filedialog

def import_from_excel():
    try:
        # Open file dialog to select Excel file
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        
        if not file_path:
            return  # User cancelled file selection

        # Read Excel file
        df = pd.read_excel(file_path)

        # Connect to database
        connect_db()

        # Iterate through rows and insert/update data
        for index, row in df.iterrows():
            print('rows:', index,row)
            query = """
            INSERT INTO products (name, description, price, purchase_price, category_id, supplier_id, 
                                  warehouse_id,  code,  selling_price, quantity, min_quantity,created_at, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,NOW(),0)
            """
            
            values = (
                row['name'], row['description'], row['price'], row['purchase_price'],
                row['category_id'], row['supplier_id'], row['warehouse_id'],
                row['code'], row['selling_price'], row['quantity'],
                row['min_quantity']
            )
            print('Values:', values)
            
            my_cursor.execute(query, values)

        connect.commit()
        messagebox.showinfo('نجاح', ' تمت الاستيراد بنجاح')
    except Exception as e:
        messagebox.showerror("خطأ في الاستيراد", f"حدث خطأ في الاستيراد الخطأ : {str(e)}")
    finally:
        if connect:
            connect.close()

from tkcalendar import DateEntry
from datetime import datetime


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
def create_entry(parent):
    font_arial =("Arial", 14)   
    entry = ctk.CTkEntry(parent, justify=justify,font=font_arial, fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=2, width=400)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text)
    label_widgets.append(label)
    return label

def product_details(id):
    connect_db()
    sql_query = '''
    SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location,p.quantity,p.description,s.name,p.code
    FROM products p JOIN product_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id JOIN suppliers s ON p.supplier_id = s.id 
    WHERE p.id = %s
    '''
    # query = f'SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location FROM products p JOIN product_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id LIMIT {limit} OFFSET {offset}'
    
    my_cursor.execute(sql_query, (id))
    result = my_cursor.fetchone() 
    
    return result
# details window

def show_details(product):
    show_window = ctk.CTkToplevel()
    show_window.title("تفاصيل المنتج")
    show_window.geometry("500x500")
    show_window.configure(fg_color="#f0f0f0")

    # Fetch product details
    details = product_details(product[0])

    # Main frame
    main_frame = ctk.CTkFrame(show_window, corner_radius=10, fg_color="#ffffff")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Product name
    name_label = ctk.CTkLabel(main_frame, text=details[1], font=("Arial", 24, "bold"), text_color="#333333")
    name_label.pack(pady=(20, 10))

    # Details frame
    details_frame = ctk.CTkFrame(main_frame, corner_radius=5, fg_color="white")
    details_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Details
    details_list = [
        (":القسم", details[2]),
        (":السعر", f"{details[3]} MRU"),
        (":المخزن", details[4]),
        (":الحد الأدنى للكمية", details[5]),
        (":الموقع", details[6]),
        (":الكمية الحالية", details[7]),
        (":المورد", details[9]),
        (":الكود", details[10]),
        # ("الوصف", details[8]),
    ]

    for i, (label, value) in enumerate(details_list):
        row_frame = ctk.CTkFrame(details_frame, fg_color="white")
        row_frame.pack(fill="both", padx=10,pady=10)

        label_widget = ctk.CTkLabel(row_frame, text=label, font=("Arial", 14, "bold"), text_color="#555555")
        label_widget.pack(side="right")

        value_widget = ctk.CTkLabel(row_frame, text=str(value), font=("Arial", 14), text_color="#333333")
        value_widget.pack(side="left",padx=10)
        
        # line
        line = ctk.CTkFrame(row_frame, height=1, fg_color="#999")
        line.pack(fill="x", padx=10, pady=10, expand=True,)


    # Center the window on the screen
    # show_window.update_idletasks()
    # width = show_window.winfo_width()
    # height = show_window.winfo_height()
    # x = (show_window.winfo_screenwidth() // 2) - (width // 2)
    # y = (show_window.winfo_screenheight() // 2) - (height // 2)
    # show_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    show_window.grab_set()  # Make the window modal
    show_window.focus_set()  # Set focus to the new window
    
# Fonction pour afficher la fenêtre de mise à jour
def open_update_window(product, update_callback):
    update_window = tk.Toplevel(background='#fff')
    # update_window.pack()
    update_window.title("تعديل ")
    

    prod = fetch_product(product[0])
        # Créer un conteneur scrollable
    canvas = ctk.CTkCanvas(update_window, width=800, height=930)
    canvas.pack( fill="both", expand=True)

    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 12)
    # Créer un frame pour contenir les champs du formulaire
    frame = ctk.CTkFrame(canvas, fg_color='#fff',)
    canvas.create_window((0,0), window=frame, anchor="center", width=799, )
    frame.columnconfigure((0,1,2), weight=1, uniform='a')
    
    #name
    name_label = create_label(frame,"اسم المنتج")
    name_label.grid(row = 0,column=0, columnspan=3, ipady=10, pady=(20,5),  sticky="news")
    
    name_entry = create_entry(frame)
    name_entry.insert(0, prod[1])  # Pré-remplir avec la valeur actuelle
    name_entry.grid(row = 1, column=0, columnspan=3, ipady=10, pady=2, padx=20, sticky="news")

    #desc
    desc_label = create_label(frame,"وصف المنتج")
    desc_label.grid(row = 2,column=0, columnspan=3, ipady=10, pady=(20,5),  sticky="news")
    
    desc_entry = create_entry(frame)
    desc_entry.insert(0, prod[2])  # Pré-remplir avec la valeur actuelle
    desc_entry.grid(row = 3, column=0, columnspan=3, ipady=10, pady=2, padx=20, sticky="news")

    #price
    price_label = create_label(frame,"السعر ")
    price_label.grid(sticky="news",row = 4, column = 2, ipady=10 , pady=2, )
    price_entry = create_entry(frame)
    
    price_entry.insert(0, str(prod[3]))  # Pré-remplir avec la valeur actuelle
    price_entry.grid(row = 5, column = 2, ipady=10 , pady=2, padx=20, )

    #before_price
    before_price_label = create_label(frame,"سعر الشراء ")
    before_price_label.grid(sticky="news",row = 4, column = 1, ipady=10 , pady=2, )
    
    before_price_entry = create_entry(frame)
    before_price_entry.insert(0, str(prod[4]))  # Pré-remplir avec la valeur actuelle
    before_price_entry.grid(row = 5, column = 1, ipady=10 , pady=2, padx=20, )
    
    # selling price
    selling_price_label = create_label(frame," سعر البيع ")
    selling_price_label.grid(sticky="news",row = 4, column = 0, ipady=10 , pady=2, )
    
    selling_price_entry = create_entry(frame)
    selling_price_entry.insert(0, str(prod[12]))  # Pré-remplir avec la valeur actuelle
    selling_price_entry.grid(row = 5, column = 0, ipady=10 , pady=2, padx=20, ) 

    # category
    connect_db()
    list_of_categories = []
    fetch_drop('product_categories',categories, list_of_categories)

    category_label = create_label(frame,"القسم ")
    category_label.grid(sticky="news",row = 6, column = 2, ipady=10 , pady=2, )
    
    prod_categ_default = f"{prod[5]}-{product[2]}"

    # Créez une variable Tkinter StringVar
    prod_categ = tk.StringVar(value=prod_categ_default)
    category_entry = ctk.CTkOptionMenu(
        frame,values=list_of_categories,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        variable=prod_categ,
    )
    # category_entry.insert(0, str(prod[5]))  # Pré-remplir avec la valeur actuelle
    category_entry.grid(row = 7, column = 2, ipady=10 , pady=2, padx=20, )
    
    
    # supplier
    list_of_suppliers = []
    fetch_drop('suppliers',suppliers, list_of_suppliers)
    
    supplier_label = create_label(frame,"المورد ")
    supplier_label.grid(sticky="news",row = 6, column = 1, ipady=10 , pady=2, )
    
    prod_supplier_default = prod[6] if prod[6] != None else list_of_suppliers[0]
    print('dfssdff:',product,prod)

    # Créez une variable Tkinter StringVar
    prod_supplier = tk.StringVar(value=prod_supplier_default)
    supplier_entry = ctk.CTkOptionMenu(
        frame,values=list_of_suppliers,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        font=font_arial,
        variable=prod_supplier
    )
    supplier_entry.grid(row = 7, column = 1, ipady=10 , pady=2, padx=20, )
    
    
    # warehouse
    list_of_warehouses = []
    fetch_drop('warehouses',warehouses, list_of_warehouses)

    warehouse_label = create_label(frame,"المخزن ")
    warehouse_label.grid(sticky="news",row = 6, column = 0, ipady=10 , pady=2, )
    prod_warehouse_default = f"{prod[8]}-{product[4]}"

    # Créez une variable Tkinter StringVar
    prod_warehouse = tk.StringVar(value=prod_warehouse_default)
    warehouse_entry = ctk.CTkOptionMenu(
        frame,values=list_of_warehouses,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        font=font_arial,
        variable=prod_warehouse
    )
    warehouse_entry.grid(row = 7, column = 0, ipady=10 , pady=2, padx=20, )

    # Create the DateEntry widget
    created_at_label = create_label(frame,"تاريخ التسجيل")
    created_at_label.grid(sticky="news",row = 8, column = 2, ipady=10 , pady=2, )
    
    created_at_entry = DateEntry(frame, width=30, background='white',font=font_arial,
                                foreground='black', justify='center', date_pattern='yyyy-mm-dd',)
    created_at_entry.grid(row = 9, column = 2, ipady=10 , pady=2, padx=20, )

    # Set the initial date if available
    if prod[7]:
        try:
            # Check if prod[7] is already a datetime object
            if isinstance(prod[7], datetime):
                created_at_entry.set_date(prod[7].date())
            else:
                # If it's a string, parse it
                created_at_entry.set_date(datetime.strptime(prod[7], '%Y-%m-%d %H:%M:%S').date())
        except ValueError as e:
            messagebox.showerror("Error", "Invalid date format: {categ[4]}, Error: {e}!")
            

    
    # code
    code_label = create_label(frame,"الكود ")
    code_label.grid(sticky="news",row = 8, column = 0, ipady=10 , pady=2, )
    
    code_entry = create_entry(frame)
    code_entry.insert(0, str(prod[10]))  # Pré-remplir avec la valeur actuelle
    code_entry.grid(row = 9, column = 0, ipady=10 , pady=2, padx=20, )
    
    # unit
    unit_label = create_label(frame,"الوحدة ")
    unit_label.grid(sticky="news",row = 8, column = 1, ipady=10 , pady=2, )
    
    unit_entry = create_entry(frame) # Pré-remplir avec la valeur actuelle
    unit_entry.grid(row = 9, column = 1, ipady=10 , pady=2, padx=20, )
    
    # qty
    qty_label = create_label(frame,"الكمية ")
    qty_label.grid(sticky="news",row = 10, column = 2, ipady=10 , pady=2, )
    
    qty_entry = create_entry(frame)
    qty_entry.insert(0, str(prod[13]))  # Pré-remplir avec la valeur actuelle
    qty_entry.grid(row = 11, column = 2, ipady=10 , pady=2, padx=20, )
    
    # min quantity
    min_qty_label = create_label(frame,"الحد الادنى")
    min_qty_label.grid(sticky="news",row = 10, column = 1, ipady=10 , pady=2, )
    
    min_qty_entry = create_entry(frame)
    min_qty_entry.insert(0, str(prod[14]))  
    min_qty_entry.grid(row = 11, column = 1, ipady=10 , pady=2, padx=20, )
    
    # status
    active_label = create_label(frame,"الحالة ")
    active_label.grid(sticky="news",row = 10, column = 0, ipady=10 , pady=2, )
    
    active_entry = create_entry(frame)    
    active_entry.insert(0, str(prod[15]))  # Pré-remplir avec la valeur actuelle
    # active_entry.grid(row = 11, column = 0, ipady=10 , pady=2, padx=20, )
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
        product_unit = unit_entry.get()
        product_selling_price = float(selling_price_entry.get())
        product_min_qty = float(min_qty_entry.get())
        product_active = int(active_entry.get())
        created_at = created_at_entry.get_date().strftime('%Y-%m-%d') if created_at_entry.get_date() else None
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
            messagebox.showerror("خطأ", "يرجى تصحيح القيم المدخلة")
            return

        messagebox.showinfo('نجاح', 'تم تحديث المنتج بنجاح')
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(frame, text="حفظ", command=save_changes,font=font_arial_title,corner_radius=2).grid(row=12, column=0, columnspan=3, ipady=10, pady=(20,10), padx=20, sticky="news")
        # Mettre à jour la taille du frame pour qu'il soit visible dans le canvas
    frame.update_idletasks( )
    canvas.configure(scrollregion=canvas.bbox("all"))
    
    
    update_window.grab_set()  # Make the window modal
    update_window.focus_set()

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
    return result

def delete_product(product_id, update_callback):
    connect_db()
    try:
        query = f"DELETE FROM products WHERE id = {product_id}"
        my_cursor.execute(query)
        connect.commit()
        messagebox.showinfo('نجاح', 'تم حذف المنتج بنجاح')
        
        # Appel de la fonction pour actualiser les données
    except Exception as e:
        messagebox.showerror('Error', str(e))
    update_callback()

# Variable globale pour stocker les résultats de recherche
search_results = []
offset = 0
# Function to show products as a styled table with pagination
def show_products_table(parent, limit=10,is_admin=1):
    
    print('Is Admin:',is_admin)
    def load_page(page_num):
        nonlocal offset
        offset = (page_num - 1) * limit
        update_table()

    def update_table():
        global search_results
        # Si des résultats de recherche existent, les utiliser   
        if search_results:
            # Si les résultats de recherche sont non vides, appliquer le limit et offset
            data = search_results[offset:offset+limit]
        else:
            # Sinon, récupérer les données avec le limit et offset par défaut
            data = fetch_products(limit, offset)
            # print('data', data)
        
        # Rest of the code...
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
                label1.grid(row=row_index, column=7 if is_admin == 1 else 6, sticky="nsew", padx=5, pady=5)
                
                label.grid(row=row_index, column=col_index + 1 if is_admin == 1 else col_index, sticky="nsew", padx=5, pady=5)

            font_arial_btn = ('Arial',14,'bold')

            # Ajouter les boutons Modifier et Supprimer
            buttons_frame = ctk.CTkFrame(data_frame, width=100, height=40, fg_color="#fff") 
            buttons_frame.grid(row=row_index, column=0, sticky="nsew", padx=5, pady=5) if is_admin == 1 else buttons_frame.grid_remove()
            show_image_path = os.path.join(os.path.dirname(__file__), "images", "info.png")
            show_image = ctk.CTkImage(light_image=Image.open(show_image_path), size=(15, 15),)
            update_button = ctk.CTkButton(buttons_frame, text="",text_color="black",
                    image=show_image,
                    fg_color='#fff',border_color='#f0f0f0',border_width=1,corner_radius=2,
                    hover_color='#f0f0f0',
                    width=40,
                    font=font_arial_btn,        
                    command=lambda row=row: show_details(row[::-1])
                    )
            update_button.grid(row=0,column=2) 
            
            edit_image_path = os.path.join(os.path.dirname(__file__), "images", "edit.png")
            edit_image = ctk.CTkImage(light_image=Image.open(edit_image_path), size=(15, 15),)
            update_button = ctk.CTkButton(buttons_frame, text="",text_color="black",
                    image=edit_image,
                    fg_color='#fff',border_color='#f0f0f0',border_width=1,corner_radius=2,
                    hover_color='#f0f0f0',
                    width=40,
                    font=font_arial_btn,        
                    command=lambda row=row: open_update_window(row[::-1],update_table)
                    )
            update_button.grid(row=0,column=1,padx=5) if is_admin == 1 else update_button.grid_remove()
            
            
            delete_image_path = os.path.join(os.path.dirname(__file__), "images", "trash-can.png")
            delete_image = ctk.CTkImage(light_image=Image.open(delete_image_path), size=(20, 20),)
            delete_button = ctk.CTkButton(buttons_frame,
                    text="",
                    text_color="black",
                    image=delete_image,
                    fg_color='#fff',border_color='#f0f0f0',border_width=1,corner_radius=2,
                    hover_color='#f0f0f0',
                    font=font_arial_btn, 
                    width=40,
                    command=lambda row=row: delete_product(row[::-1][0], update_table)
                    )
            delete_button.grid(row=0,column=0,padx=5) if is_admin == 1 else delete_button.grid_remove()
            
    
    offset = 0

    # Search Frame
    search_frame(parent, lambda: update_table(),offset)  # Appelle `update_table` comme callback
    
    columns = ('رقم القطعة ', 'اسم المنتج ', 'القسم', 'السعر', ' المخزون', 'الحد الادنى', 'الموقع')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="#fff",border_width=1,border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((0, 1, 2,3, 4, 5, 6), weight=2, uniform='a') if is_admin == 1 else header_frame.columnconfigure((0, 1, 2,3, 4, 5), weight=2, uniform='a')
    header_frame.columnconfigure((7), weight=1, uniform='a') if is_admin == 1 else header_frame.columnconfigure((6), weight=1, uniform='a')
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
        action_lab =ctk.CTkLabel(
            header_frame,
            text='الاجراءات',
            font=font_arial,
            text_color="black",
            # fg_color="#fff",
            corner_radius=1,
            width=100
        )
        action_lab.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)if is_admin == 1 else action_lab.grid_remove()
        label.grid(row=0, column=col_index+1 if is_admin == 1 else col_index, sticky="nsew", padx=5, pady=5)

    # Data Frame
    data_frame = ctk.CTkFrame(parent, corner_radius=2,  fg_color="#fff",border_width=1,border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure((0, 1, 2,3, 4, 5, 6), weight=2, uniform='a') if is_admin == 1 else data_frame.columnconfigure((0, 1, 2,3, 4, 5), weight=2, uniform='a')
    data_frame.columnconfigure((7), weight=1, uniform='a') if is_admin == 1 else data_frame.columnconfigure((6), weight=1, uniform='a')
    # data_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform='a') if is_admin == 1 else data_frame.columnconfigure((0, 1, 2,3, 4, 5, 6), weight=1, uniform='a')

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
    s_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white")
    s_frame.pack(fill='x', padx=20, pady=5)

    # s_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')

    font_arial = ('Arial',15,)
    search_entry = ctk.CTkEntry(
        s_frame,
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
        s_frame,
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
    optionmenu_var = ctk.StringVar(value="كل الاقسام",name='ddd',)
    optionmenu = ctk.CTkOptionMenu(
        s_frame,
        values=myList,
        text_color="#333",
        dropdown_fg_color="#fff",
        button_color="white",
        fg_color="white",
        dropdown_hover_color="#f0f0f0",
        button_hover_color='#fff',
        dropdown_font=('Arial',14,),
        variable=optionmenu_var,
        font=('Arial',16,),
        command=lambda value: search_by_category(value,refresh_callback)
    )
    optionmenu.pack(side="right", padx=5, pady=5, ipadx=5, ipady=5)


    list_of_howarehouses = []
    fetch_all('warehouses',warehouses,list_of_howarehouses)
    inventory_var = ctk.StringVar(value="المخزون")
    inventoryMenu = ctk.CTkOptionMenu(
        s_frame,
        values=list_of_howarehouses,
        text_color="#333",
        dropdown_fg_color="#fff",
        button_color="white",
        fg_color="white",
        dropdown_hover_color="#f0f0f0",
        button_hover_color='#fff',
        dropdown_font=('Arial',14,),
        font=('Arial',16,), 
        variable=inventory_var,
        command=lambda value: search_by_warehouses(value,refresh_callback)
    )
    inventoryMenu.pack(side="right", padx=5, pady=5, ipadx=5, ipady=5)
    image_path = os.path.join(os.path.dirname(__file__), "images", "refresh.png")
    
    image = ctk.CTkImage(light_image=Image.open(image_path), size=(20, 20),)

    refresh_button = ctk.CTkButton(
        s_frame,
        image=image,
        text="تحديث",
        fg_color="#fff",
        hover_color="#f0f0f0",
        font=font_arial,
        width=40,corner_radius=2,
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
    if not query:
        messagebox.showinfo('تنبيه', 'لا يمكنك البحث عن نتيجة فارغة')
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


def search_by_category(query, refresh_callback, ):
    global search_results  # Déclarer `search_results` comme global
    if not query:
        messagebox.showinfo('تنبيه', 'لا يمكنك البحث عن نتيجة فارغة')
        search_results = []  # Vider les résultats si la recherche est vide
    else:
        connect_db()
        sql_query = '''
        SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location
        FROM products p JOIN product_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id 
        WHERE c.name = %s 
        '''
        my_cursor.execute(sql_query, (query,))
        # search_results = my_cursor.fetchall()  # Récupérer les résultats
        search_results = my_cursor.fetchall()
        if not search_results:
            messagebox.showinfo('تنبيه', ' المنتج غير موجود')

        else:
            messagebox.showinfo("نجاح", f"تم ايجاد {len(search_results)} منتجات ")
        refresh_callback()  # Appeler la fonction de rafraîchissement pour afficher les nouvelles données

def search_by_warehouses(query, refresh_callback, ):
    global search_results  # Déclarer `search_results` comme global
    if not query:
        messagebox.showinfo('تنبيه', ' لا يمكنك البحث عن نتيجة فارغة')
        search_results = []  # Vider les résultats si la recherche est vide
    else:
        connect_db()
        sql_query = f'SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location FROM products p JOIN product_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id  WHERE w.name = %s  '
        my_cursor.execute(sql_query, (query,))
        search_results = my_cursor.fetchall()  # Récupérer les résultats
        
        if not search_results:
            messagebox.showinfo("نجاح", "لا يوجد منتجات في المخزن المحدد")

        else:
            messagebox.showinfo("نجاح", f"تم ايجاد {len(search_results)} منتجات ")
        refresh_callback()  # Appeler la fonction de rafraîchissement pour afficher les nouvelles données
# add Prod
def add_product():
    root.destroy()
    import add_product_frame
def fetch_all(table_name,total_variable,myList):
    query = f'SELECT * FROM {table_name}'
    total_variable.execute(query)
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        myList.append(variable[1])
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    return myList  # Retourner 0 si aucun résultat n'est trouvé   

def fetch_drop(table_name,total_variable,myList):
    query = f'SELECT * FROM {table_name}'
    total_variable.execute(query)
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        myList.append(f'{variable[0]}-{variable[1]}')
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
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
    

    export_button = ctk.CTkButton(
        master=title_frame,
        text=" Excel تصدير إلى ",
        font=font_arial,
        fg_color="#3eecfa",
        text_color="#333",
        hover_color="#f0f0f0",
        corner_radius=2,
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
        corner_radius=2,
        command=import_from_excel
    )    # import_button.pack(pady=10,anchor="e",padx=(10,40),)

    # import_button.grid(row=0, column=1, sticky="e", padx=5, pady=5)
    import_button.pack(side="left",padx=5)
    export_button.pack(side="left")


# def create_products_frame(root,user=None):
#     products_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

#     show_title_frame(products_frame)

#     show_products_table(products_frame,is_admin = user[4] if user else 1)
#     return products_frame

def create_products_frame(root):
    products_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

    # Titre
    show_title_frame(products_frame)

    # Frame pour le tableau des produits
    table_frame = ctk.CTkFrame(products_frame, fg_color="#fff")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def set_user(user):
        # Nettoyer la frame avant d'afficher un nouveau tableau
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Afficher le tableau des produits en fonction de l'utilisateur
        is_admin = user[4] if user else 0
        show_products_table(table_frame, is_admin=is_admin)

    # Ajouter la méthode set_user à la frame
    products_frame.set_user = set_user

    return products_frame

# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# products_frame = create_products_frame(window)
# products_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()