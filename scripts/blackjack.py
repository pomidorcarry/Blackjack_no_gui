from .deck import Deck_classic_52
from .player import Player
from .dealer import Dealer
from .hand import Hand

import sys

class BlackJack:
    def __init__(self,players:list[Player],deck:Deck_classic_52,dealer:Dealer):
        self.__players = players
        self.__deck = deck
        self.__dealer = dealer

    @property
    def players(self):
        return self.__players

    @players.setter
    def players(self,players):
        for player in players:
            if not type(player) == Player:
                raise ValueError("Only player objects in players list")
        else:
            self.__players = players

    @property
    def deck(self):
        return self.__deck

    @deck.setter
    def deck(self,deck):
        if not type(deck) == Deck_classic_52:
            raise ValueError("Only deck objects")
        else:
            self.__deck = deck
        
    @property
    def dealer(self):
        return self.__dealer

    @dealer.setter
    def dealer(self,dealer):
        if not type(dealer) == Dealer:
            raise ValueError("Only dealer objects")
        else:
            self.__dealer = dealer

    def place_bets(self)->None:
        '''
        each player in players places his bet\n
        player only has one hand at this point!
        '''
        for player in self.players:
            player.place_bet(hand=player.hands[0])

    def show_bets(self)->None:
        '''
        shows players bets
        '''
        print("---")
        for player in self.players:
            print(f"{player.name}'s bet is {player.bet} $")
        print("---")

    def initial_deal(self)->None:
        '''
        initially dealing cards to all players and the dealer\n
        face up/down\n
        right now only one hand is possible with 0 cards
        '''
        for player in self.players:
            for _ in range(2):
                player.take_card(self.deck,hand=player.hands[0],face_down=False)
        self.dealer.take_card(self.deck,face_down=True)
        self.dealer.take_card(self.deck,face_down=False)

    def check_naturals(self)->None:
        '''
        only one hand is possible right now\n
        checking if anyone won after the initial deal
        '''
        for player in self.players:
            if self.dealer.hands[0].v_status != "NaturalBlackJack" and player.hands[0].v_status == "NaturalBlackJack":
                player.hands[0].coefficient = 1.5
            elif self.dealer.hands[0].v_status == "NaturalBlackJack" and player.hands[0].v_status == "NaturalBlackJack":
                player.hands[0].coefficient = 0
            elif player.hands[0].v_status != "NaturalBlackJack":
                insurance = self.insurance(player)
                if insurance and self.dealer.hands[0].v_status == "NaturalBlackJack":
                    player.hands[0].coefficient = 0
                elif insurance and self.dealer.hands[0].v_status != "NaturalBlackJack":
                    player.cash -= insurance
                    print(f"player {player.name} has lost their insurance {insurance}$!")
                elif self.dealer.v_status == "NaturalBlackJack":
                    player.hands[0].coefficient = -1

    def show_hands(self)->None:
        for player in self.players:
            player.show_hand()
            player.show_points()

    #displaing players current cash
    def show_cash(self)->None:
        for player in self.players:
            print(f"{player.name} has {player.cash} $ on their balance")

    #ask wether the player would like to try another round?
    #or break the cycle and close the program
    def reset(self)->bool:
        try:
            answer = input("The game is over, would you like to try one more time?\ny or n?")
        except KeyboardInterrupt:
            print("Understood!Bye!")
            sys.exit()
        if answer.lower() == "y":
            for player in self.players:
                player.bet = None
                player.coefficient = None
                player.moved = False
                player.v_status = None
                player.points = None
                player.hand = []
            self.dealer.v_status = None
            self.dealer.points = None
            self.dealer.true_points = None
            self.dealer.hand = []
            return True
    
    
    #check if anyone won
    def check_v_status(self):
        #check if dealer busted, after both players've and dealer made their moves
        if self.dealer.v_status == "BUST":
            for player in self.players:
                player.coefficient = 1.0
            return
        elif self.dealer.v_status != "NaturalBlackJack":
            for player in self.players:
                if player.v_status > 21:
                    player.v_status = "BUST"
                    player.coefficient = -1.0
                if player.v_status > self.dealer.v_status:
                    player.coefficient = 1.0
                else:
                    player.coefficient = -1.0
    
    def insurance(self,player:Player)->int:
        if self.seek_and_offer_insurance():
            return player.bet/2
        return 0

    def seek_and_offer_insurance(self)->bool:
        for card in self.dealer.hand:
            if card.face_down == False and card.cost == 11:
                self.dealer.show_hand()
                if input("Looks like the dealer may have a natural blackjack\nwould you like to place half of your bet that he got a natural blackjack\n(y or n?)\n").lower() == "y":
                    return True
        else:
            return False

    #set prizes and print who won and how much
    def deal_with_winners(self):
        if self.dealer.v_status == "NaturalBlackJack":
            print(f"Ooops the dealer got {self.dealer.v_status}")
        for player in self.players:
            prize = player.calculate_prize()
            if player.coefficient>0:
                print(f"{player.name} got {player.v_status}\n He won {prize}!💸💸💸")
            else:
                print(f"Because {player.name} got {player.v_status}\n He lost {prize}!😭😭😭")
            print(f"{player.name} now got {player.cash}")
