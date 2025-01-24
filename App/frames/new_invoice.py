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
        global customers
        global warehouses

        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        categories = connect.cursor()
        customers = connect.cursor()
        warehouses = connect.cursor()
        
        # messagebox.showinfo('Connection Successful', 'Connected to the database')
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

from invoice_details_frame import frame_principal

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
    entry = ctk.CTkEntry(parent, justify=justify,font=font_arial, fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=4)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text)
    label_widgets.append(label)
    return label

def create_add_sale_frame(root,sale=None):
    
    print("Sale:",sale) if sale is not None else None
    add_sale_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    add_sale_frame.pack(padx=400,pady=10,ipady=10,)
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(add_sale_frame,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
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
    status_entry.insert(0, sale[6]) if sale is not None else None 
    status_entry.pack(ipady=10 , padx=2,fill='x',expand = True,side='right')
    
    # pay method
    create_label(second_frame,"طريقة الدفع").pack(ipady=10 , fill='x',expand = True,side='left')
    
    payment_method_entry = create_entry(second_frame_entry)
    payment_method_entry.insert(0, sale[7]) if sale is not None else None 
    payment_method_entry.pack(ipady=10 , padx=2,fill='x',expand = True,side='left')


    # payment_method and reference_number
    create_label(add_sale_frame,"رقم الفاتورة").pack(ipady=10 , padx=20,fill='x',pady=5)
    
    reference_number_entry = create_entry(add_sale_frame)
    reference_number_entry.insert(0, sale[8]) if sale is not None else None 
    reference_number_entry.pack(ipady=10 , fill='x',pady=5,padx=20,)
    
    # note
    create_label(add_sale_frame,"ملاحظات").pack(ipady=10 , padx=20,fill='x',pady=5)
    
    note_entry = create_entry(add_sale_frame)
    note_entry.insert(0, sale[9]) if sale is not None else None 
    note_entry.pack(ipady=10 , fill='x',pady=(5,0),padx=20,)
    
    
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
                if sale is None:
                    query = '''INSERT INTO sales (date, customer_id,  status, payment_method, reference_number, notes,
                    created_by,created_at,completed_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,Now(),Now())'''
                    values = (date, customer,  status, payment_method, reference_number, note, 1)
                    my_cursor.execute(query,values)
                    connect.commit()
                    messagebox.showinfo('Success', 'Sale added successfully')
                else:
                    query = '''UPDATE sales SET date=%s, customer_id=%s, status=%s, payment_method=%s, reference_number=%s, notes=%s
                    WHERE id=%s'''
                    values = (date, customer,  status, payment_method, reference_number, note, sale[0])
                    my_cursor.execute(query,values)
                    connect.commit()
                    messagebox.showinfo('Success', 'Sale updated successfully')
                
                result = messagebox.askyesno('Sale added successfully', 'do you want to clean the form?' , parent=add_sale_frame)
                if result == True and sale is None:
                    connect_db()
                    query = "SELECT id FROM sales ORDER BY id DESC LIMIT 1"
                    my_cursor.execute(query)
                    sale_id = my_cursor.fetchone()
                    print('Sale Id:', sale_id)
                    # je veux aller au frame_principal
                    add_sale_frame.destroy()
                    sales_frame = frame_principal(root,sale_id) 
                    sales_frame.pack(fill='both', expand=True)   
                else:
                    back_to_invoices(root)  
            except Exception as e:
                messagebox.showerror('Error', str(e))
            
        
    def back_to_invoices(root):
        add_sale_frame.pack_forget()  # Cache le frame actuel
        from invoices_frame import create_sales_frame  # Import ici pour éviter les dépendances circulaires
        invoices_frame = create_sales_frame(root) 
        
        invoices_frame.pack(fill="both", expand=True)  # Affiche la page des factures

    add_button = ctk.CTkButton(
        add_sale_frame,
        text="تاكيد",
        width=400,
        corner_radius=4,
        command=add_sales
            )
    add_button.pack(pady=5,ipady=10,padx=20,fill='x')
    
    
    
    return add_sale_frame

# # window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# add_sale_frame = create_add_sale_frame(window)
# add_sale_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()