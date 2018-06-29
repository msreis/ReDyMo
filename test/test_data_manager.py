import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock
import sys
sys.path.append('../')
from src.data_manager import DataManager

## @package ReDyMo.test.test_data_manager
# Contains the DataManager test class

## This class has tests for each DataManager method.
# @see DataManager
class TestGenome(unittest.TestCase):

    # All tests will use the dummy data stored in here
    db_path = "data/simulation.sqlite"
    mfa_path = "data/MFA-Seq_dummy/"

    ## Tests the constructor. 
    def test_constructor(self):
        data_mngr = DataManager(self.db_path, self.mfa_path)
        self.assertEqual(self.db_path, data_mngr.database_path)
        self.assertEqual(self.mfa_path, data_mngr.mfa_seq_folder_path)

    ## Tests query function by comparing with hard-coded data present in db.
    def test_select_chromosomes_from_database(self):
        data_mngr = DataManager(self.db_path, self.mfa_path)
        data = data_mngr.select_chromosomes_from_database(organism="dummy")
        # Comparison based on the known data inside db
        self.assertEqual(data, [('dummy_01', 150, None, 10, 5,
                                 float("inf"), 0, 'dummy')])
    
    ## Tests by comparing to hardcoded data.
    def test_probability_landscape(self):
        data_mngr = DataManager(self.db_path, self.mfa_path)
        prob = data_mngr.probability_landscape("dummy_01", 7)
        self.assertEqual(prob, [0.00010000000000021103, 0.3334000000000006, 1.0,
        0.6667000000000001, 0.6667000000000001, 0.3334000000000006,
        0.1667500000000004])
    
    ## Tests by setting up mock auxiliary functions and checking the result of
    # main function
    def test_chromosomes(self):
        # Setup
        data_mngr = DataManager(self.db_path, self.mfa_path)
        data_mngr.select_chromosomes_from_database = MagicMock(
            return_value=[("dummy_01", 150, None, 10, 5, float("inf"), 0, 'dummy')])
        data_mngr.select_transcription_regions_from_database = MagicMock(
            return_value=[(25, 80, 'dummy_01')])
        data_mngr.probability_landscape = MagicMock(
            return_value="dummy_landscape")

        # Call 
        chrm = data_mngr.chromosomes("dummy")

        # Assertions
        data_mngr.select_chromosomes_from_database.assert_called_once_with(
            organism="dummy")
        data_mngr.select_transcription_regions_from_database.assert_called_once_with(
            chromosome_code="dummy_01")
        self.assertEqual(chrm, 
        [{'code': 'dummy_01', 'length': 150,
        'probability_landscape': 'dummy_landscape',
        'transcription_regions': [{'start': 25, 'end': 80}]}]) 

    ## Test by checking output against known data
    def test_select_transcription_regions_from_database(self):
        data_mngr = DataManager(self.db_path, self.mfa_path)
        data = data_mngr.select_transcription_regions_from_database(
            chromosome_code='dummy_01')
        self.assertEqual(data, [(25, 80, 'dummy_01')])

if __name__ == '__main__':
    unittest.main()