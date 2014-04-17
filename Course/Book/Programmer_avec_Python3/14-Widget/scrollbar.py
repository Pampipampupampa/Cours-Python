#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PRÉSENTATION DU WIDGET SCROLLBAR ET TEXT"""
"COURS 14"

#########################################
### Importation fonction et modules : ###
#########################################

from tkinter import *


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #

##### CLASSE PRINCIPALE #####

class ScrolledText(Frame):
    """Widget composite associant widget text et barre de défilement"""
    def __init__(self, boss, baseFont="Times", width=50, height=25):
        Frame.__init__(self, boss, bd=2, relief=SUNKEN)
        self.boss = boss
        self.text = Text(self, font=baseFont, bg='ivory', bd=1, width=width, height=height)
        scroll = Scrollbar(self, bd=1, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH, padx=2, pady=2)
        scroll.pack(side=RIGHT, expand=NO, fill=Y, padx=2, pady=2)

    def importFichier(self, fichier, encodage="UTF8"):
        """Insertion d'un texte à partir d'un fichier"""
        with open(fichier, "r", encoding=encodage)as op:
            lignes = op.readlines()
        for ligne in lignes:
            self.text.insert(END, ligne)


# ----- Création des Fonctions ----- #


def chercheCible(event=None):
    """Défilement du texte jusqu'à la balise voulue"""
    index = st.text.tag_nextrange('cible', '0.0', END)
    st.text.see(index[0])

#############################
### Programme principal : ###
#############################

# Programme principal:
fen = Tk()
titre = Label(fen, text="Scrollbar avec du texte", font="Times 14 bold italic",
              fg="navy")
titre.pack(padx=10, pady=4)
st = ScrolledText(fen, baseFont="Helvetica 12 normal", width=40, height=10)
st.pack(expand=YES, fill=BOTH, padx=8, pady=8)

# Définition de balises, liaison d'un événement <clic du bouton droit> :
st.text.tag_configure("titre", foreground="brown",
                      font="Helvetica 11 bold italic")
st.text.tag_configure("lien", foreground="blue", font="Helvetica 11 bold")
st.text.tag_configure("cible", foreground="forest green", font="Times 12 bold")
st.text.tag_bind("lien", "<Button-3>", chercheCible)

titre = """Le Corbeau et le Renard
par Jean de la Fontaine, auteur français
\n"""
auteur = """
Jean de la Fontaine
écrivain français (1621-1695)
célèbre pour ses Contes en vers,
et surtout ses Fable, publiées
de 1668 à 1694."""

# Remplissage du widget Text (2 techniques) :
st.importFichier("CorbRenard.txt", encodage="Latin1")
# Formatage à l'ajout:
st.text.insert("0.0", titre, "titre")
st.text.insert(END, auteur, "cible")
# Ajout d'une balise supplémentaire après ajout du texte:
st.text.tag_add("lien", "2.4", "2.23")


# Insertion d'une image :
photo = PhotoImage(file="image/penguin.gif")
st.text.image_create("6.14", image=photo)

fen.mainloop()
