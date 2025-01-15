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

def create_add_supplier_frame(root):
    add_supplier_frame = ctk.CTkFrame(root, fg_color='#fff', border_width=1, border_color='#ddd')
    add_supplier_frame.pack(padx=400, pady=10, fill='y', ipady=100)

    # Validation functions
    def is_number(value_if_allowed):
        """Allow only numbers."""
        return value_if_allowed.isdigit() or value_if_allowed == ""

    def is_email(value_if_allowed):
        """Simple validation to allow email format."""
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@._-")
        return all(char in allowed_chars for char in value_if_allowed)

    def is_alpha(value_if_allowed):
        """Allow only alphabetic characters."""
        return value_if_allowed.isalpha() or value_if_allowed == ""

    # Register validation commands
    vcmd_number = root.register(is_number)
    vcmd_email = root.register(is_email)
    vcmd_alpha = root.register(is_alpha)

    # Page Title
    title_label = ctk.CTkLabel(
        add_supplier_frame, text="مورد إضافة", bg_color="#fff", 
        font=('Arial', 20, 'bold'), anchor='center'
    )
    title_label.pack(fill='x', padx=20, pady=(10, 1))

    # Input Fields
    inputs = [
        {"label": "المورد اسم", "type": "alpha", "key": "supplier_name"},
        {"label": "المسؤول الشخص", "type": "alpha", "key": "responsable_name"},
        {"label": "الهاتف رقم", "type": "number", "key": "phone"},
        {"label": "البريد الالكتروني", "type": "email", "key": "email"},
        {"label": "العنوان", "type": "text", "key": "address"},
    ]

    entry_widgets = {}
    for item in inputs:
        label = ctk.CTkLabel(add_supplier_frame, text=item["label"], bg_color="white", anchor='e')
        label.pack(fill='x', padx=20)

        # Determine the validation function
        if item["type"] == "number":
            validate_command = vcmd_number
        elif item["type"] == "alpha":
            validate_command = vcmd_alpha
        elif item["type"] == "email":
            validate_command = vcmd_email
        else:
            validate_command = None

        entry = ctk.CTkEntry(
            add_supplier_frame, font=("times new roman", 14),
            fg_color='#fff', border_width=1, border_color='#ddd', corner_radius=8, justify='right',
            validate="key", validatecommand=(validate_command, "%P") if validate_command else None
        )
        entry.pack(fill='x', ipady=10, pady=10, padx=20)

        entry_widgets[item["key"]] = entry

    # Add Supplier Action
    def add_suppliers():
        data = {key: entry.get() for key, entry in entry_widgets.items()}
        if any(not value for value in data.values()):
            messagebox.showerror("Error", "Veuillez remplir tous les champs")
        else:
            try:
                connect_db()
                query = 'INSERT INTO supplier VALUES (NULL, %s, %s, %s, %s, %s)'
                my_cursor.execute(query, (data["supplier_name"], data["responsable_name"], data["phone"], data["email"], data["address"]))
                connect.commit()
                messagebox.showinfo('Success', 'Fournisseur ajouté avec succès')

                result = messagebox.askyesno('Fournisseur ajouté avec succès', 'Voulez-vous nettoyer le formulaire?', parent=add_supplier_frame)
                if result:
                    for entry in entry_widgets.values():
                        entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror('Error', str(e))

    # Confirm Button
    add_button = ctk.CTkButton(
        add_supplier_frame,
        text="تاكيد",
        width=23,
        command=add_suppliers
    )
    add_button.pack(pady=10, fill='x', padx=20, ipady=10)

    return add_supplier_frame

# window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# add_supplier_frame = create_add_supplier_frame(window)
# add_supplier_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()