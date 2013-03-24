import os



"""AJOUTER PAR ALTERNANCE DES LISTES"""

t1 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

t2 = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
t3 = "" # déclare une liste vide

i = 0
while i < len(t1):
    t3 = t3 + str(t1[i]) + " " + t2[i] + " ; "
    i += 1
print(t3)



"""AFFICHER PROPREMENT UNE LISTE"""

t2 = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
t3 = "" # déclare une liste vide

i = 0
while i < len(t2):
    t3 = t3 + t2[i] + " "
    i += 1

print(t3)




"""RECHERCHER LE NOMBRE LE PLUS GRAND DANS UNE LISTE"""

t = [32, 5, 12, 8, 3, 75, 2, 15]

max = t[0]
i = 0
while i < len(t)- 1 : # tant qu'il reste des éléments dans la liste
    i += 1
    if t[i] > max: # vérifie que l'ancien élément retenue est plus petit ou plus grand
        max = t[i] # remplace max si élément testé plus grand
    else:
        max = max
        
print(max)




"""SEPARER LES NOMBRES PAIRS ET IMPAIR EN 2 LISTES DISTINCTES"""

t = [32, 5, 12, 8, 3, 75, 2, 15]
tp = [] # création d'une liste vide
ti = [] # création d'une liste vide
i = 0
while i < len(t) - 1 : # tant qu'il reste des éléments dans la liste
    if t[i] % 2 == 0: # vérifie la parité de l'élément
        tp.append(t[i]) # incrémente l'élément dans la liste si pair
    else:
        ti.append(t[i])
    i = i + 1 # evite une boucle infinie
print(tp)
print(ti)




"""CLASSER LES ELEMENTS D'UNE LISTE EN FONCTION DE LEUR LONGUEUR"""

t = ["Mama", "Stage", "choucroute", "anti-vol", "lavabo"]
tl = []
tc = []
i = 0
while i < len(t) - 1 :
    if len(t[i]) < 6 : # verifie si l'élément est composé de plus ou moins de 6 caractères
        tc.append(t[i])
    else:
        tl.append(t[i])
    i = i + 1
print(tl)
print(tc)




"""TRANSFORMATION EN LISTE UNE SUITE DE NOMBRE CHOISI PAR L'UTILISATEUR"""

ch=input("choisir 3 nombres séparés par une virgule")
liste = list(eval(ch))
print(liste)

    
os.system("pause")

