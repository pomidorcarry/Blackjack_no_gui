import sys
import os
import time

from .deck import DeckClassic52
from .player import Player
from .dealer import Dealer
from .blackjack import BlackJack


def main():
    while True:
        raw = BlackJack.get_name()
        if BlackJack.validate_name(raw):
            name_ = raw
            break

    game_0 = BlackJack(
        players=[
            Player(name=name_, cash=1000),
        ],
        deck=DeckClassic52(),
        dealer=Dealer(name="The Dealer"),
    )
    while True:
        print("=+= The game has just begun =+=")
        game_0.deck.shuffle_deck()
        game_0.place_bets()
        game_0.show_bets()
        game_0.initial_deal()
        game_0.check_natural_black_jack()

        for c_player in game_0.players:
            for c_hand in c_player.hands:
                if c_hand.coefficient == None:
                    print(game_0.deck.deck_info())
                    time.sleep(1)
                    game_0.show_player_dealer_hands(player=c_player, hand=c_hand)
                    c_player.make_move(game_0.deck)

        if game_0.dealer_should_play():
            game_0.dealer.make_move(game_0.deck)
        game_0.check_victory_status()
        game_0.deal_with_winners()
        time.sleep(2)
        
        if game_0.reset():
            continue
        else:
            print("Game over")
            return


if __name__ == "__main__":
    main()
