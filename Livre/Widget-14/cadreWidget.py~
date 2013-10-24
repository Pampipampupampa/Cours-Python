#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME REGROUPANT LES OPTIONS DE BORDURES TKINTER"""
"COURS 14 : AFFECTATIONS AVEC DES TUPLES"

#########################################
### Importation fonction et modules : ###
#########################################


from tkinter import *


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


# ----- Création des Fonctions ----- #


#############################
### Programme principal : ###
#############################


fen = Tk()
fen.title("Regroupe les différents types de bordures")
fen.geometry("500x300")  # Permet de définir la taille de la fenêtre

fg = Frame(fen, bg='#80C0C0')
fg.pack(side=LEFT, padx=5)
fint = [0] * 6  # Création de 6 éléments pour acceuillir les frames
conteneur = [(0, 'grey50', RAISED, 'Relief sortant'),
             (1, 'grey60', SUNKEN, 'Relief entrant'),
             (2, 'grey70', FLAT, 'Pas de relief'),
             (3, 'grey80', RIDGE, 'Crête'),
             (4, 'grey90', GROOVE, 'Sillon'),
             (5, 'grey100', SOLID, 'Bordure')]
# Utilisation d'une boucle et du conteneur pour réaliser les affectations
# Utilisation de tuples afin de rendre compact cette action
for (n, coul, bord, txt) in conteneur:
    fint[n] = Frame(fg, bd=2, relief=bord)
    e = Label(fint[n], text=txt, width=15, bg=coul)
    e.pack(side=LEFT, padx=5, pady=5)
    fint[n].pack(side=TOP, padx=10, pady=5)

fd = Frame(fen, bg='#D0D0B0', bd=2, relief=GROOVE)
fd.pack(side=RIGHT, padx=5)

can = Canvas(fd, width=80, height=80, bg='white', bd=2, relief=SOLID)
can.pack(padx=15, pady=15)
bou = Button(fd, text='Bouton')
bou.pack()

fen.mainloop()
