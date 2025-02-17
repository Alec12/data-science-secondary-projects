import datetime
import pandas as pd
from Scrapper import Scrapper
from time import sleep
import random

def get_date(days: int):
    #reference_date = datetime.date(2024, 1, 27)
    #date = reference_date - datetime.timedelta(days=days)
    date = datetime.date.today() - datetime.timedelta(days=days)
    return date.strftime('%Y-%m-%d')


def merge_news_old(new_df, old_df):
    return pd.concat([new_df, old_df], sort=False).drop_duplicates().reset_index(drop=True)


def get_data(url, datasets_name, headers):

    scrapper = Scrapper(headers=headers, max_call_errors=5)
    json = scrapper.retrieve_json_api_from_url(url=url)

    if json == None:
        return None

    dfs = {}
    for elem in json['resultSets']:
        if elem['name'] not in datasets_name:
            continue

        df = pd.DataFrame(elem['rowSet'], columns=elem['headers'])
        dfs[elem['name']] = df

    return dfs


def get_game_detail(game_id, headers):
    if type(game_id) != type(str()):
        game_id = '00' + str(game_id)

    url = 'https://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=0&GameID='+str(game_id) \
        + '&StartPeriod=1&StartRange=0'

    print(url)

    df = get_data(url, datasets_name=['PlayerStats'], headers=headers)
    # Introduce a random delay between 0.5 and 1 second
    delay = random.uniform(0.5, 1.0)
    #sleep(0.2)
    sleep(delay)
    return df['PlayerStats']
