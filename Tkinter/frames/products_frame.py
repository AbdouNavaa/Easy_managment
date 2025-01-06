import customtkinter as ctk
from tkinter import messagebox
import pymysql


# Connection settings
def connect_db():
    try:
        global connect
        global my_cursor
        global categories
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='sms')
        my_cursor = connect.cursor()
        categories = connect.cursor()
        print('Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))


# Function to fetch products with pagination
def fetch_products(limit=10, offset=0):
    connect_db()
    query = f'SELECT id,p.name,p.description,p.price,p.price_before,s.name,p.quantity FROM product p JOIN supplier s ON p.supplier = s.s_id  LIMIT {limit} OFFSET {offset}'
    my_cursor.execute(query)
    return my_cursor.fetchall()


def delete_product (product_id,parent):
    connect_db()
    print('PID', product_id)
    query = f"DELETE FROM product WHERE id = {product_id}"
    my_cursor.execute(query)
    connect.commit()
    messagebox.showinfo('Success', 'Product deleted successfully')
    connect_db()
    fetch_products()
    
    # parent.destroy()
    # show_products_table(parent)
# Function to show products as a styled table with pagination
def show_products_table(parent, limit=10):
    def load_page(page_num):
        nonlocal offset
        print(page_num)
        offset = (page_num - 1) * limit
        print(offset)
        update_table()

    def update_table():
        # Clear previous table data
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Fetch new data
        print("Offest: ",offset)
        data = fetch_products(limit, offset)

        # Add data rows
        for row_index, row in enumerate(data):
            row1 = row
            row = row[::-1]  # Reverse the row data
            for col_index, value in enumerate(row):
                label = ctk.CTkLabel(
                    data_frame,
                    text=value,
                    font=ctk.CTkFont(size=12),
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                label.grid(row=row_index, column=col_index+1, sticky="nsew", padx=5, pady=5)
                
                buttons_frame = ctk.CTkFrame(data_frame, width=100,height=40,fg_color="#fff"
                                        # command=lambda row=row: show_supplier_details(row)
                                        ) 
                buttons_frame.grid(row=row_index , column=0, sticky="nsew", padx=5, pady=5)
                update_button = ctk.CTkButton(buttons_frame, text="تعديل",fg_color="#333",font=ctk.CTkFont(size=12),width=62,)
                update_button.grid(row=0,column=1)
                delete_button = ctk.CTkButton(buttons_frame, text="حذف",fg_color="#333",font=ctk.CTkFont(size=12),width=62,
                        command=lambda row=row1: delete_product(row1[0],parent))
                delete_button.grid(row=0,column=0,padx=5)

    offset = 0

    # Table headers
    columns = ('القطعة رقم ', 'المنتج اسم ', 'الوصف', 'السعر', 'الاولي السعر', 'المورد', 'الكمية','الاجراءات')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="#333")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((0, 1, 2,3, 4, 5, 6,7), weight=1, uniform='a')
    # header_frame.columnconfigure(2, weight=2)

    # Add column headings
    for col_index, col_name in enumerate(columns):
        label = ctk.CTkLabel(
            header_frame,
            text=col_name,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="white",
            fg_color="#444",
            corner_radius=5,
            width=100
        )
        label.grid(row=0, column=col_index, sticky="nsew", padx=5, pady=5)
        

    # Data frame
    data_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="#f9f9f9")
    data_frame.pack(fill='both', expand=True, padx=20, pady=5)
    data_frame.columnconfigure((0, 1,2, 3, 4, 5, 6,7), weight=1, uniform='a')
    # data_frame.columnconfigure(2, weight=2, uniform='a')

    # Pagination controls
    nav_frame = ctk.CTkFrame(parent, fg_color="#fff")
    nav_frame.pack(fill='x', pady=10)

    prev_button = ctk.CTkButton(
        nav_frame,
        text="Previous",
        command=lambda: load_page(max(1, (offset // limit))),
        state="normal" if offset > 0 else "disabled"
    )
    prev_button.pack(side="left", padx=10)

    next_button = ctk.CTkButton(
        nav_frame,
        text="Next",
        command=lambda: load_page((offset // limit) + 2)
    )
    next_button.pack(side="right", padx=10)

    update_table()

# add Prod
def add_product():
    root.destroy()
    import add_product_frame
def fetch_total(total_variable,myList):
    query = f'SELECT * FROM category'
    total_variable.execute(query)
    # print('ffdfd:', total_variable.fetchall())
    result = total_variable.fetchall()  # Utiliser fetchone() au lieu de fetchall()
    # if result:
    for variable in result:
        
        print(variable[1])
        myList.append(variable[1])
        # return variable[1]  # Retourner le premier (et seul) élément du tuple
    print(myList)
    return myList  # Retourner 0 si aucun résultat n'est trouvé   

 
def show_title_frame(parent, ):
    
    # Table headers

    # Header frame
    title_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="transparent",)
    title_frame.pack(fill='x', padx=20, pady=5,)
    # title_frame.configure(direction="rtl")
    
    # title_frame.configure('tag-right', justify='right')
    # title_frame.insert('end', 'text ' * 10, 'tag-right')
    title_frame.columnconfigure((0, 1, 2,3, 4, 5, 6), weight=1, uniform='a',)
    # title_frame.columns = 
    # title_frame.columns[::-1]
    
    title_label = ctk.CTkLabel(
        master=title_frame,
        text="المنتجات ادارة",
        font=ctk.CTkFont(size=20, weight="bold"),
        # text_color="#0066cc"
        compound="right"
    )
    title_label.grid(row=0, column=5,columnspan=3, padx=5, pady=5,sticky="e")
    
    # add 3 button 
    # add_product_button = ctk.CTkButton(
    #     master=title_frame,
    #     text="اضافة منتج",
    #     font=ctk.CTkFont(size=12, weight="bold"),
    #     fg_color="#2498f5",
    #     text_color="#333",
    #     hover_color="#f0f0f0",
    #     corner_radius=5,
    #     command=add_product
    # )
    # # add_product_button.pack(pady=10,anchor="e",padx=(10,40),)

    # add_product_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    # add 3 button 
    export_button = ctk.CTkButton(
        master=title_frame,
        text=" Excel تصدير إلى ",
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color="#3eecfa",
        text_color="#333",
        hover_color="#f0f0f0",
        corner_radius=5,
        command=lambda: messagebox.showinfo("ا��افة منتج", "يمكنك ا��افة منتج ��ديد من خلال هذه الخا��ية")
    )
    # export_button.pack(pady=10,anchor="e",padx=(10,40),)

    export_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    import_button = ctk.CTkButton(
        master=title_frame,
        text=" Excel استيراد من ",
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color="#09d666",
        text_color="#333",
        hover_color="#f0f0f0",
        corner_radius=5,
        command=lambda: messagebox.showinfo("ا��افة منتج", "يمكنك ا��افة منتج ��ديد من خلال هذه الخا��ية")
    )
    # import_button.pack(pady=10,anchor="e",padx=(10,40),)

    import_button.grid(row=0, column=1, sticky="e", padx=5, pady=5)

    
def search_frame(parent, ):

    # Table headers

    # Header frame
    search_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white",)
    search_frame.pack(fill='x', padx=20, pady=5,)
    
    search_frame.columnconfigure((0, 1, 2,3), weight=1, uniform='a',)
    
    search_entry = ctk.CTkEntry(search_frame, placeholder_text="إبحث عن منتج", fg_color="white", bg_color="white",
                    border_color="#e5e3e0",border_width=1,
                    width=300, corner_radius=5,font=ctk.CTkFont(size=12, weight="bold"),)
    search_entry.grid(row=0, column=3, padx=5, pady=5,sticky="e")
    
    connect_db()
    myList = []
    fetch_total(categories, myList)
    optionmenu_var = ctk.StringVar(value="الاقسام كل")
    optionmenu = ctk.CTkOptionMenu(search_frame,values=myList,text_color="#333",dropdown_fg_color="#fff",
                        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",
                        # command=optionmenu_callback,
                        variable=optionmenu_var)
    optionmenu.grid(row=0, column=2, sticky="e", padx=5, pady=5)

    inventory_var = ctk.StringVar(value="المخزون")
    inventoryMenu = ctk.CTkOptionMenu(search_frame,values=["المخزون","inventory 1", "inventory 2"],text_color="#333",dropdown_fg_color="#fff",
                        button_color="white",fg_color="white",dropdown_hover_color="#f0f0f0",
                        # command=inventorymenu_callback,
                        variable=inventory_var)
    inventoryMenu.grid(row=0, column=1, sticky="e", padx=5, pady=5)
    


    
    

# Function to create the products frame
def create_products_frame(root):
    products_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

    show_title_frame(products_frame)
    search_frame(products_frame)

    show_products_table(products_frame)
    return products_frame


# Example usage
# if __name__ == "__main__":
#     root = ctk.CTk()
#     root.title("Product Management")
#     root.geometry("1200x800")
#     # root.option_add()
    
#     products_frame = create_products_frame(root)
#     products_frame.pack(fill='both', expand=True)

#     root.mainloop()
