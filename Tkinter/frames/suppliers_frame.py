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
def show_suppliers_table(parent, limit=10):
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
                label1.grid(row=row_index, column=6, sticky="nsew", padx=5, pady=5)

                label.grid(row=row_index, column=col_index+1, sticky="e", padx=5, pady=5)
                
                font_arial_btn = ('Arial',14,'bold')
                buttons_frame = ctk.CTkFrame(data_frame, width=100,height=40,fg_color="transparent",
                                        ) 
                
                buttons_frame.grid(row=row_index , column=0, sticky="nsew", padx=5, pady=5)
                
                
                edit_image_path = os.path.join(os.path.dirname(__file__), "images", "pen.png")
                edit_image = ctk.CTkImage(light_image=Image.open(edit_image_path), size=(35, 35),)
                update_button = ctk.CTkButton(buttons_frame, text="",text_color="black",
                        image=edit_image,
                        fg_color='#fff',
                        hover_color='#f0f0f0',
                        width=50,
                        font=font_arial_btn,        
                        command=lambda row=row: open_update_window(row[::-1],update_table)
                        )
                update_button.grid(row=0,column=1)
                
                
                delete_image_path = os.path.join(os.path.dirname(__file__), "images", "delete.png")
                delete_image = ctk.CTkImage(light_image=Image.open(delete_image_path), size=(35, 35),)
                delete_button = ctk.CTkButton(buttons_frame,
                        text="",
                        text_color="black",
                        image=delete_image,
                        fg_color='transparent',
                        hover_color='#fbfafa',
                        font=font_arial_btn, 
                        width=50,
                        command=lambda row=row: delete_supplier(row[::-1][0], update_table)
                        )
                delete_button.grid(row=0,column=0,padx=5)
                
    show_title_frame(parent,update_table)

    offset = 0

    # Table headers
    columns = ("رقم",'اسم المورد ', 'الشخص المسؤول ', 'رقم الهاتف', 'البريد الالكتروني',"العنوان", "الاجراءات")
    # columns = ('القطعة رقم ', 'الاسم ', 'الوصف', 'المنتجات عدد',  'الإجراءات')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="#fff",border_width=1,border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((0, 1, 2,3, 4, 5,6), weight=1, uniform='a')
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
        label.grid(row=0, column=col_index, sticky="e", padx=5, pady=5)

    # Data frame
    data_frame = ctk.CTkFrame(parent, corner_radius=2,  fg_color="#fff",border_width=1,border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure((0, 1,2, 3, 4, 5,6), weight=1, uniform='a')
    # data_frame.columnconfigure(2, weight=2, uniform='a')

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

def open_add_window(refresh_callback):
    update_window = tk.Toplevel(background='#fff')
    # update_window.pack()
    update_window.title("اضافة مورد جديد")

    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)   
    global justify 
    justify = 'left' 

# direction btn
    btns_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Fr')).pack(pady=10,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Ar')).pack(pady=10,padx=(155,5),side='right')

#name
    name_label = create_label(update_window,"اسم المورد",400)
    name_label.pack(ipady=10, pady=5, padx=20)
    
    name_entry = create_entry(update_window)
    name_entry.pack(ipady=10, padx=20)

    
#phone
    phone_label = create_label(update_window,"رقم الهاتف",400)
    phone_label.pack(ipady=10, pady=5, padx=20)
    
    phone_entry = create_entry(update_window)
    phone_entry.pack(ipady=10 , padx=20)
    
    
#email
    email_label = create_label(update_window,"البريد الالكتروني",400)
    email_label.pack(ipady=10, pady=5, padx=20)
    
    email_entry = ctk.CTkEntry(update_window, font=font_arial,
    fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,width=400)
    email_entry.pack(ipady=10 , padx=20)
    
#address
    address_label = create_label(update_window,"العنوان",400)
    address_label.pack(ipady=10, pady=5, padx=20)
    
    address_entry = create_entry(update_window)
    address_entry.pack(ipady=10 , padx=20)
    
