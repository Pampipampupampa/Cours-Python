# permet de tester si une année est bissextile ou non
annee = input("choisir l'année :  ")
annee = int(annee)
if annee % 400 == 0 or (annee % 4 == 0 and annee % 100 != 0):
    print("bissextile")
else:
    print("non bissextile")
