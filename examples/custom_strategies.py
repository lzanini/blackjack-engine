import random

from blackjack_engine.simulation import BlackjackSimulation
from blackjack_engine.strategy import BasePlayingStrategy
from blackjack_engine.strategy import BaseBettingStrategy


# Custom playing strategy
class MyStrategy(BasePlayingStrategy):
    def declare_action(self, player_hand, dealer_card, remaining_cards, available_actions):
        if 'split' in available_actions and player_hand.cards[0] == 'A':
            return 'split'
        elif 'double' in available_actions and player_hand.value == 11:
            return 'double'
        elif player_hand.is_soft and player_hand.value < 18:
            return 'hit'
        elif not player_hand.is_soft and player_hand.value < 17:
            return 'hit'
        return 'stand'


# A random betting strategy.
class RandomBetting(BaseBettingStrategy):
    def __init__(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount

    def declare_bet(self, cards_delt, remaining_cards):
        return random.uniform(self.min_amount, self.max_amount)


if __name__ == '__main__':

    simulation = BlackjackSimulation(nb_decks=1,
                                     penetration=0.5,
                                     max_hands=3,
                                     double_after_split=True,
                                     hit_soft_17=True)

    simulation.register_player(name="Bob",
                               betting_strategy=RandomBetting(min_amount=1, max_amount=2),
                               playing_strategy=MyStrategy())

    history = simulation.run(nb_rounds=3, verbose=False)
    print('gains:', history["Bob"]["gains"])