# labels frame
    labs_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    labs_frame.pack( ipady=10 , padx=20, pady=2)
    
# entries frame
    entries_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    entries_frame.pack( ipady=10 , padx=20, pady=2)
    
# credit limit
    credit_label = create_label(labs_frame,"الحد",200)
    credit_label.pack(ipady=10 ,pady=5, padx=(0,2),side='right')
    
    credit_limit = ctk.CTkEntry(entries_frame, font=font_arial, 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=200)
    credit_limit.pack(ipady=10 , padx=2,side='right')
    
# account_id 
    connect_db()
    list_of_suppliers = []
    fetch_drop(suppliers, list_of_suppliers)

    account_label = create_label(labs_frame,"الحساب",200)
    account_label.pack(ipady=10,pady=5 , padx=(2,0),side='left')

    account_id = ctk.CTkOptionMenu(
        entries_frame,values=list_of_suppliers,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        width=200,
        font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
    )
    account_id.pack(ipady=10 , padx=2,side='left')
# Bouton pour sauvegarder les modifications
    def save_changes():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()
        credit = credit_limit.get()
        account = account_id.get()[0]        
        
        try:
            connect_db()
        
            query = 'insert into suppliers (name,phone,email,address,credit_limit,account_id) values(%s,%s,%s,%s,%s,%s)'
            my_cursor.execute(query,(name,phone,email,address,credit,account))
            connect.commit()
            messagebox.showinfo('Success', 'supplier added successfully')
            refresh_callback()
            
            result = messagebox.askyesno('supplier added successfully', 'do you want to clean the form?' , parent=update_window)
            if result == True:
                name_entry.delete(0,tk.END)
                phone_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                address_entry.delete(0, tk.END) 
                credit_limit.delete(0, tk.END)
                # update_window.destroy()  # Fermer la fenêtre de mise à jour
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

    ctk.CTkButton(update_window, text=" حفظ", command=save_changes).pack(pady=10,padx=20,fill='x',ipady=5)

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
    entry = ctk.CTkEntry(parent, justify=justify,font=font_arial, fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=8, width=400)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text,wid):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text, width=wid)
    label_widgets.append(label)
    return label
