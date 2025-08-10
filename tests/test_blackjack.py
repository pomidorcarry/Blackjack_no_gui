from blackjack.scripts.player import Player
from blackjack.scripts.blackjack import BlackJack
from blackjack.scripts.deck import DeckClassic52 as dck
from blackjack.scripts.dealer import Dealer
from blackjack.scripts.hand import Hand
from blackjack.scripts.card import Card

import pytest


@pytest.mark.parametrize(
    "value", [("normalname"), ("normalname"), ("   zak   "), ("pomidor_carry")]
)
def test_validate_name_correct(value):
    res = BlackJack.validate_name(value)
    assert res == value


@pytest.mark.parametrize("value", [("100"), ("Zakhar!"), ("1Zakhar"), ("10000$")])
def test_validate_name_error(value):
    res = BlackJack.validate_name(value)
    assert res == None


@pytest.mark.parametrize(
    "p_status,d_status",
    [(15, 15), (15, "NaturalBlackJack"), (2, "NaturalBlackJack"), (2, 21)],
)
def test_natural_black_jack_calls_insurance(mocker, p_status, d_status):
    mock_seek_and_offer_insurance = mocker.patch(
        "blackjack.scripts.blackjack.BlackJack.seek_and_offer_insurance"
    )
    mock_insurance_result = mocker.patch(
        "blackjack.scripts.blackjack.BlackJack.insurance_result"
    )
    mock_seek_and_offer_insurance.return_value == True
    game_test = BlackJack(players=[Player(cash=1000.00)], deck=dck(), dealer=Dealer())
    game_test.players[0].hands[0].victory_status = p_status
    game_test.players[0].hands[0].bet = 100.00
    game_test.dealer.hand.victory_status = d_status
    game_test.check_natural_black_jack()
    mock_seek_and_offer_insurance.assert_called_once()
    mock_insurance_result.assert_called_once()


@pytest.mark.parametrize("p_status",[(15),(2)])
def test_natural_black_jack_insurance_pays(mocker,monkeypatch,p_status,d_status):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    dealer_test = Dealer(name="The dealer")
    dealer_test.hand = Hand(in_hand_cards=[Card(suit="Hearts", rank="Ace", cost=11, face_down=False),Card(suit="Hearts", rank="Queen", cost=10)])
    dealer_test.hand.calculate_points()
    dealer_test.hand.set_victory_status()
    game_test = BlackJack(players=[Player(cash=1000.00)],deck=dck(),dealer=dealer_test)
    game_test.players[0].hands[0].victory_status = p_status
    game_test.players[0].hands[0].bet = 100.00
    game_test.check_natural_black_jack()
    assert game_test.players[0].hands[0].coefficient == 0

@pytest.mark.parametrize("p_hand,d_hand,exp_coef",    [
        (
            [
                Card(suit="Hearts", rank="Ace", cost=11),
                Card(suit="Hearts", rank="Queen", cost=10),
            ],
            [
                Card(suit="Hearts", rank="Ace", cost=11, face_down=False),
                Card(suit="Hearts", rank="Six", cost=6),
            ],
            1.5,
        ),
        (
            [
                Card(suit="Hearts", rank="Ace", cost=11),
                Card(suit="Hearts", rank="Queen", cost=10),
            ],
            [
                Card(suit="Hearts", rank="Ace", cost=11, face_down=False),
                Card(suit="Hearts", rank="Queen", cost=10),
            ],
            0.0,
        ),
        (
            [
                Card(suit="Hearts", rank="Ace", cost=11),
                Card(suit="Hearts", rank="Six", cost=6),
            ],
            [
                Card(suit="Hearts", rank="Ace", cost=11, face_down=False),
                Card(suit="Hearts", rank="Queen", cost=10),
            ],
            -1.0,
        ),
    ],
)
def test_natural_black_jack_insurance_pays(mocker,monkeypatch,p_hand,d_hand,exp_coef):
    monkeypatch.setattr("builtins.input", lambda _: "n")

    dealer_test = Dealer(name="The dealer")
    dealer_test.hand = Hand(in_hand_cards=d_hand)
    dealer_test.hand.calculate_points()
    dealer_test.hand.set_victory_status()
    
    player_test = Player()
    player_test.hands[0].in_hand_cards = p_hand
    player_test.hands[0].calculate_points()
    player_test.hands[0].set_victory_status()
    player_test.hands[0].bet = 100.00

    game_test = BlackJack(players=[player_test],dealer=dealer_test,deck=dck(),)

    print(dealer_test.hand.victory_status)
    print(player_test.hands[0].victory_status)
    game_test.check_natural_black_jack()
    assert game_test.players[0].hands[0].coefficient == exp_coef


@pytest.mark.parametrize(
    "cards",
    [
        (
            [
                Card(suit="Hearts", rank="Ace", cost=11, face_down=False),
                Card(suit="Hearts", rank="Queen", cost=10),
            ]
        ),
        (
            [
                Card(suit="Hearts", rank="Ace", cost=11, face_down=False),
                Card(suit="Hearts", rank="King", cost=10),
            ]
        ),
        (
            [
                Card(suit="Spades", rank="Ace", cost=11, face_down=False),
                Card(suit="Clubs", rank="Two", cost=2),
            ]
        ),
    ],
)
def test_seek_and_offer_insurance(mocker, cards):
    mock_insurance_get_input = mocker.patch(
        "blackjack.scripts.blackjack.BlackJack.insurance_get_input"
    )
    dealer_test = Dealer()
    dealer_test.hand = Hand(in_hand_cards=cards)
    game_test = BlackJack(
        players=[Player(cash=1000.00)], deck=dck(), dealer=dealer_test
    )
    game_test.seek_and_offer_insurance()
    mock_insurance_get_input.assert_called_once()
