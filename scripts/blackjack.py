from .deck import Deck_classic_52
from .player import Player
from .dealer import Dealer
from .hand import Hand

import re
import sys
import time


class BlackJack:
    def __init__(self, players: list[Player], deck: Deck_classic_52, dealer: Dealer):
        self.__players = players
        self.__deck = deck
        self.__dealer = dealer

    @property
    def players(self):
        return self.__players

    @players.setter
    def players(self, players):
        for player in players:
            if not type(player) == Player:
                raise ValueError("Only player objects in players list")
        else:
            self.__players = players

    @property
    def deck(self):
        return self.__deck

    @deck.setter
    def deck(self, deck):
        if not type(deck) == Deck_classic_52:
            raise ValueError("Only deck objects")
        else:
            self.__deck = deck

    @property
    def dealer(self):
        return self.__dealer

    @dealer.setter
    def dealer(self, dealer):
        if not type(dealer) == Dealer:
            raise ValueError("Only dealer objects")
        else:
            self.__dealer = dealer

    def place_bets(self) -> None:
        """
        each player in players places his bet\n
        player only has one hand at this point!
        """
        for player in self.players:
            player.place_bet(hand=player.hands[0])

    def show_bets(self) -> None:
        """
        shows players bets
        """
        print("---")
        for player in self.players:
            print(f"{player.name}'s bet is {player.hands[0].bet:.2f} $")
        print("---")
        time.sleep(1)

    def initial_deal(self) -> None:
        """
        initially dealing cards to all players and the dealer\n
        face up/down\n
        right now only one hand is possible with 0 cards
        """
        for player in self.players:
            for _ in range(2):
                player.take_card(self.deck, hand=player.hands[0], face_down=False)
        self.dealer.take_card(self.deck, face_down=True)
        self.dealer.take_card(self.deck, face_down=False)

    def check_natural_black_jack(self) -> None:
        """
        only one hand is possible right now\n
        if player doesn't have blackjack we offer insurance\n
        checking if anyone has won after the initial deal
        """
        for player in self.players:

            d_hand = self.dealer.hand
            p_hand = player.hands[0]

            if p_hand.v_status != "NaturalBlackJack":
                insurance = self.seek_and_offer_insurance()
                if insurance:
                    self.insurance_result(player)
            if p_hand.coefficient != None:
                continue
            if (
                d_hand.v_status != "NaturalBlackJack"
                and p_hand.v_status == "NaturalBlackJack"
            ):
                p_hand.coefficient = 1.5
            elif (
                d_hand.v_status == "NaturalBlackJack"
                and p_hand.v_status == "NaturalBlackJack"
            ):
                p_hand.coefficient = 0.0
            elif (
                d_hand.v_status == "NaturalBlackJack"
                and p_hand.v_status != "NaturalBlackJack"
            ):
                p_hand.coefficient = -1.0

    def seek_and_offer_insurance(self) -> bool:
        """checks if it's valid to offer insurance"""
        for card in self.dealer.hand:
            if not (card.face_down == False and card.cost == 11):
                continue
            elif self.insurance_get_input():
                return True
        else:
            return False

    def insurance_get_input(self):
        """input method gets wether player want's or not to buy insurance"""
        try:
            self.dealer.show_hand(self.dealer.hand)
            ans = input(
                "Looks like the dealer may have a natural blackjack\nwould you like to place half of your bet that he got a natural blackjack\n(y or n?)\n"
            )
        except KeyboardInterrupt:
            return False
        if ans.lower() == "y":
            return True
        else:
            return False

    def insurance_result(self, player: Player):
        if self.dealer.hand.v_status == "NaturalBlackJack":
            print("Insurance pays\n")
            player.hands[0].coefficient = 0.0
        elif self.dealer.hand.v_status != "NaturalBlackJack":
            player.cash -= player.hands[0].bet / 2
            print(
                f"player {player.name} has lost their insurance {player.hands[0].bet/2}$!"
            )

    def show_player_dealer_hands(self, player, hand: Hand) -> None:
        """
        shows the current player's hand and dealer's hand
        """
        player.show_hand(hand)
        player.show_points(hand)
        time.sleep(2)
        self.dealer.show_hand(hand=self.dealer.hand)
        self.dealer.show_points(self.dealer.hand)
        time.sleep(2)

    def show_cash(self) -> None:
        """
        displaing players current cash
        """
        for player in self.players:
            print(f"{player.name} has {player.cash} $ on their balance")

    def dealer_should_play(self) -> bool:
        """if at least one player is yet not BUSTED or doesn't have NaturalBlackJack\nThe dealer should make his move"""
        for player in self.players:
            for hand in player.hands:
                if hand.v_status not in ["BUST", "NaturalBlackJack"]:
                    return True
        else:
            return False

    def check_v_status(self):
        """
        end of the round\n
        check if dealer bust\n
        compare points
        """
        if self.dealer.hand.v_status == "BUST":
            for player in self.players:
                for hand in player.hands:
                    if not hand.coefficient:
                        hand.coefficient = 1.0
        # else:
        elif self.dealer.hand.v_status != "NaturalBlackJack":
            for player in self.players:
                for hand in player.hands:
                    if isinstance(hand.coefficient, float):
                        return
                    elif hand.v_status == "BUST":
                        hand.coefficient = -1.0
                    elif hand.v_status > 21:
                        hand.coefficient = -1.0
                    elif hand.v_status > self.dealer.hand.v_status:
                        hand.coefficient = 1.0
                    else:
                        hand.coefficient = -1.0

    def deal_with_winners(self) -> None:
        """
        set prizes and print who won and how much
        """
        print(f"{self.dealer.name} got {self.dealer.hand.v_status}")
        for player in self.players:
            prize = player.calculate_prize()
            if prize > 0:
                print(
                    f"{player.name} got {'and'.join([str(i.v_status) for i in player.hands])}\nHe won {prize:.2f}$!💸💸💸"
                )
            else:
                print(
                    f"Because {player.name} got {'and'.join([str(i.v_status) for i in player.hands])}\n He lost {prize:.2f}$!😭😭😭"
                )
            print(f"{player.name} now got {player.cash}")

    def reset(self) -> bool:
        """
        ask wether the player would like to try another round\n
        or break the cycle and close the program
        """
        try:
            answer = input(
                "The game is over, would you like to try one more time?\ny or n?"
            )
        except KeyboardInterrupt:
            print("Understood!Bye!")
            sys.exit()
        if answer.lower() == "y":
            players_ = []
            for player in self.players:
                name_ = player.name
                cash_ = player.cash
                players_.append(Player(name=name_, cash=cash_))

            dealer_name = self.dealer.name

            deck_used = self.deck
            self.__init__(
                players=players_,
                dealer=Dealer(name=dealer_name),
                deck=deck_used,
            )
            return True

    @staticmethod
    def get_name() -> str:
        """input method"""
        try:
            raw = input(
                "Please input your name\nIt can contain only letters a-z, whitespace and underscore\n"
            )
        except KeyboardInterrupt:
            return None
        return raw

    @staticmethod
    def validate_name(name) -> str | None:
        """validating given name"""
        if not re.fullmatch(f"[a-zA-Z_ ]+", name):
            return None
        return name
