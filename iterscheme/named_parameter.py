# -*- coding: utf-8 -*-
"""
    named_parameter.py
    ~~~~~~~~~~~~

    Functionality for creation of named parameters for iteration schemes.
"""

from .iterscheme import adapter
from collections import namedtuple


def named_parameter(name, values):
    """Creates wrapper around values with name attribute attached.
        Wrapper allows access to all functionality of values type.
    """

    class Wrapper(type(values)): #  pylint: disable=too-few-public-methods
        """Wrapper for collection of values that assigns
            name attribute to it and gives access to all
            functionality of values type.
        """

        @property
        def parameter_name(self):
            """Property for identification of collection by name.
            """
            return name

    return Wrapper(values)


def get_name(entity):
    """
    """
    return entity.parameter_name


@adapter(get_name)
def dict_adapter(values, names):
    """
    """
    return dict(zip(names, values))

@adapter(get_name)
def namedtuple_adapter(values, names):
    """
    """
    named = namedtuple('named', ' '.join(names))
    
    return named(*values)
