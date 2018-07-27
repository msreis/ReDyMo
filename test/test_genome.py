import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock
import sys
sys.path.append('../')
from src.genome import Genome
from src.chromosome import Chromosome
from src.genomic_location import GenomicLocation


## @package ReDyMo.test.test_genome
# Contains the Genome test class

## This class has tests for each Genome method.
# @see Genome
class TestGenome(unittest.TestCase):

    ## Tests the constructor by creating a new object and comparing the setted
    # values with the given ones
    def test_constructor(self):
        chrms = [Chromosome(1, 3, [0.2, 0.5, 0.6], None, constitutive_origins=None),
                 Chromosome(3, 2, [0.1, 0.9], None, constitutive_origins=None)]
        gen = Genome(chrms)
        self.assertEqual(gen.chromosomes, chrms)

    ## Tests if the random_genomic_location stays within the chromosomes' area.
    def test_random_genomic_location(self):
        times = 500
        chrms = [Chromosome(1, 3, [0.2, 0.5, 0.6], None, constitutive_origins=None),
                 Chromosome(3, 2, [0.1, 0.9], None, constitutive_origins=None)]
        gen = Genome(chrms)
        for i in range(times):
            gen_loc = gen.random_genomic_location()
            self.assertTrue(gen_loc.chromosome in chrms)
            self.assertLess(gen_loc.base, len(gen_loc.chromosome))
            self.assertGreaterEqual(gen_loc.base, 0)

    ## Tests if the is_replicated returns true in true cases and vce versa.
    def test_is_replicated(self):
        chrms = [Chromosome(1, 3, [0.2, 0.5, 0.6], None, constitutive_origins=None),
                 Chromosome(3, 2, [0.1, 0.9], None, constitutive_origins=None)]
        chrms[0].is_replicated = MagicMock(return_value=True)
        chrms[1].is_replicated = MagicMock(return_value=False)
        gen = Genome(chrms)
        self.assertFalse(gen.is_replicated())
        chrms[1].is_replicated = MagicMock(return_value=True)
        self.assertTrue(gen.is_replicated())

    ## Tests if the function calculates accurately the distance between the
    # origins
    def test_average_interorigin_distance(self):
        chrm_1 = Mock(number_of_origins=24)
        chrm_2 = Mock(number_of_origins=30)
        chrm_1.__len__ = MagicMock(return_value=255)
        chrm_2.__len__ = MagicMock(return_value=236)
        gen = Genome([chrm_1, chrm_2])

        self.assertEqual((255 + 236) / (24 + 1 + 30 + 1),
                         gen.average_interorigin_distance())

    ## Tests by sending values manually and comparing the returned ones.
    def test_number_of_replicated_bases_in_this_step(self):
        chrms = [Mock(number_of_recently_replicated_bases=200),
                 Mock(number_of_recently_replicated_bases=195),
                 Mock(number_of_recently_replicated_bases=255)
                 ]
        gen = Genome(chrms)
        self.assertEqual(200+195+255,
                         gen.number_of_replicated_bases_in_this_step())
        chrms[0] = Mock(number_of_recently_replicated_bases=2)
        chrms[1] = Mock(number_of_recently_replicated_bases=15)
        chrms[2] = Mock(number_of_recently_replicated_bases=25)
        self.assertEqual(
            2+15+25, gen.number_of_replicated_bases_in_this_step())


if __name__ == '__main__':
    unittest.main()
