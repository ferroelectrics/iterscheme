# -*- coding: utf-8 -*-
"""
    iterscheme.py
    ~~~~~~~~~~~~~

    Implementation of declarative iteration scheme.
"""


from itertools import product


class IterationSchemeElement():
    """:class:`iterscheme.IterationSchemeElement` describes
    variables on one of the levels in the nested for loop
    structure. For example::

                                        # ISC = IterationSchemeElement
    for i in [...]:                     # i = ISC([...])
        for j,k  in zip([...], ...[]):  # jk = ISC([...], [...])
            for l in [...]:             # l = ISC([...])
    """
    def __init__(self, *variables):
        if variables:
            self._variables = [variables]
        else:
            # We simulate lack of outermost level variables this way
            self._variables = [[]]

    def __rshift__(self, other_element):
        """:meth:`__rshift__` allows chaining of multiple
        elements, what simulates nesting more loops::

        ISC = IterationSchemeElement
        ISC(x) >> ISC(y) >> ISC(z)
        """
        self._variables.extend(other_element._variables)  # pylint: disable=protected-access
        return self

    @property
    def nested_variables(self):
        """Simple property to retrieve variables structure from
        :class:`iterscheme.IterationSchemeElement` object.

        TODO:: Think about copying issues
        """
        return self._variables


class IterationScheme():
    """:class:`iterscheme.IterationScheme` object represents
    nested for loop structure, which support linear iteration
    over values.

    Constructor supports :class:`iterscheme.IterationSchemeElement`
    as :arg:`nested_variables`, but one can build this structure
    manually.
    """
    def __init__(self, nested_variables):
        if isinstance(nested_variables, IterationSchemeElement):
            self._nested_variables = nested_variables.nested_variables
        else:
            self._nested_variables = nested_variables
        self._iterator = None

    def properties(self, property_getter):
        return [property_getter(var) 
                for nested_var in self._nested_variables 
                for var in nested_var]

    def __iter__(self):
        """TODO: Explain packing of scalar arguments and other things
        """
        if self._nested_variables[0]:
            self._nested_variables[0] = \
                    tuple([v] for v in self._nested_variables[0])
        else:
            self._nested_variables = self._nested_variables[1:]
        product_components = (zip(*v) for v in self._nested_variables)
        self._iterator = product(*product_components)
        return self

    def __next__(self):
        """Iteration scheme returs plain tuple of values
        without annotation of any kind. User can only rely
        on order of values in this tuple. If elements look
        like `ISE(x) >> ISE(y,z) >> ISE(w)` then every tuple
        is (element_of_x, element_of_y, element_of_z, element_of_w)
        """
        return tuple(i for v in next(self._iterator) for i in v)


def adapter(property_getter):
    """
    """
    def getter_assigned(adapter_func):
        def adapted(ischeme):
            properties = ischeme.properties(property_getter)
            for bunch_of_values in ischeme:
                yield adapter_func(bunch_of_values, properties)

        return adapted

    return getter_assigned
    

def NoConstants():  # pylint: disable=invalid-name
    """When no constants needed use this function
        as first component in scheme.
    """
    return IterationSchemeElement()


def Constants(*values):  # pylint: disable=invalid-name
    """Wrapper for first component in IterationScheme.
    """
    return IterationSchemeElement(*values)
