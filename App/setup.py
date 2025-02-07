from cx_Freeze import setup, Executable

# Liste des packages à inclure
packages = ["pymysql", "pandas", "tkcalendar", "bcrypt", "customtkinter", "PIL", "openpyxl", "sqlalchemy", "matplotlib"]

# Liste des fichiers de données à inclure
include_files = [
    "frames/", 
    "products.xlsx", 
    "invoices.xlsx", 
    ("easy_logo.ico", "easy_logo.ico")  # Inclure l'icône dans le répertoire de construction

]

# Configuration de l'exécutable
executables = [
    Executable(
        "home.py",  # Remplacez par le nom de votre script principal
        base="Win32GUI",  # Utilisez "Win32GUI" pour une application sans console
        icon="easy_logo.ico",  # Chemin relatif ou absolu vers l'icône
    )
]

setup(
    name="Esay",
    version="1.1.1",
    description="Application de gestion de stock",
    options={
        "build_exe": {
            "packages": packages,
            "include_files": include_files,
            "excludes": ["xlrd", "xlsxwriter"],  # Exclure les modules inutiles
        }
    },
    executables=executables,
)

# pour build
# python setup.py build