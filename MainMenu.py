"""
COMP.CS 100 BlackJack peli ja sen mainmenu
Tekijä: Omar Harb
Opiskelijanumero: 050327474
Sähköposti: omar.harb@tuni.fi

Ohjelmassa pyritty saavuttamaan kehittyneen käyttöliittymän vaatimukset

Pelin säännöt englanniksi:
-The goal of blackjack is to beat the dealer's hand without going over 21.
-Face cards are worth 10. Aces are worth 1 or 11, whichever makes a better
 hand.
-Each player starts with two cards, one of the dealer's cards is hidden
 until the end.
-To 'Hit' is to ask for another card. To 'Stand' is to hold your total and
end your turn.
-If you go over 21 you bust, and the dealer wins regardless of the dealer's
 hand.
-If you are dealt 21 from the start (Ace & 10), you got a blackjack.
-Dealer will hit until his/her cards total 17 or higher.

Käyttöohjeet:

Kun ohjelman suorittaminen aloitetaan se avaa main menu ikkunan, jossa on
2 nappia. Toisesta voi sulkea ikkunan ja lopettaa ohjelman ja toisesta napista
aloitetaan itse peli. Play nappi avaa uuden ikkunan jossa peli toimii.
peli aloitetaan painamalla suurta ikkunassa olevaa kuvaa/nappia, jonka
yläpuolella lukee DEAL. Tämän jälkeen pelaajalle ja dealerille jaetaan
ensimmäiset kortit. Pelaajalla molemmat kortit ovat näkyvissä ja dealerilla
taas näkyy ensimmäinen kortti normaalisti ja toisesta vain takapuoli.
Ohjelmassa on myös toiminto, jossa kortin takapuoli vaihtuu joka pelikerralla.
Myös silloinkin kun ohjelma on käynnissä. Kun pelaajalle ja dealerille on
jaettu kortit pelaajalla on kaksi vaihtoehtoa Hit tai Stand. Painaessa Hit-
vaihtoehtoa pelaaja saa uuden kortin. Hit painiketta voi painaa niin kauan kun
pelaajan pisteet <= 21 mutta aina ei ole kuitenkaan järkevä pyytää uutta
korttia vaan pitää nykyinen käsi. Tämän toiminnon voi suorittaa painamalla
Stand painiketta. Kun pelaaja on painanut stand painiketta, alkaa dealerin
vuoro. Niin kuin säännöissä lukee dealerin on hitattava aina kun hänen
kätensä arvo on <= 16 ja standattava kun se on >16. Jos kumpikaan ei ole
"bustannut" eli käden arvo on ylittänyt 21 niin nähdään dealerin vuoron
jälkeen kumpi on voittanut. Voittaja voidaan myös nähdä erityistilanteissa
aikaisemmin esimerkiksi jos jommalla kummalla on "blackjack" eli korttien
arvo on 21 silloin kun molemmille on jaettu 2 korttia. Kun ohjelma on
ilmoittanut voittajan voi pelaaja painaa "new game" painiketta, joka ilmestyy
ruudulle aloittaaksen uuden pelin.

"""


from tkinter import *

from Game import Blackjack


class Mainmenu:

    # initissä luodaan main menu ikkuna
    def __init__(self):

        self.__mainmenu = Tk()

        imagename1 = "images/Menu.png"

        self.__canvas = Canvas(self.__mainmenu, width=1230, height=762)
        self.__canvas.pack()

        img1 = PhotoImage(file=imagename1)
        self.__canvas.background = img1
        self.__canvas.create_image(0, 0, anchor=NW, image=img1)

        self.__img2 = PhotoImage(file="images/Play.png")
        self.__img3 = PhotoImage(file="images/Quit.png")

        self.__playbutton = Button(
            self.__canvas, justify=LEFT, command=self.play
                                   )
        self.__playbutton.config(image=self.__img2)
        self.__playbutton.place(x=420, y=480)

        self.__quitbutton = Button(
            self.__canvas, command=self.quit, justify=LEFT
                                   )
        self.__quitbutton.config(image=self.__img3)
        self.__quitbutton.place(x=420, y=620)

    def play(self):
        """
        Tuhoaa main menu ikkunan ja avaa peli-ikkunan
        :return:
        """

        self.__mainmenu.destroy()
        Blackjack(Tk()).start()

    def quit(self):
        """
        Tuhoaa main menu ikkunan
        :return:
        """

        self.__mainmenu.destroy()

    def start(self):
        """
        Avaa main menu ikkunan
        :return:
        """

        self.__mainmenu.mainloop()


def main():

    Mainmenu().start()


if __name__ == "__main__":
    main()
