import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as  ttk
import customtkinter as ctk
from PIL import Image, ImageTk
# Importation des frames
from frames.home_frame import create_home_frame
from frames.products_frame import create_products_frame
from frames.categories_frame import create_categories_frame
from frames.add_product_frame import create_add_product_frame
from frames.suppliers_frame import create_suppliers_frame
from frames.inventory_frame import create_inventory_frame

def show_frame(frame):
    # Masquer tous les cadres
    for f in all_frames:
        f.pack_forget()
    # Afficher le cadre sélectionné
    frame.pack(fill="both", expand=True)

def show_subsection(section):
    print(f"Affichage de la sous-section : {section}")

# Fenêtre principale
# Configuration principale de l'application
ctk.set_appearance_mode("dark")  # Modes: "dark", "light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# Fenêtre principale
root = ctk.CTk()
root.title("Product Management")
root.state("zoomed")

# Barre de navigation
navbar = ttk.Frame(root,  height=50,bootstyle="dark")
navbar.pack(fill="x")

# Création des frames
home_frame = create_home_frame(root)
products_frame = create_products_frame(root)
categories_frame = create_categories_frame(root)
add_product_frame = create_add_product_frame(root)
# add_product_frame.pack(fill="x",side='right')
suppliers_frame = create_suppliers_frame(root)
inventory_frame = create_inventory_frame(root)

all_frames = [home_frame, products_frame, categories_frame, add_product_frame, suppliers_frame, inventory_frame]

# Labels de navigation avec menus déroulants
navbar_font = ("Arial", 14, "bold")

home_label = ttk.Label(navbar, text="الرئيسية", bootstyle="inverse-dark",font=navbar_font, cursor="hand2")
home_label.pack(side="right", padx=20, pady=10)
home_label.bind("<Button-1>", lambda e: show_frame(home_frame))

# dropdown_style = ttk.Style()
# dropdown_style.configure("TMenubutton", background="#333", foreground="white", font=navbar_font,focuscolor="#333")

dropdown_style = ttk.Style()
dropdown_style.configure(
    "TMenubutton",
    background="#333",  # Couleur de fond
    foreground="white",  # Couleur du texte
    font=("Arial", 12, "bold"),  # Police
    padding=5,  # Espacement interne
    relief="flat"  # dropdown_style de bordure
)
dropdown_style.map(
    "TMenubutton",
    background=[("active", "#333"),("pressed", "#333"),("focus", "#333")],  # Couleur quand actif
    foreground=[("focus", "red")]  # Texte grisé quand désactivé
)

# Dropdown pour Produits
products_menu_button = ttk.Menubutton(navbar, text="المنتجات", bootstyle="dark",takefocus=True)
products_menu = tk.Menu(products_menu_button, tearoff=0, bg="#fff", fg="black")
products_menu.add_command(label="قائمة المنتجات", command=lambda: show_frame(products_frame))
products_menu.add_command(label="منتج اضافة", command=lambda: show_frame(add_product_frame))
products_menu_button["menu"] = products_menu
products_menu_button.pack(side="right", padx=20, pady=10)

# Dropdown pour Catégories
categories_menu_button = ttk.Menubutton(navbar, text="الأقسام", bootstyle="dark")
categories_menu = tk.Menu(categories_menu_button, tearoff=0, bg="#fff", fg="black")
categories_menu.add_command(label="المنتجات", command=lambda: show_frame(products_frame))
categories_menu.add_command(label="الفئات", command=lambda: show_frame(categories_frame))
categories_menu.add_command(label="الموردين", command=lambda: show_frame(suppliers_frame))
categories_menu.add_command(label="تعديلات المخزون", command=lambda: show_frame(inventory_frame))
categories_menu_button["menu"] = categories_menu
categories_menu_button.pack(side="right", padx=20, pady=10)

# Afficher le cadre par défaut
show_frame(home_frame)

root.mainloop()
