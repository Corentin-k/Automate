from menu import *

from rich import print
from rich.layout import Layout

# Lancer la commande suivante pour générer l'exécutable
# pyinstaller main.py

# Explication des erreurs en python
# https://docs.python.org/fr/3/tutorial/errors.html
from rich.panel import Panel

if __name__ == '__main__':

    # # afficher_code()
    # # automate = Automate(fichier())
    # # automate.affichage_automate()
    afficher_menu()
    while True:
        menu()

