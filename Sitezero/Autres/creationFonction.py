def tablemulti(nombre=1, max=10): # creation de fonction
	i = 0
	while i < max: # limite de la boucle
		print(i + 1, "*", nombre, "=", (i + 1)*nombre)
		i += 1
tablemulti()
tablemulti(2)
tablemulti(nombre = 2)
tablemulti(max=2)
def carre(valeur): 
	return valeur * valeur # renvoi la valeur du calcul
abc = carre(9)
print(abc)
fonction = lambda x: x * x # autre type de fonction (permet réduction de formules ???)
print(fonction(3))
input("entrée pour quitter")