"""
COMP.CS 100 Dealer AI
Tekijä: Omar Harb
Opiskelijanumero: 050327474
Sähköposti: omar.harb@tuni.fi

Blackjack pelin dealerin AI, jonka perusteella dealer valitsee hit tai stand
"""


class Dealer:

    def __init__(self, score):

        self.__score = score

    def hit(self):

        if self.__score <= 16:
            return True

        else:
            return False
