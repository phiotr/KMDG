#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

rom_map = (
    ("M", 1000),
    ("CM", 900),
    ("D", 500),
    ("CD", 400),
    ("C", 100),
    ("XC", 90),
    ("L", 50),
    ("XL", 40),
    ("X", 10),
    ("IX", 9),
    ("V", 5),
    ("IV", 4),
    ("I", 1),
)


def convert2roman(n):
    """Convert integer to Roman numeral"""
    if n <= 0 or n > 3999:
        return "N/A"
    else:
        result = ''
        for numeral, integer in rom_map:
            while n >= integer:
                result += numeral
                n -= integer
        return result


if __name__ == "__main__":
    assert(convert2roman(19) == 'XIX')
    assert(convert2roman(6) == 'VI')
    assert(convert2roman(2) == 'II')
    assert(convert2roman(133) == 'CXXXIII')
    assert(convert2roman(200) == 'CC')
    assert(convert2roman(888) == 'DCCCLXXXVIII')
    assert(convert2roman(134) == 'CXXXIV')
