#! /usr/bin/env python
# -*- coding:Utf8 -*-*


"CONVERTISSEUR INTERACTIF CELSIUS VERS FAHRENHEIT"


################################################################
############# Importation fonction et modules : ################
################################################################

from tkinter import *


###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################

def convFar(event):
	cels = eval(entreeCelsius.get())
	fahrenheit.set(str(cels*1.8 + 32))

def convCels(event):
	fahr = eval(entreeFahrenheit.get())
	celsius.set(str((fahr-32)/1.8))



######################################################
############## Programme principal : #################
######################################################

fenetre = Tk()
fenetre.title("Convertisseur d'échelle de température")


"valeurs par défaut"
celsius = StringVar() # déclare et permet l'interface entre TCL et Python (permet d'utiliser ".set")
fahrenheit = StringVar()
celsius.set("100.0")
fahrenheit.set("212.0")


"éléments de la fenêtre"
entreeCelsius = Entry(fenetre, textvariable = celsius)
entreeCelsius.bind("<Return>", convFar)
entreeCelsius.grid(row = 0, column = 1, padx = 5, pady = 5)
Label(fenetre, text = 'Température en Celsius ( °C ) : ').grid(row = 0, column = 0, sticky = W)
entreeFahrenheit = Entry(fenetre, textvariable = fahrenheit)
entreeFahrenheit.bind("<Return>", convCels)
entreeFahrenheit.grid(row = 1, column = 1, padx = 5, pady = 5)
Label(fenetre, text = 'Température en Fahrenheit ( °F ) : ').grid(row = 1, column = 0, sticky = W)



fenetre.mainloop()









