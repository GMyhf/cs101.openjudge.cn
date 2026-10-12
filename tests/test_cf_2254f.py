"""Anchor the large-input XOR invariant in an exhaustive operation oracle."""
import itertools
import unittest

from cf_oracles import reachable_2254f, signature_2254f


class WhiplashOracleTests(unittest.TestCase):
    def test_invariant_matches_exhaustive_operation_reachability(self):
        for start in ((0, 0), (1, 2), (1, 1), (0, 1, 2, 3), (1, 1, 2, 2), (1, 2, 4, 8)):
            reachable = reachable_2254f(start)
            alphabet = {value for row in reachable for value in row} | {16}
            signature = signature_2254f(start)
            predicted = {row for row in itertools.product(sorted(alphabet), repeat=len(start))
                         if signature_2254f(row) == signature}
            self.assertEqual(predicted, reachable, start)
