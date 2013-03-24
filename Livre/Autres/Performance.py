import os

"""EFFICACITE D'UN PROGRAMME"""

n = 2
if n % 2: # formulation efficace
    print("impair")
else:
    print("pair")


    
n = 3
if n % 2 != 1: # formulation non optimale (utilisation de deux comparaisons)
    print("pair")
else:
    print("impair")


while a: # tant que a différent de 0 (plus efficace que "while a != 0")
    
