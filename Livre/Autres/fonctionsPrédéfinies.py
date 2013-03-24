import os

"""MODIFIER LE SEPARATEUR QUI EST DE BASE L'ESPACE"""

print("Bonjour", 333, 555, sep = "***") # remplace l'espace par 3 étoiles




"""MODIFIER L'ELEMENT DE FIN"""

n = 0
while n< 6:
    print("ihhan", end = "") # remplace par un espace le retour à la ligne
    n = n + 1

    


"""AIRE ET PERIMETRE D'UN TRIANGLE QUELCONQUE"""

print()
from math import sqrt

a, b, c = float(input("choisir la valeur du premier coté : ")),\
          float(input("choisir la valeur du second coté : ")),\
          float(input("choisir la valeur du troisième coté : "))
peri = a + b + c
aire = sqrt((peri/2) * ((peri/2) - a) * ((peri/2) - b) * ((peri/2) - c))
print("Le triangle a un périmètre de ", peri, " et une aire de ", aire, end = "\n")




"""ENCODAGE DANS UNE LISTE D'UNE INFINITE DE VALEURS"""

liste = []
valeur = "non nulle" # permet d'amorcer la boucle
while valeur != " ": # si il met un espace + entrée, la boule se stop
    valeur = input("entrer la première valeur de votre liste : ")
    if valeur != " ":
        liste.append(valeur) # ajout à la liste des valeurs entrantes
        
print(liste)    
    
