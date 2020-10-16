The goal of this project is to provide a flexible Blackjack engine, allowing to easily define and evaluate custom strategies.

## Installation

```
pip install blackjack-engine
```

## Quickstart

```python
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
```

```
100%|----------| 100000/100000 [00:03<00:00, 26235.48it/s]
Bob's total bets: 134088
Bob's total gains: -43539.5
```

## Implementing custom strategies

### Betting strategy

The betting strategy of a player consists in choosing the amount of money to bet for the next hand, before the cards are delt. To chose his bet amount, the player has access to the set of cards that were delt since the last shuffing of the shoe, and to the set of remaining cards in the shoe. 

Below is an exemple showing how to implement the [Hi-Low](https://www.instructables.com/id/Card-Counting-and-Ranging-Bet-Sizes/) betting strategy.

```python
from blackjack_engine.strategy import BaseBettingStrategy


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
```

### Playing strategy

The playing strategy consists in choosing, during a player's turn, which action to pick among available actions. 

Below is an exemple of a playing strategy, in which the player chooses to always split his pairs of Aces, always double down on 11, and otherwise hit until reaching a hard 17+ or a soft 18+.

```python
from blackjack_engine.strategy import BasePlayingStrategy


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
```

## Simulating hands

Once the betting and playing strategies are defined, you can run a simulation as demonstrated in the [Quickstart](https://github.com/lzanini/blackjack-engine/blob/master/README.md#quickstart) section. Below are all the simulationparameters available:

```python
simulation = BlackjackSimulation(nb_decks=1,
                                 penetration=0.5,
                                 max_hands=3,
                                 double_after_split=True,
                                 hit_soft_17=True)

simulation.register_player("Bob",  
                           betting_strategy=betting_strategy, 
                           playing_strategy=playing_strategy)
                        
history = simulation.run(nb_rounds=1, verbose=True)
```

```
    ~~~~~~~  |  New Round  |  ~~~~~~~

Players' bets:
  Bob: 1

Dealer's hand: [8] + one card face down

--- Player's turn: Bob ---

Playing hand n°1: [4, 2]

  Available actions: ['stand', 'hit', 'double']
  Chosen action: hit
  Current hand: [4, 2, 7]

  Available actions: ['stand', 'hit']
  Chosen action: hit
  Current hand: [4, 2, 7, 3]

  Available actions: ['stand', 'hit']
  Chosen action: hit
  Final hand: [4, 2, 7, 3, 5]

--- Dealer's turn ---

  Returning face down card: [8, 2]

  Chosen Action: hit
  Current hand: [8, 2, Q]

  Chosen Action: stand
  Final hand: [8, 2, Q]

--- Evaluation phase ---

  Player: Bob
    (bet=1) [4, 2, 7, 3, 5] vs dealer's [8, 2, Q] -> gains=1
  Total gains of Bob: 1
```
