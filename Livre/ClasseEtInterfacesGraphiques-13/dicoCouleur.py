#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME RÉALISANT UN DICTIONNAIRE DE COULEURS"""
"EXERCICE 13.22"

#########################################
### Importation fonction et modules : ###
#########################################


from tkinter import *
# Permet de rechercher un fichier sur le disque grâce à une boîte de dialogue
# standard pour enregistrer ou ouvrir
from tkinter.filedialog import asksaveasfile, askopenfile


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


class Application(Frame):
    """Instanciation d'une interface graphique à un dico de couleurs"""
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Dictionnaire de Couleurs")
        self.dico = {}

        #--- Ajout du bloc du haut ---#
        frame1 = Frame(self)
        Label(frame1, text='Nom de la couleur :').grid(column=1, row=1,
                                                       padx=5, pady=5)
        Label(frame1, text='Code hexadécimal :').grid(column=1, row=2,
                                                       padx=5, pady=5)
        self.nomEntree = Entry(frame1)
        self.nomEntree.grid(column=2, row=1, padx=5, pady=5)
        self.codeEntree = Entry(frame1)
        self.codeEntree.grid(column=2, row=2, padx=5, pady=5)
        frame1.pack()
        #--- Ajout du bloc du milieu ---#
        frame2 = Frame(self)
        # ZoneTest
        self.echantillon = Label(frame2, text='None', height=8, width=30,
                                 relief=SUNKEN)
        self.echantillon.grid(column=1, row=1, padx=5, pady=5, rowspan=3)
        # Tester la couleur
        self.test = Button(frame2, text='Tester', command=self.testeCouleur)
        self.test.grid(column=2, row=1, padx=5, pady=5)
        # Vérification de l'existance de la couleur dans le dictionnaire
        self.verification = Button(frame2, text='Vérifier',
                                   command=self.verifExistence)
        self.verification.grid(column=2, row=2, padx=5, pady=5)
        # Ajouter d'une couleur au dictionnaire
        self.ajout = Button(frame2, text='Ajouter', command=self.ajoutCouleur)
        self.ajout.grid(column=2, row=3, padx=5, pady=5)
        frame2.pack()
        #--- Ajout du bloc du bas ---#
        frame3 = Frame(self)
        self.enregistre = Button(frame3, text='Enregistrer le dictionnaire',
                                 command=self.enregistreDico)
        self.enregistre.grid(column=1, row=1, padx=5, pady=5)
        self.restaure = Button(frame3, text='Ouvrir le dictionnaire',
                               command=self.restaureDico)
        self.restaure.grid(column=2, row=1, padx=5, pady=5)
        frame3.pack()
        self.pack()

    def ajoutCouleur(self):
        """Ajout d'une paire clé/valeur"""
        if self.testeCouleur() == 0:
            return  # Renvoie le message de testeCouleur
        couleur = self.nomEntree.get()
        if len(couleur) > 2:
            self.dico[couleur] = self.codeEntree.get()
            self.echantillon.config(text="{}\na été ajoutée au dictionnaire".
                                    format(couleur), fg='white')
        else:
            self.echantillon.config(bg='white', text="Nom incorrect")

    def testeCouleur(self):
        """Vérification code hexadécimal et affichage couleur correspondante"""
        try:
            self.echantillon.config(bg=self.codeEntree.get(), text="",
                                    fg='white')
            return 1
        except:
            self.echantillon.config(text='Essaye de mettre un code valable' +
                                    '\n bouli !', bg='white', fg='black')
            return 0

    def verifExistence(self):
        """Vérification de l'existence de la couleur dans le dico"""
        couleur = self.nomEntree.get()
        if couleur in self.dico:
            self.echantillon.config(bg=self.dico[couleur],
                                    text="{}\nexiste dans le dictionnaire".
                                    format(couleur), fg='white')
        else:
            self.echantillon.config(bg='white',
                                    text="{}\n n'est pas dans le dictionnaire".
                                    format(couleur), fg='black')
    def enregistreDico(self):
        """Enregistrement du dictionnaire dans un fichier"""
        fiCible = asksaveasfile(filetypes=[("Texte", ".txt"), ("Tous", "*")])
        for clef, valeur in list(self.dico.items()):
            fiCible.write("{0} {1}\n".format(clef, valeur))
        fiCible.close()

    def restaureDico(self):
        """Restauration du dictionnaire pour pourvoir lire et écrire dedans"""
        fiSource = askopenfile(filetypes=[("Texte", ".txt"), ("Tous", "*")])
        ligneListe = fiSource.readlines()
        for ligne in ligneListe:
            champsValeur = ligne.split()
            self.dico[champsValeur[0]] = champsValeur[1]
        fiSource.close()

#############################
### Programme principal : ###
#############################


Application().mainloop()
