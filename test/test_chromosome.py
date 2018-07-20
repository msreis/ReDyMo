import unittest
import sys
sys.path.append('../')
from src.chromosome import Chromosome

# FIXME: Change Chromosome object construction to comply with new class
# arguments. 

## @package ReDyMo.test.test_chromosome
# Contains the Chromosome test class

## This class has tests for each Chromosome method.
# @see Chromosome
class TestChromosome(unittest.TestCase):

    ## Tests the construction of a Chromosome object.
    def test_constructor(self):
        chrm_1 = Chromosome(1, 3, [1, 0.7, 0.5], None)
        self.assertIsInstance(chrm_1, Chromosome)
        self.assertEqual(chrm_1.code, 1)
        self.assertEqual(chrm_1.length, 3)
        self.assertEqual(chrm_1.number_of_replicated_bases, 0)
        self.assertEqual(chrm_1.number_of_origins, 0)
        self.assertEqual(chrm_1.activation_probabilities, [1, 0.7, 0.5])

    ## Tests if by changing manually the replicated values the function returns
    # correctly that a base is replicated.
    def test_base_is_replicated(self):
        chrm_1 = Chromosome(1, 3, [1, 0.7, 0.5], None)
        chrm_2 = Chromosome(3, 2, [0.7, 0.5], None)
        chrm_2.strand = [1, 1]
        chrm_2.number_of_replicated_bases = 2
        self.assertFalse(chrm_1.base_is_replicated(0))
        self.assertFalse(chrm_1.base_is_replicated(1))
        self.assertFalse(chrm_1.base_is_replicated(2))
        self.assertTrue(chrm_2.base_is_replicated(0))
        self.assertTrue(chrm_2.base_is_replicated(1))

    ## Tests the function by manually changing the number of replicated bases
    # and checking what the function returns.
    def test_is_replicated(self):
        chrm_1 = Chromosome(1, 3, [1, 0.7, 0.5], None)
        chrm_2 = Chromosome(2, 2, [0.7, 0.5], None)
        chrm_2.strand = [1, 1]
        chrm_2.number_of_replicated_bases = 2
        chrm_1.strand = [0, 1, 1]
        chrm_1.number_of_replicated_bases = 2
        self.assertTrue(chrm_2.is_replicated())
        self.assertFalse(chrm_1.is_replicated())

    ## Tests by checking if the function return value is the same passed to 
    # the constructor.
    def test_activation_probability(self):
        chrm_1 = Chromosome(1, 3, [1, 0.7, 0.5], None)
        chrm_2 = Chromosome(2, 2, [0.4, 0.8], None)
        self.assertAlmostEqual(chrm_2.activation_probability(0), 0.4)
        self.assertAlmostEqual(chrm_2.activation_probability(1), 0.8)
        self.assertAlmostEqual(chrm_1.activation_probability(0), 1)
        self.assertAlmostEqual(chrm_1.activation_probability(1), 0.7)
        self.assertAlmostEqual(chrm_1.activation_probability(2), 0.5)

    ## Tests the replication of a range of bases and checks number of bases
    # replicated.
    def test_replicate(self):
        chrm_1 = Chromosome(1, 6, [1, 0.7, 0.5, 0.3, 0.8, 0.2], None)
        chrm_1.replicate(0, 4, 1)
        for i in range(6):
            if i in range(0, 5):
                self.assertNotEqual(chrm_1.strand[i], 0)
            else:
                self.assertEqual(chrm_1.strand[i], 0)
        self.assertEqual(chrm_1.number_of_replicated_bases, 5)
        chrm_1.replicate(4, 5, 1)
        self.assertEqual(chrm_1.length, chrm_1.number_of_replicated_bases)

    # Tests by comparing the sum of probabilities before and after applying
    # the function.
    def test_set_dormant_origin_activation_probability(self):
        chrm_size = 300000
        chrm_1 = Chromosome(1, chrm_size, [0.5] * chrm_size, None)
        chrm_2 = Chromosome(1, chrm_size, [0.9] * chrm_size, None)
        chrm_1.set_dormant_origin_activation_probability((int)((chrm_size - 1) / 2))
        chrm_2.set_dormant_origin_activation_probability((int)(chrm_size/9))
        self.assertGreater(sum(chrm_1.activation_probabilities, 0), chrm_size*0.5)
        self.assertLessEqual(sum(chrm_1.activation_probabilities, 0), chrm_size)
        self.assertGreater(sum(chrm_2.activation_probabilities, 0), chrm_size*0.9)
        self.assertLessEqual(sum(chrm_2.activation_probabilities, 0), chrm_size)


if __name__ == '__main__':
    unittest.main()
