import unittest
from src.chromosome import Chromosome

class TestChromosome(unittest.TestCase):

    # Tests the construction of a Chromosome object
    def test_construction(self):
        a = Chromosome(1, 3, [1, 0.7, 0.5], None)
        self.assertIsInstance(a, Chromosome)
        self.assertEqual(a.code, 1)
        self.assertEqual(a.length, 3)
        self.assertEqual(a.number_of_replicated_bases, 0)
        self.assertEqual(a.number_of_origins, 0)
        self.assertEqual(a.activation_probabilities, [1, 0.7, 0.5])

    # Tests if by changing manually the replicated values the function returns
    # correctly that a base is replicated
    def test_base_is_replicated(self):
        a = Chromosome(1, 3, [1, 0.7, 0.5], None)
        b = Chromosome(2, 2, [0.7, 0.5], None)
        b.strand = [1, 1]
        b.number_of_replicated_bases = 2
        self.assertFalse(a.base_is_replicated(0))
        self.assertFalse(a.base_is_replicated(1))
        self.assertFalse(a.base_is_replicated(2))
        self.assertTrue(b.base_is_replicated(0))
        self.assertTrue(b.base_is_replicated(1))

    # Tests the function by manually changing the number of replicated bases
    #  and checking what the functon returns
    def test_is_replicated(self):
        a = Chromosome(1, 3, [1, 0.7, 0.5], None)
        b = Chromosome(2, 2, [0.7, 0.5], None)
        b.strand = [1, 1]
        b.number_of_replicated_bases = 2
        a.strand = [0, 1, 1]
        a.number_of_replicated_bases = 2
        self.assertTrue(b.is_replicated())
        self.assertFalse(a.is_replicated())

    # Tests by checking if the function response is the same passed to the
    # constructor
    def test_activation_probability(self):
        a = Chromosome(1, 3, [1, 0.7, 0.5], None)
        b = Chromosome(2, 2, [0.4, 0.8], None)
        self.assertAlmostEqual(b.activation_probability(0), 0.4)
        self.assertAlmostEqual(b.activation_probability(1), 0.8)
        self.assertAlmostEqual(a.activation_probability(0), 1)
        self.assertAlmostEqual(a.activation_probability(1), 0.7)
        self.assertAlmostEqual(a.activation_probability(2), 0.5)

    def test_replicate(self):
        a = Chromosome(1, 6, [1, 0.7, 0.5, 0.3, 0.8, 0.2], None)
        a.replicate(0, 4, 1)
        for i in range(6):
            if i in range(0, 5):
                self.assertNotEqual(a.strand[i], 0)
            else:
                self.assertEqual(a.strand[i], 0)
        self.assertEqual(a.number_of_replicated_bases, 5)
        a.replicate(4, 5, 1)
        self.assertEqual(a.length, a.number_of_replicated_bases)

    def test_set_dormant_origin_activation_probability(self):
        n = 300000
        a = Chromosome(1, n, [0.5] * n, None)
        a.set_dormant_origin_activation_probability((int)((n - 1) / 2))
        print(sum(a.activation_probabilities, 0))
        self.assertGreater(sum(a.activation_probabilities, 0), n*0.5)


if __name__ == '__main__':
    unittest.main()
