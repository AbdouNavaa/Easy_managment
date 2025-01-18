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
        print('Connected to the database')
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
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # name 
    create_label(add_window,"اسم العميل").pack(ipady=10 ,pady=5, padx=20,fill='x')
    name_entry = create_entry(add_window)

    # phone 
    create_label(add_window,"هاتف العميل").pack(ipady=10 ,pady=5, padx=20,fill='x')
    phone_entry = create_entry(add_window)

    
    # email 
    create_label(add_window,"البريد الالكتروني").pack(ipady=10 ,pady=5, padx=20,fill='x')
    email_entry = ctk.CTkEntry(add_window,font=font_arial, fg_color='#fff', 
            border_width=1, border_color='#ddd', corner_radius=8, width=400)
    email_entry.pack(ipady=10 , padx=20)
    
    # address 
    create_label(add_window,"العنوان").pack(ipady=10 ,pady=5, padx=20,fill='x')
    address_entry = create_entry(add_window)
    
    # labels frame
    labels_frame = ctk.CTkFrame(add_window,fg_color='transparent',)
    labels_frame.pack( ipady=10 , padx=20, pady=2)
    
    # entries frame
    entries_frame = ctk.CTkFrame(add_window,fg_color='transparent',width=400)
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
                refresh_callback()
                
                
                result = messagebox.askyesno('Customer added successfully', 'do you want to clean the form?' , parent=add_window)
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
            # print(user)
            

    add_button = ctk.CTkButton(
        add_window,
        text="تاكيد",
        width=400,
        command=add_customers
            )
    add_button.pack(pady=10,padx=20,ipady=10)
    # ctk.CTkButton(update_window, text="Add", command=save_changes).pack(pady=10)

# Fonction pour afficher la fenêtre de mise à jour
def open_update_window(customer, update_callback):
    
    update_window = tk.Toplevel(background='#fff')
    # update_window.pack()
    update_window.title("تعديل")

    print("customer", customer)
    custom=fetch_customer(customer[0])
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    # direction btn
    btns_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # name 
    create_label(update_window,"اسم العميل").pack(ipady=10 ,pady=5, padx=20,fill='x')
    name_entry = create_entry(update_window)
    name_entry.insert(0, custom[1])  # Pré-remplir avec la valeur actuelle

    # phone 
    create_label(update_window,"هاتف العميل").pack(ipady=10 ,pady=5, padx=20,fill='x')
    phone_entry = create_entry(update_window)
    phone_entry.insert(0, custom[2])

    
    # email 
    create_label(update_window,"البريد الالكتروني").pack(ipady=10 ,pady=5, padx=20,fill='x')
    email_entry = ctk.CTkEntry(update_window,font=font_arial, fg_color='#fff', 
            border_width=1, border_color='#ddd', corner_radius=8, width=400)
    email_entry.insert(0, custom[3])  # Pré-remplir avec la valeur actuelle
    email_entry.pack(ipady=10 , padx=20)
    
    # address 
    create_label(update_window,"العنوان").pack(ipady=10 ,pady=5, padx=20,fill='x')
    address_entry = create_entry(update_window)
    address_entry.insert(0, custom[4])  # Pré-remplir avec la valeur actuelle
    
    # labels frame
    labels_frame = ctk.CTkFrame(update_window,fg_color='transparent',)
    labels_frame.pack( ipady=10 , padx=20, pady=2)
    
    # entries frame
    entries_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    entries_frame.pack( ipady=10 , padx=20, pady=2)
    # balance
    create_label(labels_frame,"الرصيد").pack(ipady=10 ,pady=5, fill='x',side='right')
    balance_entry = create_entry(entries_frame,200)
    balance_entry.insert(0, custom[6] if custom[6] else 'NULL')
    balance_entry.pack(ipady=10 , padx=20,side='right')

    
    # is_active 
    create_label(labels_frame,"الحالة").pack(ipady=10 ,pady=5, fill='x',side='left')
    is_active = ['0-غير مفعل','1-مفعل']
    default_value = is_active[1] if custom[7] == 1 else is_active[0]
    print('default_value', default_value)
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
        
        try:
            connect_db()
            query = '''UPDATE `customers` SET `name`=%s, `phone`=%s, `email`=%s, `address`=%s, `balance`=%s, `is_active`=%s WHERE `id`=%s'''
            my_cursor.execute(query, (name, phone, email, address, balance, is_active, id))
            connect.commit()
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

        messagebox.showinfo("Success", "customer updated successfully!")
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(update_window, text=" حفظ التعديل",font=font_arial_title, command=save_changes,width=400).pack(ipady=5, padx=20,pady=10,)

def fetch_drop(total_variable,myList):
    query = f'SELECT * FROM customers'
    total_variable.execute(query)
    # print('ffdfd:', total_variable.fetchall())
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        print(variable[1])
        myList.append(f'{variable[0]}-{variable[1]}')
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    print(myList)
    return myList  # Retourner 0 si aucun résultat n'est trouvé   

