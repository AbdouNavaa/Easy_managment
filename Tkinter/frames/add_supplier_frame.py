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
    name_label.pack(ipady=10, pady=1, padx=20)
    
    name_entry = create_entry(add_supplier_frame)
    name_entry.pack(ipady=10, padx=20)

    
    #phone
    phone_label = create_label(add_supplier_frame,"رقم الهاتف",400)
    phone_label.pack(ipady=10, pady=5, padx=20)
    
    phone_entry = create_entry(add_supplier_frame)
    phone_entry.pack(ipady=10 , padx=20)
    
    
    #email
    email_label = create_label(add_supplier_frame,"البريد الالكتروني",400)
    email_label.pack(ipady=10, pady=5, padx=20)
    
    email_entry = ctk.CTkEntry(add_supplier_frame, font=font_arial,
    fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,width=400)
    email_entry.pack(ipady=10 , padx=20)
    
    #address
    address_label = create_label(add_supplier_frame,"العنوان",400)
    address_label.pack(ipady=10, pady=5, padx=20)
    
    address_entry = create_entry(add_supplier_frame)
    address_entry.pack(ipady=10 , padx=20)
    
    # labels frame
    labs_frame = ctk.CTkFrame(add_supplier_frame,fg_color='transparent',width=400)
    labs_frame.pack( ipady=10 , padx=20, pady=2)
    
    # entries frame
    entries_frame = ctk.CTkFrame(add_supplier_frame,fg_color='transparent',width=400)
    entries_frame.pack( ipady=10 , padx=20, pady=2)
    
    # credit limit
    credit_label = create_label(labs_frame,"الحد",200)
    credit_label.pack(ipady=10 ,pady=5, padx=(0,2),side='right')
    
    credit_limit = ctk.CTkEntry(entries_frame, font=font_arial, 
        fg_color='#fff',border_width=1,border_color='#ddd',corner_radius=8,justify='right',width=200)
    credit_limit.pack(ipady=10 , padx=2,side='right')
    
    # account_id 
    connect_db()
    list_of_suppliers = []
    fetch_drop(suppliers, list_of_suppliers)

    account_label = create_label(labs_frame,"الحساب",200)
    account_label.pack(ipady=10,pady=5 , padx=(2,0),side='left')

    account_id = ctk.CTkOptionMenu(
        entries_frame,values=list_of_suppliers,anchor='center',
        text_color="#333",dropdown_fg_color="#fff",
        width=200,
        font=font_arial,
        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",button_hover_color='#fff',
    )
    account_id.pack(ipady=10 , padx=2,side='left')
    # Bouton pour sauvegarder les modifications
    def save_changes():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()
        credit = credit_limit.get()
        account = account_id.get()[0]        
        
        try:
            connect_db()
        
            query = 'insert into suppliers (name,phone,email,address,credit_limit,account_id) values(%s,%s,%s,%s,%s,%s)'
            my_cursor.execute(query,(name,phone,email,address,credit,account))
            connect.commit()
            messagebox.showinfo('Success', 'supplier added successfully')
            refresh_callback()
            
            result = messagebox.askyesno('supplier added successfully', 'do you want to clean the form?' , parent=add_supplier_frame)
            if result == True:
                name_entry.delete(0,tk.END)
                phone_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                address_entry.delete(0, tk.END) 
                credit_limit.delete(0, tk.END)
                # add_supplier_frame.destroy()  # Fermer la fenêtre de mise à jour
                
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
            return

    ctk.CTkButton(add_supplier_frame, text=" حفظ", command=save_changes).pack(pady=5,padx=20,fill='x',ipady=10)


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
    entry = ctk.CTkEntry(parent, justify=justify,font=font_arial, fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=8, width=400)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text,wid):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text, width=wid)
    label_widgets.append(label)
    return label

# window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# add_supplier_frame = create_add_supplier_frame(window)
# add_supplier_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()