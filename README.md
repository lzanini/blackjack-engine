The goal of this project is to provide a flexible Blackjack engine in Python, allowing to easily define and evaluate custom strategies.

## Installation

```
pip install blackjack-engine
```

## Quickstart

```python
from blackjack_engine.simulation import BlackjackSimulation
from blackjack_engine.strategy import RandomPlay
from blackjack_engine.strategy import ConstantBetting

simulation = BlackjackSimulation(nb_decks=4, penetration=0.5)
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

The betting strategy of a player consists in choosing the amount of money to bet for the next hand, before the cards are delt. Here is an exemple showing how to implement the [Hi-Low](https://www.instructables.com/id/Card-Counting-and-Ranging-Bet-Sizes/) betting strategy.

```python
from blackjack_engine.strategy import BaseBettingStrategy


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
```

Note that to chose his bet amount, the player has access to the set of cards that were delt since the last shuffing of the shoe, and therefore to the set of remaining cards in the shoe.

### Playing strategy

The playing strategy consists in choosing, during a player's turn, which action to pick among all actions available. Here is an exemple of a playing strategy, in which the player chooses to always split his pairs of Aces, always double down on 11, and otherwise hit until reaching a hard 17+ or a soft 18+.

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

Once the betting and playing strategies are defined, one can run a simulation as demonstrated in the [Quickstart](https://github.com/lzanini/blackjack-engine/blob/master/README.md#quickstart) section. Below are all the parameters available at the moment when running a simulation:

```python
simulation = BlackjackSimulation(nb_decks=1,
                                 penetration=0.5,
                                 max_hands=3,
                                 double_after_split=True,
                                 hit_soft_17=True)

simulation.register_player("Bob",  betting_strategy=betting_strategy, playing_strategy=playing_strategy)
                        
history = simulation.run(nb_rounds=1, verbose=True)
```

```

    ~~~~~~~  |  New Round  |  ~~~~~~~

Players' bets:
  Bob: 1

Dealer's hand: [K] + one card face down

--- Player's turn: Bob ---

Playing hand n°1: [7, 7]

  Available actions: ['stand', 'hit', 'double', 'split']
  Chosen action: split
  New hands: [[7, 5], [7, 3]]
  Current hand: [7, 5]

  Available actions: ['stand', 'hit', 'double']
  Chosen action: double
  Final hand: [7, 5, 8]

Playing hand n°2: [7, 3]

  Available actions: ['stand', 'hit', 'double']
  Chosen action: stand
  Final hand: [7, 3]

--- Dealer's turn ---

  Returning card face down: [K, 6]

  Chosen Action: hit
  Current hand: [K, 6, Q]

  Chosen Action: stand
  Final hand: [K, 6, Q]

--- Evaluation phase ---

  Player: Bob
    (bet=2) [7, 5, 8] vs dealer's [K, 6, Q] -> gains=2
    (bet=1) [7, 3] vs dealer's [K, 6, Q] -> gains=1
  Total gains of Bob: 3
  
```
