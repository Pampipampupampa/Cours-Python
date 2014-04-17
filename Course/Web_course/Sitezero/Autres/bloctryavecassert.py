import os

""" Test du mot clé "assert" """

valeur1, valeur2 = input("renseigner la première valeur :  "), input("renseigner la seconde valeur positive:  ")
valeur1, valeur2 = int(valeur1), int(valeur2)

try:
    valeur1 / valeur2
    assert valeur2 > 0 # permet de tester la valeur avant de continuer le code
except ZeroDivisionError:
    print("tu sais divisé par 0 toi ? ")
except AssertionError:
    print("tu sais pas lire ? ")

print(" Je vais quand même pas calculer pour toi !!! ")


os.system("pause")
