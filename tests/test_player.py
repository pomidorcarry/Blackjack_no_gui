import pytest
import unittest.mock as mock
from blackjack.scripts.player import Player
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
def player_():
    return Player()


def test_empty_player(player_: Player):
    assert player_.name == "blank"
    assert player_.cash == 0


def test_take_card_grows_hand(player_: Player):
    deck = dck()
    before_draw = len(player_.hands[0])
    player_.take_card(deck, player_.hands[0])
    after_draw = len(player_.hands[0])
    assert type(player_.hands[0][0]) is Card
    assert before_draw + 1 == after_draw


@pytest.mark.parametrize(
    "fixture_hand",
    [
        ("hand_with_cards_0"),
        ("hand_with_cards_1"),
        ("hand_with_cards_2"),
        ("hand_with_cards_3"),
        ("hand_with_cards_4"),
        ("hand_with_cards_5"),
        ("hand_with_cards_6"),
    ],
)
def test_take_card_calls_v_status(mocker, player_: Player, fixture_hand: Hand, request):
    mock_set_v_status = mocker.patch("blackjack.scripts.hand.Hand.set_v_status")
    hand_whole = request.getfixturevalue(fixture_hand)
    test_hand: Hand = hand_whole["hand"]
    player_.take_card(deck=dck(), hand=test_hand)
    mock_set_v_status.assert_called_once()


@pytest.mark.parametrize(
    "fixture_hand",
    [
        ("hand_with_cards_0"),
        ("hand_with_cards_1"),
        ("hand_with_cards_2"),
        ("hand_with_cards_3"),
        ("hand_with_cards_4"),
        ("hand_with_cards_5"),
        ("hand_with_cards_6"),
    ],
)
def test_take_card_correct_v_status(
    mocker, player_: Player, fixture_hand: Hand, request
):
    # we replace the card drawn from the deck with a mock card costing zero points
    # to test that with cards in hand the v status will be expected value
    # mock_card = mock.MagicMock()
    # mock_card.cost = 0
    mock_draw_from_deck = mocker.patch(
        "blackjack.scripts.deck.Deck_classic_52.draw_from_deck"
    )
    mock_draw_from_deck.return_value = None
    # get the hand fixture and set it as the hand of the player
    hand_whole = request.getfixturevalue(fixture_hand)
    test_hand: Hand = hand_whole["hand"]
    player_.hands = [test_hand]
    player_.take_card(deck=dck(), hand=player_.hands[0])
    # check that after player draws the card his v_status is correct
    assert player_.hands[0].v_status == hand_whole["v_status_exp"]


@pytest.mark.parametrize("values", [(["a", 1]), (["Word", 1]), ([None, 1])])
def test_place_bet_prints_error(monkeypatch, values, capsys):
    # first the incorrect value is fed to input to test correct error messages
    # then the correct value is fed to quit while loop
    it = iter(values)
    monkeypatch.setattr("builtins.input", lambda _: next(it))
    player_t = Player(cash=100)
    player_t.place_bet(player_t.hands[0])
    captured = capsys.readouterr()
    assert (
        captured.out
        == "blank has got 100$\nPlease input only numbers in a specified format\n"
    )


@pytest.mark.parametrize("values", [([300, 1]), ([1000, 1]), ([101, 1])])
def test_place_bet_cash_error(monkeypatch, values, capsys):
    # first the incorrect value is fed to input to test correct error messages
    # then the correct value is fed to quit while loop
    it = iter(values)
    monkeypatch.setattr("builtins.input", lambda _: next(it))
    player_t = Player(cash=100)
    player_t.place_bet(player_t.hands[0])
    captured = capsys.readouterr()
    assert captured.out == f"blank has got 100$\nYou only have {player_t.cash:.2f}$\n"


