#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""RÉALISATION PROTOTYPE CANON"""
"COURS 15"

#########################################
### Importation fonction et modules : ###
#########################################

from tkinter import *
from math import pi, sin, cos
from random import randrange

############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################

# ----- Création des Classes ----- #


class Canon(object):
    """Prototype d'un canon graphique"""
    def __init__(self, boss, x, y, sens, coul, id):
        self.boss = boss
        self.appli = boss.master
        self.id = id
        self.coul = coul
        self.sens = sens  # Accepte 1(droite) ou -1(gauche)
        self.x1 = x
        self.y1 = y
        self.longCanon = 30
        self.x2, self.y2 = x + self.longCanon * self.sens, y
        self.buse = boss.create_line(self.x1, self.y1, self.x2, self.y2,
                                     width=10, fill='black')
        self.rc = 15
        self.corps = boss.create_oval(x-self.rc, y-self.rc, x+self.rc,
                                      y+self.rc, fill=self.coul)
        self.obus = boss.create_oval(-10, -10, -10, -10, fill='red')
        self.anim = False  # interrupteur d’animation
        self.explo = False  # indicateur d'explosion
        # retrouver la largeur et la hauteur du canevas :
        self.xMax = int(boss.cget('width'))  # Transformation en nombre
        self.yMax = int(boss.cget('height'))

    def deplacer(self, x, y):
        """Modifier la position du canon"""
        dx, dy = x - self.x1, y - self.y1
        self.boss.move(self.buse, dx, dy)
        self.boss.move(self.corps, dx, dy)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def orienter(self, angle):
        """Choix de l'angle du canon"""
        self.angle = float(angle)*2*pi/360
        self.x2 = int(self.x1 + self.longCanon * cos(self.angle) * self.sens)
        self.y2 = int(self.y1 - self.longCanon * sin(self.angle))
        self.boss.coords(self.buse, self.x1, self.y1, self.x2, self.y2)

    def feu(self):
        "déclencher le tir d'un obus"
        if not (self.anim or self.explo):
            self.anim = True
            # position de départ de l'obus (bouche canon)
            self.boss.coords(self.obus, self.x2 - 3, self.y2, self.x2 + 3,
                             self.y2)
            v = 20  # vitesse initiale
            # composantes verticale et horizontale de cette
            self.vy = -v * sin(self.angle)
            self.vx = v * cos(self.angle) * self.sens
            self.animerObus()
            return True   # Signal envoie du coup
        else:
            return False  # Signal aucuns envois

    def animerObus(self):
        "animation de l'obus (trajectoire balistique)"
        if self.anim:
            self.boss.move(self.obus, int(self.vx), int(self.vy))
            c = tuple(self.boss.coords(self.obus))
            # coord. résultantes
            x0, y0 = c[0] + 3, c[1] + 3  # coord. du centre de l'obus
            self.testObstacle(x0, y0)   # a-t-on atteint un obstacle ?
            self.vy += .4
            self.boss.after(25, self.animerObus)
        else:
            # Modifier position du canon pour nouveau tir
            self.boss.after(250, self.finAnimation)

    def testObstacle(self, x0, y0):
        "Vérifie si le boulet entre en contact avec un élément"
        if y0 > self.yMax or x0 > self.xMax or x0 < 0:
            self.anim = False
            return
        # récupérer la description de tous les canons présents :
        self.guns = self.appli.dictionnaireCanons()
        # analyser le dictionnaire des canons pour voir si les coord.
        # de l'un d'entre eux sont proches de celles de l'obus :
        for id in self.guns:
            gun = self.guns[id]  # On récupère les canons un par un
            if x0 < gun.x1 + self.rc and x0 > gun.x1 - self.rc and\
               y0 < gun.y1 + self.rc and y0 > gun.y1 - self.rc:
                self.anim = False  # On stop la trajectoire du boulet
                # On dessine l'explosion (cerclejaune)
                self.explo = self.boss.create_oval(x0-12, y0-12, x0+12, y0+12,
                                                   fill='yellow', width=2)
                self.hit = id  # On récupère la cible
                self.boss.after(200, self.finExplosion)  # On nettoie l'impact
                break

    def finExplosion(self):
        """Efface l'explosion et réinitialise l'état self.explo"""
        self.boss.delete(self.explo)
        self.explo = False
        # Signale un coup gagnant à l'application avec tireur et touché
        self.appli.goal(self.id, self.hit)

    def finAnimation(self):
        """Réinitialise l'animation et la position du boulet"""
        self.boss.coords(self.obus, -10, -10, -10, -10)
        # Modification de la position des canons
        self.appli.modifPosition()


