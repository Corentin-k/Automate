from abc import ABC
from rich.console import Console
from rich.table import Table

# Lien vers la documentation de la fonction os.listdir
# https://rich.readthedocs.io/en/stable/tree.html


from automate_interface import AutomateInterface

console = Console(color_system="windows")


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
            while True: # recupere les transitions
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

    def affichage_automate(self, titre="Automate"):
        """Affiche l'automate dans un tableau."""
        table = Table(title=titre, show_lines=True)
        table.add_column("[green]Entré[/green]/[red]Sortie[/red]", justify="left", style="cyan")

        table.add_column("Etats", justify="center", style="magenta")
        # Ajouter les colonnes pour chaque lettre du langage
        for lettre in self.langage:
            if lettre != "":
                table.add_column(lettre, justify="center", style="magenta")
        # Ajouter les transitions pour chaque état
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

    def est_complet(self, affichage=False):
        for etat in self.etat:
            for lettre in self.langage:
                if not self.transition.get(etat, {}).get(lettre, []): # Regarde si la transition est vide
                    if affichage:
                        console.print(
                            "\n[yellow]L'automate n'est pas complet : Il manque des transitions pour un état et un symbole donné.[/yellow]\n")
                    return False
        return True

    def completer(self):
        if self.est_complet(True):
            console.print("[red]Erreur[/red] L'automate est déjà complet.")
            self.affichage_automate("Automate Complet et Déterministe")
            return

        # Créer une copie de l'automate pour le compléter
        automate_complet = Automate()
        automate_complet.copier_automate(self)

        if not self.est_deterministe():  # Si l'automate n'est pas déterministe, on le déterminise
            console.print("[red]Erreur[/red] : L'automate doit être déterministe pour être complété.")
            console.print("L'automate est en cours de déterminisation...")
            automate_complet = automate_complet.determiniser()

        # Ajoute la transition vers l'état poubelle pour chaque état et chaque lettre du langage manquant
        for etat in automate_complet.etat:
            for lettre in automate_complet.langage:
                if not automate_complet.transition.get(etat, {}).get(lettre, []):
                    if etat not in automate_complet.transition:
                        automate_complet.transition[etat] = {}
                    automate_complet.transition[etat][lettre] = ["p"]
        # Trier les transitions pour qu'elles restent dans l'ordre
        automate_complet.transition = {
            etat: {
                lettre: sorted(transitions_etat[lettre])
                for lettre in sorted(transitions_etat)
            }
            for etat, transitions_etat in sorted(automate_complet.transition.items())
        }
        # Ajouter l'état poubelle comme etat
        automate_complet.transition["p"] = {lettre: ["p"] for lettre in automate_complet.langage}
        automate_complet.complet = True
        automate_complet.etat.append("p")
        console.print("[green]\nL'automate a été complété avec succès.\n[/green]")
        automate_complet.affichage_automate("Automate Complet et Déterministe")
        return automate_complet

    def est_standard(self):
        if len(self.entree) >= 2: # Regarder si il y a plus d'un état d'entrée
            console.print("\n[yellow]L'automate n'est pas standard: Il y a plus d'un état d'entrée.[/yellow]\n")
            return False
        else:
            # Regarder si un état renvoie vers l'état d'entrée
            for etat in self.etat:
                for lettre in self.langage:
                    if self.entree[0] in self.transition.get(etat, {}).get(lettre, []):
                        console.print(
                            "\n[yellow]L'automate n'est pas standard: Un état renvoie vers l'état d'entrée.[/yellow]\n")
                        return False
            return True

    def standardiser(self):
        if self.est_standard():
            console.print("[green]Déjà standard[/green]")
            return
        automate_standardiser = Automate()
        automate_standardiser.copier_automate(self)
        # Création du nouvel état initial
        automate_standardiser.etat.append("i")
        # Création des transitions sortantes du nouvel état initial
        transitions_nouvel_etat = {}
        for lettre in automate_standardiser.langage:
            transitions_nouvel_etat[lettre] = []
            for etat_initial in automate_standardiser.entree:
                if lettre in automate_standardiser.transition.get(etat_initial, {}):
                    transitions_nouvel_etat[lettre].extend(
                        automate_standardiser.transition[etat_initial][lettre])  # on concatène les listes
                if etat_initial in automate_standardiser.sortie:  # Si l'état initial est dans la sortie, alors "i" doit être dans la sortie
                    automate_standardiser.sortie.append("i")

        # nous allons enlever les doublons maintenant
        for doublon in transitions_nouvel_etat:
            transitions_nouvel_etat[doublon] = sorted(list(set(transitions_nouvel_etat[
                                                                   doublon])))  # nous mettons en liste afin de pouvoir accéder à l'indexation si besoin / set pour enlever les doublons / sorted pour trier dans l'ordre croissant

        # nouvel état initial
        automate_standardiser.transition["i"] = transitions_nouvel_etat

        # états d'entrée et de sortie
        automate_standardiser.entree = ["i"]
        automate_standardiser.sortie = list(set(self.sortie))  # Enlever les doublons dans la sortie
        console.print("[green]\nL'automate a été standardisé avec succès.\n[/green]")
        automate_standardiser.affichage_automate("Automate Standardisé")
        self.standard = True
        return automate_standardiser

    def est_deterministe(self, affichage=False):
        bool1 = False
        if not len(self.entree) >= 2: # Regarder si il y a plus d'un état d'entrée
            for etat in self.etat:
                for lettre in self.langage:
                    if len(self.transition.get(etat, {}).get(lettre, [])) > 1: # Regarder si il y a plus d'une transition possible pour un état et un symbole donné
                        if affichage:
                            console.print(
                                "\n[yellow]L'automate n'est pas déterministe: Il y a plus d'une transition possible pour un état et un symbole donné.[/yellow]\n")
                        return False
            bool1 = True
        else:
            if affichage:
                console.print("\n[yellow]L'automate n'est pas déterministe: Il y a plus d'un état d'entrée.[/yellow]\n")
        return bool1

    def copier_automate(self, autre_automate):
        # Copie les attributs de l'automate passé en paramètre
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
        if self.est_deterministe(True):
            console.print("[red]Erreur[/red] : L'automate est déjà déterministe.")
            return
        deterministe_automate = Automate()
        deterministe_automate.langage = self.langage

        etats_a_traiter = [set(self.entree)]
        etats_traites = set()
        while etats_a_traiter:
            new_etat = etats_a_traiter.pop(0) # Prendre le premier état de la liste
            etats_traites.add(tuple(new_etat)) # Ajouter l'état traité à la liste des états traités

            reformat_new_etat = ''.join(sorted(new_etat)) # Reformater l'état en string on reunit les etats
            deterministe_automate.etat.append(reformat_new_etat) # Ajouter les états à l'automate déterministe

            for symb in self.langage: # Pour chaque lettre du langage de l'automate on regarde les transitions possibles pour chaque état de l'automate
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

        self.deterministe = True
        print("L'automate a été déterminisé avec succès.")
        deterministe_automate.affichage_automate("Automate Déterminisé")
        return deterministe_automate

    def est_minimal(self):
        """Minimise l'automate si nécessaire."""

        automate_copie = Automate()
        automate_copie.copier_automate(self)

        automate_minimal = automate_copie.minimiser()

        return self == automate_minimal

    def complementaire(self):
        """Calcule l'automate complémentaire."""

        automate_complementaire = Automate()
        automate_complementaire.copier_automate(self)
        # L'automate complémentaire doit etre deterministe et complet
        if not automate_complementaire.est_complet():
            console.print(
                "\n[yellow]L'automate a besoin d'être complété et determiniser pour obtenir le langage complémentaire.[/yellow]\n")
            automate_complementaire = automate_complementaire.completer()
        nouveaux_etats_finaux = []
        # Ajouter les états qui ne sont pas des états de sortie comme états de sortie
        for etat in automate_complementaire.etat:
            if etat not in automate_complementaire.sortie:
                nouveaux_etats_finaux.append(etat)
        # Mettre à jour les états de sortie de l'automate complémentaire
        automate_complementaire.sortie = nouveaux_etats_finaux
        console.print("[green]\nL'automate complémentaire a été créé avec succès.\n[/green]")
        automate_complementaire.affichage_automate("Automate complémentaire")

    def mot_accepte(self, mot: str):
        """Détermine si un mot est accepté par l'automate."""
        # Initialiser une liste avec l'état d'entrée initial
        etats_a_explorer = [self.entree]

        # Pour chaque symbole dans le mot
        for symbole in mot:
            # Nouvelle liste pour les états à explorer pour le prochain symbole
            nouveaux_etats = []
            transitions_possibles = []
            # Parcourez tous les états actuels dans la liste
            while etats_a_explorer:
                # Obtenez l'état courant de la liste
                etat_courant = etats_a_explorer.pop(0)
                if isinstance(etat_courant, list) and len(etat_courant) == 1:
                    etat_courant = etat_courant[0]

                for etat in etat_courant:
                    transitions_possibles += self.transition.get(etat, {}).get(symbole, [])

                # Ajoutez toutes les transitions possibles à la nouvelle liste d'états
                for etat_prochain in transitions_possibles:
                    # Assurez-vous d'ajouter chaque nouvel état à la liste sans duplication
                    if etat_prochain not in nouveaux_etats:
                        nouveaux_etats.append(etat_prochain)

            etats_a_explorer = nouveaux_etats

            # Si la liste est vide, cela signifie que le mot n'est pas accepté
            if not etats_a_explorer:
                return False

        # Vérifiez si l'un des états courants est un état de sortie de l'automate
        for etat in etats_a_explorer:
            if etat in self.sortie:
                return True

        return False

    def fonction_test(self):
        type = ""
        if self.est_standard():
            print("L'automate est standard")
            self.standard = True
            type += "standard "

        if self.est_complet(True):
            print("L'automate est complet")
            type += "complet "
            self.complet = True
        if self.est_deterministe(True):
            print("L'automate est deterministe")
            self.deterministe = True
            type += "déterministe "
        if self.est_minimal():
            print("L'automate est minimal")
            self.minimal = True
            type += "minimal "

        self.affichage_automate("Automate " + type)

    def partitioner_bloc(self,automate, bloc):
        """Partitionne un bloc d'états en sous-blocs en fonction des transitions."""
        # Utilisez un dictionnaire pour regrouper les états avec des transitions similaires
        sous_blocs = {}

        # Itérer sur chaque état dans le bloc
        for etat in bloc:
            # Créer une clé pour l'état basée sur ses transitions
            cle = tuple((lettre, automate.transition.get((etat, lettre), None)) for lettre in automate.langage)

            # Ajouter l'état au groupe correspondant
            if cle not in sous_blocs:
                sous_blocs[cle] = set()
            sous_blocs[cle].add(etat)

        # Retourner les sous-blocs résultants
        return sous_blocs.values()

    def minimiser(self):
        automate_minimal = Automate()
        automate_minimal.copier_automate(self)
        if not automate_minimal.est_deterministe():
            automate_minimal = automate_minimal.determiniser()
        if not automate_minimal.est_complet():
            automate_minimal = automate_minimal.completer()

        automate_modifie = Automate()
        automate_modifie.copier_automate(automate_minimal)

        automate_copie2 = Automate()
        automate_copie2.copier_automate(automate_minimal)

        automate_copie3 = Automate()
        automate_copie3.copier_automate(automate_minimal)

        # sorted(automate_copie2.transition.values())
        et = []  # Etats terminaux
        ent = []  # Etats non terminaux

        for etat in automate_minimal.etat:
            if etat in automate_minimal.sortie:
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
        # print(motifs_transitions)
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
        # print(transitions_avant_fusion)
        # Separer les groupes de motifs
        # print(automate_modifie)

        # print(automate_modifie)
        for etat in automate_copie3.etat:
            for symbole in automate_modifie.langage:
                destinations = automate_copie3.transition.get(etat, {}).get(symbole, [])
                nouvelles_destinations = []
                for destination in destinations:
                    for motif, etats in motifs_transitions.items():
                        if destination in etats:
                            nouvelles_destinations.append(motif)
                    automate_copie3.transition[etat][symbole] = nouvelles_destinations

        comparaison = True
        while comparaison:
            groupes_separes = {}
            for motif, etats_du_groupe in motifs_transitions.items():
                transitions_du_groupe = {}
                for etat in etats_du_groupe:
                    transitions_du_groupe[etat] = transitions_avant_fusion[etat]

                # print(f"Transitions du groupe de motifs {motif} :", transitions_du_groupe)
                for etat, transitions_etat in transitions_du_groupe.items():
                    # print(transitions_du_groupe)
                    Similaire = False
                    for groupe, transitions_groupe in groupes_separes.items():
                        if transitions_avant_fusion[transitions_groupe[0]] == transitions_etat:
                            if groupes_separes[groupe][0] in motifs_transitions[motif]:
                                groupes_separes[groupe].append(etat)
                                Similaire = True
                                break
                    if not Similaire:
                        groupes_separes[f"NewGroup{len(groupes_separes) + 1}"] = [etat]

            if motifs_transitions == groupes_separes:
                comparaison = False
            else:
                motifs_transitions = groupes_separes
        # print("Groupes séparés :", groupes_separes)
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
                    # print(symbole,":",destinations)
                    if symbole not in transitions_nouvel_etat:
                        transitions_nouvel_etat[symbole] = []
                    for destination in destinations:
                        # print(":", destination)
                        # print(transitions_nouvel_etat, "\n")
                        if destination not in transitions_nouvel_etat[symbole]:
                            transitions_nouvel_etat[symbole].append(destination)
            # print(transitions_nouvel_etat, ":::")
            for symbole, destinations in transitions_nouvel_etat.items():
                # print(symbole,destinations)
                transitions_nouvel_etat[symbole] = "".join(sorted(list(set(destinations))))

            automate_copie2.etat.append(nouvel_etat)
            automate_copie2.transition[nouvel_etat] = transitions_nouvel_etat

            for etat in etats:
                if etat in automate_minimal.entree:
                    new_entree.append(nouvel_etat)
                if etat in automate_minimal.sortie:
                    if nouvel_etat not in new_sortie:
                        new_sortie.append(nouvel_etat)

            for etat in etats:
                if etat != nouvel_etat:
                    del automate_copie2.transition[etat]
                    automate_copie2.etat.remove(etat)
                else:
                    automate_copie2.etat.remove(nouvel_etat)
        # print(automate_copie2.transition)
        # Ajouter chaque transition pour chaque lettre dans un tableau
        tab_etats = []
        for etat, transitions_etat in automate_copie2.transition.items():
            tab_etats.append(etat)
        for etat, transitions_etat in automate_copie2.transition.items():
            for symbole, destination in transitions_etat.items():
                if destination not in tab_etats:
                    destination_present = True
                    for char in destination:
                        char_found = False
                        for etat_existant in tab_etats:
                            if char in etat_existant:
                                char_found = True
                                break
                        if not char_found:
                            destination_present = False
                            break
                    if destination_present:
                        # print(f"La destination {destination} est présente dans les {etat_existant}.")
                        automate_copie2.transition[etat][symbole] = [etat_existant]
        # print(automate_copie2.transition)
        for etat, transitions_etat in automate_copie2.transition.items():
            for symbole, destination in transitions_etat.items():
                if not isinstance(destination, list):
                    automate_copie2.transition[etat][symbole] = [destination]

        automate_copie2.entree = new_entree
        automate_copie2.sortie = new_sortie
        console.print("[green]\nL'automate a été minimisé avec succès.\n[/green]")
        automate_copie2.affichage_automate("Automate Minimal (déterministe,complet)")

        return automate_copie2