import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pymysql
import os
from PIL import Image, ImageTk

from tkcalendar import DateEntry
from datetime import datetime
def connect_db():
    try:
        global connect
        global my_cursor
        global customers
        global products
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        customers = connect.cursor()
        products = connect.cursor()
        
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))



# Function to fetch sales with pagination
def fetch_sales(limit=10, offset=0):
    connect_db()
    query = f'''
    SELECT 
    s.id,
    c.name,
    s.reference_number,
    s.payment_method,
    sum(si.quantity),
    sum(si.subtotal),
    DATE(s.date)
    FROM 
    sales s 
    JOIN customers c ON s.customer_id = c.id 
    LEFT JOIN sale_items si ON s.id = si.sale_id
    GROUP BY 
    s.id
    order by (s.date)
    LIMIT {limit} OFFSET {offset}'''
    
    my_cursor.execute(query)
    return my_cursor.fetchall()

def fetch_sale(sale_id):
    connect_db()
    query = f'''
    SELECT *
    FROM sales  WHERE id = %s'''
    
    ''' '''
    
    my_cursor.execute(query, (sale_id,))
    result = my_cursor.fetchone()
    return result

def delete_sale(sale_id, update_callback):
    connect_db()
    try:
        query = f"DELETE FROM sales WHERE id = {sale_id}"
        my_cursor.execute(query)
        connect.commit()
        messagebox.showinfo('نجاح', 'تم  الحذف بنجاح')
        
        # Appel de la fonction pour actualiser les données
        update_callback()
    except Exception as e:
        messagebox.showerror('Error', str(e))

# Variable globale pour stocker les résultats de recherche
search_results = []
offset = 0


