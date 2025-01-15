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
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        print('Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))


# Function to fetch categories with pagination
def fetch_categories(limit=10, offset=0):
    connect_db()
    query = f'''
    SELECT c.id, c.name, c.description, COUNT(p.id) AS product_count
    FROM product_categories c
    LEFT JOIN products p ON c.id = p.category_id
    GROUP BY c.id, c.name, c.description
    LIMIT {limit} OFFSET {offset}'''
    my_cursor.execute(query)
    return my_cursor.fetchall()

# fenetere pour ajouter une categorie
def open_add_window(refresh_callback):
    update_window = ctk.CTkToplevel(fg_color='#fff')
    # update_window.pack()
    update_window.title(" اضافة فئة جديدة   ")
    # Champ pour le nom du produit
    ctk.CTkLabel(update_window,anchor='e', text="الفئة اسم").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    name_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    # name_entry.insert(0, category[1])  # Pré-remplir avec la valeur actuelle
    name_entry.pack(ipady=10 , padx=20)

    ctk.CTkLabel(update_window,anchor='e', text="الفئة وصف").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    # description_entry = ctk.CTkTextbox(add_category_frame, width=400, corner_radius=8)
    desc_entry = ctk.CTkTextbox(update_window, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,width=400)
    # desc_entry.insert(index='0.0', text=category[2])  # Pré-remplir avec la valeur actuelle
    desc_entry.pack(ipady=10 , padx=20,)

    # Bouton pour sauvegarder les modifications
    def save_changes():
        new_name = name_entry.get()
        new_desc = desc_entry.get(index1='0.0', index2='end')
        
        c_name = new_name
        c_description = new_desc
        
        try:
            connect_db()
        
            query = 'insert into category values(null,%s,%s)'
            my_cursor.execute(query,(c_name,c_description))
            connect.commit()
            messagebox.showinfo('Success', 'category added successfully')
            refresh_callback()
            
            
            result = messagebox.askyesno('category added successfully', 'do you want to clean the form?' , parent=update_window)
            if result == True:
                name_entry.delete(0,tk.END)
                desc_entry.delete(0,tk.END)    
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

        # messagebox.showinfo("Success", "Category updated successfully!")
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        # update_callback()

    ctk.CTkButton(update_window, text="Add", command=save_changes).pack(pady=10)


# Fonction pour afficher la fenêtre de mise à jour
def open_update_window(category, update_callback):
    update_window = ctk.CTkToplevel(fg_color='#fff')
    # update_window.pack()
    update_window.title("Update category")

    print("Category", category)
    # Champ pour le nom du produit
    ctk.CTkLabel(update_window,anchor='e', text="الفئة اسم").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    name_entry = ctk.CTkEntry(update_window, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=400)
    name_entry.insert(0, category[1])  # Pré-remplir avec la valeur actuelle
    name_entry.pack(ipady=10 , padx=20)

    ctk.CTkLabel(update_window,anchor='e', text="الفئة وصف").pack(fill='x',ipady=10 ,pady=2, padx=20,)
    # description_entry = ctk.CTkTextbox(add_category_frame, width=400, corner_radius=8)
    desc_entry = ctk.CTkTextbox(update_window, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,width=400)
    desc_entry.insert(index='0.0', text=category[2])  # Pré-remplir avec la valeur actuelle
    desc_entry.pack(ipady=10 , padx=20,)

    # Bouton pour sauvegarder les modifications
    def save_changes():
        new_name = name_entry.get()
        new_desc = desc_entry.get(index1='0.0', index2='end')
        
        c_id = category[0]
        c_name = new_name
        c_description = new_desc
        
        try:
            connect_db()
            query = 'update category set name=%s,description=%s where c_id=%s'
            my_cursor.execute(query,(c_name,c_description,c_id))
            connect.commit()
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

        messagebox.showinfo("Success", "Category updated successfully!")
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(update_window, text="Save Changes", command=save_changes).pack(pady=10)


def delete_category(category_id, update_callback):
    print('CatId', category_id)
    connect_db()
    try:
        query = f"DELETE FROM category WHERE c_id = {category_id}"
        my_cursor.execute(query)
        connect.commit()
        messagebox.showinfo('Success', 'Category deleted successfully')
        
        # Appel de la fonction pour actualiser les données
        update_callback()
    except Exception as e:
        messagebox.showerror('Error', str(e))

# Function to show categories as a styled table with pagination
def show_categories_table(parent, limit=10):
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
        data = fetch_categories(limit, offset)

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
                label1.grid(row=row_index, column=4, sticky="nsew", padx=5, pady=5)

                # prods_num = ctk.CTkLabel(
                #     data_frame,
                #     text='0',
                #     font=font_arial,
                #     text_color="#333",
                #     fg_color="#fff",
                #     corner_radius=5,
                #     width=100
                # )
                # prods_num.grid(row=row_index, column=1, sticky="e", padx=5, pady=5)
                label.grid(row=row_index, column=col_index+1, sticky="e", padx=5, pady=5)
                
                font_arial_btn = ('Arial',14,'bold')
                buttons_frame = ctk.CTkFrame(data_frame, width=100,height=40,fg_color="transparent",
                                        # command=lambda row=row: show_supplier_details(row)
                                        ) 
                
                buttons_frame.grid(row=row_index , column=0, sticky="nsew", padx=5, pady=5)
                
                
                edit_image_path = os.path.join(os.path.dirname(__file__), "images", "edit.png")
                edit_image = ctk.CTkImage(light_image=Image.open(edit_image_path), size=(15, 15),)
                update_button = ctk.CTkButton(buttons_frame, text="تعديل",text_color="black",
                        image=edit_image,
                        fg_color='#f9f9f9',
                        hover_color='#f0f0f0',
                        width=100,
                        font=font_arial_btn,        
                        command=lambda row=row: open_update_window(row[::-1],update_table)
                        )
                update_button.grid(row=0,column=1)
                
                
                delete_image_path = os.path.join(os.path.dirname(__file__), "images", "trash-can.png")
                delete_image = ctk.CTkImage(light_image=Image.open(delete_image_path), size=(20, 20),)
                delete_button = ctk.CTkButton(buttons_frame,
                        text="حذف",
                        text_color="black",
                        image=delete_image,
                        fg_color='#f9f9f9',
                        hover_color='#f00',
                        font=font_arial_btn, 
                        width=100,
                        command=lambda row=row: delete_category(row[::-1][0], update_table)
                        )
                delete_button.grid(row=0,column=0,padx=5)
                
    
    show_title_frame(parent,update_table)
    offset = 0

    # Table headers
    columns = (' رقم ', 'الاسم ', 'الوصف', 'عدد المنتجات','الاجراءات')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=2, fg_color="#fff",border_width=1,border_color="#f0f0f0")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure(( 1, 4), weight=1, uniform='a')
    header_frame.columnconfigure((0,), weight=2, uniform='a')
    header_frame.columnconfigure((2,3), weight=3, uniform='a')  
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
    # data_frame.columnconfigure((0, 1,2, 3,4), weight=1, uniform='a')

    data_frame.columnconfigure(( 1, 4), weight=1, uniform='a')
    data_frame.columnconfigure((0,), weight=2, uniform='a')
    data_frame.columnconfigure((2,3), weight=3, uniform='a')    # data_frame.columnconfigure(2, weight=2, uniform='a')

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
        text="فئات المنتجات",
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
        text=" اضافة فئة جديدة",
        font=font_arial,
        width=40,
        text_color="#333",
        fg_color="#f0f0f0",
        hover_color="#f0f0f0",
        corner_radius=5,
        # border_color="#f0f0f0",
        command=lambda: open_add_window(refresh_callback)
    )
    add_inventory_button.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5)


    
    

# Function to create the categories frame
def create_categories_frame(root):
    categories_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")


    show_categories_table(categories_frame)
    return categories_frame



window = ctk.CTk(fg_color="#fff")
window.title('customtkinter app')
window.geometry('1200x550')
window.state('zoomed')


categories_frame = create_categories_frame(window)
categories_frame.pack(fill='both', expand=True)

# run
window.mainloop()