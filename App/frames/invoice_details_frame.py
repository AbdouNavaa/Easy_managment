import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox,ttk
import pymysql
from PIL import Image, ImageTk
import os

# create a database connection
def connect_db():
    try:
        global connect
        global my_cursor
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
        
# first frame
def show_details_frame(root,sale_id,details):
    title_frame = ctk.CTkFrame(root, corner_radius=1, fg_color="#fff", border_width=1, border_color="#f0f0f0", width=400)

    title_label = ctk.CTkLabel(title_frame, text="المنتجات المضافة", font=('Ariel', 20, 'bold'))
    title_label.pack(pady=10)
    def recalculate_totals():
        global total_amount, final_total

        # Recalculer le montant total
        total_amount = sum(item[3] for item in inv_data)  # item[3] = total pour chaque ligne

        # Calculer le total final en incluant les taxes
        final_total = total_amount + (total_amount * taxe * 0.01)


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
                if not inv_data:
                    messagebox.showerror("Error", "No products added yet.")
                    return
                try:
                    connection = connect_db()
                    with connection.cursor() as cursor:
                            
                        prod = search_product(row[0])
                        print("Product founded:", prod)
                        id = prod[0]
                        query = "delete from sale_items where product_id= %s"
                        cursor.execute(query, (id))
                        
                        connection.commit()
                    
                    messagebox.showinfo("Success", "تم الحذف")
                    # je veux remove le row dans le list inv_data
                    inv_data = [item for item in inv_data if item[0] != row[0]]
                    print('INv:',inv_data)
            
                    # update the table
                    
                    update_table()
                    print('Inv Data:', inv_data)
                
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

        # Recalculer et mettre à jour les totaux
        recalculate_totals()
        update_totals_display()
    columns = ('المنتج', 'الكمية', 'السعر', 'المجموع','حذف')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(title_frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
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
    data_frame = ctk.CTkFrame(title_frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure((0, 1, 2, 3,4), weight=1, uniform='a')
    
    total_frame = ctk.CTkFrame(title_frame, corner_radius=2, fg_color="#fff", border_width=1, border_color="#f0f0f0")
    total_frame.pack(fill='x', padx=20, pady=(5,20))
    
    def update_totals_display():
        # Mettre à jour les valeurs affichées pour les totaux
        for widget in total_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(total_frame, text=": المجموع", font=('Arial', 15, 'bold')).pack(side='right', padx=20, pady=5)
        ctk.CTkLabel(total_frame, text=round(total_amount, 2), font=('Arial', 15, 'bold')).pack(side='right', padx=(0, 130))

        ctk.CTkLabel(total_frame, text=": الضريبة", font=('Arial', 15, 'bold')).pack(side='right', padx=20, pady=5)
        ctk.CTkLabel(total_frame, text=f"{taxe}%", font=('Arial', 15, 'bold')).pack(side='right', padx=(0, 130))

        ctk.CTkLabel(total_frame, text=": الاجمالي", font=('Arial', 15, 'bold')).pack(side='right', padx=20, pady=5)
        ctk.CTkLabel(total_frame, text=round(final_total, 2), font=('Arial', 15, 'bold')).pack(side='right', padx=(0, 130))

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
                    print("Product founded:", prod)
                    id = prod[0]
                    query = "INSERT INTO sale_items (sale_id, product_id, quantity, discount, subtotal) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query, (sale_id, id, item[1], taxe, item[3]))
                
                connection.commit()
            
            messagebox.showinfo("Success", "The items were successfully added")
            inv_data = []
            update_table()
            print('Inv Data:', inv_data)
        
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
        title_frame,
        text="تاكيد",
        width=400,
        corner_radius=4,
        command=add_invoice
    )
    add_button.pack(pady=(5, 20), ipady=10, padx=20, fill='x') if details == False else add_button.pack_forget()

    # update the
    update_table()
    return title_frame, update_table

inv_data = []  # Change this to a list instead of a tuple
total_amount = 0
taxe = 15
final_total = 0
def search_product(name_or_code):
    connect = connect_db()
    cursor = connect.cursor()
    
    query = "SELECT * FROM products WHERE name = %s OR code = %s"
    cursor.execute(query, (name_or_code, name_or_code))
    
    result = cursor.fetchone()
    if result is None:
        messagebox.showinfo("Product Not Found", "The product was not found in the database.")
        
    cursor.close()
    connect.close()
    
    return result


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
def change(symbol):
    global change_value
    if symbol == '+' :
        change_value += 1 
    else:
        change_value -= 1 
    update_entry()
def update_entry():
    for entry in entry_widgets:
        if entry.winfo_exists():
            var_change = tk.StringVar(value=change_value) 
            entry.configure(textvariable=var_change)

# for entries
change_value = 0
def create_entry1(parent,wid=200):
    var_change = tk.StringVar(value=change_value) 
    entry = ctk.CTkEntry(parent,font=("Arial", 14), fg_color='#fff', border_width=1,justify='center',
                        border_color='#ddd', corner_radius=1, width=300,textvariable=var_change)
    entry_widgets.append(entry)
    return entry

def create_label(parent,text,*args):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='e', text=text)
    label_widgets.append(label)
    return label

