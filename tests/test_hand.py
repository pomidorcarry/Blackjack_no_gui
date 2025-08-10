import pytest
import unittest.mock as mock


from blackjack.scripts.hand import Hand
from blackjack.scripts.card import Card
from blackjack.scripts.deck import DeckClassic52


###fixtures
@pytest.fixture
def empty_hand():
    hand = Hand()
    return hand


@pytest.fixture
def hand_with_cards_0() -> dict:
    hand = Hand()
    hand.in_hand_cards = []
    hand_fix = {
        "hand": hand,
        "true_points_exp": 0,
        "show_points_exp": 0,
        "victory_status_exp": 0,
    }
    return hand_fix


@pytest.fixture
def hand_with_cards_1() -> dict:
    hand = Hand()
    hand.in_hand_cards = [
        Card(suit="Spades", rank="Five", cost=5),
        Card(suit="Spades", rank="Ace", cost=11),
        Card(suit="Spades", rank="Queen", cost=10),
    ]
    hand_fix = {
        "hand": hand,
        "true_points_exp": 26,
        "show_points_exp": 26,
        "victory_status_exp": 16,
    }
    return hand_fix


@pytest.fixture
def hand_with_cards_2() -> dict:
    hand = Hand()
    hand.in_hand_cards = [
        Card(suit="Hearts", rank="Two", cost=2),
        Card(suit="Spades", rank="Ace", cost=11),
        Card(suit="Spades", rank="Queen", cost=10),
    ]
    hand_fix = {
        "hand": hand,
        "true_points_exp": 23,
        "show_points_exp": 23,
        "victory_status_exp": 13,
    }
    return hand_fix


@pytest.fixture
def hand_with_cards_3() -> dict:
    hand = Hand()
    hand.in_hand_cards = [Card(suit="Spades", rank="Queen", cost=10)]
    hand_fix = {
        "hand": hand,
        "true_points_exp": 10,
        "show_points_exp": 10,
        "victory_status_exp": 10,
    }
    return hand_fix


@pytest.fixture
def hand_with_cards_4() -> dict:
    hand = Hand()
    hand.in_hand_cards = [
        Card(suit="Spades", rank="Queen", cost=10),
        Card(suit="Spades", rank="Queen", cost=10, face_down=True),
        Card(suit="Spades", rank="Queen", cost=10, face_down=True),
    ]
    hand_fix = {
        "hand": hand,
        "true_points_exp": 30,
        "show_points_exp": 10,
        "victory_status_exp": "BUST",
    }
    return hand_fix


@pytest.fixture
def hand_with_cards_5() -> dict:
    hand = Hand()
    hand.in_hand_cards = [
        Card(suit="Spades", rank="Ace", cost=11),
        Card(suit="Spades", rank="Queen", cost=10),
    ]
    hand_fix = {
        "hand": hand,
        "true_points_exp": 21,
        "show_points_exp": 21,
        "victory_status_exp": "NaturalBlackJack",
    }
    return hand_fix


@pytest.fixture
def hand_with_cards_6() -> dict:
    hand = Hand()
    hand.in_hand_cards = [
        Card(suit="Spades", rank="Ace", cost=11),
        Card(suit="Spades", rank="Queen", cost=10, face_down=True),
    ]
    hand_fix = {
        "hand": hand,
        "true_points_exp": 21,
        "show_points_exp": 11,
        "victory_status_exp": "NaturalBlackJack",
    }
    return hand_fix


###fixtures


@pytest.mark.parametrize("is_dealers", [(False,), (True,)])
def test_init_correct(is_dealers):
    hand_ = Hand(is_dealers)
    assert hand_.is_dealers == is_dealers
    assert hand_.in_hand_cards == []
    assert hand_.moved == False


###properties


@pytest.mark.parametrize("error", [("ERROR"), (0), (None)])
def test_in_hand_cards_invalid(empty_hand: Hand, error):
    with pytest.raises(ValueError):
        empty_hand.in_hand_cards = error


@pytest.mark.parametrize("value", [(10.0), (666.9556), (1.0)])
def test_bet_correct(empty_hand: Hand, value):
    empty_hand.bet = value
    assert empty_hand.bet == value


@pytest.mark.parametrize("error", [("ERROR"), ({}), (None), (-1), (0)])
def test_bet_invalid(empty_hand: Hand, error):
    bet = (error, 100)
    with pytest.raises(ValueError):
        empty_hand.bet = bet


