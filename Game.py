"""
COMP.CS 100 Blackjack peli
Tekijä: Omar Harb
Opiskelijanumero: 050327474
Sähköposti: omar.harb@tuni.fi

Tästä tiedostosta löytyy itse peli ja siinä esiintyvät

"""

from tkinter import *

import random

from Deck import Deck

from DealerAI import Dealer


class Blackjack:

    # initissä luodaan kaikki ikkunat ja alueet napeille ja kuville

    def __init__(self, master):

        self.__mainwindow = master

        self.__mainwindow.geometry("1500x900")

        self.__playerframe = Frame(self.__mainwindow, background="#66FF66")
        self.__playerframe.pack(side=BOTTOM, fill=BOTH)

        self.__dealerframe = Frame(self.__mainwindow, background="#66FF66")
        self.__dealerframe.pack(side=TOP, fill=X)

        self.__scoreboard = Frame(self.__mainwindow, background="#9999FF")
        self.__scoreboard.pack(side=LEFT, fill=Y)

        self.__splitcards = Frame(
            self.__mainwindow, background="#66FF66"
                                  )

        self.__buttonframe = Frame(self.__playerframe, background="#9999FF")
        self.__buttonframe.pack(side=LEFT, fill=Y)

        self.__pcardframe = Frame(self.__playerframe, bg="#66FF66")
        self.__pcardframe.pack(side=RIGHT, fill=BOTH)

        self.__pcard1 = Label(
            self.__pcardframe, bg="#66FF66"
                                )
        self.__pcard1.pack(side=RIGHT)

        self.__pcard2 = Label(
            self.__pcardframe, bg="#66FF66"
                                )
        self.__pcard2.pack(side=RIGHT)

        self.__dcardframe = Frame(self.__dealerframe, bg="#66FF66")
        self.__dcardframe.pack(side=RIGHT, fill=BOTH)

        self.__dcard1 = Label(
            self.__dcardframe, bg="#66FF66")
        self.__dcard1.pack(side=RIGHT)

        self.__dcard2 = Label(
            self.__dcardframe, bg="#66FF66")
        self.__dcard2.pack(side=RIGHT)

        self.__pscorevalue = IntVar()

        self.__playerscore = Label(
            self.__scoreboard, text=f"Player score: ", background="#9999FF",
            font=("Comic Sans", 20)
                                    )

        self.__dscorevalue = IntVar()

        self.__dealerscore = Label(
            self.__scoreboard, text=f"Dealer score: ", background="#9999FF",
            font=("Comic Sans", 20)
                                    )

        self.__bustedimage = PhotoImage(file="images/Busted.png")
        self.__hitimage = PhotoImage(file="images/Hit.png")
        self.__standimage = PhotoImage(file="images/Stand.png")
        self.__dealimage = PhotoImage(file="images/Deal.png")
        self.__exitimage = PhotoImage(file="images/Exit.png")
        self.__newgameimg = PhotoImage(file="images/NewGame.png")
        self.__victoryimage = PhotoImage(file="images/Victory.png")
        self.__defeatimage = PhotoImage(file="images/Defeat.png")
        self.__pushimage = PhotoImage(file="images/Push.png")
        self.__cardbackcolor = None
        self.__dcard2image = None

        self.__hit = Button(
            self.__buttonframe, image=self.__hitimage, bg="LightCyan3",
            command=self.hit
                                )

        self.__stand = Button(
            self.__buttonframe, image=self.__standimage, bg="LightCyan3",
            command=self.stand
                                )

        self.__deal = Button(
            self.__mainwindow, image=self.__dealimage, bg="LightCyan3",
            text="DEAL", font=("Comic Sans", 35), compound=BOTTOM,
            command=self.startgame
                                )
        self.__deal.pack(side=TOP)

        self.__quit = Button(
            self.__buttonframe, image=self.__exitimage, command=self.quit
                                )

        self.__playerbusted = Label(
            self.__pcardframe, image=self.__bustedimage, background="#66FF66"
                                        )

        self.__dealerbusted = Label(
            self.__dcardframe, image=self.__bustedimage, background="#66FF66"
                                        )

        self.__newgamebutton = Button(
            self.__mainwindow, image=self.__newgameimg, command=self.newgame
                                        )
        self.__newgamebutton.config(anchor=CENTER)

        self.__resultlabel = Label(self.__mainwindow, font=("Comic Sans", 30))
        self.__resultlabel.config(anchor=CENTER)

        self.__deck = Deck().return_list()
        self.__cardbacks = ["purple", "green", "red", "yellow", "gray", "blue"]
        self.__cardimages = {}
        self.__playercards = []
        self.__dealercards = []
        self.__dcardlabels = []
        self.__pcardlabels = []

    def startgame(self):
        """
        Aloittaa pelin ja jakaa molemmille pelaajille 2 korttia.
        :return:
        """
        # lataa ohjemaan korttien kuvat myöhempää käyttöä varten
        self.load_card_images()

        # vaihtaa joka pelikerralle kortin takapuolta
        self.shuffle_cardback()

        self.__dealerscore.pack(side=TOP)
        self.__playerscore.pack(side=BOTTOM)
        self.__stand.pack(side=TOP, fill=BOTH)
        self.__hit.pack(side=TOP, fill=BOTH)
        self.__quit.pack(side=TOP, fill=BOTH)

        # tuhoaa suuren pelinaloitusnapin
        self.__deal.destroy()

        # ottaa satunnaisen kortin sekoitetusta pakasta, jotta varmistutaan
        # siitä että kortit eivät tule järjestyksessä.
        pcard1 = self.__deck.pop(random.randrange(len(self.__deck)))
        pcard2 = self.__deck.pop(random.randrange(len(self.__deck)))

        # lisää kortit listaan joka sisältää pelaajan kortit
        self.__playercards.append(pcard1)
        self.__playercards.append(pcard2)

        # korteista lisätään myös kuvat ruudulle
        self.__pcard1.config(image=self.__cardimages[pcard1])
        self.__pcard2.config(image=self.__cardimages[pcard2])

        dcard1 = self.__deck.pop(random.randrange(len(self.__deck)))
        dcard2 = self.__deck.pop(random.randrange(len(self.__deck)))

        self.__dealercards.append(dcard1)

        # dealerin score lasketaan ennemmin toisen kortin lisäämistä pakkaan,
        # jotta toisen kortin arvoa ei nähdä ennemmin kun pelaaja on standannyt
        # tai jos jommalla kummalla pelaajalla on blackjack
        self.calculate_dealer_score()
        self.__dealercards.append(dcard2)

        self.__dcard1.config(image=self.__cardimages[dcard1])
        self.__dcard2.config(image=self.__cardbackcolor)

        self.__dcard2image = self.__cardimages[dcard2]

        # päivittää pelaajien pisteet
        self.calculate_player_score()
        self.update_scoreboard()
        self.calculate_dealer_score()

        # jos jommalla kummalla pelaajalla on blackjack ohjelma tarkistaa
        # voittajan heti. Muuten peli jatkuu normaalisti
        if self.check_if_dealer_blackjack():
            self.stand()

        if self.check_if_player_blackjack():
            self.stand()

    def check_if_player_blackjack(self):
        """
        Tarkistaa onko pelaajalla blackjack
        :return: True, jos on blackjack
                 False, jos ei ole blackjack
        """

        if self.__pscorevalue.get() == 21 and len(self.__playercards) == 2:
            return True

        else:
            return False

    def check_if_dealer_blackjack(self):
        """
        Tarkistaa onko dealerilla blackjack
        :return: True, jos on blackjack
                 False, jos ei ole blackjack
        """

        if self.__dscorevalue.get() == 21 and len(self.__dealercards) == 2:
            return True

        else:
            return False

    def shuffle_cardback(self):
        """
        Valitsee satunnaisen kortin takapuolen listasta
        :return:
        """

        color = random.randrange(len(self.__cardbacks))
        filename = "cards/{}_back.png".format(self.__cardbacks[color])
        self.__cardbackcolor = PhotoImage(file=filename)

    def calculate_player_score(self):
        """
        Laskee pelaajan pisteet
        :return:
        """

        # koska vain yhdestä ässästä voi saada 11 pistettä käytetään ace = True
        # tällöin kun ensimmäisestä ässästä on annettu 11 pistettä niin
        # acen arvoksi annetaan False ja muista seuraavista ässistä tulee 1
        # piste.

        ace = True
        score = 0

        for value in self.__playercards:

            # Kaikkien kuvakorttien arvo on 10 pistettä

            if value[0] == "J" or value[0] == "K" or value[0] == "Q":
                points = 10
                score += points

            # Jos kortti on ässä ensimmäisestä saa 11 pistettä ja muista 1
            # pisteen.

            elif value[0] == "A":

                if ace:
                    points = 11
                    score += points
                    ace = False

                else:
                    points = 1
                    score += points

            else:

                # Kokeillaan muuttaa arvon toista merkkiä kokonaisluvuksi
                # jolloin nähdään onko kyseessä kymmenen vai yksinumeroinen
                # luku. Muuten kortin ensimmäisen merkin arvo pisteisiin.
                # Kortit ovat listassa siis muodossa ArvoMaa.

                try:
                    int(value[1])
                    points = 10
                    score += points

                except ValueError:
                    score += int(value[0])

        self.__pscorevalue.set(score)

        # Koska voi tulla sellainen tilanne että ässälle on annettu arvo 11
        # ja pelaaja saa lisää kortteja niin että hän bustaisi eli pisteet
        # ovat yli 21 niin tällaisessa tilanteessa pistelaskuri muuttaa
        # tämän yhden ässän arvoksi 1 blackjackin sääntöjen mukaisesti.
        # Jos pelaajalla ei ole ässiä mitään ei tapahdu. Ensimmäisen ässän
        # arvo on siis 1 tai 11 riippuen tilanteesta.

        ace = True

        if self.__pscorevalue.get() > 21:

            for value in self.__playercards:

                if value[0] == "A" and ace:
                    self.__pscorevalue.set(self.__pscorevalue.get() - 10)
                    ace = False

                else:
                    pass

        else:
            pass

    def calculate_dealer_score(self):
        """
        Laskee dealerin pisteet samalla tavalla kuin pelaajan pisteet
        eli kaikki asiat calculate_player_score metodissa
        :return:
        """

        ace = True
        score = 0

        for value in self.__dealercards:

            if value[0] == "J" or value[0] == "K" or value[0] == "Q":
                points = 10
                score += points

            elif value[0] == "A":
                if ace:
                    points = 11
                    score += points
                    ace = False

                else:
                    points = 1
                    score += points

            else:

                try:
                    int(value[1])
                    points = 10
                    score += points

                except ValueError:
                    score += int(value[0])

        self.__dscorevalue.set(score)
        ace = True

        if self.__dscorevalue.get() > 21:

            for value in self.__dealercards:

                if value[0] == "A" and ace:
                    self.__dscorevalue.set(self.__dscorevalue.get()-10)
                    ace = False

                else:
                    pass

        else:
            pass

    def check_player_bust(self):
        """
        Tarkistaa onko pelaajan pisteet yli 21
        :return: True, jos pisteet yli 21
                 False, jos pisteet <= 21
        """

        if self.__pscorevalue.get() > 21:
            self.__playerbusted.pack(side=RIGHT)
            return True

        else:
            return False

    def check_dealer_bust(self):
        """
        Tarkistaa onko dealerin pisteet yli 21
        :return: True, jos pisteet yli 21
                 False, jos pisteet <= 21
        """

        if self.__dscorevalue.get() > 21:
            self.__dealerbusted.pack(side=RIGHT)
            return True

        else:
            return False

    def update_scoreboard(self):
        """
        Päivittää pistetaulukon
        :return:
        """
        self.__dealerscore.configure(
            text=f"Dealer score: {self.__dscorevalue.get()}"
        )

        self.__playerscore.configure(
            text=f"Player score: {self.__pscorevalue.get()}"
        )

    def update_player_score_if_hit(self):
        """
        Päivittää pistetaulukkoon vain pelaajan pisteet
        :return:
        """

        self.__playerscore.configure(
            text=f"Player score: {self.__pscorevalue.get()}"
        )

    def update_dealer_score_if_hit(self):
        """
        Päivittää pistetaulukkoon vain dealerin pisteet
        :return:
        """

        self.__dealerscore.configure(
            text=f"Dealer score: {self.__dscorevalue.get()}"
        )

    def stand(self):
        """
        Pelaajan painaessa stand nappia poistetaan hit ja stand napit
        käytöstä ja aloitetetaan dealerin vuoro ja dealerin vuoron jälkeen
        katsotaan kumpi voitti.
        :return:
        """

        # poistaa hit ja stand napit käytöstä

        self.__hit["state"] = DISABLED
        self.__stand["state"] = DISABLED

        # laittaa dealerin toisen kortin näkyville

        self.__dcard2.config(image=self.__dcard2image)
        self.update_scoreboard()

        # jos pelaajalla on blackjack mennään suoraan voittajan tarkistamiseen
        # muuten siirrytään dealerin vuoroon

        if not self.check_if_player_blackjack():

            # loopin ehtona käytetään Dealer luokkaa, jonka perusteella
            # dealer ottaa uuden kortin tai pitää nykyisen kätensä

            while Dealer(self.__dscorevalue.get()).hit():

                new_card = self.__deck.pop(random.randrange(len(self.__deck)))
                self.__dealercards.append(new_card)

                # luodaan uusi label johon laitetaan kuva dealerin saamasta
                # kortista ja label lisätään listaan myöhempää käyttöä varten

                label = Label(
                    self.__dcardframe, image=self.__cardimages[new_card],
                    bg="#66FF66"
                )
                label.pack(side=RIGHT)

                self.__dcardlabels.append(label)
                self.calculate_dealer_score()
                self.update_dealer_score_if_hit()
                self.check_dealer_bust()

        self.checkwinner()

    def hit(self):
        """
        Pelaajan painaessa nappia lisätään ruudulle uusi kortti ja tarkistetaan
        pelaajan pisteet ja tarvittaessa voittaja.
        :return:
        """

        # sama prosessi kuin stand metodissa
        new_card = self.__deck.pop(random.randrange(len(self.__deck)))

        self.__playercards.append(new_card)

        label = Label(self.__pcardframe, image=self.__cardimages[new_card],
                      bg="#66FF66")
        label.pack(side=RIGHT)

        self.__pcardlabels.append(label)

        self.calculate_player_score()

        self.update_player_score_if_hit()

        if self.check_player_bust():
            self.checkwinner()

    def load_card_images(self):
        """
        Lataa ohjelmaan kuvat korteista ja lisää ne luokassa olevaan listaan
        jotta niitä voidaan käyttää.
        :return:
        """

        for card in self.__deck:
            filename = "cards/{}.png".format(card)
            image = PhotoImage(file=filename)
            self.__cardimages[str(card)] = image

    def checkwinner(self):
        """
        Tarkistaa kumpi voittaa pelin ja lisää ruudulle voitto/häviökuvan ja
        napin, joka aloittaa uuden pelin
        :return:
        """
        # jokainen ehto johtaa siihen että näytölle ilmestyy voitto tai häviö
        # kuva, hit ja stand napit poistuvat käytöstä ja näytölle tulee
        # new game nappi, josta nimensä mukaan saa aloitettua uuden pelin

        if self.check_player_bust() and self.check_dealer_bust():
            self.__resultlabel.config(
                text="DEALER WINS!", image=self.__defeatimage, compound=BOTTOM
            )
            self.__resultlabel.pack(side=LEFT)
            self.__newgamebutton.pack(side=RIGHT)
            self.__stand["state"] = DISABLED
            self.__hit["state"] = DISABLED

        if self.check_player_bust() and not self.check_dealer_bust():
            self.__resultlabel.config(
                text="DEALER WINS!", image=self.__defeatimage, compound=BOTTOM
            )
            self.__resultlabel.pack(side=LEFT)
            self.__newgamebutton.pack(side=RIGHT)
            self.__stand["state"] = DISABLED
            self.__hit["state"] = DISABLED

        if not self.check_player_bust() and self.check_dealer_bust():
            self.__resultlabel.config(image=self.__victoryimage)
            self.__resultlabel.pack(side=LEFT)
            self.__newgamebutton.pack(side=RIGHT)
            self.__stand["state"] = DISABLED
            self.__hit["state"] = DISABLED

        if self.check_if_dealer_blackjack() and not\
           self.check_if_player_blackjack():

            self.__resultlabel.config(
                text="DEALER WINS!", image=self.__defeatimage, compound=BOTTOM
            )
            self.__resultlabel.pack(side=LEFT)
            self.__newgamebutton.pack(side=RIGHT)
            self.__stand["state"] = DISABLED
            self.__hit["state"] = DISABLED

        if self.check_if_dealer_blackjack() and\
           self.check_if_player_blackjack():

            self.__resultlabel.config(
                text="PUSH", image=self.__pushimage, compound=BOTTOM
                                        )
            self.__resultlabel.pack(side=LEFT)
            self.__newgamebutton.pack(side=RIGHT)
            self.__stand["state"] = DISABLED
            self.__hit["state"] = DISABLED

        if not self.check_dealer_bust() and not self.check_player_bust():

            if self.__stand["state"] == DISABLED:

                if self.__pscorevalue.get() < self.__dscorevalue.get():
                    self.__resultlabel.config(
                        text="DEALER WINS", image=self.__defeatimage,
                        compound=BOTTOM
                                                )
                    self.__resultlabel.pack(side=LEFT)
                    self.__hit["state"] = DISABLED
                    self.__newgamebutton.pack(side=RIGHT)

                elif self.__pscorevalue.get() > self.__dscorevalue.get():
                    self.__resultlabel.config(image=self.__victoryimage)
                    self.__resultlabel.pack(side=LEFT)
                    self.__newgamebutton.pack(side=RIGHT)
                    self.__hit["state"] = DISABLED

                else:
                    self.__resultlabel.config(
                        text="PUSH", image=self.__pushimage, compound=BOTTOM
                                                )
                    self.__resultlabel.pack(side=LEFT)
                    self.__newgamebutton.pack(side=RIGHT)
                    self.__hit["state"] = DISABLED

        else:
            pass

    def reset_values(self):
        """
        Metodi nimensä mukaan resetoi kaikki muuttuneet arvot alkutilaansa ja
        poistaa muutamia kuvia näkyvistä.
        :return:
        """

        self.__dscorevalue.set(0)
        self.__pscorevalue.set(0)

        self.__deck += self.__playercards + self.__dealercards

        self.__hit["state"] = NORMAL
        self.__stand["state"] = NORMAL

        self.update_scoreboard()

        self.__playerbusted.forget()
        self.__dealerbusted.forget()
        self.__resultlabel.forget()
        self.__newgamebutton.forget()

        self.__playercards = []
        self.__dealercards = []
        self.__pcardlabels = []
        self.__dcardlabels = []

    def newgame(self):
        """
        Tuhoaa kaikkien korttien labelit, resetoi muuttuneet arvot ja aloittaa
        uuden pelin
        :return:
        """

        for label in self.__pcardlabels:
            label.destroy()

        for label in self.__dcardlabels:
            label.destroy()

        self.reset_values()
        self.startgame()

    def quit(self):
        """
        Sulkee ikkunan ja lopettaa ohjelman
        :return:
        """

        self.__mainwindow.destroy()

    def start(self):
        """
        Avaa peli-ikkunan
        :return:
        """

        self.__mainwindow.mainloop()
