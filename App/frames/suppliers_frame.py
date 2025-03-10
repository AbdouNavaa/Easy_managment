import customtkinter as ctk
from tkinter import messagebox
import pymysql
import tkinter as tk

import tkinter as tk
import os
from PIL import Image, ImageTk

# Connection settings
def connect_db():
    try:
        global connect
        global my_cursor
        global suppliers
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        suppliers = connect.cursor()
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))


# Function to fetch suppliers with pagination
def fetch_suppliers(limit=10, offset=0):
    connect_db()
    query = f'SELECT id, name,name, phone,email, address FROM suppliers LIMIT {limit} OFFSET {offset}'
    my_cursor.execute(query)
    return my_cursor.fetchall()


# Function to show suppliers as a styled table with pagination
def show_suppliers_table(parent, limit=10,is_admin= 0):
    def load_page(page_num):
        nonlocal offset
        offset = (page_num - 1) * limit
        update_table()

    def update_table():
        # Clear previous table data
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Fetch new data
        data = fetch_suppliers(limit, offset)

        # Add data rows
        for row_index, row in enumerate(data):
            row = row[::-1]  # Reverse the row data
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
                    text=row_index+1,
                    font=font_arial,
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                
                label1.grid(row=row_index, column=6 if is_admin == 1 else 5, sticky="e", padx=5, pady=5)
                
                label.grid(row=row_index, column=col_index + 1 if is_admin == 1 else col_index, sticky="e", padx=5, pady=5)
                
                font_arial_btn = ('Arial',14,'bold')
                buttons_frame = ctk.CTkFrame(data_frame, width=100,height=40,fg_color="transparent",) 
                
                buttons_frame.grid(row=row_index , column=0, sticky="nsew", padx=5, pady=5) if is_admin == 1 else buttons_frame.grid_remove()

                
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
                update_button.grid(row=0,column=1) if is_admin == 1 else update_button.pack_forget()

                
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
                        command=lambda row=row: delete_supplier(row[::-1][0], update_table)
                        )
                delete_button.grid(row=0,column=0,padx=5)if is_admin == 1 else delete_button.pack_forget()
                
    show_title_frame(parent,update_table)

    offset = 0

    # Table headers
    columns = ("رقم",'اسم المورد ', 'الشخص المسؤول ', 'رقم الهاتف', 'البريد الالكتروني',"العنوان")
    # columns = ('القطعة رقم ', 'الاسم ', 'الوصف', 'المنتجات عدد',  'الإجراءات')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="#fff",border_width=1,border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure(( 1,2, 4, 5), weight=2, uniform='a')  if is_admin == 1 else header_frame.columnconfigure((0,1,2,4,5), weight=2, uniform='a')
    header_frame.columnconfigure((0,3,6), weight=1, uniform='a') if is_admin == 1 else header_frame.columnconfigure((2,5), weight=1, uniform='a')
    
    # header_frame.columnconfigure((0, 1, 2,3, 4, 5,6), weight=1, uniform='a') if is_admin == 1 else header_frame.columnconfigure((0,1,2,3,4,5), weight=1, uniform='a')
    font_arial = ('Arial',14,'bold')    
    # header_frame.columnconfigure(2, weight=2)

    # Add column headings
    for col_index, col_name in enumerate(columns):
        label = ctk.CTkLabel(
            header_frame,
            text=col_name,
            font=font_arial,
            text_color="black",
            fg_color="transparent",
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
        action_lab.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)if is_admin == 1 else action_lab.grid_remove()
        label.grid(row=0, column=col_index+1 if is_admin == 1 else col_index, sticky="e", padx=5, pady=5)

    # Data frame
    data_frame = ctk.CTkFrame(parent, corner_radius=2,  fg_color="#fff",border_width=1,border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure(( 1,2, 4, 5), weight=2, uniform='a')  if is_admin == 1 else data_frame.columnconfigure((0,1,2,4,5), weight=2, uniform='a')
    data_frame.columnconfigure((0,3,6), weight=1, uniform='a') if is_admin == 1 else data_frame.columnconfigure((2,5), weight=1, uniform='a')

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
    
import re 
# Fonctions de validation
def validate_string(input_str):
    return bool(re.match(r'^[A-Za-z\s]+$', input_str))

def validate_number(input_str):
    # Vérifie que l'entrée contient uniquement des chiffres et a une longueur d'au moins 5
    return bool(re.match(r'^[0-9]{8,}$', input_str))

def validate_email(input_str):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', input_str))

def direction_btn(parent,text):
    btn = ctk.CTkButton(parent, text=text, width=40, fg_color='#f6f7f7',hover_color='#eee', text_color='black', command=lambda: direction(text))
    btn.pack(pady=10, padx=(5, 155), side='left')
    return btn
    
def open_add_window(refresh_callback):
    add_window = tk.Toplevel(background='#fff')
    add_window.grab_set()  # Make the window modal
    add_window.focus_set()
    add_window.title("اضافة مورد جديد")

    font_arial_title = ("Arial", 16, 'bold')
    font_arial = ("Arial", 14)
    global justify
    justify = 'left'

    # direction btn
    btns_frame = ctk.CTkFrame(add_window, fg_color='transparent', width=400)
    btns_frame.pack(ipady=10, padx=20, pady=2)
    
    direction_btn(btns_frame,'Fr').pack(pady=10, padx=(5, 155), side='left')
    direction_btn(btns_frame,'Ar').pack(pady=10, padx=(155, 5), side='right')
    # name
    name_label = create_label(add_window, "اسم المورد" )
    name_entry = create_entry(add_window)

    # Label d'erreur pour le nom
    name_error_label = error_message(add_window, "")
    
    # phone
    phone_label = create_label(add_window, "رقم الهاتف", )
    phone_entry = create_entry(add_window)

    # Label d'erreur pour le téléphone
    phone_error_label = error_message(add_window, "")

    # email
    email_label = create_label(add_window, "البريد الالكتروني", )
    email_entry = ctk.CTkEntry(add_window, font=font_arial, fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=2, width=400)
    email_entry.pack(ipady=10, padx=20)

    # Label d'erreur pour l'email
    email_error_label = error_message(add_window, "")

    # address
    address_label = create_label(add_window, "العنوان", )
    address_entry = create_entry(add_window)
    # Label d'erreur pour l'adresse
    address_error_label = error_message(add_window, "")


    def save_changes():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        # Réinitialiser les messages d'erreur
        name_error_label.configure(text="")
        phone_error_label.configure(text="")
        email_error_label.configure(text="")
        address_error_label.configure(text="")

        # Validation des champs
        has_error = False

        if not validate_string(name):
            name_error_label.configure(text="ادخل اسم صحيح (حروف فقط)")
            has_error = True

        if not validate_number(phone):
            phone_error_label.configure(text="ادخل رقم هاتف صحيح (8 أرقام على الأقل)")
            has_error = True

        if not validate_email(email):
            email_error_label.configure(text="ادخل بريد الكتروني صحيح")
            has_error = True
        
        if address == '':
            address_error_label.configure(text="ادخل  عنوان ")
            has_error = True      
        if has_error:
            return  # Ne pas continuer si une erreur est détectée

        try:
            connect_db()
            query = 'INSERT INTO suppliers (name, phone, email, address) VALUES (%s, %s, %s, %s)'
            my_cursor.execute(query, (name, phone, email, address))
            connect.commit()
            messagebox.showinfo('نجاح', 'تمت الاضافة بنجاح')
            refresh_callback()
            result = messagebox.askyesno('تم الاضافة', 'هل تريد اضافة مورد جديد؟', parent=add_window)
            if result:
                name_entry.delete(0, tk.END)
                phone_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                address_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Bouton pour sauvegarder les modifications
    ctk.CTkButton(add_window, text=" حفظ", command=save_changes, corner_radius=2, font=font_arial_title).pack(pady=(10,15), padx=20, fill='x', ipady=5)


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
    entry.pack(ipady=10, padx=20)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text, width=400)
    label.pack(ipady=10, pady=5, padx=20)
    label_widgets.append(label)
    return label

