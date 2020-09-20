from blackjack_engine.simulation import BlackjackSimulation

from blackjack_engine.strategy import RandomPlay
from blackjack_engine.strategy import ConstantBetting


if __name__ == '__main__':
    simulation = BlackjackSimulation(nb_decks=1,
                                     penetration=0.5,
                                     max_hands=3,
                                     double_after_split=True,
                                     hit_soft_17=True)

    simulation.register_player(name="Bob",
                               betting_strategy=ConstantBetting(),
                               playing_strategy=RandomPlay())

    simulation.register_player(name="Patrick",
                               betting_strategy=ConstantBetting(1),
                               playing_strategy=RandomPlay())

    history = simulation.run(nb_rounds=1000, verbose=True)
    print("Bob's total gains:", sum(history["Bob"]["gains"]))
    print("Patrick's total gains:", sum(history["Patrick"]["gains"]))
