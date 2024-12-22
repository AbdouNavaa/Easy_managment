from tkinter import messagebox
from ttkthemes import ThemedTk
import pymysql
import ttkbootstrap as ttk


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


# Function to show products as a styled table (without Treeview)
def show_products_table(parent):
    connect_db()
    query = 'SELECT * FROM product'
    my_cursor.execute(query)
    data = my_cursor.fetchall()

    # Columns of the table
    columns = ('ID', 'Name', 'Description', 'Price', 'Stock', 'Category', 'Supplier')
    # je veux inverser cette label
    columns = columns[::-1]

    # Frame for the table header
    header_frame = ttk.Frame(parent, height=50)
    header_frame.pack(fill='x', padx=20, pady=2)

    # Add column headings
    for col_index, col_name in enumerate(columns):
        label = ttk.Label(header_frame, text=col_name, font=("Arial", 15, "bold"), anchor="center", 
                          bootstyle="deafult", width=100,background="#333", foreground="white")
        label.grid(row=0, column=col_index, sticky="nsew", padx=2, pady=2)

    # Frame for the table data
    data_frame = ttk.Frame(parent)
    data_frame.pack(fill='both', expand=True, padx=20, pady=2)

    # Add data rows
    for row_index, row in enumerate(data):
        row = row[::-1]  # Reverse the row data = data[::-1]
        
        for col_index, value in enumerate(row):
            label = ttk.Label(data_frame, text=value, font=("Arial", 12),  anchor="center", 
                          bootstyle="deafult", width=100,background="#fff" )
            label.grid(row=row_index, column=col_index, sticky="nesw", padx=2, pady=2,ipady=5)

    # Configure column weights for responsiveness
    for col_index in range(len(columns)):
        header_frame.grid_columnconfigure(col_index, weight=1)
        data_frame.grid_columnconfigure(col_index, weight=1)


# Function to create the products frame
def create_products_frame(root):
    products_frame = ttk.Frame(root, bootstyle='default')
    ttk.Label(products_frame, text="منتجاتنا", font=("Arial", 20), bootstyle='info').pack(pady=20)

    show_products_table(products_frame)
    return products_frame


# Example usage
if __name__ == "__main__":
    root = ThemedTk(theme="cerculean")
    root.title("Product Management")
    root.state("zoomed")

    products_frame = create_products_frame(root)
    products_frame.pack(fill='both', expand=True)

    root.mainloop()
