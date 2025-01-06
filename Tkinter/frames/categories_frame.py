import customtkinter as ctk
from tkinter import messagebox
import pymysql


# Connection settings
def connect_db():
    try:
        global connect
        global my_cursor
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='sms')
        my_cursor = connect.cursor()
        print('Connected to the database')
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))


# Function to fetch categories with pagination
def fetch_categories(limit=10, offset=0):
    connect_db()
    query = f'SELECT * FROM category LIMIT {limit} OFFSET {offset}'
    my_cursor.execute(query)
    return my_cursor.fetchall()


# Function to show categories as a styled table with pagination
def show_categories_table(parent, limit=10):
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
        data = fetch_categories(limit, offset)

        # Add data rows
        for row_index, row in enumerate(data):
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
                
                prods_num = ctk.CTkLabel(
                    data_frame,
                    text='0',
                    font=ctk.CTkFont(size=12),
                    text_color="#333",
                    fg_color="#fff",
                    corner_radius=5,
                    width=100
                )
                prods_num.grid(row=row_index, column=0, sticky="nsew", padx=5, pady=5)
                label.grid(row=row_index, column=col_index+1, sticky="nsew", padx=5, pady=5)
                

    offset = 0

    # Table headers
    columns = ('القطعة رقم ', 'الاسم ', 'الوصف', 'المنتجات عدد')
    # columns = ('القطعة رقم ', 'الاسم ', 'الوصف', 'المنتجات عدد',  'الإجراءات')
    columns = columns[::-1]

    # Header frame
    header_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="#333")
    header_frame.pack(fill='x', padx=20, pady=5)
    header_frame.columnconfigure((0, 1, 2,3), weight=1, uniform='a')
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
    data_frame.columnconfigure((0, 1,2, 3), weight=1, uniform='a')
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
        text="المنتجات فئات",
        font=ctk.CTkFont(size=20, weight="bold"),
        # text_color="#0066cc"
        compound="right"
    )
    title_label.grid(row=0, column=5,columnspan=3, padx=5, pady=5,sticky="e")
    
    # add 3 button 
    add_inventory_button = ctk.CTkButton(
        master=title_frame,
        text="  فئة جديدة اضافة  ",
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color="#2498f5",
        text_color="#333",
        hover_color="#f0f0f0",
        corner_radius=5,
        command=lambda: messagebox.showinfo("اضافة فئة", "يمكنك اضافة فئة جديدة من خلال هذه الخاصية")
    )
    add_inventory_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)


    
    

# Function to create the categories frame
def create_categories_frame(root):
    categories_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#fff")

    show_title_frame(categories_frame)

    show_categories_table(categories_frame)
    return categories_frame


# Example usage
# if __name__ == "__main__":
#     root = ctk.CTk()
#     root.title("Product Management")
#     root.geometry("1200x800")
#     # root.option_add()
    
#     categories_frame = create_categories_frame(root)
#     categories_frame.pack(fill='both', expand=True)

#     root.mainloop()
