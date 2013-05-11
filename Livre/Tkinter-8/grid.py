#! /usr/bin/env python
# -*- coding:Utf8 -*-


" INITIATION A LA METHODE GRID"

############# Importation fonction et modules : ################

from tkinter import *

############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############



############## Programme principal : #################

fen1 = Tk()

"Sticky permet l'alignement vers un des points cardinaux"
"Ici on ajouter un Champs Label ans déclarer de variables et on lui applique directement la méthode grid pour le placer"
"Utile si on ne va pas réutiliser la variable, on économise ainsi de la mémoire"
Label(fen1, text = "Champs numéro 1 : ").grid(row = 0, padx = 10, pady = 10, sticky = E)
Label(fen1, text = "Champs 2 : ").grid(row = 1, padx = 10, pady = 10, sticky = E)
Label(fen1, text = "Troisième : ").grid(row = 2, padx = 10, pady = 10, sticky = E)

"Ici on déclare une variable car on veut pouvoir récupérer sa valeur"
entry1 = Entry(fen1)
entry2 = Entry(fen1)
entry3 = Entry(fen1)

"Juste pour tester"
check1 = Checkbutton(fen1, text = 'coche pour voir minus')

"Création d'un widget Canvas contenant une image"
can1 = Canvas(fen1, width = 160, height = 160, bg = 'white')
photo = PhotoImage(file = '/home/pampi/Images/ImagePython/permis.gif')
item = can1.create_image(80, 80, image = photo) # position du centre de l'image, donc ici au centre du canvas

"Permet de positionner le widget sur une grille virtuelle et donc\
de permettre plus de possibilités que la méthode pack"
entry1.grid(row = 0, column = 1, padx = 10, pady = 10)
entry2.grid(row = 1, column = 1, padx = 10, pady = 10)
entry3.grid(row = 2, column = 1, padx = 10, pady = 10)
can1.grid(row = 1, column = 3, rowspan = 3, padx = 10, pady = 10)
check1.grid(columnspan = 2, padx = 10, pady = 10)


fen1.mainloop()
















