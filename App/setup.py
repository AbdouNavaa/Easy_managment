from cx_Freeze import setup, Executable

# Liste des packages à inclure
packages = ["pymysql", "pandas", "tkcalendar", "bcrypt", "customtkinter", "PIL"]

# Liste des fichiers de données à inclure
include_files = ["user_data.json", "frames/"]
# Configuration de l'exécutable
executables = [
    Executable(
        "home.py",  # Remplacez par le nom de votre script principal
        base="Win32GUI",  # Utilisez "Win32GUI" pour une application sans console
        # icon="icon.ico",  # Optionnel : ajoutez une icône pour votre application
    )
]
setup(
    name="MyApp",
    version="1.1",
    description="My App Description",
    options={
        "build_exe": {
            "packages": packages,
            "include_files": include_files,
            "excludes": ["xlrd", "xlsxwriter"],  # Exclure les modules inutiles
        }
    },
    executables=executables,
)