@pytest.mark.parametrize("value", [(10), (50), (100)])
def test_bet_not_enough_cash(empty_hand: Hand, value):
    bet = (value, 1)
    with pytest.raises(ValueError):
        empty_hand.bet = bet


@pytest.mark.parametrize("error", [("ERROR"), ({}), (None), (-1), (0)])
def test_coefficient_invalid(empty_hand: Hand, error):
    with pytest.raises(ValueError):
        empty_hand.coefficient = error


@pytest.mark.parametrize("error", [("ERROR"), ({}), (None), ([]), (DeckClassic52)])
def test_points_invalid(empty_hand: Hand, error):
    with pytest.raises(ValueError):
        empty_hand.coefficient = error


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
def test_calculate_points_returns_correct_amount(fixture_hand, request):
    hand_whole = request.getfixturevalue(fixture_hand)
    hand: Hand = hand_whole["hand"]
    hand.calculate_points()
    assert hand.show_points == hand_whole["show_points_exp"]
    assert hand.true_points == hand_whole["true_points_exp"]


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
def test_calculate_points_property_called(fixture_hand, mocker, request):
    mock_true = mocker.patch.object(
        Hand, "true_points", new_callable=mocker.PropertyMock
    )
    mock_show = mocker.patch.object(
        Hand, "show_points", new_callable=mocker.PropertyMock
    )

    hand_whole = request.getfixturevalue(fixture_hand)
    hand: Hand = hand_whole["hand"]
    hand.calculate_points()

    mock_true.assert_called_once()
    mock_show.assert_called_once()


@pytest.mark.parametrize(
    "value", [("BUST"), ("NaturalBlackJack"), (10), (2), (0), (21), (24)]
)
def test_victory_status_correct(empty_hand: Hand, value):
    empty_hand.victory_status = value
    assert empty_hand.victory_status == value


@pytest.mark.parametrize(
    "value", [("ERROR"), ("randomtest"), (-10), (-2), (-21), (-24), ([]), (None)]
)
def test_victory_status_invalid(empty_hand: Hand, value):
    with pytest.raises(ValueError):
        empty_hand.victory_status = value


@pytest.mark.parametrize(
    "fixture_hand",
    [
        ("hand_with_cards_0"),
        ("hand_with_cards_1"),
        ("hand_with_cards_2"),
        ("hand_with_cards_3"),
        ("hand_with_cards_4"),
        ("hand_with_cards_5"),
    ],
)
def test_set_victory_status_correct(fixture_hand, request):
    hand_whole = request.getfixturevalue(fixture_hand)
    hand: Hand = hand_whole["hand"]
    hand.calculate_points()
    hand.set_victory_status()
    assert hand.victory_status == hand_whole["victory_status_exp"]


@pytest.mark.parametrize(
    "value", [("ERROR"), ("randomtest"), (-10), (-2), (-21), (-24), ([]), (None)]
)
def test_moved_invalid(empty_hand: Hand, value):
    with pytest.raises(ValueError):
        empty_hand.victory_status = value


@mock.patch("blackjack.scripts.hand.Hand.calculate_points")
def test_soft_hand_spot_called_on_22(mocker):
    hand = Hand(
        in_hand_cards=[
            Card(rank="Ace", suit="Hearts", cost=11),
            Card(rank="King", suit="Hearts", cost=10),
        ]
    )
    hand.true_points = 22
    hand.soft_hand_spot()
    mocker.assert_called_once()


def test_soft_hand_spot_reduces_cost_one_ace():
    hand = Hand(
        in_hand_cards=[
            Card(rank="Ace", suit="Hearts", cost=11),
            Card(rank="King", suit="Hearts", cost=10),
            Card(rank="King", suit="Hearts", cost=10),
        ]
    )
    hand.calculate_points()
    assert hand.true_points == 31
    hand.soft_hand_spot()
    ace = hand.in_hand_cards[0]
    assert ace.cost == 1


def test_soft_hand_spot_reduces_cost_two_aces():
    hand = Hand(
        in_hand_cards=[
            Card(rank="Ace", suit="Hearts", cost=11),
            Card(rank="Ace", suit="Spades", cost=11),
            Card(rank="King", suit="Hearts", cost=10),
            Card(rank="King", suit="Hearts", cost=10),
        ]
    )
    hand.calculate_points()
    assert hand.true_points == 42
    hand.soft_hand_spot()
    ace_1 = hand.in_hand_cards[0]
    assert ace_1.cost == 1
    ace_2 = hand.in_hand_cards[1]
    assert ace_2.cost == 1
