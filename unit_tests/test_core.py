import unittest

from leadsheets.core import (
    get_contact_scores, get_normalized_scores, label, get_labeled_scores)


class TestCore(unittest.TestCase):
    def test_get_contact_scores(self):
        self.assertEqual(get_contact_scores([(1, 'web', 1)]), [(1, 1)])
        self.assertEqual(get_contact_scores([(1, 'email', 1)]), [(1, 1.2)])
        self.assertEqual(get_contact_scores([(1, 'social', 1)]), [(1, 1.5)])
        self.assertEqual(get_contact_scores([(1, 'webinar', 1)]), [(1, 2)])
        self.assertEqual(get_contact_scores([(1, 'web', 1), (1, 'web', 2)]), [(1, 3)])
        self.assertEqual(get_contact_scores(
            [(1, 'web', 1), (1, 'webinar', 1), (1, 'email', 1), (1, 'social', 1)]),
            [(1, 1 + 1.2 + 1.5 + 2)]
        )

    def test_get_normalized_scores(self):
        self.assertEqual(get_normalized_scores([(1, 5)]), [(1, 0)])
        self.assertEqual(get_normalized_scores([(1, 5), (2, 10)]), [(1, 0), (2, 100)])
        self.assertEqual(get_normalized_scores(
            [(1, 0), (2, 50), (3, 100)]), [(1, 0), (2, 50), (3, 100)]
        )
        self.assertEqual(get_normalized_scores(
            [(1, 50), (2, 50), (3, 100)]), [(1, 0), (2, 0), (3, 100)]
        )
        self.assertEqual(get_normalized_scores(
            [(1, 100), (2, 150), (3, 300)]), [(1, 0), (2, 25), (3, 100)]
        )

    def test_label(self):
        self.assertEqual(label(0), 'bronze')
        self.assertEqual(label(25), 'silver')
        self.assertEqual(label(50), 'gold')
        self.assertEqual(label(75), 'platinum')
        self.assertEqual(label(100), 'platinum')

    def test_get_labeled_scores(self):
        self.assertEqual(get_labeled_scores(
            [(1, 10), (2, 50)]), [(1, 'bronze', 10), (2, 'gold', 50)]
        )
