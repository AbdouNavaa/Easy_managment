# create_inventory_frame
import tkinter as tk

def create_inventory_frame(root):
    inventory_frame = tk.Frame(root, bg="#fff")
    tk.Label(inventory_frame, text="المخزون", background='#fff', font=("Arial", 20)).pack(pady=20)
    return inventory_frame