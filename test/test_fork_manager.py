import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock
import sys
sys.path.append('../')
from src.genome import Genome
from src.chromosome import Chromosome
from src.fork_manager import ForkManager


## @package ReDyMo.test.test_fork_manager
# Contains the Fork Manager test class

## This class has tests for each Fork Manager method.
# @see Fork Manager
class TestForkManager(unittest.TestCase):

    ## Test constructor by checking the generated object.
    def test_constructor(self):
        gen = MagicMock()
        fork_mngr = ForkManager(234, gen, 15)
        self.assertEqual(fork_mngr.number_of_free_forks, 234)
        index = 0
        for fork in fork_mngr.replication_forks:
            self.assertEqual(fork_mngr.replication_forks[index].genome, gen)
            self.assertEqual(fork_mngr.replication_forks[index].speed, 15)
            self.assertFalse(fork_mngr.just_unattached[fork])
            index += 1

    ## Test by creating mock forks and making them collide with the RNAP and
    # then checking if the necessary methods are called and that certain
    # properties are wth the right value.
    def test_check_replication_transcription_conflicts(self):
        gen = MagicMock()
        fork_mngr = ForkManager(5, gen, 15)
        chrm = MagicMock(transcription_regions=[{'start': 1000, 'end': 2600},
                                                {'start': 5000, 'end': 5601},
                                                {'start': 9000, 'end': 10300}])

        fork1 = fork_mngr.replication_forks[0] = MagicMock(genome=gen, speed=15)
        fork2 = fork_mngr.replication_forks[1] = MagicMock(genome=gen, speed=15)
        fork3 = fork_mngr.replication_forks[2] = MagicMock(genome=gen, speed=15)


        # Set up the forks so that all will collide
        fork1.get_base.return_value = 1400
        fork2.get_base.return_value = 5400
        fork3.get_base.return_value = 9400

        fork1.get_chromosome.return_value = chrm
        fork2.get_chromosome.return_value = chrm
        fork3.get_chromosome.return_value = chrm

        fork1.get_direction.return_value = -1
        fork2.get_direction.return_value = -1
        fork3.get_direction.return_value = -1

        fork1.is_attached.return_value = True
        fork2.is_attached.return_value = True
        fork3.is_attached.return_value = True

        # 3 of 5 forks are attached
        fork_mngr.number_of_free_forks = 2

        # test with time = 1400 and period 1000
        self.assertEqual(
            fork_mngr.check_replication_transcription_conflicts(1400, 1000, True), 3)

        fork1.unattach.assert_called_once()
        fork2.unattach.assert_called_once()
        fork3.unattach.assert_called_once()

        chrm.set_dormant_origin_activation_probability.assert_called()
        self.assertEqual(fork_mngr.number_of_free_forks, 5)

    ## Test if attached forks are advanced, if unattached forks aren't touched
    # and if just unattached forks are prepared to be attached again.
    def test_advance_attached_forks(self):
        gen = MagicMock()
        fork_mngr = ForkManager(3, gen, 15)

        fork1 = fork_mngr.replication_forks[0]
        fork2 = fork_mngr.replication_forks[1]
        fork3 = fork_mngr.replication_forks[2]

        # Prepare mocks of forks
        fork1.advance = Mock(return_value=True)
        fork3.advance = Mock(return_value=False)
        fork1.is_attached = Mock(return_value=True)
        fork2.is_attached = Mock(return_value=False)
        fork3.is_attached = Mock(return_value=True)
        fork_mngr.just_unattached[fork2] = True

        fork_mngr.advance_attached_forks(12)

        self.assertFalse(fork_mngr.just_unattached[fork1])

        self.assertFalse(fork_mngr.just_unattached[fork2])

        self.assertTrue(fork_mngr.just_unattached[fork3])

        fork1.advance.assert_called_with(time=12)
        fork1.advance.assert_called_with(time=12)

    ## Test by setting up a certain amount of forks and checking method calls
    # and properties.
    def test_attach_forks(self):
        gen = MagicMock()

        fork_mngr = ForkManager(2, gen, 15)
        fork_mngr.number_of_free_forks = 2

        fork1 = fork_mngr.replication_forks[0] = MagicMock()
        fork2 = fork_mngr.replication_forks[1] = MagicMock()

        fork1.is_attached.return_value = False
        fork2.is_attached.return_value = False

        fork_mngr.just_unattached[fork1] = False
        fork_mngr.just_unattached[fork2] = False

        gen_loc = MagicMock()
        fork_mngr.attach_forks(gen_loc, 14)
        fork1.attach.assert_called_once_with(genomic_location=gen_loc, direction=1, time=14)
        fork2.attach.assert_called_once_with(genomic_location=gen_loc, direction=-1, time=14)
        self.assertEqual(fork_mngr.number_of_free_forks, 0)

        # Set up for test with only 1 fork available
        fork_mngr.number_of_free_forks = 1

        fork1 = fork_mngr.replication_forks[0] = MagicMock()
        fork1.is_attached.return_value = False

        fork_mngr.just_unattached[fork1] = False
        fork_mngr.just_unattached[fork2] = True
        gen_loc = MagicMock()

        fork_mngr.attach_forks(gen_loc, 14)

        fork1.attach.assert_called_once_with(genomic_location=gen_loc, direction=1, time=14)
        self.assertEqual(fork_mngr.number_of_free_forks, 0)

if __name__ == '__main__':
    unittest.main()
