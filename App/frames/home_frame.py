import customtkinter as ctk
from PIL import Image, ImageTk
import pymysql
import os


def connect_db():
    try:
        # create a connection object
        global connect
        global my_cursor
        global product_total
        global category_total
        global inventory_total
        global supplier_total
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        product_total = connect.cursor()
        category_total = connect.cursor()
        # inventory_total = connect.cursor()
        supplier_total = connect.cursor()
        # messagebox.showinfo('Connection Successful', 'Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
    

def fetch_total(table_name,total_variable):
    query = f'SELECT COUNT(*) FROM {table_name}'
    total_variable.execute(query)
    result = total_variable.fetchone()  # Utiliser fetchone() au lieu de fetchall()
    if result:
        return result[0]  # Retourner le premier (et seul) élément du tuple
    return 0  # Retourner 0 si aucun résultat n'est trouvé   

def create_card(parent, title, description, color):
    """Créer une carte simple avec CustomTkinter."""
    card_frame = ctk.CTkFrame(parent, fg_color='#fff',bg_color='#fff', corner_radius=1,border_width=1,border_color='#e2e2e2')

    # Titre de la carte
    title_label = ctk.CTkLabel(card_frame, text=title, 
                            font=('Arial',18,'bold'),anchor='e', )
    title_label.pack( pady=5,ipadx=100,padx=10,anchor="ne")

    # Description de la carte
    description_label = ctk.CTkLabel(card_frame, text=description,
                                    font=('Arial',18,'bold'), text_color=color,anchor="e")
    description_label.pack( pady=5,ipadx=100,padx=10,anchor="ne")

    return card_frame


def create_card_with_items(parent, title, items, bg="#fff"):
    """Créer une carte avec sous-cartes contenant des images et des titres."""
    card_frame = ctk.CTkFrame(parent, fg_color='#fff',bg_color='#fff', corner_radius=1,border_width=1,border_color='#e2e2e2')

    # Titre principal de la carte
    title_label = ctk.CTkLabel(card_frame, text=title, font=('Arial',18,'bold'),fg_color='#f9f9f9',anchor='e')
    title_label.pack(pady=(10,2),padx=20,fill='x')

    # Conteneur pour les sous-éléments
    items_container = ctk.CTkFrame(card_frame,fg_color=bg, )
    items_container.pack(anchor="e", pady=10,padx=10,expand=True,fill='both')

    
    # Ajout des sous-éléments
    for row_index, (item_title, item_image_path) in enumerate(items):
        item_container = ctk.CTkFrame(items_container,fg_color=bg, border_width=1, border_color='#f0f0f0', corner_radius=1)
        item_container.pack(padx=10,expand=True,fill='both')
        item_container.columnconfigure((0),weight=1, uniform = 'a')

        image_path = os.path.join(os.path.dirname(__file__), "images", item_image_path)
        
        item_image = ctk.CTkImage(
            light_image=Image.open(image_path),
            size=(22, 22))
        image_label = ctk.CTkLabel(item_container, image=item_image, text="")
        image_label.grid(row=row_index, column=2, padx=10, pady=5, sticky="nesw")


        # Titre
        title_label = ctk.CTkLabel(item_container, text=item_title, font=('Arial',14),)
        title_label.grid(row=row_index, column=1, padx=10, pady=5, sticky="nesw")

    return card_frame


def create_home_frame(root):
    """Créer le cadre principal contenant toutes les cartes."""
    home_frame = ctk.CTkFrame(root,fg_color='white')
    home_frame.pack(fill='both', expand=True)

    # Conteneur des cartes de la première rangée
    cards_container = ctk.CTkFrame(home_frame,fg_color='#fff')
    cards_container.pack(pady=20,fill='x',padx=10)

    # Conteneur des cartes de la deuxième rangée
    cards_container1 = ctk.CTkFrame(home_frame,fg_color='#fff')
    cards_container1.pack(pady=20,fill='x',padx=10)
    
    connect_db()
    prods= fetch_total('products',product_total)
    # categs = fetch_total('product_categories',category_total)
    # inventories = fetch_total('inventorie',product_total)
    # suppliers = fetch_total('suppliers',supplier_total)
    # Données des cartes
    card_data = [
        ("الفواتير اليوم", "0",'#08fbfb'),
        ("المنتجات المنخفضة", "0",'#b3cb18'),
        ("عدد المنتجات", prods, '#2ca12c'),
        ("المبيعات اليوم", "0",'#2972d6'),
    ]

    # Données pour les cartes avec sous-éléments
    card_data2 = [
        ("المخزون  ", [("إضافة منتج جديد", "add.png"), ("قائمة المنتجات", "list (2).png"), ("تعديل المخزون", "transfer-data.png")]),
        (" المبيعات  ", [("فاتورة جديدة", "invoice (1).png"), ("قائمة الفواتير", "shopping.png"), ("المرتجعات", "undo.png")]),
        ("التقارير  ", [("تقرير المبيعات", "computer.png"), ("قائمة المخزون", "raport.png")]),
    ]

    # Ajout des cartes simples
    for title, description,color in card_data:
        card = create_card(cards_container, title, description,color)
        card.pack(side="left", padx=5, fill="both",ipady=20, expand=True)

    # Ajout des cartes avec sous-éléments
    for title, items in card_data2:
        card_with_items = create_card_with_items(cards_container1, title, items)
        card_with_items.pack(side="right", padx=10,expand=True,anchor="n",fill='x')

    return home_frame



# window 
# window = ctk.CTk(fg_color="#fff")
# window.title('customtkinter app')
# window.geometry('1200x550')
# window.state('zoomed')

# home_frame = create_home_frame(window)
# home_frame.pack(fill='both', expand=True)

# # run
# window.mainloop()