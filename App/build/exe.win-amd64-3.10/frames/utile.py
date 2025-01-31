import json
from tkinter import messagebox
import pymysql

def load_user_data():
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return messagebox.showinfo("Alerte", "l'utilisateur n'est pas connecté ")
    
def connect_db():
    try:
        global connect
        global my_cursor
        global categories
        global warehouses
        global suppliers
        connect = pymysql.connect(host='localhost', user='root', password='Azerty2024', database='easy_db')
        my_cursor = connect.cursor()
        categories = connect.cursor()
        warehouses = connect.cursor()
        suppliers = connect.cursor()
        return connect
    except Exception as e:
        messagebox.showerror('Connection Failed', str(e))