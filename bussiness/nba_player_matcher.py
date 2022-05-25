from copy import copy
from bussiness.nba_player_matcher_exceptions import EmptyDataFrame, WrongDataSource
import pandas as pd


class NBAPlayerMatcher:
    def __init__(self, dataset):
        self.__dataset = dataset
        self.__transform_data()

    def __transform_data(self):
        if self.__dataset.shape[0] == 0:
            raise EmptyDataFrame
        else:
            if 'first_name' in self.__dataset and 'last_name' in self.__dataset \
                    and 'h_in' in self.__dataset and 'h_meters' in self.__dataset:
                self.__dataset = self.__dataset.astype({'h_in': int}, copy=False)
                self.__dataset.drop("h_meters", axis=1, inplace=True)
                self.__dataset.sort_values(by='h_in', ascending=True, inplace=True)
                self.__dataset.reset_index(inplace=True, drop=True)
            else:
                raise WrongDataSource

    def __filter_data(self, expected_sum):
        # Discard all the rows with h_in greater than the expected sum.
        self.__dataset = self.__dataset[self.__dataset['h_in'] < expected_sum]

    def match(self, expected_sum):
        result = []
        self.__filter_data(expected_sum)
        if self.__dataset.shape[0] > 1:
            # Take every row and determine if it can be summed to another row to get the expected sum.
            for _, row in self.__dataset.iterrows():
                # Search the rows with h_in equal to the difference between the expected sum and the h_in
                # of the current row. If any row was found it means that the current row can be summed to
                # the found rows to get the expected sum.
                missing = expected_sum - row['h_in']
                if missing >= row['h_in']:
                    temp_dataset = copy(self.__dataset[self.__dataset['h_in'] == missing])
                    temp_dataset = temp_dataset[(temp_dataset['first_name'] != row['first_name'])
                                                & (temp_dataset['last_name'] != row['last_name'])]
                    # Combine the current row with each found rows.
                    if temp_dataset.shape[0] > 0:
                        for _, row_t in temp_dataset.iterrows():
                            result.append({
                                'player_one': row['first_name'] + ' ' + row['last_name'],
                                'player_two': row_t['first_name'] + ' ' + row_t['last_name']
                            })
                    # Delete the current row to prevent a repeated combination
                    self.__dataset.drop(0, inplace=True)
                    self.__dataset.reset_index(inplace=True, drop=True)
                else:
                    break
        return pd.DataFrame(result)
