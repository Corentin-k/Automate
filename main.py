from rich.progress import track
from test import *
import time
from rich.tree import Tree
from test import *

from Automate import *
from Code import *
import os


# pyinstaller main.py


# Press the green button in
# the gutter to run the script.

# https://python.readthedocs.io/en/stable/library/os.html#os.listdir

def fichier():
    dossier_programme = os.path.dirname(__file__) + "\\automates"
    print(dossier_programme)
    fichiers = []
    tree = Tree("Fichier")
    for fichier in track(os.listdir(dossier_programme), description="Recupération des fichiers..."):
        if fichier.endswith(".txt") and fichier.startswith("automate"):
            fichiers.append(fichier)
            tree.add(fichier)
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(tree)

    print("\nQuel automate voulez vous chosir ?\n")
    choix = int(input(">>>"))
    if choix == 0:
        return None
    return dossier_programme + "\\" + fichiers[choix - 1]


def menu():
    print("Menu :")
    print("1. voir le code d'une fonction afficher_code")
    print("2. Accéder à la définition d'un mot")
    print("3. Afficher l'aide")
    print("4. Ouvrir un automate")
    print("5. Afficher les_credits")
    print("6. Quitter")

    print("Choisissez une option :")
    choix = input(">>>")

    if choix == "1":
        afficher_code()
    elif choix == "2":
        recherchemot()
    elif choix == "3":
        print_help()
    elif choix == "5":
        print_credit()

    elif choix == "4":

        automate=Automate(fichier())
        automate.affichage_automate()
        automate.completer()
        automate.completer()
    elif choix == "7":
        print("Au revoir !")
    else:
        print("Option invalide.")


if __name__ == '__main__':
    # afficher_code()
    # automate = Automate(fichier())
    # automate.affichage_automate()

    x = 0
    while True:
        menu()
