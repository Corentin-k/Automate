from rich.progress import track
import time
import os
from dico import *
from automate import *
from rich.console import Console

# Lien vers la documentation de la fonction os.listdir
# https://python.readthedocs.io/en/stable/library/os.html#os.listdir

console = Console(color_system="auto")


def print_help():
    console.print("\nBienvenue dans l'aide du programme !")
    console.print("\nLe programme permet d'analyser des automates.")
    console.print("Il peut analyser un automate pour déterminer s'il est [underline]déterministe[/underline], "
                  "[underline]standardisé[/underline], [underline]complet[/underline], ou [underline]minimisé"
                  "[/underline].")
    console.print("Il peut également déterminer si un mot est accepté par l'automate et donner le complémentaire d'un "
                  "automate.")
    console.print(
        "Pour plus d'informations, veuillez consulter le [blue][link=https://github.com/Corentin-k/Automate]README.md[/link][/blue]."
    )
    console.print("Ou si vous voulez plus d'information sur les automates finis, veuillez consulter le lien suivant : "
                  "[blue][link=https://github.com/Corentin-k/Automate/wiki]Wiki[/link][/blue]")
    console.print("\nPour afficher le menu et voir les action possible, tapez [purple]menu[/purple].\n")




def print_credit():
    console.print("[red]Ce projet a été réalisé par : [/red]")
    console.print("    Corentin KERVAGORET")
    console.print("    Henri Su")
    console.print("    Gabriel TANNOUS")
    console.print("    Vidjay VELAYOUDAM")
    console.print("    Hippolyte Vallata")
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
            number = int(filename.replace("B05-", "").replace(".txt", ""))
            return number
        except ValueError:
            # Si la conversion échoue, retourner un grand nombre pour ignorer le fichier dans le tri
            return float('inf')

    # Récupérer les fichiers et les trier
    files = [fichier_ for fichier_ in os.listdir(dossier_programme) if
             fichier_.endswith(".txt") and fichier_.startswith("B05")]

    # Trier les fichiers par numéro, ou les ignorer si le numéro est invalide
    files.sort(key=sort_by_number)

    # Ajouter les fichiers triés à l'arbre et les afficher
    for fichier_ in track(files, description="Recupération des fichiers..."):
        fichiers.append(fichier_)
        tree.add(fichier_)
        time.sleep(0)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(tree)

    print("\nQuel automate voulez-vous choisir ?")
    while True:
        try:
            choix = int(input(">>>"))
            if choix not in range(1, 31) and choix not in range(36, 45):
                raise ValueError
            else:
                break
        except ValueError:
            console.print("\n[red]Erreur:[/red] Veuillez entrer un nombre valide entre 1 et 30 ou entre 36 et 44.")
        print("\nQuel automate voulez-vous choisir ?")

    # Retourner le chemin complet du fichier choisi
    print("\nVous avez choisi l'automate : " + f"B05-" + str(choix) + ".txt")
    return os.path.join(dossier_programme, "B05-" + str(choix) + ".txt")


def afficher_menu():
    # Créez une table pour le menu
    table = Table(title="Menu")

    # Ajoutez des colonnes pour les options, les raccourcis et les descriptions
    table.add_column("Option", style="cyan")
    table.add_column("Raccourcis", style="yellow")
    table.add_column("Description", style="magenta")

    # Liste des options disponibles
    options = [
        ("1", "voir", "Voir le code d'une fonction afficher_code"),
        ("2", "def", "Accéder à la définition d'un mot"),
        ("3", "help", "Afficher l'aide"),
        ("4", "open", "Ouvrir un automate"),
        ("5", "credit", "Afficher les crédits"),
        ("6", "quit", "Quitter"),
        ("7", "menu", "Afficher le menu"),
        ("8", "affichage", "[bold green]Actions sur un automate :[/bold green] Afficher l'automate"),
        ("9", "déterminiser", "[bold green]Actions sur un automate :[/bold green] Déterminiser l'automate"),
        ("10", "standardiser", "[bold green]Actions sur un automate :[/bold green] Standardiser l'automate"),
        ("11", "minimiser", "[bold green]Actions sur un automate :[/bold green] Minimiser l'automate"),
        ("12", "compléter", "[bold green]Actions sur un automate :[/bold green] Compléter l'automate"),
        ("13", "complementaire",
         "[bold green]Actions sur un automate :[/bold green] Afficher le complémentaire de l'automate"),
        ("14", "mot_accepte",
         "[bold green]Actions sur un automate :[/bold green] Vérifier si un mot est accepté par l'automate")
    ]

    # Ajoutez chaque option à la table
    for option, raccourcis, description in options:
        table.add_row(option, raccourcis, description)

    # Affichez la table
    console.print(table)


