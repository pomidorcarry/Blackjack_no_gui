from abc import ABC,abstractmethod
from .deck import Deck
from .hand import Hand
class AbstractPlayer(ABC):
    def __init__(self,name:str="blank",cash = 0):
        super().__init__()
        self.name = name
        self.__cash = cash
        self.hands:list[Hand] = []

    @property
    def cash(self):
        return self.__cash
    
    @cash.setter
    def cash(self,value):
        if not (type(value) == int or type(value) == float):
            raise ValueError("Please, enter floats and integers for cash")
        else:
            self.__cash = float(value)

    @abstractmethod
    def make_move(self):
        pass
            
    def take_card(self,deck:Deck,hand:Hand,face_down = False)->None:
        if drawn:= deck.draw_from_deck():
            drawn.face_down = face_down
            hand.append(drawn)
        hand.points = hand.calculate_points()
        
    def show_hand(self,hand)->None:
        if not hand:
            print("Your hand is empty")
        else:
            print("==========")
            print(f"{self.name}'s current hand is:")
            for card in self.hand:
                if card.face_down == True:
                    print(f"    🃏This card is face down")
                elif card.face_down ==False:
                    print(f"    🃏{card}")
            print("==========")

    def show_points(self,hand) -> None:
        for card in hand:
            if card.face_down == True:
                print(f"{self.name}'s current points are {self.points} + X points")
                return
        print(f"{self.name}'s current points are {self.points}")
            
