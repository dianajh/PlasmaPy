"""
Convert to and from Roman numerals.

This file is adapted from the roman package that is available on PyPI,
which has the following copyright/license information:

Copyright (c) 2001 Mark Pilgrim

This program is free software; you can redistribute it and/or modify
it under the terms of the Python 2.1.1 license, available at
https://www.python.org/download/releases/2.1.1/license/

"""

import re
import numpy as np
import typing


class RomanError(Exception):
    """A base exception for errors from `~plasmapy.utils.roman`."""
    pass


class OutOfRangeError(RomanError):
    """
    An exception to be raised for integers that outside of the range
    that can be converted to Roman numerals.
    """
    pass


class InvalidRomanNumeralError(RomanError):
    """
    An exception to be raised when the input is not a valid Roman
    numeral.
    """
    pass


#Define digit mapping
_romanNumeralMap = (('M', 1000),
                    ('CM', 900),
                    ('D',  500),
                    ('CD', 400),
                    ('C',  100),
                    ('XC', 90),
                    ('L',  50),
                    ('XL', 40),
                    ('X',  10),
                    ('IX', 9),
                    ('V',  5),
                    ('IV', 4),
                    ('I',  1))

#Define pattern to detect valid Roman numerals
_romanNumeralPattern = re.compile("""
    ^                   # beginning of string
    M{0,4}              # thousands - 0 to 4 M's
    (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                        #            or 500-800 (D, followed by 0 to 3 C's)
    (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                        #        or 50-80 (L, followed by 0 to 3 X's)
    (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                        #        or 5-8 (V, followed by 0 to 3 I's)
    $                   # end of string
    """, re.VERBOSE)



def toRoman(n: typing.Union[int, np.integer]) -> str:
    """
    Convert an integer to a Roman numeral.

    Parameters
    ----------
    n : int or `~numpy.integer`
        The integer to be converted to a Roman numeral that must be
        between 1 and 4999, inclusive.

    Returns
    -------
    result : str
        The number in Roman numeral notation.

    Raises
    ------
    TypeError
        If the input is not an integer.

    ~plasmapy.utils.roman.OutOfRangeError
        If the number is not between 1 and 4999, inclusive.

    See Also
    --------
    fromRoman

    Examples
    --------
    >>> toRoman(5)
    'V'
    >>> toRoman(2525)
    'MMDXXV'

    """
    if not isinstance(n, (int, np.integer)):
        raise TypeError(f"{n} cannot be converted to a Roman numeral.")
    if not (0 < n < 5000):
        raise OutOfRangeError("Number is out of range (need 0 < n < 5000)")

    result = ""
    for numeral, integer in _romanNumeralMap:
        while n >= integer:
            result += numeral
            n -= integer
    return result


def fromRoman(s: str) -> int:
    """
    Convert a Roman numeral to an integer.

    Parameters
    ----------
    s : str
        A Roman numeral.

    Returns
    -------
    result : int
        The integer corresponding to the Roman numeral.

    Raises
    ------
    TypeError
        The argument is not a `str`.

    ~plasmapy.utils.roman.InvalidRomanNumeralError
        The argument is not a valid Roman numeral.

    See Also
    --------
    toRoman

    Examples
    --------
    >>> fromRoman('V')
    5
    >>> fromRoman('MMMMCCCLXVII')
    4367

    """
    if not isinstance(s, str):
        raise TypeError('The argument to fromRoman must be a string.')
    if not _romanNumeralPattern.search(s):
        raise InvalidRomanNumeralError('Invalid Roman numeral: %s' % s)

    result = 0
    index = 0
    for numeral, integer in _romanNumeralMap:
        while s[index:index+len(numeral)] == numeral:
            result += integer
            index += len(numeral)
    return result
