
class Card:
    valid_suits = [
        "Hearts",
        "Diamonds",
        "Clubs",
        "Spades"
    ]
    valid_ranks_face = {
        "Ace":11,
        "Jack":10,
        "Queen":10,
        "King":10,
    }
    valid_ranks_digits = {
        "Two":2,
        "Three":3,
        "Four":4,
        "Five":5,
        "Six":6,
        "Seven":7,
        "Eight":8,
        "Nine":9,
        "Ten":10,
    }

    def __init__(self,suit:str,rank:str,cost:int,face_down=False):
        self.rank = rank
        self.cost = cost
        self.suit = suit
        self.face_down = face_down

###suit
    @property
    def suit(self):
        return self.__suit
    
    @suit.setter
    def suit(self,value):
        if value in Card.valid_suits:
            self.__suit = value
        else:
            raise ValueError("{value} isn't one of the possible card suits")
###suit

###rank
    @property
    def rank(self):
        return self.__rank
    
    @rank.setter
    def rank(self,value):
        if value in Card.valid_ranks_digits or value in Card.valid_ranks_face.keys():
            self.__rank = value
        else:
            raise ValueError("{value} isn't one of the possible card ranks")
###rank
    @property
    def name(self):
        return f"The {self.__rank} of {self.suit}"

    @property
    def cost(self):
        return self.__cost
    
    @cost.setter
    def cost(self,value):
        if value > 0:
            self.__cost = value
        else:
            raise ValueError(f"{value} should be greater than zero")
    
    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Card({self.suit},{self.rank},{self.cost})"
    
    def __lt__(self,other):
        if type(other)==Card:
            return self.cost < other.cost
        else:
            raise ValueError(f"{other} isn't a card object")

    def __gt__(self,other):
        if type(other)==Card:
            return self.cost > other.cost
        else:
            raise ValueError(f"{other} isn't a card object")

    def __eq__(self,other):
        if type(other)==Card:
            return self.rank == other.rank and self.suit == other.suit
        else:
            raise ValueError(f"{other} isn't a card object")
    
    # def __mul__(self,other):
    #     if type(other)==int:
    #         return [Card(name=self.name,cost=self.cost) for i in range(other)]
    #     else:
    #         raise ValueError(f"{other} isn't an integer")
