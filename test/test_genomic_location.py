import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock
import sys
sys.path.append('../')
from src.genome import Genome
from src.chromosome import Chromosome
from src.genomic_location import GenomicLocation

## @package ReDyMo.test.test_genomic_location
# Contains the Genomic Location test class

## This class has tests for each Genomic Location method.
# @see Genomic Location
class TestGenomicLocation(unittest.TestCase):

    ## Tests the constructor by comparing the input with the objects generated.
    def test_constructor(self):
        chrms = [Chromosome(1, 3, [0.5, 1, 0.4], None),
                 Chromosome(3, 2, [0.0, 0.4], None)]

        gen_loc_1 = GenomicLocation(2, chrms[0])
        gen_loc_2 = GenomicLocation(2, chrms[1])
        gen_loc_3 = GenomicLocation(3, chrms[1])

        self.assertEqual(gen_loc_1.base, 2)
        self.assertEqual(gen_loc_3.base, 3)
        self.assertEqual(gen_loc_2.chromosome, chrms[1])
        self.assertEqual(gen_loc_1.chromosome, chrms[0])

    ## Tests by comparing the mock value with the function response.
    def test_is_replicated(self):
        chrms = [Chromosome(1, 3, [0.5, 1, 0.4], None),
                 Chromosome(3, 2, [0.0, 0.4], None)]

        chrms[0].base_is_replicated = MagicMock(return_value=False)
        chrms[1].base_is_replicated = MagicMock(return_value=True)

        gen_loc_1 = GenomicLocation(2, chrms[0])
        gen_loc_2 = GenomicLocation(2, chrms[1])

        self.assertTrue(gen_loc_2.is_replicated())
        self.assertFalse(gen_loc_1.is_replicated())

        chrms[0].base_is_replicated = MagicMock(return_value=True)

        self.assertTrue(gen_loc_1.is_replicated())
        self.assertTrue(gen_loc_2.is_replicated())

    ## Tests by comaparing the proportion of times the function returns true
    # with the probability to return true. 
    def test_will_activate(self):
        chrms = [Chromosome(1, 3, [0.5, 1, 0.4], None),
                 Chromosome(3, 2, [0.0, 0.4], None)]

        chrms[0].base_is_replicated = MagicMock(return_value=False)
        chrms[1].base_is_replicated = MagicMock(return_value=True)

        gen_loc_1 = GenomicLocation(1, chrms[0])
        gen_loc_2 = GenomicLocation(1, chrms[1])
        gen_loc_3 = GenomicLocation(0, chrms[1])
        pass

        times_true = 0
        for i in range(50000):
            self.assertTrue(gen_loc_1.will_activate())
            self.assertFalse(gen_loc_3.will_activate())
            if gen_loc_2.will_activate():
                times_true += 1
        
        # Compares the number of times it was activated with its activation
        # probability.
        self.assertAlmostEqual(times_true/50000, 0.4, 2)

if __name__ == '__main__':
    unittest.main()
