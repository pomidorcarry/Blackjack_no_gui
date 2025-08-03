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
        self.__show_points = None
        self.__true_points = None

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
        if type(value) is list:
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
        if not (type(value) is int or type(value) is float):
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
        if not type(value) is float:
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
    #these points are public and for show
    @property
    def show_points(self):
        return self.__show_points
    
    @show_points.setter
    def show_points(self,value:int):
        if not type(value) is int:  
            raise ValueError("Only integers for this value")
        else:
            self.__show_points = value

    #these points are used for calculations and checks
    @property
    def true_points(self):
        return self.__true_points
    
    @true_points.setter
    def true_points(self,value:int):
        if not type(value) is int:  
            raise ValueError("Only integers for this value")
        else:
            self.__true_points = value

    def calculate_points(self)->None:
        show_points = 0
        true_points = 0
        for card in self.in_hand_cards:
            if card.face_down:
                true_points += card.cost
            else:
                true_points += card.cost
                show_points += card.cost
        self.true_points = true_points
        self.show_points = show_points
    
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
        if not (value in Hand.possible_v_statuses or type(value) is int):
            raise ValueError("Only allowed v_statuses")
        elif type(value) is int and value < 0: 
            raise ValueError("Only allowed v_statuses")
        else:
            self.__v_status = value

    def set_v_status(self)->None:
        self.soft_hand_spot()
        if self.true_points > 21:
            self.v_status = "BUST"
        elif self.true_points == 21 and len(self.in_hand_cards) == 2:
            self.v_status = "NaturalBlackJack"
        else:
            self.v_status = self.true_points

    def soft_hand_spot(self)->None:
        if self.true_points > 21:
            for card in self.in_hand_cards:
                if card.cost == 11:
                    print("Soft hand spotted!")
                    card.cost = 1
                    print(f"{card.name} now costs 1 point")
                    self.calculate_points()
                    break

#v_statuts

    @property
    def moved(self):
        return self.__moved
    @moved.setter
    def moved(self,value:bool):
        if type(value) is bool:
            self.__moved = value
        else:
            raise ValueError("Only boolean values")
    