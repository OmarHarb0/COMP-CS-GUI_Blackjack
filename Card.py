"""
COMP.CS 100 Kortit
Tekijä: Omar Harb
Opiskelijanumero: 050327474
Sähköposti: omar.harb@tuni.fi

Luokka korttien käsittelyn selkeyttämiseksi

"""


class Card:

    def __init__(self, maa, arvo):

        self.__maa = maa
        self.__arvo = arvo

    def __str__(self):

        return self.__arvo + self.__maa

    def maa(self):

        return self.__maa

    def arvo(self):

        return self.__arvo
