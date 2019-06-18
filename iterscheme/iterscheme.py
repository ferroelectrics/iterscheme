# -*- coding: utf-8 -*-
"""
    iterscheme.py
    ~~~~~~~~~~~~~

    Implementation of declarative iteration scheme.
"""


from itertools import product


class IterationScheme():
    """:class:`iterscheme.IterationScheme` object represents
    one of the levels of nested for loop structure. Combining
    multiple instances results in whole iteration scheme from
    which all iteration parameters can be accessed linearly.

    When instance of this class is asked for :meth:`__iter__`
    no more adding of new components is allowed.
    """
    def __init__(self, *values):
        if values:
            self._values = [values]
        else:
            self._values = [[]]
        self._iterator = None

    def __rshift__(self, other):
        """Method for combining parts of iteration scheme::

            IS = IterationScheme
            IS([1,2,3]) >> IS(['a','b','c'], [obj1,obj2,obj3])
        """
        if self._iterator is not None:
            raise Exception('Iteration scheme is ready!'
                            'Can\'t add more parameters.')
        self._values.extend(other._values)  # pylint: disable=protected-access
        return self

    def __iter__(self):
        """TODO: Explain packing of scalar arguments and other things
        """
        if self._values[0]:
            self._values[0] = tuple([v] for v in self._values[0])
        else:
            self._values = self._values[1:]
        product_components = (zip(*v) for v in self._values)
        self._iterator = product(*product_components)
        return self

    def __next__(self):
        return tuple(i for v in next(self._iterator) for i in v)


def NoConstants():  # pylint: disable=invalid-name
    """When no constants needed use this function
        as first component in scheme.
    """
    return IterationScheme()


def Constants(*values):  # pylint: disable=invalid-name
    """Wrapper for first component in IterationScheme.
    """
    return IterationScheme(*values)
