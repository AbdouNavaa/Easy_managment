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


# import 
def create_add_customer_frame(root):
    
    add_customer_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    add_customer_frame.pack(padx=400,pady=10,ipady=10,)
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(add_customer_frame,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # name 
    create_label(add_customer_frame,"اسم العميل").pack(ipady=10 ,pady=5, padx=20,fill='x')
    name_entry = create_entry(add_customer_frame)

    # phone 
    create_label(add_customer_frame,"هاتف العميل").pack(ipady=10 ,pady=5, padx=20,fill='x')
    phone_entry = create_entry(add_customer_frame)

    
    # email 
    create_label(add_customer_frame,"البريد الالكتروني").pack(ipady=10 ,pady=5, padx=20,fill='x')
    email_entry = ctk.CTkEntry(add_customer_frame,font=font_arial, fg_color='#fff', 
            border_width=1, border_color='#ddd', corner_radius=8, width=400)
    email_entry.pack(ipady=10 , padx=20)
    
    # address 
    create_label(add_customer_frame,"العنوان").pack(ipady=10 ,pady=5, padx=20,fill='x')
    address_entry = create_entry(add_customer_frame)
    
    # labels frame
    labels_frame = ctk.CTkFrame(add_customer_frame,fg_color='transparent',)
    labels_frame.pack( ipady=10 , padx=20, pady=2)
    
    # entries frame
    entries_frame = ctk.CTkFrame(add_customer_frame,fg_color='transparent',width=400)
    entries_frame.pack( ipady=10 , padx=20, pady=2)
    # balance
    create_label(labels_frame,"الرصيد").pack(ipady=10 ,pady=5, fill='x',side='right')
    balance_entry = create_entry(entries_frame,200)
    balance_entry.pack(ipady=10 , padx=20,side='right')

    
    # is_active 
    create_label(labels_frame,"الحالة").pack(ipady=10 ,pady=5, fill='x',side='left')
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
        balance = float(balance_entry.get())
        int(is_active_entry.get()[0])
        is_active = int(is_active_entry.get()[0])
        
        # Validation des informations de connexion
        if name == "" or phone == "" or email == "" or address == "" :
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                connect_db()
                query = '''INSERT INTO `customers` ( `name`, `phone`, `email`, `address`, `created_at`, `balance`, `is_active`) 
                VALUES (%s, %s, %s, %s, NOW(), %s, %s)'''
                
                my_cursor.execute(query, (name, phone, email, address, balance, is_active))
                connect.commit()
                messagebox.showinfo('Success', 'Customer added successfully')
                
                
                result = messagebox.askyesno('Customer added successfully', 'do you want to clean the form?' , parent=add_customer_frame)
                if result == True:
                    name_entry.delete(0,tk.END)
                    phone_entry.delete(0, tk.END)
                    email_entry.delete(0, tk.END)
                    address_entry.delete(0, tk.END)
                    balance_entry.delete(0, tk.END)
                    is_active_entry.set(0)
                    # add_customer_frame.destroy()
            except Exception as e:
                messagebox.showerror('Error', str(e))
            

    add_button = ctk.CTkButton(
        add_customer_frame,
        text="تاكيد",
        width=400,
        command=add_customers
            )
    add_button.pack(pady=10,padx=20,ipady=10)
    
    
    
    return add_customer_frame


# window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# # window.geometry('1200x550')
# window.state('zoomed')

# add_customer_frame = create_add_customer_frame(window)
# add_customer_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()