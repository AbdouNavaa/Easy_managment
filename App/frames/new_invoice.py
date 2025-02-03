import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pymysql
import os
from PIL import Image, ImageTk
def connect_db():
    try:
        # create a connection object
        global connect
        global my_cursor
        global products
        global customers
        global warehouses

        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        products = connect.cursor()
        customers = connect.cursor()
        warehouses = connect.cursor()
        
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
        
def fetch_total(table_name,total_variable,myList):
    query = f'SELECT * FROM {table_name}'
    total_variable.execute(query)
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        myList.append(f'{variable[0]}-{variable[1]}')
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    return myList  # Retourner 0 si aucun résultat n'est trouvé   

# import
from tkcalendar import DateEntry
from datetime import datetime 


justify = 'left'
entry_widgets = []  
entry1_widget = []  
label_widgets = []  

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
def update_state():
    for entry in entry_widgets:
        if entry.winfo_exists():
            entry.configure(state=state)

# for entries
state = 'normal'
reference = ''
def create_entry(parent,*args):
    font_arial =("Arial", 14)   
    entry = ctk.CTkEntry(parent, justify=justify,font=font_arial, fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=4,state=state)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text)
    label_widgets.append(label)
    return label

inv_data = []  # Change this to a list instead of a tuple
total_amount = 0
taxe = 15
total_qty = 0
def search_product(id):
    connect = connect_db()
    cursor = connect.cursor()
    
    query = "SELECT * FROM products WHERE id = %s or name = %s OR code = %s"
    cursor.execute(query, (id, id, id))
    
    result = cursor.fetchone()
    if result is None:
        messagebox.showinfo('نجاح', ' المنتج غير موجود في قاعدة البيانات')
        
    cursor.close()
    connect.close()
    
    return result

def search_sale(reference):
    connect = connect_db()
    cursor = connect.cursor()
    
    query = "SELECT id FROM sales WHERE reference_number = %s "
    cursor.execute(query, (reference,))
    
    result = cursor.fetchone()
    if result is None:
        messagebox.showinfo('تنبيه', 'الفاتورة غير موجودة في قاعدة البيانات')
    cursor.close()
    connect.close()
    
    return result

import random
import uuid

def generate_reference():
    reference = str(uuid.uuid4()).upper()[0:4] + str(random.randint(1000, 9999))
    return reference

# Utilisation de la fonction pour générer un numéro de référence
reference = generate_reference()
print(reference)

def change(symbol):
    global change_value
    if symbol == '+' :
        change_value += 1 
    else:
        change_value -= 1 
    update_entry()
def update_entry():
    for entry in entry1_widget:
        if entry.winfo_exists():
            var_change = tk.StringVar(value=change_value) 
            entry.configure(textvariable=var_change)

# for entries
change_value = 0
def create_entry1(parent,wid=200):
    var_change = tk.StringVar(value=change_value) 
    entry = ctk.CTkEntry(parent,font=("Arial", 14), fg_color='#fff', border_width=1,justify='center',
                        border_color='#ddd', corner_radius=1, width=100,textvariable=var_change)
    entry1_widget.append(entry)
    return entry

