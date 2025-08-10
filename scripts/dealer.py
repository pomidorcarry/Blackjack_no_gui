import time

from .abstract_player import AbstractPlayer
from .deck import DeckClassic52
from .deck import Deck
from .hand import Hand


class Dealer(AbstractPlayer):
    def __init__(self, name="blank", cash=0):
        super().__init__(name, cash)
        self.hand = Hand(is_dealers=True)

    def take_card(self, deck:DeckClassic52, face_down=False) -> None:
        """
        draws card from the deck into deale's single hand\ncalculates points and victory_status

        :param deck: From what deck the card will be drawn from
        :type deck: DeckClassic52
        :param face_down: Wether the card will be drawn face up or down
        :type face_down: bool
        """
        if drawn := deck.draw_from_deck():
            drawn.face_down = face_down
            self.hand.append(drawn)

        self.hand.calculate_points()
        self.hand.set_victory_status()

    def make_move(self, deck: DeckClassic52) -> None:
        """dealer's move"""
        self.moved = True
        print("And now let's see dealer's hand")
        print(f"total points are {self.hand.true_points}")
        time.sleep(1.5)
        self.show_hand(self.hand)
        
        if self.hand.true_points < 17:
            while self.hand.true_points < 17:
                print("dealer takes a card")
                self.take_card(deck)
                self.show_hand(self.hand)
                time.sleep(2)
                print(f"Dealer total points are {self.hand.true_points}")