class PupitreCanon(Frame):
    """Ensemble de paramètres pour le canon + score joueur"""
    def __init__(self, boss, canon):
        Frame.__init__(self, bd=3, relief=GROOVE)
        self.boss = boss
        self.canon = canon
        self.score = 0
        # Widget permettant la modification de l'orie&ntation du canon
        self.scale1 = Scale(self, label="Modifier orientation", from_=90,
                            to=-20, command=self.orienter,
                            troughcolor=canon.coul)
        self.scale1.pack(side=LEFT, pady=5, padx=5)
        self.scale1.set(25)  # Orientation de base
        # Ajout du nom du joueur ou du canon
        Label(self, text=canon.id).pack(side=TOP, pady=5)
        # Ajout du boutton pour déclencher le tir
        self.boutTir = Button(self, text='Feu !', command=self.tirer)
        self.boutTir.pack(side=BOTTOM, padx=5, pady=5)
        # Ajout du nombre des points
        Label(self, text="points").pack()
        self.points = Label(self, text='0', bg='white')
        self.points.pack()
        # Modifier la position de la frame en fonction de la position du canon
        if canon.sens == -1:
            self.pack(padx=5, pady=5, side=RIGHT)
        else:
            self.pack(padx=5, pady=5, side=LEFT)

    def tirer(self):
        """Envoie du boulet de canon"""
        self.canon.feu()

    def orienter(self, angle):
        """Modifier l'orientation de la buse du canon"""
        self.canon.orienter(angle)

    def modifScore(self, p):
        """Ajout du score lors d'une explosion"""
        self.score += p
        # self.points.config(text='{}'.config(self.score))  # Fonctionne pas
        self.points.config(text=' %s ' % self.score)


##### CLASSE PRINCIPALE #####


class Application(Frame):
    """Regroupe l'ensemble  frame + canon + Canvas"""
    def __init__(self):
        Frame.__init__(self)
        self.master.title("#### Jeu de Bombarde ####")
        self.pack()
        # Ajout du canevas
        self.larg = 500
        self.haut = 450
        self.can = Canvas(self, width=self.larg, height=self.haut, bg='ivory',
                          relief=SUNKEN)
        self.can.pack(padx=10, pady=10)
        # Ajout des canons
        self.guns = {}
        self.guns["Jeremy"] = Canon(self.can, 50, 200, 1, 'blue', "Jeremy")
        self.guns["Nadia"] = Canon(self.can, self.larg-50, 200, -1, 'red', "Nadia")
        # Ajout des frame des canons
        self.pupitre = {}
        self.pupitre["Jeremy"] = PupitreCanon(self, self.guns["Jeremy"])
        self.pupitre["Nadia"] = PupitreCanon(self, self.guns["Nadia"])

    def modifPosition(self):
        """Amorce la modification des canons"""
        for id in self.guns:
            gun = self.guns[id]
            if gun.sens == -1:
                x = randrange(self.larg-80, self.larg-20)
            else:
                x = randrange(20, 80)
            gun.deplacer(x, randrange(self.haut-self.haut/2, self.haut-10))

    def goal(self, tireur, cible):
        """Attribution de points au tireur gagnant"""
        if tireur != cible:
            # touche l'adversaire
            self.pupitre[tireur].modifScore(1)
        else:
            # touche son propre canon
            self.pupitre[tireur].modifScore(-1)

    def dictionnaireCanons(self):
        "Renvoyer le dictionnaire décrivant les canons présents"
        return self.guns


# ----- Création des Fonctions ----- #

#############################
### Programme principal : ###
#############################

if __name__ == '__main__':
    Application().mainloop()
