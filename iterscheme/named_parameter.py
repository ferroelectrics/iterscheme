# -*- coding: utf-8 -*-
"""
    named_parameter.py
    ~~~~~~~~~~~~

    Functionality for creation of named parameters for iteration schemes.
"""


from collections import namedtuple
import numpy
from .iterscheme import adapter


def named_parameter(name, values):
    """Creates wrapper around values with name attribute attached.
    Wrapper allows access to all functionality of values type.
    """

    inherit_from = type(values)
    if isinstance(values, bool):
        inherit_from = int

    def prepare_cons_args(values):
        args = list()
        kwargs = dict()
        if isinstance(values, (list, dict, set)):
            args = [values]
        elif isinstance(values, numpy.ndarray):
            kwargs = {'shape': values.shape, 
                      'buffer': values.data, 
                      'dtype': values.dtype}
        else:
            args = [values]

        return args, kwargs

    class Wrapper(inherit_from):  # pylint: disable=too-few-public-methods
        """Wrapper for collection of values that assigns
        name attribute to it and gives access to all
        functionality of values type.
        """

        @property
        def parameter_name(self):
            """Property for identification of collection by name.
            """
            return name

        def __getitem__(self, key):
            """Allows propagating of parameter name to slices.
            """
            if isinstance(key, slice):
                data = inherit_from.__getitem__(self, key)
                args, kwargs = prepare_cons_args(data)
                return Wrapper(*args, **kwargs)

            return inherit_from.__getitem__(self, key)

    args, kwargs = prepare_cons_args(values)
    return Wrapper(*args, **kwargs)


def get_name(entity):
    """Helper function to extract name from named parameter
    """
    return entity.parameter_name


@adapter(get_name)
def dict_adapter(values, names):
    """Adapter returns name-values dict instead of pure tuple
    from iteration scheme.
    """
    return dict(zip(names, values))


@adapter(get_name)
def namedtuple_adapter(values, names):
    """Adapter returns namedtuple object instead of pure tuple
    from iteration scheme.
    """
    named = namedtuple('named', ' '.join(names))
    return named(*values)
