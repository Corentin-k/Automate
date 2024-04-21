import inspect
from rich import print  # pip install rich
from rich.syntax import Syntax
from rich.tree import Tree

from automate import *

# Lien vers la documentation de la fonction inspect
# https://docs.python.org/3/library/inspect.html#inspect.getsource


"""
Fichier B05-dico.py
Ce fichier contient des fonctions pour afficher le code d'une fonction de la classe Automate et pour rechercher un mot
dans un dictionnaire.

Fonctions :

    - definition(mot) : donne la définition d'un mot
    - recherche_mot() : permet de rechercher un mot dans un dictionnaire
    - afficher_code() : affiche le code d'une fonction de la classe Automate
    
"""


def definition(mot):
    """Donne la définition d'un mot
    :param mot: str
    : return bool
    """
    console = Console(color_system="auto")
    definitions = {
        "minimal": {
            "synonymes": ["minimal", "minimiser", "minimale"],
            "definition": "Un automate minimal est l'[underline]unique[/underline] automate [underline]déterministe"
                          "[/underline] et [underline]complet[/underline] avec le plus petit nombre d'états."
        },
        "complet": {
            "synonymes": ["complet", "compléter"],
            "definition": "Un automate est complet s'il possède [underline]une[/underline] transition pour chaque "
                          "possibilité à partir de chaque état."
        },
        "standard": {
            "synonymes": ["standard", "standardiser", "standardisé"],
            "definition": "Un automate est standardisé s'il admet une et une seule entrée et qu'aucune transition "
                          "n'amène à"
                          "cette entrée."
        },
        "déterministe": {
            "synonymes": ["déterministe", "déterminer", "déterminiser"],
            "definition": "Un automate est déterministe s'il admet une unique entrée et qu'il n'y a pas d'états où il y"
                          "a plus d'une sortie avec le même libellé."
        }
    }

    for cle, valeur in definitions.items():
        if mot in valeur["synonymes"]:
            console.print(f"\n[red]Définition de '{cle}'[/red] : {valeur['definition']}")
            return True

    return False


def recherche_mot():
    """Permet de rechercher un mot dans un dictionnaire"""
    while True:
        print("\nQuel mot voulez-vous rechercher ?")
        mot_recherche = input(">>> ").lower()
        try:
            if not definition(mot_recherche):
                raise ValueError("Le mot n'est pas présent dans le dictionnaire.")
        except ValueError as e:
            # Le mot n'a pas été trouvé
            print("\n[bold yellow]Attention :[/bold yellow] " + str(e))
        print("\nVoulez-vous chercher un autre mot ? (o/n)")
        choix = input(">>> ").lower()
        if choix not in ["oui", "o", "yes", "y"]:
            return


def afficher_code():
    """Affiche le code d'une fonction de la classe Automate
    :return:
    """

    tree = Tree("Automate")

    for name, obj in inspect.getmembers(Automate):  # On récupère les membres de la classe Automate
        if inspect.isfunction(obj):  # On vérifie que l'objet est une fonction
            tree.add(name)

    print(tree)
    print("Quelle fonction voulez-vous afficher ?")
    fonction = input(">>> ")

    try:
        fonction = "Automate." + fonction
        code = inspect.getsource(eval(fonction))
        syntax = Syntax(code, "python", theme="ansi_dark", line_numbers=True)
        print(syntax)
    except AttributeError:
        print("La fonction spécifiée n'existe pas dans Automate.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
