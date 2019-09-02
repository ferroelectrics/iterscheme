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


def test_combined_loop():
    ischeme = Constants(0.5) >> ISE([1,2,3], [4,5,6])
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(len(ischeme_content) == 3)
    assert(ischeme_content[0] == (0.5, 1, 4, ))
    assert(ischeme_content[1] == (0.5, 2, 5, ))
    assert(ischeme_content[2] == (0.5, 3, 6, ))


def test_vector_var():
    ischeme = Constants(0.5) >> ISE([[1,2,3], [4,5,6], [7,8,9]])
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(len(ischeme_content) == 3)
    assert(ischeme_content[0] == (0.5, [1,2,3], ))
    assert(ischeme_content[1] == (0.5, [4,5,6], ))
    assert(ischeme_content[2] == (0.5, [7,8,9], ))


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

def test_single_bool_named():
    c1 = named_parameter('c1', False)
    ischeme = Constants(c1)
    ischeme_content = list(IS(ischeme))

    assert(len(ischeme_content) == 1)
    assert(ischeme_content[0] == (False,))

def test_single_string():
    ischeme = Constants('some_string')
    ischeme_content = list(IS(ischeme))

    assert(len(ischeme_content) == 1)
    assert(ischeme_content[0] == ('some_string',))

def test_single_string_named():
    c1 = named_parameter('c1', 'some_string')
    ischeme = Constants(c1)
    ischeme_content = list(IS(ischeme))

    assert(len(ischeme_content) == 1)
    assert(ischeme_content[0] == ('some_string',))

def test_splitter():
    c1 = named_parameter('c', 0.5)
    x = named_parameter('x', [1,2,3,4,5,6])
    ischeme = Constants(c1) >> ISE(x).split(2)
    ischeme_parts = ischeme.nested_variables
    ischeme_content = [IS(part) for part in ischeme_parts]
    parts = [list(p) for p in ischeme_content]
    
    assert(len(parts) == 2)
    assert(len(parts[0]) == 3)
    assert(len(parts[1]) == 3)
    assert(parts[0][0] == (0.5, 1, ))
    assert(parts[0][1] == (0.5, 2, ))
    assert(parts[0][2] == (0.5, 3, ))
    assert(parts[1][0] == (0.5, 4, ))
    assert(parts[1][1] == (0.5, 5, ))
    assert(parts[1][2] == (0.5, 6, ))


def test_splitter_odd():
    c1 = named_parameter('c', 0.5)
    x = named_parameter('x', [1,2,3,4,5,6,7])
    ischeme = Constants(c1) >> ISE(x).split(2)
    ischeme_parts = ischeme.nested_variables
    ischeme_content = [IS(part) for part in ischeme_parts]
    parts = [list(p) for p in ischeme_content]
    
    assert(len(parts) == 2)
    assert(len(parts[0]) == 3)
    assert(len(parts[1]) == 4)
    assert(parts[0][0] == (0.5, 1, ))
    assert(parts[0][1] == (0.5, 2, ))
    assert(parts[0][2] == (0.5, 3, ))
    assert(parts[1][0] == (0.5, 4, ))
    assert(parts[1][1] == (0.5, 5, ))
    assert(parts[1][2] == (0.5, 6, ))
    assert(parts[1][3] == (0.5, 7, ))


def test_splitter_multiple():
    c1 = named_parameter('c', 0.5)
    x = named_parameter('x', [1,2,3,4,5,6])
    y = named_parameter('y', 'abcdef')
    ischeme = Constants(c1) >> ISE(x,y).split(2)
    ischeme_parts = ischeme.nested_variables
    ischeme_content = [IS(part) for part in ischeme_parts]
    parts = [list(p) for p in ischeme_content]
    
    assert(len(parts) == 2)
    assert(len(parts[0]) == 3)
    assert(len(parts[1]) == 3)
    assert(parts[0][0] == (0.5, 1, 'a',))
    assert(parts[0][1] == (0.5, 2, 'b',))
    assert(parts[0][2] == (0.5, 3, 'c',))
    assert(parts[1][0] == (0.5, 4, 'd',))
    assert(parts[1][1] == (0.5, 5, 'e',))
    assert(parts[1][2] == (0.5, 6, 'f',))


def test_splitter_inset():
    c1 = named_parameter('c', 0.5)
    x = named_parameter('x', [1,2])
    y = named_parameter('y', ['a', 'b', 'c', 'd'])
    z = named_parameter('z', [11,22])
    ischeme = Constants(c1) >> ISE(x) >> ISE(y).split(2) >> ISE(z)
    ischeme_parts = ischeme.nested_variables
    ischeme_content = [IS(part) for part in ischeme_parts]
    parts = [list(p) for p in ischeme_content]
    
    assert(len(parts) == 2)
    assert(len(parts[0]) == 8)
    assert(len(parts[1]) == 8)
    assert(parts[0][0] == (0.5, 1, 'a', 11))
    assert(parts[0][1] == (0.5, 1, 'a', 22))
    assert(parts[0][2] == (0.5, 1, 'b', 11))
    assert(parts[0][3] == (0.5, 1, 'b', 22))
    assert(parts[0][4] == (0.5, 2, 'a', 11))
    assert(parts[0][5] == (0.5, 2, 'a', 22))
    assert(parts[0][6] == (0.5, 2, 'b', 11))
    assert(parts[0][7] == (0.5, 2, 'b', 22))
    assert(parts[1][0] == (0.5, 1, 'c', 11))
    assert(parts[1][1] == (0.5, 1, 'c', 22))
    assert(parts[1][2] == (0.5, 1, 'd', 11))
    assert(parts[1][3] == (0.5, 1, 'd', 22))
    assert(parts[1][4] == (0.5, 2, 'c', 11))
    assert(parts[1][5] == (0.5, 2, 'c', 22))
    assert(parts[1][6] == (0.5, 2, 'd', 11))
    assert(parts[1][7] == (0.5, 2, 'd', 22))

def test_splitter_noconstants():
    x = named_parameter('x', [1,2,3,4,5,6])
    ischeme = NoConstants() >> ISE(x).split(2)
    ischeme_parts = ischeme.nested_variables
    ischeme_content = [IS(part) for part in ischeme_parts]
    parts = [list(p) for p in ischeme_content]
    
    assert(len(parts) == 2)
    assert(len(parts[0]) == 3)
    assert(len(parts[1]) == 3)
    assert(parts[0][0] == (1, ))
    assert(parts[0][1] == (2, ))
    assert(parts[0][2] == (3, ))
    assert(parts[1][0] == (4, ))
    assert(parts[1][1] == (5, ))
    assert(parts[1][2] == (6, ))


def test_slice():
    x = named_parameter('x', [1,2,3,4,5,6])
    
    sl1 = x[:3]
    sl2 = x[3:]

    assert(len(sl1) == 3)
    assert(len(sl2) == 3)
    assert(sl1[0] == 1)
    assert(sl1[1] == 2)
    assert(sl1[2] == 3)
    assert(sl2[0] == 4)
    assert(sl2[1] == 5)
    assert(sl2[2] == 6)


def test_slice_numpy():
    x = named_parameter('x', numpy.array([1,2,3,4,5,6]))
    
    sl1 = x[:3]
    sl2 = x[3:]

    assert(len(sl1) == 3)
    assert(len(sl2) == 3)
    assert(sl1[0] == 1)
    assert(sl1[1] == 2)
    assert(sl1[2] == 3)
    assert(sl2[0] == 4)
    assert(sl2[1] == 5)
    assert(sl2[2] == 6)