def error_message(parent,text):
    message = ctk.CTkLabel(parent, text="", text_color="red", font=("Arial", 12),height=10)
    message.pack(padx=20,)
    return message
# Fonction pour afficher la fenêtre de mise à jour
def open_update_window(supplier, update_callback):
    global entry_widgets
    entry_widgets = []  # Reset the list for each new window
    
    update_window = tk.Toplevel(background='#fff')
    update_window.grab_set()  # Make the window modal
    update_window.focus_set()
    update_window.title("تعديل المورد")

    supp=fetch_supplier(supplier[0])
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)   
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    
    
    direction_btn(btns_frame,'Fr').pack(pady=10, padx=(5, 155), side='left')
    direction_btn(btns_frame,'Ar').pack(pady=10, padx=(155, 5), side='right')

    #name
    name_label = create_label(update_window,"اسم المورد")
    
    name_entry = create_entry(update_window)
    name_entry.insert(0,supplier[1])
    name_error_label = error_message(update_window, "")
    
    #phone
    phone_label = create_label(update_window,"رقم الهاتف")
    
    phone_entry = create_entry(update_window)
    phone_entry.insert(0,supplier[3])
    phone_error_label = error_message(update_window, "")
    
    #email
    email_label = create_label(update_window,"البريد الالكتروني")
    
    email_entry = ctk.CTkEntry(update_window, font=font_arial, 
    fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=2,width=400)
    email_entry.insert(0,supplier[4])
    email_entry.pack(ipady=10 , padx=20)
    email_error_label = error_message(update_window, "")
    
    #address
    address_label = create_label(update_window,"العنوان")
    address_entry = create_entry(update_window, )
    address_entry.insert(0, supplier[5])
    address_error_label = error_message(update_window, "")
    

    # Bouton pour sauvegarder les modifications
    def save_changes():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()
        
        id = supplier[0]
        
        # Réinitialiser les messages d'erreur
        name_error_label.configure(text="")
        phone_error_label.configure(text="")
        email_error_label.configure(text="")
        address_error_label.configure(text="")
        # Validation des champs
        has_error = False

        if not validate_string(name):
            name_error_label.configure(text="ادخل اسم صحيح (حروف فقط)")
            has_error = True

        if not validate_number(phone):
            phone_error_label.configure(text="ادخل رقم هاتف صحيح (8 أرقام على الأقل)")
            has_error = True

        if not validate_email(email):
            email_error_label.configure(text="ادخل بريد الكتروني صحيح")
            has_error = True
        
        if address == '':
            address_error_label.configure(text="ادخل  عنوان ")
            has_error = True      
        if has_error:
            return
        
        try:
            connect_db()
            query = 'update suppliers set name=%s,phone=%s,email=%s,address=%s  where id=%s'
            my_cursor.execute(query,(name,phone,email,address,id))
            connect.commit()
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

        messagebox.showinfo('نجاح', 'تم تحديث  معلومات المورد بنجاح')
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(update_window, text=" حفظ", command=save_changes,corner_radius=2,font=font_arial_title).pack(pady=(10,15),padx=20,ipady=5,fill='x',expand=True)
def fetch_supplier(supplier_id):
    connect_db()
    query = f'''
    SELECT *
    FROM suppliers  WHERE id = %s'''
    
    my_cursor.execute(query, (supplier_id,))
    result = my_cursor.fetchone()
    return result

