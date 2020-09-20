from abc import ABC, abstractmethod
import random


class BasePlayingStrategy(ABC):
    """

    Abstract class representing the player's strategy, from which other strategies must derive.

    Playing strategies must implement the abstact method 'declare_action', which takes as arguments some information
    about the game (player hand, dealer card, remaining cards and available actions) and returns the player's action.

    """
    @abstractmethod
    def declare_action(self, player_hand, dealer_card, remaining_cards, available_actions):
        return 'stand'


class RandomPlay(BasePlayingStrategy):
    """
    This strategy returns a random available action.
    """
    def declare_action(self, player_hand, dealer_card, remaining_cards, available_actions):
        return random.choice(available_actions)


class BasicStrategy(BasePlayingStrategy):
    """

    Implementation of the basic strategy, which is the optimal strategy assuming that the probability of
    each card of beaing delt is the same.

    Source: https://www.blackjackapprenticeship.com/blackjack-strategy-charts/

    """
    def __init__(self, double_after_split=True):
        self.double_after_split = double_after_split

    def declare_action(self, player_hand, dealer_card, remaining_cards, available_actions):

        # 3rd table: split or not
        if 'split' in available_actions:
            player_card = player_hand.cards[0]

            if player_card in [0, 7]:
                return 'split'

            elif player_card == 8 and dealer_card in [1, 2, 3, 4, 5, 7, 8]:
                return 'split'

            elif player_card == 6 and dealer_card in [1, 2, 3, 4, 5, 6]:
                return 'split'

            elif player_card == 5:
                if self.double_after_split and dealer_card == 1:
                    return 'split'
                elif dealer_card in [2, 3, 4, 5]:
                    return 'split'

            elif player_card == 3 and self.double_after_split and dealer_card in [4, 5]:
                return 'split'

            elif player_card in [1, 2] and dealer_card in [1, 2, 3, 4, 5, 6]:
                if self.double_after_split or dealer_card >= 3:
                    return 'split'

        # 1st table: hard hands
        can_double = 'double' in available_actions
        if not player_hand.is_soft:
            
            if player_hand.value >= 17:
                return 'stand'
            
            elif player_hand.value >= 13 and dealer_card in [1, 2, 3, 4, 5]:
                return 'stand'
            
            elif player_hand.value == 12 and dealer_card in [3, 4, 5]:
                return 'stand'
            
            elif can_double and player_hand.value == 11:
                return 'double'
            
            elif can_double and player_hand.value == 10 and dealer_card not in [0, 9, 10, 11, 12]:
                return 'double'
            
            elif can_double and player_hand.value == 9 and dealer_card in [2, 3, 4, 5]:
                return 'double'
            return 'hit'

        # 2nd table: soft hands
        else:
            
            if player_hand.value == 20:
                return 'stand'
            elif player_hand.value == 19:
                if can_double and dealer_card == 5:
                    return 'double'
                else:
                    return 'stand'
                
            elif player_hand.value == 18:
                if dealer_card in [1, 2, 3, 4, 5] and can_double:
                    return 'double'
                elif dealer_card in [8, 9, 10, 11, 12, 0]:
                    return 'hit'
                return 'stand'
                
            elif player_hand.value == 17 and dealer_card in [2, 3, 4, 5]:
                if can_double:
                    return 'double'
                return 'hit'
                
            elif player_hand.value in [15, 16] and dealer_card in [3, 4, 5]:
                if can_double:
                    return 'double'
                return 'hit'
                
            elif player_hand.value in [13, 14] and dealer_card in [4, 5]:
                if can_double:
                    return 'double'
                return 'hit'
                
            else:
                return 'hit'