# Function to show sales as a styled table with pagination
def show_sales_table(root,parent,user=None, limit=10,is_admin=1):
    
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
            data = fetch_sales(limit, offset)
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
            
            show_image_path = os.path.join(os.path.dirname(__file__), "images", "bill.png")
            show_image = ctk.CTkImage(light_image=Image.open(show_image_path), size=(23, 23),)
            show_button = ctk.CTkButton(buttons_frame, text="",text_color="black",
                    image=show_image,
                    fg_color='#fff',border_color='#f0f0f0',border_width=1,corner_radius=2,
                    hover_color='#eee',
                    width=20,
                    font=font_arial_btn,    
                    command=lambda row=row:details_and_update(row[::-1][0],update_table)
                    )
            show_button.grid(row=0, column=2) if is_admin == 1 else show_button.grid_remove()
            
                
            edit_image_path = os.path.join(os.path.dirname(__file__), "images", "receipt.png")
            edit_image = ctk.CTkImage(light_image=Image.open(edit_image_path), size=(23, 23),)
            update_button = ctk.CTkButton(buttons_frame, text="",text_color="black",
                    image=edit_image,
                    fg_color='#fff',border_color='#f0f0f0',border_width=1,corner_radius=2,
                    hover_color='#eee',
                    width=20,
                    font=font_arial_btn,        
                    command=lambda row=row: open_update_window(row[::-1][0],update_table)
                    )
            update_button.grid(row=0, column=1,padx=5) if is_admin == 1 else update_button.grid_remove()
            
            
            delete_image_path = os.path.join(os.path.dirname(__file__), "images", "delete_invoice.png")
            delete_image = ctk.CTkImage(light_image=Image.open(delete_image_path), size=(23, 23),)
            delete_button = ctk.CTkButton(buttons_frame,
                text="",
                text_color="black",
                image=delete_image,
                fg_color='#fff',border_color='#f0f0f0',border_width=1,corner_radius=2,
                hover_color='#eee',
                font=font_arial_btn, 
                width=20,
                command=lambda row=row: delete_sale(row[::-1][0], update_table)
                )
            delete_button.grid(row=0, column=0, padx=5) if is_admin == 1 else delete_button.grid_remove()
    
    offset = 0

    # Search Frame
    search_frame(root,parent, lambda: update_table(),offset,limit)  # Appelle `update_table` comme callback
    # SELECT s.id,c.name,s.reference_number,s.payment_method,s.total_amount,s.discount,s.final_amount,s.date
    columns = ('رقم القطعة ', 'اسم العميل ', 'رقم الفاتورة', 'طريقة الدفع', ' الكمية',  'المبلغ النهائي', 'التاريخ')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="#fff",border_width=1,border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((0, 1, 2,3, 4, 5, 6,7), weight=1, uniform='a') if is_admin == 1 else header_frame.columnconfigure((0, 1, 2,3, 4, 5,6), weight=1, uniform='a')
    font_arial = ('Arial',14,'bold')

    # Add column headings
    for col_index, col_name in enumerate(columns):
        label = ctk.CTkLabel(
            header_frame,
            text=col_name,
            font=font_arial,
            text_color="black",
            # fg_color="#eee",
            corner_radius=1,
            width=100
        )
        action_lab =ctk.CTkLabel(
            header_frame,
            text='الاجراءات',
            font=font_arial,
            text_color="black",
            # fg_color="#eee",
            # fg_color="#fff",
            corner_radius=1,
            width=100
        )
        action_lab.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)if is_admin == 1 else action_lab.grid_remove()
        label.grid(row=0, column=col_index+1 if is_admin == 1 else col_index, sticky="nsew", padx=5, pady=5)

    # Data Frame
    data_frame = ctk.CTkFrame(parent, corner_radius=2,  fg_color="#fff",border_width=1,border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6,7), weight=1, uniform='a') if is_admin == 1 else data_frame.columnconfigure((0, 1, 2,3, 4, 5,6), weight=1, uniform='a')

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
def search_frame(root,parent, refresh_callback,offset,limit):
    """Crée une barre de recherche avec options."""
    s_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white")
    s_frame.pack(fill='x', padx=20, pady=5)

    # s_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')

    font_arial = ('Arial',18,)
    search_entry = ctk.CTkEntry(
        s_frame,
        placeholder_text="إبحث عن اسم العميل او رقم الفاتورة او طريقة الدفع ",
        fg_color="white",
        bg_color="white",
        border_color="#e5e3e0",
        border_width=1,
        width=300,
        corner_radius=0,
        font=('Arial',15,),
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
        command=lambda: search(search_entry.get(),refresh_callback,limit,offset)
    )
    search_button.pack(side="right", pady=5, ipadx=5, ipady=5)

        # Option Menus
    image_path = os.path.join(os.path.dirname(__file__), "images", "refresh.png")
    
    image = ctk.CTkImage(light_image=Image.open(image_path), size=(20, 20),)

    refresh_button = ctk.CTkButton(
        s_frame,
        image=image,
        text="تحديث",
        fg_color="#fff",
        hover_color="#f0f0f0",
        font=font_arial,corner_radius=2,
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
def search(query,refresh_callback,limit=10, offset=0):
    global search_results  # Déclarer `search_results` comme global
    if not query:
        messagebox.showinfo('تنبيه', 'لا يمكنك البحث عن نتيجة فارغة')
        search_results = []  # Vider les résultats si la recherche est vide
    else:
        connect_db()
        sql_query = '''
        SELECT 
        s.id,
        c.name,
        s.reference_number,
        s.payment_method,
        sum(si.quantity),
        sum(si.subtotal),
        DATE(s.date)
        FROM 
        sales s 
        JOIN customers c ON s.customer_id = c.id 
        LEFT JOIN sale_items si ON s.id = si.sale_id
        where s.reference_number = %s or c.name = %s or s.payment_method = %s 
        GROUP BY 
        s.id
        order by (s.date)
        '''
        # query = f'SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location FROM sales p JOIN sale_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id LIMIT {limit} OFFSET {offset}'
        
        my_cursor.execute(sql_query, (query, query,query))
        search_results = my_cursor.fetchall()  # Récupérer les résultats
        refresh_callback()  # Appeler la fonction de rafraîchissement pour afficher les nouvelles données

def sale_items(id):
    """Afficher les articles d'une vente."""
    connect_db()
    sql_query = '''
    SELECT p.name, s.quantity, p.price, s.subtotal from sale_items s
    JOIN products p ON s.product_id = p.id
    WHERE sale_id = %s
    '''
    my_cursor.execute(sql_query, (id,))
    items = my_cursor.fetchall()
    print('results::', items,id)
    return items


def search_product(id):
    connect = connect_db()
    cursor = connect.cursor()
    
    query = "SELECT * FROM products WHERE id = %s or name = %s OR code = %s"
    cursor.execute(query, (id, id, id))
    
    result = cursor.fetchone()
    if result is None:
        messagebox.showinfo('تنبيه', 'المنتج غير موجود في قاعدة البيانات.')
        
    cursor.close()
    connect.close()
    
    return result

def search_sale_item(id):
    """Afficher les articles d'une vente."""
    connect_db()
    sql_query = '''
    SELECT p.name, s.quantity, p.selling_price, s.subtotal from sale_items s
    JOIN products p ON s.product_id = p.id
    WHERE sale_id = %s or product_id = %s
    '''
    my_cursor.execute(sql_query, (id,id))
    items = my_cursor.fetchall()
    print('results::', items,id)
    return items


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


import pandas as pd
def export_to_excel():
    connect_db()
    query = f'''
    SELECT 
    s.id,
    c.name as  العميل,
    s.reference_number as رقم_الفاتورة,
    s.payment_method as طريقة_الدفع,
    sum(si.quantity) as الكمية,
    sum(si.subtotal) as المبلغ,
    DATE(s.date) as تاريخ
    FROM 
    sales s 
    JOIN customers c ON s.customer_id = c.id 
    LEFT JOIN sale_items si ON s.id = si.sale_id
    GROUP BY 
    s.id
    order by (s.date)'''
    df = pd.read_sql(query, connect)
    df.to_excel('invoices.xlsx', index=False)
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


def show_title_frame(parent, ):
    
    # Table headers

    # Header frame
    title_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="transparent",)
    title_frame.pack(fill='x', padx=20, pady=5,)
    title_frame.columnconfigure((0, 1, 2,3, 4, 5, 6), weight=1, uniform='a',)
    
    
    font_arial_title = ('Arial',20,'bold')
    font_arial = ('Arial',12,)

    title_label = ctk.CTkLabel(
        master=title_frame,
        text="ادارة المبيعات",
        font=font_arial_title,
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


    
# def create_sales_frame(root,user=None):
#     sales_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

#     show_title_frame(sales_frame)

#     show_sales_table(root,sales_frame,user=user,is_admin = user[4] if user else 0)
#     return sales_frame

def create_sales_frame(root):
    sales_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

    # Titre
    show_title_frame(sales_frame)

    # Frame pour le tableau des catégories
    table_frame = ctk.CTkFrame(sales_frame, fg_color="#fff")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def set_user(user):
        # Nettoyer la frame avant d'afficher un nouveau tableau
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Afficher le tableau des catégories en fonction de l'utilisateur
        is_admin = user[4] if user else 0
        show_sales_table(root,table_frame, is_admin=is_admin)

    # Ajouter la méthode set_user à la frame
    sales_frame.set_user = set_user

    return sales_frame
        
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
    entry = ctk.CTkEntry(parent, justify=justify,font=font_arial, fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=2)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text)
    label_widgets.append(label)
    return label

