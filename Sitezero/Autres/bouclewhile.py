# table multiplication
nombre = input("Renseignez la table que vous voulez étudier :  ")
max = input("renseigner l'étendue :  ")
nombre = int(nombre)
max = int(max)
def tablemulti(nombre, max=10):
	i = 0
	while i < max: # limite de la boucle
		print(i + 1, "*", nombre, "=", (i + 1)*nombre)
		i += 1
tablemulti(nombre, max)
input("entrée pour quitter")