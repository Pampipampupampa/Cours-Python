import os

""" permet de tester le mot clé "raise" """


annee = input("choisir l'année :  ")
try:
    annee = int(annee)
    if annee <= 0:
        raise ValueError("l'année saisie est négative ou nulle") # lève une erreur avant l'interpréteur 
except ValueError as exception_retournee: # erreur de type (impossible de prendre la partie réelle d'une "str"
    # "as" permet de renvoyer l'erreur à l'utilisateur
    print(" erreur veuillez renseigner un nombre positif", "(", exception_retournee, ")")

if annee % 400 == 0 or (annee % 4 == 0 and annee % 100 != 0):
    print("bissextile")
else:
    print("non bissextile")

os.system("pause")
