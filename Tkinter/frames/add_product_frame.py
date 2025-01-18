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
        global suppliers
        global warehouses

        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        categories = connect.cursor()
        suppliers = connect.cursor()
        warehouses = connect.cursor()
        
        # messagebox.showinfo('Connection Successful', 'Connected to the database')
        print('Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
        
def fetch_total(table_name,total_variable,myList):
    query = f'SELECT * FROM {table_name}'
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

# import
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
    font_arial =("Arial", 14)   
    entry = ctk.CTkEntry(parent, justify=justify,font=font_arial, fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=8, width=400)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text)
    label_widgets.append(label)
    return label

def create_add_product_frame(root):
    container = ctk.CTkFrame(root, fg_color="#fff")
    container.pack(fill='both', expand=True)

    # Create canvas for scrolling
    canvas = tk.Canvas(container, bg="#fff", highlightthickness=0,width=800, height=930)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    title_frame = ctk.CTkFrame(canvas, fg_color="#fff", border_color='#ddd')
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="#fff",border_width=1, border_color='#ddd')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # canvas.create_window((0, 0), window=title_frame,anchor="s", width=799,height=60)
    # canvas.create_window((1, 1), window=scrollable_frame,anchor="n", width=799)
    canvas.create_window((1, 1), window=scrollable_frame, width=799)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True,padx=500,pady=10,ipady=100)
    scrollbar.pack(side="right", fill="y")

    # Champ de nom d'utilisateur
    # Titre de la page
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 12)

    scrollable_frame.columnconfigure((0,1,2), weight=1, uniform='a')

    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(scrollable_frame,fg_color='transparent',width=400)
    btns_frame.grid(padx=5,row = 0, column=0, columnspan=3, ipady=4, pady=2,  sticky="news")
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Fr')).pack(padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Ar')).pack(padx=(155,5),side='right')
    #name
    name_label = create_label(scrollable_frame,"اسم المنتج")
    name_label.grid(padx=5,row = 1, column=0, columnspan=3, ipady=10, pady=2,  sticky="news")
    
    name_entry = create_entry(scrollable_frame)
    name_entry.grid(row = 2, column=0, columnspan=3, ipady=10, pady=2, padx=20, sticky="news")

    #desc
    desc_label = create_label(scrollable_frame,"وصف المنتج")
    desc_label.grid(padx=5,row = 3, column=0, columnspan=3, ipady=10, pady=2,  sticky="news")
    
    desc_entry = create_entry(scrollable_frame)
    desc_entry.grid(row = 4, column=0, columnspan=3, ipady=10, pady=2, padx=20, sticky="news")


    #price
    price_label = create_label(scrollable_frame,"السعر ")
    price_label.grid(sticky="news",row = 5, column = 2, ipady=10 , pady=2, )
    price_entry = create_entry(scrollable_frame)
    
    price_entry.grid(row = 6, column = 2, ipady=10 , pady=2, padx=20, )

    #before_price
    before_price_label = create_label(scrollable_frame,"سعر الشراء ")
    before_price_label.grid(sticky="news",row = 5, column = 1, ipady=10 , pady=2, )
    
    before_price_entry = create_entry(scrollable_frame)
    before_price_entry.grid(row = 6, column = 1, ipady=10 , pady=2, padx=20, )
    
    # selling price
    selling_price_label = create_label(scrollable_frame," سعر البيع ")
    selling_price_label.grid(sticky="news",row = 5, column = 0, ipady=10 , pady=2, )
    
    selling_price_entry = create_entry(scrollable_frame)
    selling_price_entry.grid(row = 6, column = 0, ipady=10 , pady=2, padx=20, ) 

    # category
    connect_db()
    list_of_categories = []
    fetch_total('product_categories',categories, list_of_categories)

    category_label = create_label(scrollable_frame,"القسم ")
    category_label.grid(sticky="news",row = 7, column = 2, ipady=10 , pady=2, )
    
    category_entry = ctk.CTkOptionMenu(
        scrollable_frame,values=list_of_categories,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',

    )
    category_entry.grid(row = 8, column = 2, ipady=10 , pady=2, padx=20, )
    
    
    # supplier
    list_of_suppliers = []
    fetch_total('suppliers',suppliers, list_of_suppliers)
    
    #supplier
    supplier_label = create_label(scrollable_frame,"المورد ")
    supplier_label.grid(sticky="news",row = 7, column = 1, ipady=10 , pady=2, )

    supplier_entry = ctk.CTkOptionMenu(
        scrollable_frame,values=list_of_suppliers,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        font=font_arial,
    )
    supplier_entry.grid(row = 8, column = 1, ipady=10 , pady=2, padx=20, )
    
    
    # warehouse
    list_of_warehouses = []
    fetch_total('warehouses',warehouses, list_of_warehouses)

    warehouse_label = create_label(scrollable_frame,"المخزن ")
    warehouse_label.grid(sticky="news",row = 7, column = 0, ipady=10 , pady=2, )

    warehouse_entry = ctk.CTkOptionMenu(
        scrollable_frame,values=list_of_warehouses,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        font=font_arial,
    )
    warehouse_entry.grid(row = 8, column = 0, ipady=10 , pady=2, padx=20, )

    # Create the DateEntry widget
    created_at_label = create_label(scrollable_frame,"تاريخ التسجيل")
    created_at_label.grid(sticky="news",row = 9, column = 2, ipady=10 , pady=2, )
    
    created_at_entry = DateEntry(scrollable_frame, width=30, background='white',font=font_arial,
                                foreground='black', justify='center', date_pattern='yyyy-mm-dd',)
    created_at_entry.grid(row = 10, column = 2, ipady=10 , pady=2, padx=20, )
    
    # code
    code_label = create_label(scrollable_frame,"الكود ")
    code_label.grid(sticky="news",row = 9, column = 0, ipady=10 , pady=2, )
    
    code_entry = create_entry(scrollable_frame)
    code_entry.grid(row = 10, column = 0, ipady=10 , pady=2, padx=20, )
    
    # unit
    unit_label = create_label(scrollable_frame,"الوحدة ")
    unit_label.grid(sticky="news",row = 9, column = 1, ipady=10 , pady=2, )
    
    unit_entry = create_entry(scrollable_frame)
    unit_entry.grid(row = 10, column = 1, ipady=10 , pady=2, padx=20, )
    
    # qty
    qty_label = create_label(scrollable_frame,"الكمية ")
    qty_label.grid(sticky="news",row = 11, column = 2, ipady=10 , pady=2, )
    
    qty_entry = create_entry(scrollable_frame)
    qty_entry.grid(row = 12, column = 2, ipady=10 , pady=2, padx=20, )
    
    # min quantity
    min_qty_label = create_label(scrollable_frame,"الحد الادنى")
    min_qty_label.grid(sticky="news",row = 11, column = 1, ipady=10 , pady=2, )
    
    min_qty_entry = create_entry(scrollable_frame)
    min_qty_entry.grid(row = 12, column = 1, ipady=10 , pady=2, padx=20, )
    
    # status
    active_label = create_label(scrollable_frame,"الحالة ")
    active_label.grid(sticky="news",row = 11, column = 0, ipady=10 , pady=2, )
    
    active_entry = create_entry(scrollable_frame)    
    active_entry.grid(row = 12, column = 0, ipady=10 , pady=2, padx=20, )


    def add_products():
        name = name_entry.get()
        description = desc_entry.get()
        price = float(price_entry.get())
        purchase_price = float(before_price_entry.get())
        category = category_entry.get()[0]
        supplier = supplier_entry.get()[0]
        warehouse = warehouse_entry.get()[0]
        code = code_entry.get()
        unit = unit_entry.get()
        selling_price = float(selling_price_entry.get())
        min_qty = float(min_qty_entry.get())
        active = int(active_entry.get())
        created_at = created_at_entry.get_date().strftime('%Y-%m-%d') if created_at_entry.get_date() else None
        quantity = qty_entry.get()
        
        # Validation des informations de connexion
        if name == "" or description == "" or price == "" or purchase_price == "" or  quantity == '' or min_qty == '':
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                
                connect_db()
                query = '''insert into products (id,name,description,price,purchase_price,category_id,supplier_id,warehouse_id,code,selling_price,
                quantity,min_quantity,is_active,created_at) values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())'''
                my_cursor.execute(query,(name,description,price,purchase_price,category,supplier,warehouse,code,selling_price,quantity,min_qty,active))
                connect.commit()
                messagebox.showinfo('Success', 'Product added successfully')
                
                
                result = messagebox.askyesno('Product added successfully', 'do you want to clean the form?' , parent=add_product_frame)
                if result == True:
                    name_entry.delete(0,tk.END)
                    desc_entry.delete(0,tk.END)
                    price_entry.delete(0,tk.END)
                    before_price_entry.delete(0,tk.END)
                    # category_entry.delete(0,tk.END) 
                    # supplier_entry.delete(0,tk.END)
                    # warehouse_entry.delete(0,tk.END)
                    code_entry.delete(0,tk.END)
                    # unit_entry.delete(0,tk.END)
                    selling_price_entry.delete(0,tk.END)
                    qty_entry.delete(0,tk.END)
                    min_qty_entry.delete(0,tk.END)
                    active_entry.delete(0,tk.END)
                    created_at_entry.set_date(None)
                    # root.destroy()
                    # import products_frame
            except Exception as e:
                messagebox.showerror('Error', str(e))
            # print(user)
    
    # ctk.CTkButton(scrollable_frame, text="حفظ", command=save_changes,).grid(row=12, column=0, columnspan=3, ipady=10, pady=(20,10), padx=20, sticky="news")       

    add_button = ctk.CTkButton(
        scrollable_frame,
        font=font_arial_title,text="تاكيد",
        width=23,
        command=add_products
        
    ).grid(row=13, column=0, columnspan=3, ipady=10, pady=(10,5), padx=20, sticky="news")

    return container

# # window 
window = ctk.CTk(fg_color="#fff")
window.title('customtkinter app')
window.geometry('1200x550')
window.state('zoomed')

add_product_frame = create_add_product_frame(window)
add_product_frame.pack(fill='both', expand=True)

# run
window.mainloop()