def add_frame(root, update_table):
    add_prod_frame = ctk.CTkFrame(root, corner_radius=1, fg_color="#fff", border_width=1, border_color="#f0f0f0", width=300)

    title_label = ctk.CTkLabel(add_prod_frame, text=" اضافة منتج", font=('Arial', 20, 'bold'))
    title_label.pack(pady=10, fill='x',padx=20)
    
    create_label(add_prod_frame, '   بحث عن منتج').pack(pady=10, padx=10, ipady=10, fill='x')
    
    # frame
    search_frame = ctk.CTkFrame(add_prod_frame, fg_color='transparent', width=350, height=50, corner_radius=1)
    search_frame.pack(pady=10, padx=10)
    
    product = ctk.CTkEntry(search_frame, font=("Arial", 14), fg_color='#fff', border_width=1,
                        border_color='#ddd', corner_radius=1, width=345, placeholder_text='اسم المنتج او الكود', justify='center')
    product.pack(ipady=10, fill='x', side='right', padx=(0,10))
    

    
    btn = ctk.CTkButton(search_frame, text='ok', width=45, height=42, corner_radius=1, fg_color='#eee', text_color='#333', command=lambda:search_product(product.get()))
    btn.pack(pady=10, fill='x', padx=(10,0), side='right')
    
    # ... (keep the rest of the add_frame function as is)

    create_label(add_prod_frame, "الكمية  ").pack(pady=10,fill = 'x',padx=10,ipady=10)
    
    # frame
    qty_frame = ctk.CTkFrame(add_prod_frame,fg_color='transparent',width=300,height=50,corner_radius=1)
    qty_frame.pack(pady=10,padx=10)

    btn = ctk.CTkButton(qty_frame,font=('Ariel',20),text='+',width=45,height=42,corner_radius=1,fg_color='#eee',hover_color='#fff',
        text_color='#333',command=lambda:change('+')).pack(pady=10,padx=(0,10),side='right')
    
    qty_entry = create_entry1(qty_frame)
    qty_entry.pack(ipady=10,fill = 'x',side='right',anchor='center')
    
    btn = ctk.CTkButton(qty_frame,font=('Ariel',20),text='-',width=45,height=42,corner_radius=1,fg_color='#eee',hover_color='#fff',
        text_color='#333',command=lambda:change('-')).pack(pady=10,padx=(10,0),side='right')

    # ... (keep the existing code)

    def search_and_display():
        name_or_code = product.get()
        result = search_product(name_or_code)

        if result and float(qty_entry.get()) > 0:
            global inv_data
            global total_amount
            global final_total
            print('Result:', result)

            # Extraire les informations nécessaires du produit
            product_code = result[1]  # Supposons que le code produit est à l'index 1
            quantity = float(qty_entry.get())
            price = float(result[4])  # Supposons que le prix est à l'index 4
            total = quantity * price
            # total_amount += total  

            # Vérifier si le produit existe déjà dans inv_data
            product_exists = False
            for index, item in enumerate(inv_data):
                if item[0] == product_code:  # Vérifie si le code produit existe
                    # Si le produit existe, augmenter uniquement la quantité
                    existing_quantity = item[1]
                    new_quantity = existing_quantity + quantity
                    inv_data[index] = (item[0], new_quantity, price, new_quantity * price)
                    product_exists = True
                    # total_amount += item[2] * quantity
                    break

            # Si le produit n'existe pas, l'ajouter comme une nouvelle entrée
            if not product_exists:
                inv_data.append((product_code, quantity, price, total))

            # Mettre à jour l'affichage
            update_table()

            # Réinitialiser les champs d'entrée
            product.delete(0, 'end')
            qty_entry.delete(0, 'end')
            qty_entry.insert(0, '0')
            global change_value
            change_value = 0
        else:
            messagebox.showinfo("Erreur", "Le produit n'a pas été trouvé dans la base de données ou la quantité est invalide.")
    # btn
    add_button = ctk.CTkButton(
        add_prod_frame,
        text="تاكيد",
        width=400,
        corner_radius=4,
        command=search_and_display
    )
    add_button.pack(pady=5, ipady=10, padx=20, fill='x')
    return add_prod_frame
# tree = 
def frame_principal(root, sale_id=4, details=False,data=[]):
    invoice_detail_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")
    global inv_data 
    if details:
        inv_data = data
    print('sale_id:', sale_id) 
    show_frame, update_table = show_details_frame(invoice_detail_frame,sale_id=sale_id,details=details)
    show_frame.pack( expand=True, padx=10, pady=10,fill='x',side='left')
    
    add_prod = add_frame(invoice_detail_frame, update_table)
    add_prod.pack(expand=True, padx=5, pady=10,fill='x',side='left')  

    return invoice_detail_frame

# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# # window.state('zoomed')

# sales_frame = frame_principal(window)
# sales_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()
    
