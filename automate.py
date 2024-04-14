from abc import ABC
from rich.console import Console
from rich.table import Table

# Lien vers la documentation de la fonction os.listdir
# https://rich.readthedocs.io/en/stable/tree.html


from automate_interface import AutomateInterface


class Automate(AutomateInterface, ABC):
    """Classe Automate qui permet de créer un automate à partir d'un fichier texte
    et de le manipuler

    Use :
        automate = Automate("fichier.txt")
        automate.affichage_automate()

    Attributs
        etat : liste des états
        langage : liste des lettres du langage
        entree : liste des états d'entrée
        sortie : liste des états de sortie
        transition : dictionnaire des transitions
        complet : booléen indiquant si l'automate est complet
        standard : booléen indiquant si l'automate est standard
        deterministe : booléen indiquant si l'automate est déterministe

    """

    def __init__(self, lien_fichier=None):
        self.verif = None
        self.etat = []
        self.langage = []
        self.entree = []
        self.sortie = []
        self.transition = {}
        self.complet = False
        self.standard = False
        self.deterministe = False
        self.minimal = False
        if lien_fichier:
            self._construire_automate(lien_fichier)

    def _construire_automate(self, lien_fichier):  # Fonction privée indiquée par le _
        with open(lien_fichier, "r") as Fichier:

            contenu = Fichier.readline().strip("Etat={}\n")  # recupere la premiere ligne et enleve le retour à la ligne
            if contenu == "":
                return

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
        self.verif_automate()

    def verif_automate(self):

        if len(self.etat) == 0 or len(self.transition) == 0:
            self.verif = False
        else:
            self.verif = True

    def __str__(self):
        affichage = f"Etat: {self.etat}\nLangage: {self.langage}\nEntree : {self.entree},\nSortie : {self.sortie},"
        affichage += f"\nTransition : {self.transition},\nComplet : {self.complet},"
        affichage += f" Standard : {self.standard}, Deterministe : {self.deterministe}, Minimal : {self.minimal}"
        return affichage

    def affichage_automate(self):
        console = Console(color_system="windows")
        table = Table(title="Automate", show_lines=True)
        table.add_column("[green]Entré[/green]/[red]Sortie[/red]", justify="left", style="cyan")

        table.add_column("Etats", justify="center", style="magenta")
        for lettre in self.langage:
            if lettre != "":
                table.add_column(lettre, justify="center", style="magenta")
        for etat in self.etat:

            etat_str = ','.join(etat)

            transitions = {}
            for lettre in self.langage:
                transition = self.transition.get(etat, {}).get(lettre, [])
                transitions[lettre] = ','.join(transition) if transition else ""
            # Type entre ou sortie

            if etat in self.entree:
                if etat in self.sortie:
                    type_etat = "[green]E[/green]//[red]S[/red]"
                else:
                    type_etat = "[green]E[/green]"
            elif etat in self.sortie:
                type_etat = "[red]S[/red]"
            else:
                type_etat = ""
            table.add_row(type_etat, etat_str, *transitions.values())

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

    def est_standard(self):
        if len(self.entree) >= 2:
            return False

        else:

            # Regarder si un état renvoie vers l'état d'entrée
            for etat in self.etat:
                for lettre in self.langage:
                    if self.entree[0] in self.transition.get(etat, {}).get(lettre, []):
                        return False
            return True

    def standardiser(self):
        if self.est_standard():
            print("Déjà standard")
            return
        self.etat.append("i")
        # Création des transitions sortantes du nouvel état initial
        transitions_nouvel_etat = {}
        for lettre in self.langage:
            transitions_nouvel_etat[lettre] = []
            for etat_initial in self.entree:
                if lettre in self.transition.get(etat_initial, {}):
                    transitions_nouvel_etat[lettre].extend(
                        self.transition[etat_initial][lettre])  # on concatène les listes
                if etat_initial in self.sortie:  # Si l'état initial est dans la sortie, alors "i" doit être dans la sortie
                    self.sortie.append("i")

        # nous allons enlever les doublons maintenant
        for doublon in transitions_nouvel_etat:
            transitions_nouvel_etat[doublon] = sorted(list(set(transitions_nouvel_etat[
                                                                   doublon])))  # nous mettons en liste afin de pouvoir accéder à l'indexation si besoin / set pour enlever les doublons / sorted pour trier dans l'ordre croissant

        # nouvel état initial

        self.transition["i"] = transitions_nouvel_etat

        # états d'entrée et de sortie
        self.entree = ["i"]
        self.sortie = list(set(self.sortie))  # Enlever les doublons dans la sortie
        self.affichage_automate()
        self.standard = True

    def est_deterministe(self):
        bool = False
        if not len(self.entree) >= 2:
            for etat in self.etat:
                for lettre in self.langage:

                    if len(self.transition.get(etat, {}).get(lettre, [])) > 1:
                        print(self.transition.get(etat, {}).get(lettre, []))
                        return False
            bool = True
        return bool

    def copier_automate(self, autre_automate):

        self.etat = autre_automate.etat[:]
        self.langage = autre_automate.langage[:]
        self.entree = autre_automate.entree[:]
        self.sortie = autre_automate.sortie[:]
        self.transition = dict(autre_automate.transition)
        self.complet = autre_automate.complet
        self.standard = autre_automate.standard
        self.deterministe = autre_automate.deterministe
        self.minimal = autre_automate.minimal

    def determiniser(self):
        if self.est_deterministe():
            print("Erreur : L'automate est déjà déterministe.")
            return
        deterministe_automate = Automate()

        deterministe_automate.langage = self.langage

        etats_a_traiter = [set(self.entree)]
        etats_traites = set()

        while etats_a_traiter:
            new_etat = etats_a_traiter.pop(0)
            etats_traites.add(tuple(new_etat))
            deterministe_automate.etat.append(tuple(sorted(new_etat)))

            for symb in self.langage:
                etats_atteignable = set()

                for etat in new_etat:
                    if symb in self.transition.get(etat, {}):
                        etats_atteignable.update(self.transition[etat][symb])

                if tuple(etats_atteignable) not in etats_traites:
                    etats_a_traiter.append(etats_atteignable)
                    etats_traites.add(tuple(etats_atteignable))

                cle_etat = tuple(sorted(new_etat))
                if cle_etat not in deterministe_automate.transition:
                    deterministe_automate.transition[cle_etat] = {}
                deterministe_automate.transition[cle_etat].update({symb: tuple(sorted(etats_atteignable))})

        deterministe_automate.entree = tuple(sorted(self.entree))
        deterministe_automate.sortie = [etat for etat in deterministe_automate.etat if
                                        set(etat).intersection(self.sortie)]

        # Ajout des états d'entrée dans l'automate deterministe
        deterministe_automate.entree=[]
        for etat in self.entree:
            for tuple_etat in deterministe_automate.etat:

                if etat in tuple_etat:
                    if tuple_etat not in deterministe_automate.entree:
                        deterministe_automate.entree.append(tuple_etat)


        self.copier_automate(deterministe_automate)
        self.deterministe = True
        print("L'automate a été déterminisé avec succès.")

    def minimiser(self):
        """Minimise l'automate si nécessaire."""
        pass

    def est_minimal(self):
        pass
