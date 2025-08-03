import pytest
import unittest.mock as mock
from blackjack.scripts.abstract_player import AbstractPlayer as abs
from blackjack.scripts.deck import Deck_classic_52 as dck
from blackjack.scripts.card import Card

@pytest.fixture
def player_0():
    abs.__abstractmethods__ = set()
    return abs(name="NAME",cash=333)

@pytest.mark.parametrize("value",[100,1,999.999])
def test_cash_correct(player_0,value):
    player_0.cash = value
    assert player_0.cash == value

@pytest.mark.parametrize("value",[0,-1,None,"string"])
def test_cash_invalid(player_0,value):
    with pytest.raises(ValueError):
        player_0.cash = value


@mock.patch("blackjack.scripts.deck.Deck_classic_52.draw_from_deck")
def test_take_card_calls_draw_from_deck(mocker,player_0:abs):
    mock_card = mock.MagicMock()
    mock_card.cost = 10
    mock_card.name = "Ten of Hearts"
    mock_card.face_down = False
    mocker.return_value = mock_card
    deck = dck()
    player_0.take_card(deck,hand=player_0.hands[0])
    mocker.assert_called_once()

@mock.patch("blackjack.scripts.hand.Hand.append")
def test_take_card_calls_append(mocker,player_0:abs):
    deck = dck()
    player_0.take_card(deck,hand=player_0.hands[0])
    mocker.assert_called_once()

@mock.patch("blackjack.scripts.hand.Hand.calculate_points")
def test_take_card_calls_calculate_points(mocker,player_0:abs):
    deck = dck()
    player_0.take_card(deck,hand=player_0.hands[0])
    mocker.assert_called_once()

def test_take_card_grows_hand(player_0:abs):
    deck = dck()
    before_draw = len(player_0.hands[0])
    player_0.take_card(deck,player_0.hands[0])
    after_draw = len(player_0.hands[0])
    assert type(player_0.hands[0][0]) is Card
    assert before_draw + 1 == after_draw 