from rich import print  # pip install rich
from rich.console import Console

"""
Donner les def de chaque terme  : determination, standardisation, complémentaire, minimisation
Choisir l'automate à analyser
    Dire ce que l'automate est
    Demandé ce que l'utilisateur veut faire
Help
Crédit
Quitter

"""


console = Console(color_system="auto")


def print_help():
    console.print("Le programme permet d'analyser les automates")
    console.print("Il peut analyser un automate pour déterminer s'il est [underline]déterministe[/underline], "
                  "[underline]standardisé[/underline], [underline]complet[/underline] ou [underline]minimisé"
                  "[/underline].")
    console.print("Pour analyser un automate, placez-le dans un fichier .txt avec le format spécifié.")
    console.print("Veillez à placer le fichier dans le même dossier que le programme Python ou à spécifier le chemin "
                  "du fichier.")


def print_credit():
    console.print("[red]Ce projet a été réalisé par ....... [/red]")
    console.print("Dans le cadre du cours de Automates finis et expression relationnelles en L2 à l'Efrei")
    console.print("@2024")


def definition(mot):
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


def rechercheMot():
    while True:
        print("\nQuel mot voulez-vous rechercher ?")
        mot_recherche = input(">>> ").lower()
        if definition(mot_recherche):
            continue
        else:
            print("\nCe mot n'est pas présent dans le dictionnaire.")
            print("\nVoulez-vous chercher un autre mot ? (o/n)")
            choix = input(">>> ").lower()
            if choix not in ["oui", "o", "yes", "y"]:
                return
