import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pymysql
def connect_db():
    try:
        # create a connection object
        global connect
        global my_cursor
        global categories
        global suppliers
        global warehouses

        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        categories = connect.cursor()
        suppliers = connect.cursor()
        warehouses = connect.cursor()
        
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
        
def fetch_total(table_name,total_variable,myList):
    query = f'SELECT * FROM {table_name}'
    total_variable.execute(query)
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        myList.append(f'{variable[0]}-{variable[1]}')
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    return myList  # Retourner 0 si aucun résultat n'est trouvé   

# import
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

def create_add_product_frame(root):
    
    add_product_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    add_product_frame.pack(padx=400,pady=1,ipady=10,)
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(add_product_frame,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # first frame labels
    first_frame = ctk.CTkFrame(add_product_frame,fg_color='transparent',width=400)
    first_frame.pack(ipady=10 , padx=20,fill='x')
    first_frame.columnconfigure((0,1), weight=1, uniform='equal') 
    
    # first frame entries
    first_frame_entries = ctk.CTkFrame(add_product_frame,fg_color='transparent',width=400)
    first_frame_entries.pack(ipady=10 , padx=20,fill='x')
    first_frame_entries.columnconfigure((0,1), weight=1, uniform='equal')
    
    # name
    create_label(first_frame,"اسم المنتج").grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2, )
    name_entry = create_entry(first_frame_entries)
    name_entry.grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2, padx=(5,0))
    
    # Desc
    create_label(first_frame,"وصف المنتج").grid(sticky="news",row = 0, column = 0, ipady=10 , pady=2, )
    desc_entry = create_entry(first_frame_entries)
    desc_entry.grid(sticky="news",row = 0, column = 0, ipady=10 , pady=2, padx=(5,0))
    
    # prices labels frame
    price_lab = ctk.CTkFrame(add_product_frame,fg_color='transparent',width=400)
    price_lab.pack(ipady=10 , padx=20,fill='x')
    price_lab.columnconfigure((0,1,2), weight=1, uniform='equal')
    # price_lab.columnconfigure((0,1,2), weight=1, uniform='a')
    
    # prices entries frame
    prices_entry = ctk.CTkFrame(add_product_frame,fg_color='transparent',width=400)
    prices_entry.pack(ipady=10 , padx=20,fill='x')
    prices_entry.columnconfigure((0,1,2), weight=1, uniform='a')
    
    # prices
    create_label(price_lab,"سعر المنتج").grid(sticky="news",row = 0, column = 2, ipady=10 , pady=2, )
    price_entry = create_entry(prices_entry)
    price_entry.grid(sticky="news",row = 0, column = 2,ipady=10 , pady=2, padx=(5,0),  )
    
    create_label(price_lab,"سعر البيع").grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2, )
    sell_price_entry = create_entry(prices_entry)
    sell_price_entry.grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2,padx=(5,0)  )
    
    create_label(price_lab,"سعر الشراء").grid(sticky="news",row = 0, column = 0, ipady=10 , pady=2, )
    buy_price_entry = create_entry(prices_entry)
    buy_price_entry.grid(sticky="news",row = 0, column = 0, ipady=10 , pady=2, padx=(5,0),)
    
    # dropdowns label frame
    dropdowns_lab = ctk.CTkFrame(add_product_frame,fg_color='transparent',width=400)
    dropdowns_lab.pack(ipady=10 , padx=20,fill='x')
    dropdowns_lab.columnconfigure((0,1,2), weight=1, uniform='equal')
    
    # dropdowns entries frame
    dropdowns_entry = ctk.CTkFrame(add_product_frame,fg_color='transparent',width=400)
    dropdowns_entry.pack(ipady=10 , padx=20,fill='x')
    dropdowns_entry.columnconfigure((0,1,2), weight=1, uniform='a')

    connect_db()
    list_of_categories = []
    fetch_total('product_categories',categories, list_of_categories)

    category_label = create_label(dropdowns_lab,"القسم ")
    category_label.grid(sticky="news",row = 0, column = 2, ipady=10 , pady=2, )
    
    category_entry = ctk.CTkOptionMenu(
        dropdowns_entry,values=list_of_categories,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        font=font_arial,dropdown_font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',

    )
    category_entry.grid(sticky="news",row = 0, column = 2,ipady=10 , pady=2, padx=(15,0),  )
    
    
    # supplier
    list_of_suppliers = []
    fetch_total('suppliers',suppliers, list_of_suppliers)
    
    #supplier
    supplier_label = create_label(dropdowns_lab,"المورد ")
    supplier_label.grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2, )

    supplier_entry = ctk.CTkOptionMenu(
        dropdowns_entry,values=list_of_suppliers,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        font=font_arial,
    )
    supplier_entry.grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2,padx=(15,0)  )
    
    
    # warehouse
    list_of_warehouses = []
    fetch_total('warehouses',warehouses, list_of_warehouses)

    warehouse_label = create_label(dropdowns_lab,"المخزن ")
    warehouse_label.grid(sticky="news",row = 0, column = 0, ipady=10 , pady=2, )

    warehouse_entry = ctk.CTkOptionMenu(
        dropdowns_entry,values=list_of_warehouses,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        font=font_arial,
    )
    warehouse_entry.grid(sticky="news",row = 0, column = 0, ipady=10 , pady=2, padx=(15,0),)
    
    # second frame  labels
    second_frame = ctk.CTkFrame(add_product_frame,fg_color='transparent',width=400)
    second_frame.pack(ipady=10 , padx=20,fill='x')
    second_frame.columnconfigure((0,1,2,3), weight=1, uniform='a')
    
    # second frame entries
    second_frame_entry = ctk.CTkFrame(add_product_frame,fg_color='transparent',width=400)
    second_frame_entry.pack(ipady=10 , padx=20,fill='x')
    second_frame_entry.columnconfigure((0,1,2,3), weight=1, uniform='a')
    
    code_label = create_label(second_frame,"الكود ")
    code_label.grid(sticky="news",row = 0, column =3, ipady=10 , pady=2, )
    
    code_entry = create_entry(second_frame_entry)
    code_entry.grid(sticky="news",row = 0, column =3,ipady=10 , pady=2, padx=(5,0),  )
    
    # unit
    unit_label = create_label(second_frame,"الوحدة ")
    unit_label.grid(sticky="news",row = 0, column = 2, ipady=10 , pady=2, )
    
    unit_entry = create_entry(second_frame_entry)
    unit_entry.grid(sticky="news",row = 0, column = 2,ipady=10 , pady=2, padx=(5,0)  )
    
    
    # qty
    qty_label = create_label(second_frame,"الكمية ")
    qty_label.grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2, )
    
    qty_entry = create_entry(second_frame_entry)
    qty_entry.grid(sticky="news",row = 0, column = 1,ipady=10 , pady=2, padx=(5,0),  )

    # min quantity
    min_qty_label = create_label(second_frame,"الكمية الادنى ")
    min_qty_label.grid(sticky="news",row = 0, column = 0, ipady=10 , pady=2, )
    
    min_qty_entry = create_entry(second_frame_entry)
    min_qty_entry.grid(sticky="news",row = 0, column = 0,ipady=10 , pady=2, padx=(5,0),  )
    
    # pour table purchases
    # third frame  labels
    third_frame = ctk.CTkFrame(add_product_frame,fg_color='transparent',width=400)
    third_frame.pack(ipady=10 , padx=20,pady=0,fill='x')
    third_frame.columnconfigure((0,1), weight=1, uniform='equal') 
    
    
    # calendar
    created_at_label = create_label(third_frame,"تاريخ الاضافة ").grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2, )
    
    date_entry = DateEntry(third_frame,width=30, background='white',font=font_arial,
                                foreground='black', justify='center', date_pattern='yyyy-mm-dd',)
    date_entry.grid(sticky="news",row = 0, column = 0, ipady=10 , pady=2, padx=(5,0))
    
    def add_products():
        name = name_entry.get()
        description = desc_entry.get()
        price = float(price_entry.get())
        purchase_price = float(buy_price_entry.get())
        selling_price = float(sell_price_entry.get())
        category = category_entry.get().split('-')[0]
        supplier = supplier_entry.get().split('-')[0]
        warehouse = warehouse_entry.get().split('-')[0]
        code = code_entry.get()
        unit = unit_entry.get()
        min_qty = float(min_qty_entry.get())
        quantity = float(qty_entry.get())
        reference = generate_reference()
        date = date_entry.get_date()
    
        if name == "" or description == "" or price == "" or purchase_price == "" or quantity == '' or min_qty == '':
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            connect_db()
            
            # Check if a purchase exists for this supplier today
            my_cursor.execute("SELECT id FROM purchases WHERE supplier_id = %s AND DATE(created_at) = CURDATE()", (supplier,))
            existing_purchase = my_cursor.fetchone()
            
            if existing_purchase:
                # Update existing purchase
                pur_id = existing_purchase[0]
                query = '''UPDATE purchases SET date = %s, payment_method = 'cash', reference_number = %s WHERE id = %s'''
                my_cursor.execute(query, (date, reference, pur_id))
            else:
                # Create new purchase
                my_cursor.execute("INSERT INTO purchases (date, supplier_id, payment_method, reference_number, created_at) VALUES (%s, %s, 'cash', %s, NOW())", (date, supplier, reference))
                pur_id = my_cursor.lastrowid
                # print("New purchase created with ID:", pur_id)
                

            # Insert new product
            query = '''INSERT INTO products (name, description, price, purchase_price, category_id, supplier_id, warehouse_id, code, selling_price,
            quantity, min_quantity, is_active, created_at, purchase_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, NOW(), %s)'''
            my_cursor.execute(query, (name, description, price, purchase_price, category, supplier, warehouse, code, selling_price, quantity, min_qty, pur_id))

            connect.commit()
            messagebox.showinfo('نجاح', 'تم اضافة المنتج بنجاح')
            
            result = messagebox.askyesno('تم الاضافة', 'هل تريد اضافة منتج جديد?', parent=add_product_frame)
            if result:
                for entry in [name_entry, desc_entry, price_entry, sell_price_entry, code_entry, unit_entry, buy_price_entry, qty_entry, min_qty_entry]:
                    entry.delete(0, tk.END)
            
    add_button = ctk.CTkButton(
        add_product_frame,
        text="تاكيد",
        width=400,
        command=add_products,corner_radius=2,font=font_arial_title
            )
    add_button.pack(ipady=10 , padx=20,fill='x')
    
    return add_product_frame

import random
import uuid

def generate_reference():
    reference = str(uuid.uuid4()).upper()[0:4] + str(random.randint(1000, 9999))
    return reference

# Utilisation de la fonction pour générer un numéro de référence
reference = generate_reference()
print(reference)
# # window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# add_product_frame = create_add_product_frame(window)
# add_product_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()