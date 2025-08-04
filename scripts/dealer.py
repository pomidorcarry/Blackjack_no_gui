import time

from .abstract_player import AbstractPlayer
from .deck import Deck
from .hand import Hand

class Dealer(AbstractPlayer):
    def __init__(self, name = "blank", cash=0):
        super().__init__(name, cash)
        self.hand = Hand(is_dealers=True)
        # self.__hand.is_dealers = True

    def take_card(self,deck,face_down=False):
        if drawn:= deck.draw_from_deck():
            drawn.face_down = face_down
            self.hand.append(drawn)
        self.hand.calculate_points()
        self.hand.set_v_status()

    def make_move(self,deck:Deck) -> None:
        self.moved = True
        print("And now let's see dealer's hand")
        print(f"total points are {self.hand.true_points}")
        time.sleep(3)
        self.show_hand(self.hand)
        if self.hand.true_points < 17:
            while self.hand.true_points < 17:
                print("dealer takes a card")
                self.take_card(deck)
                self.show_hand(self.hand)
                print(f"Dealer total points are {self.hand.true_points}")
                if not self.hand.true_points > 21:
                    time.sleep(3)