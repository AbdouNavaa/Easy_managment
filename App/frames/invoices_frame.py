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
        global suppliers
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        customers = connect.cursor()
        
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
    sum(si.subtotal) AS total_amount,
    si.discount,
    s.date,
    sum(si.subtotal + si.subtotal * si.discount * 0.01) AS final_total
    FROM 
    sales s 
    JOIN customers c ON s.customer_id = c.id 
    LEFT JOIN sale_items si ON s.id = si.sale_id
    GROUP BY 
    s.id
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
        messagebox.showinfo('Success', 'sale deleted successfully')
        
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
                label1.grid(row=row_index, column=8 if is_admin == 1 else 7, sticky="nsew", padx=5, pady=5)
                
                label.grid(row=row_index, column=col_index + 1 if is_admin == 1 else col_index, sticky="nsew", padx=5, pady=5)

            font_arial_btn = ('Arial',14,'bold')

            # Ajouter les boutons Modifier et Supprimer
            buttons_frame = ctk.CTkFrame(data_frame, width=100, height=40, fg_color="#fff") 
            buttons_frame.grid(row=row_index, column=0, sticky="nsew", padx=5, pady=5) if is_admin == 1 else buttons_frame.grid_remove()
            
            show_image_path = os.path.join(os.path.dirname(__file__), "images", "bill.png")
            show_image = ctk.CTkImage(light_image=Image.open(show_image_path), size=(23, 23),)
            show_button = ctk.CTkButton(buttons_frame, text="",text_color="black",
                    image=show_image,
                    fg_color='transparent',
                    # bg_color='#fff',
                    hover_color='#eee',
                    width=20,
                    font=font_arial_btn,        
                    # command=more_details
                    command=lambda row=row: more_details(root,row[::-1][0])
                    )
            show_button.grid(row=0, column=2) if is_admin == 1 else show_button.grid_remove()
            
            def more_details(root,sale_id):
                res = []
                res = sale_items(sale_id)
                # parent.destroy()
                sales_frame = switch_frame(root,frame_principal,sale_id,True,res) 
                sales_frame.pack(fill='x', padx=50,pady=30) 
                
            edit_image_path = os.path.join(os.path.dirname(__file__), "images", "receipt.png")
            edit_image = ctk.CTkImage(light_image=Image.open(edit_image_path), size=(23, 23),)
            update_button = ctk.CTkButton(buttons_frame, text="",text_color="black",
                    image=edit_image,
                    fg_color='transparent',
                    # bg_color='#fff',
                    hover_color='#eee',
                    width=20,
                    font=font_arial_btn,        
                    command=lambda row=row: update(root,row[::-1][0])
                    )
            update_button.grid(row=0, column=1) if is_admin == 1 else update_button.grid_remove()
            
            def update(root,sale_id):
                res = []
                res = fetch_sale(sale_id)
                # parent.destroy()
                create_add_sale_frame(root,user=user,sale=res)
                switch_frame(root,create_add_sale_frame,user=user,sale=res)
            
            delete_image_path = os.path.join(os.path.dirname(__file__), "images", "delete_invoice.png")
            delete_image = ctk.CTkImage(light_image=Image.open(delete_image_path), size=(23, 23),)
            delete_button = ctk.CTkButton(buttons_frame,
                text="",
                text_color="black",
                image=delete_image,
                fg_color='#fff',
                # bg_color='#fff',
                hover_color='#eee',
                font=font_arial_btn, 
                width=20,
                command=lambda row=row: delete_sale(row[::-1][0], update_table)
                )
            delete_button.grid(row=0, column=0, padx=5) if is_admin == 1 else delete_button.grid_remove()
    
    offset = 0

    # Search Frame
    search_frame(root,parent, lambda: update_table(),offset)  # Appelle `update_table` comme callback
    # SELECT s.id,c.name,s.reference_number,s.payment_method,s.total_amount,s.discount,s.final_amount,s.date
    columns = ('رقم القطعة ', 'اسم العميل ', 'رقم الفاتورة', 'طريقة الدفع', ' الاجمالي', ' الضريبة', 'المبلغ النهائي', 'التاريخ')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="#fff",border_width=1,border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((0, 1, 2,3, 4, 5, 6,7,8), weight=1, uniform='a') if is_admin == 1 else header_frame.columnconfigure((0, 1, 2,3, 4, 5,6,7), weight=1, uniform='a')
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
    data_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6,7,8), weight=1, uniform='a') if is_admin == 1 else data_frame.columnconfigure((0, 1, 2,3, 4, 5,6,7), weight=1, uniform='a')

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
def search_frame(root,parent, refresh_callback,offset):
    """Crée une barre de recherche avec options."""
    s_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white")
    s_frame.pack(fill='x', padx=20, pady=5)

    # s_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')

    font_arial = ('Arial',18,)
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
    image_path = os.path.join(os.path.dirname(__file__), "images", "refresh.png")
    
    image = ctk.CTkImage(light_image=Image.open(image_path), size=(20, 20),)

    refresh_button = ctk.CTkButton(
        s_frame,
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
    
        
    add_image_path = os.path.join(os.path.dirname(__file__), "images", "add.png")
    
    add_image = ctk.CTkImage(light_image=Image.open(add_image_path), size=(15, 15),)
    add_inventory_button = ctk.CTkButton(
        master=s_frame,
        image=add_image,
        text=" اضافة فاتورة جديدة",
        font=font_arial,
        width=40,
        text_color="#333",
        fg_color="#fafafa",
        hover_color="#f0f0f0",
        corner_radius=5,
        command=lambda: add_frame(root)
    )
    add_inventory_button.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5)
    
    def add_frame(root,):
        parent.destroy()
        create_add_sale_frame(root)
    
        

