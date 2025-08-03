import pytest
import unittest.mock as mock

from blackjack.scripts.hand import Hand
from blackjack.scripts.card import Card
from blackjack.scripts.deck import Deck_classic_52


@pytest.fixture
def my_hand():
    hand = Hand()
    return hand

@pytest.fixture
def hand_with_cards_0():
    hand = Hand()
    hand.in_hand_cards = [Card(suit="Spades",rank="Queen",cost=10)]
    return hand

@pytest.fixture
def hand_with_cards_0():
    hand = Hand()
    hand.in_hand_cards = []
    return hand

@pytest.mark.parametrize("is_dealers",[(False,),(True,)])
def test_init_correct(is_dealers):
    hand_ = Hand(is_dealers)
    assert hand_.is_dealers == is_dealers
    assert hand_.in_hand_cards == []
    assert hand_.moved == False

###properties

@pytest.mark.parametrize("error",[("ERROR"),(0),(None)])
def test_in_hand_cards_invalid(my_hand:Hand,error):
    with pytest.raises(ValueError):
        my_hand.in_hand_cards = error

@pytest.mark.parametrize("value",[(10),(1000.9556),(1.0)])
def test_bet_correct(my_hand:Hand,value):
    my_hand.bet = value
    assert my_hand.bet == value

@pytest.mark.parametrize("error",[("ERROR"),({}),(None),(-1),(0)])
def test_bet_invalid(my_hand:Hand,error):
    with pytest.raises(ValueError):
        my_hand.bet = error

@pytest.mark.parametrize("error",[("ERROR"),({}),(None),(-1),(0)])
def test_coefficient_invalid(my_hand:Hand,error):
    with pytest.raises(ValueError):
        my_hand.coefficient = error

@pytest.mark.parametrize("error",[("ERROR"),({}),(None),([]),(Deck_classic_52)])
def test_points_invalid(my_hand:Hand,error):
    with pytest.raises(ValueError):
        my_hand.coefficient = error

@pytest.mark.parametrize("hand_",[(my_hand),(hand_with_cards_0)])
def test_calculate_points_correct_type(hand_:Hand,request):
    assert type(request.getfixturevalue(my_hand).calculate_points()) == int