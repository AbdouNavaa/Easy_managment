import customtkinter as ctk
from tkinter import messagebox
import pymysql
import tkinter as tk
import os
from PIL import Image, ImageTk

# Connection settings
def connect_db():
    try:
        global connect
        global my_cursor
        global customers
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        customers = connect.cursor()
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))


# Function to fetch customers with pagination
def fetch_customers(limit=10, offset=0):
    connect_db()
    query = f'''
    SELECT id, name,phone,email,address
    FROM customers 
    LIMIT {limit} OFFSET {offset}'''
    my_cursor.execute(query)
    return my_cursor.fetchall()

def direction_btn(parent,text):
    btn = ctk.CTkButton(parent, text=text, width=40, fg_color='#f6f7f7',hover_color='#eee', text_color='black', command=lambda: direction(text))
    return btn

def error_message(parent,text):
    message = ctk.CTkLabel(parent, text="", text_color="red", font=("Arial", 12),height=10)
    return message

import re 
# Fonctions de validation
def validate_string(input_str):
    return bool(re.match(r'^[A-Za-z\s]+$', input_str))

def validate_number(input_str):
    # Vérifie que l'entrée contient uniquement des chiffres et a une longueur d'au moins 5
    return bool(re.match(r'^[0-9]{8,}$', input_str))

def validate_email(input_str):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', input_str))

# fenetere pour ajouter une categorie
def open_add_window(refresh_callback):
    add_window = tk.Toplevel(background='#fff')
    add_window.grab_set()  # Make the window modal
    add_window.focus_set()
    # add_window.pack()
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(add_window,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)

    direction_btn(btns_frame,'Fr').pack(pady=(10,0), padx=(5, 155), side='left')
    direction_btn(btns_frame,'Ar').pack(pady=(10,0), padx=(155, 5), side='right')
    # name 
    create_label(add_window,"اسم العميل").pack(ipady=5 ,pady=5, padx=20,fill='x')
    name_entry = create_entry(add_window)
    
    name_error = error_message(add_window,"")
    name_error.pack( padx=20,fill='x')

    # phone 
    create_label(add_window,"هاتف العميل").pack(ipady=5 ,pady=5, padx=20,fill='x')
    phone_entry = create_entry(add_window)
    
    phone_error = error_message(add_window,"")
    phone_error.pack( padx=20,fill='x')

    
    # email 
    create_label(add_window,"البريد الالكتروني").pack(ipady=5 ,pady=5, padx=20,fill='x')
    email_entry = ctk.CTkEntry(add_window,font=font_arial, fg_color='#fff', 
            border_width=1, border_color='#ddd', corner_radius=8, width=400)
    email_entry.pack(ipady=10 , padx=20)
    
    email_error = error_message(add_window,"")
    email_error.pack( padx=20,fill='x')
    
    # address 
    create_label(add_window,"العنوان").pack(ipady=5 ,pady=5, padx=20,fill='x')
    address_entry = create_entry(add_window)
    
    address_error = error_message(add_window,"")
    address_error.pack( padx=20,fill='x')
    
    # labels frame
    labels_frame = ctk.CTkFrame(add_window,fg_color='transparent',)
    labels_frame.pack( ipady=10 , padx=20, pady=2)
    
    # entries frame
    entries_frame = ctk.CTkFrame(add_window,fg_color='transparent',width=400)
    entries_frame.pack( ipady=10 , padx=20, pady=2)
    # balance
    create_label(labels_frame,"الرصيد").pack(ipady=5 ,pady=5, fill='x',side='right')
    balance_entry = create_entry(entries_frame,200)
    balance_entry.pack(ipady=10 , padx=20,side='right')

    
    # is_active 
    create_label(labels_frame,"الحالة").pack(ipady=5 ,pady=5, fill='x',side='left')
    is_active = ['0-غير مفعل','1-مفعل']

    is_active_entry = ctk.CTkOptionMenu(
        entries_frame,values=is_active,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
    )
    is_active_entry.pack(ipady=10 , padx=20,side='left')
    
    def add_customers():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()
        balance = (balance_entry.get())
        int(is_active_entry.get()[0])
        is_active = int(is_active_entry.get()[0])
        
        # Validation des informations de connexion
        name_error.configure(text="")
        phone_error.configure(text="")
        email_error.configure(text="")
        address_error.configure(text="")
        has_error = False
        
        if name == '':
            name_error.configure(text="ادخل اسم صحيح (حروف فقط)")
            has_error = True
            
        if not validate_number(phone):
            phone_error.configure(text="ادخل رقم صحيح (بدون مسافات)")
            has_error = True
            
        if not validate_email(email):
            email_error.configure(text="ادخل بريد الكتروني صحيح")
            has_error = True
            
        if address == '':
            address_error.configure(text="ادخل عنوان صحيح")
            has_error = True
            
        if has_error:
            return

        else:
            try:
                connect_db()
                query = '''INSERT INTO `customers` ( `name`, `phone`, `email`, `address`, `created_at`, `balance`, `is_active`) 
                VALUES (%s, %s, %s, %s, NOW(), %s, %s)'''
                
                my_cursor.execute(query, (name, phone, email, address, balance, is_active))
                connect.commit()
                messagebox.showinfo('نجاح', 'تم اضافة العميل بنجاح')
                refresh_callback()
                
                result = messagebox.askyesno('تم الاضافة', 'هل تريد اضافة عميل جديد?' , parent=add_window)
                if result == True:
                    name_entry.delete(0,tk.END)
                    phone_entry.delete(0, tk.END)
                    email_entry.delete(0, tk.END)
                    address_entry.delete(0, tk.END)
                    balance_entry.delete(0, tk.END)
                    is_active_entry.set(0)
                    # add_window.destroy()
            except Exception as e:
                messagebox.showerror('Error', str(e))
            

    add_button = ctk.CTkButton(
        add_window,
        text="تاكيد",
        width=400,
        command=add_customers,font=font_arial_title,corner_radius=2
            )
    add_button.pack(pady=5,padx=20,ipady=8)
    # ctk.CTkButton(update_window, text="Add", command=save_changes).pack(pady=10)

