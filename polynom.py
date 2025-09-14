import itertools
import functools
import math


class Polynom:
    """
    Diese Klasse modelliert ein Polynom
    """    
    def __init__(self, coefficients):
        """
        Die uebergebene Koeffizienten-Liste bestimmt den Grad des Polynoms.
        Sie sind in aufsteigender Reihenfolge, d.h. 'coefficients[i]' ist der Skalar vor x**i.
        """
        coefficients = list(coefficients)

        # ueberfluessige Nullen abschneiden
        i = len(coefficients) - 1
        while i >= 0 and coefficients[i] == 0:
            i -= 1
        
        self._coefficients = coefficients[:i+1]
    
    def deg(self):
        return len(self._coefficients) - 1 if len(self._coefficients) > 0 else -math.inf
    
    def __call__(self, x):
        """
        Liefert den Wert dieses Polynoms an der Stelle x zurueck.
        """
        # TODO: Hier kommt ihr Code
        pass

    def __str__(self):
        """
        Gibt eine String-Repraesentation dieses Polynoms zurueck.
        """
        # TODO: Hier kommt ihr Code
        pass
    
    def __add__(self, other):
        """
        Liefert die Summe dieses Polynoms mit einem anderen oder einer Zahl zurueck.
        """
        # TODO: Hier kommt ihr Code
        pass
    
    def __radd__(self, other):
        # TODO: Hier kommt ihr Code
        pass
    
    def __mul__(self, other):
        """
        Liefert das Produkt dieses Polynoms mit einem anderen oder einer Zahl zurueck.
        """
        # TODO: Hier kommt ihr Code
        pass
    
    def __rmul__(self, other):
        # TODO: Hier kommt ihr Code
        pass
    
    def __neg__(self):
        """
        Liefert die Negation dieses Polynoms zurueck.
        """
        # TODO: Hier kommt ihr Code
        pass
    
    def __sub__(self, other):
        """
        Liefert die Differenz dieses Polynoms mit einem anderen oder einer Zahl zurueck.
        """
        # TODO: Hier kommt ihr Code
        pass
    
    def __rsub__(self, other):
        # TODO: Hier kommt ihr Code
        pass
    
    def __pow__(self, exp):
        """
        Liefert die ganzzahlige Potenz dieses Polynoms mit Exponent 'exp' zurueck.
        """
        # TODO: Hier kommt ihr Code
        pass
    
    
    # TODO: Hier kommt ihr Code


if __name__ == "__main__":
    # Test __init__
    p = Polynom([1, 0, 3])
    p2 = Polynom([-3, 1, 2])

    # Teste __call__
    print("__call__ ", p(42))
    
    # Teste __str__
    print("__str__  ", p)
    
    # Teste __add__ und __radd__
    # __add__ mit einem anderen Polynom
    print("__add__  ", p + p2)
    # __add__ mit einer Zahl
    print("__add__  ", p + 1)
    # __radd__ mit einer Zahl
    print("__radd__ ", 1 + p)
    
    # Teste __mul__ und __rmul__
    # __mul__ mit einem anderen Polynom
    print("__mul__  ", p * p2)
    # __mul__ mit einer Zahl
    print("__mul__  ", p * 4)
    # __rmul__ mit einer Zahl
    print("__rmul__ ", 4 * p)
    
    # Teste __neg__
    print("__neg__  ", -p)
    
    # Teste __sub__ und __rsub__
    # __sub__ mit einem anderen Polynom
    print("__sub__  ", p - p2)
    # __sub__ mit einer Zahl
    print("__sub__  ", p - 1)
    # __rsub__ mit einer Zahl
    print("__rsub__ ", 1 - p)
    
    # Teste __pow__
    print("__pow__  ", p**3)


    print()
    # Teste staticmethod 'Polynom.x()'
    x = Polynom.x()
    p3 = 1337 * x**3 - 42 * x +69
    print(p3)
    print(p3(3.141592))
    