def fetch_customer(prod_id):
    connect_db()
    query = f'''
    SELECT *
    FROM customers  WHERE id = %s'''
    
    ''' '''
    
    my_cursor.execute(query, (prod_id,))
    result = my_cursor.fetchone()
    # print('Categ with Id', result)
    return result


def delete_customer(customer_id, update_callback):
    print('CatId', customer_id)
    connect_db()
    try:
        query = f"DELETE FROM customers WHERE id = {customer_id}"
        my_cursor.execute(query)
        connect.commit()
        messagebox.showinfo('Success', 'Customer deleted successfully')
        
        # Appel de la fonction pour actualiser les données
        update_callback()
    except Exception as e:
        messagebox.showerror('Error', str(e))

# Function to show customers as a styled table with pagination
def show_customers_table(parent, limit=10):
    def load_page(page_num):
        nonlocal offset
        print(page_num)
        offset = (page_num - 1) * limit
        print(offset)
        update_table()

    def update_table():
        # Clear previous table data
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Fetch new data
        print("Offest: ",offset)
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
                    font=font_arial,anchor='center',
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                label1.grid(row=row_index, column=5, sticky="nsew", padx=5, pady=1)

                label.grid(row=row_index, column=col_index+1, sticky="nsew", padx=5, pady=1)
                
                font_arial_btn = ('Arial',14,'bold')
                buttons_frame = ctk.CTkFrame(data_frame, height=40,fg_color="#fcfcfc",
                                        ) 
                
                buttons_frame.grid(row=row_index , column=0, sticky="nsew", padx=(5,0), pady=5)
                
                
                edit_image_path = os.path.join(os.path.dirname(__file__), "images", "edit.png")
                edit_image = ctk.CTkImage(light_image=Image.open(edit_image_path), size=(17, 17),)
                update_button = ctk.CTkButton(buttons_frame, text="",text_color="black",
                        image=edit_image,
                        fg_color='#05f100',
                        hover_color='#0f9',
                        width=30,
                        font=font_arial_btn,        
                        command=lambda row=row: open_update_window(row[::-1],update_table)
                        )
                update_button.pack(side="right", padx=5, pady=5)
                
                
                delete_image_path = os.path.join(os.path.dirname(__file__), "images", "delete.png")
                delete_image = ctk.CTkImage(light_image=Image.open(delete_image_path), size=(23, 23),)
                delete_button = ctk.CTkButton(buttons_frame,
                        text="",
                        text_color="black",
                        image=delete_image,
                        fg_color='#f50',
                        hover_color='#f50',
                        font=font_arial_btn, 
                        width=30,
                        command=lambda row=row: delete_customer(row[::-1][0], update_table)
                        )
                delete_button.pack(side="right", padx=5, pady=5,after=update_button)
                
    
    show_title_frame(parent,update_table)
    offset = 0

    # Table headers
    columns = (' رقم ', 'الاسم ', 'الهاتف','البريد الالكتروني', 'العنوان ','الاجراءات')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="#fff",border_width=1,border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure(( 3, 4), weight=2, uniform='a')
    header_frame.columnconfigure((1,2), weight=3, uniform='a')  
    header_frame.columnconfigure((0,5), weight=1, uniform='a')  
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
        label.grid(row=0, column=col_index, sticky="nsew", padx=5, pady=5)

    # Data frame
    data_frame = ctk.CTkFrame(parent, corner_radius=2,  fg_color="#fff",border_width=1,border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure(( 3, 4), weight=2, uniform='a')
    data_frame.columnconfigure((1,2), weight=3, uniform='a')  
    data_frame.columnconfigure((0,5), weight=1, uniform='a')  


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
        text="فائمة العملاء ",
        font=font_arial_title,
        # compound="right"
    )
    title_label.pack(side="right", padx=5, pady=5, ipadx=5, ipady=5)
    
    # add 3 button 
    
    add_image_path = os.path.join(os.path.dirname(__file__), "images", "add.png")
    
    add_image = ctk.CTkImage(light_image=Image.open(add_image_path), size=(15, 15),)
    add_inventory_button = ctk.CTkButton(
        master=title_frame,
        image=add_image,
        text=" اضافة عميل ",
        font=font_arial,
        width=40,
        text_color="#333",
        fg_color="#fcfcfc",
        hover_color="#f0f0f0",
        corner_radius=5,
        # border_color="#f0f0f0",
        command=lambda: open_add_window(refresh_callback)
    )
    add_inventory_button.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5)

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


# Function to create the customers frame
def create_customers_frame(root):
    customers_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")


    show_customers_table(customers_frame)
    return customers_frame



# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')


# customers_frame = create_customers_frame(window)
# customers_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()