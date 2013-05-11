import os

def ligneCar(n, ca):
    "fonction multipliant un caractère <ca>, <n> fois"
    chaine = ca * n
    return chaine

print(ligneCar(5, "b"))
print("")

    
def maximum(n1, n2, n3):
    "renvoie le plus grand des 3 nombres"
    if n1 >= n2 and  n1 >= n3:
        max = n1
    elif n2 >= n1 and n2 >= n3:
        max = n2
    else:
        max = n3
    return max
        

print(maximum(1, 88, 5))
print("")

        
    
