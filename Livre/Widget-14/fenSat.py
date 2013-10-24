#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME UTILISANT <TOPLEVEL> ET UN RAPPORT ENTRE LES FENÊTRES SATELLITE"""
"COURS 14"

#########################################
### Importation fonction et modules : ###
#########################################

from tkinter import *

############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


class FunnyButton(Button):
    """Petit boutton virant au rouge suite à un clic"""
    def __init__(self, boss, **Arguments):
        Button.__init__(self, boss, bg='dark grey', fg='white', bd=5,
                        activebackground='red', activeforeground='yellow',
                        font=('Helvetica', 12, 'bold'), **Arguments)


class SpinBox(Frame):
    """Widget composite comportant des bouttons pour régler la dimension"""
    def __init__(self, boss, largC=5, largB=2, vlist=[0], liInd=0, orient=Y):
        Frame.__init__(self, boss)
        self.vlist = vlist    # Liste des valeurs à présenter
        self.liInd = liInd    # Valeur par défaut pour les dimensions
        if orient == Y:
            s, augm, dimi = TOP, '^', 'v'
        else:
            s, augm, dimi = RIGHT, '>', '<'
        Button(self, text=augm, width=largB, command=self.up).pack(side=s)
        self.champ = Label(self, bg='white', width=largC,
                           text=str(vlist[liInd]), relief=SUNKEN)
        self.champ.pack(pady=3, side=s)
        Button(self, text=dimi, width=largB, command=self.down).pack(side=s)

    def up(self):
        if self.liInd < len(self.vlist)-1:
            self.liInd += 1
        else:
            self.bell()
        self.champ.configure(text=str(self.vlist[self.liInd]))

    def down(self):
        if self.liInd > 0:
            self.liInd -= 1
        else:
            self.bell()
        self.champ.configure(text=str(self.vlist[self.liInd]))

    def get(self):
        return self.vlist[self.liInd]


class FenDessin(Toplevel):
    """Fenêtre sat modale contenant le dessin"""
    def __init__(self, **Arguments):
        Toplevel.__init__(self, **Arguments)
        self.geometry("250x200+100+240")
        self.overrideredirect(1)     # Aucunes bordures et bandeaux
        self.transient(self.master)  # Fenêtre modale
        self.can = Canvas(self, bg='ivory', width=200, height=150)
        self.img = PhotoImage(file="image/papillon2.gif")
        self.can.create_image(90, 80, image=self.img)
        self.can.pack(padx=20, pady=20)


class FenControle(Toplevel):
    """Fenêtre permettant de contrôler la taille de <FenDessin>"""
    def __init__(self, boss, **Arguments):
        Toplevel.__init__(self, boss, **Arguments)
        self.geometry("250x200+400+230")
        self.resizable(width=0, height=0)  # Bloque le redimensionnement
        choix = (10, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300)
        self.spX = SpinBox(self, largC=5, largB=1, vlist=choix,
                           liInd=5, orient=X)
        self.spY = SpinBox(self, largC=5, largB=1, vlist=choix,
                           liInd=5, orient=Y)
        self.spX.pack(pady=5)
        self.spY.pack(pady=5)
        FunnyButton(self, text='Redimensionner',
                    command=boss.redimF1).pack(pady=5)


##### CLASSE PRINCIPALE #####


class Demo(Frame):
    """Fenêtre principale permettant l'accès aux fenêtres filles"""
    def __init__(self):
        Frame.__init__(self)
        self.master.geometry("400x300+200+200")
        self.master.config(bg='cadet blue')
        FunnyButton(self, text="Top 1", command=self.top1).pack(side=LEFT)
        FunnyButton(self, text="Top 2", command=self.top2).pack(side=LEFT)
        FunnyButton(self, text="Quitter", command=self.quit).pack()
        self.pack(side=BOTTOM, padx=10, pady=10)

    def top1(self):
        self.fen1 = FenDessin(bg="grey")

    def top2(self):
        self.fen2 = FenControle(self, bg="khaki")

    def redimF1(self):
        dimX, dimY = self.fen2.spX.get(), self.fen2.spY.get()
        self.fen1.can.config(width=dimX, height=dimY)


# ----- Création des Fonctions ----- #


#############################
### Programme principal : ###
#############################


if __name__ == '__main__':
    Demo().mainloop()
