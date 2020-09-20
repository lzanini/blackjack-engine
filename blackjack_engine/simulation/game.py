
from tqdm import trange

from blackjack_engine.strategy import BasePlayingStrategy
from blackjack_engine.strategy import BaseBettingStrategy

from blackjack_engine.simulation.shoe import Shoe
from blackjack_engine.simulation.rules import BlackJackRules
from blackjack_engine.simulation.hand import Hand


class Player:
    """

    A player is defined by its betting strategy and his playing strategy.

    Attributes
    ----------

        betting strategy: instance of AbstractBettingStrategy
            Computes the bet amount before starting a hand.

        playing_strategy: instance of AbstractPlayingStrategy
            Computes the action taken by the player.

        hands: list of Hand.
            List of hands of a given player (more than one if the player split his first hand)

    """
    def __init__(self, betting_strategy, playing_strategy):
        assert isinstance(betting_strategy, BaseBettingStrategy)
        assert isinstance(playing_strategy, BasePlayingStrategy)
        self.betting_strategy = betting_strategy
        self.playing_strategy = playing_strategy
        self.hands = []

    def declare_bet(self, cards_delt, remaining_cards):
        return self.betting_strategy.declare_bet(cards_delt, remaining_cards)

    def declare_action(self, hand_idx, dealer_card, remaining_cards, available_actions):
        player_hand = self.hands[hand_idx]
        return self.playing_strategy.declare_action(player_hand, dealer_card, remaining_cards, available_actions)