@pytest.mark.parametrize("value", [(5), (50), (99)])
def test_place_bet_correct(monkeypatch, value, capsys):
    monkeypatch.setattr("builtins.input", lambda _: value)
    player_t = Player(cash=100)
    player_t.place_bet(player_t.hands[0])
    assert player_t.hands[0].bet == value


def test_place_bet_interrupt(monkeypatch):
    # chatgpt told we use it
    # idk what the heck it is
    monkeypatch.setattr(
        "builtins.input", lambda _: (_ for _ in ()).throw(KeyboardInterrupt)
    )
    player_t = Player(cash=100)
    player_t.place_bet(player_t.hands[0])
    assert player_t.hands[0].bet == 1.0


@pytest.mark.parametrize(
    "hands_p",
    [
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Ten", suit="Hearts", cost=10),
                    Card(rank="Ten", suit="Spades", cost=10),
                ]
            )
        ],
        [
            Hand(
                in_hand_cards=[
                    Card(rank="King", suit="Hearts", cost=10),
                    Card(rank="King", suit="Spades", cost=10),
                ]
            )
        ],
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Six", suit="Hearts", cost=6),
                    Card(rank="Six", suit="Spades", cost=6),
                ]
            )
        ],
    ],
)
def test_check_pair_calls_slit_hand(monkeypatch, mocker, hands_p):
    mock_split_hand = mocker.patch("blackjack.scripts.player.Player.split_hand")
    monkeypatch.setattr("builtins.input", lambda _: "y")
    player_t = Player(cash=200)
    player_t.hands = hands_p
    player_t.hands[0].calculate_points()
    player_t.hands[0].bet = 100.0
    player_t.check_pair()
    mock_split_hand.assert_called_once()


@pytest.mark.parametrize(
    "hands_p",
    [
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Ten", suit="Hearts", cost=10),
                    Card(rank="Ten", suit="Spades", cost=10),
                ]
            ),
            Hand(
                in_hand_cards=[
                    Card(rank="Ten", suit="Hearts", cost=10),
                    Card(rank="Ten", suit="Spades", cost=10),
                ]
            ),
        ],
        [
            Hand(
                in_hand_cards=[
                    Card(rank="King", suit="Hearts", cost=10),
                    Card(rank="King", suit="Spades", cost=10),
                ]
            ),
            Hand(
                in_hand_cards=[
                    Card(rank="King", suit="Hearts", cost=10),
                    Card(rank="King", suit="Spades", cost=10),
                ]
            ),
        ],
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Six", suit="Hearts", cost=6),
                    Card(rank="Six", suit="Spades", cost=6),
                ]
            ),
            Hand(
                in_hand_cards=[
                    Card(rank="Six", suit="Hearts", cost=6),
                    Card(rank="Six", suit="Spades", cost=6),
                ]
            ),
        ],
    ],
)
def test_check_pair_two_hands(hands_p, capsys):
    player_t = Player(cash=200)
    player_t.hands = hands_p
    player_t.hands[0].calculate_points()
    player_t.hands[0].bet = 100.0
    player_t.check_pair()
    captured = capsys.readouterr()
    assert captured.out == "More than one hand\n"


@pytest.mark.parametrize(
    "hands_p",
    [
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Six", suit="Hearts", cost=6),
                    Card(rank="Six", suit="Spades", cost=6),
                    Card(rank="Six", suit="Spades", cost=6),
                ]
            )
        ],
        [
            Hand(
                in_hand_cards=[
                    Card(rank="King", suit="Hearts", cost=10),
                ]
            )
        ],
    ],
)
def test_check_pair_not_two_cards(hands_p, capsys):
    player_t = Player(cash=200)
    player_t.hands = hands_p
    player_t.hands[0].calculate_points()
    player_t.hands[0].bet = 100.0
    player_t.check_pair()
    captured = capsys.readouterr()
    assert captured.out == "Splitting is only possible for two cards\n"


