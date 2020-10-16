from blackjack_engine.simulation import BlackjackSimulation
from blackjack_engine.strategy import RandomPlay
from blackjack_engine.strategy import ConstantBetting
from blackjack_engine.strategy import BaseBettingStrategy
from blackjack_engine.strategy import BasePlayingStrategy


from blackjack_engine.simulation import BlackjackSimulation
from blackjack_engine.strategy import RandomPlay
from blackjack_engine.strategy import ConstantBetting

simulation = BlackjackSimulation(nb_decks=4,
                                 penetration=0.5)

simulation.register_player(name="Bob",
                           betting_strategy=ConstantBetting(),
                           playing_strategy=RandomPlay())

history = simulation.run(nb_rounds=100000)
print("Bob's total bets:", sum(history["Bob"]["bets"]))
print("Bob's total gains:", sum(history["Bob"]["gains"]))


class HiLowBetting(BaseBettingStrategy):
    def __init__(self, betting_unit):
        self.betting_unit = betting_unit

    def declare_bet(self, cards_delt, remaining_cards):
        """ Cards 2 to 6 decrease the running count by 1, and cards 10 to A increase it by 1. """
        running_count = 0
        for card in ['10', 'J', 'Q', 'K', 'A']:
            running_count += cards_delt[card]
        for card in ['2', '3', '4', '5', '6']:
            running_count -= cards_delt[card]
        remaining_decks = sum(remaining_cards.values()) / 52
        true_count = running_count / remaining_decks
        return max(self.betting_unit, self.betting_unit * (true_count - 1))


betting_strategy = HiLowBetting(betting_unit=1)


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


playing_strategy = MyStrategy()

simulation = BlackjackSimulation(nb_decks=1,
                                 penetration=0.5,
                                 max_hands=3,
                                 double_after_split=True,
                                 hit_soft_17=True)

simulation.register_player("Bob", betting_strategy=betting_strategy, playing_strategy=playing_strategy)

history = simulation.run(nb_rounds=1, verbose=True)
