import math # importe le module "math"
print(math.sqrt(25)) # utilisation d'une fonction math : racine carree

import math as mathematique # modifie le nom sous lequel on importe le module math
print(mathematique.sqrt(25))

from math import fabs # ici on importe qu'une fonction du module
print(fabs(-5))

from math import * # importe toutes les fonctions mais contrairement à la fonction "importer" on a seulement le nom de la fonction (attention même niveau que les autres comme print)
print(sqrt(25))
