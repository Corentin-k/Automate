from rich.progress import track
import time
import os

from dico import *
from automate import *


# Lien vers la documentation de la fonction os.listdir
# https://python.readthedocs.io/en/stable/library/os.html#os.listdir


def print_help():
    console = Console(color_system="auto")
    console.print("Le programme permet d'analyser les automates")
    console.print("Il peut analyser un automate pour déterminer s'il est [underline]déterministe[/underline], "
                  "[underline]standardisé[/underline], [underline]complet[/underline] ou [underline]minimisé"
                  "[/underline].")
    console.print("Pour analyser un automate, placez-le dans un fichier .txt avec le format spécifié.")
    console.print("Veillez à placer le fichier dans le même dossier que le programme Python ou à spécifier le chemin "
                  "du fichier.")


def print_credit():
    console = Console(color_system="auto")
    console.print("[red]Ce projet a été réalisé par ....... [/red]")
    console.print("Dans le cadre du cours de Automates finis et expression relationnelles en L2 à l'Efrei")
    console.print("@2024")


def fichier():
    dossier_programme = os.path.dirname(__file__) + "\\automates"
    print(dossier_programme)
    fichiers = []
    tree = Tree("Fichier")
    for fichier_ in track(os.listdir(dossier_programme), description="Recupération des fichiers..."):
        if fichier_.endswith(".txt") and fichier_.startswith("automate"):
            fichiers.append(fichier_)
            tree.add(fichier_)
            time.sleep(0.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(tree)

    print("\nQuel automate voulez vous choisir ?\n")
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
        recherche_mot()
    elif choix == "3":
        print_help()
    elif choix == "5":
        print_credit()

    elif choix == "4":
        try:

            automate = Automate(fichier())

            automate.affichage_automate()
            automate.completer()
        except:
            print("Erreur lors de l'ouverture de l'automate")
            print("Verifier votre format d'automate")

    elif choix == "7":
        print("Au revoir !")
    else:
        print("Option invalide.")
