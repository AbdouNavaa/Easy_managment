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
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        suppliers = connect.cursor()
        # messagebox.showinfo('Connection Successful', 'Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
        
def fetch_drop(total_variable,myList):
    query = f'SELECT * FROM accounts'
    total_variable.execute(query)
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        myList.append(f'{variable[0]}-{variable[1]}')
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    return myList  # Retourner 0 si aucun résultat n'est trouvé   


# import 

def create_add_supplier_frame(root):
    add_supplier_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    add_supplier_frame.pack(padx=400, pady=10, fill='y', ipady=100)

    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)   
    global justify 
    justify = 'left' 

# direction btn
    btns_frame = ctk.CTkFrame(add_supplier_frame,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=2)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#eee',text_color='black',command=lambda:direction('Fr')).pack(pady=10,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#eee',text_color='black',command=lambda:direction('Ar')).pack(pady=10,padx=(155,5),side='right')

    #name
    name_label = create_label(add_supplier_frame,"اسم المورد",400)
    name_entry = create_entry(add_supplier_frame)
    name_error_label = error_message(add_supplier_frame, "")
    
    #phone
    phone_label = create_label(add_supplier_frame,"رقم الهاتف",400)    
    phone_entry = create_entry(add_supplier_frame)    
    phone_error_label = error_message(add_supplier_frame, "")
    
    #email
    email_label = create_label(add_supplier_frame,"البريد الالكتروني",400)    
    email_entry = ctk.CTkEntry(add_supplier_frame, font=font_arial,
    fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=2,width=400)    
    email_entry.pack(ipady=10 , padx=20)
    email_error_label = error_message(add_supplier_frame, "")
    
    #address
    address_label = create_label(add_supplier_frame,"العنوان",400)    
    address_entry = create_entry(add_supplier_frame)
    address_error_label = error_message(add_supplier_frame, "")
    # Bouton pour sauvegarder les modifications
    def save_changes():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()    
        
        # Réinitialiser les messages d'erreur
        name_error_label.configure(text="")
        phone_error_label.configure(text="")
        email_error_label.configure(text="")
        address_error_label.configure(text="")

        # Validation des champs
        has_error = False

        if not validate_string(name):
            name_error_label.configure(text="ادخل اسم صحيح (حروف فقط)")
            has_error = True

        if not validate_number(phone):
            phone_error_label.configure(text="ادخل رقم هاتف صحيح (8 أرقام على الأقل)")
            has_error = True

        if not validate_email(email):
            email_error_label.configure(text="ادخل بريد الكتروني صحيح")
            has_error = True        
        
        if address == '':
            address_error_label.configure(text="ادخل  عنوان ")
            has_error = True        
        
        if has_error:
            return  # Ne pas continuer si une erreur est détectée
            
        try:
            connect_db()
        
            query = 'insert into suppliers (name,phone,email,address) values(%s,%s,%s,%s)'
            my_cursor.execute(query,(name,phone,email,address))
            connect.commit()
            messagebox.showinfo('نجاح', 'تم اضافة المورد بنجاح')
            
            result = messagebox.askyesno('تم الاضافة', 'هل تريد اضافة مورد جديد?' , parent=add_supplier_frame)
            if result == True:
                name_entry.delete(0,tk.END)
                phone_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                address_entry.delete(0, tk.END) 
                # add_supplier_frame.destroy()  # Fermer la fenêtre de mise à jour
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

    ctk.CTkButton(add_supplier_frame, text=" حفظ", command=save_changes,width=400,corner_radius=2,font=font_arial_title).pack(pady=5,padx=20,ipady=10)


    return add_supplier_frame

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
    entry = ctk.CTkEntry(parent, justify=justify,font=font_arial, fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=2, width=400)
    entry.pack(ipady=10 , padx=20)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text,wid):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text, width=wid)
    label.pack(ipady=10, pady=5, padx=20)
    label_widgets.append(label)
    return label

def error_message(parent,text):
    message = ctk.CTkLabel(parent, text="", text_color="red", font=("Arial", 12))
    message.pack(padx=20)
    return message

import re 
# Fonctions de validation
def validate_string(input_str):
    return bool(re.match(r'^[A-Za-z\s]+$', input_str))

def validate_number(input_str):
    # Vérifie que l'entrée contient uniquement des chiffres et a une longueur d'au moins 5
    return bool(re.match(r'^[0-9]{8,}$', input_str))

def validate_email(input_str):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', input_str))


# window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# add_supplier_frame = create_add_supplier_frame(window)
# add_supplier_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()