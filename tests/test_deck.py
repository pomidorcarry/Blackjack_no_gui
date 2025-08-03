import pytest
import unittest.mock as mock

from blackjack.scripts.deck import Deck_classic_52
from blackjack.scripts.abstract_player import AbstractPlayer as abs
from blackjack.scripts.card import Card

@pytest.fixture
def my_deck():
    Deck_classic_52().__abstractmethods__ = set()
    return Deck_classic_52()

def test_correct_initialize(my_deck):
    assert type(my_deck.existing_cards) == dict
    assert type(my_deck.in_deck_cards) == list
    assert len(my_deck.in_deck_cards) == 52 
    assert my_deck.in_deck_cards_total_num == 52

def test_no_duplicates(my_deck):
    pass

def test_instance_of_card(my_deck):
    for card in my_deck.in_deck_cards:
        assert type(card) == Card

#list has a different card order,same length and cards
def test_shuffle(my_deck):
    pass

#deck decreased by one after drawing
def test_drawing_deck_decrease(my_deck):
    pass


#card isn't in the deck after drawing
def test_drawing_card_gone(my_deck):
    pass

def test_drawing_returns_a_card(my_deck):
    pass

def test_drawing_no_cards_left(my_deck):
    pass

#multiple
#prints correct string when no left
#reflects that card was drawn or deck shuffled
def test_display_all(my_deck):
    pass

