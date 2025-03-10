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
        global users
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        users = connect.cursor()
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))


# Function to fetch users with pagination
def fetch_users(limit=10, offset=0):
    connect_db()
    query = f'''
    SELECT id, username,email,date(created_at),updated_at
    FROM users 
    LIMIT {limit} OFFSET {offset}'''
    my_cursor.execute(query)
    return my_cursor.fetchall()

# fenetere pour ajouter une categorie
import bcrypt

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
    
    direction_btn(btns_frame,'Fr').pack(pady=10, padx=(5, 155), side='left')
    direction_btn(btns_frame,'Ar').pack(pady=10, padx=(155, 5), side='right')
    # name 
    create_label(add_window,"اسم المستخدم").pack(ipady=10 ,pady=5, padx=20,fill='x')
    username_entry = create_entry(add_window) 
    
    name_error = error_message(add_window, "")
    name_error.pack(ipady=10 , padx=20)
    
    # email
    create_label(add_window,"البريد الالكتروني").pack(ipady=10 ,pady=5, padx=20,fill='x')
    email_entry = create_entry(add_window)
    email_error = error_message(add_window, "")
    email_error.pack(ipady=10 , padx=20)
    
    # password_hash
    create_label(add_window,"كلمة المرور").pack(ipady=10 ,pady=5, padx=20,fill='x')
    password_entry = create_entry(add_window)
    password_error = error_message(add_window, "")
    password_error.pack(ipady=10 , padx=20)
    def add_users():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        
        # Réinitialiser les messages d'erreur
        name_error.configure(text="")
        password_error.configure(text="")
        email_error.configure(text="")
        
        
        # Validation des champs
        has_error = False

        if not validate_string(username):
            name_error.configure(text="ادخل اسم صحيح (حروف فقط)")
            has_error = True

        if not validate_email(email):
            email_error.configure(text="ادخل بريد الكتروني صحيح")
            has_error = True
            
        if password == '' or len(password) < 4:
            password_error.configure(text="ادخل كلمة مرور صحيحة ( 4 حروف او ارقام على الأقل)")
            has_error = True


        if has_error:
            return
        
        else:
            try:
                connect_db()
                
                # Hash the password
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                query = '''INSERT INTO `users` ( `username`, `email`, `password_hash`, `created_at`, `updated_at`) 
                VALUES (%s, %s, %s, NOW(),NOW())'''
                my_cursor.execute(query, (username, email, hashed_password))
                connect.commit()
                messagebox.showinfo('نجاح', 'تم اضافة  المستخدم بنجاح')
                refresh_callback()
                
                result = messagebox.askyesno('تم الاضافة', 'هل تريد اضافة مستخدم جديد?' , parent=add_window)
                if result == True:
                    username_entry.delete(0,tk.END)
                    email_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror('Error', str(e))

    add_button = ctk.CTkButton(
        add_window,
        text="تاكيد",
        width=400,
        command=add_users,corner_radius=2,font=font_arial_title
    )
    add_button.pack(pady=(10,40),padx=20,ipady=10)# Fonction pour afficher la fenêtre de mise à jour
def open_update_window(user, update_callback):
    
    update_window = tk.Toplevel(background='#fff')
    update_window.grab_set()  # Make the window modal
    update_window.focus_set()
    # update_window.pack()
    update_window.title("تعديل")

    custom=fetch_user(user[0])
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    # direction btn
    btns_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    
    direction_btn(btns_frame,'Fr').pack(pady=10, padx=(5, 155), side='left')
    direction_btn(btns_frame,'Ar').pack(pady=10, padx=(155, 5), side='right') 
    # username 
    create_label(update_window,"اسم المستخدم ").pack(ipady=10 ,pady=5, padx=20,fill='x')
    username_entry = create_entry(update_window)
    username_entry.insert(0, custom[1])  # Pré-remplir avec la valeur actuelle
    
    name_error = error_message(update_window, "")
    name_error.pack(ipady=10 , padx=20)

    
    # email 
    create_label(update_window,"البريد الالكتروني").pack(ipady=10 ,pady=5, padx=20,fill='x')
    email_entry = ctk.CTkEntry(update_window,font=font_arial, fg_color='#fff', 
            border_width=1, border_color='#ddd', corner_radius=2, width=400)
    email_entry.pack(ipady=10 , padx=20)
    email_entry.insert(0, custom[2])  
    email_error = error_message(update_window, "")
    email_error.pack(ipady=10 , padx=20)
    
    # password
    create_label(update_window,"كلمة المرور").pack(ipady=10 ,pady=5, padx=20,fill='x')
    password_entry = create_entry(update_window)
    password_entry.insert(0, custom[3]) 
    password_error = error_message(update_window, "")
    password_error.pack(ipady=10 , padx=20)
    
    # Bouton pour sauvegarder les modifications
    def save_changes():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        id = user[0]
        
        # Réinitialiser les messages d'erreur
        name_error.configure(text="")
        password_error.configure(text="")
        email_error.configure(text="")
        
        
        # Validation des champs
        has_error = False

        if not validate_string(username):
            name_error.configure(text="ادخل اسم صحيح (حروف فقط)")
            has_error = True

        if not validate_email(email):
            email_error.configure(text="ادخل بريد الكتروني صحيح")
            has_error = True
            
        if password == '' or len(password) < 4:
            password_error.configure(text="ادخل كلمة مرور صحيحة")
            has_error = True


        if has_error:
            return

        
        try:
            connect_db()
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            query = '''UPDATE `users` SET `username`=%s, `email`=%s, `password_hash`=%s, updated_at=NOW() WHERE `id`=%s'''
            my_cursor.execute(query, (username, email, hashed_password, id))
            connect.commit()
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

        messagebox.showinfo('نجاح', 'تم تعديل معلومات المستخدم بنجاح')
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(update_window, text=" حفظ التعديل",font=font_arial_title, command=save_changes,width=400,corner_radius=2).pack(ipady=5, padx=20,pady=(10,40),)



