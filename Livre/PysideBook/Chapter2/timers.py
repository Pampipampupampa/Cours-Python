#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""UNE FENÊTRE CUSTOMISÉE AVEC DES ÉLÉMENTS BASIQUES"""
"COURS PYSIDE CHAPITRE 2"

#########################################
### Importation fonction et modules : ###
#########################################


import sys
from PySide.QtGui import QApplication, QWidget, QLCDNumber
from PySide.QtCore import QDateTime, QTimer, SIGNAL


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


class MyTimer(QWidget):
    """Main window class for timer"""
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("My digital Clock")
        timer = QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), self.updtTime)
        self.myTimeDisplay = QLCDNumber(self)  # Choix du type d'apparence
        self.myTimeDisplay.setSegmentStyle(QLCDNumber.Filled)
        self.myTimeDisplay.setDigitCount(8)  # Nombre de chiffres affichés
        self.myTimeDisplay.resize(500, 150)
        timer.start(1000)  # Bouclage tout le 1 sec

    def updtTime(self):
        """Update current Time"""
        currentTime = QDateTime.currentDateTime().toString('hh:mm:ss')
        self.myTimeDisplay.display(currentTime)


# ----- Création des Fonctions ----- #

#############################
### Programme principal : ###
#############################

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MyTimer()
        window.show()
        app.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error : ", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window")
    except Exception:
        print("sys.exc_info()[1]")