class BlackjackSimulation:
    """

    Attributes
    ----------

        shoe: Shoe
            Set of cards in play.

        players: list of Player
            Set of players.

        dealer_hand: Hand
            Dealer's hand.

        game_rules: BlackJackRules
            Defines the rules of the game.

        players_history: list of dict
            Bets and earnings history of each player

    Parameters
    ----------

        nb_decks: int
            Number of decks in the shoe.

        penetration: float, between 0 and 1.
            Proportion of the shoe to play before re-shuffling.

        max_hands: int
            Maximum number of hands allowed for one player. For instance, if max_hands=2,
            players can only split their hand once.

        double_after_split: bool
            If True, the player is allowed to double after splitting his hand.

        hit_soft_17: bool
            If True, the dealer hits when holding a soft 17.

    """
    def __init__(self, nb_decks=4, penetration=0.75, max_hands=3, double_after_split=True, hit_soft_17=True):
        self.game_rules = BlackJackRules(max_hands, double_after_split, hit_soft_17)
        self.shoe = Shoe(nb_decks=nb_decks, penetration=penetration)
        self.dealer_hand = Hand([])
        self.players = {}
        self.players_history = {}
        self.verbose = False

    def register_player(self, name, betting_strategy, playing_strategy):
        """ Adds a new player to the table. """
        player = Player(betting_strategy, playing_strategy)
        self.players[name] = player
        self.players_history[name] = {'bets': [], 'gains': []}

    def run(self, nb_rounds, verbose=False):
        """ Runs the simulation for a specified number of hands. """
        self.verbose = verbose
        self.shoe.shuffle()
        _range = range if verbose else trange
        for _ in _range(nb_rounds):
            self.play_round()
        return self.players_history

    def play_round(self):
        self.info("~~~~~~~  |  New Round  |  ~~~~~~~", newlines=3, tabs=2)
        bets = self.betting_round()
        self.info("Players' bets:", newlines=1)
        for name, bet in bets.items():
            pass
            self.info(name, ": ", bet, tabs=1)
        self.deal_cards(bets)
        self.info(f"Dealer's hand: [{self.dealer_hand.cards[0]}] + one card face down", newlines=1)
        for name, player in self.players.items():
            self.player_turn(name, player)
        self.dealer_turn()
        self.evaluate_gains()
        if self.shoe.needs_shuffling():
            self.info('Reshuffling the shoe.', newlines=1)
            self.shoe.shuffle()

    def betting_round(self):
        bets = {}
        for name, player in self.players.items():
            bets[name] = player.declare_bet(self.shoe.delt_cards, self.shoe.remaining_cards)
        return bets

    def deal_cards(self, bets):
        for name, player in self.players.items():
            player.hands = [
                Hand(
                    cards=[self.shoe.deal_card(), self.shoe.deal_card()],
                    bet=bets[name])
            ]
        self.dealer_hand = Hand(cards=[self.shoe.deal_card(), self.shoe.deal_card()])

    def player_turn(self, name, player):
        self.info("--- Player's turn: ", name, " ---", newlines=1)
        dealer_card = self.dealer_hand.visible_card
        remaining_cards = self.shoe.remaining_cards
        hand_idx = 0

        while hand_idx < len(player.hands):

            action = None
            player_hand = player.hands[hand_idx]
            nb_hands = len(player.hands)
            available_actions = self.game_rules.available_actions(player_hand, action)

            self.info('Playing hand n°', hand_idx+1, ": ", player_hand, newlines=1)
            self.info('Available actions: ', available_actions, newlines=1, tabs=1)

            while available_actions:

                action = player.declare_action(hand_idx, dealer_card, remaining_cards, available_actions)
                self.info('Chosen action: ', action, tabs=1)
                assert action in available_actions

                if action == 'hit':
                    # hit -> add a card to the hand
                    player_hand.add_card(self.shoe.deal_card())

                elif action == 'double':
                    # double -> double bet amount & deal a card
                    player_hand.bet *= 2
                    player_hand.add_card(self.shoe.deal_card())

                elif action == 'split':
                    # split -> create 2 new hands and deal one card for each.
                    card = player_hand.cards[0]
                    bet = player_hand.bet
                    player_hand = Hand(cards=[card, self.shoe.deal_card()], bet=bet, nb_hands=nb_hands+1)
                    new_player_hand = Hand(cards=[card, self.shoe.deal_card()], bet=bet, nb_hands=nb_hands+1)
                    player.hands[hand_idx] = player_hand
                    player.hands.insert(hand_idx+1, new_player_hand)
                    self.info("New hands: ", player.hands, tabs=1)

                nb_hands = len(player.hands)
                available_actions = self.game_rules.available_actions(player_hand, action)
                if available_actions:
                    self.info('Current hand: ', player_hand, tabs=1)
                    self.info('Available actions: ', available_actions, newlines=1, tabs=1)
                else:
                    self.info('Final hand: ', player_hand, tabs=1)
            hand_idx += 1

    def dealer_turn(self):
        self.info("--- Dealer's turn ---", newlines=1)
        self.info("Returning face down card: ", self.dealer_hand, newlines=1, tabs=1)
        action = None
        while action != 'stand':
            action = self.game_rules.dealer_action(self.dealer_hand)
            self.info('Chosen Action: ', action, newlines=1, tabs=1)
            if action == 'hit':
                self.dealer_hand.add_card(self.shoe.deal_card())
                self.info('Current hand: ', self.dealer_hand, tabs=1)
            else:
                self.info('Final hand: ', self.dealer_hand, tabs=1)

    def evaluate_gains(self):
        self.info("--- Evaluation phase ---", newlines=1)
        for name, player in self.players.items():
            self.info('Player: ', name, newlines=1, tabs=1)
            bet, gains = self.evaluate_hands(player.hands)
            self.players_history[name]["bets"].append(bet)
            self.players_history[name]["gains"].append(gains)
            self.info('Total gains of ', name,  ": ", gains, tabs=1)

    def evaluate_hands(self, player_hands):
        """

        Compute the total gains for all hands hold by one player.

        Parameters
        ----------

            player_hands: list of Hand
                cards hold by the player.

        """
        player_gains, player_bet = 0, 0
        for player_hand in player_hands:
            gains = player_hand.bet * self.game_rules.evaluate_hand(player_hand, self.dealer_hand)
            player_bet += player_hand.bet
            player_gains += gains
            self.info("(bet=", player_hand.bet, ") ", player_hand, " vs dealer's ",
                      self.dealer_hand, " -> gains=", gains, tabs=2)
        return player_bet, player_gains

    def info(self, *messages, newlines=0, tabs=0):
        if self.verbose:
            # the message is reconstructed here to avoid string operations when self.verbose=False
            message = ''.join([str(m) for m in messages])
            print(newlines * '\n' + tabs * '  ' + message)