def fetch_user(prod_id):
    connect_db()
    query = f'''
    SELECT *
    FROM users  WHERE id = %s'''
    
    ''' '''
    
    my_cursor.execute(query, (prod_id,))
    result = my_cursor.fetchone()
    return result


def delete_user(user_id, update_callback):
    connect_db()
    try:
        query = f"DELETE FROM users WHERE id = {user_id}"
        my_cursor.execute(query)
        connect.commit()
        messagebox.showinfo('نجاح', ' تم حذف المستخدم بنجاح')
        
        # Appel de la fonction pour actualiser les données
        update_callback()
    except Exception as e:
        messagebox.showerror('Error', str(e))

# Function to show users as a styled table with pagination
def show_users_table(parent, limit=10,is_admin= 0):
    def load_page(page_num):
        nonlocal offset
        offset = (page_num - 1) * limit
        update_table()

    def update_table():
        # Clear previous table data
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Fetch new data
        data = fetch_users(limit, offset)

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
                    font=font_arial,anchor='center',
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                label1.grid(row=row_index, column=5 if is_admin == 1 else 4, sticky="nsew", padx=5, pady=5)
                
                label.grid(row=row_index, column=col_index + 1 if is_admin == 1 else col_index, sticky="nsew", padx=5, pady=5)
                
                
                font_arial_btn = ('Arial',14,'bold')
                buttons_frame = ctk.CTkFrame(data_frame, height=40,
                                            fg_color="transparent",
                                            # fg_color="#fcfcfc",
                                        ) 
                
                buttons_frame.grid(row=row_index , column=0, sticky="nsew", padx=(5,0), pady=5) if is_admin == 1 else buttons_frame.grid_remove()
                
            # edit
                edit_image_path = os.path.join(os.path.dirname(__file__), "images", "edit.png")
                edit_image = ctk.CTkImage(light_image=Image.open(edit_image_path), size=(15, 15),)
                update_button = ctk.CTkButton(buttons_frame, text="",text_color="black",
                        image=edit_image,
                        fg_color='#fff',border_color='#f0f0f0',border_width=1,corner_radius=2,
                        hover_color='#f0f0f0',
                        width=50,
                        font=font_arial_btn,        
                        command=lambda row=row: open_update_window(row[::-1],update_table)
                        )
                update_button.pack(side="right", padx=5, pady=5) if is_admin == 1 else update_button.pack_forget()
                
            #delete 
                delete_image_path = os.path.join(os.path.dirname(__file__), "images", "trash-can.png")
                delete_image = ctk.CTkImage(light_image=Image.open(delete_image_path), size=(20, 20),)
                delete_button = ctk.CTkButton(buttons_frame,
                        text="",
                        text_color="black",
                        image=delete_image,
                        fg_color='#fff',border_color='#f0f0f0',border_width=1,corner_radius=2,
                        hover_color='#f0f0f0',
                        font=font_arial_btn, 
                        width=60,
                        command=lambda row=row: delete_user(row[::-1][0], update_table)
                        )
                delete_button.pack(side="right", padx=5, pady=5,after=update_button) if is_admin == 1 else delete_button.pack_forget()
                
    
    show_title_frame(parent,update_table)
    offset = 0

    # Table headers
    # is_admin
    columns = (' رقم ', 'الاسم الكامل ','البريد الالكتروني', 'تاريخ التسجيل','آخر تعديل')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="#fff",border_width=1,border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((1,2 ,3, 4), weight=2, uniform='a')if is_admin == 1 else header_frame.columnconfigure((0, 1, 2,3), weight=1, uniform='a')
    header_frame.columnconfigure((0,5), weight=1, uniform='a')if is_admin == 1 else header_frame.columnconfigure((4), weight=1, uniform='a')
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
        action_lab.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)if is_admin == 1 else action_lab.grid_remove()
        label.grid(row=0, column=col_index+1 if is_admin == 1 else col_index, sticky="nsew", padx=5, pady=5)

    # Data frame
    data_frame = ctk.CTkFrame(parent, corner_radius=2,  fg_color="#fff",border_width=1,border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)

    data_frame.columnconfigure((1,2 ,3, 4), weight=2, uniform='a')if is_admin == 1 else data_frame.columnconfigure((0, 1, 2,3), weight=1, uniform='a')
    data_frame.columnconfigure((0,5), weight=1, uniform='a')if is_admin == 1 else data_frame.columnconfigure((4), weight=1, uniform='a')


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
    title_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="transparent",)
    title_frame.pack(fill='x', padx=20, pady=5,)

    font_arial_title = ('Arial',20,'bold')
    font_arial = ('Arial',14,)
    title_label = ctk.CTkLabel(
        master=title_frame,
        text="قائمة المستخدمين",
        font=font_arial_title,
        # compound="right"
    )
    title_label.pack(side="right", padx=5, pady=5, ipadx=5, ipady=5)
    
    # add 3 button 
    add_image_path = os.path.join(os.path.dirname(__file__), "images", "add-user (2).png")
    
    add_image = ctk.CTkImage(light_image=Image.open(add_image_path), size=(20, 20),)
    add_inventory_button = ctk.CTkButton(
        master=title_frame,
        # image=add_image,
        text=" اضافة مستخدم  ",
        font=font_arial,
        width=40,
        text_color="#fff",
        fg_color="#0b0d0e",hover=False,
        corner_radius=2,
        command=lambda: open_add_window(refresh_callback)
    )
    add_inventory_button.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5)
    image_path = os.path.join(os.path.dirname(__file__), "images", "refresh.png")
    image = ctk.CTkImage(light_image=Image.open(image_path), size=(20, 20),)

    refresh_button = ctk.CTkButton(
        title_frame,
        image=image,
        text="تحديث",
        fg_color="#fff",
        hover_color="#f0f0f0",
        font=font_arial,
        width=40,corner_radius=2,
        text_color="#333",
        # command=lambda: refresh_callback,compound="left"
        command=lambda: refresh(refresh_callback),compound="left"
    )
    refresh_button.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5)