def create_add_sale_frame(root,user=None,sale=None):
    
    print("Sale Infos:",sale) if sale is not None else None
    
    principal_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd',)
    principal_frame.pack(expand=True,fill='both')
    
    add_sale_frame = ctk.CTkFrame(principal_frame, fg_color='#fff', border_width=1, border_color='#ddd',)
    
    add_prod_sale_frame = ctk.CTkFrame(principal_frame, fg_color='#fff', border_width=1, border_color='#ddd',)
    
    add_prod_sale_frame.pack(ipadx=1,padx=20,pady=20,ipady=10,fill='y',side='right')
    add_sale_frame.pack(padx=(30,20),pady=20,ipady=10,fill='y',side='left')
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(add_sale_frame,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=(20,2))
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # first frame labels
    first_frame = ctk.CTkFrame(add_sale_frame,fg_color='transparent',width=400)
    first_frame.pack(ipady=10 , padx=20,fill='x')
    first_frame.columnconfigure((0,1), weight=1, uniform='equal') 
    
    # first frame entries
    first_frame_entries = ctk.CTkFrame(add_sale_frame,fg_color='transparent',width=400)
    first_frame_entries.pack(ipady=10 , padx=20,fill='x')
    first_frame_entries.columnconfigure((0,1), weight=1, uniform='equal')

    connect_db()
    # customer
    list_of_customers = []
    fetch_total('customers',customers, list_of_customers)
    
    #customer
    customer_label = create_label(first_frame,"العميل")
    customer_label.grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2, )

    customer_entry = ctk.CTkOptionMenu(
        first_frame_entries,values=list_of_customers,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        font=font_arial,
    )
    customer_entry.grid(sticky="news",row = 0, column = 1, ipady=10 , pady=2,padx=(15,0)  )
    
    # date
    date_label = create_label(first_frame,"تاريخ ")
    date_label.grid(sticky="news",row = 0, column = 0, ipady=10 , pady=2, )
    
    date_entry = DateEntry(first_frame_entries, width=30, background='white',font=font_arial,
                                foreground='black', justify='center', date_pattern='yyyy-mm-dd',)
    date_entry.grid(row = 0, column = 0, ipady=10 , pady=2, padx=20, )
    
        
    # second frame  labels
    second_frame = ctk.CTkFrame(add_sale_frame,fg_color='transparent',width=400)
    second_frame.pack(ipady=10 , padx=20,fill='x')
    
    # second frame entries
    second_frame_entry = ctk.CTkFrame(add_sale_frame,fg_color='transparent',width=400)
    second_frame_entry.pack(ipady=10 , padx=20,fill='x')
    

    # status
    create_label(second_frame," الحالة").pack(ipady=10 , fill='x',expand = True,side='right')    
    status_entry = create_entry(second_frame_entry)
    status_entry.pack(ipady=10 , padx=2,fill='x',expand = True,side='right')
    
    # pay method
    create_label(second_frame,"طريقة الدفع").pack(ipady=10 , fill='x',expand = True,side='left')
    
    payment_method_entry = create_entry(second_frame_entry)
    payment_method_entry.pack(ipady=10 , padx=2,fill='x',expand = True,side='left')


    # payment_method and reference_number
    create_label(add_sale_frame,"رقم الفاتورة").pack(ipady=10 , padx=20,fill='x',pady=5)
    

    # Générer un numéro de référence automatiquement
    reference = generate_reference()

    # Insérer le numéro de référence dans l'entrée
    reference_number_entry = create_entry(add_sale_frame)
    reference_number_entry.insert(0, reference)
    reference_number_entry.pack(ipady=10 , fill='x',pady=5,padx=20,)
    
    # note
    create_label(add_sale_frame,"ملاحظات").pack(ipady=10 , padx=20,fill='x',pady=5)
    
    note_entry = create_entry(add_sale_frame)
    note_entry.pack(ipady=10 , fill='x',pady=(5,0),padx=20,)
    
    
    # third frame labels
    third_frame = ctk.CTkFrame(add_prod_sale_frame,fg_color='transparent',width=400)
    third_frame.pack(ipady=10 ,pady=10, padx=20,fill='x')
    
    # third frame entries
    third_frame_entry = ctk.CTkFrame(add_prod_sale_frame,fg_color='transparent',width=400)
    third_frame_entry.pack(ipady=10 , padx=20,fill='x')
    # products
    list_of_products = []
    fetch_total('products',products, list_of_products)
    
    #product
    create_label(third_frame,"المنتجات").pack(ipady=10 , fill='x',expand = True,side='right')

    product_entry = ctk.CTkOptionMenu(
        third_frame_entry,values=list_of_products,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        font=font_arial,
    )
    product_entry.pack(ipady=10 , fill='x',expand = True,side='right')  
    
    # quantity
    create_label(third_frame," الكمية").pack(ipady=10 , fill='x',expand = True,side='left')  
    # quantity_entry = create_entry1(third_frame_entry)
    btn = ctk.CTkButton(third_frame_entry,font=('Ariel',20),text='+',width=45,height=42,corner_radius=1,fg_color='#eee',hover_color='#fff',
    text_color='#333',command=lambda:change('+')).pack(pady=10,padx=(0,10),side='right')
    
    quantity_entry = create_entry1(third_frame_entry)
    quantity_entry.pack(ipady=10,fill = 'x',side='right',anchor='center')
    
    btn = ctk.CTkButton(third_frame_entry,font=('Ariel',20),text='-',width=45,height=42,corner_radius=1,fg_color='#eee',hover_color='#fff',
        text_color='#333',command=lambda:change('-')).pack(pady=10,padx=(10,0),side='right')
    
    def add_product():
        id = product_entry.get().split('-')[0]
        print('ID:',id)
        result = search_product(id)

        if result and float(quantity_entry.get()) > 0:
            global inv_data
            global total_amount
            global total_qty
            print('Result:', result)

            # Extraire les informations nécessaires du produit
            product_code = result[1]  # Supposons que le code produit est à l'index 1
            quantity = float(quantity_entry.get())
            price = float(result[11])  # Supposons que le prix est à l'index 4
            total = quantity * price
            # total_amount += total  

            # Vérifier si le produit existe déjà dans inv_data
            product_exists = False
            for index, item in enumerate(inv_data):
                if item[0] == product_code:  
                    # Si le produit existe, mettre à jour la quantité directement dans la liste
                    existing_quantity = item[1]
                    new_quantity = existing_quantity + quantity
                    inv_data[index] = (item[0], new_quantity, price, new_quantity * price)
                    product_exists = True
                    break

            # Si le produit n'existe pas, l'ajouter comme une nouvelle entrée
            if not product_exists:
                print('Im here',inv_data)
                if isinstance(inv_data, tuple):
                    inv_data = list(inv_data)
                # else:
                inv_data.append((product_code,quantity, price, total))

            # Mettre à jour l'affichage
            update_table()
            quantity_entry.insert(0, '0')
            
            global change_value
            change_value = 0

            
        else:
            messagebox.showinfo('خطا', 'المنتج غير موجود في قاعدة البيانات او الكمية غير صحيحة')
    # btn

    
    add_prod = ctk.CTkButton(
        third_frame_entry,
        text="أضف",
        width=40,
        corner_radius=4,
        fg_color='#333',
        text_color='#fff',hover_color='#000',
        command=add_product
    )
    add_prod.pack(ipady=10,expand = False,side='left')
    
    title_label = ctk.CTkLabel(add_prod_sale_frame, text="المنتجات المضافة", font=('Ariel', 20, 'bold'))
    title_label.pack(pady=10)
    def recalculate_totals():
        global total_amount, total_qty

        # Recalculer le montant total
        total_amount = sum(item[3] for item in inv_data)  # item[3] = total pour chaque ligne
        total_qty = sum(item[1] for item in inv_data)

    global inv_data
    def update_table():
        # Clear previous table data
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Fetch new data
        data = inv_data

        # Ajouter les nouvelles données dans la table
        for row_index, row in enumerate(data):
            row = list(row)  # Convertir le tuple en liste
            row.reverse()  # Inverser les colonnes pour l'affichage
            for col_index, value in enumerate(row):
                label = ctk.CTkLabel(
                    data_frame,
                    text=value,
                    font=('Arial', 12.5),
                    anchor='e',
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                label.grid(row=row_index, column=col_index+1, sticky="nsew", padx=5, pady=1)

            # Ajouter le bouton de suppression
            delete_image_path = os.path.join(os.path.dirname(__file__), "images", "delete_invoice.png")
            delete_image = ctk.CTkImage(light_image=Image.open(delete_image_path), size=(23, 23),)
            delete_button = ctk.CTkButton(data_frame,
                text="",
                text_color="black",
                image=delete_image,
                fg_color='#fff',
                # bg_color='#fff',
                hover_color='#eee',
                width=20,
                font=('Arial',15),
                command=lambda row=row: delete_item(row[::-1]),
            )
            delete_button.grid(row=row_index, column=0, padx=5, pady=1)
            
            def delete_item(row):
                global inv_data

                inv_data = [item for item in inv_data if item[0] != row[0]]
                messagebox.showinfo("نجاح", "تم الحذف بنجاح")
                print('INv:',inv_data)
        
                # update the table
                
                update_table()

        # Recalculer et mettre à jour les totaux
        recalculate_totals()
        update_totals_display()
    columns = ('المنتج', 'الكمية', 'السعر', 'المجموع','حذف')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(add_prod_sale_frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((0, 1, 2, 3,4), weight=1, uniform='a')
    font_arial = ('Arial', 14, 'bold')

    # Add column headings
    for col_index, col_name in enumerate(columns):
        label = ctk.CTkLabel(
            header_frame,
            text=col_name,
            font=font_arial,
            anchor='e',
            text_color="black",
            fg_color="#fff",
            corner_radius=5,
            width=100
        )
        label.grid(row=0, column=col_index, sticky="nsew", padx=5, pady=5)

    # Data frame
    data_frame = ctk.CTkFrame(add_prod_sale_frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure((0, 1, 2, 3,4), weight=1, uniform='a')
    
    total_frame = ctk.CTkFrame(add_prod_sale_frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    total_frame.pack(fill='x', padx=20, pady=5)
    
    def update_totals_display():
        # Mettre à jour les valeurs affichées pour les totaux
        for widget in total_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(total_frame, text=round(total_amount, 2), font=('Arial', 15, 'bold')).pack(side='left', expand=True)
        ctk.CTkLabel(total_frame, text=": المجموع", font=('Arial', 15, 'bold')).pack(side='left', padx=20, pady=5)

        ctk.CTkLabel(total_frame, text=": الكمية", font=('Arial', 15, 'bold')).pack(side='right', padx=20, pady=5)
        ctk.CTkLabel(total_frame, text=round(total_qty, 2), font=('Arial', 15, 'bold')).pack(side='right', expand=True)

    def add_invoice():
        global inv_data
        if not inv_data:
            messagebox.showerror("Error", "No products added yet.")
            return
    
        try:
            connection = connect_db()
            with connection.cursor() as cursor:
                for item in inv_data:
                    prod = search_product(item[0])
                    sale = search_sale(reference)
                    print("Product founded:", prod)
                    id = prod[0]
                    query = "INSERT INTO sale_items (sale_id, product_id, quantity, subtotal) VALUES ( %s, %s, %s, %s)"
                    cursor.execute(query, (sale, id, item[1], item[3]))
                    
                    # Mettre à jour la quantité du produit
                    query = "UPDATE products SET quantity = quantity - %s WHERE id = %s"
                    cursor.execute(query, (item[1], id)) 
                connection.commit()
            messagebox.showinfo('نجاح', 'تمت اضافة المنتجات بنجاح')
            inv_data = []
            global state
            
            state = 'normal'
            update_state()
            update_table()
        
        except pymysql.Error as e:
            connection.rollback()
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
        finally:
            if connection:
                connection.close()
    add_button = ctk.CTkButton(
        add_prod_sale_frame,
        text="تاكيد",
        width=400,font=font_arial_title,
        corner_radius=4,
        command=add_invoice
    )
    add_button.pack(pady=(5,10), ipady=10, padx=20, fill='x') 

    # update the
    update_table()

    

    def add_sales():
        customer = customer_entry.get()[0]
        date = date_entry.get_date().strftime('%Y-%m-%d') if date_entry.get_date() else None
        # total_amount = float(total_amount_entry.get())
        # discount = float(discount_entry.get())
        # final_amount = ((total_amount) + ( total_amount*discount*0.01))
        status = status_entry.get()
        payment_method = payment_method_entry.get()
        reference_number = reference_number_entry.get()
        note = note_entry.get()
        
        
        # Validation des informations de connexion
        if payment_method == "" or status == "" or note == ""  or  reference_number == '':
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                connect_db()
                query = '''INSERT INTO sales (date, customer_id,  status, payment_method, reference_number, notes,
                created_by,created_at,completed_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,Now(),Now())'''
                values = (date, customer,  status, payment_method, reference_number, note, 1)
                my_cursor.execute(query,values)
                connect.commit()
                messagebox.showinfo('نجاح', 'تمت اضافة الفاتورة بنجاح')
                                
                result = messagebox.askyesno('تم الاضافة', 'هل تريد اضافة فاتورة جديد?' , parent=add_sale_frame)
                if result == True:
                    status_entry.delete(0,tk.END)
                    payment_method_entry.delete(0,tk.END)
                    global reference
                    reference = reference_number
                    reference_number_entry.delete(0,tk.END)
                    note_entry.delete(0,tk.END)
                    global state
                    print('Reference number:', reference)
                    state = 'disabled'
                    update_state()
                
            except Exception as e:
                messagebox.showerror('Error', str(e))
            
    add_button = ctk.CTkButton(
        add_sale_frame,
        text="إضافة",
        width=400,
        font=font_arial_title,
        corner_radius=4,
        command=add_sales
            )
    add_button.pack(pady=15,ipady=10,padx=20,fill='x')
    
    
    
    return principal_frame
# # window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# add_sale_frame = create_add_sale_frame(window)
# # add_sale_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()