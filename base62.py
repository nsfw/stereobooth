#!/usr/bin/env python

#
# Converts any integer into a base [BASE] number. I have chosen 62
# as it is meant to represent the integers using all the alphanumeric
# characters, [no special characters] = {0..9}, {A..Z}, {a..z}
#
# I plan on using this to shorten the representation of possibly long ids,
# a la url shortenters
#
# encode()  takes the base 62 key, as a string, and turns it back into an integer
# decode() takes an integer and turns it into the base 62 string
#
import math
import sys

BASE = 62

UPPERCASE_OFFSET = 55
LOWERCASE_OFFSET = 61
DIGIT_OFFSET = 48

def true_ord(char):
    """
    Turns a digit [char] in character representation
    from the number system with base [BASE] into an integer.
    """

    if char.isdigit():
        return ord(char) - DIGIT_OFFSET
    elif 'A' <= char <= 'Z':
        return ord(char) - UPPERCASE_OFFSET
    elif 'a' <= char <= 'z':
        return ord(char) - LOWERCASE_OFFSET
    else:
        raise ValueError("%s is not a valid character" % char)

def true_chr(integer):
    """
    Turns an integer [integer] into digit in base [BASE]
    as a character representation.
    """
    if integer < 10:
        return chr(integer + DIGIT_OFFSET)
    elif 10 <= integer <= 35:
        return chr(integer + UPPERCASE_OFFSET)
    elif 36 <= integer < 62:
        return chr(integer + LOWERCASE_OFFSET)
    else:
        raise ValueError("%d is not a valid integer in the range of base %d" % (integer, BASE))


def decode(key):
    """
    Turn the base [BASE] number [key] into an integer
    """
    int_sum = 0
    reversed_key = key[::-1]
    for idx, char in enumerate(reversed_key):
        int_sum += true_ord(char) * int(math.pow(BASE, idx))
    return int_sum


def encode(integer):
    """
    Turn an integer [integer] into a base [BASE] number
    in string representation
    """

    # we won't step into the while if integer is 0
    # so we just solve for that case here
    if integer == 0:
        return '0'

    string = ""
    while integer > 0:
        remainder = integer % BASE
        string = true_chr(remainder) + string
        integer /= BASE
    return string

def expandAndEncode(x):
    nx = expand(expand(x ^ 0x5bf03635) ^ 0xdeadbeaf)
    return encode(nx)

def expand (x):
    """
    convert a 32 bit sequential number into something thats not obviously sequential
    based on: http://preshing.com/20121224/how-to-generate-a-sequence-of-unique-random-integers/
    is 1:1 so we can call it on itself to further scramble things
    """
    mask32 = 0xffffffff
    prime = 0xfffffffb # 4294967291
    #
    x &= mask32
    if (x >= prime):
        return x    # The 5 integers out of range are mapped to themselves.
    residue = (x * x) % prime
    if (x <= prime/2):
        return residue
    else:
        return (prime - residue) & mask32


if __name__ == '__main___':

    # not really unit tests just a rough check to see if anything is way off
    if sys.argv[1] == '-tests':
        passed_tests = True
        for i in xrange(0, 1000):
            passed_tests &= (i == decode(encode(i)))
        print passed_tests
    else:
        user_input = sys.argv[2]
        try:
            if sys.argv[1] == '-e':
                print encode(user_input)
            elif sys.argv[1] == '-d':
                print decode(int(user_input))
            else:
                print "I don't understand option %s" % sys.argv[1]
        except ValueError as e:
            print e
