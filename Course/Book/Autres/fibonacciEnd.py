import os

"""exercices"""

"""suite de fibonacci"""

a, b, c = 1, 1, 1
while c < 20:
    print(b, end = " ") # remplace le retour à la ligne par un espace
    a, b, c = b, a + b, c + 1


"""table de 7"""

i = 1
while i <= 20:
    valeur = i * 7
    print(i, " fois ", 7, " = ", valeur)
    i += 1



"""conversion d'euros en dollar"""

euro = 1
fin = "\n"
while euro <= 16384:
    dollar = euro * 1.65
    print(euro, " euros ", " = ", dollar, " dollars ", ":::", end = fin)
    fin, euro = " ", euro + euro


"""tripler un nombre choisi aléatoirement"""

from random import randrange # importe fonction aléatoire

nombre = randrange(10)
i = 1
print()
print(nombre, end = " ")
while i <= 12: # limite évitant une boucle infinie
    i += 1
    nombre = nombre *3
    print(nombre, end = " ")
    

