import customtkinter as ctk
from PIL import Image, ImageTk
import pymysql
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def connect_db():
    try:
        # create a connection object
        global connect
        global my_cursor
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))

def fetch_total(total_variable, table_name):
    query = f'SELECT COUNT(*) FROM {table_name}'
    total_variable.execute(query)
    result = total_variable.fetchone()
    if result:
        return result[0]
    return 0

def fetch_law_prod():
    query = "select count(*) from products where min_quantity > quantity"
    my_cursor.execute(query)
    result = my_cursor.fetchone()
    if result:
        return result[0]
    return 0

def fetch_daily_sales():
    query = "SELECT count(*) FROM sales WHERE DATE(date) = CURDATE()"
    my_cursor.execute(query)
    result = my_cursor.fetchone()
    if result:
        return result[0]
    return 0

def fetch_sales_data():
    """Récupérer les données de la table sales pour le graphique en ligne."""
    query ='''SELECT DATE(s.date),
    sum(si.subtotal)
    from sales s 
    LEFT JOIN sale_items si ON s.id = si.sale_id
    GROUP BY date(s.date)'''
    my_cursor.execute(query)
    result = my_cursor.fetchall()
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dates = [row[0].strftime('%Y-%m-%d') for row in result]
    amounts = [row[1] for row in result]
    print('amounts:',amounts,'date:',dates,'result:',result)
    return dates, amounts

def fetch_warehouse_data():
    """Récupérer le nombre de produits par entrepôt pour le graphique à barres."""
    query = """
    SELECT w.name, COUNT(p.id) 
    FROM warehouses w 
    LEFT JOIN products p ON w.id = p.warehouse_id 
    GROUP BY w.name
    """
    my_cursor.execute(query)
    result = my_cursor.fetchall()
    warehouses = [row[0] for row in result]
    product_counts = [row[1] for row in result]
    return warehouses, product_counts

def create_card(parent, title, description, color):
    """Créer une carte simple avec CustomTkinter."""
    card_frame = ctk.CTkFrame(parent, fg_color='#fff', bg_color='#fff', corner_radius=8, border_width=1, border_color='#f0f0f0')

    # Titre de la carte
    title_label = ctk.CTkLabel(card_frame, text=title, font=('Arial', 18, 'bold'), anchor='e')
    title_label.pack(pady=5, ipadx=100, padx=10, anchor="center")

    # Description de la carte
    description_label = ctk.CTkLabel(card_frame, text=description, font=('Arial', 18, 'bold'), text_color=color, anchor="e")
    description_label.pack(pady=5, ipadx=100, padx=10, anchor="center")

    return card_frame

def create_graph_frame(parent, title, x_data, y_data, labels=None, colors=None, graph_type='bar'):
    """Créer un cadre avec un graphique."""
    card_frame = ctk.CTkFrame(parent, fg_color='#fff', bg_color='#fff', corner_radius=1)

    # Titre de la carte
    title_label = ctk.CTkLabel(card_frame, text=title, font=('Arial', 18, 'bold'))
    title_label.pack(pady=5, ipadx=100, padx=10, anchor="center")

    # Création du graphique
    fig, ax = plt.subplots()
    if graph_type == 'bar':
        ax.bar(x_data, y_data, color=colors)
        ax.set_xticks(range(len(x_data)))
        ax.set_xticklabels(labels, rotation=45)
    elif graph_type == 'line':
        ax.plot(x_data, y_data, marker='o', color=colors[0])
        ax.set_xticks(range(len(x_data)))
        ax.set_xticklabels(x_data, rotation=45)
    # ax.set_title(title)

    # Intégration du graphique dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=card_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=False)

    return card_frame


law_product = 0
daily_sale = 0
prods = 0
warehouses = 0
sales_dates = []
sales_amounts = []
product_counts = []
warehouse_names = []

def refresh_data():

    """Rafraîchir les données affichées."""
    global law_product, daily_sale, prods, warehouses, sales_dates, sales_amounts,warehouse_names, product_counts

    # Se connecter à la base de données et récupérer les données
    connect_db()
    law_product = fetch_law_prod()
    daily_sale = fetch_daily_sales()
    prods = fetch_total(my_cursor, 'products')
    warehouses = fetch_total(my_cursor, 'warehouses')
    print('warehouses:',warehouses)
    # Récupérer les données pour les graphiques
    sales_dates, sales_amounts = fetch_sales_data()
    warehouse_names, product_counts = fetch_warehouse_data()