def refresh(refresh_callback):
    global search_results  # Déclarer `search_results` comme global
    search_results = []
    # Appeler la fonction de rafraîchissement pour afficher les données à partir de la base de données
    refresh_callback()
def search(query,refresh_callback):
    global search_results  # Déclarer `search_results` comme global
    if not query:
        messagebox.showinfo("Warning", "Search input is empty!")
        search_results = []  # Vider les résultats si la recherche est vide
    else:
        connect_db()
        sql_query = '''
        SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location
        FROM sales p JOIN sale_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id 
        WHERE p.name = %s OR c.name = %s OR w.name = %s OR w.location = %s
        LIMIT 10
        '''
        # query = f'SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location FROM sales p JOIN sale_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id LIMIT {limit} OFFSET {offset}'
        
        my_cursor.execute(sql_query, (query, query,query,query))
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
def search_by_category(query, refresh_callback, ):
    global search_results  # Déclarer `search_results` comme global
    if not query:
        messagebox.showinfo("Warning", "Search input is empty!")
        search_results = []  # Vider les résultats si la recherche est vide
    else:
        connect_db()
        sql_query = '''
        SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location
        FROM sales p JOIN sale_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id 
        WHERE c.name = %s 
        LIMIT 10
        '''
        my_cursor.execute(sql_query, (query,))
        # search_results = my_cursor.fetchall()  # Récupérer les résultats
        search_results = my_cursor.fetchall()
        if not search_results:
            messagebox.showinfo("Warning", "No sales found with this category!")

        else:
            messagebox.showinfo("success", f"{len(search_results)} sales found successfully!")
        refresh_callback()  # Appeler la fonction de rafraîchissement pour afficher les nouvelles données

def search_by_warehouses(query, refresh_callback, ):
    global search_results  # Déclarer `search_results` comme global
    if not query:
        messagebox.showinfo("Warning", "Search input is empty!")
        search_results = []  # Vider les résultats si la recherche est vide
    else:
        connect_db()
        sql_query = f'SELECT p.id,p.name,c.name,p.price,w.name,p.min_quantity,w.location FROM sales p JOIN sale_categories c ON p.category_id = c.id JOIN warehouses w ON p.warehouse_id = w.id  WHERE w.name = %s  '
        my_cursor.execute(sql_query, (query,))
        search_results = my_cursor.fetchall()  # Récupérer les résultats
        
        if not search_results:
            messagebox.showinfo("Warning", "No sales found with this warehouse!")

        else:
            messagebox.showinfo("success", f"{len(search_results)} sales found successfully!")
        refresh_callback()  # Appeler la fonction de rafraîchissement pour afficher les nouvelles données
# add Prod
def add_sale():
    root.destroy()
    create_add_sale_frame
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
    title_frame.columnconfigure((0, 1, 2,3, 4, 5, 6), weight=1, uniform='a',)
    
    
    font_arial_title = ('Arial',20,'bold')
    font_arial = ('Arial',12,)

    title_label = ctk.CTkLabel(
        master=title_frame,
        text="ادارة المنتجات",
        font=font_arial_title,
    )
    title_label.pack(side="right")
    



