import numpy as np


class Shoe:
    """

    This class represents the set of cards used during a blackjack game.

    Parameters
    ----------

        nb_decks: int
            number of 52-cards decks used.

        penetration: float, between 0 and 1
            fraction of the decks dealt before re-shuffling.

    Attributes
    ----------

        cards_order: array of size (nb_decks * 52,)
            Order of the cards in the shoe.

        remaining_cards: dict<str, int>
            Number of cards remaining for each value (Ace, 2, ...)

        delt_cards: dict<str, int>
            Number of cards delt for each value (Ace, 2, ...)

        max_cards_delt: int
            Maximum number of cards to deal before re-shuffling the deck.

        nb_cards_delt: int
            Number of cards delt since the last shuffling of the shoe.

        nb_decks: int
            Number of decks used in the shoe.

    """

    cards_names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, nb_decks, penetration):
        assert 0 <= penetration <= 1, "penetration must be between 0 and 1."
        self.cards = np.repeat(np.arange(13), 4 * nb_decks)
        self.cards_order = np.random.permutation(self.cards.shape[0])
        self.remaining_cards = {i: 4 * nb_decks for i in self.cards_names}
        self.delt_cards = {i: 0 for i in self.cards_names}
        self.max_cards_delt = penetration * len(self.cards)
        self.nb_cards_delt = 0
        self.nb_decks = nb_decks

    def deal_card(self):
        """

        Deal a card from the shoe.

        Returns
        -------

            card: string
                Card among ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        """
        if self.nb_cards_delt >= len(self.cards_order):
            self.shuffle()
        card_idx = self.cards[self.cards_order[self.nb_cards_delt]]
        self.remaining_cards[self.cards_names[card_idx]] -= 1
        self.delt_cards[self.cards_names[card_idx]] += 1
        self.nb_cards_delt += 1
        return self.cards_names[card_idx]

    def shuffle(self):
        """ Re-shuffle all cards into the shoe. """
        self.remaining_cards = {i: 4 * self.nb_decks for i in self.cards_names}
        self.delt_cards = {i: 0 for i in self.cards_names}
        self.cards_order = np.random.permutation(self.cards.shape[0])
        self.nb_cards_delt = 0

    def needs_shuffling(self):
        """ Whether the shoe needs to be shuffled. """
        return self.nb_cards_delt >= self.max_cards_delt
