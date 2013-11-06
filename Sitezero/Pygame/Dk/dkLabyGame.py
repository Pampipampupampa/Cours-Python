#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""CORPS PRINCIPAL DU JEU DK LABY
L'ÉDITION DE NOUVEAU NIVEAUX EST RÉALISABLE FACILEMENT EN UTILISANT UN TABLEUR
TYPE EXCEL, IL SUFFIT ALORS D'IMPORTER LA NOUVELLE GRILLE (15x15)"""
"COURS PYGAME DU SDZ"

#########################################
### Importation fonction et modules : ###
#########################################


import sys
from PySide.QtGui import *
from PySide.QtCore import *

from dkClasse import *
from dkContantes import *


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


class FenPrincipale(QWidget):
    """Fenêtre principale du programme"""
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Paramètres de la fenêtre
        self.resize(fenPrinLong, fenPrinLarg)
        self.setWindowTitle("Jeu de Labyrinthe avec DK")

        # Récupération de la taille de la fenêtre et de l'écran
        sizeEcran = QDesktopWidget().screenGeometry()
        sizeFenetre = self.geometry()
        self.move((sizeEcran.width()-sizeFenetre.width())/2,
                  (sizeEcran.height()-sizeFenetre.height())/2)

        # Ajout de l'image de fond
        self.pixmap = QPixmap(imageAccueil)
        if self.pixmap.isNull():  # On vérifie le chargement de l'image
            print("Chemin incorrect ou image invalide")

        # Ajouter une image de fond à un widget (ajoute à tous pour le moment)
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, self.pixmap)
        self.setPalette(self.palette)

        # self.label = QLabel(self)
        # self.label.setPixmap(self.pixmap)
        # self.label.show()

        # self.scn = QGraphicsScene(self)
        # self.view = QGraphicsView(self.scn)
        # self.gfxPixItem = self.scn.addPixmap(self.pixmap)
        # self.view.fitInView(self.gfxPixItem)
        # self.view.show()

        # # Ajoute une couleur au widget
        # p = self.palette()
        # p.setColor(self.backgroundRole(), Qt.black)
        # self.setPalette(p)

        # Ajout du bouton pour quitter l'application
        self.quitter = QPushButton("Quitter", self)
        self.quitter.clicked.connect(self.close)
        self.quitter.move(fenPrinLong*0.8, fenPrinLarg*0.9)
        # Boutton ouvrant le niveau 1
        self.niveau1 = QPushButton("Niveau 1", self)
        self.niveau1.clicked.connect(lambda: self.lanceNiveau(lv1))
        self.niveau1.move(fenPrinLong*0.1, fenPrinLarg*0.9)
        # Boutton ouvrant le niveau 2
        self.niveau1 = QPushButton("Niveau 2", self)
        self.niveau1.clicked.connect(lambda: self.lanceNiveau(lv2))
        self.niveau1.move(fenPrinLong*0.4, fenPrinLarg*0.9)

    def closeEvent(self, event):
        """Ouverture d'une fenêtre de confirmation"""
        msg = QMessageBox.question(self, "Demande de confirmation",
                                   "Voulez vous vraiment quitter \
                                   l'application?", QMessageBox.Yes,
                                   QMessageBox.No)
        if msg == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def lanceNiveau(self, choix):
        pygame.init()
        pygame.key.set_repeat(400, 30)  # Activation du clic enfoncé
        # Initialisation des élément de la fenêtre
        fenetre = pygame.display.set_mode((fenTaille, fenTaille))
        icone = pygame.image.load(fenIcone)
        pygame.display.set_icon(icone)
        pygame.display.set_caption(fenTitre)
        pygame.time.Clock().tick(50)  # Limitation de vitesse de la boucle
        # Boucle infinie permettant de garder le programme ouvert
        continuer = 1
        #Chargement du fond
        fond = pygame.image.load(imageFond).convert()
        #Génération d'un niveau à partir d'un fichier
        niveau = Niveau(choix)
        niveau.recuperation()
        niveau.afficher(fenetre)
        #Création de Donkey Kong
        dk = Donkey(dkDroite, dkGauche, dkHaut, dkBas, niveau)
        #Boucle infinie
        while continuer:
            # On parcours la liste de tous les événements reçus
            for event in pygame.event.get():
                if event.type == QUIT:  # Événements de type QUIT
                    continuer = 0      # On arrête la boucle
                elif event.type == KEYDOWN:
                    if event.key == K_DOWN:  # Si "flèche bas"
                        # On descend le perso
                        dk.deplacer("bas")
                    if event.key == K_UP:  # Si "flèche bas"
                        # On monte le perso
                        dk.deplacer("haut")
                    if event.key == K_LEFT:  # Si "flèche bas"
                        # On avance à gauche le perso
                        dk.deplacer("gauche")
                    if event.key == K_RIGHT:  # Si "flèche bas"
                        # On avance à droite le perso
                        dk.deplacer("droite")
            # Reaffichage des changements
            fenetre.blit(fond, (0, 0))
            niveau.afficher(fenetre)
            #dk.direction = l'image dans la bonne direction
            fenetre.blit(dk.deplacement, (dk.x, dk.y))
            pygame.display.flip()

            #Victoire -> Retour à l'accueil
            if niveau.structure[dk.numCaseY][dk.numCaseX] == b'a':
                font = pygame.font.SysFont("Loma", 30)
                rendered = font.render("FÉLICITATION L'AMI !!!", 0, (0, 0, 0))
                fenetre.blit(rendered, (50, fenTaille/2))
                pygame.display.flip()
                continuer = 0

        pygame.quit()


# ----- Création des Fonctions ----- #

#############################
### Programme principal : ###
#############################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = FenPrincipale()
    mainWindow.show()
    sys.exit(app.exec_())
