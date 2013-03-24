#! /usr/bin/env python
# -*- coding:Utf8 -*-

import os

"""GRAIN DE RIZ ET ECHEC"""

"""afficher le nombre de grains de riz sur chaques cases d'un jeu d'échec
   (64 cases)de telle sorte que le nombre de riz double à chaque fois """

# en nombre flottant
case = 1
riz = 1.0
while case <= 64:
    print("on place ", riz, "riz sur la case", case)
    riz = float(riz + riz) # on double le nombre de riz à chaque fois
    case += 1 # on change de case
    

# en nombre entier
case = 1
riz = 1
while case <= 64:
    print("on place ", riz, "riz sur la case", case)
    riz, case = int(riz + riz), case + 1
    
os.system("pause") # empêche le programme de fermer sans que l'utilisteur le veuille
