import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from bussiness.nba_player_matcher import NBAPlayerMatcher, EmptyDataFrame, WrongDataSource


class TestNBAPlayerMatcher(unittest.TestCase):
    def test_match_empty_dataframe_exception(self):
        with self.assertRaises(EmptyDataFrame):
            matcher = NBAPlayerMatcher(pd.DataFrame())

    def test_match_wrong_datasource_exception(self):
        with self.assertRaises(WrongDataSource):
            matcher = NBAPlayerMatcher(pd.DataFrame([{
                'player_one': 'Brevin Knight',
                'player_two': 'Nate Robinson'
            }]))

    def test_match_no_matches(self):
        matcher = NBAPlayerMatcher(pd.read_csv('resources/data.csv'))
        result = matcher.match(9999)
        self.assertEqual(result.shape[0], 0)

    def test_match_same_height(self):
        matcher = NBAPlayerMatcher(pd.read_csv('resources/data.csv'))
        result = matcher.match(180)
        self.assertEqual(result.shape[0], 0)

    def test_match_MachEight_success_example(self):
        matcher = NBAPlayerMatcher(pd.read_csv('resources/data.csv'))
        result = matcher.match(139)
        expected = pd.DataFrame([
            {
                'player_one': 'Nate Robinson',
                'player_two': 'Brevin Knight'
            },
            {
                'player_one': 'Nate Robinson',
                'player_two': 'Mike Wilks'
            }
        ])
        self.assertIsNone(assert_frame_equal(expected, result))

    def test_match_expected_sum_140(self):
        matcher = NBAPlayerMatcher(pd.read_csv('resources/data.csv'))
        result = matcher.match(140)
        expected = pd.DataFrame([
            {
                'player_one': 'Nate Robinson',
                'player_two': 'Speedy Claxton'
            },
            {
                'player_one': 'Nate Robinson',
                'player_two': 'Chucky Atkins'
            },
            {
                'player_one': 'Brevin Knight',
                'player_two': 'Mike Wilks'
            }
        ])
        self.assertIsNone(assert_frame_equal(expected, result))
