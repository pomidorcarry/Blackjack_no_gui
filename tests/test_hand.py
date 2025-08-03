import pytest
import unittest.mock as mock

from blackjack.scripts.hand import Hand
from blackjack.scripts.card import Card
from blackjack.scripts.deck import Deck_classic_52


###fixtures
@pytest.fixture
def empty_hand():
    hand = Hand()
    return hand

@pytest.fixture
def hand_with_cards_0():
    hand = Hand()
    hand.in_hand_cards = [Card(suit="Spades",rank="Queen",cost=10)]
    return hand

@pytest.fixture
def hand_with_cards_1():
    hand = Hand()
    hand.in_hand_cards = [Card(suit="Spades",rank="Five",cost=5)]
    points = 5
    return hand

#hands with cards using parameters in a fixture
@pytest.fixture(params=[(Hand(in_hand_cards=[Card(suit="Spades",rank="Queen",cost=10)]),10)])
def hands_with_cards(request):
    return request.param
###fixtures


@pytest.mark.parametrize("is_dealers",[(False,),(True,)])
def test_init_correct(is_dealers):
    hand_ = Hand(is_dealers)
    assert hand_.is_dealers == is_dealers
    assert hand_.in_hand_cards == []
    assert hand_.moved == False

###properties

@pytest.mark.parametrize("error",[("ERROR"),(0),(None)])
def test_in_hand_cards_invalid(empty_hand:Hand,error):
    with pytest.raises(ValueError):
        empty_hand.in_hand_cards = error

@pytest.mark.parametrize("value",[(10),(1000.9556),(1.0)])
def test_bet_correct(empty_hand:Hand,value):
    empty_hand.bet = value
    assert empty_hand.bet == value

@pytest.mark.parametrize("error",[("ERROR"),({}),(None),(-1),(0)])
def test_bet_invalid(empty_hand:Hand,error):
    with pytest.raises(ValueError):
        empty_hand.bet = error

@pytest.mark.parametrize("error",[("ERROR"),({}),(None),(-1),(0)])
def test_coefficient_invalid(empty_hand:Hand,error):
    with pytest.raises(ValueError):
        empty_hand.coefficient = error

@pytest.mark.parametrize("error",[("ERROR"),({}),(None),([]),(Deck_classic_52)])
def test_points_invalid(empty_hand:Hand,error):
    with pytest.raises(ValueError):
        empty_hand.coefficient = error


@pytest.mark.parametrize("fixture_hand",[("hand_with_cards_0"),("hand_with_cards_1")])
def test_calculate_points_correct_type(fixture_hand,request):
    hand = request.getfixturevalue(fixture_hand)
    assert isinstance(hand,Hand)