entry1_widget = []  

def change(symbol):
    global change_value
    if symbol == '+' :
        change_value += 1 
    else:
        change_value -= 1 
    update_entry()
def update_entry():
    for entry in entry1_widget:
        if entry.winfo_exists():
            var_change = tk.StringVar(value=change_value) 
            entry.configure(textvariable=var_change)

# for entries
change_value = 0
def create_entry1(parent,wid=200):
    var_change = tk.StringVar(value=change_value) 
    entry = ctk.CTkEntry(parent,font=("Arial", 14), fg_color='#fff', border_width=1,justify='center',
                        border_color='#ddd', corner_radius=1, width=100,textvariable=var_change)
    entry1_widget.append(entry)
    return entry

import re
def error_message(parent,text):
    message = ctk.CTkLabel(parent, text="", text_color="red", font=("Arial", 12),height=10)
    return message

def open_update_window(sale, update_callback):
    update_window = tk.Toplevel(background='#fff')
    # update_window.pack()
    update_window.title("تعديل ")
    
    print("Update:",sale)
    sale = fetch_sale(sale)
        # Créer un conteneur scrollable
    canvas = ctk.CTkCanvas(update_window, width=800, height=930)
    canvas.pack( fill="both", expand=True)

    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 12)
    # Créer un frame pour contenir les champs du formulaire
    frame = ctk.CTkFrame(canvas, fg_color='#fff',)
    canvas.create_window((0,0), window=frame, anchor="center", width=799, )
    # frame.columnconfigure((0,1,2), weight=1, uniform='a')
    
    # first frame labels
    first_frame = ctk.CTkFrame(frame,fg_color='transparent',width=400)
    first_frame.pack(ipady=10 , padx=20,fill='x',expand=True,pady=20)
    first_frame.columnconfigure((0,1), weight=1, uniform='equal') 
    
    # first frame entries
    first_frame_entries = ctk.CTkFrame(frame,fg_color='transparent',width=400)
    first_frame_entries.pack(ipady=10 , padx=20,fill='x')
    first_frame_entries.columnconfigure((0,1), weight=1, uniform='equal')

    connect_db()
    # customer
    list_of_customers = []
    fetch_total('customers',customers, list_of_customers)
    
    #customer
    customer_label = create_label(first_frame,"العميل")
    customer_label.grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2, )

    customer_entry = ctk.CTkOptionMenu(
        first_frame_entries,values=list_of_customers,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        font=font_arial,
    )
    customer_entry.grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2,padx=(15,0)  )
    
    # date
    date_label = create_label(first_frame,"تاريخ ")
    date_label.grid(sticky="news",row = 0, column = 0, ipady=10 , pady=2, )
    
    date_entry = DateEntry(first_frame_entries, width=30, background='white',font=font_arial,
                                foreground='black', justify='center', date_pattern='yyyy-mm-dd',)
    date_entry.grid(row = 0, column = 0, ipady=10 , pady=2, padx=20, )
    
        
    # second frame  labels
    second_frame = ctk.CTkFrame(frame,fg_color='transparent',width=400)
    second_frame.pack(ipady=10 , padx=20,fill='x')
    
    # second frame entries
    second_frame_entry = ctk.CTkFrame(frame,fg_color='transparent',width=400)
    second_frame_entry.pack(ipady=10 , padx=20,fill='x')

    # status
    print("status Sale:",sale)
    create_label(second_frame," الحالة").pack(ipady=10 , fill='x',expand = True,side='right')    
    status_entry = create_entry(second_frame_entry)
    status_entry.insert(0, sale[3])
    status_entry.pack(ipady=10 , padx=2,fill='x',expand = True,side='right')
    
    # pay method
    create_label(second_frame,"طريقة الدفع").pack(ipady=10 , fill='x',expand = True,side='left')
    
    payment_method_entry = create_entry(second_frame_entry)
    payment_method_entry.insert(0, sale[4])
    payment_method_entry.pack(ipady=10 , padx=2,fill='x',expand = True,side='left')

    
    error_frame = ctk.CTkFrame(frame,fg_color='transparent',width=400,height=20)
    error_frame.pack(ipady=10 , padx=20,fill='x')
    
    
    # Label d'erreur pour le nom
    status_error_label = error_message(error_frame,"")
    status_error_label.pack( padx=2,fill='x',expand = True,side='right')

    # Label d'erreur pour le nom
    payment_method_error_label = error_message(error_frame,"")
    payment_method_error_label.pack( padx=2,fill='x',expand = True,side='left')
    
    # payment_method and reference_number
    create_label(frame,"رقم الفاتورة").pack(ipady=10 , padx=20,fill='x',pady=5)
    
    reference_number_entry = create_entry(frame)
    reference_number_entry.insert(0, sale[5])
    reference_number_entry.pack(ipady=10 , fill='x',pady=5,padx=20,)
    
    
    ref_num_error = error_message(frame, "")
    ref_num_error.pack( fill='x',pady=5,padx=20,)
    # note
    create_label(frame,"ملاحظات").pack(ipady=10 , padx=20,fill='x',pady=5)
    
    note_entry = create_entry(frame)
    note_entry.insert(0, sale[6])
    note_entry.pack(ipady=10 , fill='x',pady=(5,0),padx=20,)
    
    # Bouton pour sauvegarder les modifications
    def validate_string(input_str):
        # Cette regex vérifie que l'entrée contient uniquement des lettres et des espaces
        return bool(re.match(r'^[A-Za-z\s]+$', input_str))


    def save_changes():
        customer = customer_entry.get()[0]
        date = date_entry.get_date().strftime('%Y-%m-%d') if date_entry.get_date() else None
        status = status_entry.get()
        payment_method = payment_method_entry.get()
        reference_number = reference_number_entry.get()
        note = note_entry.get()
        sale_id = sale[0]
        
        # Réinitialiser les messages d'erreur
        status_error_label.configure(text="")
        payment_method_error_label.configure(text="")
        ref_num_error.configure(text="")
        
        # Validation des champs
        has_error = False
        
        # Validation du champ "status"
        if not validate_string(status):
            status_error_label.configure(text="ادخل حالة صحيح (حروف فقط)")
            has_error = True
        
        # Validation du champ "payment_method"
        if not validate_string(payment_method):
            payment_method_error_label.configure(text="ادخل طريقة الدفع صحيحة (حروف فقط)")
            has_error = True
        
        if reference_number == '':
            ref_num_error.configure(text="ادخل رقم المرجع")
            has_error = True
        

        # Si une erreur est détectée, arrêter la fonction
        if has_error:
            return
        
        try:
            connect_db()
            print('Data:',customer,date,status,payment_method,reference_number,note,sale_id)
            query = '''
            UPDATE sales SET
            customer_id=%s,
            date=%s,
            status=%s,
            payment_method=%s,
            reference_number=%s,
            notes=%s
            WHERE id=%s'''
            
            my_cursor.execute(query, (customer,date,status,payment_method,reference_number,note,sale_id))
            connect.commit()
            messagebox.showinfo('نجاح', ' تم تحديث البيانات بنجاح')
        except Exception as e:
            print(e)
            messagebox.showerror('خطاء', 'حدث خطاء في تحديث البيانات')
            return
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(frame, text="حفظ", command=save_changes,font=font_arial_title,corner_radius=2).pack(ipady=10 , fill='x',pady=(20,100),padx=20,)
        # Mettre à jour la taille du frame pour qu'il soit visible dans le canvas
    frame.update_idletasks( )
    canvas.configure(scrollregion=canvas.bbox("all"))

