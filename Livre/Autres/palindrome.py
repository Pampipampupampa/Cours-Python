import os

"""PALINDROME OU PAS PALINDROME"""

nom = "ours"
mon = ""
i = len(nom) - 1 # permet de commencer par le dernier caractère

while i >= 0: # tant que le premier caractère (caractère 0) n'est pas incrémenté
              # on continue la boucle
    mon = mon + nom[i]
    i = i - 1
   
if nom == mon: # on vérifie que le mot se lie dans les 2 sens
    print(nom, "est un palindrome mon petit")
else: # si il se lit que dans un sens 
    print("et ben non mon grand")


    
""" REPETITION DES JOURS DE LA SEMAINE """


jour = ['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi']
a, b = 0, 0
while a < 25:
    a = a + 1
    b = a % 7 # permet de naviguer dans la liste en avancant de 1 jour par itération
    print(a, jour[b])
