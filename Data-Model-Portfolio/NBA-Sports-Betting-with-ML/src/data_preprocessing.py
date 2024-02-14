import pandas as pd
import numpy as np
import warnings
from time import time

from utils.config import pathname
from utils.helper_functions import read_file
from src.odds_api_script import retrieve_odds_data


# Ignore all warnings
warnings.filterwarnings("ignore")

def prepare_data():
    t0 = time()
    # Summarize game detail stats
    gdf = read_file("games_details")
    gdf = gdf.groupby(['GAME_ID', 'TEAM_ID'], as_index=False)[['FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
                                                              'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS']].sum()

    gdf['FT_PCT'] = gdf['FGM'] / gdf['FGA']
    gdf['FG_PCT'] = gdf['FG3M'] / gdf['FG3A']
    gdf['FG3_PCT'] = gdf['FTM'] / gdf['FTA']

    gdf.drop(['FGM', 'FG3M', 'FTM', 'REB'], axis=1, inplace=True)

    df = read_file("games")

    # Convert 'GAME_DATE_EST' to datetime
    df['GAME_DATE_EST'] = pd.to_datetime(df['GAME_DATE_EST'])

    # Create game meta df
    gmeta = df[['GAME_ID', 'SEASON', 'GAME_DATE_EST']]
    # Merge date_count with gdf
    gdf2 = gdf.merge(gmeta, on='GAME_ID', how='left').sort_values(by=['SEASON', 'GAME_DATE_EST'])

    # Identify non-id stat columns
    non_id_columns = gdf2.columns.difference(['GAME_ID', 'TEAM_ID', 'SEASON', 'GAME_DATE_EST', 'date_rank'])

    # Re-arrange columns
    gdf2 = gdf2[['GAME_ID', 'TEAM_ID', 'SEASON', 'GAME_DATE_EST'] + non_id_columns.to_list()]
    gdf2['PTS'] = gdf2.pop('PTS')

    # Filter for current season
    max_season = gdf2['SEASON'].max()
    gdf2 = gdf2[gdf2['SEASON'] == max_season]

    # Make gdf2 to numpy for efficiency
    gdf2 = gdf2.to_numpy()

    # Identify non-id stat columns
    non_id_columns = np.setdiff1d(np.arange(gdf2.shape[1]), [0, 1, 2, 3])

    # Create placeholder numpy memory
    result_array = np.empty((gdf2.shape[0], 4), dtype=object)

    for i, row in enumerate(gdf2):
        curr_team = row[1]  # Assuming 'TEAM_ID' is at index 1
        curr_season = row[2]  # Assuming 'SEASON' is at index 2
        curr_date = row[3]  # Assuming 'GAME_DATE_EST' is at index 17

        # Filter rows based on conditions using boolean indexing
        temp_array = gdf2[(gdf2[:, 1] == curr_team) & (gdf2[:, 2] == curr_season) & (gdf2[:, 3] < curr_date)]

        if temp_array.shape[0] > 0:
            # Calculate mean for each stat using vectorized operations
            mean_values = np.nanmean(temp_array[:, non_id_columns], axis=0)
        else:
            # If tempdf is empty, set mean_values to NaN
            mean_values = np.full(len(non_id_columns), np.nan)

        # Flatten the array and assign values to the result array
        result_array[i, 0] = curr_team
        result_array[i, 1] = curr_season
        result_array[i, 2] = curr_date
        result_array[i, 3] = mean_values.tolist()

    model_df = np.hstack((gdf2[:, 0].reshape(-1, 1), result_array))
    model_df = np.hstack([model_df[:, :4], np.nan_to_num(np.vstack(model_df[:, 4]))])

    rolling_szn_avgs = pd.DataFrame(model_df, columns=['GAME_ID', 'TEAM_ID', 'SEASON', 'GAME_DATE_EST', 'AST', 'BLK', 'DREB',
                                                        'FG3A', 'FG3_PCT', 'FGA', 'FG_PCT', 'FTA', 'FT_PCT', 'OREB', 'PF',
                                                        'STL', 'TO', 'PTS'])

    # Group by 'TEAM_ID' and find the index of the row with the maximum 'GAME_DATE_EST' value in each group
    max_indices = rolling_szn_avgs.groupby('TEAM_ID')['GAME_DATE_EST'].idxmax()

    # Filter for only upcoming teams
    odds_data, new_odds = retrieve_odds_data()
    team_id_list = np.concatenate([new_odds['home_team_id'].unique(), new_odds['away_team_id'].unique()]).tolist()

    # Use the indices to extract the corresponding rows
    current_day_avg_data = rolling_szn_avgs.loc[max_indices]
    current_day_avg_data = current_day_avg_data[(current_day_avg_data['SEASON'] == max_season)&(current_day_avg_data['TEAM_ID'].isin(team_id_list))]

    # Replace current season data with new averages
    result_array_avgs = pd.read_csv('data/result_array_avgs.csv')
    # Remove current season data from result_array_avgs
    result_array_avgs = result_array_avgs[result_array_avgs['SEASON'] != max_season]

    # Concatenate rolling_szn_avgs into result_array_avgs
    result_array_avgs = pd.concat([result_array_avgs, rolling_szn_avgs], ignore_index=True)

    # Save the updated DataFrame back to result_array_avgs.csv
    result_array_avgs.to_csv('data/result_array_avgs.csv', index=False)

    # append new averages to main df
    current_day_avg_data.to_csv(r'data/current_day_avg_data.csv', index=False)
    print("Pre-Processing Complete. Execution time : %.2fs" % (time() - t0))

def process_odds_data():
    odds_data, new_odds = retrieve_odds_data()

    odd2 = new_odds.copy()

    # Merge df with home stats
    current_day_avg_data = pd.read_csv(r'data/current_day_avg_data.csv')
    odd2 = odd2.merge(current_day_avg_data, how='left', left_on=['home_team_id'], right_on=['TEAM_ID']).drop('GAME_ID', axis=1)
    odd2 = odd2[~odd2['TEAM_ID'].isnull()].drop(['TEAM_ID'], axis=1)

    # Merge df with away stats
    odd2 = odd2.merge(current_day_avg_data, how='left', left_on=['away_team_id'], right_on=['TEAM_ID'], suffixes=('_HOME', '_AWAY')).drop('GAME_ID', axis=1)
    # odd2 = odd2.merge(rolling_szn_avgs, how='left', left_on=['GAME_ID','VISITOR_TEAM_ID'], right_on=['TEAM_ID'], suffixes=('_HOME','_AWAY'))
    odd2 = odd2[~odd2['TEAM_ID'].isnull()].drop(['TEAM_ID'], axis=1)
    
    return odd2
