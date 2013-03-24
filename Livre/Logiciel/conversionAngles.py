import os

"""CONVERTIR DEGRES EN RADIANS"""

from math import pi

choix = "e" # base afin d'amorcer la boucle

while choix != "Q": # permet à l'utilisateur de choisir entre une nouvelle conversion ou quitter
    
    choix = input(""" ""rad"" pour radian vers degres ,\n ""deg"" pour degrès vers radians ,\n ""Q"" pour quitter l'application : """)
    
    try:
        choix == "rad" or choix == "deg" or choix == "Q" # test si donnée utilisateur correcte
    except ValueError:
        print("met rad ou deg")
        choix = "e"
        continue # permet de directement passer les choix suivants et de relancer la boucle
    
    
    if choix == "deg": # pasage degres ves radians
        degre, minute, seconde = float(input("nombre de degres : ")),\
                             float(input("nombre de minutes : ")),\
                             float(input("nombre de seconde : "))     
        seconde1 = seconde / 60 # passage des secondes en minutes
        minute1 = (minute + seconde1) / 60 # passage des secondes et des minutes en degres
        degre1 = float(degre + minute1) # degres totaux
        radian = degre1 * 2 * pi / 360 # conversion
        print(degre, "degres", minute, "minutes", "et", seconde, "secondes \ndonne en radians : ",radian) # renvoie la valeur en radians de l'angle donné en degre

    elif choix == "rad": # passage radians ver degres
        radian = float(input("entrez la valeur de l'angle en radians : "))
        
        # séparation des degres minutes et secondes
        degre1 = (radian * 360) / (2 * pi)
        minute = (degre1 - int(degre1)) * 60
        seconde = (minute - int(minute)) * 60
        degre = int(degre1)
        print(radian, "radians donne", degre, " degres ", minute, " minutes ", seconde, " secondes ") # inscrit la valeur de l'angle en degre minute et secondes
        print(radian, "radians donne en degre : ", degre1)# inscrit la valeur en degres (non fractionnée) de l'angle en radians

    else:
        print ("""choisir entre ""rad"" et ""deg"" !!!! """) # averti l'utilisateur sur son erreur
        
os.system("pause")
