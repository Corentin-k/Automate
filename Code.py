import inspect
from rich import print
from rich.syntax import Syntax
from rich.tree import Tree
from Automate import *


# Lien vers la documentation de la fonction inspect
# https://docs.python.org/3/library/inspect.html#inspect.getsource

def afficher_code():
    tree = Tree("Automate")
    for name, obj in inspect.getmembers(Automate):
        if inspect.isfunction(obj):
            tree.add(name)
    print(tree)
    print("Quelle fonction voulez-vous afficher ?")
    fonction = input(">>> ")
    try:
        fonction = "Automate." + fonction
        code = inspect.getsource(eval(fonction))
        syntax = Syntax(code, "python", theme="ansi_dark", line_numbers=True)
        print(syntax)
    except AttributeError:
        print("La fonction spécifiée n'existe pas dans Automate.")
    except TypeError:
        print("La fonction spécifiée n'est pas un objet que vous pouvez afficher.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
