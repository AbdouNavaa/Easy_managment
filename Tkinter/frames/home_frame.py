import tkinter as tk
from ttkbootstrap import ttk


def create_card(parent, title, description, bg="#fff"):
    """Créer une carte simple."""
    card_frame = tk.Frame(parent, bg=bg, bd=1, relief="solid", width=300, padx=90, pady=20)

    # Titre de la carte
    tk.Label(card_frame, text=title, font=("Arial", 14, "bold"), bg=bg).pack(anchor="e", pady=5)

    # Description de la carte
    tk.Label(card_frame, text=description, font=("Arial", 10), bg=bg, wraplength=200).pack(anchor="e")

    return card_frame


def create_card_with_items(parent, title, items, bg="#fff"):
    """Créer une carte avec une sous-carte contenant une image et un titre."""
    card_frame = tk.Frame(parent, bg=bg, bd=1, relief="solid", padx=10, pady=10)

    # Titre principal de la carte
    tk.Label(card_frame, text=title, font=("Arial", 14, "bold"), bg=bg).pack(anchor="e", pady=10)

    # Conteneur pour les sous-éléments
    items_container = tk.Frame(card_frame, bg='#fff')
    items_container.pack(anchor="e",  pady=10,)
    # items_container.pack(anchor="e",  pady=10, fill="x",side='right',expand=True)

    # Configuration de la grille pour un alignement uniforme
    for row_index, (item_title, item_image_path) in enumerate(items):
        # Image
        item_image = tk.PhotoImage(file=item_image_path).subsample(3, 3)  # Réduire la taille de l'image
        image_label = tk.Label(items_container, image=item_image, bg='#fff')
        image_label.image = item_image  # Empêche la suppression de l'image
        image_label.grid(row=row_index, column=1, padx=10, pady=5, sticky="e")

        # Titre
        tk.Label(items_container, text=item_title, font=("Arial", 10), bg='#fff').grid(
            row=row_index, column=0, padx=10, pady=5, sticky="e",
        )
        
    return card_frame


def create_home_frame(root):
    home_frame = tk.Frame(root, bg="#fff")

    # Conteneur des cartes
    cards_container = tk.Frame(home_frame, bg="#fff")
    cards_container.pack(pady=20)

    cards_container1 = tk.Frame(home_frame, bg="#fff")
    cards_container1.pack(pady=20)
    # Liste des données pour les cartes de la première ligne
    card_data = [
        ("الفواتير اليوم", "0"),
        ("المنتجات المنخفضة", "0"),
        ("عدد المنتجات", "0"),
        ("المبيعات اليوم", "0"),
    ]

    # Liste des données pour les cartes de la deuxième ligne (avec sous-cartes)
    card_data2 = [
        ("المخزون", [("تقرير المبيعات ", "computer.png"), ("قائمة المخزون ", "raport.png")]),
        ("المبيعات", [("فاتورة جديدة", "invoice (1).png"), ("قائمة الفواتير ", "shopping.png"), (" المرتجعات", "undo.png")]),
        ("التقارير", [("اضافة منتج جديد ", "add.png"), ("قائمة المنتجات ", "list (2).png"), (" تعديل المخزون", "transfer-data.png")]),
    ]

    # Création et placement des cartes de la première ligne
    for i, (title, description) in enumerate(card_data):
        card = create_card(cards_container, title, description)
        card.pack( side="right", padx=10,fill='both',expand=True,)

    # Création et placement des cartes de la deuxième ligne
    for i, (title, items) in enumerate(card_data2):
        card1 = create_card_with_items(cards_container1, title, items)
        card1.pack( side="right", padx=10,fill='both',expand=True,ipadx=110,)
        # card1.grid(row=i // 3, column=i +1, padx=10, pady=10, sticky="nsew",ipadx=67,ipady=10)

    return home_frame


# Fenêtre principale
# root = tk.Tk()
# root.title("Exemple de cartes")
# root.state("zoomed")

# # Création du cadre Home
# home_frame = create_home_frame(root)
# home_frame.pack(fill="both", expand=True)

# root.mainloop()
