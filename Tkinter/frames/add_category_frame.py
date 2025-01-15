import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pymysql
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
def create_add_category_frame(root):
    
    add_category_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    add_category_frame.pack(padx=400,pady=(10,80),ipady=10,)
    
    # info colored labelframe style
    # ctk.CTkLabelframe(add_category_frame,bootstyle="info").pack()

    # Champ de nom d'utilisateur
    # Titre de la page
    title_label = ctk.CTkLabel(
        add_category_frame, text="فئة إضافة",  bg_color="#fff",  font=('Arial', 20, 'bold'),anchor='center'
    )
    title_label.pack(fill='x', padx=20,pady=(10,1))

    category_name_label = ctk.CTkLabel(
        add_category_frame, text=" الفئة اسم",bg_color='white',anchor='e'
    )
    category_name_label.pack(fill='x', padx=20,)
    
    # name_placeholder = tk.StringVar(value='اسم المنتج')
    category_name_entry = ctk.CTkEntry(
        add_category_frame, font=("times new roman", 14), 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right'
    )
    category_name_entry.pack(fill='x',ipady=10 ,pady=10, padx=20,)

    # Champ de mot de passe
    description_label = ctk.CTkLabel(
        add_category_frame, text=" الفئة وصف  ", bg_color="white",anchor='e'
    )
    description_label.pack(fill='x', padx=(10,20),)
    description_entry = ctk.CTkTextbox(add_category_frame, width=400, corner_radius=8)
    description_entry.pack(fill='x',ipady=10 ,pady=(30,10), padx=20,)

    
    # Bouton de connexion

    def add_categories():
        category_name = category_name_entry.get()
        category_description = description_entry.get(index1='0', index2='end')
        
        # Validation des informations de connexion
        if category_name == "" or category_description == "" :
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                
                connect_db()
                query = 'insert into category values(null,%s,%s)'
                my_cursor.execute(query,(category_name,category_description))
                connect.commit()
                messagebox.showinfo('Success', 'category added successfully')
                
                
                result = messagebox.askyesno('category added successfully', 'do you want to clean the form?' , parent=add_category_frame)
                if result == True:
                    category_name_entry.delete(0,tk.END)
                    description_entry.delete(0,tk.END)
            except Exception as e:
                messagebox.showerror('Error', str(e))
            # print(user)
            

    add_button = ctk.CTkButton(
        add_category_frame,
        text="تاكيد",
        width=23,
        command=add_categories
        
    )
    add_button.pack(pady=10,fill='x',padx=20,ipady=15)
    
    
    
    return add_category_frame


# window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# add_category_frame = create_add_category_frame(window)
# add_category_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()