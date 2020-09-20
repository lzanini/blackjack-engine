from blackjack_engine.simulation import BlackjackSimulation
from blackjack_engine.strategy import RandomPlay
from blackjack_engine.strategy import ConstantBetting
from blackjack_engine.strategy import BaseBettingStrategy
from blackjack_engine.strategy import BasePlayingStrategy


simulation = BlackjackSimulation(nb_decks=4, penetration=0.5)
simulation.register_player(name="Bob",
                           betting_strategy=ConstantBetting(),
                           playing_strategy=RandomPlay())

history = simulation.run(nb_rounds=100_000)
print("Bob's total bets:", sum(history["Bob"]["bets"]))
print("Bob's total gains:", sum(history["Bob"]["gains"]))


class HiLowBetting(BaseBettingStrategy):
    def __init__(self, betting_unit, max_spread):
        self.betting_unit = betting_unit
        self.max_spread = max_spread

    def declare_bet(self, cards_delt, remaining_cards):
        # cards_delt[0] countains the number of delt Aces, cards_delt[1] the number of 2's
        # ...and cards_delt[12] the number of Kings.
        remaining_decks = sum(remaining_cards) / 52
        running_count = sum(cards_delt[1:6]) - sum(cards_delt[9:]) - cards_delt[0]
        true_count = running_count / remaining_decks
        if true_count >= 2:
            return min(self.betting_unit * self.max_spread, self.betting_unit * (true_count - 1))
        return self.betting_unit


betting_strategy = HiLowBetting(betting_unit=1, max_spread=5)


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
