from B05_menu import *

# Lancer la commande suivante pour générer l'exécutable
# pyinstaller B05_main.py
#pyinstaller B05_main.py --strip --onefile  --add-data "C:\\Users\\ckerv\\Documents\\GitHub\\Automate\\fichier_automate;fichier_automate"  --add-data "C:\\Users\\ckerv\\Documents\\GitHub\\Automate\\B05_automate.py;." --name automate
# Explication des erreurs en python
# https://docs.python.org/fr/3/tutorial/errors.html


if __name__ == '__main__':
    # app_sur_tous_les_automate()
    # # afficher_code()
    # # automate = Automate(fichier())
    # # automate.affichage_automate()
    afficher_menu()
    while True:
        menu()