@pytest.mark.parametrize(
    "hands_p",
    [
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Ace", suit="Hearts", cost=11),
                    Card(rank="Ace", suit="Spades", cost=11),
                ]
            )
        ],
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Ace", suit="Clubs", cost=11),
                    Card(rank="Ace", suit="Diamonds", cost=11),
                ]
            )
        ],
    ],
)
def test_check_pair_aces(hands_p, capsys):
    player_t = Player(cash=200)
    player_t.hands = hands_p
    player_t.hands[0].calculate_points()
    player_t.hands[0].bet = 100.0
    player_t.check_pair()
    captured = capsys.readouterr()
    assert captured.out == "More than 22 points\n"

@pytest.mark.parametrize(
    "hands_p",
    [
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Six", suit="Hearts", cost=6),
                    Card(rank="Six", suit="Spades", cost=6),
                ]
            )
        ],
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Queen", suit="Clubs", cost=10),
                    Card(rank="Queen", suit="Diamonds", cost=10),
                ]
            )
        ],
    ],
)
def test_check_pair_low_on_cash(hands_p, capsys):
    player_t = Player(cash=1)
    player_t.hands = hands_p
    player_t.hands[0].calculate_points()
    player_t.hands[0].bet = 100.0
    player_t.check_pair()
    captured = capsys.readouterr()
    assert captured.out == "Not enough cash for a pair\n"


@pytest.mark.parametrize(
    "hands_before",
    [
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Six", suit="Hearts", cost=6),
                    Card(rank="Six", suit="Spades", cost=6),
                ]
            )
        ],  
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Queen", suit="Hearts", cost=10),
                    Card(rank="Queen", suit="Spades", cost=10),
                ]
            )
        ],
    ],
)
def test_split_hand_take_card_called(mocker,hands_before):
    mock_take_card = mocker.patch("blackjack.scripts.player.Player.take_card")
    player_t = Player(cash=200)
    player_t.hands = hands_before
    player_t.hands[0].bet = 100.0
    player_t.split_hand()
    mock_take_card.assert_called()

@pytest.mark.parametrize(
    "hands_before,hands_after",
    [
        ([
            Hand(
                in_hand_cards=[
                    Card(rank="Six", suit="Hearts", cost=6),
                    Card(rank="Six", suit="Spades", cost=6),
                ]
            )
        ],
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Six", suit="Hearts", cost=6),
                    
                ]
            ),
            Hand(
                in_hand_cards=[
                    Card(rank="Six", suit="Spades", cost=6),
                    
                ]
            )
        ]),        
        ([
            Hand(
                in_hand_cards=[
                    Card(rank="Queen", suit="Hearts", cost=10),
                    Card(rank="Queen", suit="Spades", cost=10),
                ]
            )
        ],
        [
            Hand(
                in_hand_cards=[
                    Card(rank="Queen", suit="Hearts", cost=10),
                    
                ]
            ),
            Hand(
                in_hand_cards=[
                    Card(rank="Queen", suit="Spades", cost=10),
                    
                ]
            )
        ]),
    ],
)
def test_split_hand_correct_hands(mocker,hands_before,hands_after):
    # mock_card = Card(rank="Two", suit="Hearts", cost=2)
    mock_take_card = mocker.patch("blackjack.scripts.player.Player.take_card")
    # mock_take_card.return_value = mock_card
    player_t = Player(cash=200)
    player_t.hands = hands_before
    # player_t.hands[0].calculate_points()
    init_bet = 100.00
    player_t.hands[0].bet = 100.00
    player_t.split_hand()
    assert len(player_t.hands) == 2
    assert len(player_t.hands[0]) == 1
    assert len(player_t.hands[1]) == 1
    assert player_t.hands[0].in_hand_cards == hands_after[0].in_hand_cards
    assert player_t.hands[1].in_hand_cards == hands_after[1].in_hand_cards
    assert player_t.hands[0].bet == init_bet
    assert player_t.hands[1].bet == init_bet

