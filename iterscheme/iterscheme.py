# -*- coding: utf-8 -*-
"""
    iterscheme.py
    ~~~~~~~~~~~~~

    Implementation of declarative iteration scheme.
"""


from itertools import product
from collections import namedtuple


class IterationSchemeElement():
    """:class:`iterscheme.IterationSchemeElement` describes
    variables on one of the levels in the nested for loop
    structure. For example::

                                        # ISC = IterationSchemeElement
    for i in [...]:                     # i = ISC([...])
        for j,k  in zip([...], ...[]):  # jk = ISC([...], [...])
            for l in [...]:             # l = ISC([...])
    """
    
    _split = namedtuple('split', 'variables slices')

    def __init__(self, *variables):
        if variables:
            self._variables = [self._split(variables, None)]
        else:
            # We simulate lack of outermost level variables this way
            self._variables = [self._split([], None)]

    def __rshift__(self, other_element):
        """:meth:`__rshift__` allows chaining of multiple
        elements, what simulates nesting more loops::

        ISC = IterationSchemeElement
        ISC(x) >> ISC(y) >> ISC(z)
        """

        #sliced = []
        #if self._variables.slices:
        #    for sl in self._variables.slices:
        #        sliced.append(tuple(var[sl] for var in self._variables.variables))
        #    self._components.append(sliced)
        #else:
        #    self._components.append(other_element._variables)  # pylint: disable=protected-access

        self._variables.extend(other_element._variables)  # pylint: disable=protected-access
        return self

    def _split_at(self, n):
        l = len(self._variables[0].variables[0])
        div = l // n
        slices = [slice(div*i, div*(i+1)) for i in range(n-1)]
        slices.append(slice(slices[-1].stop, l))
        return slices 

    def split(self, n):
        """:meth:`split` splits current element container 
        into n chunks of equal size.
        """
        equal_len = all(len(v)==len(self._variables[0].variables[0]) 
                    for v in self._variables[0].variables[1:])
        if not equal_len:
            raise Exception("")
        self._variables[0] = self._split(self._variables[0].variables, self._split_at(n))

        return self

    def _unpack_slices(self, variables):
        if variables.slices is None:
            return variables.variables

        sliced = []
        for sl in variables.slices:
            sliced.append(tuple(var[sl] for var in variables.variables))

        return sliced

    def _left_tuple(self, l):
        if len(l) == 1:
            return l[0]

        return l

    @property
    def nested_variables(self):
        """Simple property to retrieve variables structure from
        :class:`iterscheme.IterationSchemeElement` object.

        TODO:: Think about copying issues
        """

        slices_exist = any(v.slices for v in self._variables)

        if slices_exist:
            slices = []
            vs = [self._unpack_slices(v) for v in self._variables]

            slice_encountered = True

            while slice_encountered:
                slice_encountered = False
                sl = []
                for i, v in enumerate(vs):
                    if isinstance(v, tuple):
                        sl.append(v)
                    elif isinstance(v, list):
                        if len(v) > 0:
                            sl.append(v[0])
                            vs[i] = self._left_tuple(vs[i][1:])
                            slice_encountered = True
                        else:
                            sl.append([])

                slices.append(sl)

            return slices
        else:
            return [v.variables for v in self._variables]


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
        """With :func:`property_getter` supplied creates list
        of variable's properties for adapter function.
        """
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
    """:func:`iterscheme.adapter` transforms pure tuple output
    from :class:`iterscheme.IterationScheme` object to representation
    described by :arg:`adapter_func` of :func:`getter_assigned`.
    :arg:`property_getter` describes how property assigned to single
    variable from `IterationScheme` object can be extracted.
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
