#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""DÉTAIL DU WIDGET CANVAS """
"COURS 15"

#########################################
### Importation fonction et modules : ###
#########################################


from tkinter import *
from random import randrange


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


class ScrolledCanvas(Frame):
    """Canevas redimensionnable avec barre de défilement"""
    def __init__(self, boss, width=100, height=100, bg="white", bd=2,
                 scrollregion=(0, 0, 300, 300), relief=SUNKEN):
        Frame.__init__(self, boss, bd=bd, relief=relief)
        self.can = Canvas(self, width=width-20, height=height-20, bg=bg,
                          scrollregion=scrollregion, bd=1)
        self.can.grid(row=0, column=0)
        bdv = Scrollbar(self, orient=VERTICAL, command=self.can.yview, bd=1)
        bdh = Scrollbar(self, orient=HORIZONTAL, command=self.can.xview, bd=1)
        self.can.configure(xscrollcommand=bdh.set, yscrollcommand=bdv.set)
        bdv.grid(row=0, column=1, sticky=NS)
        bdh.grid(row=1, column=0, sticky=EW)
        self.bind("<Configure>", self.redim)
        self.started = False

    def redim(self, event):
        "Redimensionne le widget automatiquement"
        if not self.started:
            self.started = True
            return
        # À partir des nouvelles dimensions du cadre, redimensionner le canevas
        # (la diff. de 20 pixels sert à compenser l'épaisseur des scrollbars)
        larg, haut = self.winfo_width()-20, self.winfo_height()-20
        self.can.config(width=larg, height=haut)


##### CLASSE PRINCIPALE #####

class FenPrinc(Tk):
    """Fenêtre principale """
    def __init__(self):
        Tk.__init__(self)
        self.libelle = Label(text="Scroll Game", font="Helvetica 14 bold")
        self.libelle.pack(pady=3)
        terrainJeu = ScrolledCanvas(self, width=500, height=300, relief=SOLID,
                                    scrollregion=(-600, -600, 600, 600), bd=3)
        terrainJeu.pack(expand=YES, fill=BOTH, padx=6, pady=6)
        self.can = terrainJeu.can
        couleurs = ("red", "orange", "yellow", "green", "cyan", "dark blue",
                    "light blue", "violet", "purple", "indian red", "khaki",
                    "firebrick", "plum", "coral")
        for r in range(80):
            x1, y1 = randrange(-600, 450), randrange(-600, 450)
            x2, y2 = x1 + randrange(40, 300), y1 + randrange(40, 300)
            coul = couleurs[randrange((len(couleurs)))]
            self.can.create_oval(x1, y1, x2, y2, fill=coul, outline='black')
        # Ajout d'une petite image GIF :
        self.img = PhotoImage(file='image/linux2.gif')
        self.can.create_image(50, 20, image=self.img)
        # Bouton à attraper :
        self.x, self.y = 50, 100
        self.bou = Button(self.can, text="Start", command=self.start)
        self.fb = self.can.create_window(self.x, self.y, window=self.bou)

    def anim(self):
        if self.run == 0:
            return
        self.x += randrange(-60, 61)
        self.y += randrange(-60, 61)
        self.can.coords(self.fb, self.x, self.y)
        self.libelle.config(text='Cherchez en %s %s' % (self.x, self.y))
        self.after(250, self.anim)

    def stop(self):
        self.run = 0
        self.bou.configure(text="Start", command=self.start)

    def start(self):
        self.bou.configure(text="Attrapez-moi !", command=self.stop)
        self.run = 1
        self.anim()


#############################
### Programme principal : ###
#############################


if __name__ == "__main__":  # --- Programme de test ---
    FenPrinc().mainloop()
