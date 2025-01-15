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

    canvas.create_window((0, 0), window=title_frame,anchor="s", width=799,height=60)
    canvas.create_window((1, 1), window=scrollable_frame,anchor="n", width=799)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True,padx=500,pady=10,ipady=100)
    scrollbar.pack(side="right", fill="y")

    # Champ de nom d'utilisateur
    # Titre de la page
    font_arial = ('Arial', 15, 'bold')
    font_arial_title = ('Arial', 20, 'bold')
    title_label = ctk.CTkLabel(
        title_frame, text="إضافة منتج",  text_color="#000",  font=font_arial_title,anchor='center'
    )
    title_label.pack(fill='x', padx=20,pady=(10,1))

    scrollable_frame.columnconfigure((0,1,2), weight=1, uniform='a')
    # Champ pour le nom du produit
    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": اسم المنتج").grid(row = 0, column = 2, ipady=10 , pady=(10,2), padx=10,)
    name_entry = ctk.CTkEntry(scrollable_frame, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    name_entry.grid(row = 0, column = 0, ipady=10 ,pady=(10,2), padx=20,columnspan=2)

    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": وصف المنتج").grid(row = 1, column = 2, ipady=10 , pady=2, padx=10,)
    desc_entry = ctk.CTkEntry(scrollable_frame, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    desc_entry.grid(row = 1, column = 0, ipady=10 , pady=2, padx=20, columnspan=2)

    # Champ pour le prix du produit
    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=" : السعر").grid(row = 2, column = 2, ipady=10 , pady=2, padx=20,)
    price_entry = ctk.CTkEntry(scrollable_frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    price_entry.grid(row = 3, column = 2, ipady=10 , pady=2, padx=20, )

    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": سعر الشراء ").grid(row = 2, column = 1, ipady=10 , pady=2, padx=20,)
    before_price_entry = ctk.CTkEntry(scrollable_frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    before_price_entry.grid(row = 3, column = 1, ipady=10 , pady=2, padx=20, )
    
    # selling price
    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=" : سعر البيع  ").grid(row = 2, column = 0, ipady=10 , pady=2, padx=20,)
    selling_price_entry = ctk.CTkEntry(scrollable_frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    selling_price_entry.grid(row = 3, column = 0, ipady=10 , pady=2, padx=20, )    
    # category
    connect_db()
    list_of_categories = []
    fetch_total('product_categories',categories, list_of_categories)

    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": القسم",).grid(row = 4, column = 2, ipady=10 , pady=2, padx=20,)

    category_entry = ctk.CTkOptionMenu(
        scrollable_frame,values=list_of_categories,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
    )
    category_entry.grid(row = 5, column = 2, ipady=10 , pady=2, padx=20, )
    
    
    # supplier
    list_of_suppliers = []
    fetch_total('suppliers',suppliers, list_of_suppliers)
    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": المورد ",).grid(row = 4, column = 1, ipady=10 , pady=2, padx=20,)

    # Créez une variable Tkinter StringVar
    supplier_entry = ctk.CTkOptionMenu(
        scrollable_frame,values=list_of_suppliers,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',

    )
    supplier_entry.grid(row = 5, column = 1, ipady=10 , pady=2, padx=20, )
    
    
    # warehouse
    list_of_warehouses = []
    fetch_total('warehouses',warehouses, list_of_warehouses)
    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": المخزن ").grid(row = 4, column = 0, ipady=10 , pady=2, padx=20,)

    warehouse_entry = ctk.CTkOptionMenu(
        scrollable_frame,values=list_of_warehouses,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
    )
    warehouse_entry.grid(row = 5, column = 0, ipady=10 , pady=2, padx=20, )
    # created at
    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": تاريخ التسجيل  ").grid(row = 6, column = 2, ipady=10 , pady=2, padx=20,)
    created_at_entry = ctk.CTkEntry(scrollable_frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    created_at_entry.grid(row = 7, column = 1, ipady=10 , pady=2, padx=20, columnspan=2)
    
    # code
    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": الكود ").grid(row = 6, column = 0, ipady=10 , pady=2, padx=20,)
    code_entry = ctk.CTkEntry(scrollable_frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    code_entry.grid(row = 7, column = 0, ipady=10 , pady=2, padx=20, )
    
    # unit
    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": الوحدة ").grid(row = 8, column = 0, ipady=10 , pady=2, padx=20,)
    unit_entry = ctk.CTkEntry(scrollable_frame,font=("times new roman", 14),   
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    unit_entry.grid(row = 9, column = 0, ipady=10 , pady=2, padx=20, )
    

    
    # quantity

    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": الكمية ").grid(row = 8, column = 2, ipady=10 , pady=2, padx=20,)
    qty_entry = ctk.CTkEntry(scrollable_frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    qty_entry.grid(row = 9, column = 1, ipady=10 , pady=2, padx=20, columnspan=2)
    
    # min quantity
    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": الحد الادنى").grid(row = 10, column = 2, ipady=10 , pady=2, padx=20,)
    min_qty_entry = ctk.CTkEntry(scrollable_frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    min_qty_entry.grid(row = 11, column = 1, ipady=10 , pady=2, padx=20, columnspan=2)
    
    # active
    ctk.CTkLabel(scrollable_frame,anchor='e', font=font_arial,text=": الحالة ").grid(row = 10, column = 0, ipady=10 , pady=2, padx=20,)
    active_entry = ctk.CTkEntry(scrollable_frame,font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400) 
    active_entry.grid(row = 11, column = 0, ipady=10 , pady=2, padx=20, )
    

    
    # Bouton de connexion

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
        created_at = created_at_entry.get()
        quantity = qty_entry.get()
        
        # Validation des informations de connexion
        if name == "" or description == "" or price == "" or purchase_price == "" or  quantity == '' or min_qty == '':
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                
                connect_db()
                query = 'insert into products (id,name,description,price,purchase_price,category_id,supplier_id,created_at,warehouse_id,code,selling_price,quantity,min_quantity,is_active) values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                my_cursor.execute(query,(name,description,price,purchase_price,category,supplier,created_at,warehouse,code,selling_price,quantity,min_qty,active))
                connect.commit()
                messagebox.showinfo('Success', 'Product added successfully')
                
                
                result = messagebox.askyesno('Product added successfully', 'do you want to clean the form?' , parent=add_product_frame)
                if result == True:
                    product_name_entry.delete(0,tk.END)
                    description_entry.delete(0,tk.END)
                    price_entry.delete(0,tk.END)
                    price1_entry.delete(0,tk.END)
                    # supplier_entry.delete(0,tk.END)
                    quantity_entry.delete(0,tk.END)
                    # root.destroy()
                    # import products_frame
            except Exception as e:
                messagebox.showerror('Error', str(e))
            # print(user)
            

    add_button = ctk.CTkButton(
        scrollable_frame,
        font=font_arial,text="تاكيد",
        width=23,
        command=add_products
        
    ).grid(row=14, column=0, columnspan=3, ipady=10, pady=10, padx=20, sticky="news")

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