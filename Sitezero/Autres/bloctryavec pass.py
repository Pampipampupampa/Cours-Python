import os

""" Test du mot clé "pass" """

valeur1, valeur2 = input("renseigner la première valeur :  "), input("renseigner la seconde valeur :  ")
valeur1, valeur2 = int(valeur1), int(valeur2)

try:
    valeur1 / valeur2
except ZeroDivisionError as erreur:
    print("erreur survenue : ", erreur)
    pass # continue même si erreur trouvée (utilité ?)

os.system("pause")
