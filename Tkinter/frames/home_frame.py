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
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='sms')
        my_cursor = connect.cursor()
        product_total = connect.cursor()
        category_total = connect.cursor()
        # inventory_total = connect.cursor()
        supplier_total = connect.cursor()
        # messagebox.showinfo('Connection Successful', 'Connected to the database')
        print('Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))
    

def fetch_total(table_name,total_variable):
    query = f'SELECT COUNT(*) FROM {table_name}'
    total_variable.execute(query)
    result = total_variable.fetchone()  # Utiliser fetchone() au lieu de fetchall()
    if result:
        print(result[0])
        return result[0]  # Retourner le premier (et seul) élément du tuple
    return 0  # Retourner 0 si aucun résultat n'est trouvé   

def create_card(parent, title, description, bg="#fff"):
    """Créer une carte simple avec CustomTkinter."""
    card_frame = ctk.CTkFrame(parent, fg_color=bg, corner_radius=10,border_width=1,)

    # Titre de la carte
    title_label = ctk.CTkLabel(card_frame, text=title, 
                            font=ctk.CTkFont(family='Arial',size=14,weight='bold'),)
    title_label.pack(anchor="e", pady=5,ipadx=100,padx=10)

    # Description de la carte
    description_label = ctk.CTkLabel(card_frame, text=description, font=ctk.CTkFont(family='Arial',size=14,weight='bold'), wraplength=200,)
    description_label.pack(anchor="e", pady=5,ipadx=100,padx=10)

    return card_frame


def create_card_with_items(parent, title, items, bg="#fff"):
    """Créer une carte avec sous-cartes contenant des images et des titres."""
    card_frame = ctk.CTkFrame(parent, fg_color=bg, corner_radius=10,border_width=1,)

    # Titre principal de la carte
    title_label = ctk.CTkLabel(card_frame, text=title, font=ctk.CTkFont(family='Arial',size=18,weight='bold'),)
    title_label.pack(anchor="e", pady=10,padx=10,ipadx=75)

    # Conteneur pour les sous-éléments
    items_container = ctk.CTkFrame(card_frame,fg_color=bg, )
    items_container.pack(anchor="e", pady=10,padx=10)

    # Ajout des sous-éléments
    for row_index, (item_title, item_image_path) in enumerate(items):

        image_path = os.path.join(os.path.dirname(__file__), "images", item_image_path)
        
        item_image = ctk.CTkImage(
            light_image=Image.open(image_path),
            size=(25, 25))
        image_label = ctk.CTkLabel(items_container, image=item_image, text="")
        image_label.grid(row=row_index, column=1, padx=10, pady=5, sticky="e")


        # Titre
        title_label = ctk.CTkLabel(items_container, text=item_title, font=ctk.CTkFont(family='Arial',size=14,weight='bold'),)
        title_label.grid(row=row_index, column=0, padx=10, pady=5, sticky="e")

    return card_frame


def create_home_frame(root):
    """Créer le cadre principal contenant toutes les cartes."""
    home_frame = ctk.CTkFrame(root,fg_color='white')
    home_frame.pack(fill='both', expand=True)

    # Conteneur des cartes de la première rangée
    cards_container = ctk.CTkFrame(home_frame,fg_color='#fff')
    cards_container.pack(pady=20)

    # Conteneur des cartes de la deuxième rangée
    cards_container1 = ctk.CTkFrame(home_frame,fg_color='#fff')
    cards_container1.pack(pady=20)
    
    connect_db()
    prods= fetch_total('product',product_total)
    categs = fetch_total('category',category_total)
    inventories = fetch_total('inventorie',product_total)
    suppliers = fetch_total('supplier',supplier_total)
    # print(prods,categs,suppliers)
    # Données des cartes
    card_data = [
        ("الفواتير اليوم", "0"),
        ("المنتجات المنخفضة", "0"),
        ("عدد المنتجات", prods),
        ("المبيعات اليوم", "0"),
    ]

    # Données pour les cartes avec sous-éléments
    card_data2 = [
        ("التقارير", [("إضافة منتج جديد", "add.png"), ("قائمة المنتجات", "list (2).png"), ("تعديل المخزون", "transfer-data.png")]),
        ("المبيعات", [("فاتورة جديدة", "invoice (1).png"), ("قائمة الفواتير", "shopping.png"), ("المرتجعات", "undo.png")]),
        ("المخزون", [("تقرير المبيعات", "computer.png"), ("قائمة المخزون", "raport.png")]),
    ]

    # Ajout des cartes simples
    for title, description in card_data:
        card = create_card(cards_container, title, description)
        card.pack(side="right", padx=5, fill="both",ipady=20,ipadx=50, expand=True)

    # Ajout des cartes avec sous-éléments
    for title, items in card_data2:
        card_with_items = create_card_with_items(cards_container1, title, items)
        card_with_items.pack(side="right", padx=10, fill="both", expand=True, ipadx=160)

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