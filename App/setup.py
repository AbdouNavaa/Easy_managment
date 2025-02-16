from cx_Freeze import setup, Executable
import os

# Chemin vers le dossier des images
image_dir = os.path.join(os.path.dirname(__file__), "images")

# Liste des packages à inclure
packages = ["pymysql", "pandas", "tkcalendar", "bcrypt", "customtkinter", "PIL", "openpyxl", "sqlalchemy", "matplotlib"]

# Configuration de l'exécutable
executables = [
    Executable(
        "home.py",  # Remplacez par le nom de votre script principal
        base="Win32GUI",  # Utilisez "Win32GUI" pour une application sans console
        icon="easy_logo.ico",  # Chemin relatif ou absolu vers l'icône
    )
]

setup(
    name="Easy",
    version="1.3.1",
    description="Easy for management",
    options={
        "build_exe": {
            "packages": packages,
            "include_files": [("images", "images")],  # Assurez-vous que les fichiers sont bien copiés
            "excludes": ["xlrd", "xlsxwriter"],
        }
    },
    executables=executables,
)
# pour build
# python setup.py build