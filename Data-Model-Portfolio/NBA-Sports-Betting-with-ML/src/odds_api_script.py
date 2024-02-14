import requests
import pandas as pd
import numpy as np
from time import time, sleep
from utils.helper_functions import read_file

f = open('utils/API_KEY.txt', 'r')
API_KEY = f.read()
f.close()

SPORT = 'basketball_nba' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'american' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

BOOKMAKERS = 'draftkings' # 'draftkings' | 'fanduel' | 'pointsbetus'| 'williamhill_us'| 'betmgm'|'unibet_us'| 'betrivers'| 'bovada'| 'wynnbet'| 'mybookieag'|'lowvig'| 'betonlineag'| 'betus'| 'superbook'

BET_SIZE = 100


def retrieve_odds_data():
    t0 = time()

    # Update this line if the data directory is not in the parent directory
    path = "/Users/alecnaidoo/Downloads/nba-data-04-20/"

    # Get old games data to find out the last date that the script was executed
    try: 
        old_odds = pd.read_csv(path + 'odds_data.csv', index_col=None)
    
    except:
        raise Exception(
            'odds_data.csv should be in the data/ directory'
        )
    
    try:
        # Total Odds Data
        odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
        params={
            'api_key': API_KEY,
            'regions': REGIONS,
            'markets': MARKETS,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        }).json()

        # Events Data
        event_response = requests.get(
            f'https://api.the-odds-api.com/v4/sports/{SPORT}/events',
            params={
                'api_key': API_KEY,
                'regions': REGIONS,
                'markets': MARKETS,
                'oddsFormat': ODDS_FORMAT,
                'dateFormat': DATE_FORMAT,
            }).json()

        # Reformat the Odds Data
        events = pd.DataFrame(event_response)
        data_list = []

        for odds_response_entry in odds_response:
            for bookmaker_entry in odds_response_entry['bookmakers']:
                for market_entry in bookmaker_entry['markets']:
                    id = odds_response_entry['id']
                    key = bookmaker_entry['key']
                    title = bookmaker_entry['title']
                    last_update = market_entry['last_update']
                    team1_name = market_entry['outcomes'][0]['name']
                    team1_price = market_entry['outcomes'][0]['price']
                    team1_point = market_entry['outcomes'][0]['point']
                    team2_name = market_entry['outcomes'][1]['name']
                    team2_price = market_entry['outcomes'][1]['price']
                    team2_point = market_entry['outcomes'][1]['point']

                    data_list.append([id, key, title, last_update, team1_name, team1_price, team1_point, team2_name, team2_price, team2_point])

        event_data = pd.DataFrame(data_list, columns=['id', 'key', 'title', 'last_update', 'team1_name', 'team1_price', 'team1_point', 'team2_name', 'team2_price', 'team2_point'])

        def join_odds_data(bookmaker):
            newdata = events.merge(event_data[event_data['key']==bookmaker], on='id', how='left').dropna() #drop games with no odds data
            return newdata
        
        # change bookmaker if needed
        new_odds = join_odds_data('draftkings')

        # Identify the Team ID for each of the teams in odds
        team_list = np.concatenate([new_odds['home_team'].unique(), new_odds['away_team'].unique()]).tolist()

        # Clean up Team ID
        team_meta = read_file('teams')
        team_meta['CITY-TEAM'] = team_meta['CITY'] + ' ' + team_meta['NICKNAME']
        team_meta = team_meta[['TEAM_ID','CITY-TEAM']]

        #Merge in Team ID
        new_odds = new_odds.merge(team_meta, left_on='home_team', right_on='CITY-TEAM', how='left').rename(columns={'TEAM_ID':'home_team_id'}).drop('CITY-TEAM',axis=1)
        new_odds = new_odds.merge(team_meta, left_on='away_team', right_on='CITY-TEAM', how='left').rename(columns={'TEAM_ID':'away_team_id'}).drop('CITY-TEAM',axis=1)


        # Exclude duplicates from the old data
        df_old_no_duplicates = old_odds[~old_odds['id'].isin(new_odds['id'])]

        # Concatenate old data without duplicates and the new data
        full_odds = pd.concat([df_old_no_duplicates, new_odds]).reset_index(drop=True)
        full_odds.to_csv(path + r'odds_data.csv', index=False)
        
        return full_odds, new_odds

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    
    