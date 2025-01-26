import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pymysql
import bcrypt

# === Connexion à la base de données ===
def connect_db():
    try:
        global connect
        global my_cursor
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        print('Connected to the database')
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))

# === Fonction de Connexion ===
def login_action(login_window):
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please fill all the fields")
        return

    try:
        connect_db()

        # Rechercher l'utilisateur par nom d'utilisateur
        query = 'SELECT * FROM users WHERE username=%s'
        my_cursor.execute(query, (username,))
        result = my_cursor.fetchone()  # Récupère le hash du mot de passe

        if result:
            print(result)
            stored_hashed_password = result[3]

            # Comparer les mots de passe
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                messagebox.showinfo("Login Successful", f"Welcome! {username}")
                # import time as time
                # time.sleep(5)  # Attendre 1 seconde avant de lancer l'interface principale
                login_window.destroy()  # Détruire la fenêtre de login aprss  quelques secondes
                import home
                home.launch_main_window(result)
                launch_main_window(result)  # Lancer l'interface principale
            else:
                messagebox.showerror("Login Failed", "Invalid Username or Password")
        else:
            messagebox.showerror("Login Failed", "User not found")

    except Exception as e:
        messagebox.showerror('Error', str(e))

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
def create_entry(parent,width=400):
    entry = ctk.CTkEntry(parent, justify=justify,font=("Arial", 14), fg_color='#fff', 
                        border_width=1, border_color='#ddd', corner_radius=8, width=width)
    entry.pack(ipady=10 , padx=20)
    entry_widgets.append(entry)
    return entry

# for labels
def create_label(parent,text,wid=200):
    label = ctk.CTkLabel(parent, bg_color='#f9f9f9', font=("Arial", 16,'bold'), anchor='center', text=text, width=wid)
    label_widgets.append(label)
    return label




# === Création de la fenêtre de connexion ===
def launch_login_window():
    login_window = ctk.CTk(fg_color="#fff")
    login_window.title("تسجيل الدخول")
    login_window.state("zoomed")
    # login_window.resizable(False, False)
    navbar = ctk.CTkFrame(login_window, fg_color="#333", corner_radius=0)
    navbar.pack(side="top", fill="x")
    button_style = {"font": ("Arial", 16), "fg_color": "#333", "text_color": "white", "hover_color": "#333"}
    # logo button
    logo_btn = ctk.CTkButton(navbar, text="Easy", **button_style,width=140,anchor='w')
    logo_btn.pack(side="right", padx=1, pady=5)
    global username_entry, password_entry  # Pour l'utiliser dans login_action
    # Création du frame
    login_frame = ctk.CTkFrame(login_window, fg_color='#fff', border_width=1, border_color='#ddd')
    login_frame.pack(padx=400,pady=100,ipady=30,)
    
    font_arial_title =("Arial", 16,'bold')
    font_arial =("Arial", 14)
    global justify 
    justify = 'left' 

    # direction btn
    btns_frame = ctk.CTkFrame(login_frame,fg_color='transparent',width=400)
    btns_frame.pack( ipady=10 , padx=20, pady=10)
    ctk.CTkButton(btns_frame, text="Fr",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Fr')).pack(pady=1,padx=(5,155),side='left')
    ctk.CTkButton(btns_frame, text="Ar",width=40,fg_color='#f6f7f7',hover_color='#fff',text_color='black',command=lambda:direction('Ar')).pack(pady=1,padx=(155,5),side='right')
    # name 
    create_label(login_frame,"اسم المستخدم").pack(ipady=10 ,pady=10, padx=20,fill='x')
    username_entry = create_entry(login_frame)
    
    
    # password_hash
    create_label(login_frame,"كلمة المرور").pack(ipady=10 ,pady=10, padx=20,fill='x')
    password_entry = create_entry(login_frame)
    
    # check box for remember me
    # check_frame = ctk.CTkFrame(login_frame,fg_color='transparent')
    # check_frame.pack(ipady=10, padx=20, pady=10,fill='x')
    
    # remember_me_var = tk.IntVar()
    # remember_me_check_box = ctk.CTkCheckBox(check_frame, text="", variable=remember_me_var,border_color='#f0f0f0',checkmark_color='blue',
    #                                     font=('Arial',16),fg_color='#eee',hover_color='#eee',)
    # remember_me_check_box.pack(pady=10, padx=2,side='right',fill='x',anchor='e')
    
    # label = ctk.CTkLabel(check_frame,text='تذكرني', font=('Arial',16),anchor='e',fg_color='#e11')
    # label.pack(pady=10, padx=2,side='right',fill='x')
    
    add_button = ctk.CTkButton(
        login_frame,
        font=font_arial_title,
        text="تسجيل الدخول",
        width=400,
        command=lambda: login_action(login_window),
    )
    add_button.pack(pady=20,padx=20,ipady=10)# Fonction pour afficher la fenêtre de mise à jour

    # Afficher la fenêtre de connexion
    login_window.mainloop()

# === Exécution de l'application ===
if __name__ == "__main__":
    launch_login_window()