def details_and_update(sale_id,update_callback):
    print('sale_id:',sale_id)
    saleItems = []
    saleItems= search_sale_item(sale_id)
    global inv_data
    inv_data = saleItems
    print('D1: ', saleItems)
    window = tk.Toplevel(background='#fff')
    # window.pack()
    window.title("إضافة ")
    
    # Créer un conteneur scrollable
    canvas = ctk.CTkCanvas(window, width=800, height=930)
    canvas.pack( fill="both", expand=True)

    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 12)
    # Créer un frame pour contenir les champs du formulaire
    frame = ctk.CTkFrame(canvas, fg_color='#fff',)
    canvas.create_window((0,0), window=frame, anchor="center", width=799, )
    # frame.columnconfigure((0,1,2), weight=1, uniform='a')
    

    # first frame labels
    first_frame = ctk.CTkFrame(frame,fg_color='transparent',width=400)
    first_frame.pack(ipady=10 , padx=20,fill='x',expand=True,pady=(20,0))
    
    # first frame entries
    first_frame_entry = ctk.CTkFrame(frame,fg_color='transparent',width=400)
    first_frame_entry.pack(ipady=10 , padx=20,fill='x',expand=True,pady=10)
    # products
    connect_db()
    list_of_products = []
    fetch_total('products',products, list_of_products)
    
    #product
    create_label(first_frame,"المنتجات").pack(ipady=10 , fill='x',expand = True,side='right')

    product_entry = ctk.CTkOptionMenu(
        first_frame_entry,values=list_of_products,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        font=font_arial,
    )
    product_entry.pack(ipady=10 , fill='x',expand = True,side='right')  
    
    # quantity
    create_label(first_frame," الكمية").pack(ipady=10 , fill='x',expand = True,side='left')  
    # quantity_entry = create_entry1(first_frame_entry)
    btn = ctk.CTkButton(first_frame_entry,font=('Ariel',20),text='+',width=45,height=42,corner_radius=1,fg_color='#eee',hover_color='#fff',
    text_color='#333',command=lambda:change('+')).pack(pady=10,padx=(0,10),side='right')
    
    quantity_entry = create_entry1(first_frame_entry)
    quantity_entry.pack(ipady=10,fill = 'x',side='right',anchor='center')
    
    btn = ctk.CTkButton(first_frame_entry,font=('Ariel',20),text='-',width=45,height=42,corner_radius=1,fg_color='#eee',hover_color='#fff',
        text_color='#333',command=lambda:change('-')).pack(pady=10,padx=(10,0),side='right')
    
    def add_product():
        global inv_data
        global total_amount
        global final_total
        global change_value
    
        id = product_entry.get().split('-')[0]
        print('ID:', id)
        result = search_product(id)
    
        if result and float(quantity_entry.get()) > 0:
            print('Result:', result)
    
            # Ensure inv_data is a list
            if isinstance(inv_data, tuple):
                inv_data = list(inv_data)
            product_code = result[1]
            quantity = float(quantity_entry.get())
            price = float(result[11])
            total = quantity * price
    
            # Check if product already exists in inv_data
            product_exists = False
            for index, item in enumerate(inv_data):
                if item[0] == product_code:
                    print('Item:', item)
                    existing_quantity = item[1]
                    new_quantity = existing_quantity + quantity
                    inv_data[index] = (item[0], new_quantity, price, new_quantity * price)
                    product_exists = True
                    break
    
            # If product doesn't exist, add it as a new entry
            if not product_exists:
                inv_data.append((product_code, quantity, price, total))
    
            print('inv_data:', inv_data)
    
            # Update display
            update_inv_table()
            quantity_entry.delete(0, 'end')
            quantity_entry.insert(0, '0')
            
            change_value = 0
    
        else:
            messagebox.showinfo('تحذير', 'المنتج غير موجود')

    
    add_prod = ctk.CTkButton(
        first_frame_entry,
        text="أضف",
        width=40,
        corner_radius=4,
        fg_color='#333',
        text_color='#fff',hover_color='#444',
        command=add_product
    )
    add_prod.pack(ipady=10,expand = False,side='left')
    
    title_label = ctk.CTkLabel(frame, text="المنتجات المضافة", font=('Ariel', 20, 'bold'))
    title_label.pack(pady=10)
    def recalculate_totals():
        global total_amount, total_qty

        # Recalculer le montant total
        total_amount = sum(item[3] for item in inv_data)  # item[3] = total pour chaque ligne
        total_qty = sum(item[1] for item in inv_data) 
        print(total_qty,'item:',inv_data)



    def update_inv_table():
        # Clear previous table data
        for widget in data_frame.winfo_children():
            widget.destroy()
        data = inv_data

        # Ajouter les nouvelles données dans la table
        for row_index, row in enumerate(data):
            row = list(row)  # Convertir le tuple en liste
            row.reverse()  # Inverser les colonnes pour l'affichage
            for col_index, value in enumerate(row):
                label = ctk.CTkLabel(
                    data_frame,
                    text=value,
                    font=('Arial', 12.5),
                    anchor='e',
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                label.grid(row=row_index, column=col_index+1, sticky="nsew", padx=5, pady=1)

            # Ajouter le bouton de suppression
            delete_image_path = os.path.join(os.path.dirname(__file__), "images", "delete_invoice.png")
            delete_image = ctk.CTkImage(light_image=Image.open(delete_image_path), size=(23, 23),)
            delete_button = ctk.CTkButton(data_frame,
                text="",
                text_color="black",
                image=delete_image,
                fg_color='#fff',
                # bg_color='#fff',
                hover_color='#eee',
                width=20,
                font=('Arial',15),
                command=lambda row=row: delete_item(row[::-1]),
            )
            delete_button.grid(row=row_index, column=0, padx=5, pady=1)
            
            def delete_item(row):
                global inv_data
                inv_data = saleItems
                if not inv_data:
                    messagebox.showerror("Error", "No products added yet.")
                    return
                try:
                    connection = connect_db()
                    with connection.cursor() as cursor:
                        
                        prod = search_product(row[0])
                        print("Product founded:", prod)
                        id = prod[0]
                        cursor.execute("SELECT id, quantity FROM sale_items WHERE sale_id = %s AND product_id = %s", (sale_id, id))
                        is_existe = cursor.fetchone()
                        print("Is Ex",is_existe)
                        if is_existe:
                            query = "delete from sale_items where id= %s"
                            cursor.execute(query, (is_existe[0]))
                            
                            # Augmenter la quantité du produit
                            query = "UPDATE products SET quantity = quantity + %s WHERE id = %s"
                            cursor.execute(query, (is_existe[1], id))
                            
                            connection.commit()
                    
                    messagebox.showinfo("نجاح", "تم الحذف بنجاح")
                    # je veux remove le row dans le list inv_data
                    inv_data = [item for item in inv_data if item[0] != row[0]]
                    print('INv:',inv_data)
                    update_inv_table()
            
                    
                except pymysql.Error as e:
                    connection.rollback()
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                except Exception as e:
                    messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
                finally:
                    if connection:
                        connection.close()
                update_callback()
        # Recalculer et mettre à jour les totaux
        recalculate_totals()
        update_totals_display()
    columns = ('المنتج', 'الكمية', 'السعر', 'المجموع','حذف')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((0, 1, 2, 3,4), weight=1, uniform='a')
    font_arial = ('Arial', 14, 'bold')

    # Add column headings
    for col_index, col_name in enumerate(columns):
        label = ctk.CTkLabel(
            header_frame,
            text=col_name,
            font=font_arial,
            anchor='e',
            text_color="black",
            fg_color="#fff",
            corner_radius=5,
            width=100
        )
        label.grid(row=0, column=col_index, sticky="nsew", padx=5, pady=5)

    # Data frame
    data_frame = ctk.CTkFrame(frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure((0, 1, 2, 3,4), weight=1, uniform='a')
    
    total_frame = ctk.CTkFrame(frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    total_frame.pack(fill='x', padx=20, pady=5)
    
    def update_totals_display():
        # Mettre à jour les valeurs affichées pour les totaux
        for widget in total_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(total_frame, text=round(total_amount, 2), font=('Arial', 15, 'bold')).pack(side='left', expand=True)
        ctk.CTkLabel(total_frame, text=": المجموع", font=('Arial', 15, 'bold')).pack(side='left', padx=10, pady=5)

        ctk.CTkLabel(total_frame, text=": الكمية", font=('Arial', 15, 'bold')).pack(side='right', padx=10, pady=5)
        ctk.CTkLabel(total_frame, text=total_qty, font=('Arial', 15, 'bold')).pack(side='right', expand=True)

    def add_invoice():
        global inv_data
        if not inv_data:
            messagebox.showerror("Error", "No products added yet.")
            return

        try:
            connection = connect_db()
            with connection.cursor() as cursor:
                for item in inv_data:
                    prod = search_product(item[0])
                    print("Product found:", prod)
                    if not prod:
                        raise ValueError(f"Product with ID {item[0]} not found")
                    
                    prod_id = prod[0]

                    # Check if the item already exists in sale_items
                    cursor.execute("SELECT id, quantity FROM sale_items WHERE sale_id = %s AND product_id = %s", (sale_id, prod_id))
                    existing_item = cursor.fetchone()

                    if existing_item:
                        print(f"Updating existing item: {item}")
                        query = "UPDATE sale_items SET quantity = %s,  subtotal = %s WHERE id = %s"
                        cursor.execute(query, (item[1], item[3], existing_item[0]))

                        # Calculer la différence entre la quantité actuelle et la nouvelle quantité
                        quantity_diff = item[1] - existing_item[1]

                        # Mettre à jour la quantité du produit
                        query = "UPDATE products SET quantity = quantity - %s WHERE id = %s"
                        cursor.execute(query, (quantity_diff, prod_id))
                    else:
                        print(f"Inserting new item: {item}")
                        query = "INSERT INTO sale_items (sale_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)"
                        cursor.execute(query, (sale_id, prod_id, item[1], item[3]))

                        # Mettre à jour la quantité du produit
                        query = "UPDATE products SET quantity = quantity - %s WHERE id = %s"
                        cursor.execute(query, (item[1], prod_id))

                connection.commit()

            messagebox.showinfo('نجاح', 'تم اضافة/تحديث المنتجات بنجاح')
            inv_data = []            
            update_inv_table()
            update_callback()
            window.destroy()

        except pymysql.Error as e:
            connection.rollback()
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
            print(f"Database Error: {str(e)}")  # For debugging
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            print(f"Value Error: {str(e)}")  # For debugging
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
            print(f"Unexpected Error: {str(e)}")  # For debugging
        finally:
            if connection:
                connection.close()                
    add_button = ctk.CTkButton(
        frame,
        text="تاكيد",
        width=400,font=font_arial_title,
        corner_radius=4,
        command=add_invoice
    )
    add_button.pack(pady=(10,140), ipady=10, padx=20, fill='x') 

    # update the
    update_inv_table()

    # ctk.CTkButton(frame, text="حفظ", command=save_changes,).pack(ipady=10 , fill='x',pady=(20,100),padx=20,)
        # Mettre à jour la taille du frame pour qu'il soit visible dans le canvas
    frame.update_idletasks( )
    canvas.configure(scrollregion=canvas.bbox("all"))

inv_data = []  # Change this to a list instead of a tuple
total_amount = 0
total_qty = 0

#     return sale_frame
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# sales_frame = create_sales_frame(window)
# sales_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()