import unittest
from src.data_manager import DataManager
from tvDatafeed import Interval  # Added: Import Interval for assertion comparison.

class TestDataManager(unittest.TestCase):
    def test_map_interval(self):
        dm = DataManager()
        # Corrected: Assert against the actual enum object, not a string.
        self.assertEqual(dm.map_interval('1D'), Interval.in_daily)

if __name__ == '__main__':
    unittest.main()