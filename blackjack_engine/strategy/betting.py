from abc import ABC, abstractmethod

import numpy as np


class BaseBettingStrategy(ABC):
    """

    Abstract class representing the player's betting strategy, from which other strategies must derive.

    Betting strategies must implement the abstact method 'declare_bet', which takes as arguments
    some information about the game (cards delt, remaining cards) and returns the player's bet for the turn.

    """
    @abstractmethod
    def declare_bet(self, cards_delt, remaining_cards):
        pass


class ConstantBetting(BaseBettingStrategy):
    """
    The player bets a constant amount.
    """
    def __init__(self, betting_unit=1):
        self.betting_unit = betting_unit

    def declare_bet(self, cards_delt, remaining_cards):
        return self.betting_unit


class HiLowBetting(BaseBettingStrategy):
    """

    The player bets according to the hi-low true count of the shoe, with a given spread.

    Source: https://www.instructables.com/id/Card-Counting-and-Ranging-Bet-Sizes/

    """
    def __init__(self, betting_unit=1, max_spread=10):
        self.betting_unit = betting_unit
        self.max_spread = max_spread

    def declare_bet(self, cards_delt, remaining_cards):
        remaining_decks = np.sum(remaining_cards) / 52
        running_count = cards_delt[1:6].sum() - cards_delt[0] - cards_delt[9:].sum()
        true_count = running_count / remaining_decks
        if true_count >= 2:
            return min(self.betting_unit * self.max_spread, self.betting_unit * (true_count - 1))
        else:
            return self.betting_unit
