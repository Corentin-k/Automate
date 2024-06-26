from abc import ABC, abstractmethod


class AutomateInterface(ABC):
    """Interface de base pour les automates-test."""

    @abstractmethod
    def copier_automate(self, autre_automate):
        """Copie un automate."""
        pass

    @abstractmethod
    def est_complet(self):
        """Vérifie si l'automate est complet."""
        pass

    @abstractmethod
    def completer(self):
        """Complète l'automate si nécessaire."""
        pass

    @abstractmethod
    def est_standard(self):
        """Vérifie si l'automate est standard."""
        pass

    @abstractmethod
    def standardiser(self):
        """Standardise l'automate si nécessaire."""
        pass

    @abstractmethod
    def est_deterministe(self):
        """Vérifie si l'automate est déterministe."""
        pass

    @abstractmethod
    def determiniser(self):
        """Déterminise l'automate si nécessaire."""
        pass

    @abstractmethod
    def est_minimal(self):
        """Vérifie si l'automate est minimal."""
        pass

    @abstractmethod
    def minimiser(self):
        """Minimise l'automate si nécessaire."""
        pass

    @abstractmethod
    def affichage_automate(self):
        """Affiche l'automate."""
        pass

    @abstractmethod
    def complementaire(self):
        """Affiche le complémentaire de l'automate"""
        pass

    @abstractmethod
    def mot_accepte(self, mot: str):
        """Détermine si un mot est accepté par l'automate."""
        pass
