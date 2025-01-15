import customtkinter as ctk
from tkinter import messagebox
import pymysql
import tkinter as tk


# Connection settings
def connect_db():
    try:
        global connect
        global my_cursor
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='sms')
        my_cursor = connect.cursor()
        print('Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))


# Function to fetch suppliers with pagination
def fetch_suppliers(limit=10, offset=0):
    connect_db()
    query = f'SELECT * FROM supplier LIMIT {limit} OFFSET {offset}'
    my_cursor.execute(query)
    return my_cursor.fetchall()


# Function to show suppliers as a styled table with pagination
def show_suppliers_table(parent, limit=10):
    def load_page(page_num):
        nonlocal offset
        print('PageNum',page_num)
        offset = (page_num - 1) * limit
        print(offset)
        update_table()

    def update_table():
        # Clear previous table data
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Fetch new data
        print("Offest: ",offset)
        data = fetch_suppliers(limit, offset)

        # Add data rows
        for row_index, row in enumerate(data):
            row = row[::-1]  # Reverse the row data
            for col_index, value in enumerate(row):
                # print("val:",col_index,value)
                label = ctk.CTkLabel(
                    data_frame,
                    text=value,
                    font=ctk.CTkFont(size=12),
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                label1 = ctk.CTkLabel(
                    data_frame,
                    text=row_index+1,
                    font=ctk.CTkFont(size=12),
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                
                buttons_frame = ctk.CTkFrame(data_frame, width=100,height=40,fg_color="transparent",
                                        # command=lambda row=row: show_supplier_details(row)
                                        ) 
                buttons_frame.grid(row=row_index , column=0, sticky="nsew", padx=5, pady=5)
                update_button = ctk.CTkButton(buttons_frame, text="تعديل",fg_color="#0f7",font=ctk.CTkFont(size=12),
                        width=75,text_color='#000',
                        command=lambda row=row: open_update_window(row[::-1],update_table)
                        )
                update_button.grid(row=0,column=1)
                delete_button = ctk.CTkButton(buttons_frame, text="حذف",fg_color="#f03",font=ctk.CTkFont(size=12),width=75,
                        command=lambda row=row: delete_supplier(row[::-1][0], update_table)
                        )
                delete_button.grid(row=0,column=0,padx=5)
                
                label1.grid(row=row_index, column=6, sticky="nsew", padx=5, pady=5)
                label.grid(row=row_index, column=col_index +1, sticky="nsew", padx=5, pady=5)
                
    show_title_frame(parent,update_table)

    offset = 0

    # Table headers
    columns = ("رقم",'المورد اسم ', 'المسؤول الشخص ', 'الهاتف رقم', 'الالكتروني البريد',"العنوان", "الاجراءات")
    # columns = ('القطعة رقم ', 'الاسم ', 'الوصف', 'المنتجات عدد',  'الإجراءات')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="#333")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((0, 1, 2,3, 4, 5,6), weight=1, uniform='a')
    # header_frame.columnconfigure(2, weight=2)

    # Add column headings
    for col_index, col_name in enumerate(columns):
        label = ctk.CTkLabel(
            header_frame,
            text=col_name,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="white",
            fg_color="#444",
            corner_radius=5,
            width=100
        )
        label.grid(row=0, column=col_index, sticky="nsew", padx=5, pady=5)

    # Data frame
    data_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="#f9f9f9")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure((0, 1,2, 3, 4, 5,6), weight=1, uniform='a')
    # data_frame.columnconfigure(2, weight=2, uniform='a')

    # Pagination controls
    nav_frame = ctk.CTkFrame(parent, fg_color="#fff")
    nav_frame.pack(fill='x', pady=10)

    prev_button = ctk.CTkButton(
        nav_frame,
        text="السابق",
        command=lambda: load_page(max(1, (offset // limit))),
        # state="normal" if offset > 0 else "disabled"
    )
    prev_button.pack(side="left", padx=10)

    next_button = ctk.CTkButton(
        nav_frame,
        text="التالي",
        command=lambda: load_page((offset // limit) + 2)
    )
    next_button.pack(side="right", padx=10)

    update_table()

def open_add_window(refresh_callback):
    update_window = ctk.CTkToplevel(fg_color='#fff')
    # update_window.pack()
    update_window.title("اضافة مورد جديد")
    # Champ pour le nom du produit
    ctk.CTkLabel(update_window,anchor='e', text="المورد اسم").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    name_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    name_entry.pack(ipady=10 , padx=20)


    # 1
    ctk.CTkLabel(update_window,anchor='e', text="المسؤول الشخص").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    responsable_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    responsable_entry.pack(ipady=10 , padx=20)
    
    # 2
    ctk.CTkLabel(update_window,anchor='e', text="الهاتف رقم").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    phone_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
    fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    phone_entry.pack(ipady=10 , padx=20)
    
    
    # 3
    ctk.CTkLabel(update_window,anchor='e', text="البريد الالكتروني").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    email_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
    fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    email_entry.pack(ipady=10 , padx=20)
    
    # 4
    ctk.CTkLabel(update_window,anchor='e', text="العنوان").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    address_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    address_entry.pack(ipady=10 , padx=20)
    # Bouton pour sauvegarder les modifications
    def save_changes():
        new_name = name_entry.get()
        new_phone = phone_entry.get()
        new_email = email_entry.get()
        new_responsable = responsable_entry.get()
        new_address = address_entry.get()
        
        s_name = new_name
        s_phone = new_phone
        s_email = new_email
        s_responsable = new_responsable
        s_address = new_address
        
        try:
            connect_db()
        
            query = 'insert into supplier values(null,%s,%s,%s,%s,%s)'
            my_cursor.execute(query,(s_name,s_responsable,s_phone,s_email,s_address))
            connect.commit()
            messagebox.showinfo('Success', 'supplier added successfully')
            refresh_callback()
            
            result = messagebox.askyesno('supplier added successfully', 'do you want to clean the form?' , parent=update_window)
            if result == True:
                name_entry.delete(0,tk.END)
                phone_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                responsable_entry.delete(0, tk.END)
                address_entry.delete(0, tk.END) 
                update_window.destroy()  # Fermer la fenêtre de mise à jour
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

        # messagebox.showinfo("Success", "supplier updated successfully!")
        # update_window.destroy()  # Fermer la fenêtre de mise à jour
        # update_callback()

    ctk.CTkButton(update_window, text="Add", command=save_changes).pack(pady=10)

# Fonction pour afficher la fenêtre de mise à jour
def open_update_window(supplier, update_callback):
    update_window = ctk.CTkToplevel(fg_color='#fff')
    # update_window.pack()
    update_window.title("Update supplier")

    print("supplier", supplier)
    # Champ pour le nom du produit
    ctk.CTkLabel(update_window,anchor='e', text="المورد اسم").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    name_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    name_entry.insert(0, supplier[1])  # Pré-remplir avec la valeur actuelle
    name_entry.pack(ipady=10 , padx=20)

    # 1
    ctk.CTkLabel(update_window,anchor='e', text="المسؤول الشخص").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    responsable_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    responsable_entry.insert(0, supplier[2])  # Pré-remplir avec la valeur actuelle
    responsable_entry.pack(ipady=10 , padx=20)
    
    # 2
    ctk.CTkLabel(update_window,anchor='e', text="الهاتف رقم").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    phone_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
    fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    phone_entry.insert(0, supplier[3])  # Pré-remplir avec la valeur actuelle
    phone_entry.pack(ipady=10 , padx=20)
    
    
    # 3
    ctk.CTkLabel(update_window,anchor='e', text="البريد الالكتروني").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    email_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
    fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    email_entry.insert(0,supplier[4])
    email_entry.pack(ipady=10 , padx=20)
    
    # 4
    ctk.CTkLabel(update_window,anchor='e', text="العنوان").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    address_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    address_entry.insert(0, supplier[5])
    address_entry.pack(ipady=10 , padx=20)

    # Bouton pour sauvegarder les modifications
    def save_changes():
        new_name = name_entry.get()
        new_responsable = responsable_entry.get()
        new_phone = phone_entry.get()
        new_email = email_entry.get()
        new_address = address_entry.get()
        
        s_id = supplier[0]
        s_name = new_name
        s_responsable = new_responsable
        s_phone = new_phone
        s_email = new_email
        s_address = new_address
        
        try:
            connect_db()
            query = 'update supplier set name=%s,responsable_name=%s,phone=%s,email=%s,address=%s where s_id=%s'
            my_cursor.execute(query,(s_name,s_responsable,s_phone,s_email,s_address,s_id))
            connect.commit()
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

        messagebox.showinfo("Success", "supplier updated successfully!")
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(update_window, text="Save Changes", command=save_changes).pack(pady=10)


def delete_supplier(supplier_id, update_callback):
    print('SupId', supplier_id)
    connect_db()
    try:
        query = f"DELETE FROM supplier WHERE s_id = {supplier_id}"
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
    title_frame.pack(fill='x', padx=20, pady=5,)
    title_frame.columnconfigure((0, 1, 2,3, 4, 5, 6), weight=1, uniform='a',)
    
    title_label = ctk.CTkLabel(
        master=title_frame,
        text="الموردين قائمة",
        font=ctk.CTkFont(size=20, weight="bold"),
        # text_color="#0066cc"
        compound="right"
    )
    title_label.grid(row=0, column=5,columnspan=3, padx=5, pady=5,sticky="e")
    
    # add 3 button 
    add_inventory_button = ctk.CTkButton(
        master=title_frame,
        text="جديد مورد اضافة",
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color="#2498f5",
        text_color="#333",
        hover_color="#f0f0f0",
        corner_radius=5,
        command=lambda: open_add_window(refresh_callback)
    )
    add_inventory_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)

    # button de refresh
    # refresh_button = ctk.CTkButton(
    #     master=title_frame,
    #     text="  تحديث  ",
    #     font=ctk.CTkFont(size=12, weight="bold"),
    #     fg_color="#2498f5",
    #     text_color="#333",
    #     hover_color="#f0f0f0",
    #     corner_radius=5,
    #     # command=lambda: refresh_table(parent)
    #     command=refresh_callback
    # )
    # refresh_button.grid(row=0, column=1, sticky="e", padx=5, pady=5)
    
    

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