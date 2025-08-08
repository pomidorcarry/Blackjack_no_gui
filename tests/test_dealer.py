import pytest

from blackjack.scripts.dealer import Dealer
from blackjack.scripts.deck import Deck_classic_52 as dck
from blackjack.scripts.hand import Hand
from blackjack.scripts.card import Card
from blackjack.tests.test_hand import (
    hand_with_cards_0,
    hand_with_cards_1,
    hand_with_cards_2,
    hand_with_cards_3,
    hand_with_cards_4,
    hand_with_cards_5,
    hand_with_cards_6,
)


@pytest.fixture
def dealer_():
    return Dealer()

def test_empty_dealer(dealer_: Dealer):
    assert dealer_.name == "blank"
    assert dealer_.cash == 0


def test_take_card_grows_hand(dealer_: Dealer):
    deck = dck()
    before_draw = len(dealer_.hand)
    dealer_.take_card(deck)
    after_draw = len(dealer_.hand)
    assert type(dealer_.hand[0]) is Card
    assert before_draw + 1 == after_draw