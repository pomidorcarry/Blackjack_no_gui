import sys
import re
import time

from .abstract_player import AbstractPlayer
from .deck import Deck
from .hand import Hand


class Player(AbstractPlayer):
    def __init__(self, name="blank", cash=0):
        super().__init__(name, cash)

    def take_card(self, deck: Deck, hand: Hand, face_down=False):
        """
        draws card from chosen deck and appends to the hand\n
        calculates points for the hand\n
        sets v_status for the hand\n
        optionaly checks for a pair and sets
        """
        super().take_card(deck, hand, face_down)
        hand.set_v_status()

    def get_bet(self) -> str:
        """input method\ngetting the bet"""
        try:
            raw = input(
                f"{self.name}, please, input your bet as a float of dollars and cents\nformat: 'dollars.cents'\n"
            )
        except KeyboardInterrupt:
            raw = "1.0"
        return raw

    def validate_bet(self, raw) -> float:
        """checking if the bet is in the correct format"""
        if not re.fullmatch(r"\d+\.\d{2}", raw):
            print("Please input in a format of 100.00")
            return 0
        bet = float(raw)
        if bet > self.cash or 0 >= bet:
            print(f"Bet should be under {self.cash:.2f} $\nbut greater than zero")
            return 0
        return bet

    def place_bet(self, hand: Hand) -> None:
        """setting validated bet in the bet attribute"""
        print(f"{self.name} has got {self.cash} $")
        while True:
            raw_bet = self.get_bet()
            bet = self.validate_bet(raw=raw_bet)
            if bet:
                hand.bet = bet
                print(f"Bet placed as {bet:.2f}")
                break

    def make_move(self, deck: Deck) -> None:
        """core gameplay method\nchecks if user got a pair\nprints options\nendless loop letting the player play\n until he either quits the game or end the round"""
        for hand in self.hands:
            print(f"==========\n⭐ It's {self.name}'s turn ⭐\n")
            options = {
                1: "Show your hand",
                2: "Take a card",
                3: "End your turn",
                4: "Double",
                10: "End the game",
            }
            self.moved = True
            if len(hand) == 1:
                self.take_card(deck, hand)
            double = 0
            self.check_pair(deck)
            while True:
                for k, v in options.items():
                    print(k, v)
                raw_choice = self.make_move_get_input()
                choice = self.make_move_validate_input(choice=raw_choice, options=options)
                if not choice:
                    continue
                match choice:
                    case 1:
                        self.show_hand(hand)
                        self.show_points(hand)
                    case 2:
                        if double == 2:
                            print("Only one card after double")
                        else:
                            print("HIT!")
                            self.take_card(deck, hand)
                            self.show_hand(hand)
                            self.show_points(hand)
                            if double == 1:
                                double += 1
                    case 3:
                        if len(hand) == 2:
                            print(f"Player {self.name} chose to STAND")
                            self.moved = True
                            break
                        else:
                            print(f"Player {self.name} has finished their turn")
                            self.moved = True
                            break
                    case 4:
                        if len(self.hands) > 1:
                            print("Can't make bet's with two hands")
                            continue
                        elif double > 0:
                            print("Already doubled")
                            continue
                        else:
                            bet = self.hands[0].bet
                            self.hands[0].bet = bet * 2
                            double = 1
                            print(f"your bet is now {self.hands[0].bet}$")
                    case 10:
                        print("Bye!\nClosing the program in 3!")
                        time.sleep(1)
                        print("2!")
                        time.sleep(1)
                        print("1!")
                        time.sleep(1)
                        sys.exit()

    def make_move_get_input(self) -> str:
        """input method, getting player's choice"""
        try:
            raw_choice = input("Make your move\n")
        except KeyboardInterrupt:
            print("Aborted")
            sys.exit()
        return raw_choice

    def make_move_validate_input(self, choice, options) -> int:
        """validating player's choice"""
        try:
            choice = int(choice)
        except ValueError:
            print("Only integers")
            return None
        if not choice in options.keys():
            print("Only numbers from the list")
            return None
        return choice

    def check_pair(self, deck_) -> None:
        """Chek's if there is a pair in the given hand and calls split"""
        if len(self.hands) > 1:
            print("More than one hand")
            return
        # to ensure that there are no aces in a pair
        elif not len(self.hands[0]) == 2:
            print("Splitting is only possible for two cards")
            return
        elif self.hands[0].true_points >= 22:
            print("More than 22 points")
            return
        elif not self.cash >= (self.hands[0].bet * 2):
            print("Not enough cash for a pair")
            return
        elif not(self.hands[0][0].rank == self.hands[0][1].rank):
            return
        else:
            print("Pair spotted")
            if self.check_pair_get_input():
                self.split_hand(deck_)

    def check_pair_get_input(self) -> bool:
        """get's user input on splitting the hand"""
        try:
            answer = input(
                "You have two cards of the same rank\nWould you like to split your hand?\ny or n?\n"
            )
        except KeyboardInterrupt:
            return False
        if answer.lower() == "y":
            return True

    def split_hand(self, deck_) -> None:
        """splits hand in two\nplacing equal bet on the second hand\ntakes one card in each hand\n"""
        inital_bet = self.hands[0].bet
        card1, card2 = self.hands[0][0], self.hands[0][1]
        hand1 = Hand()
        hand1.append(card1)
        hand1.bet = inital_bet
        hand2 = Hand()
        hand2.append(card2)
        hand2.bet = inital_bet
        self.hands = [hand1, hand2]
        self.take_card(deck=deck_, hand=self.hands[0])
        self.take_card(deck=deck_, hand=self.hands[1])

    def calculate_prize(self) -> float:
        """transforms players victory status into their cash prize"""
        prize = 0
        for hand in self.hands:
            prize_t = hand.bet * hand.coefficient
            prize += prize_t

        if self.cash + prize <= 0:
            print(f"You balance is now {self.cash + prize <= 0}\nGame over")
            time.sleep(2)
            sys.exit()
        else:
            self.cash += prize
            return prize
