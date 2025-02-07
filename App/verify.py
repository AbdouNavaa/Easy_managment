import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

# Chemin du fichier contenant les codes de licence
LICENSE_FILE = "licenses.txt"

def load_license_codes():
    """Charge les codes de licence depuis le fichier."""
    try:
        with open(LICENSE_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier de licence introuvable.")
        return []

def verify_license(entered_code):
    """Vérifie si le code entré est valide."""
    license_codes = load_license_codes()
    return entered_code in license_codes

def create_home_frame(parent, app):
    """Crée la frame d'accueil avec la vérification de licence."""
    home_frame = ctk.CTkFrame(parent, fg_color="white")

    # Titre
    title_label = ctk.CTkLabel(home_frame, text="Page d'Accueil", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

    # Champ pour entrer le code de licence
    license_label = ctk.CTkLabel(home_frame, text="Entrez le code de licence :", font=("Arial", 16))
    license_label.pack(pady=10)

    license_entry = ctk.CTkEntry(home_frame, font=("Arial", 14), width=300)
    license_entry.pack(pady=10)

    # Bouton pour vérifier la licence
    def on_verify_license():
        entered_code = license_entry.get().strip()
        if verify_license(entered_code):
            messagebox.showinfo("Succès", "Licence valide. Vous pouvez maintenant vous connecter.")
            app.show_frame("Login")  # Afficher la frame de connexion
        else:
            messagebox.showerror("Erreur", "Code de licence invalide.")

    verify_button = ctk.CTkButton(home_frame, text="Vérifier la licence", font=("Arial", 16), command=on_verify_license)
    verify_button.pack(pady=20)

    return home_frame