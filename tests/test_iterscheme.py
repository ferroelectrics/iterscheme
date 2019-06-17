# -*- coding: utf-8 -*-


import pytest
from iterscheme import IterationScheme, NoConstants


IS = IterationScheme


def test_basics():
    const1 = 0.5
    const2 = 's'
    const3 = [1, 2, 3]
    var1 = [4, 5, 6]
    var2 = ['a', 'b', 'c']
    var3 = [101, 102, 103]

    is1 = IS(const1, const2) >> IS(var1)
    is1_content = list(is1)

    assert(len(is1_content) == 3)
    assert(is1_content[0] == (0.5, 's', 4))
    assert(is1_content[1] == (0.5, 's', 5))
    assert(is1_content[2] == (0.5, 's', 6))

    is2 = NoConstants() >> IS(var1) >> IS(var2)
    is2_content = list(is2)

    assert(len(is2_content) == 9)
    assert(is2_content[0] == (4, 'a'))
    assert(is2_content[1] == (4, 'b'))
    assert(is2_content[2] == (4, 'c'))
    assert(is2_content[3] == (5, 'a'))
    assert(is2_content[4] == (5, 'b'))
    assert(is2_content[5] == (5, 'c'))
    assert(is2_content[6] == (6, 'a'))
    assert(is2_content[7] == (6, 'b'))
    assert(is2_content[8] == (6, 'c'))

    is3 = NoConstants() >> IS(var1) >> IS(var2, var3)
    is3_content = list(is3)

    assert(len(is3_content) == 9)
    assert(is3_content[0] == (4, 'a', 101))
    assert(is3_content[1] == (4, 'b', 102))
    assert(is3_content[2] == (4, 'c', 103))
    assert(is3_content[3] == (5, 'a', 101))
    assert(is3_content[4] == (5, 'b', 102))
    assert(is3_content[5] == (5, 'c', 103))
    assert(is3_content[6] == (6, 'a', 101))
    assert(is3_content[7] == (6, 'b', 102))
    assert(is3_content[8] == (6, 'c', 103))

    is4 = IS(const3) >> IS(var1)
    is4_content = list(is4)

    assert(len(is4_content) == 3)
    assert(is4_content[0] == ([1, 2, 3], 4))
    assert(is4_content[1] == ([1, 2, 3], 5))
    assert(is4_content[2] == ([1, 2, 3], 6))