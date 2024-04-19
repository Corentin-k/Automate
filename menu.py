from rich.progress import track
import time
import os
from dico import *
from automate import *

# Lien vers la documentation de la fonction os.listdir
# https://python.readthedocs.io/en/stable/library/os.html#os.listdir

console = Console(color_system="auto")


def print_help():
    console.print("Le programme permet d'analyser les automates-test")
    console.print("Il peut analyser un automate pour déterminer s'il est [underline]déterministe[/underline], "
                  "[underline]standardisé[/underline], [underline]complet[/underline] ou [underline]minimisé"
                  "[/underline].")
    console.print("Pour analyser un automate, placez-le dans un fichier .txt avec le format spécifié.")
    console.print("Veillez à placer le fichier dans le même dossier que le programme Python ou à spécifier le chemin "
                  "du fichier.")


def print_credit():
    console.print("[red]Ce projet a été réalisé par : [/red]")
    console.print("Corentin KERVAGORET")
    console.print("_____")
    console.print("_____")
    console.print("_____")

    console.print("Dans le cadre du cours de Automates finis et expression relationnelles en L2 à l'Efrei")
    console.print("@2024")


def fichier():
    dossier_programme = os.path.dirname(__file__) + "\\fichier_automate"
    print(dossier_programme)
    fichiers = []
    tree = Tree("Fichier")

    # Définir la fonction de tri par numéro
    def sort_by_number(filename):
        # Extraire le numéro du nom de fichier en supprimant le préfixe "automate-" et le suffixe ".txt"
        try:
            number = int(filename.replace("automate-", "").replace(".txt", ""))
            return number
        except ValueError:
            # Si la conversion échoue, retourner un grand nombre pour ignorer le fichier dans le tri
            return float('inf')

    # Récupérer les fichiers et les trier
    files = [fichier_ for fichier_ in os.listdir(dossier_programme) if
             fichier_.endswith(".txt") and fichier_.startswith("automate")]

    # Trier les fichiers par numéro, ou les ignorer si le numéro est invalide
    files.sort(key=sort_by_number)

    # Ajouter les fichiers triés à l'arbre et les afficher
    for fichier_ in track(files, description="Recupération des fichiers..."):
        fichiers.append(fichier_)
        tree.add(fichier_)
        time.sleep(0)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(tree)

    print("\nQuel automate voulez-vous choisir ?\n")
    choix = int(input(">>>"))
    if choix == 0:
        return None

    # Retourner le chemin complet du fichier choisi
    return os.path.join(dossier_programme, fichiers[choix - 1])


def afficher_menu():
    table = Table(title="Menu")
    table.add_column("Option", style="cyan")
    table.add_column("Raccourcis", style="yellow")
    table.add_column("Description", style="magenta")

    options = [
        ("1", "voir", "Voir le code d'une fonction afficher_code"),
        ("2", "def", "Accéder à la définition d'un mot"),
        ("3", "help", "Afficher l'aide"),
        ("4", "open", "Ouvrir un automate"),
        ("5", "credit", "Afficher les crédits"),
        ("6", "quit", "Quitter"),
        ("7", "menu", "Afficher le menu")
    ]

    for option, raccourcis, description in options:
        table.add_row(option, raccourcis, description)

    print(table)
    print("Choisissez une option :")


def menu():
    choix = input(">>>").lower()

    if choix == "1" or choix == "voir":
        afficher_code()
    elif choix == "2" or choix == "def":
        recherche_mot()
    elif choix == "3" or choix == "help":
        print_help()
    elif choix == "4" or choix == "open":

        automate = Automate(fichier())
        # if automate.verif:
        #     automate.affichage_automate()
        #     automate.completer()
        #     if automate.est_deterministe():
        #         print("L'automate est déterministe")
        #     else:
        #         print("L'automate n'est pas déterministe")
        #     automate.determiniser()
        #
        #     automate.affichage_automate()
        #     automate.standardiser()
        #     if automate.est_deterministe():
        #         print("L'automate est déterministe")
        #     else:
        #         print("L'automate n'est pas déterministe")
        #     if automate.est_standard():
        #         print("L'automate est standard")
        #     else:
        #         print("L'automate n'est pas standard")
        # else:
        #     print("Erreur dans la construction de l'automate")
        #     print("Regarder la structure dans le fichier automate-exemple.txt")
        automate.affichage_automate()
        print("mot accepter :",automate.mot_accepte("ad"))
        automate.minimiser()
        automate.affichage_automate()
        print("mot accepter :", automate.mot_accepte("ad"))
    elif choix == "5" or choix == "credit":
        print_credit()
    elif choix == "6" or choix == "quit":
        console.print("Au revoir !")
        return
    elif choix == "7" or choix == "menu":
        menu()
    else:
        console.print("Option invalide.", style="bold red")
