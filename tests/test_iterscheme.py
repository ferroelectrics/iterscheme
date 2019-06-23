# -*- coding: utf-8 -*-


import pytest
from iterscheme import IterationSchemeElement, IterationScheme, \
                       NoConstants, Constants


IS = IterationScheme
ISE = IterationSchemeElement


def test_noconst():
    ischeme = NoConstants()
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(ischeme_content == [()])

def test_one_const_only():
    ischeme = Constants(0.5)
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(ischeme_content == [(0.5,)])

def test_mult_const_only():
    ischeme = Constants(0.5, 's')
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(ischeme_content == [(0.5,'s',)])

def test_vector_const_only():
    ischeme = Constants([1,2,3])
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(ischeme_content == [([1,2,3],)])

def test_one_level_loop():
    ischeme = Constants(0.5) >> ISE([1,2,3])
    ischeme_content = list(IS(ischeme.nested_variables))

    assert(ischeme_content[0] == (0.5, 1, ))
    assert(ischeme_content[1] == (0.5, 2, ))
    assert(ischeme_content[2] == (0.5, 3, ))

def test_two_level_loop():
    ischeme = Constants(0.5) >> ISE([1,2,3]) >> ISE([4,5,6])
    ischeme_content = list(IS(ischeme.nested_variables))

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

    assert(ischeme_content[0] == (0.5, 1, 4, ))
    assert(ischeme_content[1] == (0.5, 2, 5, ))
    assert(ischeme_content[2] == (0.5, 3, 6, ))

def test_pass_element():
    ischeme = Constants(0.5) >> ISE([1,2,3])
    ischeme_content = list(IS(ischeme))

    assert(ischeme_content[0] == (0.5, 1, ))
    assert(ischeme_content[1] == (0.5, 2, ))
    assert(ischeme_content[2] == (0.5, 3, ))

