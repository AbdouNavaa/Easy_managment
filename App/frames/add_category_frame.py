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
    query = f'SELECT * FROM product_categories'
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
    entry = ctk.CTkEntry(parent, justify=justify,font=("Arial", 14), fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=8, width=400)
    entry.pack(ipady=10 , padx=20)
    entry_widgets.append(entry)
    return entry

def create_label(parent,text):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text)
    label_widgets.append(label)
    return label


# import 
def create_add_category_frame(root):
    
    add_category_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    add_category_frame.pack(padx=400,pady=10,ipady=10,)
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(add_category_frame,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#eee',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#eee',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # name 
    create_label(add_category_frame,"اسم الفئة").pack(ipady=10 ,pady=5, padx=20,fill='x')
    name_entry = create_entry(add_category_frame)

    # desc 
    create_label(add_category_frame,"وصف الفئة").pack(ipady=10 ,pady=5, padx=20,fill='x')
    desc_entry = ctk.CTkTextbox(add_category_frame, font=("Arial", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,width=400,)
    desc_entry.pack(ipady=10 , padx=20,)
    
    # parent
    connect_db()
    list_of_categories = []
    fetch_drop(categories, list_of_categories)

    ctk.CTkLabel(add_category_frame,anchor='center', text="القسم",font=font_arial_title,bg_color='#f9f9f9').pack(ipady=10 ,pady=5, padx=20,fill='x')

    category_entry = ctk.CTkOptionMenu(
        add_category_frame,values=list_of_categories,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
    )
    category_entry.pack(ipady=10 , padx=20,)
    
    
    def add_categories():
        name = name_entry.get()
        description = desc_entry.get(index1='0.0', index2='end')
        category_id = category_entry.get().split('-')[0]
        # created_at = created_at_entry.get_date().strftime('%Y-%m-%d') if created_at_entry.get_date() else None
        
        # Validation des informations de connexion
        if name == "" or description == "" :
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                
                connect_db()
                query = 'insert into product_categories values(null,%s,%s,%s,NOW())'
                my_cursor.execute(query,(name, description,category_id))
                connect.commit()
                messagebox.showinfo('Success', 'category added successfully')
                
                
                result = messagebox.askyesno('category added successfully', 'do you want to clean the form?' , parent=add_category_frame)
                if result == True:
                    name_entry.delete(0,tk.END)
                    desc_entry.delete(1.0, tk.END)
            except Exception as e:
                messagebox.showerror('Error', str(e))
            

    add_button = ctk.CTkButton(
        add_category_frame,
        text="تاكيد",
        command=add_categories
        
    )
    add_button.pack(pady=10,fill='x',padx=20,ipady=10)
    
    
    
    return add_category_frame


# window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# # window.geometry('1200x550')
# window.state('zoomed')

# add_category_frame = create_add_category_frame(window)
# add_category_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()