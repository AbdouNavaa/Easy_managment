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
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        categories = connect.cursor()
        # messagebox.showinfo('Connection Successful', 'Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
        
def fetch_drop(total_variable,myList):
    query = f'SELECT * FROM customers'
    total_variable.execute(query)
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        myList.append(f'{variable[0]}-{variable[1]}')
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    return myList  # Retourner 0 si aucun résultat n'est trouvé   

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
def create_entry(parent,width=400):
    entry = ctk.CTkEntry(parent, justify=justify,font=("Arial", 14), fg_color='#fff', 
                        border_width=1, border_color='#ddd', corner_radius=8, width=width)
    entry.pack(ipady=10 , padx=20)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text,wid=200):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text, width=wid)
    label_widgets.append(label)
    return label


import bcrypt

# import 
def create_add_user_frame(root):
    
    add_user_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    add_user_frame.pack(padx=400,pady=10,ipady=10,)
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(add_user_frame,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # name 
    create_label(add_user_frame,"اسم المستخدم").pack(ipady=10 ,pady=5, padx=20,fill='x')
    username_entry = create_entry(add_user_frame)
    
    # email
    create_label(add_user_frame,"البريد الالكتروني").pack(ipady=10 ,pady=5, padx=20,fill='x')
    email_entry = create_entry(add_user_frame)
    
    # password_hash
    create_label(add_user_frame,"كلمة المرور").pack(ipady=10 ,pady=5, padx=20,fill='x')
    password_entry = create_entry(add_user_frame)
    
    def add_users():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        
        # Validation des informations de connexion
        if username == "" or email == "" or password == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                connect_db()
                
                # Hash the password
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                query = '''INSERT INTO `users` ( `username`, `email`, `password_hash`, `created_at`, `updated_at`) 
                VALUES (%s, %s, %s, NOW(),NOW())'''
                my_cursor.execute(query, (username, email, hashed_password))
                connect.commit()
                messagebox.showinfo('Success', 'User added successfully')
                refresh_callback()
                
                result = messagebox.askyesno('User added successfully', 'Do you want to clean the form?', parent=add_user_frame)
                if result == True:
                    username_entry.delete(0,tk.END)
                    email_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror('Error', str(e))

    add_button = ctk.CTkButton(
        add_user_frame,
        text="تاكيد",
        width=400,
        command=add_users
    )
    add_button.pack(pady=10,padx=20,ipady=10)# Fonction pour afficher la fenêtre de mise à jour
    
    
    
    return add_user_frame


# window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# # window.geometry('1200x550')
# window.state('zoomed')

# add_user_frame = create_add_user_frame(window)
# add_user_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()