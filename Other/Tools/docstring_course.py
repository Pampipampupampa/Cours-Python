#!/usr/bin/env python
# -*- coding: utf-8 -*-


def add(a, b):
    """
        Adds two numbers and returns the result.

        This add two real numbers and return a real result. You will want to
        use this function in any place you would usually use the ``+`` operator
        but requires a functional equivalent.

        :param a: The first number to add
        :param b: The second number to add
        :type a: int
        :type b: int
        :return: The result of the addition
        :rtype: int

        :Example:

        >>> add(1, 1)
        2
        >>> add(2.1, 3.4)  # all int compatible types work
        5.5

        Il faut préciser qu’on veut tester une sortie tronquée avec +ELLIPSIS :
        >>> print(list(range(20))) # doctest: +ELLIPSIS
        [0, 1, ..., 18, 19]

        >>> print(list(range(20))) # doctest: +ELLIPSIS
        ...                        # doctest: +NORMALIZE_WHITESPACE
        [0,    1, ...,   18,    19]

        Les espaces sont signficatifs, du coup il faut parfois marquer les tests
        avec +NORMALIZE_WHITESPACE :
        >>> print(list(range(20)))  # doctest: +NORMALIZE_WHITESPACE
        [0,   1,  2,  3,  4,  5,  6,  7,  8,  9,
        10,  11, 12, 13, 14, 15, 16, 17, 18, 19]

        .. seealso:: sub(), div(), mul()
        .. warnings:: This is a completly useless function. Use it only in a
                      tutorial unless you want to look like a fool.
        .. note:: You may want to use a lambda function instead of this.
        .. todo:: Delete this function. Then masturbate with olive oil.
    """
    return a + b


# TODO: un truc à faire (format à utiliser si on prévoit la modification car
#                        reconnu par certain pareurs)

# A la fin de votre script, mettez ce snippet qui va activer les doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