def refresh(refresh_callback):
    global search_results  # Déclarer `search_results` comme global
    search_results = []
    # Appeler la fonction de rafraîchissement pour afficher les données à partir de la base de données
    refresh_callback()


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


import re 
def error_message(parent,text):
    message = ctk.CTkLabel(parent, text="", text_color="red", font=("Arial", 12),height=10)
    return message
# Fonctions de validation
def validate_string(input_str):
    return bool(re.match(r'^[A-Za-z\s]+[0-9]+$', input_str))


def validate_email(input_str):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', input_str))

def direction_btn(parent,text):
    btn = ctk.CTkButton(parent, text=text, width=40, fg_color='#f6f7f7',hover_color='#eee', text_color='black', command=lambda: direction(text))
    btn.pack(pady=10, padx=(5, 155), side='left')
    return btn

# Function to create the users frame
# def create_users_frame(root ,user=None):
#     users_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

#     # print('User_:',user[0]) if user else None
#     show_users_table(users_frame ,is_admin = user[4] if user else 0)
#     return users_frame


def create_users_frame(root):
    users_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")


    # Frame pour le tableau des catégories
    table_frame = ctk.CTkFrame(users_frame, fg_color="#fff")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def set_user(user):
        # Nettoyer la frame avant d'afficher un nouveau tableau
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Afficher le tableau des catégories en fonction de l'utilisateur
        is_admin = user[4] if user else 0
        show_users_table(table_frame, is_admin=is_admin)

    # Ajouter la méthode set_user à la frame
    users_frame.set_user = set_user

    return users_frame
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')


# users_frame = create_users_frame(window)
# users_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()