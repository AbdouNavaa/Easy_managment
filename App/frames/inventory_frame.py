import customtkinter as ctk
from tkinter import messagebox
import pymysql

def create_inventory_frame(root,user=None):
    inventory_frame = ctk.CTkFrame(root, fg_color="#fff")
    ctk.CTkLabel(inventory_frame, text="المخزون", bg_color='#fff', font=("Arial", 20)).pack(pady=20)
    return inventory_frame
# if __name__ == "__main__":
#     # ctk.set_appearance_mode("dark")  # Modes: "dark", "light"
#     # ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

#     root = ctk.CTk()
#     root.title("Dashboard")
#     root.geometry("800x500")

#     inventory_frame = create_inventory_frame(root)
#     inventory_frame.pack(fill='both', expand=True)

#     root.mainloop()
