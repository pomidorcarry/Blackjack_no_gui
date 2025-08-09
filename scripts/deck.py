from abc import ABC, abstractmethod
import random
from .card import Card


class Deck(ABC):
    @abstractmethod
    def display_all_existing(self):
        pass

    @abstractmethod
    def display_all_in_deck(self):
        pass

    @abstractmethod
    def shuffle_deck(self):
        pass

    @abstractmethod
    def draw_from_deck(self):
        pass


class Deck_classic_52(Deck):
    def __init__(self):
        self.__existing_cards = {}
        self.fill_existing()
        self.__in_deck_cards = list(self.__existing_cards.values())[:]
        self.__in_deck_cards_total_num = len(self.__in_deck_cards)

    @property
    def existing_cards(self):
        return self.__existing_cards

    @property
    def in_deck_cards(self):
        return self.__in_deck_cards

    @in_deck_cards.setter
    def in_deck_cards(self, value):
        if type(value) is list:
            self.__in_deck_cards = value
        else:
            raise ValueError("Only lists for this value")

    @property
    def in_deck_cards_total_num(self):
        return self.__in_deck_cards_total_num

    @in_deck_cards_total_num.setter
    def in_deck_cards_total_num(self, value):
        self.__in_deck_cards_total_num = value

    def __getitem__(self, key):
        return self.__existing_cards[key]

    def fill_existing(self) -> None:
        """adding all numbered cards and face cards to the deck"""
        for suit_i in Card.valid_suits:

            for name, c in Card.valid_ranks_face.items():
                card_obj = Card(suit=suit_i, rank=name, cost=c)
                self.__existing_cards[card_obj.name] = card_obj

            for name, c in Card.valid_ranks_digits.items():
                card_obj = Card(suit=suit_i, rank=name, cost=c)
                self.__existing_cards[card_obj.name] = card_obj

    def display_all_existing(self) -> None:
        if self.__existing_cards:
            for i, card in enumerate(self.__existing_cards.values()):
                print(i, card)
        else:
            print(f"No cards in deck defined")

    def display_all_in_deck(self) -> None:
        if self.__in_deck_cards:
            for i, card in enumerate(self.__in_deck_cards):
                print(i, card)
        else:
            print(f"No cards in deck right now")

    def deck_info(self) -> str:
        """how many cards are left and how many cards are still in"""
        total = self.__in_deck_cards_total_num
        inside = len(self.__in_deck_cards)
        return f"""=============\nOut of the total {total} cards,\n{inside} cards are still in the deck\n============="""

    def shuffle_deck(self) -> None:
        random.shuffle(self.__in_deck_cards)

    def draw_from_deck(self) -> Card:
        if self.__in_deck_cards:
            drawn = self.__in_deck_cards.pop(0)
            return drawn
        else:
            raise ValueError("No cards left to draw!")
