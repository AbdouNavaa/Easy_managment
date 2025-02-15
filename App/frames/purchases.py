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
        global suppliers
        global products
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        suppliers = connect.cursor()
        products = connect.cursor()
        
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))



# Function to fetch purchases with pagination
def fetch_purchases(limit=10, offset=0):
    connect_db()
    query = f'''
    SELECT 
    s.id,
    sp.name,
    s.reference_number,
    s.payment_method,
    sum(p.quantity),
    sum(p.quantity * p.purchase_price),
    DATE(s.date)
    FROM 
    purchases s 
    JOIN suppliers sp ON s.supplier_id = sp.id 
    LEFT JOIN products p ON s.id = p.purchase_id
    GROUP BY 
    s.id
    order by (s.date)
    LIMIT {limit} OFFSET {offset}'''
    
    my_cursor.execute(query)
    return my_cursor.fetchall()

def fetch_purchase(purchase_id):
    connect_db()
    query = f'''
    SELECT *
    FROM purchases  WHERE id = %s'''
    
    ''' '''
    
    my_cursor.execute(query, (purchase_id,))
    result = my_cursor.fetchone()
    return result

def delete_purchase(purchase_id, update_callback):
    connect_db()
    try:
        query = f"DELETE FROM purchases WHERE id = {purchase_id}"
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


# Function to show purchases as a styled table with pagination
def show_purchases_table(root,parent,user=None, limit=10,is_admin=1):
    
    print('Is Admin:',is_admin)
    def load_page(page_num):
        nonlocal offset
        offset = (page_num - 1) * limit
        update_table()

    def update_table():
        global search_results
        print("update_table")
        # Si des résultats de recherche existent, les utiliser   
        if search_results:
            # Si les résultats de recherche sont non vides, appliquer le limit et offset
            data = search_results[offset:offset+limit]
        else:
            # Sinon, récupérer les données avec le limit et offset par défaut
            data = fetch_purchases(limit, offset)
            print('data', data)
        
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
                    command=lambda row=row:details_and_update(row[::-1][0],update_table,row[::-1][4],row[::-1][5])
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
                command=lambda row=row: delete_purchase(row[::-1][0], update_table)
                )
            delete_button.grid(row=0, column=0, padx=5) if is_admin == 1 else delete_button.grid_remove()
    
    offset = 0

    # Search Frame
    search_frame(root,parent, lambda: update_table(),offset,limit)  # Appelle `update_table` comme callback
    # SELECT s.id,c.name,s.reference_number,s.payment_method,s.total_amount,s.discount,s.final_amount,s.date
    columns = ('رقم القطعة ', 'اسم  ', 'رقم الفاتورة', 'طريقة الدفع', ' الكمية',  'المبلغ النهائي', 'التاريخ')
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
        sp.name,
        s.reference_number,
        s.payment_method,
        sum(p.quantity),
        sum(p.quantity * p.purchase_price),
        DATE(s.date)
        FROM 
        purchases s 
        JOIN suppliers sp ON s.supplier_id = sp.id 
        LEFT JOIN products p ON s.id = p.purchase_id
        WHERE p.name = %s OR sp.name = %s OR s.reference_number = %s OR s.payment_method = %s 
        GROUP BY 
        s.id
        order by (s.date)
        limit 10
        '''
        # query = f'SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location FROM purchases p JOIN purchase_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id LIMIT {limit} OFFSET {offset}'
        
        my_cursor.execute(sql_query, (query, query,query,query))
        search_results = my_cursor.fetchall()  # Récupérer les résultats
        refresh_callback()  # Appeler la fonction de rafraîchissement pour afficher les nouvelles données




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
    sp.name as  اسم_المورد,
    s.reference_number as رقم_الفاتورة,
    s.payment_method as طريقة_الدفع,
    sum(p.quantity) as الكمية,
    sum(p.quantity * p.purchase_price) as السعر,
    DATE(s.date) as تاريخ
    FROM 
    purchases s 
    JOIN suppliers sp ON s.supplier_id = sp.id 
    LEFT JOIN products p ON s.id = p.purchase_id
    GROUP BY 
    s.id
    order by (s.date)'''
    df = pd.read_sql(query, connect)
    df.to_excel('purchases.xlsx', index=False)
    messagebox.showinfo('نجاح في التصدير', ' لقد تم تصدير البيانات بنجاح في "purchases.xlsx".')

from tkinter import filedialog



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

    export_button.pack(side="left")

def pur_prod(id):
    connect_db()
    my_cursor.execute("SELECT p.name, p.quantity, p.purchase_price, p.quantity* p.purchase_price FROM purchases s JOIN products p ON s.id = p.purchase_id WHERE s.id = %s", (id))
    items = my_cursor.fetchall()
    print('results::', items,id)
    return items
    
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

