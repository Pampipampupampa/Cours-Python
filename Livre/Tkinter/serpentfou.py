#! /usr/bin/env python
# -*- coding:Utf8 -*-



################################################################
############# Importation fonction et modules : ################
################################################################



from tkinter import *




###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



def start_it():
    "Démarrage de l'animation"
    global flag
    if flag ==0:
        flag =1
        move()



def stop_it():
    "Arrêt de l'animation"
    global flag
    flag =0
    

def move():
    "Animation du serpent par récursivité"
    global flag
    # Principe du mouvement opéré : on déplace le carré de queue, dont les
    # caractéristiques sont mémorisées dans le premier élément de la liste
    # <serp>, de manière à l'amener en avant du carré de tête, dont les
    # caractéristiques sont mémorisées dans le dernier élément de la liste.
    # On définit ainsi un nouveau carré de tête pour le serpent, dont on
    # mémorise les caractéristiques en les ajoutant à la liste.
    # Il ne reste plus qu'à effacer alors le premier élément de la liste,
    # et ainsi de suite ... :
    c = serp[0]             # extraction des infos concernant le carré de queue
    cq = c[0]               # réf. de ce carré (coordonnées inutiles ici)
    l =len(serp)            # longueur actuelle du serpent (= n. de carrés)
    c = serp[l-1]           # extraction des infos concernant le carré de tête
    xt, yt = c[1], c[2]     # coordonnées de ce carré
    # Préparation du déplacement proprement dit.
    # (cc est la taille du carré. dx & dy indiquent le sens du déplacement) : 
    xq, yq = xt+dx*cc, yt+dy*cc             # coord. du nouveau carré de tête
   
    # Vérification : a-t-on atteint les limites du canevas ? :
    if xq<0 or xq>canX-cc or yq<0 or yq>canY-cc:
        flag =0             # => arrêt de l'animation
        can.create_text(canX/2, 200, anchor =CENTER, text ="Perdu !!!", fill ="orange", font="Arial 16 bold")
   
    # Mouvement du serpent et effacement du bloc de fin 
    can.coords(cq, xq, yq, xq+cc, yq+cc)    # déplacement effectif
    serp.append([cq, xq, yq])     # mémorisation du nouveau carré de tête
    del(serp[0])                  # effacement (retrait de la liste)
    
    # Appel récursif de la fonction par elle-même (=> boucle d'animation) : 
    if flag >0:
        fen.after(50, move)    



def go_left(event =None):
    global dx, dy
    dx, dy = -1, 0



def go_right(event =None):
    global dx, dy
    dx, dy = 1, 0



def go_up(event =None):
    global dx, dy
    dx, dy = 0, -1
    


def go_down(event =None):
    global dx, dy
    dx, dy = 0, 1



######################################################
############## Programme principal : #################
######################################################



"Variables à utilisation globales"
canX, canY = 500, 500   # dimensions du canevas
x, y, cc = 100, 100, 15 # coordonnées et coté du premier carré
flag =0                 # commutateur pour l'animation
dx, dy = 1, 0           # indicateurs pour le sens du déplacement



"Elements principaux"
fen =Tk()
can =Canvas(fen, bg ='white', height =canX, width =canY)
can.pack(padx =10, pady =10)
bou1 =Button(fen, text="Start", width =10, command =start_it)
bou1.pack(side =LEFT)
bou2 =Button(fen, text="Stop", width =10, command =stop_it)
bou2.pack(side =LEFT)



"Serpent initial"
# On mémorisera les infos concernant les carrés créés dans une liste de listes :
serp =[]                        # liste vide
x, y, cc = 100, 100, 10         # coordonnées et coté du premier carré
flag =0                         # commutateur pour l'animation
# Création et mémorisation des 5 carrés : le dernier (à droite) est la tête.
i =0
while i <5:
    carre =can.create_rectangle(x, y, x+cc, y+cc, fill="green")
    # Pour chaque carré, on mémorise une petite sous-liste contenant
    # 3 éléments : la référence du carré et ses coordonnées de base :
    serp.append([carre, x, y])
    x =x+cc                     # le carré suivant sera un peu plus à droite
    i =i+1



"Animation du serpent fou"
fen.bind("<Left>", go_left)         # Attention : les événements clavier
fen.bind("<Right>", go_right)       # doivent toujours être associés à la
fen.bind("<Up>", go_up)             # fenêtre principale, et non au canevas
fen.bind("<Down>", go_down)         # ou à un autre widget.



fen.mainloop()
