#! /usr/bin/env python3
# -*- coding:Utf8 -*-


"""Manipulate 2D vectors"""

##########################################
### Importation fonction et modules : ####
##########################################

import math
import operator

############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


class Vector2D:

    """
        Create a Vector2D instance
        Accept Tuple, List, Array, Number (type = int or float)

        This class support various operations :
            Arithmetic operations (Operation with dict raise an IndexError)
            Comparison operators (Compare with dict raise an IndexError)
            Pickle

    """

    __slots__ = ['x', 'y']  # Prepare memory space ( speed up)

    def __init__(self, x_or_pair=(0, 0), y=None):
        if y is None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
        try:
            self.x += 0
            self.y += 0
        except TypeError:
            raise

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __str__(self):
        x = repr(self)
        return "Vect2D{}".format(x)

    def __getitem__(self, key):
        """Get a vector element"""
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript " + str(key) + " to Vector2D")

    def __setitem__(self, key, value):
        """Set a vector element"""
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
        """Return vector length (always equal to 2)"""
        return 2

    def __eq__(self, other):
        """Test equality : raise KeyError if compare with a dict"""
        if hasattr(other, "__getitem__") and len(other) == 2:
            try:
                return self.x == other[0] and self.y == other[1]
            except KeyError as e:
                raise e
        else:
            return False

    def __ne__(self, other):
        """Test inequality : raise KeyError if compare with a dict"""
        if hasattr(other, "__getitem__") and len(other) == 2:
            try:
                return self.x != other[0] or self.y != other[1]
            except KeyError as e:
                raise e
        else:
            return True

    def __bool__(self):
        """Test if vector are empty"""
        return bool(self.x or self.y)

    def _operator_handler(self, other, func):
        """Compute func with func in operator modul methods
           Operations with vector at right side"""
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
        """Compute func with func in operator modul methods
           Operation with vector at left side"""
        if hasattr(other, "__getitem__"):
            return Vector2D(func(other[0], self.x),
                            func(other[1], self.y))
        else:
            return Vector2D(func(other, self.x),
                            func(other, self.y))

    def _i_operator_handler(self, other, func):
        """Compute func with func in operator modul methods
           Incrementals operations on vector instance"""
        if hasattr(other, "__getitem__"):
            self.x = func(self.x, other[0]),
            self.y = func(self.y, other[1])
        else:
            self.x = func(self.x, other),
            self.y = func(self.y, other)

    @classmethod
    def from_points(cls, p1, p2):
        """Create new vector from two points :
           Accept Tuple, Vector2D, Liste, Array"""
        return cls(p2[0] - p1[0], p2[1] - p1[1])

    # Fonction du vecteur
    def get_magnitude(self):
        """Get vector length (magnitude)"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def _set_magnitude(self, value):
        """Set vector length (magnitude)"""
        magnitude = self.get_magnitude()
        self.x *= value/magnitude
        self.y *= value/magnitude

    magnitude = property(get_magnitude, _set_magnitude, None, "Gets or sets the magnitude of the vector")

    def rotate(self, angle):
        """Rotate vector according to angle argument (counterclockwise)
           angle represents degrees
           If you want a copy use rotated instead"""
        rad = math.radians(angle)
        x = self.x * math.cos(rad) - self.y * math.sin(rad)
        y = self.x * math.sin(rad) + self.y * math.cos(rad)
        self.x, self.y = round(x, 8), round(y, 8)

    def rotated(self, angle):
        """Rotate vector according to angle argument (counterclockwise)
           angle represents degrees
           This function create a copy
           If you want to change current instance use rotate instead"""
        rad = math.radians(angle)
        x = self.x * math.cos(rad) - self.y * math.sin(rad)
        y = self.x * math.sin(rad) - self.y * math.cos(rad)
        return Vector2D(round(x, 8), round(y, 8))

    def _get_angle(self):
        """Get vector angle (angle represent degrees)"""
        if not bool(self):  # Check if it's an empty vector
            return 0
        return math.degrees(math.atan2(self.y, self.x))

    def _set_angle(self, angle):
        """Set vector angle (angle represent degrees)"""
        self.x = self.magnitude
        self.y = 0
        self.rotate(angle)

    angle = property(_get_angle, _set_angle, None, "Gets or sets the angle of a vector")

    def get_angle_between(self, other):
        """Return angle between two vectors"""
        cross = self.cross(other)
        dot = self.dot(other)
        # <atan2> prend en compte le signe des 2 éléments contrairement à <atan>
        return round(math.degrees(math.atan2(cross, dot)), 8)

    def get_distance(self, other):
        """Return distance between two vectors"""
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)

    def interpolate_to(self, other, range=0.5):
        """Return an interpolate vector between two vector
           range argument affect new vector relative position from other vector
           ---------------  0 < range < 1  ----------------
           range = 1  ----> Le vecteur prend les coordonnées de other"""
        return Vector2D(self.x + (other[0] - self.x)*range,
                        self.y + (other[1] - self.y)*range)

    def cross(self, other):
        """Return cross product between two vectors"""
        return self.x*other[1] - self.y*other[0]

    def dot(self, other):
        """Return dot product between two vectors"""
        return float(self.x * other[0] + self.y * other[1])

    def perpendicular(self):
        """Return a perpendicular self copy"""
        return Vector2D(-self.y, self.x)

    def normalize(self):
        """Normalize vector (magnitude == 1)"""
        magnitude = self.magnitude
        if magnitude != 0:
            self.x /= magnitude
            self.y /= magnitude
        return magnitude

    def normalized(self):
        """Return a copy of the normalized vector"""
        magnitude = self.magnitude
        if magnitude != 0:
            return self/magnitude
        return Vector2D(self)

    def __add__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        # Liste, array, or tuple
        elif hasattr(other, "__getitem__"):
            return Vector2D(self.x + other[0], self.y + other[1])
        # Number
        else:
            return Vector2D(self.x + other, self.y + other)
    __radd__ = __add__

    def __iadd__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            self.x += other.x
            self.y += other.y
        # Liste, array, or tuple
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        # Number
        else:
            self.x += other
            self.y += other
        return self

    # Soustraction
    def __sub__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        # Liste, array, or tuple
        elif (hasattr(other, "__getitem__")):
            return Vector2D(self.x - other[0], self.y - other[1])
        # Number
        else:
            return Vector2D(self.x - other, self.y - other)

    def __rsub__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            return Vector2D(other.x - self.x, other.y - self.y)
       # Liste, array, or tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(other[0] - self.x, other[1] - self.y)
        # Number
        else:
            return Vector2D(other - self.x, other - self.y)

    def __isub__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            self.x -= other.x
            self.y -= other.y
        # Liste, array, or tuple
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        # Si on soustrait par un simple nombre
        else:
            self.x -= other
            self.y -= other
        return self

    def __mul__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        # Liste, array, or tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(self.x * other[0], self.y * other[1])
        # Number
        else:
            return Vector2D(self.x * other, self.y * other)
    __rmul__ = __mul__

    def __imul__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            self.x *= other.x
            self.y *= other.y
        # Liste, array, or tuple
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        # Number
        else:
            self.x *= other
            self.y *= other
        return self

    def __truediv__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)
        # Liste, array, or tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(self.x / other[0], self.y / other[1])
        # Number
        else:
            return Vector2D(self.x / other, self.y / other)

    def __rtruediv__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            return Vector2D(other.x / self.x, other.y / self.y)
        # Liste, array, or tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(other[0] / self.x, other[1] / self.y)
        # Number
        else:
            raise TypeError(other, type(other), "Must be a list, tuple, array, or Vector2D")

    def __itruediv__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            self.x /= other.x
            self.y /= other.y
        # Liste, array, or tuple
        elif (hasattr(other, "__getitem__")):
            self.x /= other[0]
            self.y /= other[1]
        # Number
        else:
            self.x /= other
            self.y /= other
        return self

    # Keep only python3 division
    __div__, __rdiv__, __idiv__ = __truediv__, __rtruediv__, __itruediv__

    def __floordiv__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            return Vector2D(self.x // other.x, self.y // other.y)
        # Liste, array, or tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(self.x // other[0], self.y // other[1])
        # Number
        else:
            return Vector2D(self.x // other, self.y // other)

    def __rfloordiv__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            return Vector2D(other.x // self.x, other.y // self.y)
        # Liste, array, or tuple
        if (hasattr(other, "__getitem__")):
            return Vector2D(other[0] // self.x, other[1] // self.y)
        # Number
        else:
            raise TypeError(other, type(other), "Must be a list, tuple, array, or Vector2D")

    def __ifloordiv__(self, other):
        # Vector
        if isinstance(other, Vector2D):
            self.x //= other.x
            self.y //= other.y
        # Liste, array, or tuple
        elif (hasattr(other, "__getitem__")):
            self.x //= other[0]
            self.y //= other[1]
        # Number
        else:
            self.x //= other
            self.y //= other
        return self

    def __mod__(self, other):
        return self._operator_handler(other, operator.mod)

    def __rmod__(self, other):
        return self._r_operator_handler(other, operator.mod)

    def __pow__(self, other):
        return self._operator_handler(other, operator.pow)

    def __rpow__(self, other):
        return self._r_operator_handler(other, operator.pow)

    # Arithmetic operation
    def __neg__(self):
        """Return opposite for each vector elements"""
        return Vector2D(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self):
        """Return each elements from the vectors with no changes"""
        return Vector2D(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self):
        """Return for ech elements abs(element)"""
        return Vector2D(abs(self.x), abs(self.y))

    def __invert__(self):
        """Reverse the vector"""
        return Vector2D(-self.x, -self.y)

    # Pickle
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
            print("Creation succeed")

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
            print("Math operations succeed")

        def testReverseMath(self):
            v = Vector2D(111, 222)
            self.assertEqual(1 + v, Vector2D(112, 223))
            self.assertEqual(2 - v, [-109, -220])
            self.assertEqual(3 * v, (333, 666))
            self.assertEqual([222, 888] / v, [2, 4])
            self.assertEqual([111, 222] ** Vector2D(2, 3), [12321, 10941048])
            self.assertEqual([-11, 78] + v, Vector2D(100, 300))
            self.assertEqual(Vector2D(1110, 4410) // v, (10, 19))
            print("Reversed math operations succeed")

        def testArithmetric(self):
            v = Vector2D(111, 222)
            v = -v
            self.assertTrue(v, [-111, -222])
            v = abs(v)
            self.assertTrue(v, [111, 222])
            print("Arithmetics succeed")

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
            print("Comparisons succeed")

        def testMagnitude(self):
            v = Vector2D(3, 4)
            self.assertEqual(v.magnitude, 5)
            self.assertEqual(v.normalize(), 5)
            self.assertEqual(v.magnitude, 1)
            v.magnitude = 5
            self.assertEqual(v, Vector2D(3, 4))
            v2 = Vector2D(10, -2)
            self.assertEqual(v.get_distance(v2), (v - v2).get_magnitude())
            print("Magnitude succeed")

        def testCrossInterpolate(self):
            v = Vector2D(1, .5)
            u = Vector2D(10, 8)
            self.assertTrue(v.cross(u) == 3)
            self.assertTrue(v.interpolate_to(u, 1) == u)
            print("Interpolations succeed")

        def testCopy(self):
            v = Vector2D(55, 55)
            b = Vector2D(v)  # Create copy
            c = v  # Create alias
            v.normalize()
            self.assertFalse(v == b)
            self.assertTrue(v == c)
            print("Copy succeed")

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
            print(".Angle succeed")

        def testCrossDot(self):
            vect = Vector2D(1, .5)
            vect2 = Vector2D(4, 6)
            self.assertTrue(vect.cross(vect2) == 4)
            self.assertTrue(vect.dot(vect2) == 7)
            print("Cross and dot products succeed")

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
            print("Inplace operators succeed")

        def testPickle(self):
            testvec = Vector2D(5, .3)
            testvec_str = pickle.dumps(testvec)
            loaded_vec = pickle.loads(testvec_str)
            self.assertEqual(testvec, loaded_vec)
            print("Pickle succeed")

    unittest.main()