# Fonction pour afficher la fenêtre de mise à jour
def open_update_window(customer, update_callback):
    
    update_window = tk.Toplevel(background='#fff')
    update_window.grab_set()  # Make the window modal
    update_window.focus_set()
    update_window.title("تعديل")

    custom=fetch_customer(customer[0])
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    # direction btn
    btns_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    
    direction_btn(btns_frame,'Fr').pack(pady=(10,0), padx=(5, 155), side='left')
    direction_btn(btns_frame,'Ar').pack(pady=(10,0), padx=(155, 5), side='right')
    
    # name 
    create_label(update_window,"اسم العميل").pack(ipady=5 ,pady=5, padx=20,fill='x')
    name_entry = create_entry(update_window)
    name_entry.insert(0, custom[1])  # Pré-remplir avec la valeur actuelle

    name_error = error_message(update_window, "")
    name_error.pack(pady=5, padx=20,fill='x')
    # phone 
    create_label(update_window,"هاتف العميل").pack(ipady=5 ,pady=5, padx=20,fill='x')
    phone_entry = create_entry(update_window)
    phone_entry.insert(0, custom[2])
    
    phone_error = error_message(update_window, "")
    phone_error.pack(pady=5, padx=20,fill='x')

    # email 
    create_label(update_window,"البريد الالكتروني").pack(ipady=5 ,pady=5, padx=20,fill='x')
    email_entry = ctk.CTkEntry(update_window,font=font_arial, fg_color='#fff', 
            border_width=1, border_color='#ddd', corner_radius=8, width=400)
    email_entry.insert(0, custom[3])  # Pré-remplir avec la valeur actuelle
    email_entry.pack(ipady=5 , padx=20)
    
    email_error = error_message(update_window, "")
    email_error.pack(pady=5, padx=20,fill='x')
    
    # address 
    create_label(update_window,"العنوان").pack(ipady=5 ,pady=5, padx=20,fill='x')
    address_entry = create_entry(update_window)
    address_entry.insert(0, custom[4]) 
    
    address_error = error_message(update_window, "")
    address_error.pack(pady=5, padx=20,fill='x')
    
    # labels frame
    labels_frame = ctk.CTkFrame(update_window,fg_color='transparent',)
    labels_frame.pack( ipady=5 , padx=20, pady=2)
    
    # entries frame
    entries_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    entries_frame.pack( ipady=5 , padx=20, pady=2)
    # balance
    create_label(labels_frame,"الرصيد").pack(ipady=5 ,pady=5, fill='x',side='right')
    balance_entry = create_entry(entries_frame,200)
    balance_entry.insert(0, custom[6] if custom[6] else 'NULL')
    balance_entry.pack(ipady=5 , padx=20,side='right')

    
    # is_active 
    create_label(labels_frame,"الحالة").pack(ipady=5 ,pady=5, fill='x',side='left')
    is_active = ['0-غير مفعل','1-مفعل']
    default_value = is_active[1] if custom[7] == 1 else is_active[0]
    # Create a StringVar to hold the selected value
    is_active_var = tk.StringVar(value=default_value)


    is_active_entry = ctk.CTkOptionMenu(
        entries_frame,values=is_active,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        variable=is_active_var
    )
    is_active_entry.pack(ipady=10 , padx=20,side='left')
    
    # Bouton pour sauvegarder les modifications
    def save_changes():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()
        balance = balance_entry.get()
        is_active = is_active_entry.get()[0]
        id = customer[0]

        # Validation des informations de connexion
        name_error.configure(text="")
        phone_error.configure(text="")
        email_error.configure(text="")
        address_error.configure(text="")
        has_error = False
        
        if name == '':
            name_error.configure(text="ادخل اسم صحيح (حروف فقط)")
            has_error = True
            
        if not validate_number(phone):
            phone_error.configure(text="ادخل رقم صحيح (بدون مسافات)")
            has_error = True
            
        if not validate_email(email):
            email_error.configure(text="ادخل بريد الكتروني صحيح")
            has_error = True
            
        if address == '':
            address_error.configure(text="ادخل عنوان صحيح")
            has_error = True
            
        if has_error:
            return        
        try:
            connect_db()
            query = '''UPDATE `customers` SET `name`=%s, `phone`=%s, `email`=%s, `address`=%s, `balance`=%s, `is_active`=%s WHERE `id`=%s'''
            my_cursor.execute(query, (name, phone, email, address, balance, is_active, id))
            connect.commit()
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

        messagebox.showinfo('نجاح', 'تم  التحديث بنجاح')
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(update_window, text=" حفظ التعديل",font=font_arial_title, command=save_changes,width=400,corner_radius=2).pack(ipady=5, padx=20,pady=10,)

