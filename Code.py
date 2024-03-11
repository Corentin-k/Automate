import inspect
from rich import print
from rich.syntax import Syntax
from rich.tree import Tree
from Automate import *
def afficher_code():
    tree = Tree("Automate")
    tree.add("__init__")
    tree.add("__str__")
    tree.add("affichage_automate")
    tree.add("est_complet")
    print(tree)
    print("Quelle fonction voulez-vous afficher ?")
    fonction = input(">>> ")
    fonction="Automate."+fonction
    code=inspect.getsource(eval(fonction))
    syntax = Syntax(code, "python", theme="ansi_dark", line_numbers=True)
    print(syntax)