def open_update_window(purchase_id, update_callback):
    update_window = tk.Toplevel(background='#fff')
    # update_window.pack()
    update_window.title("تعديل ")
    
    print("Update:",purchase_id)
    purchase = fetch_purchase(purchase_id)
    print("purchase:",purchase)
        # Créer un conteneur scrollable
    canvas = ctk.CTkCanvas(update_window, width=800, height=700)
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
    # supplier
    list_of_suppliers = []
    fetch_total('suppliers',suppliers, list_of_suppliers)
    supplier_default = f"{purchase[2]}---"

    # Créez une variable Tkinter StringVar
    supplier = tk.StringVar(value=supplier_default)
    #supplier
    supplier_label = create_label(first_frame,"مورد")
    supplier_label.grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2, )

    supplier_entry = ctk.CTkOptionMenu(
        first_frame_entries,values=list_of_suppliers,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        font=font_arial,
        variable=supplier
    )
    supplier_entry.grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2,padx=(15,0)  )
    
    # date
    date_label = create_label(first_frame,"تاريخ ")
    date_label.grid(sticky="news",row = 0, column = 0, ipady=10 , pady=2, )
    
    date_entry = DateEntry(first_frame_entries, width=30, background='white',font=font_arial,
                                foreground='black', justify='center', date_pattern='yyyy-mm-dd',)
    date_entry.grid(row = 0, column = 0, ipady=10 , pady=2, padx=20, )
    
        # Set the initial date if available
    if purchase[1]:
        try:
            # Check if purchase[1] is already a datetime object
            if isinstance(purchase[1], datetime):
                date_entry.set_date(purchase[1].date())
            else:
                # If it's a string, parse it
                date_entry.set_date(datetime.strptime(purchase[1], '%Y-%m-%d %H:%M:%S').date())
        except ValueError as e:
            messagebox.showerror("Error", "Invalid date format: {purchase[1]}, Error: {e}!")
        
    # second frame  labels
    second_frame = ctk.CTkFrame(frame,fg_color='transparent',width=400)
    second_frame.pack(ipady=10 , padx=20,fill='x')
    
    # second frame entries
    second_frame_entry = ctk.CTkFrame(frame,fg_color='transparent',width=400)
    second_frame_entry.pack(ipady=10 , padx=20,fill='x')

    create_label(second_frame," رقم الفاتورة").pack(ipady=10 , fill='x',expand = True,side='right')    
    reference_number_entry = create_entry(second_frame_entry)
    reference_number_entry.insert(0, purchase[4])
    reference_number_entry.pack(ipady=10 , padx=2,fill='x',expand = True,side='right')
    
    # pay method
    create_label(second_frame,"طريقة الدفع").pack(ipady=10 , fill='x',expand = True,side='left')
    methods = ['نقدي','بطاقة الدفع']
    methode_default = purchase[3]

    # Créez une variable Tkinter StringVar
    methode = tk.StringVar(value=methode_default)
    payment_method_entry = ctk.CTkOptionMenu(
        second_frame_entry,values=methods,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        variable=methode,
    )
    payment_method_entry.pack(ipady=10 , padx=2,fill='x',expand = True,side='left')

    error_frame = ctk.CTkFrame(frame,fg_color='transparent',width=400,height=20)
    error_frame.pack(ipady=10 , padx=20,fill='x')
    

    ref_num_error = error_message(error_frame, "")
    ref_num_error.pack( padx=2,fill='x',expand = True,side='right')
    # Label d'erreur pour le nom
    payment_method_error_label = error_message(error_frame,"")
    payment_method_error_label.pack( padx=2,fill='x',expand = True,side='left')
    
    # note
    create_label(frame,"ملاحظات").pack(ipady=10 , padx=20,fill='x',pady=5)
    
    note_entry = create_entry(frame)
    note_entry.insert(0, purchase[5])
    note_entry.pack(ipady=10 , fill='x',pady=(5,0),padx=20,)
    
    # Bouton pour sauvegarder les modifications
    def validate_string(input_str):
        # Cette regex vérifie que l'entrée contient uniquement des lettres et des espaces
        return bool(re.match(r'^[A-Za-z\s]+$', input_str))


    def save_changes():
        supplier = supplier_entry.get()[0]
        date = date_entry.get_date().strftime('%Y-%m-%d') if date_entry.get_date() else None
        payment_method = payment_method_entry.get()
        reference_number = reference_number_entry.get()
        note = note_entry.get()
        purchase_id = purchase[0]
        
        # Réinitialiser les messages d'erreur
        payment_method_error_label.configure(text="")
        ref_num_error.configure(text="")
        
        # Validation des champs
        has_error = False
                
        if reference_number == '':
            ref_num_error.configure(text="ادخل رقم المرجع")
            has_error = True
        

        # Si une erreur est détectée, arrêter la fonction
        if has_error:
            return
        
        try:
            connect_db()
            print('Data:',supplier,date,payment_method,reference_number,note,purchase_id)
            query = '''
            UPDATE purchases SET
            supplier_id=%s,
            date=%s,
            payment_method=%s,
            reference_number=%s,
            note=%s
            WHERE id=%s'''
            
            my_cursor.execute(query, (supplier,date,payment_method,reference_number,note,purchase_id))
            connect.commit()
            messagebox.showinfo('نجاح', ' تم تحديث البيانات بنجاح')
        except Exception as e:
            print(e)
            messagebox.showerror('خطاء', 'حدث خطاء في تحديث البيانات')
            return
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(frame, text="حفظ", command=save_changes,font=font_arial_title,corner_radius=2).pack(ipady=10 , fill='x',pady=20,padx=20,)
        # Mettre à jour la taille du frame pour qu'il soit visible dans le canvas
    frame.update_idletasks( )
    canvas.configure(scrollregion=canvas.bbox("all"))
    
    update_window.grab_set()  # Make the window modal
    update_window.focus_set()

