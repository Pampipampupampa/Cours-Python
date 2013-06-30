#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""CONSTRUCTION D'UN PANNEAU DE CONTRÔLE À 3 CURSEURS"""
"COURS 13"

###########################################
#### Importation fonction et modules : ####
###########################################


from tkinter import *
from math import pi


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


class ChoixVibratoire(Frame):
    """Curseur pour choisir amplitude, fréquence, et phase d'une vibration"""
    def __init__(self, boss=None, coul='red'):
        Frame.__init__(self)
        self.freq, self.phase, self.ampl = 0, 0, 0
        self.coul = coul
        # Création de la case à cocher
        self.chk = IntVar()  # Instanciation d'un Objet variable tkinter
        Checkbutton(self, text='Afficher', variable=self.chk, fg=self.coul,
                    command=self.setCurve).pack(side=LEFT)
        # Création des 3 widgets curseurs
        Scale(self, length=150, orient=HORIZONTAL, label='Fréquence : ',
              troughcolor='dark grey', sliderlength=20, showvalue=0, from_=1.,
              to=9., tickinterval=2,
              command=self.setFrequence).pack(side=LEFT)
        Scale(self, length=150, orient=HORIZONTAL, label='Phase (degrès) : ',
              troughcolor='dark grey', sliderlength=20, showvalue=0,
              from_=-180, to=180, tickinterval=90,
              command=self.setPhase).pack(side=LEFT)
        Scale(self, length=150, orient=HORIZONTAL, label='Amplitude : ',
              troughcolor='dark grey', sliderlength=20, showvalue=0, from_=1.,
              to=10., tickinterval=2,
              command=self.setAmplitude).pack(side=LEFT)

    def setCurve(self):
        self.event_generate('<Control-Z>')

    def setFrequence(self, f):
        self.freq = float(f)
        self.event_generate('<Control-Z>')

    def setPhase(self, p):
        # TypeError: can't multiply sequence by non-int of type 'float'
        # ---> On doit créer une variable intermédiaire
        pp = float(p)
        self.phase = pp*2*pi/360  # Conversion en radians
        self.event_generate('<Control-Z>')

    def setAmplitude(self, a):
        self.ampl = float(a)
        self.event_generate('<Control-Z>')


############# Création des Fonctions #############


def afficherTout(event=None):
    # On récupère les informations des divers éléments
    lab.configure(text='{0} - {1} - {2} - {3}'.format(fra.chk.get(), fra.freq, fra.phase, fra.ampl))


###############################
#### Programme principal : ####
###############################


if __name__ == '__main__':
    root = Tk()
    fra = ChoixVibratoire(root, 'navy')
    fra.pack(side=TOP)
    lab = Label(root, text='test')
    lab.pack()
    root.bind('<Control-Z>', afficherTout)
    root.mainloop()
