import pytest
import unittest.mock as mock
from blackjack.scripts.abstract_player import AbstractPlayer as abs
from blackjack.scripts.deck import Deck_classic_52 as dck

@pytest.fixture
def player():
    abs.__abstractmethods__ = set()
    return abs(name="NAME",cash=333)

# @pytest.mark.parametrize("points,hand,result",[(23,[1,1,1],"BUST"),(21,[1,1],"NaturalBlackJack")])
# def test__set_v_status(player,points,result,hand):
#     player.points = points
#     player.hand = hand
#     player.set_v_status()
#     assert player.v_status == result

# @mock.patch("game_21.scripts.abstract_player.AbstractPlayer.offer_split_hand")
# def test_set_v_status_split_is_called(mocker,player):
#     #changed actual function to mocker
#     player.points = 100
#     player.hand = [1,1]
#     #calling function
#     player.set_v_status()
#     #asserting that mocker was called
#     mocker.assert_called_once()

# @mock.patch("game_21.scripts.deck.Deck_classic_52.draw_from_deck")
# def test_take_card_calls_draw_from_deck(mocker,player):
#     deck = dck()
#     player.take_card(deck)
#     mocker.assert_called_once()

# @mock.patch("game_21.scripts.abstract_player.AbstractPlayer.calculate_points")
# def test_take_card_calls_calculate_points(mocker,player):
#     deck = dck()
#     player.take_card(deck)
#     mocker.assert_called_once()