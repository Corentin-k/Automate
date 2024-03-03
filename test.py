from rich import print  # pip install rich
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.progress import track
from rich.syntax import Syntax

"""
Donner les def de chaque erme  : determinisation, standardisation, complémentaire, minimisation
Choisir l'automate à analyser
    Dire ce que l'automate est
    DEmandé ce que l'utilisatuer veut faire
Help
Crédit
Quitter

"""


def menu_automate(action):
    menu = Console(color_system="windows")
    print("Bonjour bienvenu dans ce programme pour les automates")

    if action.lower() == "help":
        menu.print("Le programme permet d'analyser les automates")
        menu.print("Il peut annalyser celui ci et dire si il est [underline]déterministe[/underline], "
                   "[underline]standardiser[/underline], [underline]complet[/underline] ou [underline]minimiser["
                   "/underline]")
        menu.print("Pour analyser l'automate veuillez le mettre dans un fichier .txt avec le format suivant")
        menu.print("format .....")
        menu.print(
            "Vueillez mettre le fichier dans le même dossier que le programme python ou choisisser l'option spécifier "
            "le chemin du fichier")

    if action.lower() in ["crédit", "crédits", "credit", "credits"]:
        menu.print("\033[31mCe projet a été réaliser par ....... ")
        menu.print("Dans le cut du cours de Automate finis et expression relationnel en L2 à l'efrei")
        menu.print("@2024")


def recherchemot():
    print("\nQuel mot voulez vous rechercher ?")
    mot_recherche = input(">>> ")
    if not definition(mot_recherche.lower()):
        print("\nCe mot n'est pas présent dans le dictionnaire")
    print("\nVouler vous chercher un autre mot o/n")
    choix = input(">>> ")
    if choix.lower() in ["oui", "y", "o", "yes"]:
        recherchemot()
    else:
        menu_automate("help")


def definition(mot):
    dictionnaire = Console(color_system="windows")

    if mot in ["minimal", "minimiser"]:
        dictionnaire.print("\n[red]Automate minimal[/red] : Un automate minimal est l'[underline]unique[/underline] "
                           "automate [underline]détermniste[/underline] et [underline]complet[/underline] avec le "
                           "[bold]plus petit nombre d'états[/bold]")
        dictionnaire.print("Automate complet ")
        return True
    if mot in ["complet"]:
        dictionnaire.print("\n[red]Automate complet[/red]: Un automate est complet si et seulement si pour chaque "
                           "états il y a [underline]une[/underline] trnasition pour chaque possibilité")
        return True
    if mot in ["standard", "standardiser", "standardisé"]:
        dictionnaire.print("\n[red]Automate standardisé[/red] : un automate est standardisé si et seulement si il "
                           "admet une et une seule entrée et qu'aucune transition amène à cette entrée")
        return True
    if mot in ["déterministe", "déterminiser"]:
        dictionnaire.print("\n[red]Automate déterministe[/red] : Un automate est deterministe si et seulement si il "
                           "admet une unique entrée et qu'il n'y ait pas d'états où il y a plus de une sortie avec le"
                           " même libellé")
        return True
    else:
        return False
