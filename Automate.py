from rich.console import Console
from rich.table import Table


# https://rich.readthedocs.io/en/stable/tree.html

class Automate:
    # Attribut
    complet = False
    standard = False
    deterministe = False
    minimal = False

    def __init__(self, lien_fichier):

        with open(lien_fichier, "r") as Fichier:
            contenu = Fichier.readline().strip("Etat={}\n")  # recupere la premiere ligne et enleve le retour à la ligne
            etat = contenu.split(",")
            self.etat = etat

            contenu = Fichier.readline().replace("Langage={", "").replace("}\n", "").split(",")
            self.langage = contenu

            contenu = Fichier.readline().strip(
                "Entree={}\n")  # recupere la premiere ligne et enleve le retour à la ligne
            entree = contenu.split(",")
            self.entree = entree

            contenu = Fichier.readline().strip(
                "Sortie={}\n")  # recupere la premiere ligne et enleve le retour à la ligne
            sortie = contenu.split(",")
            self.sortie = sortie

            self.transition = {}
            Fichier.readline()
            while True:
                contenu = Fichier.readline().strip()
                if not contenu:
                    break
                transition = contenu.split(":")
                etat, actions = transition[0], transition[1].split(";")
                self.transition[etat] = {}
                for action in actions:
                    symbole, destination = action.strip().split()
                    destination = destination.strip().split(",")

                    self.transition[etat][symbole] = destination

    def __str__(self):

        return f"Etat: {self.etat}\nLangage: {self.langage}\nEntree : {self.entree},\nSortie : {self.sortie},\nTransition : {self.transition},\nComplet : {self.complet}, Standard : {self.standard}, Deterministe : {self.deterministe}, Minimal : {self.minimal}"

    def affichage_automate(self):
        console = Console(color_system="windows")
        table = Table(title="Automate", show_lines=True)
        table.add_column("[green]Entré[/green]/[red]Sortie[/red]", justify="left", style="cyan")

        table.add_column("Etats", justify="center", style="magenta")
        for lettre in self.langage:
            if lettre != "":
                table.add_column(lettre, justify="center", style="magenta")
        for etat in self.etat:

            transitions = {}
            for lettre in self.langage:
                transition = self.transition.get(etat, {}).get(lettre, [])
                transitions[lettre] = ','.join(transition) if transition else ""

            if etat in self.entree:
                if etat in self.sortie:
                    type = "[green]E[/green]//[red]S[/red]"
                else:
                    type = "[green]E[/green]"
            elif etat in self.sortie:
                type = "[red]S[/red]"
            else:
                type = ""
            table.add_row(type, etat, *transitions.values())

        console.print(table)

    def est_complet(self):
        for etat in self.etat:
            for lettre in self.langage:
                if not self.transition.get(etat, {}).get(lettre, []):
                    return False
        return True

    def completer(self):
        if self.est_complet():
            print("Deja complet")
            return
        for etat in self.etat:
            for lettre in self.langage:
                if not self.transition.get(etat, {}).get(lettre, []):
                    if etat not in self.transition:
                        self.transition[etat] = {}
                    self.transition[etat][lettre] = "p"
        self.transition["p"] = {lettre: ["p"] for lettre in self.langage}
        self.complet = True
        self.etat.append("p")
        self.affichage_automate()
