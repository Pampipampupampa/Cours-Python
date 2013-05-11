# -*- coding:Utf8 -*-

import os

##############################################
##                                          ##
##  """UTILISATION DE FONCTION IMPORTEES""  ##
##                                          ##
##############################################

from dessins_tortue import *


"""FONCTION PERMETTANT DE REMPLACER UN CARACTERE PAR UN AUTRE DANS UNE CHAINE"""

def changeCar(ch, ca1 = " ", ca2 = "*", deb = 0, fin = -1): # parametres par defaut si l'utilisateur ne renseigne rien
    if fin == -1:
        fin = len(ch)
    nch = ""
    i = 0
    while i < len(ch):
        if i >= deb and i <= fin and ch[i] == ca1:
            nch = nch + ca2
        else:
            nch = nch + ch[i]
        i += 1
    return nch

print(changeCar("choucroute noire"))
print((changeCar("choucroute noire", "o", "t", fin = 5))) # l'utilisateur renseigne le caractère à  remplacer et par quoi il veut le remplacer et enfin jusqu'à quel caractère il veut que ce oit effectif (ici 6)
print((changeCar("choucroute noire", "o", "t")))

print("")
    




"""FONCTION RENVOYANT LE NOM DU MOIS CORRESPONDANT AU NUMERO"""

def nomMois(numero):
    mois = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    nom = mois[numero - 1]
    return nom

print(nomMois(5))
print("")


"""FONCTION TORTUE"""


up() # relève le crayon
goto(-150, 50) # recule en haut à gauche


i = 0
while i < 10 : # dessine 10 carrés alignés
    down() # abaisse le crayon
    carre(25, "red", 90)
    up()
    forward(30)
    down()
    triangle(25, "red", 120)
    up()
    forward(30)
    down()
    etoile5(25, "blue", 90)
    up()
    forward(30)
    i = i + 1

print("")





"""DOCUMENTATION D'UNE FONCTION"""

def test():
    "ceci est la documentation"
    print("ben je fais rien monsieur")
    
print(test())    
print(test._doc_)


os.system("pause")
