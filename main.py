from data.client import Client
from bussiness.nba_player_matcher import NBAPlayerMatcher
from settings import *
import pandas as pd
import json


def main():
    try:
        instructions = 'This application receive an integer and finds the pairs of NBA players\n' \
                       'whose height in inches adds up to the integer input.\n'
        integer_input = int(input(instructions))
        client = Client(DATASOURCE_URL)
        response = client.get()
        if response.status_code == 200:
            data_source = json.loads(response.content)['values']
            matcher = NBAPlayerMatcher(pd.DataFrame(data_source))
            result = matcher.match(integer_input)
            if result.shape[0] > 0:
                for _, row in result.iterrows():
                    print(row['player_one'], ' ', row['player_two'])
            else:
                print('No matches found')
        else:
            raise Exception
    except ValueError:
        print('The input must be an integer.')
    except Exception:
        print('An error has occurred')


if __name__ == '__main__':
    main()
