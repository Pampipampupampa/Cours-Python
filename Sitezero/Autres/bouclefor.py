# Initiation à l'instruction "for"
phrase = input("écrivez une phrase sans accents :  ") # trouve les consonnes
i = 0
y = 0
for lettre in phrase:
    if lettre in "AEIOUYaeiouy": # si lettre = voyelle
        y += 1
    elif lettre in " ": # exclusion des espaces
	    i = i
    else:
	    i += 1
print("    Il y a", i, "consonnes")
print("    Il y a", y, "voyelles")
input("enter to exit")
