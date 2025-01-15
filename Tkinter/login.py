from tkinter import *
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk  # Pour charger et manipuler les images
import pymysql

# Fonction pour valider les informations de connexion
def connect_db():
    try:
        # create a connection object
        global connect
        global my_cursor
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='sms')
        my_cursor = connect.cursor()
        print('Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please fill all the fields")
    else:
        connect_db()
        query = 'SELECT * FROM user WHERE name=%s AND password=%s'
        user = my_cursor.execute(query, (username, password))
        print(user)

    if user == 1:
        messagebox.showinfo("Login Successful", f"Welcome! {username}")
        main_window.destroy()
        import home  # Exemple : changez à votre convenance
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# Fenêtre principale
main_window = ThemedTk()
main_window.get_themes()
main_window.set_theme('arc')
main_window.state('zoomed')
main_window.resizable(True, True)
main_window.title("تسجيل الدخول")

# Charger l'image de fond
bg_image_path = "./assets/blanch_bg1.jpg"
try:
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((main_window.winfo_screenwidth(), main_window.winfo_screenheight()), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(main_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    print(f"Erreur lors du chargement de l'image de fond : {e}")

# Style pour ttk.Frame
style = ttk.Style()
style.configure("Login.TFrame", background="white", borderwidth=1, relief="ridge")

# Cadre pour le formulaire de connexion
login_frame = ttk.Frame(main_window, style="Login.TFrame", width=600, height=700, padding=70)
login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Titre de la page
title_label = ttk.Label(login_frame, text="تسجيل الدخول", background="white", foreground="#333", font=('Arial', 20, 'bold'))
title_label.grid(row=0, column=1, pady=10, sticky=N)

# Champ de nom d'utilisateur
username_label = ttk.Label(login_frame, text="اسم المستخدم", background="white")
username_label.grid(row=1, column=1, pady=10, sticky=E)
username_entry = ttk.Entry(login_frame, font=("times new roman", 14), width=30, state="normal")
username_entry.grid(row=2, column=1, pady=10, padx=10, ipady=7)

# Champ de mot de passe
password_label = ttk.Label(login_frame, text="كلمة المرور", background="white")
password_label.grid(row=3, column=1, pady=10, sticky=E)
password_entry = ttk.Entry(login_frame, font=("times new roman", 14), width=30, show="*")
password_entry.grid(row=4, column=1, pady=10, padx=10, ipady=7)

# Bouton de connexion
login_button = Button(
    login_frame,
    text="دخول",
    font=("Helvetica", 14, "bold"),
    bg="#001",
    fg="white",
    activebackground="white",
    activeforeground="black",
    cursor="hand2",
    command=login,
    width=23,
)
login_button.grid(row=5, column=1, columnspan=3, pady=20)

# Pied de page
footer_label = Label(
    main_window,
    text="© 2024 MyApp. All rights reserved.",
    font=("Helvetica", 10),
    bg="white",
    fg="#666",
)
footer_label.place(relx=0.5, rely=0.95, anchor=CENTER)

connect_db()
main_window.mainloop()
