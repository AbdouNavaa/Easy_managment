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
        global warehouses
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        warehouses = connect.cursor()
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))


# Function to fetch warehouses with pagination
def fetch_warehouses(limit=10, offset=0):
    connect_db()
    query = f'''
    SELECT w.id,w.name, w.location,w.description,DATE(w.updated_at),sum(p.quantity)
    FROM warehouses w
    LEFT JOIN products p ON w.id = p.warehouse_id
    GROUP BY w.id
    LIMIT {limit} OFFSET {offset}'''
    my_cursor.execute(query)
    return my_cursor.fetchall()

# fenetere pour ajouter une categorie
def open_add_window(refresh_callback):
    add_window = tk.Toplevel(background='#fff')
    # add_window.pack()
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(add_window,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # name 
    create_label(add_window,"اسم المخزون").pack(ipady=10 ,pady=5, padx=20,fill='x')
    name_entry = create_entry(add_window)

    # desc 
    create_label(add_window,"تفاصيل المخزون").pack(ipady=10 ,pady=5, padx=20,fill='x')
    desc_entry = create_entry(add_window)
    desc_entry.pack(ipady=10 , padx=20,)

    # location 
    create_label(add_window,"مكان المخزون").pack(ipady=10 ,pady=5, padx=20,fill='x')
    location_entry = create_entry(add_window)
    location_entry.pack(ipady=10 , padx=20,)

    
    def add_warehouses():
        name = name_entry.get()
        description = desc_entry.get()
        location = location_entry.get()
        
        # Validation des informations de connexion
        if name == "" or description == "" or location == "" :
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                
                connect_db()
                query = 'insert into warehouses (name,description,location,updated_at) values(%s,%s,%s,%s)'
                my_cursor.execute(query,(name, description,location, datetime.now()))
                connect.commit()
                messagebox.showinfo('نجاح', 'تم اضافة المخزون')
                refresh_callback()
                
                
                result = messagebox.askyesno('تم اضافة المخزون', 'هل تريد الاضافة مرة اخرى?' , parent=add_window)
                if result == True:
                    name_entry.delete(0,tk.END)
                    desc_entry.delete(0, tk.END)
                    location_entry.delete(0, tk.END)
                    # add_window.destroy()
            except Exception as e:
                messagebox.showerror('Error', str(e))
            

    add_button = ctk.CTkButton(
        add_window,
        text="تاكيد",
        width=23,
        command=add_warehouses,font=font_arial_title,corner_radius=2
        
    )
    add_button.pack(pady=(10,30),fill='x',padx=20,ipady=15)
    # ctk.CTkButton(update_window, text="Add", command=save_changes).pack(pady=10)

from tkcalendar import DateEntry
from datetime import datetime
# Fonction pour afficher la fenêtre de mise à jour
def open_update_window(warehouse, update_callback):
    
    update_window = tk.Toplevel(background='#fff')
    # update_window.pack()
    update_window.title("تعديل")

    warehouse=fetch_warehouse(warehouse[0])
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    # direction btn
    btns_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # name 

    create_label(update_window,"اسم المخزون").pack(ipady=10 ,pady=5, padx=20,fill='x')
    name_entry = create_entry(update_window)
    name_entry.insert(0, warehouse[1])  # Pré-remplir avec la valeur actuelle

    # desc 
    create_label(update_window,"تفاصيل المخزون").pack(ipady=10 ,pady=5, padx=20,fill='x')
    desc_entry = create_entry(update_window)
    desc_entry.insert(0, warehouse[3])
    
    # location 
    create_label(update_window,"مكان المخزون").pack(ipady=10 ,pady=5, padx=20,fill='x')
    location_entry = create_entry(update_window)
    location_entry.insert(0, warehouse[2])


    
    # Bouton pour sauvegarder les modifications
    def save_changes():
        name = name_entry.get()
        description = desc_entry.get()
        location = location_entry.get()
        id = warehouse[0]
        
        try:
            connect_db()
            query = 'update warehouses set name=%s, description=%s,location=%s,updated_at=NOW() where id=%s'
            my_cursor.execute(query, (name, description,location, id))
            connect.commit()
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

        messagebox.showinfo('نجاح', 'تم  تعديل المخزون بنجاح')
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(update_window, text=" حفظ التعديل",font=font_arial_title, command=save_changes,corner_radius=2,).pack(fill='x' ,ipady=5, padx=20,pady=(10,30))

def fetch_warehouse(prod_id):
    connect_db()
    query = f'''
    SELECT *
    FROM warehouses  WHERE id = %s'''
    
    ''' '''
    
    my_cursor.execute(query, (prod_id,))
    result = my_cursor.fetchone()
    return result


def delete_warehouse(warehouse_id, update_callback):
    connect_db()
    try:
        print('delete',warehouse_id)
        query = f"DELETE FROM warehouses WHERE id = {warehouse_id}"
        my_cursor.execute(query)
        connect.commit()
        messagebox.showinfo('نجاح', 'تم حذف المخزون بنجاح')
        
        # Appel de la fonction pour actualiser les données
        update_callback()
    except Exception as e:
        messagebox.showerror('Error', str(e))

# Function to show warehouses as a styled table with pagination
def show_warehouses_table(parent, limit=10,is_admin= 0):
    def load_page(page_num):
        nonlocal offset
        offset = (page_num - 1) * limit
        update_table()

    def update_table():
        # Clear previous table data
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Fetch new data
        data = fetch_warehouses(limit, offset)

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
                    # fg_color="#fcfcfc",
                    corner_radius=1,anchor='center',
                )
                label1 = ctk.CTkLabel(
                    data_frame,
                    text=row_index+1,
                    font=font_arial,
                    text_color="#333",
                    # fg_color="#fcfcfc"
                    corner_radius=1,anchor='center',
                )
                label1.grid(row=row_index, column=6 if is_admin == 1 else 5, sticky="nsew", padx=(0,2),ipady=5, pady=1)
                
                label.grid(row=row_index, column=col_index + 1 if is_admin == 1 else col_index, sticky="nsew", padx=2,ipady=5, pady=1)
                
                font_arial_btn = ('Arial',14,'bold')
                buttons_frame = ctk.CTkFrame(data_frame, width=100,height=40,fg_color="#fff",
                                        ) 
                
                buttons_frame.grid(row=row_index , column=0, sticky="nsew", padx=1,ipady=5, pady=3) if is_admin == 1 else buttons_frame.grid_remove()
                
                
                edit_image_path = os.path.join(os.path.dirname(__file__), "images", "edit.png")
                edit_image = ctk.CTkImage(light_image=Image.open(edit_image_path), size=(15, 15),)
                update_button = ctk.CTkButton(buttons_frame, text="",text_color="black",
                        image=edit_image,
                        fg_color='#fff',border_color='#f0f0f0',border_width=1,corner_radius=2,
                        # fg_color='transparent',
                        hover_color='#f0f0f0',
                        width=40,
                        font=font_arial_btn,        
                        command=lambda row=row: open_update_window(row[::-1],update_table)
                        )
                update_button.grid(row=0,column=1) if is_admin == 1 else update_button.grid_remove()
                
                
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
                        command=lambda row=row: delete_warehouse(row[::-1][0], update_table)
                        )
                delete_button.grid(row=0,column=0,padx=5) if is_admin == 1 else delete_button.grid_remove()
                
    
    show_title_frame(parent,update_table)
    offset = 0

    # Table headers 
    columns = (' رقم ', 'اسم المخزن ', 'مكان المخزن', ' تفاصيل المخزن ','آخر تحديث','السعة الحالية')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="#fff",border_width=1,border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    
    
    header_frame.columnconfigure((2,3,4,5), weight=2, uniform='a')if is_admin == 1 else header_frame.columnconfigure(( 1,2,3,4), weight=2, uniform='a')
    header_frame.columnconfigure((0,1,6), weight=1, uniform='a')if is_admin == 1 else header_frame.columnconfigure((0,5), weight=1, uniform='a')
    font_arial = ('Arial',14,'bold')
    
    # header_frame.columnconfigure(2, weight=2)

    # Add column headings
    for col_index, col_name in enumerate(columns):
        label = ctk.CTkLabel(
            header_frame,
            text=col_name,
            font=font_arial,
            text_color="black",
            # fg_color="#fcfcfc",
            corner_radius=1,
            width=100
        )      
        action_lab =ctk.CTkLabel(
            header_frame,
            text='الاجراءات',
            font=font_arial,
            text_color="black",
            corner_radius=1,
            width=100
        )
        action_lab.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)if is_admin == 1 else action_lab.grid_remove()
        label.grid(row=0, column=col_index +1 if is_admin == 1 else col_index, sticky="nsew", padx=5, pady=5)

    # Data frame
    data_frame = ctk.CTkFrame(parent, corner_radius=2,  fg_color="#fff",border_width=1,border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    
    data_frame.columnconfigure((2,3,4,5), weight=2, uniform='a')if is_admin == 1 else data_frame.columnconfigure(( 1,2,3,4), weight=2, uniform='a')
    data_frame.columnconfigure((0,1,6), weight=1, uniform='a')if is_admin == 1 else data_frame.columnconfigure((0,5), weight=1, uniform='a')

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
        text=" المستودعات",
        font=font_arial_title,
        # compound="right"
    )
    title_label.pack(side="right", padx=5, pady=5, ipadx=5, ipady=5)
    
    # add 3 button 
    
    add_image_path = os.path.join(os.path.dirname(__file__), "images", "add.png")
    
    add_image = ctk.CTkImage(light_image=Image.open(add_image_path), size=(15, 15),)
    add_inventory_button = ctk.CTkButton(
        master=title_frame,
        # image=add_image,
        text="اضافة مخزن",
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
        fg_color="#fff",hover=False,
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
def create_entry(parent):
    entry = ctk.CTkEntry(parent, justify=justify,font=("Arial", 14), fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=2, width=400)
    entry.pack(ipady=10 , padx=20)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text)
    label_widgets.append(label)
    return label


# Function to create the warehouses frame
def create_warehouses_frame(root,user=None):
    warehouses_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")
    
    show_warehouses_table(warehouses_frame,is_admin = user[2] if user else 0)
    return warehouses_frame



# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')


# warehouses_frame = create_warehouses_frame(window)
# warehouses_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()