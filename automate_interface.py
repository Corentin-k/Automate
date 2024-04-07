
from abc import ABC, abstractmethod


class AutomateInterface(ABC):
    """Interface de base pour les automates-test."""

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
