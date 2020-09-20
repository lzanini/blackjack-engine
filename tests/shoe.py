import unittest
import numpy as np

from blackjack_engine.simulation.shoe import Shoe


class TestShoe(unittest.TestCase):

    def setUp(self):
        self.shoe = Shoe(nb_decks=1, penetration=0.5)

    def test_drawn(self):
        for _ in range(20):
            card = self.shoe.deal_card()
            self.assertIn(card, range(13))

    def test_remaining_cards(self):
        for _ in range(20):
            nb_cards = np.sum(self.shoe.remaining_cards)
            self.shoe.deal_card()
            self.assertEqual(nb_cards-1, np.sum(self.shoe.remaining_cards))

    def test_drawn_cards(self):
        for _ in range(20):
            nb_cards_drawn = np.sum(self.shoe.delt_cards)
            self.shoe.deal_card()
            self.assertEqual(nb_cards_drawn + 1, np.sum(self.shoe.delt_cards))

    def test_shuffle(self):
        order = self.shoe.cards_order.copy()
        self.shoe.shuffle()
        self.assertFalse(np.all(order == self.shoe.cards_order))


if __name__ == '__main__':
    unittest.main()
