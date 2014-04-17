import os

""" permet de tester si une année est bissextile ou non"""

# seule l'erreur TypeError est pertinante ici

test = False
annee = input("choisir l'année :  ")
while test == False:  
    try:
        annee = int(annee)
        test = True
    except TypeError: # erreur de type (int, float, str)
        print(" erreur veuillez renseigner un nombre entier")
        annee = input("choisir l'année :  ")
    except NameError: # une des variables n'a pas était définie
        print(" erreur veuillez renseigner un nombre entier")
        annee = input("choisir l'année :  ")
    except ZeroDivisionError: # impossible de diviser par 0
        print(" erreur veuillez renseigner un nombre différent de 0")
        annee = input("choisir l'année :  ")
    except ValueError as exception_retournee: # erreur de type (impossible de prendre la partie réelle d'une "str"
        # "as" permet de renvoyer l'erreur à l'utilisateur
        print(" erreur veuillez renseigner un nombre entier", "(", exception_retournee, ")")
        annee = input("choisir l'année :  ")
    #finally: """ permet l'excécution de code après un "try" (se lance dans tous les cas même si une erreur est survenue"""
        #instructions à effectuer dans ce cas
    #else: """ permet l'excécution de code si les erreurs en amont ne sont pas survenues """
        #instructions à effectuer dans ce cas


if annee % 400 == 0 or (annee % 4 == 0 and annee % 100 != 0):
    print("bissextile")
else:
    print("non bissextile")

os.system("pause")
