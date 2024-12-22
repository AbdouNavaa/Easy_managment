# create_suppliers_frame
import tkinter as tk

def create_suppliers_frame(root):
    suppliers_frame = tk.Frame(root, bg="#fff")
    tk.Label(suppliers_frame, text=" الموردين", background='#fff', font=("Arial", 20)).pack(pady=20)
    return suppliers_frame