def delete_supplier(supplier_id, update_callback):
    connect_db()
    try:
        query = f"DELETE FROM suppliers WHERE id = {supplier_id}"
        my_cursor.execute(query)
        connect.commit()
        messagebox.showinfo('نجاح', 'تم حذف المورد بنجاح')
        # Appel de la fonction pour actualiser les données
        update_callback()
    except Exception as e:
        messagebox.showerror('Error', str(e))


def show_title_frame(parent,refresh_callback ):
    
    # Table headers

    # Header frame
    title_frame = ctk.CTkFrame(parent, corner_radius=20, fg_color="transparent",)
    title_frame.pack(fill='x', padx=20, pady=5)
    
    title_label = ctk.CTkLabel(
        master=title_frame,
        text="قائمة الموردين",
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
        corner_radius=2,width=70,
        command=refresh_callback
    )
    # add button 
    add_image_path = os.path.join(os.path.dirname(__file__), "images", "add.png")
    add_image = ctk.CTkImage(light_image=Image.open(add_image_path), size=(15, 15),)
    
    add_supplier_button = ctk.CTkButton(
        master=title_frame,
        # image=add_image,
        text="اضافة مورد ",
        font=('Arial',14,),
        fg_color="#333",hover=False,
        text_color="#fff",
        corner_radius=3,width=50,
        command=lambda: open_add_window(refresh_callback)
    )
    add_supplier_button.pack(side="left", padx=1, pady=5, ipadx=5, ipady=5)
    refresh_button.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5)    


# Function to create the suppliers frame
# def create_suppliers_frame(root,user=None):
#     suppliers_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

#     show_suppliers_table(suppliers_frame,is_admin = user[4] if user else 0)
#     return suppliers_frame

def create_suppliers_frame(root):
    suppliers_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")


    # Frame pour le tableau des catégories
    table_frame = ctk.CTkFrame(suppliers_frame, fg_color="#fff")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def set_user(user):
        # Nettoyer la frame avant d'afficher un nouveau tableau
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Afficher le tableau des catégories en fonction de l'utilisateur
        is_admin = user[4] if user else 0
        show_suppliers_table(table_frame, is_admin=is_admin)

    # Ajouter la méthode set_user à la frame
    suppliers_frame.set_user = set_user

    return suppliers_frame
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')


# suppliers_frame = create_suppliers_frame(window)
# suppliers_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()