def refresh_data1(cards_cont1, cards_cont2):
    
    for widget in cards_cont1.winfo_children():
            widget.destroy()

    for widget in cards_cont2.winfo_children():
            widget.destroy()
    connect_db()
    new_law_product = fetch_law_prod()
    new_daily_sale = fetch_daily_sales()
    new_prods = fetch_total(my_cursor, 'products')
    new_warehouses = fetch_total(my_cursor, 'warehouses')
    print('warehouses2:',warehouses)
    # Récupérer les données pour les graphiques
    sales_dates, sales_amounts = fetch_sales_data()
    warehouse_names, product_counts = fetch_warehouse_data()   
    
    card_data = [
        ("المخازن ", new_warehouses, '#08d1fb'),
        ("المنتجات المنخفضة", new_law_product, '#b3cb18'),
        ("عدد المنتجات", new_prods, '#2ca12c'),
        ("المبيعات اليوم", new_daily_sale, '#2972d6'),
    ]
    for title, description, color in card_data:
        card = create_card(cards_cont1, title, description, color)
        card.pack(side="left", padx=10, fill="both", ipady=20, expand=True)
        
    sales_graph = create_graph_frame(cards_cont2, "المبيعات", sales_dates, sales_amounts, colors=['#2972d6'],labels=sales_dates, graph_type='line')
    sales_graph.pack(side="left", padx=10, fill="both", expand=True)

    warehouse_graph = create_graph_frame(cards_cont2, "المنتجات بالمخازن", warehouse_names, product_counts, labels=warehouse_names, colors=['#08d1fb', '#b3cb18', '#2ca12c'], graph_type='bar')
    warehouse_graph.pack(side="left", padx=10, fill="both", expand=True)

    # refresh_data()

def create_home_frame(root):
    """Créer le cadre principal contenant toutes les cartes."""
    # Rafraîchir les données avant de créer le frame
    refresh_data()
    # refresh_data1()

    home_frame = ctk.CTkFrame(root, fg_color='white')
    home_frame.pack(fill='both', expand=True)

    # Conteneur des cartes de la première rangée
    ref_container = ctk.CTkFrame(home_frame, fg_color='#fff',height=30)
    ref_container.pack(pady=2, fill='x', padx=10)
    
    cards_container = ctk.CTkFrame(home_frame, fg_color='#fff')
    cards_container.pack(pady=20, fill='x', padx=10)

    # Conteneur des cartes de la deuxième rangée
    cards_container1 = ctk.CTkFrame(home_frame, fg_color='#fff')
    cards_container1.pack(pady=20, fill='x', padx=10)

    # Données des cartes
    card_data = [
        ("المخازن ", warehouses, '#08d1fb'),
        ("المنتجات المنخفضة", law_product, '#b3cb18'),
        ("عدد المنتجات", prods, '#2ca12c'),
        ("المبيعات اليوم", daily_sale, '#2972d6'),
    ]

    # Ajout des cartes simples
    image_path = os.path.join(os.path.dirname(__file__), "images", "refresh.png")
    
    image = ctk.CTkImage(light_image=Image.open(image_path), size=(20, 20),)

    refresh_button = ctk.CTkButton(
        ref_container,
        image=image,
        text="تحديث",
        fg_color="#fff",
        hover_color="#f0f0f0",
        font=('Arial',18),corner_radius=2,
        width=50,
        text_color="#333",
        command=lambda: refresh_data1(cards_container,cards_container1),compound="left"
    )
    
    refresh_button.pack(side="left", padx=10, fill="x", ipady=10)
    for title, description, color in card_data:
        card = create_card(cards_container, title, description, color)
        card.pack(side="left", padx=10, fill="both", ipady=20, expand=True)

    # Ajout des graphiques
    # print("\n================================",sales_dates,sales_amounts)
    # print("\n================================",warehouse_names,product_counts)
    sales_graph = create_graph_frame(cards_container1, "المبيعات", sales_dates, sales_amounts, colors=['#2972d6'],labels=sales_dates, graph_type='line')
    sales_graph.pack(side="left", padx=10, fill="both", expand=True)

    warehouse_graph = create_graph_frame(cards_container1, "المنتجات بالمخازن", warehouse_names, product_counts, labels=warehouse_names, colors=['#08d1fb', '#b3cb18', '#2ca12c'], graph_type='bar')
    warehouse_graph.pack(side="left", padx=10, fill="both", expand=True)

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