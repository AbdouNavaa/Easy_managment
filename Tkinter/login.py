from tkinter import *
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
import pymysql

# Fonction pour valider les informations de connexion

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
        
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    # Validation des informations de connexion
    if username == "" or password == "":
        messagebox.showerror("Error", "Please fill all the fields")
    else:
        connect_db()
        query = 'SELECT * FROM user WHERE name=%s AND password=%s'
        user = my_cursor.execute(query,(username,password))
        print(user)
        
    if user == 1 :  # Exemple simple
        messagebox.showinfo("Login Successful", f"Welcome! {username}")
        main_window.destroy()
        # Créer une nouvelle fenêtre avec des widgets supplémentaires
        import home
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# Fenêtre principale
main_window = ThemedTk()
main_window.get_themes()

# main_window.set_theme('equilux') # belles fonts : breeze ou equilux ,arc ou adapta
main_window.set_theme('arc') # change the theme to vista

# main_window = Tk()
# main_window.geometry('700x700')
main_window.state('zoomed')
main_window.resizable(True, True)
main_window.title("تسجيل الدخول")


# Couleur de fond
main_window.configure(bg="#fff")
# Style pour ttk.Frame
style = ttk.Style()
style.configure(
    "Login.TFrame",
    background="#fff",  # Couleur de fond
    borderwidth=1,
    relief="ridge"  ,# Type de bordure (flat, solid, ridge, etc.)
    
)


# Cadre pour le formulaire de connexion
login_frame = ttk.Frame(main_window, style="Login.TFrame", width=600,height=700, padding=70)
login_frame.pack(pady=50)

# Champ de nom d'utilisateur
# Titre de la page
title_label = ttk.Label(
    login_frame, text="تسجيل الدخول",  background="#fff", foreground="#333", font=('book antiqua', 20, 'bold')
)
title_label.grid(row=0, column=1, pady=10, sticky=N,)

username_label = ttk.Label(
    login_frame, text="اسم المستخدم",background='white'
)
username_label.grid(row=1, column=1, pady=10, sticky=E,)
username_entry = ttk.Entry(
    login_frame, font=("times new roman", 14), width=30, state="normal",
)
username_entry.grid(row=2, column=1, pady=10, padx=10, ipady=7,)

# Champ de mot de passe
password_label = ttk.Label(
    login_frame, text="كلمة المرور", background="white"
)
password_label.grid(row=3, column=1, pady=10, sticky=E)
password_entry = ttk.Entry(
    login_frame, font=("times new roman", 14), width=30,  show="*",
)
password_entry.grid(row=4, column=1, pady=10, padx=10,ipady=7,)

# Bouton de connexion

b_style = ttk.Style()
b_style.configure(
    "button.TButton",
    background="#000",  # Couleur de fond
    # bgcolor="#000",
    borderwidth=1,
    relief="ridge"  ,# Type de bordure (flat, solid, ridge, etc.)
    
)
login_button = Button(
    login_frame,
    text="دخول",
    # style="button.TButton",
    font=("Helvetica", 14, "bold"),
    bg="#001",
    fg="white",
    activebackground="white",
    activeforeground="black",
    cursor="hand2",
    # padding=10,
    command=login,width=23,
)
login_button.grid(row=5, column=1, columnspan=3, pady=20, )

# Pied de page
footer_label = Label(
    main_window,
    text="© 2024 MyApp. All rights reserved.",
    font=("Helvetica", 10),
    bg="#fff",
    fg="#666",
)
footer_label.pack(side=BOTTOM, pady=10)

connect_db()
main_window.mainloop()
