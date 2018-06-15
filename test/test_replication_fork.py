import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock
import sys
sys.path.append('/home/brunobbs/Documents/IC/ReDyMo/')
from src.replication_fork import ReplicationFork
from src.genome import Genome
from src.chromosome import Chromosome
from src.genomic_location import GenomicLocation


## @package ReDyMo.test.test_replication_fork
# Contains the Genomic Location test class

## This class has tests for each Genomic Location method.
# @see Genomic Location
class test_replication_fork(unittest.TestCase):

    ## Test the constructor by checking the created object with the input.
    def test_constructor(self):
        gen = Genome([])
        rep_fork = ReplicationFork(gen, 1)
        self.assertEqual(rep_fork.genome, gen)
        self.assertEqual(rep_fork.speed, 1)

    ## Test the fork attachment by first trying to attach to an already
    # attached fork, then tries with a non attached for and checks if the
    # replicate method is called with the right parameters.
    def test_attach(self):
        rep_fork = ReplicationFork(Mock(), 1)
        rep_fork.base = 1
        # Assert throws exception
        with self.assertRaises(ValueError):
            rep_fork.attach(Mock(), None, None)

        chrms = [Chromosome(1, 3, [0.2, 0.5, 0.6], None),
                 Chromosome(3, 2, [0.1, 0.9], None)]
        chrms[0].replicate = MagicMock(return_value=True)

        gen = Genome(chrms)
        gen_loc = Mock(base=1,chromosome=chrms[0])
        rep_fork = ReplicationFork(gen, 2) 
        rep_fork.attach(gen_loc, 1, 3)

        chrms[0].replicate.assert_called_with(start=1, end=1, time=3)

    ## Test if the fork will reset its variables when it unataches.
    def test_unattach(self):
        rep_fork = ReplicationFork(Mock(), 1)
        rep_fork.base = 1
        rep_fork.unattach()
        self.assertNotEqual(rep_fork.base, 1)
        self.assertEqual(rep_fork.chromosome, None)
        self.assertEqual(rep_fork.direction, None)
        
    ## Test the advancing of the fork by attaching it to a base and checking
    # that the replicate function was called with the right bases.
    def test_advance(self):
        chrms = [Chromosome(1, 3, [0.2, 0.5, 0.6], None),
                 Chromosome(3, 2, [0.1, 0.9], None)]
        chrms[0].replicate = MagicMock(return_value=True)

        gen = Genome(chrms)
        gen_loc = Mock(base=1,chromosome=chrms[0])
        rep_fork = ReplicationFork(gen, 2) 
        rep_fork.base = gen_loc.base
        rep_fork.chromosome = gen_loc.chromosome
        rep_fork.direction = 1
        self.assertTrue(rep_fork.advance(4))
        chrms[0].replicate.assert_called_with(start=gen_loc.base,
                                               end=gen_loc.base + 2, time=4)
        
        chrms[0].replicate = MagicMock(return_value=False)
        self.assertFalse(rep_fork.advance(4))

    ## Test if a frk will report attached when is and not when it isn't.
    def test_is_attached(self):
        rep_fork = ReplicationFork(Mock(), 2)
        self.assertFalse(rep_fork.is_attached())
        rep_fork.base = 1
        self.assertTrue(rep_fork.is_attached())


if __name__ == '__main__':
    unittest.main()