automate = None  # Variable globale pour stocker l'automate


def menu():
    global automate
    console.print("\n[dim]Taper help/menu si vous avez besoin d'aide sinon tapez votre commande :[/dim]")
    choix = input(">>>").lower()
    liste_action = [
        "8", "affichage",
        "9", "déterminiser",
        "10", "standardiser",
        "11", "minimiser",
        "12", "compléter",
        "13", "complementaire",
        "14", "mot_accepte",
        "15", "test",
    ]

    if choix in ["1", "voir"]:
        afficher_code()
    elif choix in ["2", "def"]:
        recherche_mot()
    elif choix in ["3", "help"]:
        print_help()
    elif choix in ["4", "ouvrir"]:
        # Mettre à jour l'automate avec un nouvel automate
        if automate is not None:
            console.print("\nAttention : Un automate est déjà ouvert. Voulez-vous en ouvrir un autre ?",
                          style="bold yellow")
            choix_ouvrir = input("    >>>").lower()
            if choix_ouvrir in ['oui', 'o', 'yes', 'y']:
                automate = Automate(fichier())
                automate.affichage_automate()
            else:
                console.print("Vous avez choisi de conserver l'automate actuel.", style="bold green")
                automate.affichage_automate()
        else:
            automate = Automate(fichier())
            automate.affichage_automate()

    elif choix in ["5", "credits"]:
        print_credit()
    elif choix in ["6", "quitter","quit"]:
        console.print("Au revoir !", style="bold green")
        quit()
    elif choix in ["7", "menu"]:
        afficher_menu()
    elif automate is not None and choix in liste_action:
        if choix in ["8", "affichage"]:
            automate.affichage_automate()
        elif choix in ["9", "déterminiser"]:
            # Déterminiser l'automate
            automate.determiniser()
        elif choix in ["10", "standardiser"]:
            # Standardiser l'automate
            automate.standardiser()
        elif choix in ["11", "minimiser"]:
            # Minimiser l'automate
            automate.minimiser()
        elif choix in ["12", "compléter"]:
            # Compléter l'automate
            automate.completer()
        elif choix in ["13", "complementaire"]:
            # Afficher le complémentaire de l'automate
            automate.complementaire()
        elif choix in ["14", "mot_accepte"]:
            # Vérifier si un mot est accepté par l'automate
            mot = input("Entrez le mot à vérifier : ")
            accepte = automate.mot_accepte(mot)
            if accepte:
                console.print(f"Le mot '{mot}' est accepté par l'automate.", style="bold green")
            else:
                console.print(f"Le mot '{mot}' n'est pas accepté par l'automate.", style="bold red")
        elif choix in ["15", "test"]:
            # Test de l'automate
            automate.fonction_test()
            type = ""
            if automate.complet:
                type += "complet "
            if automate.deterministe:
                type += "déterministe "
            if automate.standard:
                type += "standard "
            if automate.minimal:
                type += "minimal "

            automate.affichage_automate("Automate " + type)
        else:
            console.print("Option invalide ou l'automate n'est pas ouvert actuellement.", style="bold red")
    elif automate is None and choix in liste_action:
        console.print("Erreur : pas d'automate ouvert.", style="bold red")
    else:
        console.print("Option invalide.", style="bold red")
