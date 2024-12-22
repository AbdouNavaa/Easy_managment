import tkinter as tk

def create_categories_frame(root):
    categories_frame = tk.Frame(root, bg="#fff")
    tk.Label(categories_frame, text="الاقسام", background='#fff', font=("Arial", 20)).pack(pady=20)
    return categories_frame
