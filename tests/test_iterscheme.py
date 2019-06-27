# -*- coding: utf-8 -*-


import pytest
from iterscheme import IterationSchemeElement, IterationScheme, \
                       NoConstants, Constants, named_parameter, \
                       dict_adapter, namedtuple_adapter
import numpy

IS = IterationScheme
ISE = IterationSchemeElement


def test_noconst():
    ischeme = NoConstants()
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(len(ischeme_content) == 1)
    assert(ischeme_content == [()])


def test_one_const_only():
    ischeme = Constants(0.5)
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(len(ischeme_content) == 1)
    assert(ischeme_content == [(0.5,)])


def test_mult_const_only():
    ischeme = Constants(0.5, 's')
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(len(ischeme_content) == 1)
    assert(ischeme_content == [(0.5,'s',)])


def test_vector_const_only():
    ischeme = Constants([1,2,3])
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(len(ischeme_content) == 1)
    assert(ischeme_content == [([1,2,3],)])


def test_one_level_loop():
    ischeme = Constants(0.5) >> ISE([1,2,3])
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(len(ischeme_content) == 3)
    assert(ischeme_content[0] == (0.5, 1, ))
    assert(ischeme_content[1] == (0.5, 2, ))
    assert(ischeme_content[2] == (0.5, 3, ))


def test_two_level_loop():
    ischeme = Constants(0.5) >> ISE([1,2,3]) >> ISE([4,5,6])
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(len(ischeme_content) == 9)
    assert(ischeme_content[0] == (0.5, 1, 4, ))
    assert(ischeme_content[1] == (0.5, 1, 5, ))
    assert(ischeme_content[2] == (0.5, 1, 6, ))
    assert(ischeme_content[3] == (0.5, 2, 4, ))
    assert(ischeme_content[4] == (0.5, 2, 5, ))
    assert(ischeme_content[5] == (0.5, 2, 6, ))
    assert(ischeme_content[6] == (0.5, 3, 4, ))
    assert(ischeme_content[7] == (0.5, 3, 5, ))
    assert(ischeme_content[8] == (0.5, 3, 6, ))


def test_vector_var():
    ischeme = Constants(0.5) >> ISE([[1,2,3], [4,5,6], [7,8,9]])
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(len(ischeme_content) == 3)
    assert(ischeme_content[0] == (0.5, [1,2,3], ))
    assert(ischeme_content[1] == (0.5, [4,5,6], ))
    assert(ischeme_content[2] == (0.5, [7,8,9], ))


def test_combined_loop():
    ischeme = Constants(0.5) >> ISE([1,2,3], [4,5,6])
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(len(ischeme_content) == 3)
    assert(ischeme_content[0] == (0.5, 1, 4, ))
    assert(ischeme_content[1] == (0.5, 2, 5, ))
    assert(ischeme_content[2] == (0.5, 3, 6, ))


def test_pass_element():
    ischeme = Constants(0.5) >> ISE([1,2,3])
    ischeme_content = list(IS(ischeme))

    assert(len(ischeme_content) == 3)
    assert(ischeme_content[0] == (0.5, 1, ))
    assert(ischeme_content[1] == (0.5, 2, ))
    assert(ischeme_content[2] == (0.5, 3, ))


def test_dict_adapter():
    c1 = named_parameter('c1', 0.5)
    x = named_parameter('x', [1,2,3])
    y = named_parameter('y', ['a','b','c'])

    ischeme = Constants(c1) >> ISE(x) >> ISE(y)
    ischeme_content = list(dict_adapter(IS(ischeme.nested_variables)))

    assert(len(ischeme_content) == 9)
    assert(ischeme_content[0] == dict(c1=0.5, x=1, y='a'))
    assert(ischeme_content[1] == dict(c1=0.5, x=1, y='b'))
    assert(ischeme_content[2] == dict(c1=0.5, x=1, y='c'))
    assert(ischeme_content[3] == dict(c1=0.5, x=2, y='a'))
    assert(ischeme_content[4] == dict(c1=0.5, x=2, y='b'))
    assert(ischeme_content[5] == dict(c1=0.5, x=2, y='c'))
    assert(ischeme_content[6] == dict(c1=0.5, x=3, y='a'))
    assert(ischeme_content[7] == dict(c1=0.5, x=3, y='b'))
    assert(ischeme_content[8] == dict(c1=0.5, x=3, y='c'))


def test_namedtuple_adapter():
    c1 = named_parameter('c1', 0.5)
    x = named_parameter('x', [1,2,3])
    y = named_parameter('y', ['a','b','c'])

    ischeme = Constants(c1) >> ISE(x) >> ISE(y)
    ischeme_content = list(namedtuple_adapter(IS(ischeme.nested_variables)))

    assert(len(ischeme_content) == 9)
    for entry, xval, yval in zip(ischeme_content, [1,1,1,2,2,2,3,3,3], ['a','b','c']*3):
        assert(entry.c1 == 0.5)
        assert(entry.x == xval)
        assert(entry.y == yval)


def test_numpy():
    ischeme = Constants(0.5) >> ISE(numpy.array([1,2,3]))
    ischeme_content = list(IS(ischeme))

    assert(len(ischeme_content) == 3)
    assert(ischeme_content[0] == (0.5, 1, ))
    assert(ischeme_content[1] == (0.5, 2, ))
    assert(ischeme_content[2] == (0.5, 3, ))


def test_named_numpy():
    c1 = named_parameter('c1', 0.5)
    x = named_parameter('x', numpy.array([1,2,3]))
    ischeme = Constants(c1) >> ISE(x)
    ischeme_content = list(namedtuple_adapter(IS(ischeme)))

    assert(len(ischeme_content) == 3)
    for entry, xval in zip(ischeme_content, [1,2,3]):
        assert(entry.c1 == 0.5)
        assert(entry.x == xval)


def test_named_numpy_2():
    c1 = named_parameter('c1', 0.5)
    x = named_parameter('x', numpy.array([1.0,2.0,3.0]))
    ischeme = Constants(c1) >> ISE(x)
    ischeme_content = list(namedtuple_adapter(IS(ischeme)))

    assert(len(ischeme_content) == 3)
    for entry, xval in zip(ischeme_content, [1.0,2.0,3.0]):
        assert(entry.c1 == 0.5)
        assert(entry.x == xval)

