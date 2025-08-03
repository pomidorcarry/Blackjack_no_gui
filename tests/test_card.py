import pytest

from blackjack.scripts.card import Card
from blackjack.scripts.deck import Deck_classic_52

@pytest.fixture
def my_card():
    return Card(rank="King",cost=10,suit="Hearts",face_down=False)

###init
@pytest.mark.parametrize("rank0,cost0,suit0,face_down0",[("King",10,"Hearts",False),("King",10,"Spades",False),("Two",2,"Clubs",True)])
def test_init_correct(rank0,cost0,suit0,face_down0):
    card_ = Card(rank=rank0,suit=suit0,cost=cost0,face_down=face_down0)
    assert card_.cost == cost0
    assert card_.rank == rank0
    assert card_.suit == suit0
    assert card_.face_down == face_down0

@pytest.mark.parametrize("rank0,cost0,suit0,face_down0",[("King",10,0,False),("King",10,"ERROR",False)])
def test_init_invalid_suit(rank0,cost0,suit0,face_down0):
    with pytest.raises(ValueError):
        card_ = Card(rank=rank0,suit=suit0,cost=cost0,face_down=face_down0)

@pytest.mark.parametrize("rank0,cost0,suit0,face_down0",[("prince",10,"Hearts",False),("Ralsei",10,"Hearts",False),(404,10,"Spades",False)])
def test_init_invalid_rank(rank0,cost0,suit0,face_down0):
    with pytest.raises(ValueError):
        card_ = Card(rank=rank0,suit=suit0,cost=cost0,face_down=face_down0)
    
@pytest.mark.parametrize("rank0,cost0,suit0,face_down0",[("King",0,"Hearts",False),("King",-4,"Hearts",False),("King",-1000,"Spades",False)])
def test_init_invalid_cost(rank0,cost0,suit0,face_down0):
    with pytest.raises(ValueError):
        card_ = Card(rank=rank0,suit=suit0,cost=cost0,face_down=face_down0)
###init+property

def test_name_str_repr_property(my_card):
    assert type(my_card.name) == str
    assert type(my_card.__str__()) == str
    assert type(my_card.__repr__()) == str


def test_comparison():
    card1 = Card(rank="Two",cost=2,suit="Spades",face_down=False)
    card2 = Card(rank="Ace",cost=11,suit="Hearts",face_down=False)
    card3 = Card(rank="Two",cost=2,suit="Hearts",face_down=False)
    card4 = Card(rank="Two",cost=20,suit="Hearts",face_down=False)
    assert card1 < card2
    assert card2 > card1
    assert not card1 == card3
    assert card3 == card4


def test_comparison_error():
    card1 = Card(rank="Two",cost=2,suit="Hearts",face_down=False)
    deck = Deck_classic_52()
    a_number = 101
    with pytest.raises(ValueError):
        assert card1 < a_number
        assert a_number > card1
        assert card1 == a_number
    with pytest.raises(ValueError):
        assert card1 < a_number
        assert a_number > card1
        assert card1 == a_number
