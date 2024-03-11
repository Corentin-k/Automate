# Projet d'Automate finis et expressions relationnelles

## Contributeurs
- [Corentin KERVAGORET](https://github.com/Corentin-k)

## Informations
- Projet réalisé dans le cadre de l'UE "Automates et expressions relationnelles" au semestre 4 de la L2 à L'EFREI Paris.
- Le projet est réalisé en Python
<a href="https://www.python.org/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/python-original.svg" alt="Python" height="50" /></a>  

- Les bibliothèques utilisées sont : 
  - [Rich](https://rich.readthedocs.io/en/stable/index.html) pour une meilleure visualisation des automates
  - [Os](https://python.readthedocs.io/en/stable/library/os.html#os.listdir) pour la gestion des fichiers


- Le projet est sous licence MIT

> **Note:** Le projet est en cours de développement et de nouvelles fonctionnalités seront ajoutées au fur et à mesure.

## Introduction
Ce projet à pour but de gérer les automates finis. Il permet nottemment de dire si ceux xi sont déterministes, complets, reconnaissent un mot, sont équivalents, etc. 

## Utilisation
Pour utiliser ce projet, il suffit de cloner le dépôt git et de lancer le fichier `main.py`. Il est possible de modifier les automates dans le fichier `main.py` pour les tester.
Il faut également installer la bibliotheque rich pour une meilleure visualisation des automates. Pour cela, il suffit de lancer la commande `pip install rich` dans un terminal.

## Fonctionnalités

Voir toutes les fonctionnalités dans le wiki du projet [ici](https://github.com/Corentin-k/Automate/wiki)

> :warning: Attention pour pouvoir lire les automates il faut les stocker comme suit dans un fichier.txt dans un repertoire "automates" à la racine du projet :

```txt
# Exemple d'automate

Etat={1,2,3,4} # Lister tous les états de l'automate
Langage={a,b}  # Lister tous les caractères du langage
Entree={1,2}   # Lister tous les états d'entrée
Sortie={3,4}   # Lister tous les états de sortie
Transition=    # Lister toutes les transitions
1: a 3,5; b 4  # Etat: caractere etats d'arrivée,etat d'arrivée,.. ; caractere suivnat etats d'arrivée,etat d'arrivée,...
2: a 2
4: a 3; b 2
```

## License
Ce projet est sous licence MIT. Voir le fichier [LICENSE](