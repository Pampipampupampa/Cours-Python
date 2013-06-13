#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME TESTANT L'ÉFFICACITÉ DE LA FONCTION RANDOM"""
"EXERCICE 10.43 CORRECTION LIVRE"

###########################################
#### Importation fonction et modules : ####
###########################################


from random import random           # tire au hasard un réel entre 0 et 1


###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################


###############################
#### Programme principal : ####
###############################

# Exercice 10.43 : Vérification de la génération de nombres
n = input("Nombre de valeurs à tirer au hasard (défaut = 1000) : ")
if n == "":
    nVal = 1000
else:
    nVal = int(n)
n = input("Nombre de fractions dans l'intervalle 0-1 (entre 2 et {}, "
          "défaut =5) : ".format(nVal//10))
if n == "":
    nFra = 5
else:
    nFra = int(n)

if nFra < 2:
    nFra = 2
elif nFra > nVal/10:
    nFra = nVal/10

print("Tirage au sort des", nVal, "valeurs ...")
listVal = [0]*nVal                      # créer une liste de zéros
for i in range(nVal):                   # puis modifier chaque élément
    listVal[i] = random()

print("Comptage des valeurs dans chacune des", nFra, "fractions ...")
listCompt = [0]*nFra                    # créer une liste de compteurs

# parcourir la liste des valeurs :
for valeur in listVal:
    # trouver l'index de la fraction qui contient la valeur :
    index = int(valeur*nFra)
    # incrémenter le compteur correspondant :
    listCompt[index] = listCompt[index] + 1

# afficher l'état des compteurs :
for compt in listCompt:
    print(compt, end=' ')
print()