def details_and_update(purchase_id,update_callback,total_qty,total_amount):
    print('qty:',total_qty,'total_amount',total_amount)
    purchaseItems = []
    purchaseItems= pur_prod(purchase_id)
    global inv_data
    inv_data = purchaseItems
    print('D1: ', purchaseItems)
    window = tk.Toplevel(background='#fff')
    # window.pack()
    window.title("المنتجات ")
    
    # Créer un conteneur scrollable
    canvas = ctk.CTkCanvas(window, width=800,height=500)
    canvas.pack( fill="both", expand=True)

    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 12)
    # Créer un frame pour contenir les champs du formulaire
    frame = ctk.CTkFrame(canvas, fg_color='#fff',)
    canvas.create_window((0,0), window=frame, anchor="center", width=799, height=500)
    

    
    title_label = ctk.CTkLabel(frame, text="المنتجات المضافة", font=('Ariel', 20, 'bold'))
    title_label.pack(pady=(20,10))



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
                label.grid(row=row_index, column=col_index, sticky="nsew", padx=5, pady=1)

            
    columns = ('المنتج', 'الكمية', 'السعر', 'المجموع')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
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
    data_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
    
    total_frame = ctk.CTkFrame(frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    total_frame.pack(fill='x', padx=20, pady=(5,30))
    # total_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
    

    ctk.CTkLabel(total_frame, text=round(total_amount, 2), font=('Arial', 13)).pack(side='left', expand=True)
    ctk.CTkLabel(total_frame, text=": المجموع", font=('Arial', 15, 'bold')).pack(side='left', padx=10, pady=5)

    ctk.CTkLabel(total_frame, text=": الكمية", font=('Arial', 15, 'bold')).pack(side='right', padx=10, pady=5)
    ctk.CTkLabel(total_frame, text=total_qty, font=('Arial', 13)).pack(side='right', expand=True)
    
    update_inv_table()
    
    # ctk.CTkButton(frame, text="حفظ", command=save_changes,).pack(ipady=10 , fill='x',pady=(20,100),padx=20,)
        # Mettre à jour la taille du frame pour qu'il soit visible dans le canvas
    frame.update_idletasks( )
    canvas.configure(scrollregion=canvas.bbox("all"))
    
    window.grab_set()  # Make the window modal
    window.focus_set()

inv_data = []  # Change this to a list instead of a tuple
total_amount = 0
total_qty = 0


# def create_purchases_frame(root,user=None):
#     purchases_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

#     show_title_frame(purchases_frame)

#     show_purchases_table(root,purchases_frame,user=user,is_admin = user[4] if user else 1)
#     return purchases_frame

def create_purchases_frame(root):
    purchases_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

    # Titre
    show_title_frame(purchases_frame)

    # Frame pour le tableau des catégories
    table_frame = ctk.CTkFrame(purchases_frame, fg_color="#fff")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def set_user(user):
        # Nettoyer la frame avant d'afficher un nouveau tableau
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Afficher le tableau des catégories en fonction de l'utilisateur
        is_admin = user[4] if user else 0
        show_purchases_table(root,table_frame, is_admin=is_admin)

    # Ajouter la méthode set_user à la frame
    purchases_frame.set_user = set_user

    return purchases_frame
        

#     return purchase_frame
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# purchases_frame = create_purchases_frame(window)
# purchases_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()