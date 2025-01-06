import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pymysql
def connect_db():
    try:
        # create a connection object
        global connect
        global my_cursor
        global suppliers

        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='sms')
        my_cursor = connect.cursor()
        suppliers = connect.cursor()
        
        # messagebox.showinfo('Connection Successful', 'Connected to the database')
        print('Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
        
def fetch_total(total_variable,myList):
    query = f'SELECT * FROM supplier'
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
    
    add_product_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    add_product_frame.pack(padx=400,pady=10,ipady=100)
    
    # info colored labelframe style
    # ctk.CTkLabelframe(add_product_frame,bootstyle="info").pack()

    # Champ de nom d'utilisateur
    # Titre de la page
    
    title_label = ctk.CTkLabel(
        add_product_frame, text="منتج إضافة",  bg_color="#fff",  font=('book antiqua', 20, 'bold'),anchor='center'
    )
    title_label.pack(fill='x', padx=20,pady=(10,1))

    product_name_label = ctk.CTkLabel(
        add_product_frame, text=" المنتج اسم",bg_color='white',anchor='e'
    )
    product_name_label.pack(fill='x', padx=20,)
    
    # name_placeholder = tk.StringVar(value='اسم المنتج')
    product_name_entry = ctk.CTkEntry(
        add_product_frame, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right'
    )
    product_name_entry.pack(fill='x',ipady=10 ,pady=10, padx=20,)

    # Champ de mot de passe
    description_label = ctk.CTkLabel(
        add_product_frame, text=" المنتج وصف  ", bg_color="white",anchor='e'
    )
    description_label.pack(fill='x', padx=20,)
    description_entry = ctk.CTkEntry(
        add_product_frame, font=("times new roman", 14), width=30,
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right'  
    )
    description_entry.pack(fill='x',ipady=10 ,pady=10, padx=20,)

    # Champ de mot de Price
    price_label = ctk.CTkLabel(
        add_product_frame, text=" السعر", bg_color="white",anchor='e'
    )
    price_label.pack(fill='x', padx=20,)
    price_entry = ctk.CTkEntry(
        add_product_frame, font=("times new roman", 14), width=30,
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right'  
    )
    price_entry.pack(fill='x',ipady=10 ,pady=10, padx=20, )


    # Champ de price2
    price1_label = ctk.CTkLabel(
        add_product_frame, text="الشراء سعر  ", bg_color="white",anchor='e'
    )
    price1_label.pack(fill='x', padx=20,)
    price1_entry = ctk.CTkEntry(
        add_product_frame, font=("times new roman", 14), width=30,
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right'  
    )
    price1_entry.pack(fill='x',ipady=10 ,pady=10, padx=20,)
    
    
    # Champ de Supplier
    supplier_label = ctk.CTkLabel(
        add_product_frame, text="المورد", bg_color="white",anchor='e'
    )
    supplier_label.pack(fill='x', padx=20,)
    connect_db()
    myList = []
    fetch_total(suppliers, myList)
    # optionmenu_var = ctk.StringVar(value="موردا اختر")
    supplier_entry = ctk.CTkOptionMenu(
        add_product_frame,values=myList,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
        #  variable=optionmenu_var
    )
    
    
    # optionmenu = ctk.CTkOptionMenu(search_frame,values=["الاقسام كل","option 1", "option 2"],text_color="#333",dropdown_fg_color="#fff",
    #                     button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",
    #                     # command=optionmenu_callback,
    #                     variable=optionmenu_var)
    supplier_entry.pack(fill='x',ipady=10 ,pady=10, padx=20,)
    

    
    
    # quantity
    quantity_label = ctk.CTkLabel(
        add_product_frame, text="الكمية", bg_color="white",anchor='e'
    )
    quantity_label.pack(fill='x', padx=20,) 
    quantity_entry = ctk.CTkEntry(
        add_product_frame, font=("times new roman", 14), width=30,
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right'  
    )
    quantity_entry.pack(fill='x',ipady=10 ,pady=(10,1), padx=20,)
    
    # Bouton de connexion

    def add_products():
        product_name = product_name_entry.get()
        product_description = description_entry.get()
        product_price = price_entry.get()
        price_before = price1_entry.get()
        supplier = supplier_entry.get()[0]
        quantity = quantity_entry.get()
        
        # Validation des informations de connexion
        if product_name == "" or product_description == "" or product_price == "" or price_before == "" or supplier == "" or quantity == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                
                connect_db()
                query = 'insert into product values(null,%s,%s,%s,%s,%s,%s)'
                my_cursor.execute(query,(product_name,product_description,product_price,price_before,supplier,quantity))
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
        add_product_frame,
        text="تاكيد",
        width=23,
        command=add_products
        
    )
    add_button.pack(pady=10,fill='x',padx=20,ipady=10)
    
    
    
    return add_product_frame


# # window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# add_product_frame = create_add_product_frame(window)
# add_product_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()