#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""DÉCOUVERTE DU WIDGET SCALE"""
"COURS 13"

###########################################
#### Importation fonction et modules : ####
###########################################


from tkinter import *


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


############# Création des Fonctions #############


def updateLabel(x):
    lab.configure(text='Valeur actuelle = ' + str(x))


###############################
#### Programme principal : ####
###############################


root = Tk()
Scale(root, length=250, orient=HORIZONTAL, label='Réglage : ',
      troughcolor='purple', sliderlength=20, showvalue=0, from_=-25,
      to=125, tickinterval=25, command=updateLabel).pack()
lab = Label(root)
lab.pack()
root.mainloop()