def fetch_drop(total_variable,myList):
    query = f'SELECT * FROM customers'
    total_variable.execute(query)
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        myList.append(f'{variable[0]}-{variable[1]}')
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    return myList  # Retourner 0 si aucun résultat n'est trouvé   

def fetch_customer(prod_id):
    connect_db()
    query = f'''
    SELECT *
    FROM customers  WHERE id = %s'''
    
    ''' '''
    
    my_cursor.execute(query, (prod_id,))
    result = my_cursor.fetchone()
    return result


def delete_customer(customer_id, update_callback):
    connect_db()
    try:
        query = f"DELETE FROM customers WHERE id = {customer_id}"
        my_cursor.execute(query)
        connect.commit()
        messagebox.showinfo('نجاح', 'تم  الحذف بنجاح')
        
        # Appel de la fonction pour actualiser les données
        update_callback()
    except Exception as e:
        messagebox.showerror('Error', str(e))

# Function to show customers as a styled table with pagination
def show_customers_table(parent, limit=10,is_admin= 0):
    def load_page(page_num):
        nonlocal offset
        offset = (page_num - 1) * limit
        update_table()

    def update_table():
        # Clear previous table data
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Fetch new data
        data = fetch_customers(limit, offset)

        # Add data rows
        for row_index, row in enumerate(data):
            row = row[::-1]  # Reverse the row data
            for col_index, value in enumerate(row):
                font_arial = ('Arial',12.5,)
                
                label = ctk.CTkLabel(
                    data_frame,
                    text=value,
                    font=font_arial,anchor='e',
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                label1 = ctk.CTkLabel(
                    data_frame,
                    text=row_index+1,
                    font=font_arial,anchor='e',
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                label1.grid(row=row_index, column=5 if is_admin == 1 else 4, sticky="e", padx=5, pady=1)
                
                label.grid(row=row_index, column=col_index + 1 if is_admin == 1 else col_index, sticky="nsew", padx=5, pady=1)
                
                font_arial_btn = ('Arial',14,'bold')
                buttons_frame = ctk.CTkFrame(data_frame, height=40,fg_color="#fff",width=100) 
                
                buttons_frame.grid(row=row_index , column=0, sticky="nsew", padx=(5,0), pady=5) if is_admin == 1 else buttons_frame.grid_remove()
                
                
                edit_image_path = os.path.join(os.path.dirname(__file__), "images", "edit.png")
                edit_image = ctk.CTkImage(light_image=Image.open(edit_image_path), size=(15, 15),)
                update_button = ctk.CTkButton(buttons_frame, text="",text_color="black",
                        image=edit_image,
                        fg_color='#fff',border_color='#f0f0f0',border_width=1,corner_radius=2,
                        hover_color='#eee',
                        width=40,
                        font=font_arial_btn,        
                        command=lambda row=row: open_update_window(row[::-1],update_table)
                        )
                update_button.pack(side="right", padx=5, pady=5) if is_admin == 1 else update_button.pack_forget()
                
                delete_image_path = os.path.join(os.path.dirname(__file__), "images", "trash-can.png")
                delete_image = ctk.CTkImage(light_image=Image.open(delete_image_path), size=(20, 20),)
                delete_button = ctk.CTkButton(buttons_frame,
                        text="",
                        text_color="black",
                        image=delete_image,
                        fg_color='#fff',border_color='#f0f0f0',border_width=1,corner_radius=2,
                        hover_color='#eee',
                        font=font_arial_btn, 
                        width=40,
                        command=lambda row=row: delete_customer(row[::-1][0], update_table)
                        )
                delete_button.pack(side="right", padx=5, pady=5,after=update_button) if is_admin == 1 else delete_button.pack_forget()
    
    show_title_frame(parent,update_table)
    offset = 0

    # Table headers
    columns = (' رقم ', 'الاسم ', 'الهاتف','البريد الالكتروني', 'العنوان')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="#fff",border_width=1,border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure(( 3, 4), weight=2, uniform='a') if is_admin == 1 else header_frame.columnconfigure((2,3), weight=2, uniform='a')
    header_frame.columnconfigure((1,2), weight=3, uniform='a')  if is_admin == 1 else header_frame.columnconfigure((0,1), weight=3, uniform='a')
    header_frame.columnconfigure((0,5), weight=1, uniform='a')  if is_admin == 1 else header_frame.columnconfigure((4), weight=1, uniform='a')
    font_arial = ('Arial',14,'bold')
    
    # header_frame.columnconfigure(2, weight=2)

    # Add column headings
    for col_index, col_name in enumerate(columns):
        label = ctk.CTkLabel(
            header_frame,
            text=col_name,
            font=font_arial,anchor='e',
            text_color="black",
            fg_color="#fff",
            corner_radius=5,
            width=100
        )      
        action_lab =ctk.CTkLabel(
            header_frame,
            text='الاجراءات',
            font=font_arial,
            text_color="black",
            fg_color="#fff",
            # fg_color="#fff",
            corner_radius=1,
            width=100
        )
        action_lab.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) if is_admin == 1 else action_lab.grid_remove()
        label.grid(row=0, column=col_index+1 if is_admin == 1 else col_index, sticky="nsew", padx=5, pady=5)

    # Data frame
    data_frame = ctk.CTkFrame(parent, corner_radius=2,  fg_color="#fff",border_width=1,border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure(( 3, 4), weight=2, uniform='a') if is_admin == 1 else data_frame.columnconfigure((2,3), weight=2, uniform='a')
    data_frame.columnconfigure((1,2), weight=3, uniform='a')  if is_admin == 1 else data_frame.columnconfigure((0,1), weight=3, uniform='a')
    data_frame.columnconfigure((0,5), weight=1, uniform='a') if is_admin == 1 else data_frame.columnconfigure((4), weight=1, uniform='a') 


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

def show_title_frame(parent, refresh_callback):
    
    # Table headers

    # Header frame
    title_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="transparent",)
    title_frame.pack(fill='x', padx=20, pady=5,)

    title_label = ctk.CTkLabel(
        master=title_frame,
        text="قائمة العملاء",
        font=('Arial',20,'bold'),
        # text_color="#0066cc"
        compound="right"
    )
    
    title_label.pack(side="right",  pady=5, ipadx=5, ipady=5)

    # button de refresh
    image_path = os.path.join(os.path.dirname(__file__), "images", "refresh.png")
    
    image = ctk.CTkImage(light_image=Image.open(image_path), size=(20, 20),)
    refresh_button = ctk.CTkButton(
        master=title_frame,
        image=image,
        text="تحديث",
        fg_color="#fff",
        hover_color="#f0f0f0",
        font=('Arial',14,),
        text_color="#333",
        corner_radius=2,width=60,
        command=refresh_callback
    )
    # add button 
    add_image_path = os.path.join(os.path.dirname(__file__), "images", "add-user (1).png")
    add_image = ctk.CTkImage(light_image=Image.open(add_image_path), size=(20, 20),)
    
    add_customer_button = ctk.CTkButton(
        master=title_frame,
        # image=add_image,
        text="اضافة عميل",
        font=('Arial',14,),
        fg_color="#0b0d0e",
        text_color="#fff",hover=False,
        compound="right",
        corner_radius=2,width=80,
        command=lambda: open_add_window(refresh_callback)
    )
    add_customer_button.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5)
    refresh_button.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5,anchor="w")    
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
                        border_width=1, border_color='#ddd', corner_radius=2, width=width)
    entry.pack(ipady=10 , padx=20)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text,wid=200):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text, width=wid)
    label_widgets.append(label)
    return label


# Function to create the customers frame
# def create_customers_frame(root,user=None):
#     customers_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")


#     show_customers_table(customers_frame,is_admin = user[4] if user else 0)
#     return customers_frame

def create_customers_frame(root):
    customers_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")


    # Frame pour le tableau des catégories
    table_frame = ctk.CTkFrame(customers_frame, fg_color="#fff")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def set_user(user):
        # Nettoyer la frame avant d'afficher un nouveau tableau
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Afficher le tableau des catégories en fonction de l'utilisateur
        is_admin = user[4] if user else 0
        show_customers_table(table_frame, is_admin=is_admin)

    # Ajouter la méthode set_user à la frame
    customers_frame.set_user = set_user

    return customers_frame


# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')


# customers_frame = create_customers_frame(window)
# customers_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()