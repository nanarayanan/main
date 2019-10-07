"""Provides two functions, number2roman() to convert a Number to a Roman Numeral
and roman2number() to convert a Roman Numeral to number.

Roman Numerals are valid only for the range 1..4999 (both inclusive).

"""

import sys

# number2roman() converts the given number to a Roman Numeral and returns the
# Roman Numeral as a string. If the given number is invalid---a number not in
# 1..4999, it returns the string "Invalid Number <the given number>".
#
# Traverse the number digit-by-digit in reverse and use roman_list[][] to get
# the associated roman number for that digit.

def number2roman(num: int) -> str:

    roman_list = [ [ "", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX" ],
                   [ "", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC" ],
                   [ "", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM" ],
                   [ "", "M", "MM", "MMM", "MMMM" ]
                  ]

    if (num < 1) or (num > 4999):
        return "Invalid Number " + str(num)

    digit = 0
    roman_numeral = ""

    while (num > 0):
        val = num % 10
        if (val > 0):
            roman_numeral = roman_list[digit][val] + roman_numeral
            # print("DBG: digit =", digit, " num =", num, " val =", val, " roman_numeral =", roman_numeral)
        num = num // 10
        digit = digit + 1

    return roman_numeral

# end def number2roman


# roman2number() converts the given Roman Numeral to a number and returns the
# number as a string. If the given Roman Numeral is invalid, it returns the
# string "Invalid Roman Numeral <the given roman_numeral>"
#
# This is a crude implementation in the sense that it compares the Roman Numeral
# for every number in the range 1..4999 (both inclusive) and compares if the
# returned Roman Numeral equals the Roman Numeral we are interested in.

def roman2number(roman_numeral: str) -> int:
    for num in range(1,5000):
        if (number2roman(num) == roman_numeral):
            return str(num)

    return "Invalid Roman Numeral " + roman_numeral

# end def roman2number


# main

while (True):
    print("Decimal to Roman Numeral: press 1");
    print("Roman Numeral to Decimal: press 2");
    option = int(input(""));
    if option == 1:
        num = int(input("Enter number (1 thru 4999) to be converted to a Roman Numeral: "))
        roman_numeral = number2roman(num)
        print("Roman Numeral for", num, "is", roman_numeral, "\n")
    elif option == 2:
        roman_numeral = input("Enter a Roman Numeral: ")
        num = roman2number(roman_numeral)
        print("Number for", roman_numeral, "is", num, "\n")
    else:
        print("Invalid Option; expected input is 1 or 2");

# end of main
