
card_values = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
               '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}


class Hand:
    """

    This class represents a set of cards hold by the player or the dealer.

    Attributes
    ----------

        cards: list of string
            Set of cards hold by the player / dealer.

        nb_hands: int
            How many hands in total the owner of the hand has. (1 if it is the dealer's hand)
            This is used to evaluate the value of the hand :for instance A + 10 after a split is not a blackjack.

        value: int
            Value of the hand.

        is_soft: bool
            Whether the hand is soft (contains an Ace valued 11) or not.

        bet: float
            Amount of money bet on the hand (None if it is a dealer's hand)

    """
    def __init__(self, cards, bet=None, nb_hands=1):
        self.cards = cards
        self.nb_hands = nb_hands
        self.value, self.is_soft = self.compute_value()
        self.bet = bet

    def add_card(self, card):
        self.cards.append(card)
        self.value, self.is_soft = self.compute_value()

    def compute_value(self):
        value = sum([card_values[card] for card in self.cards])
        soft_aces = self.cards.count('A')
        while value > 21 and soft_aces > 0:
            value -= 10
            soft_aces -= 1
        is_soft = soft_aces > 0
        return value, is_soft

    @property
    def is_blackjack(self):
        return (self.nb_hands == 1) and (len(self.cards) == 2) and (self.value == 21)

    @property
    def is_pair(self):
        return len(self.cards) == 2 and (self.cards[0] == self.cards[1])

    @property
    def is_busted(self):
        return self.value > 21

    @property
    def visible_card(self):
        """ If it is the dealer's hand: only his first card is observable during the player's turn. """
        return self.cards[0]

    def __repr__(self):
        string = f"[{', '.join(self.cards)}]"
        return string
