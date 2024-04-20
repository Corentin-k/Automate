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

    def _construire_automate(self, lien_fichier):  # Fonction privée indiquée par le '_'
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

            transitions = {}
            for lettre in self.langage:
                transition = self.transition.get(etat, {}).get(lettre, [])
                transitions[lettre] = ','.join(str(item) for item in transition) if transition else ""

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

            table.add_row(type_etat, etat, *transitions.values())

        console.print(table)

    def est_complet(self):
        for etat in self.etat:
            for lettre in self.langage:
                if not self.transition.get(etat, {}).get(lettre, []):
                    self.complet = False
                    return False
        self.complet = True
        return True

    def completer(self):
        if self.complet:
            print("Erreur : L'automate est déjà complet.")
            return
        if self.est_complet():
            print("Erreur : L'automate est déjà complet.")
            return
        if self.deterministe is None:
            print("Voulez vous determiniser l'automate ?")
            choix = input(">>>")
            if choix in ["oui", "o", "yes", "y"]:
                self.determiniser()
            else:
                print("Erreur : L'automate doit être non déterministe pour être complété.")
                return
        elif not self.deterministe:
            print("Erreur : L'automate doit être déterministe pour être completé.")
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
        print("L'automate a été complété avec succès.")
        self.affichage_automate()

    def est_standard(self):
        if len(self.entree) >= 2:
            self.standard = False
            return False

        else:

            # Regarder si un état renvoie vers l'état d'entrée
            for etat in self.etat:
                for lettre in self.langage:
                    if self.entree[0] in self.transition.get(etat, {}).get(lettre, []):
                        self.standard = False
                        return False
            self.standard = True
            return True

    def standardiser(self):
        if self.standard:
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
        bool1 = False
        if not len(self.entree) >= 2:
            for etat in self.etat:
                for lettre in self.langage:
                    if len(self.transition.get(etat, {}).get(lettre, [])) > 1:
                        self.deterministe = False
                        return False
            bool1 = True
        self.deterministe = bool1
        return bool1

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
        if self.deterministe or self.est_deterministe():
            print("Erreur : L'automate est déjà déterministe.")
            return
        deterministe_automate = Automate()
        deterministe_automate.langage = self.langage

        etats_a_traiter = [set(self.entree)]
        etats_traites = set()
        while etats_a_traiter:
            new_etat = etats_a_traiter.pop(0)
            etats_traites.add(tuple(new_etat))

            reformat_new_etat = ''.join(sorted(new_etat))
            deterministe_automate.etat.append(reformat_new_etat)

            for symb in self.langage:
                etats_atteignable = set()

                for etat in new_etat:
                    if symb in self.transition.get(etat, {}):
                        etats_atteignable.update(self.transition[etat][symb])

                if etats_atteignable:
                    if tuple(etats_atteignable) not in etats_traites:
                        etats_a_traiter.append(etats_atteignable)
                        etats_traites.add(tuple(etats_atteignable))

                    reformat_destinations = ''.join(sorted(etats_atteignable))

                    cle_etat = reformat_new_etat
                    if cle_etat not in deterministe_automate.transition:
                        deterministe_automate.transition[cle_etat] = {}

                    # Évitez d'ajouter des destinations vides
                    if reformat_destinations:
                        deterministe_automate.transition[cle_etat][symb] = [reformat_destinations]

        # Transformer les états tuple en string pour l'affichage
        deterministe_automate.etat = [''.join(sorted(etat)) for etat in deterministe_automate.etat]
        deterministe_automate.entree = []
        deterministe_automate.sortie = []

        # Regarder si un état est un état d'entrée ou de sortie dans l'automate initial
        first_entry_added = False
        for etat in self.entree:
            for tuple_etat in deterministe_automate.etat:
                if etat in tuple_etat:
                    if not first_entry_added:
                        deterministe_automate.entree.append(tuple_etat)
                        first_entry_added = True
                    break

        for etat in self.sortie:
            for tuple_etat in deterministe_automate.etat:
                if etat in tuple_etat:
                    if tuple_etat not in deterministe_automate.sortie:
                        deterministe_automate.sortie.append(tuple_etat)

        self.copier_automate(deterministe_automate)
        self.deterministe = True
        print("L'automate a été déterminisé avec succès.")

    def est_minimal(self):
        """Minimise l'automate si nécessaire."""
        pass

    def minimiser(self):
        self.determiniser()
        self.completer()
        self.affichage_automate()
        automate_modifie = Automate()
        automate_modifie.copier_automate(self)

        automate_copie2 = Automate()
        automate_copie2.copier_automate(self)

        et = []  # Etats terminaux
        ent = []  # Etats non terminaux

        for etat in self.etat:
            if etat in self.sortie:
                et.append(etat)
            else:
                ent.append(etat)
        # print(et,ent)

        temp = {}

        for etat in automate_modifie.etat:
            temp1 = automate_copie2.transition.get(etat, {})
            temp[etat] = dict(temp1)

        # cree un automate copie de l'automate avec les etats terminaux et non terminaux
        for etat in automate_modifie.etat:
            for symbole in automate_modifie.langage:
                destinations = automate_modifie.transition.get(etat, {}).get(symbole, [])
                nouvelles_destinations = []
                for destination in destinations:
                    if destination in et:
                        nouvelles_destinations.append("T")
                    elif destination in ent:
                        nouvelles_destinations.append("NT")
                    else:
                        nouvelles_destinations.append(destination)
                automate_modifie.transition[etat][symbole] = nouvelles_destinations

        motifs_transitions = {}

        # Reunir les etats sortie qui ont le meme schéma de transition
        for etat_terminal in et:
            transitions_etat_terminal = automate_modifie.transition.get(etat_terminal, {})
            motif = ""
            for symbole, destinations in transitions_etat_terminal.items():
                motif += "".join(destinations)
            motif = "T" + motif
            if motif not in motifs_transitions:
                motifs_transitions[motif] = [etat_terminal]
            else:
                motifs_transitions[motif].append(etat_terminal)

        print(motifs_transitions)

        motifs_transitions2 = {}
        # Reunir les autres etat qui ont le meme schéma de transition
        for etat_terminal in ent:
            transitions_etat_terminal = automate_modifie.transition.get(etat_terminal, {})
            motif = ""
            for symbole, destinations in transitions_etat_terminal.items():
                motif += "".join(destinations)
            motif = "NT" + motif
            if motif not in motifs_transitions2:
                motifs_transitions2[motif] = [etat_terminal]
            else:
                motifs_transitions2[motif].append(etat_terminal)

        motifs_transitions.update(motifs_transitions2)
        print(motifs_transitions)
        transitions_avant_fusion = {}
        for etat, transitions in temp.items():
            transitions_avant_fusion[etat] = {}
            for symbole, destinations in transitions.items():
                groupes_destinations = []
                for destination in destinations:
                    for motif, etats in motifs_transitions.items():
                        if destination in etats:
                            groupes_destinations.append(motif)
                            break
                transitions_avant_fusion[etat][symbole] = groupes_destinations

        # Separer les groupes de motifs
        groupes_separes = {}

        for motif, etats_du_groupe in motifs_transitions.items():
            transitions_du_groupe = {}
            for etat in etats_du_groupe:
                transitions_du_groupe[etat] = transitions_avant_fusion[etat]

            # print(f"Transitions du groupe de motifs {motif} :", transitions_du_groupe)

            for etat, transitions_etat in transitions_du_groupe.items():
                Similaire = False

                for groupe, transitions_groupe in groupes_separes.items():
                    if transitions_avant_fusion[transitions_groupe[0]] == transitions_etat:
                        groupes_separes[groupe].append(etat)
                        Similaire = True
                        break
                if not Similaire:
                    groupes_separes[f"NewGroup{len(groupes_separes) + 1}"] = [etat]
        #print("Groupes séparés :", groupes_separes)
        # print("Groupes séparés :", groupes_separes)
        # for etat, transitions in temp.items():
        # print(etat,transitions)
        new_entree = []
        new_sortie = []
        # print(motifs_transitions)
        for motif, etats in groupes_separes.items():
            nouvel_etat = "".join(etats)
            transitions_nouvel_etat = {}
            for etat in etats:
                transitions_etat = temp[etat]

                for symbole, destinations in transitions_etat.items():
                    #print(symbole,":",destinations)
                    if symbole not in transitions_nouvel_etat:
                        transitions_nouvel_etat[symbole] = []
                    for destination in destinations:
                        #print(":", destination)
                        #print(transitions_nouvel_etat, "\n")
                        if destination not in transitions_nouvel_etat[symbole]:
                            transitions_nouvel_etat[symbole].append(destination)
            # print(transitions_nouvel_etat, ":::")
            for symbole, destinations in transitions_nouvel_etat.items():
                # print(symbole,destinations)
                transitions_nouvel_etat[symbole] = "".join(sorted(list(set(destinations))))

            automate_copie2.etat.append(nouvel_etat)
            automate_copie2.transition[nouvel_etat] = transitions_nouvel_etat

            for etat in etats:
                if etat in self.entree:
                    new_entree.append(nouvel_etat)
                if etat in self.sortie:
                    if nouvel_etat not in new_sortie:
                        new_sortie.append(nouvel_etat)

            for etat in etats:
                if etat != nouvel_etat:
                    del automate_copie2.transition[etat]
                    automate_copie2.etat.remove(etat)
                else:
                    automate_copie2.etat.remove(nouvel_etat)
        # Ajouter chaque transition pour chaque lettre dans un tableau

        for etat, transitions_etat in automate_copie2.transition.items():
            for symbole, destination in transitions_etat.items():
               if not isinstance(destination, list):
                    automate_copie2.transition[etat][symbole] = [destination]

        print(automate_copie2)

        automate_copie2.entree = new_entree
        automate_copie2.sortie = new_sortie

        self.copier_automate(automate_copie2)

    def complementaire(self):
        """Calcule l'automate complémentaire."""
        print("Automate complémentaire")
        automate_complementaire = Automate()
        automate_complementaire.copier_automate(self)
        nouveaux_etats_finaux = []

        for etat in automate_complementaire.etat:
            if etat not in automate_complementaire.sortie:
                nouveaux_etats_finaux.append(etat)

        automate_complementaire.sortie = nouveaux_etats_finaux
        automate_complementaire.affichage_automate()

    def mot_accepte(self, mot: str):
        """Détermine si un mot est accepté par l'automate."""
        # Initialiser une liste avec l'état d'entrée initial
        etats_a_explorer = [self.entree]

        # Pour chaque symbole dans le mot
        for symbole in mot:
            # Nouvelle liste pour les états à explorer pour le prochain symbole
            nouveaux_etats = []

            # Parcourez tous les états actuels dans la liste
            while etats_a_explorer:
                # Obtenez l'état courant de la liste
                etat_courant = etats_a_explorer.pop(0)
                if isinstance(etat_courant, list) and len(etat_courant) == 1:
                    etat_courant = etat_courant[0]
                # Obtenez les transitions possibles pour l'état courant et le symbole
                transitions_possibles = self.transition.get(etat_courant, {}).get(symbole, [])

                # Ajoutez toutes les transitions possibles à la nouvelle liste d'états
                for etat_prochain in transitions_possibles:
                    # Assurez-vous d'ajouter chaque nouvel état à la liste sans duplication
                    if etat_prochain not in nouveaux_etats:
                        nouveaux_etats.append(etat_prochain)

            # Mettre à jour la liste des états à explorer avec les nouveaux états
            etats_a_explorer = nouveaux_etats

            # Si la liste est vide, cela signifie que le mot n'est pas accepté
            if not etats_a_explorer:
                return False

        # Vérifiez si l'un des états courants est un état de sortie de l'automate
        for etat in etats_a_explorer:
            if etat in self.sortie:
                return True

        # Si aucun état courant n'est un état de sortie, le mot n'est pas accepté
        return False

