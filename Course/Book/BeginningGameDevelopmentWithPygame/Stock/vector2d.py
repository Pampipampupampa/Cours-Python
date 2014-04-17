#! /usr/bin/env python3
# -*- coding:Utf8 -*-


"""CLASSE PERMETTANT DE CRÉER DES VECTEURS 2D ET DE FAIRE DES OPÉRATIONS DESSUS
   """

##########################################
### Importation fonction et modules : ####
##########################################

import math
import operator

############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


class Vector2D:

    """Création d'un vecteur 2D avec méthodes pour les différentes opérations
       Accepte : Tuple, Liste, Array, Nombre (type = int ou float)"""

    __slots__ = ['x', 'y']  # Prépare un espace mémoire ( speed up)

    def __init__(self, x_ou_pair=(0, 0), y=None):
        if y is None:
            self.x = x_ou_pair[0]
            self.y = x_ou_pair[1]
        else:
            self.x = x_ou_pair
            self.y = y
        try:
            self.x += 0
            self.y += 0
        except TypeError:
            raise

    def __repr__(self):
        """Représentation pour le débogage"""
        return "({}, {})".format(self.x, self.y)

    def __str__(self):
        """Représentation pour l'affichage"""
        x = repr(self)
        return "Vect2D{}".format(x)

    def __getitem__(self, key):
        """Obtention de la valeur d'un des éléments self.x ou self.y"""
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript " + str(key) + " to Vector2D")

    def __setitem__(self, key, value):
        """Modification de la valeur d'un des éléments self.x ou self.y"""
        try:
            value += 0
        except TypeError:
            raise

        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript " + str(key) + " to Vector2D")

    def __len__(self):
        """Retourne la taille du vecteur (différent de la longueur mathématique"""
        return 2

    # Comparison
    def __eq__(self, other):
        """Utilisée pour comparer des vecteurs entre eux"""
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other):
        """Utilisée pour comparer des vecteurs entre eux"""
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True

    def __bool__(self):
        """Utilisée pour vérifier que le vecteur n'est pas vide"""
        return bool(self.x or self.y)

    # Fonctions "patron" pour les fonctions utilisants le module operator
    def _operator_handler(self, other, func):
        """Retourne le vecteur transformé (copie)
           Le vecteur doit être à gauche de l'opérateur
           Voir _r_operator_handler pour un vecteur à droite"""
        if isinstance(other, Vector2D):
            return Vector2D(func(self.x, other.x),
                            func(self.y, other.y))
        elif hasattr(other, "__getitem__"):
            return Vector2D(func(self.x, other[0]),
                            func(self.y, other[1]))
        else:
            return Vector2D(func(self.x, other),
                            func(self.y, other))

    def _r_operator_handler(self, other, func):
        """Retourne le vecteur transformé (copie)
        Le vecteur doit être à droite de l'opérateur
        Voir _operator_handler pour un vecteur à gauche"""
        if hasattr(other, "__getitem__"):
            return Vector2D(func(other[0], self.x),
                            func(other[1], self.y))
        else:
            return Vector2D(func(other, self.x),
                            func(other, self.y))

    def _i_operator_handler(self, other, func):
        """Modification du vecteur par la fonction de l'opérateur"""
        if hasattr(other, "__getitem__"):
            self.x = func(self.x, other[0]),
            self.y = func(self.y, other[1])
        else:
            self.x = func(self.x, other),
            self.y = func(self.y, other)

    # Création de nouveau vecteur à partir de 2 autres
    @classmethod
    def from_points(cls, p1, p2):
        """Création d'un nouveau vecteur à partir de points :
           Accepte : Tuple, Vector2D, Liste, Array"""
        return cls(p2[0] - p1[0], p2[1] - p1[1])

    # Fonction du vecteur
    def get_magnitude(self):
        """Retourne la longueur du vecteur"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def _set_magnitude(self, value):
        """Modification de la longueur du vecteur"""
        magnitude = self.get_magnitude()
        self.x *= value/magnitude
        self.y *= value/magnitude

    # Création d'une propriété d'attribut :
    # 1er paramètre : fonction pour obtenir la valeur de l'attribut
    # 2ème paramètre : fonction pour définir la valeur de l'attribut
    # 3ème paramètre : fonction pour supprimer la valeur de l'attribut (None)
    magnitude = property(get_magnitude, _set_magnitude, None, "Gets or sets the magnitude of the vector")

    def rotate(self, angle):
        """Rotation du vecteur selon un angle en degrès (sens anti-horaire)"""
        rad = math.radians(angle)
        x = self.x * math.cos(rad) - self.y * math.sin(rad)
        y = self.x * math.sin(rad) + self.y * math.cos(rad)
        self.x, self.y = round(x, 8), round(y, 8)

    def rotated(self, angle):
        """Retourne le vecteur après avoir subit une rotation selon un angle
           en degrès (sens anti-horaire)"""
        rad = math.radians(angle)
        x = self.x * math.cos(rad) - self.y * math.sin(rad)
        y = self.x * math.sin(rad) - self.y * math.cos(rad)
        return Vector2D(round(x, 8), round(y, 8))

    def get_angle(self):
        """Renvois l'angle du vecteur en degrès"""
        if ((self.x ** 2 + self.y ** 2) == 0):  # N'est pas Vect2D(0, 0)
            return 0
        return math.degrees(math.atan2(self.y, self.x))

    def set_angle(self, angle):
        """Modifie l'angle du vecteur (angle en degrès)"""
        self.x = self.magnitude
        self.y = 0
        self.rotate(angle)

    # Création d'une propriété d'attribut
    angle = property(get_angle, set_angle, None, "Gets or sets the angle of a vector")

    def get_angle_between(self, other):
        """Retourne l'angle entre 2 vecteurs grâce aux produits vectoriels,
           scalaires et à l'arc tangente"""
        cross = self.cross(other)
        dot = self.dot(other)
        # <atan2> prend en compte le signe des 2 éléments contrairement à <atan>
        return round(math.degrees(math.atan2(cross, dot)), 8)

    def get_distance(self, other):
        """Retourne la distance entre 2 vecteurs"""
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)

    def interpolate_to(self, other, range):
        """Retourne un vecteur interpolé entre self et other de x range
           ---------------  0 < range < 1  ----------------
           range = 1  ----> Le vecteur prend les coordonnées de other"""
        return Vector2D(self.x + (other[0] - self.x)*range,
                        self.y + (other[1] - self.y)*range)

    def cross(self, other):
        """Retourne le résultat du produit vectoriel des vecteurs"""
        return self.x*other[1] - self.y*other[0]

    def dot(self, other):
        """Retourne le produit scalaire des vecteurs"""
        return float(self.x * other[0] + self.y * other[1])

    def perpendicular(self):
        """Retourne un vecteur perpendiculaire au vecteur"""
        return Vector2D(-self.y, self.x)

    # Normalisation
    def normalize(self):
        """Modification des éléments du vecteur afin d'obtenir une magnitude de 1"""
        magnitude = self.magnitude
        if magnitude != 0:
            self.x /= magnitude
            self.y /= magnitude
        return magnitude

    def normalized(self):
        """Retourne la valeur des éléments après normalisation"""
        magnitude = self.magnitude
        if magnitude != 0:
            return self/magnitude
        return Vector2D(self)

    # Addition
    def __add__(self, other):
        """Retourne l'addition d'un vecteur par un élément (int ou float)
           Éléments supportés : Liste, Tuple, Array, ou nombre.
           Élément à gauche ou à droite de l'opérateur (__add__ == __radd__)"""
        # Si on additionne 2 vecteurs
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        # Si on ajoute un object de type : liste, array, ou tuple
        elif hasattr(other, "__getitem__"):
            return Vector2D(self.x + other[0], self.y + other[1])
        # Si on ajoute un simple nombre
        else:
            return Vector2D(self.x + other, self.y + other)
    __radd__ = __add__

    def __iadd__(self, other):
        """Modification du vecteur en lui ajoutant une valeur.
           Supporte l'addition à partir d'une Liste, Tuple, Array, ou nombre."""
        # Si on additionne 2 vecteurs
        if isinstance(other, Vector2D):
            self.x += other.x
            self.y += other.y
        # Si on ajoute un object de type : liste, array, ou tuple
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        # Si on ajoute un simple nombre
        else:
            self.x += other
            self.y += other
        return self

    # Soustraction
    def __sub__(self, other):
        """Retourne la soustraction d'un vecteur par un élément (int ou float)
           Éléments supportés : Liste, Tuple, Array, ou nombre.
           L'élément doit être à gauche du vecteur"""
        # Si on soustrait 2 vecteurs
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        # Si on soustrait par un object de type : liste, array, ou tuple
        elif (hasattr(other, "__getitem__")):
            return Vector2D(self.x - other[0], self.y - other[1])
        # Si on soustrait par un simple nombre
        else:
            return Vector2D(self.x - other, self.y - other)

    def __rsub__(self, other):
        """Retourne la soustraction d'un élément par un vecteur (int ou float)
           Éléments supportés : Liste, Tuple, Array, ou nombre.
           L'élément doit être à droite du vecteur"""
        # Si on soustrait 2 vecteurs
        if isinstance(other, Vector2D):
            return Vector2D(other.x - self.x, other.y - self.y)
        # Si on soustrait par un object de type : liste, array, ou tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(other[0] - self.x, other[1] - self.y)
        # Si on soustrait par un simple nombre
        else:
            return Vector2D(other - self.x, other - self.y)

    def __isub__(self, other):
        """Modification du vecteur en lui enlevant une valeur (int ou float)
           Éléments supportés : Liste, Tuple, Array, ou nombre."""
        # Si on soustrait 2 vecteurs
        if isinstance(other, Vector2D):
            self.x -= other.x
            self.y -= other.y
        # Si on soustrait par un object de type : liste, array, ou tuple
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        # Si on soustrait par un simple nombre
        else:
            self.x -= other
            self.y -= other
        return self

    # Multiplication
    def __mul__(self, other):
        """Retourne la multiplication d'un vecteur par un élément (int ou float)
           Éléments supportés : Liste, Tuple, Array, ou nombre.
           Élément à gauche ou à droite de l'opérateur (__mul__ == __rmul__)"""
        # Si on multiplie par un autre vecteur
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        # Si on multiplie par un object de type : liste, array, ou tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(self.x * other[0], self.y * other[1])
        # Si on multiplie par un simple nombre
        else:
            return Vector2D(self.x * other, self.y * other)
    __rmul__ = __mul__

    def __imul__(self, other):
        """Modification du vecteur par un élément (int ou float)
           Éléments supportés : Liste, Tuple, Array, ou nombre."""
        # Si on multiplie par un autre vecteur
        if isinstance(other, Vector2D):
            self.x *= other.x
            self.y *= other.y
        # Si on multiplie par un object de type : liste, array, ou tuple
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        # Si on multiplie par un simple nombre
        else:
            self.x *= other
            self.y *= other
        return self

    # Division réelle
    # def __truediv__(self, other):
    #     """Retourne la division d'un vecteur par un élément (int ou float)
    #        Éléments supportés : Liste, Tuple, Array, ou nombre
    #        Éléments à gauche de l'opérateur"""
    #     return self._operator_handler(other, operator.truediv)
    # # __div__ = __truediv__

    # def __rtruediv__(self, other):
    #     """Retourne la division d'un élément (int ou float) par un vecteur
    #        Éléments supportés : Liste, Tuple, Array, ou nombre
    #        Éléments à droite de l'opérateur"""
    #     return self._r_operator_handler(other, operator.truediv)
    # # __rdiv__ = __rtruediv__

    # def __itruediv__(self, other):
    #     """Modification du vecteur après division par un élément (int ou float)
    #        Éléments supportés : Liste, Tuple, Array, ou nombre"""
    #     return self._i_operator_handler(other, operator.truediv)
    # # __idiv__ = __itruediv__

    # Division réelle
    def __truediv__(self, other):
        """Retourne la division d'un vecteur par un élément (int ou float)
           Éléments supportés : Liste, Tuple, Array, ou nombre
           Éléments à gauche de l'opérateur"""
        # Si on divise un vecteur
        if isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)
        # Si on divise par un object de type : liste, array, ou tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(self.x / other[0], self.y / other[1])
        # Si on divise par un simple nombre
        else:
            return Vector2D(self.x / other, self.y / other)

    def __rtruediv__(self, other):
        """Retourne la division d'un élément (int ou float) par un vecteur
           Éléments supportés : Liste, Tuple, Array, ou nombre
           Éléments à droite de l'opérateur"""
        # Si on divise un vecteur
        if isinstance(other, Vector2D):
            return Vector2D(other.x / self.x, other.y / self.y)
        # Si on divise un object de type : liste, array, ou tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(other[0] / self.x, other[1] / self.y)
        # Si on divise un objet de type non supporté
        else:
            raise TypeError(other, type(other), "Must be a list, tuple, array, or Vector2D")

    def __itruediv__(self, other):
        """Modification du vecteur après division par un élément (int ou float)
           Éléments supportés : Liste, Tuple, Array, ou nombre"""
        # Si on divise par un autre vecteur
        if isinstance(other, Vector2D):
            self.x /= other.x
            self.y /= other.y
        # Si on divise par un object de type : liste, array, ou tuple
        elif (hasattr(other, "__getitem__")):
            self.x /= other[0]
            self.y /= other[1]
        # Si on divise par un simple nombre
        else:
            self.x /= other
            self.y /= other
        return self

    # # Division entière
    # def __floordiv__(self, other):
    #     """Retourne la division entière d'un vecteur par un élément (int ou float)
    #        Éléments supportés : Liste, Tuple, Array, ou nombre
    #        Éléments à gauche de l'opérateur"""
    #     return self._operator_handler(other, operator.floordiv)

    # def __rfloordiv__(self, other):
    #     """Retourne la division entière d'un élément (int ou float)par un vecteur
    #        Éléments supportés : Liste, Tuple, Array, ou nombre
    #        Éléments à droite de l'opérateur"""
    #     return self._r_operator_handler(other, operator.floordiv)

    # def __ifloordiv__(self, other):
    #     """Modification du vecteur après division entière par un élément (int ou float)
    #        Éléments supportés : Liste, Tuple, Array, ou nombre"""
    #     return self._i_operator_handler(other, operator.floordiv)

    def __floordiv__(self, other):
        """Retourne la division d'un vecteur par un élément (int ou float)
           Éléments supportés : Liste, Tuple, Array, ou nombre
           Éléments à gauche de l'opérateur"""
        # Si on divise un vecteur
        if isinstance(other, Vector2D):
            return Vector2D(self.x // other.x, self.y // other.y)
        # Si on divise par un object de type : liste, array, ou tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(self.x // other[0], self.y // other[1])
        # Si on divise par un simple nombre
        else:
            return Vector2D(self.x // other, self.y // other)

    def __rfloordiv__(self, other):
        """Retourne la division d'un élément (int ou float) par un vecteur
           Éléments supportés : Liste, Tuple, Array, ou nombre
           Éléments à droite de l'opérateur"""
        # Si on divise un vecteur
        if isinstance(other, Vector2D):
            return Vector2D(other.x // self.x, other.y // self.y)
        # Si on divise un object de type : liste, array, ou tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(other[0] // self.x, other[1] // self.y)
        # Si on divise un objet de type non supporté
        else:
            raise TypeError(other, type(other), "Must be a list, tuple, array, or Vector2D")

    def __ifloordiv__(self, other):
        """Modification du vecteur après division par un élément (int ou float)
           Éléments supportés : Liste, Tuple, Array, ou nombre"""
        # Si on divise par un autre vecteur
        if isinstance(other, Vector2D):
            self.x //= other.x
            self.y //= other.y
        # Si on divise par un object de type : liste, array, ou tuple
        elif (hasattr(other, "__getitem__")):
            self.x //= other[0]
            self.y //= other[1]
        # Si on divise par un simple nombre
        else:
            self.x //= other
            self.y //= other
        return self

    # Modulo
    def __mod__(self, other):
        """Retourne le modulo du vecteur par un élément
           Éléments supportés : Liste, Tuple, Array, ou nombre
           Éléments à gauche de l'opérateur"""
        return self._operator_handler(other, operator.mod)

    def __rmod__(self, other):
        """Retourne le modulo de l'élément par le vecteur
           Éléments supportés : Liste, Tuple, Array, ou nombre
           Éléments à droite de l'opérateur"""
        return self._r_operator_handler(other, operator.mod)

    # Puissance
    def __pow__(self, other):
        return self._operator_handler(other, operator.pow)

    def __rpow__(self, other):
        return self._r_operator_handler(other, operator.pow)

    # Arithmetic operation
    def __neg__(self):
        """Retourne l'opposée de chaques éléments du vecteur"""
        return Vector2D(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self):
        """Retourne la même valeur pour chaques éléments du vecteur"""
        return Vector2D(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self):
        """Retourne la valeur absolue des éléments du vecteur"""
        return Vector2D(abs(self.x), abs(self.y))

    def __invert__(self):
        """Retourne le vecteur inversé"""
        return Vector2D(-self.x, -self.y)

    # Copy : Voir les tests pour le fonctionnement

    # Function to pickle
    def __getstate__(self):
        return [self.x, self.y]

    def __setstate__(self, dict):
        self.x, self.y = dict

##########################################################
######### Test du module avec le module unittest #########
##########################################################

if __name__ == "__main__":

    import unittest
    import pickle

    class UnitTestVector2D(unittest.TestCase):

        def setUp(self):
            pass

        def testCreationAndAccess(self):
            v = Vector2D(111, 222)
            self.assertTrue((v.x == 111) and (v.y == 222))
            v.x = 333
            v[1] = 444
            self.assertTrue((v[0] == 333) and (v[1] == 444))
            self.assertFalse(Vector2D() != (0, 0))
            self.assertFalse(Vector2D() != Vector2D(0, 0))
            with self.assertRaises(TypeError):
                Vector2D("4", "1")
            with self.assertRaises(TypeError):
                Vector2D(3, "nn")
            with self.assertRaises(IndexError):
                v[3] = 2
            with self.assertRaises(TypeError):
                v[1] = "3"
            with self.assertRaises(IndexError):
                v[3]
            print("Tests de création réussis")

        def testMath(self):
            v = Vector2D(111, 222)
            self.assertEqual(v + 1, Vector2D(112, 223))
            self.assertEqual(v - 2, [109, 220])
            self.assertEqual(v * 3, (333, 666))
            self.assertEqual(v / 2.0, Vector2D(55.5, 111))
            self.assertEqual(v / 2, (55.5, 111))
            self.assertEqual(v ** Vector2D(2, 3), [12321, 10941048])
            self.assertEqual(v + [-11, 78], Vector2D(100, 300))
            self.assertEqual(v / [10, 2], [11.1, 111])
            self.assertEqual(v // Vector2D(10, 10), (11, 22))
            self.assertEqual(v / Vector2D(10, 10), (11.1, 22.2))
            print("Tests des opération mathématiques réussis")

        def testReverseMath(self):
            v = Vector2D(111, 222)
            self.assertEqual(1 + v, Vector2D(112, 223))
            self.assertEqual(2 - v, [-109, -220])
            self.assertEqual(3 * v, (333, 666))
            self.assertEqual([222, 888] / v, [2, 4])
            self.assertEqual([111, 222] ** Vector2D(2, 3), [12321, 10941048])
            self.assertEqual([-11, 78] + v, Vector2D(100, 300))
            self.assertEqual(Vector2D(1110, 4410) // v, (10, 19))
            print("Tests des opération mathématiques inverses réussis")

        def testArithmetric(self):
            v = Vector2D(111, 222)
            v = -v
            self.assertTrue(v, [-111, -222])
            v = abs(v)
            self.assertTrue(v, [111, 222])
            print("Tests arithmetrics réussis")

        def testComparison(self):
            int_vec = Vector2D(3, -2)
            flt_vec = Vector2D(3.0, -2.0)
            zero_vec = Vector2D(0, 0)
            self.assertTrue(int_vec, flt_vec)
            self.assertNotEqual(int_vec, zero_vec)
            self.assertFalse(flt_vec == zero_vec)
            self.assertFalse(flt_vec != int_vec)
            self.assertTrue(int_vec, (3, -2))
            self.assertNotEqual(int_vec, [0, 0])
            self.assertNotEqual(int_vec, 5)
            self.assertNotEqual(int_vec, [3, -2, -5])
            print("Tests de comparaisons réussis")

        def testMagnitude(self):
            v = Vector2D(3, 4)
            self.assertEqual(v.magnitude, 5)
            self.assertEqual(v.normalize(), 5)
            self.assertEqual(v.magnitude, 1)
            v.magnitude = 5
            self.assertEqual(v, Vector2D(3, 4))
            v2 = Vector2D(10, -2)
            self.assertEqual(v.get_distance(v2), (v - v2).get_magnitude())
            print("Tests de calcul de magnitude réussis")

        def testCrossInterpolate(self):
            v = Vector2D(1, .5)
            u = Vector2D(10, 8)
            self.assertTrue(v.cross(u) == 3)
            self.assertTrue(v.interpolate_to(u, 1) == u)
            print("Tests des interpolation et des multiplication croisée réussis")

        def testCopy(self):
            v = Vector2D(55, 55)
            b = Vector2D(v)  # Create copy
            c = v  # Create alias
            v.normalize()
            self.assertFalse(v == b)
            self.assertTrue(v == c)
            print("Tests de copie réussis")

        def testAngles(self):
            v = Vector2D(0, 3)
            self.assertEqual(v.angle, 90)
            v2 = Vector2D(v)
            v.rotate(-90)
            self.assertEqual(v.get_angle_between(v2), 90)
            v2.angle -= 90
            self.assertEqual(v.magnitude, v2.magnitude)
            self.assertEqual(v2.angle, 0)
            self.assertEqual(v2, [3, 0])
            self.assertAlmostEqual((v - v2).magnitude, 0, 15)
            self.assertEqual(v.magnitude, v2.magnitude)
            v2.rotate(300)
            self.assertAlmostEqual(v.get_angle_between(v2), -60)
            v2.rotate(v2.get_angle_between(v))
            self.assertAlmostEqual(v.get_angle_between(v2), 0)
            print(".Tests des opérations d'angles réussis")

        def testCrossDot(self):
            vect = Vector2D(1, .5)
            vect2 = Vector2D(4, 6)
            self.assertTrue(vect.cross(vect2) == 4)
            self.assertTrue(vect.dot(vect2) == 7)
            print("Tests des produits scalaires et vectoriels réussis")

        def testInplace(self):
            inplaceVec = Vector2D(5, 13)
            inplaceRef = inplaceVec
            inplaceVec *= .5
            inplaceVec *= Vector2D(3, -2)
            inplaceVec /= Vector2D(3, -2)
            inplaceVec += .5
            inplaceVec += (2, 4)
            inplaceVec /= (3, 6)
            inplaceVec += Vector2D(-1, -1)
            self.assertEqual(inplaceVec, inplaceRef)
            vect = Vector2D(8, 9)
            vect //= Vector2D(4, 5)
            self.assertEqual(vect, Vector2D(2, 1))
            vect = Vector2D(8, 9)
            vect /= Vector2D(4, 5)
            self.assertEqual(vect, (2., 1.8))
            print("Tests des opérateurs inplace réussis")

        def testPickle(self):
            testvec = Vector2D(5, .3)
            testvec_str = pickle.dumps(testvec)
            loaded_vec = pickle.loads(testvec_str)
            self.assertEqual(testvec, loaded_vec)
            print("Tests de sérialisation réussis")

    unittest.main()
