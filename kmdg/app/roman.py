#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

rom_map = (("M", 1000),
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
        ("I", 1))

def convert2roman(n):
    """Convert integer to Roman numeral"""

    if n <= 0 or n > 3999:
        return "N/A"

    result = ''
    for numeral, integer in rom_map:

        while n >= integer:
            result += numeral
            n -= integer

    return result


### TEST MODUŁU
if __name__ == "__main__":

    print convert2roman(19)
    print convert2roman(6)
    print convert2roman(2)
    print convert2roman(133)
    print convert2roman(200)
    print convert2roman(888)
    print convert2roman(134)
