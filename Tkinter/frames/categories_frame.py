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
        global categories
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        categories = connect.cursor()
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
    add_window = tk.Toplevel(background='#fff')
    # add_window.pack()
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

# direction btn
    btns_frame = ctk.CTkFrame(add_window,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # name 
    create_label(add_window,"اسم الفئة").pack(ipady=10 ,pady=5, padx=20,fill='x')
    name_entry = create_entry(add_window)

    # desc 
    create_label(add_window,"وصف الفئة").pack(ipady=10 ,pady=5, padx=20,fill='x')
    desc_entry = ctk.CTkTextbox(add_window, font=("Arial", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,width=400,)
    desc_entry.pack(ipady=10 , padx=20,)
    
    # parent
    connect_db()
    list_of_categories = []
    fetch_drop(categories, list_of_categories)

    ctk.CTkLabel(add_window,anchor='center', text="القسم",font=font_arial_title,bg_color='#f9f9f9').pack(ipady=10 ,pady=5, padx=20,fill='x')

    category_entry = ctk.CTkOptionMenu(
        add_window,values=list_of_categories,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
    )
    category_entry.pack(ipady=10 , padx=20,)
    
    ctk.CTkLabel(add_window, anchor='e', text="تاريخ الانشاء", font=font_arial_title).pack(fill='x', ipady=10, pady=2, padx=20)
    
    # Create a frame to hold the DateEntry widget and a button
    date_frame = ctk.CTkFrame(add_window, fg_color='transparent',height=30)
    date_frame.pack(fill='x', padx=20, pady=5)

    # Create the DateEntry widget
    created_at_entry = DateEntry(date_frame, width=30, background='white',font=font_arial,
                                foreground='black', justify='center', date_pattern='yyyy-mm-dd',)
    created_at_entry.pack( side='right',padx=(0, 10),ipady=10)

    # Create a button to clear the date
    clear_date_button = ctk.CTkButton(date_frame, text="Clear Date", text_color='black',
        width=100, height=30, command=lambda: created_at_entry.set_date(None), fg_color='#f9f9f9', hover_color='#f9f9f8', corner_radius=5)
    clear_date_button.pack(side='left')
    # Bouton de connexion

    def add_categories():
        name = name_entry.get()
        description = desc_entry.get(index1='0.0', index2='end')
        category_id = category_entry.get().split('-')[0]
        created_at = created_at_entry.get_date().strftime('%Y-%m-%d') if created_at_entry.get_date() else None
        
        # Validation des informations de connexion
        if name == "" or description == "" :
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                
                connect_db()
                query = 'insert into product_categories values(null,%s,%s,%s,%s)'
                my_cursor.execute(query,(name, description,category_id,created_at))
                connect.commit()
                messagebox.showinfo('Success', 'category added successfully')
                refresh_callback()
                
                
                result = messagebox.askyesno('category added successfully', 'do you want to clean the form?' , parent=add_window)
                if result == True:
                    name_entry.delete(0,tk.END)
                    desc_entry.delete(1.0, tk.END)
                    created_at_entry.set_date(None)
                    # add_window.destroy()
            except Exception as e:
                messagebox.showerror('Error', str(e))
            

    add_button = ctk.CTkButton(
        add_window,
        text="تاكيد",
        width=23,
        command=add_categories
        
    )
    add_button.pack(pady=10,fill='x',padx=20,ipady=15)
    # ctk.CTkButton(update_window, text="Add", command=save_changes).pack(pady=10)

from tkcalendar import DateEntry
from datetime import datetime
# Fonction pour afficher la fenêtre de mise à jour
def open_update_window(category, update_callback):
    
    update_window = tk.Toplevel(background='#fff')
    # update_window.pack()
    update_window.title("تعديل")

    categ=fetch_category(category[0])
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
# direction btn
    btns_frame = ctk.CTkFrame(update_window,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # name 
    create_label(update_window,"اسم الفئة").pack(ipady=10 ,pady=5, padx=20,fill='x')
    name_entry = create_entry(update_window)
    name_entry.insert(0, categ[1])  # Pré-remplir avec la valeur actuelle

    # desc 
    create_label(update_window,"وصف الفئة").pack(ipady=10 ,pady=5, padx=20,fill='x')
    desc_entry = ctk.CTkTextbox(update_window, font=font_arial, 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,width=400,)
    desc_entry.insert(index='0.0', text=categ[2])  # Pré-remplir avec la valeur actuelle
    desc_entry.pack(ipady=10 , padx=20,)
    
    # parent
    connect_db()
    list_of_categories = []
    fetch_drop(categories, list_of_categories)

    ctk.CTkLabel(update_window,anchor='center', text="القسم",font=font_arial_title,bg_color='#f9f9f9').pack(ipady=10 ,pady=5, padx=20,fill='x')

    category_entry = ctk.CTkOptionMenu(
        update_window,values=list_of_categories,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
    )
    # category_entry.insert(0, str(prod[5]))  # Pré-remplir avec la valeur actuelle
    category_entry.pack(ipady=10 , padx=20,)
    
    ctk.CTkLabel(update_window, anchor='e', text="تاريخ الانشاء", font=font_arial_title).pack(fill='x', ipady=10, pady=2, padx=20)
    
    # Create a frame to hold the DateEntry widget and a button
    date_frame = ctk.CTkFrame(update_window, fg_color='transparent',height=30)
    date_frame.pack(fill='x', padx=20, pady=5)

    # Create the DateEntry widget
    created_at_entry = DateEntry(date_frame, width=30, background='white',font=font_arial,
                                foreground='black', justify='center', date_pattern='yyyy-mm-dd',)
    created_at_entry.pack( side='right',padx=(0, 10),ipady=10)

    # Set the initial date if available
    if categ[4]:
        try:
            # Check if categ[4] is already a datetime object
            if isinstance(categ[4], datetime):
                created_at_entry.set_date(categ[4].date())
            else:
                # If it's a string, parse it
                created_at_entry.set_date(datetime.strptime(categ[4], '%Y-%m-%d %H:%M:%S').date())
        except ValueError as e:
            messagebox.showerror("Error", "Invalid date format: {categ[4]}, Error: {e}!")

    clear_date_button = ctk.CTkButton(date_frame, text="Clear Date", text_color='black',
        width=100, height=30, command=lambda: created_at_entry.set_date(None), fg_color='#f9f9f9', hover_color='#f9f9f8', corner_radius=5)
    clear_date_button.pack(side='left')

    # Bouton pour sauvegarder les modifications
    def save_changes():
        name = name_entry.get()
        description = desc_entry.get(index1='0.0', index2='end')
        category_id = category_entry.get().split('-')[0]
        created_at = created_at_entry.get_date().strftime('%Y-%m-%d') if created_at_entry.get_date() else None
        id = category[0]
        
        try:
            connect_db()
            query = 'update product_categories set name=%s, description=%s, parent_id=%s, created_at=%s where id=%s'
            my_cursor.execute(query, (name, description, category_id, created_at, id))
            connect.commit()
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

        messagebox.showinfo("Success", "Category updated successfully!")
        update_window.destroy()  # Fermer la fenêtre de mise à jour
        update_callback()

    ctk.CTkButton(update_window, text=" حفظ التعديل",font=font_arial_title, command=save_changes).pack(fill='x' ,ipady=5, padx=20,pady=10,after=date_frame)

def fetch_drop(total_variable,myList):
    query = f'SELECT * FROM product_categories'
    total_variable.execute(query)
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        myList.append(f'{variable[0]}-{variable[1]}')
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    # print(myList)
    return myList  # Retourner 0 si aucun résultat n'est trouvé   

def fetch_category(prod_id):
    connect_db()
    query = f'''
    SELECT *
    FROM product_categories  WHERE id = %s'''
    
    ''' '''
    
    my_cursor.execute(query, (prod_id,))
    result = my_cursor.fetchone()
    return result


def delete_category(category_id, update_callback):
    connect_db()
    try:
        query = f"DELETE FROM product_categories WHERE id = {category_id}"
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
        offset = (page_num - 1) * limit
        update_table()

    def update_table():
        # Clear previous table data
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Fetch new data
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

                label.grid(row=row_index, column=col_index+1, sticky="nsew", padx=5, pady=5)
                
                font_arial_btn = ('Arial',14,'bold')
                buttons_frame = ctk.CTkFrame(data_frame, width=100,height=40,fg_color="transparent",
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
    entry = ctk.CTkEntry(parent, justify=justify,font=("Arial", 14), fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=8, width=400)
    entry.pack(ipady=10 , padx=20)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text)
    label_widgets.append(label)
    return label


# Function to create the categories frame
def create_categories_frame(root):
    categories_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")


    show_categories_table(categories_frame)
    return categories_frame



# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')


# categories_frame = create_categories_frame(window)
# categories_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()