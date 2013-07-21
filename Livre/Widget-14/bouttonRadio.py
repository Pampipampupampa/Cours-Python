#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""UTILISATION DU BOUTTON RADIO"""
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


class RadioDemo(Frame):
    """Démonstration du widget radio"""
    def __init__(self, boss=None):
        """Champ d'entrée avec 4 boutons radio"""
        Frame.__init__(self)
        self.pack()  # Possible de le pack avant
        self.texte = Entry(self, width=30, font='Arial 14')
        self.texte.insert(END, "La programmation, c'est génial")
        self.texte.pack(padx=8, pady=8)
        stylePoliceTk = ['normal', 'bold', 'italic', 'bold italic']
        stylePoliceFr = ['Normal', 'Gras', 'Italique', 'Gras/Italique']
        self.choixPolice = StringVar()
        self.choixPolice.set(stylePoliceTk[0])
        # Création des 4 boutons radio avec une boucle for
        for n in range(4):
            bout = Radiobutton(self, text=stylePoliceFr[n],
                               variable=self.choixPolice,  # Variable tkinter
                               value=stylePoliceTk[n], command=self.chPolice)
            bout.pack(side=LEFT, padx=5)

    def chPolice(self):
        """Remplacement du style de la police actuelle"""
        police = "Arial 15 " + self.choixPolice.get()
        # Le style de la police peut être une chaine de caractères si
        # elle ne comporte pas d'espaces sinon il faut renseigner
        # un tuple ('nom', taille, 'style')
        self.texte.configure(font=police)


#############################
### Programme principal : ###
#############################


if __name__ == '__main__':
    RadioDemo().mainloop()
