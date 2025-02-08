from cx_Freeze import setup, Executable

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
    version="1.2.0",
    description="Easy for management",
    options={
        "build_exe": {
            "packages": packages,
            "excludes": ["xlrd", "xlsxwriter"],  # Exclure les modules inutiles
        }
    },
    executables=executables,
)

# pour build
# python setup.py build