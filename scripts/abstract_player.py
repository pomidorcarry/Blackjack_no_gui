from abc import ABC, abstractmethod
from .deck import DeckClassic52
from .hand import Hand


class AbstractPlayer(ABC):
    def __init__(self, name: str = "blank", cash=0, hands=None):
        super().__init__()
        self.name = name
        self.__cash = cash
        if hands:
            self.hands: list[Hand] = hands
        else:
            self.hands = [Hand()]

    @property
    def cash(self):
        return self.__cash

    @cash.setter
    def cash(self, value):
        if not (type(value) is int or type(value) is float):
            raise ValueError("Please, enter floats and integers for cash")
        elif value <= 0:
            raise ValueError("Cash value should be greater than zero")
        else:
            self.__cash = float(value)

    @abstractmethod
    def make_move(self,deck: DeckClassic52)->None:
        pass

    def take_card(self, deck: DeckClassic52, hand: Hand, face_down=False) -> None:
        """
        draws card from chosen deck and appends to the hand\n
        calculates points for the hand
        """
        if hand.victory_status == "BUST":
            print("Busted, you can't take any more cards")
            return

        elif drawn := deck.draw_from_deck():
            drawn.face_down = face_down
            hand.append(drawn)
        hand.calculate_points()

    def show_hand(self, hand: Hand) -> None:
        """shows hand of the player or dealer and shows or hides hidden cards"""
        if not hand:
            print("Your hand is empty")

        elif hand.is_dealers:
            print("==========")
            print("Dealer's hand\n========")
            for card in hand.in_hand_cards:
                if card.face_down == True:
                    print(f"    🃏This card is face down")
                elif card.face_down == False:
                    print(f"    🃏{card}")
            print("==========\n")
            
        else:
            print(f"{self.name}'s current hand is:\n")
            for card in hand.in_hand_cards:
                print(f"    🃏{card}")
            print("==========\n")

    def show_points(self, hand: Hand) -> None:
        """shows player's and dealer's currrent points"""
        if hand.is_dealers:
            print(f"{self.name}'s current points are {hand.show_points} + X points\n")
        else:
            print(f"{self.name}'s current points are {hand.true_points}\n")
