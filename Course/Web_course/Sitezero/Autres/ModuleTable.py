"""module multiplicatif contenant la fonction table"""

import os

def table(nombre, max=10):
    i = 0
    while i < max: # limite de la boucle
	    print(i + 1, "*", nombre, "=", (i + 1)*nombre)
	    i += 1
	    
# test fonction table
if __name__ == "__main__":
    table(4)
    os.system("pause")
    
