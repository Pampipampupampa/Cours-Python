#! /usr/bin/env python
# -*- coding:Utf8 -*-

import os

""" Programme simulant un jeux de roulette simplifié"""

# appel des fonctions utiles
from random import randrange
from math import ceil


import numpy as np


argent = -2
while argent < 0:
    argent = input(" Choisir le montant de départ :  ")
    try:
        argent = ceil(float(argent))
    except ValueError:
        print("met un nombre, on ne triche pas ici !!!")
        argent = -2
        continue
    if argent <= 0:
        print("faut mettre de l'argent sur la table bonhomme !!!")

while argent > 0:  # tant qu'il lui reste de l'argent il peut rejouer
    print("il vous reste", argent, "euros")

    # vérifie que l'utilisateur ne met pas plus que ce qu'il lui reste en jeu
    mise = -2  # perm et de démarrer la boucle
    while mise < 0 or mise > argent:
        mise = input("choisir la mise de départ :  ")  # quelle mise ?
        try:
            mise = ceil(float(mise))
        except ValueError:
            print("vous n'avez pas choisi de nombre")
            mise = -2
            continue
        if mise < 0:
            print("une mise est toujours positive")
        if mise > argent:
            print("Il ne vous reste que ", argent, "euros, veuillez choisir un autre montant")

    resultat = randrange(50)  # choisi un nombre aléatoirement entre 0 et 49

    # vérifie l'existance du numéro
    numero = 100
    while numero > 49 or numero < 0:
        numero = input("choisir un numéro entre 0 et 49 :  ")  # quel numero ?
        try:
            numero = ceil(float(numero))
        except ValueError:
            print("vous n'avez pas choisi de nombre")
            numero = 100
            continue
        if numero < 0 or numero > 49:
            print("merci d'inscrire un nombre existant sur la roulette")

    # test la parité du nombre tombé
    if resultat % 2 == 0:
        resultatparite = "pair"
    else:
        resultatparite = "impair"

    # test la parité du nombre joué
    if numero % 2 == 0:
        numeroparite = "pair"
    else:
        numeroparite = "impair"

    print("Le numéro choisie est le ", numero, "et le numéro sortant est le ", resultat)  # indique les numéros (joué et gagnant)

    # test afin de savoir si il gagne ou perd de l'argent
    if resultat == numero:
        argent = ceil(4 * mise + argent)
        print("Well done, You win ", mise * 4, "euros")
    elif resultat != numero and numeroparite == resultatparite:
        argent = ceil(1.5 * mise + argent)
        print("Well done, You win ", mise * 1.5, "euros")
    else:
        argent = ceil(argent - mise)
        print("Bad luck, You lose ", mise, "euros")

print("Vous avez perdu misérablement, bye bye . . . ")  # il a plus d'argent

os.system("pause")
