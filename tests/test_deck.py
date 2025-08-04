import pytest
import unittest.mock as mock

from blackjack.scripts.deck import Deck_classic_52
from blackjack.scripts.abstract_player import AbstractPlayer as abs
from blackjack.scripts.card import Card


@pytest.fixture
def my_deck():
    Deck_classic_52().__abstractmethods__ = set()
    return Deck_classic_52()


def test_correct_init(my_deck):
    assert type(my_deck.existing_cards) is dict
    assert type(my_deck.in_deck_cards) is list
    assert len(my_deck.in_deck_cards) == 52
    assert my_deck.in_deck_cards_total_num == 52


def test_no_duplicates_in_deck_cards(my_deck):
    visited = []
    for card in my_deck.in_deck_cards:
        assert card not in visited
        visited.append(card)


def test_instance_of_card(my_deck):
    for card in my_deck.in_deck_cards:
        assert type(card) == Card


# list has a different card order,same length and cards
def test_shuffle(my_deck):
    before = my_deck.in_deck_cards[:]
    my_deck.shuffle_deck()
    after = my_deck.in_deck_cards[:]
    assert len(before) == len(after)
    assert before != after


# deck decreased by one after drawing
def test_drawing_deck_decrease(my_deck):
    before = len(my_deck.in_deck_cards)
    my_deck.draw_from_deck()
    after = len(my_deck.in_deck_cards)
    assert before == after + 1


# card isn't in the deck after drawing
def test_drawing_card_gone(my_deck):
    card = my_deck.in_deck_cards[0]
    assert card in my_deck.in_deck_cards
    my_deck.draw_from_deck()
    assert card not in my_deck.in_deck_cards


def test_drawing_returns_a_card(my_deck):
    assert type(my_deck.draw_from_deck()) is Card


def test_drawing_no_cards_left_error(my_deck):
    my_deck.in_deck_cards = []
    with pytest.raises(ValueError):
        my_deck.draw_from_deck()
