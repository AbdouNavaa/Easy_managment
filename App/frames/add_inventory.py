import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pymysql
def connect_db():
    try:
        # create a connection object
        global connect
        global my_cursor
        global warehouses
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        warehouses = connect.cursor()
        # messagebox.showinfo('Connection Successful', 'Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
        
def fetch_drop(total_variable,myList):
    query = f'SELECT * FROM product_warehouses'
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
def create_entry(parent):
    entry = ctk.CTkEntry(parent, justify=justify,font=("Arial", 14), fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=2, width=400)
    entry.pack(ipady=10 , padx=20)
    entry_widgets.append(entry)
    return entry

def create_label(parent,text):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text,width=400)
    label_widgets.append(label)
    return label

def error_message(parent,text):
    message = ctk.CTkLabel(parent, text="", text_color="red", font=("Arial", 12),height=10)
    return message
# Fonctions de validation

# import 
def create_add_warehouse_frame(root):
    
    add_warehouse_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    add_warehouse_frame.pack(padx=400,pady=10,ipady=10,)
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(add_warehouse_frame,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#eee',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#eee',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # name 
    create_label(add_warehouse_frame,"اسم المخزون").pack(ipady=10 ,pady=5, padx=20,fill='x')
    name_entry = create_entry(add_warehouse_frame)
    name_error = error_message(add_warehouse_frame, "")
    name_error.pack(ipady=10 ,pady=5, padx=20,fill='x')
    

    # desc 
    create_label(add_warehouse_frame,"تفاصيل المخزون").pack(ipady=10 ,pady=5, padx=20,fill='x')
    desc_entry = create_entry(add_warehouse_frame)
    desc_error = error_message(add_warehouse_frame,"")
    desc_error.pack(ipady=10 ,pady=5, padx=20,fill='x')

    # location 
    create_label(add_warehouse_frame,"مكان المخزون").pack(ipady=10 ,pady=5, padx=20,fill='x')
    location_entry = create_entry(add_warehouse_frame)
    location_error = error_message(add_warehouse_frame,"")
    location_error.pack(ipady=10 ,pady=5, padx=20,fill='x')

    
    def add_warehouses():
        name = name_entry.get()
        description = desc_entry.get()
        location = location_entry.get()
        
        name_error.configure(text="")
        desc_error.configure(text="")
        location_error.configure(text="")
        has_error = False

        
        if  name == '':
            name_error.configure(text="الرجاء ادخال اسم المخزون")
            has_error = True

        if description == '':
            desc_error.configure(text="الرجاء ادخال تفاصيل المخزون")
            has_error = True

        if location == '':
            location_error.configure(text="الرجاء ادخال مكان المخزون")
            has_error = True
        
        if has_error:
            return

        else:
            try:
                
                connect_db()
                query = 'insert into warehouses (name,description,location,updated_at) values(%s,%s,%s,%s)'
                my_cursor.execute(query,(name, description,location, datetime.now()))
                connect.commit()
                messagebox.showinfo('نجاح', 'تم اضافة المخزون')
                
                
                result = messagebox.askyesno('تم اضافة المخزون', 'هل تريد الاضافة مرة اخرى?' , parent=add_warehouse_frame)
                if result == True:
                    name_entry.delete(0,tk.END)
                    desc_entry.delete(0, tk.END)
                    location_entry.delete(0, tk.END)
                    # add_warehouse_frame.destroy()
            except Exception as e:
                messagebox.showerror('Error', str(e))
            

    add_button = ctk.CTkButton(
        add_warehouse_frame,
        text="تاكيد",
        width=400,
        command=add_warehouses,font=font_arial_title,corner_radius=2
        
    )
    add_button.pack(pady=(10,30),padx=20,ipady=10)    
    
    
    return add_warehouse_frame


# window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# # window.geometry('1200x550')
# window.state('zoomed')

# add_warehouse_frame = create_add_warehouse_frame(window)
# add_warehouse_frame.pack(fill='x', expand=True)

# # run
# window.mainloop()