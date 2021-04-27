"""
COMP.CS 100 Korttipakka
Tekijä: Omar Harb
Opiskelijanumero: 050327474
Sähköposti: omar.harb@tuni.fi

Ohjelma luo ja sekoittaa korttipakan blackjack peliä varten
"""

import random

from Card import Card

korttiarvot = [
 "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"
]

maat = [
 "S", "H", "D", "C"
]


class Deck:

    def __init__(self):

        # luodaan korttipakka Card luokan avulla
        self.__kortit = [
            str(Card(maa, arvo)) for arvo in korttiarvot for maa in maat
                         ]
        random.shuffle(self.__kortit)

    def return_list(self):

        return self.__kortit
