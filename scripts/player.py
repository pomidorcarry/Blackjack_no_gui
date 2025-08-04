import sys

from .abstract_player import AbstractPlayer
from .deck import Deck
from .hand import Hand

class Player(AbstractPlayer):
    def __init__(self, name = "blank", cash=0):
        super().__init__(name, cash)
        
    def take_card(self, deck:Deck, hand:Hand, face_down=False):
        '''
        draws card from chosen deck and appends to the hand\n
        calculates points for the hand\n
        sets v_status for the hand\n
        optionaly checks for a pair and sets 
        '''
        super().take_card(deck, hand, face_down)
        hand.set_v_status()
        print(f"{hand.v_status}")
        
    def place_bet(self,hand:Hand):
        print(f"{self.name} has got {self.cash}$")
        while True:
            try:
                bet_ = float(input(f"{self.name}, please, input your bet as a float of dollars and cents\nformat: 'dollars.cents'\n"))
            except KeyboardInterrupt:
                bet_ = 0.0
                print("Bet placed as 0 dollars 0 cents")
                break
            except ValueError:
                print("Please input only numbers in a specified format")
                continue
            if bet_ > self.cash:
                print(f"You only have {self.cash:.2f}$")
            else:
                break
        hand.bet = bet_

    def make_move(self,deck:Deck) -> None:
        if len(self.hands) == 1:
            if len(self.hands[0]) == 2 and self.cash >= (self.hands[0].bet*2):
                self.check_pair(self.hands[0])
        for hand in self.hands:
            print(f"==========\n⭐ It's {self.name}'s turn ⭐")
            options = {
                1:"Show your hand",
                2:"Take a card",
                3:"End your turn",
                0:"End the game"
            }
            self.moved = True
            if len(hand) == 1:
                self.take_card(deck,hand)
            while True:
                for k,v in options.items():
                    print(k,v)
                try:
                    choice = int(input("Make a move\n"))
                except KeyboardInterrupt:
                    print("Aborted")
                    return
                except ValueError:
                    print("only integers")
                    return
                if choice == 1:
                    self.show_hand(hand)
                    self.show_points(hand)
                elif choice == 2:
                    print("HIT!")
                    self.take_card(deck,hand)
                elif choice == 3:
                    if len(hand) == 2:
                        print(f"Player {self.name} chose to STAND")
                        break
                    else:
                        print(f"Player {self.name} has finished their turn")
                        break
                elif choice == 0:
                    "Bye!"
                    sys.exit()
                else:
                    print("Only numbers from the list")

    def check_pair(self,hand):
        if hand[0].rank == hand[1].rank:
            print("Pair spotted")
            try:
                answer = input("Would you like to split your hand?\ny or n?\n")
            except KeyboardInterrupt:
                return
            if answer.lower() == "y":
                self.split_hand()

    def split_hand(self):
        inital_bet = self.hands[0].bet
        card1,card2 = self.hands[0][0],self.hands[0][1]
        hand1 = Hand()
        hand1.append(card1)
        hand1.bet = inital_bet
        hand2 = Hand()
        hand2.append(card2)
        hand2.bet = inital_bet
        self.hands = [hand1,hand2]

    #we transform players victory status into their cash prize
    def calculate_prize(self)->float:
        for hand in self.hands:
            prize =  hand.bet * hand.coefficient    
            self.cash += prize
            return prize