# Fonction pour afficher la fenêtre de mise à jour
def open_update_window(supplier, update_callback):
    global entry_widgets
    entry_widgets = []  # Reset the list for each new window
    
    update_window = tk.Toplevel(background='#fff')
    # update_window.pack()
    update_window.title("تعديل المورد")

    supp=fetch_supplier(supplier[0])
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)   
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#eee',text_color='black',command=lambda:direction('Fr')).pack(pady=10,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#eee',text_color='black',command=lambda:direction('Ar')).pack(pady=10,padx=(155,5),side='right')

    #name
    name_label = create_label(update_window,"اسم المورد",400)
    name_label.pack(ipady=10, pady=5, padx=20)
    
    name_entry = create_entry(update_window)
    name_entry.insert(0,supplier[1])
    name_entry.pack(ipady=10, padx=20)

    
    #phone
    phone_label = create_label(update_window,"رقم الهاتف",400)
    phone_label.pack(ipady=10, pady=5, padx=20)
    
    phone_entry = create_entry(update_window)
    phone_entry.insert(0,supplier[3])
    phone_entry.pack(ipady=10 , padx=20)
    
    
    #email
    email_label = create_label(update_window,"البريد الالكتروني",400)
    email_label.pack(ipady=10, pady=5, padx=20)
    
    email_entry = ctk.CTkEntry(update_window, font=font_arial, 
    fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,width=400)
    email_entry.insert(0,supplier[4])
    email_entry.pack(ipady=10 , padx=20)
    
    #address
    address_label = create_label(update_window,"العنوان",400)
    address_label.pack(ipady=10, pady=5, padx=20)
    
    address_entry = create_entry(update_window, )
    address_entry.insert(0, supplier[5])
    address_entry.pack(ipady=10 , padx=20)
    
    # labels frame
    labs_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    labs_frame.pack( ipady=10 , padx=20, pady=2)
    
    # entries frame
    entries_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    entries_frame.pack( ipady=10 , padx=20, pady=2)
    # credit limit
    credit_label = create_label(labs_frame,"الحد",200)
    credit_label.pack(ipady=10 ,pady=5, padx=(0,2),side='right')
    
    credit_limit = ctk.CTkEntry(entries_frame, font=font_arial, 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=200)
    credit_limit.insert(0, supplier[5])
    credit_limit.pack(ipady=10 , padx=2,side='right')
    # account_id 
    # category
    connect_db()
    list_of_suppliers = []
    fetch_drop(suppliers, list_of_suppliers)
    
    credit_label = create_label(labs_frame,"الحساب",200)
    credit_label.pack(ipady=10,pady=5 , padx=(2,0),side='left')
    
    account_default =f'numebe:{supp[8]}' if supp[8] else 'NULL'

    # Créez une variable Tkinter StringVar
    account = tk.StringVar(value=account_default)
    account_id = ctk.CTkOptionMenu(
        entries_frame,values=list_of_suppliers,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        width=200,
        font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        variable=account,
    )
    account_id.pack(ipady=10 , padx=2,side='left')

    # Bouton pour sauvegarder les modifications
    def save_changes():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()
        credit = credit_limit.get()
        account = account_id.get()[0]
        
        id = supplier[0]
        
        try:
            connect_db()
            query = 'update suppliers set name=%s,phone=%s,email=%s,address=%s, credit_limit=%s,account_id=%s where id=%s'
            my_cursor.execute(query,(name,phone,email,address,credit_limit,account,id))
            connect.commit()
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

        messagebox.showinfo("Success", "supplier updated successfully!")
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(update_window, text=" حفظ", command=save_changes).pack(pady=10,padx=20,ipady=5,fill='x',expand=True)
def fetch_supplier(supplier_id):
    connect_db()
    query = f'''
    SELECT *
    FROM suppliers  WHERE id = %s'''
    
    my_cursor.execute(query, (supplier_id,))
    result = my_cursor.fetchone()
    return result
def fetch_drop(total_variable,myList):
    query = f'SELECT * FROM accounts'
    total_variable.execute(query)
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        myList.append(f'{variable[0]}-{variable[1]}')
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    return myList  # Retourner 0 si aucun résultat n'est trouvé   


def delete_supplier(supplier_id, update_callback):
    connect_db()
    try:
        query = f"DELETE FROM suppliers WHERE id = {supplier_id}"
        my_cursor.execute(query)
        connect.commit()
        messagebox.showinfo('Success', 'supplier deleted successfully')
        
        # Appel de la fonction pour actualiser les données
        update_callback()
    except Exception as e:
        messagebox.showerror('Error', str(e))


def show_title_frame(parent,refresh_callback ):
    
    # Table headers

    # Header frame
    title_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="transparent",)
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
        fg_color="#f9fbfb",
        hover_color="#f0f0f0",
        font=('Arial',14,),
        text_color="#333",
        corner_radius=5,
        command=refresh_callback
    )
    # add button 
    add_image_path = os.path.join(os.path.dirname(__file__), "images", "add.png")
    add_image = ctk.CTkImage(light_image=Image.open(add_image_path), size=(15, 15),)
    
    add_inventory_button = ctk.CTkButton(
        master=title_frame,
        image=add_image,
        text="اضافة مورد جديد",
        font=('Arial',14,),
        fg_color="#f9fbfb",
        text_color="#333",
        hover_color="#f0f0f0",
        corner_radius=5,
        command=lambda: open_add_window(refresh_callback)
    )
    add_inventory_button.pack(side="left", pady=5,)
    refresh_button.pack(side="left",padx=5, pady=5)    


# Function to create the suppliers frame
def create_suppliers_frame(root):
    suppliers_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")


    show_suppliers_table(suppliers_frame)
    return suppliers_frame

# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')


# suppliers_frame = create_suppliers_frame(window)
# suppliers_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()