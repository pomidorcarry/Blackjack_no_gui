from .card import Card

class Hand:
    def __init__(self,is_dealers=False,in_hand_cards=None):
        if in_hand_cards is None:
            self.in_hand_cards:list[Card] = []
        else:
            self.in_hand_cards:list[Card] =in_hand_cards
        self.is_dealers = is_dealers
        self.moved = False
        self.__v_status = None 
        self.__coefficient = None

    def append(self,value):
        self.__in_hand_cards.append(value)

    def __getitem__(self,key):
        return self.__in_hand_cards[key]

    def __len__(self):
        return len(self.__in_hand_cards)

###in_hand_cards
    @property
    def in_hand_cards(self):
        return self.__in_hand_cards
    
    @in_hand_cards.setter
    def in_hand_cards(self,value):
        if type(value) == list:
            self.__in_hand_cards=value
        else:
            raise ValueError("Only list values for this property")
###in_hand_cards

###bet
    @property
    def bet(self):
        return self.__bet
    
    @bet.setter
    def bet(self,value:int|float):
        if not (type(value) == int or type(value) == float):
            raise ValueError("Only int or float values for this property")
        elif not value > 0:
            raise ValueError("Only int or float values for this property")
        else:
            self.__bet = value

    @bet.deleter
    def bet(self):
        del self.__bet
###bet
###coefficient
    @property
    def coefficient(self):
        return self.__coefficient
    
    @coefficient.setter
    def coefficient(self,value:float):
        if not type(value) == float:
            raise ValueError("Not expected value error")
        if not value in [1.5,1.0,-1.0,0.0]:
            raise ValueError("Not expected value error")   
        else:
            self.__coefficient = value

    @coefficient.deleter
    def coefficient(self):
        del self.__coefficient
###coefficient
###points
    @property
    def points(self):
        return self.__points
    
    @points.setter
    def points(self,points:int):
        if not type(points) == int:  
            raise ValueError("Only integers for this value")
        else:
            self.__points = points    

    @points.deleter
    def points(self):
        del self.__points

    def calculate_points(self)->int:
        points = 0
        for card in self.in_hand_cards:
            if card.face_down == False:
                points += card.cost
        return points
###points
#v_statuts
    possible_v_statuses = [
        "BUST",
        "NaturalBlackJack",
    ]

    @property
    def v_status(self):
        return self.__v_status
    
    @v_status.setter
    def v_status(self,value):
        if value in Hand.possible_v_statuses or type(value) == int:
            self.__v_status = value
        # else:
        #     self.__v_status = None

    @v_status.deleter
    def v_status(self):
        del self.__v_status

    def set_v_status(self)->None:
        if self.points > 21:
            for card in self.hand:
                if card.cost == 11:
                    print("Soft hand spotted!")
                    card.cost = 1
                    print(f"{card.name} now costs 1 point")
                    break
            else:
                self.v_status = "BUST"
        elif self.points == 21 and len(self.hand) == 2:
            self.v_status = "NaturalBlackJack"
        else:
            self.v_status = self.points

#v_statuts

    @property
    def moved(self):
        return self.__moved
    @moved.setter
    def moved(self,value:bool):
        if type(value) == bool:
            self.__moved = value
    