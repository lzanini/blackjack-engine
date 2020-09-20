

class BlackJackRules:
    """

    https://en.wikipedia.org/wiki/Blackjack

    Fixed rules:
        * An Ace + 10 after a split is not considered a blackjack.
        * After spliting Aces, a single card is delt on each Ace.

    Implementation details:
        * the 'split' action consist in spliting + getting a card delt for the two new hands.

    Attributes
    ----------

        max_hands: int
            maximum number of hands a player is allowed to have during a single turn.

        double_after_split: bool
            Whether the player is allowed to double down on split hands.

        hit_soft_17: bool
            If True, the dealer hits on a soft 17 hand (i.e. a with an Ace valued 11).

    """
    def __init__(self, max_hands=4, double_after_split=True, hit_soft_17=True):
        self.max_hands = max_hands
        self.double_after_split = double_after_split
        self.hit_soft_17 = hit_soft_17

    def dealer_action(self, dealer_hand):
        """

        Action chosen by the dealer, given his current hand.

        Returns
        -------

            action: str
                Dealer's action, among ['hit', 'stand']

        """
        if dealer_hand.value < 17:
            return 'hit'
        elif self.hit_soft_17 and dealer_hand.is_soft and dealer_hand.value == 17:
            return 'hit'
        else:
            return 'stand'

    def available_actions(self, player_hand, last_action):
        """

        Subset of ['hit', 'stand', 'double', 'split']

        Parameters
        ----------

            player_hand: Hand
                player's current hand.

            last_action: int or None
                last action of the player on the current hand.
                None if it's his first action.

        """
        value = player_hand.value
        if value >= 21 or last_action in ['stand', 'double']:
            # After busting / standing / doubling down, no action is allowed
            available_actions = []
        elif player_hand.nb_hands > 1 and player_hand.cards[0] == 0:
            # After splitting aces, a single card is delt for each ace and no other action is allowed
            available_actions = []
        else:
            # not busted, previously split or hit.
            available_actions = ['stand', 'hit']
            if len(player_hand.cards) == 2 and (player_hand.nb_hands == 1 or self.double_after_split):
                # if the player holds 2 cards and didn't split / double after split is allowed: double down is allowed
                available_actions.append('double')
            if player_hand.is_pair and player_hand.nb_hands < self.max_hands:
                # if the hand is a pair & didn't split too many times: split is allowed
                available_actions.append('split')
        return available_actions

    @staticmethod
    def evaluate_hand(player_hand, dealer_hand):
        """

        Compute the player's gains given his hand and the dealer's hand.

        Parameters
        ----------

            player_hand: Hand
                cards hold by the player.

            dealer_hand: Hand
                cards hold by the dealer

        Return
        ------

            gains: float
             The player's gains for a unit bet. (negative in case of a loss)

        """
        if player_hand.is_busted:
            # the player is busted
            return -1
        elif player_hand.is_blackjack:
            if dealer_hand.is_blackjack:
                # the player and the dealer both have a blackjack
                return 0
            else:
                # the player has a blackjack and the dealer doesn't
                return 1.5
        else:
            if dealer_hand.value > 21:
                # the dealer is busted and the player not, and the player doesn't have a blackjack
                return 1
            elif dealer_hand.is_blackjack:
                # the dealer has a blackjack and the player don't
                return -1
            else:
                if player_hand.value > dealer_hand.value:
                    # the player has a higher score than the dealer
                    return 1
                elif player_hand.value < dealer_hand.value:
                    # the dealer has a higher score than the player
                    return -1
                else:
                    # the player and the dealer have the same score
                    return 0
