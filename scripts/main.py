from .deck import Deck_classic_52
from .player import Player
from .dealer import Dealer
from .blackjack import BlackJack


def main():
    game_0 = BlackJack(players=[Player(name="Zakhar",cash=1000),],deck=Deck_classic_52(),dealer=Dealer(name="The Dealer"))
    while True:
        print("=+= The game has just begun =+=")
        game_0.deck.shuffle_deck()
        game_0.place_bets()
        game_0.show_bets()
        game_0.initial_deal()
        game_0.check_naturals()
        for player in game_0.players:
            print(player.coefficient)
            if player.coefficient == None:
                print(game_0.deck.deck_info())
                game_0.show_hands()
                game_0.dealer.show_hand()
                game_0.dealer.show_points()
                player.make_move(game_0.deck)
        #check if someone is still without a coefficient
        for player in game_0.players:
            if player.coefficient != None:
                continue
            else:
                game_0.dealer.make_move(game_0.deck)
                game_0.check_v_status()     
                break
        game_0.deal_with_winners()
        if game_0.reset():
            continue
        else:
            print("Game over")
            return

if __name__ == "__main__":
    main()