def create_sales_frame(root,user=None):
    sales_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

    show_title_frame(sales_frame)
    print('User:',user[0]) if user else None

    show_sales_table(root,sales_frame,user=user,is_admin = user[2] if user else 1)
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
    entry = ctk.CTkEntry(parent, justify=justify,font=font_arial, fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=4)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text)
    label_widgets.append(label)
    return label

def create_add_sale_frame(root,user=None,sale=None):
    
    print("Sale Infos:",sale) if sale is not None else None
    
    # cancel frame
    cancel_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")
    cancel_frame.pack(fill='x', padx=20, pady=5,)
    
    #add btn for cancel
    cancel_btn = ctk.CTkButton(
        master=cancel_frame,
        text="اغلاق",
        font=('arial', 16),
        width=40,
        text_color="#333",
        fg_color="#fafafa",
        hover_color="#f0f0f0",
        corner_radius=5,
        command=lambda: switch_frame(root,create_sales_frame)
    ) 
    cancel_btn.pack()
    
    add_sale_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    add_sale_frame.pack(padx=400,pady=10,ipady=10,)
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(add_sale_frame,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # first frame labels
    first_frame = ctk.CTkFrame(add_sale_frame,fg_color='transparent',width=400)
    first_frame.pack(ipady=10 , padx=20,fill='x')
    first_frame.columnconfigure((0,1), weight=1, uniform='equal') 
    
    # first frame entries
    first_frame_entries = ctk.CTkFrame(add_sale_frame,fg_color='transparent',width=400)
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
    second_frame = ctk.CTkFrame(add_sale_frame,fg_color='transparent',width=400)
    second_frame.pack(ipady=10 , padx=20,fill='x')
    
    # second frame entries
    second_frame_entry = ctk.CTkFrame(add_sale_frame,fg_color='transparent',width=400)
    second_frame_entry.pack(ipady=10 , padx=20,fill='x')
    

    # status
    create_label(second_frame," الحالة").pack(ipady=10 , fill='x',expand = True,side='right')    
    status_entry = create_entry(second_frame_entry)
    status_entry.insert(0, sale[6]) if sale is not None else None 
    status_entry.pack(ipady=10 , padx=2,fill='x',expand = True,side='right')
    
    # pay method
    create_label(second_frame,"طريقة الدفع").pack(ipady=10 , fill='x',expand = True,side='left')
    
    payment_method_entry = create_entry(second_frame_entry)
    payment_method_entry.insert(0, sale[7]) if sale is not None else None 
    payment_method_entry.pack(ipady=10 , padx=2,fill='x',expand = True,side='left')


    # payment_method and reference_number
    create_label(add_sale_frame,"رقم الفاتورة").pack(ipady=10 , padx=20,fill='x',pady=5)
    
    reference_number_entry = create_entry(add_sale_frame)
    reference_number_entry.insert(0, sale[8]) if sale is not None else None 
    reference_number_entry.pack(ipady=10 , fill='x',pady=5,padx=20,)
    
    # note
    create_label(add_sale_frame,"ملاحظات").pack(ipady=10 , padx=20,fill='x',pady=5)
    
    note_entry = create_entry(add_sale_frame)
    note_entry.insert(0, sale[9]) if sale is not None else None 
    note_entry.pack(ipady=10 , fill='x',pady=(5,0),padx=20,)
    
    
    def add_sales():
        customer = customer_entry.get()[0]
        date = date_entry.get_date().strftime('%Y-%m-%d') if date_entry.get_date() else None
        # total_amount = float(total_amount_entry.get())
        # discount = float(discount_entry.get())
        # final_amount = ((total_amount) + ( total_amount*discount*0.01))
        status = status_entry.get()
        payment_method = payment_method_entry.get()
        reference_number = reference_number_entry.get()
        note = note_entry.get()
        
        
        # Validation des informations de connexion
        if payment_method == "" or status == "" or note == ""  or  reference_number == '':
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                connect_db()
                if sale is None:
                    query = '''INSERT INTO sales (date, customer_id,  status, payment_method, reference_number, notes,
                    created_by,created_at,completed_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,Now(),Now())'''
                    values = (date, customer,  status, payment_method, reference_number, note, 1)
                    my_cursor.execute(query,values)
                    connect.commit()
                    messagebox.showinfo('Success', 'Sale added successfully')
                else:
                    query = '''UPDATE sales SET date=%s, customer_id=%s, status=%s, payment_method=%s, reference_number=%s, notes=%s
                    WHERE id=%s'''
                    values = (date, customer,  status, payment_method, reference_number, note, sale[0])
                    my_cursor.execute(query,values)
                    connect.commit()
                    messagebox.showinfo('Success', 'Sale updated successfully')
                    # sales_frame = switch_frame(root,create_sales_frame) 
                    
                
                result = messagebox.askyesno('Sale added successfully', 'do you want to clean the form?' , parent=add_sale_frame)
                if result == True and sale is None:
                    connect_db()
                    query = "SELECT id FROM sales ORDER BY id DESC LIMIT 1"
                    my_cursor.execute(query)
                    sale_id = my_cursor.fetchone()
                    print('Sale Id:', sale_id)
                    # add_sale_frame.destroy()
                    sales_frame = switch_frame(root,frame_principal,sale_id) 
                else:
                    back_to_invoices(root)  
            except Exception as e:
                messagebox.showerror('Error', str(e))
            
        
    def back_to_invoices(root):
        # add_sale_frame.pack_forget()  # Cache le frame actuel
        # invoices_frame = create_sales_frame(root) 
        switch_frame(root,create_sales_frame)
        # invoices_frame.pack(fill="both", expand=True)  # Affiche la page des factures

    add_button = ctk.CTkButton(
        add_sale_frame,
        text="تاكيد",
        width=400,
        corner_radius=4,
        command=add_sales
            )
    add_button.pack(pady=5,ipady=10,padx=20,fill='x')
    
    
    
    return add_sale_frame

def switch_frame(root, frame_class, *args, **kwargs):
    """
    Permet de changer de frame dans l'application.
    """
    for widget in root.winfo_children():
        widget.destroy()  # Détruit tous les widgets précédents

    frame = frame_class(root, *args, **kwargs)
    frame.pack(fill="both", expand=True)
    return frame

        
def show_details_frame(root,sale_id,details):
    title_frame = ctk.CTkFrame(root, corner_radius=1, fg_color="#fff", border_width=1, border_color="#f0f0f0", width=400)

    title_label = ctk.CTkLabel(title_frame, text="المنتجات المضافة", font=('Ariel', 20, 'bold'))
    title_label.pack(pady=10)
    def recalculate_totals():
        global total_amount, final_total

        # Recalculer le montant total
        total_amount = sum(item[3] for item in inv_data)  # item[3] = total pour chaque ligne

        # Calculer le total final en incluant les taxes
        final_total = total_amount + (total_amount * taxe * 0.01)


    global inv_data
    def update_table():
        # Clear previous table data
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Fetch new data
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
                if not inv_data:
                    messagebox.showerror("Error", "No products added yet.")
                    return
                try:
                    connection = connect_db()
                    with connection.cursor() as cursor:
                            
                        prod = search_product(row[0])
                        print("Product founded:", prod)
                        id = prod[0]
                        query = "delete from sale_items where product_id= %s"
                        cursor.execute(query, (id))
                        
                        connection.commit()
                    
                    messagebox.showinfo("Success", "تم الحذف")
                    # je veux remove le row dans le list inv_data
                    inv_data = [item for item in inv_data if item[0] != row[0]]
                    print('INv:',inv_data)
            
                    # update the table
                    
                    update_table()
                    print('Inv Data:', inv_data)
                
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

        # Recalculer et mettre à jour les totaux
        recalculate_totals()
        update_totals_display()
    columns = ('المنتج', 'الكمية', 'السعر', 'المجموع','حذف')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(title_frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
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
    data_frame = ctk.CTkFrame(title_frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure((0, 1, 2, 3,4), weight=1, uniform='a')
    
    total_frame = ctk.CTkFrame(title_frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    total_frame.pack(fill='x', padx=20, pady=(5,20))
    
    def update_totals_display():
        # Mettre à jour les valeurs affichées pour les totaux
        for widget in total_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(total_frame, text=": المجموع", font=('Arial', 15, 'bold')).pack(side='right', padx=20, pady=5)
        ctk.CTkLabel(total_frame, text=round(total_amount, 2), font=('Arial', 15, 'bold')).pack(side='right', padx=(0, 130))

        ctk.CTkLabel(total_frame, text=": الضريبة", font=('Arial', 15, 'bold')).pack(side='right', padx=20, pady=5)
        ctk.CTkLabel(total_frame, text=f"{taxe}%", font=('Arial', 15, 'bold')).pack(side='right', padx=(0, 130))

        ctk.CTkLabel(total_frame, text=": الاجمالي", font=('Arial', 15, 'bold')).pack(side='right', padx=20, pady=5)
        ctk.CTkLabel(total_frame, text=round(final_total, 2), font=('Arial', 15, 'bold')).pack(side='right', padx=(0, 130))

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
                    print("Product founded:", prod)
                    id = prod[0]
                    if details:
                        query = 'update sale_items set sale_id = %  product_id = %, quantity = %, discount = %, subtotal =% where id = %s'
                        cursor.execute(query, (sale_id, id, item[1], taxe, item[3]))
                    else:
                        query = "INSERT INTO sale_items (sale_id, product_id, quantity, discount, subtotal) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(query, (sale_id, id, item[1], taxe, item[3]))
                
                connection.commit()
            
            messagebox.showinfo("Success", "The items were successfully added")
            inv_data = []
            
            result = messagebox.askyesno('Successfully', 'do you want to go to invoices?' , parent=title_frame)
            if result:
                switch_frame(root,create_sales_frame) 
        
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
    add_button = ctk.CTkButton(
        title_frame,
        text="تاكيد",
        width=400,
        corner_radius=4,
        command=add_invoice
    )
    add_button.pack(pady=(5, 20), ipady=10, padx=20, fill='x') if details == False else add_button.pack_forget()

    # update the
    update_table()
    return title_frame, update_table

inv_data = []  # Change this to a list instead of a tuple
total_amount = 0
taxe = 15
final_total = 0
def search_product(name_or_code):
    connect = connect_db()
    cursor = connect.cursor()
    
    query = "SELECT * FROM products WHERE name = %s OR code = %s"
    cursor.execute(query, (name_or_code, name_or_code))
    
    result = cursor.fetchone()
    if result is None:
        messagebox.showinfo("Product Not Found", "The product was not found in the database.")
        
    cursor.close()
    connect.close()
    
    return result


def change(symbol):
    global change_value
    if symbol == '+' :
        change_value += 1 
    else:
        change_value -= 1 
    update_entry()
def update_entry():
    for entry in entry_widgets:
        if entry.winfo_exists():
            var_change = tk.StringVar(value=change_value) 
            entry.configure(textvariable=var_change)

# for entries
change_value = 0
def create_entry1(parent,wid=200):
    var_change = tk.StringVar(value=change_value) 
    entry = ctk.CTkEntry(parent,font=("Arial", 14), fg_color='#fff', border_width=1,justify='center',
                        border_color='#ddd', corner_radius=1, width=300,textvariable=var_change)
    entry_widgets.append(entry)
    return entry

def create_label1(parent,text,*args):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='e', text=text)
    label_widgets.append(label)
    return label

def add_inv_prod_frame(root, update_table,details=False, data=[]):
    add_prod_frame = ctk.CTkFrame(root, corner_radius=1, fg_color="#fff", border_width=1, border_color="#f0f0f0", width=300)

    title_label = ctk.CTkLabel(add_prod_frame, text=" اضافة منتج", font=('Arial', 20, 'bold'))
    title_label.pack(pady=10, fill='x',padx=20)
    
    create_label1(add_prod_frame, '   بحث عن منتج').pack(pady=10, padx=10, ipady=10, fill='x')
    
    # frame
    search_frame = ctk.CTkFrame(add_prod_frame, fg_color='transparent', width=350, height=50, corner_radius=1)
    search_frame.pack(pady=10, padx=10)
    
    product = ctk.CTkEntry(search_frame, font=("Arial", 14), fg_color='#fff', border_width=1,
                        border_color='#ddd', corner_radius=1, width=345, placeholder_text='اسم المنتج او الكود', justify='center')
    product.pack(ipady=10, fill='x', side='right', padx=(0,10))
    

    
    btn = ctk.CTkButton(search_frame, text='ok', width=45, height=42, corner_radius=1, fg_color='#eee', text_color='#333', command=lambda:search_product(product.get()))
    btn.pack(pady=10, fill='x', padx=(10,0), side='right')
    
    # ... (keep the rest of the add_frame function as is)

    create_label1(add_prod_frame, "الكمية  ").pack(pady=10,fill = 'x',padx=10,ipady=10)
    
    # frame
    qty_frame = ctk.CTkFrame(add_prod_frame,fg_color='transparent',width=300,height=50,corner_radius=1)
    qty_frame.pack(pady=10,padx=10)

    btn = ctk.CTkButton(qty_frame,font=('Ariel',20),text='+',width=45,height=42,corner_radius=1,fg_color='#eee',hover_color='#fff',
        text_color='#333',command=lambda:change('+')).pack(pady=10,padx=(0,10),side='right')
    
    qty_entry = create_entry1(qty_frame)
    qty_entry.pack(ipady=10,fill = 'x',side='right',anchor='center')
    
    btn = ctk.CTkButton(qty_frame,font=('Ariel',20),text='-',width=45,height=42,corner_radius=1,fg_color='#eee',hover_color='#fff',
        text_color='#333',command=lambda:change('-')).pack(pady=10,padx=(10,0),side='right')

    # ... (keep the existing code)

    def search_and_display():
        name_or_code = product.get()
        result = search_product(name_or_code)

        if result and float(qty_entry.get()) > 0:
            global inv_data
            global total_amount
            global final_total
            print('Result:', result)
            if details :
                # inv_data = data
                print('hmm:', details,inv_data,data)

            # Extraire les informations nécessaires du produit
            product_code = result[1]  # Supposons que le code produit est à l'index 1
            quantity = float(qty_entry.get())
            price = float(result[4])  # Supposons que le prix est à l'index 4
            total = quantity * price
            # total_amount += total  

            # Vérifier si le produit existe déjà dans inv_data
            product_exists = False
            for index, item in enumerate(inv_data):
                if item[0] == product_code:  
                    # Si le produit existe, mettre à jour la quantité directement dans la liste
                    existing_quantity = item[1]
                    new_quantity = existing_quantity + quantity
                    inv_data[index] = (item[0], new_quantity, price, new_quantity * price)
                    product_exists = True
                    break

            # Si le produit n'existe pas, l'ajouter comme une nouvelle entrée
            if not product_exists:
                print('Im here',inv_data)
                if isinstance(inv_data, tuple):
                    inv_data = list(inv_data)
                # if inv_data != []:
                # inv_data += [(product_code, quantity, price, total)]
                # else:
                inv_data.append((product_code, 
                                 quantity, price, total))

            # Mettre à jour l'affichage
            update_table()

            # Réinitialiser les champs d'entrée
            product.delete(0, 'end')
            qty_entry.delete(0, 'end')
            qty_entry.insert(0, '0')
            global change_value
            change_value = 0
            # message for asking

            
        else:
            messagebox.showinfo("Erreur", "Le produit n'a pas été trouvé dans la base de données ou la quantité est invalide.")
    # btn
    add_button = ctk.CTkButton(
        add_prod_frame,
        text="تاكيد",
        width=400,
        corner_radius=4,
        command=search_and_display
    )
    add_button.pack(pady=5, ipady=10, padx=20, fill='x')
    return add_prod_frame
# tree = 
def frame_principal(root, sale_id=4, details=False,data=[]):
    invoice_detail_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")
    # cancel frame
    cancel_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")
    cancel_frame.pack(fill='x', padx=20, pady=5,)
    # add btn for cancel
    cancel_btn = ctk.CTkButton(
        master=cancel_frame,
        text="اغلاق",
        font=('arial', 16),
        width=40,
        text_color="#333",
        fg_color="#fafafa",
        hover_color="#f0f0f0",
        corner_radius=5,
        command=lambda: switch_frame(root,create_sales_frame)
    ) 
    cancel_btn.pack()
    global inv_data 
    if details:
        inv_data = data
    print('sale_id:', sale_id) 
    show_frame, update_table = show_details_frame(invoice_detail_frame,sale_id=sale_id,details=details)
    show_frame.pack( expand=True, padx=10, pady=10,fill='x',side='left')
    
    add_prod = add_inv_prod_frame(invoice_detail_frame, update_table,details= details,data=inv_data)
    add_prod.pack(expand=True, padx=5, pady=10,fill='x',side='left')  

    return invoice_detail_frame

    
#     return sale_frame
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# sales_frame = switch_frame(window,create_sales_frame)
# sales_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()