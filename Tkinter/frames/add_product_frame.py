import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedTk
import pymysql
import ttkbootstrap as  ttk

# functions

def connect_db():
    try:
        # create a connection object
        global connect
        global my_cursor
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='sms')
        my_cursor = connect.cursor()
        # messagebox.showinfo('Connection Successful', 'Connected to the database')
        print('Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
        

# import 
def create_add_product_frame(root):
    
    
    style = ttk.Style()
    style.configure(
        "AddProd.TFrame",
        background="#fff",  # Couleur de fond
        borderwidth=1,
        relief="ridge"  ,# Type de bordure (flat, solid, ridge, etc.)
        
    )
    
    add_product_frame = ttk.Frame(root, style="AddProd.TFrame", padding=20,)
    add_product_frame.pack(padx=600,pady=10,fill='y',ipady=100,)
    
    # info colored labelframe style
    # ttk.Labelframe(add_product_frame,bootstyle="info").pack()

    # Champ de nom d'utilisateur
    # Titre de la page
    title_label = ttk.Label(
        add_product_frame, text="منتج إضافة",  background="#fff", foreground="#333", font=('book antiqua', 20, 'bold'),anchor='center'
    )
    title_label.pack(fill='x', padx=620,)

    product_name_label = ttk.Label(
        add_product_frame, text="اسم المنتج",background='white',anchor='e'
    )
    product_name_label.pack(fill='x', padx=620,)
    
    name_placeholder = tk.StringVar(value='Name')
    product_name_entry = ttk.Entry(
        add_product_frame, font=("times new roman", 14), width=30, textvariable=name_placeholder,
    )
    product_name_entry.pack(fill='x',ipady=10 ,pady=10, padx=620,)

    # Champ de mot de passe
    description_label = ttk.Label(
        add_product_frame, text="وصف المنتج", background="white",anchor='e'
    )
    description_label.pack(fill='x', padx=620,)
    description_entry = ttk.Entry(
        add_product_frame, font=("times new roman", 14), width=30,  
    )
    description_entry.pack(fill='x',ipady=10 ,pady=10, padx=620,)

# Champ de mot de Price
    price_label = ttk.Label(
        add_product_frame, text=" السعر", background="white",anchor='e'
    )
    price_label.pack(fill='x', padx=620,)
    price_entry = ttk.Entry(
        add_product_frame, font=("times new roman", 14), width=30,  
    )
    price_entry.pack(fill='x',ipady=10 ,pady=10, padx=620,)


    # Champ de price2
    price1_label = ttk.Label(
        add_product_frame, text=" سعر الشراء", background="white",anchor='e'
    )
    price1_label.pack(fill='x', padx=620,)
    price1_entry = ttk.Entry(
        add_product_frame, font=("times new roman", 14), width=30,  
    )
    price1_entry.pack(fill='x',ipady=10 ,pady=10, padx=620,)
    
    
# Champ de Supplier
    supplier_label = ttk.Label(
        add_product_frame, text="المورد", background="white",anchor='e'
    )
    supplier_label.pack(fill='x', padx=620,)
    supplier_entry = ttk.Entry(
        add_product_frame, font=("times new roman", 14), width=30,  
    )
    supplier_entry.pack(fill='x',ipady=10 ,pady=10, padx=620,)
    

    
    
# quantity
    quantity_label = ttk.Label(
        add_product_frame, text="الكمية", background="white",anchor='e'
    )
    quantity_label.pack(fill='x', padx=620,) 
    quantity_entry = ttk.Entry(
        add_product_frame, font=("times new roman", 14), width=30,  
    )
    quantity_entry.pack(fill='x',ipady=10 ,pady=10, padx=620,)
    
    # Bouton de connexion

    def add_products():
        product_name = product_name_entry.get()
        product_description = description_entry.get()
        product_price = price_entry.get()
        price_before = price1_entry.get()
        supplier = supplier_entry.get()
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
                    product_name_entry.delete(0, END)
                    description_entry.delete(0, END)
                    price_entry.delete(0, END)
                    price1_entry.delete(0, END)
                    supplier_entry.delete(0, END)
                    quantity_entry.delete(0, END)
            except Exception as e:
                messagebox.showerror('Error', str(e))
            # print(user)
            
        if user == 1 :  # Exemple simple
            messagebox.showinfo("Login Successful", f"Welcome! {username}")
            main_window.destroy()
            # Créer une nouvelle fenêtre avec des widgets supplémentaires
            import home
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    b_style = ttk.Style()
    b_style.configure(
        "button.TButton",
        background="#000",  # Couleur de fond
        # bgcolor="#000",
        borderwidth=1,
        relief="ridge"  ,# Type de bordure (flat, solid, ridge, etc.)
        
    )
    add_button = ttk.Button(
        add_product_frame,
        text="تاكيد",
        bootstyle="success",
        # style="button.TButton",
        # font=("Helvetica", 14, "bold"),
        # bg="#001",
        # fg="white",anchor='center',
        # activebackground="white",
        # activeforeground="black",
        # cursor="hand2",
        # padding=10,
        width=23,
        command=add_products
        
    )
    add_button.pack(pady=20,fill='x',padx=620,ipady=10)
    
    
    
    return add_product_frame


# Fenêtre principale
# root =ttk.Window()
# root.title("Add Product")
# root.state("zoomed")

# # Création du cadre Home
# add_product_frame = create_add_product_frame(root)
# add_product_frame.pack(fill="x")

# root.mainloop()