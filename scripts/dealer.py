from .abstract_player import AbstractPlayer
from .deck import Deck
from .hand import Hand

class Dealer(AbstractPlayer):
    def __init__(self, name = "blank", cash=0):
        super().__init__(name, cash)
        self.__hand = Hand()
        self.__hand.is_dealers = True

    @property
    def true_points(self):
        return self.__true_points
    
    @true_points.setter
    def true_points(self,true_points:int):
        self.__true_points = true_points

    def take_card(self, deck, face_down=False):
        super().take_card(deck, face_down)
        self.true_points = self.calculate_true_points(self.hand)
        self.set_v_status()

    def calculate_true_points(self,hand):
        points = 0
        for card in hand:
            points += card.cost
        return points

    def make_move(self,deck:Deck) -> None:
        self.moved = True
        print("And now let's see dealer's hand")
        print(f"total points are {self.true_points}")
        self.show_true_hand()
        if self.true_points < 17:
            while self.true_points < 17:
                print("dealer takes a card")
                self.take_card(deck)
                self.show_true_hand()
                print(f"Dealer total points are {self.true_points}")
  
    def show_true_hand(self):
        print("Dealer's hand\n========")
        for card in self.hand:
            print(f"    🃏{card}")
        print("==========")

    def set_v_status(self):
        if self.true_points > 21:
            for card in self.hand:
                if card.cost == 11:
                    print("Soft hand spotted!")
                    card.cost = 1
                    print(f"{card.name} now costs 1 point")
                    break
            else:
                self.v_status = "BUST"
        elif self.true_points == 21 and len(self.hand) == 2:
            self.v_status = "NaturalBlackJack"
        else:
            self.v_status = self.true_points