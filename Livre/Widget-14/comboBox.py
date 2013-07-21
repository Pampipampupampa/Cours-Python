#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""ILLUSTRATION DES COMBOS BOX ET DES FENÊTRE EN TOP LEVEL"""
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


class ComboFull(Frame):
    "Widget composite 'Combo box' (champ d'entrée + liste 'déroulante')"
    def __init__(self, boss, item='', items=[], command='', width=10,
                 listSize=5):
        Frame.__init__(self, boss)  # constructeur de la classe parente
        self.boss = boss            # référence du widget 'maître'
        self.items = items          # items à placer dans la boîte de liste
        self.command = command      # fonction à invoquer après clic ou <enter>
        self.item = item            # item entré ou sélectionné
        self.listSize = listSize    # nombre d'items visibles dans la liste
        self.width = width          # largeur du champ d'entrée (en caract.)

        # Champ d'entrée :
        self.entree = Entry(self, width=width)  # largeur en caractères
        self.entree.insert(END, item)
        self.entree.bind("<Return>", self.sortieE)
        self.entree.pack(side=LEFT)

        # Bouton pour faire apparaître la liste associée :
        self.gif1 = PhotoImage(file="image/down.gif")  # ! variable persistante
        Button(self, image=self.gif1, width=15, height=15,
               command=self.popup).pack()

    def sortieL(self, event=None):
        # Extraire de la liste l'item qui a été sélectionné :
        index = self.bListe.curselection()  # renvoie un tuple d'index
        ind0 = int(index[0])                # on ne garde que le premier
        self.item = self.items[ind0]
        # Actualiser le champ d'entrée avec l'item choisi :
        self.entree.delete(0, END)
        self.entree.insert(END, self.item)
        # Exécuter la commande indiquée, avec l'item choisi comme argument :
        self.command(self.item)
        self.pop.destroy()                     # supprimer la fenêtre secondaire

    def sortieE(self, event=None):
        # Exécuter la commande indiquée, avec l'argument-item encodé tel quel :
        self.command(self.entree.get())

    def get(self):
        # Renvoyer le dernier item sélectionné dans la boîte de liste
        return self.item

    def popup(self):
        # Faire apparaître la petite fenêtre secondaire contenant la liste.

        # On commence par récupérer les coordonnées du coin supérieur gauche
        # du présent widget dans la fenêtre principale :
        xW, yW = self.winfo_x(), self.winfo_y()
        # ... et les coordonnées de la fenêtre principale sur l'écran, grâce à
        # la méthode geometry() qui renvoie une chaîne avec taille et coordo. :
        geo = self.boss.geometry().split("+")
        xF, yF = int(geo[1]), int(geo[2])  # coord. coin supérieur gauche
        # On peut alors positionner une petite fenêtre, modale et sans bordure,
        # exactement sous le champ d'entrée :
        xP, yP = xF + xW + 10, yF + yW + 45  # +45 : compenser hauteur ch.Entry
        self.pop = Toplevel(self)            # fenêtre secondaire ("pop up")
        self.pop.geometry("+{}+{}".format(xP, yP))  # positionnement à l'écran
        self.pop.overrideredirect(1)     # => fenêtre sans bordure ni bandeau
        self.pop.transient(self.master)  # => fenêtre modale (1er ground ever)

        # Boîte de liste, munie d'un 'ascenseur' (scroll bar) :
        cadreLB = Frame(self.pop)  # cadre pour l'ensemble des 2
        self.bListe = Listbox(cadreLB, height=self.listSize,
                              width=self.width-1)
        # Liaison de la scrollbar à la Listbox
        scrol = Scrollbar(cadreLB, command=self.bListe.yview)
        # Autorisation vertical en scroll
        self.bListe.config(yscrollcommand=scrol.set)
        self.bListe.bind("<ButtonRelease-1>", self.sortieL)
        self.bListe.pack(side=LEFT)
        scrol.pack(expand=YES, fill=Y)
        cadreLB.pack()
        # Remplissage de la boîte de liste avec les items fournis :
        for it in self.items:
            self.bListe.insert(END, it)


# ----- Création des Fonctions ----- #


if __name__ == "__main__":
    def changeCoul(col):
        fen.configure(background=col)

    def changeLabel():
        lab.configure(text=combo.get())


#############################
### Programme principal : ###
#############################


if __name__ == "__main__":  # --- Programme de test ---
    couleurs = ('navy', 'royal blue', 'steelblue1', 'cadet blue',
                'lawn green', 'forest green', 'yellow', 'dark red',
                'grey80', 'grey60', 'grey40', 'grey20', 'pink')
    fen = Tk()
    combo = ComboFull(fen, item="Ben choisi ...", items=couleurs, command=changeCoul,
                      width=15, listSize=6)
    combo.grid(row=1, columnspan=2, padx=10, pady=10)
    bou = Button(fen, text="Test", command=changeLabel)
    bou.grid(row=3, column=0, padx=8, pady=8)
    lab = Label(fen, text="Bonjour", bg="ivory", width=15)
    lab.grid(row=3, column=1, padx=8)
    fen.mainloop()
