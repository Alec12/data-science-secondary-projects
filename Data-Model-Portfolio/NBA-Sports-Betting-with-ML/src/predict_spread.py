import pandas as pd
import numpy as np
from time import time
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data_preprocessing import process_odds_data
from src.choose_model import choose_model

def predict_new_data():
    t0 = time()
    data = process_odds_data()

    #Drop Unnecessary Fields
    drop = ['SEASON_HOME', 'SEASON_AWAY','GAME_DATE_EST_HOME', 
            'GAME_DATE_EST_AWAY', 'date_rank_HOME',
            'date_rank_AWAY','PTS_HOME', 'PTS_AWAY',
            'team1_name', 'team1_price','team1_point',
            'team2_name','team2_price','team2_point',
            'home_team_id', 'away_team_id']

    target = ['HOME_PT_DIFF']
    IDcol = ['id','sport_key','sport_title',
            'commence_time','home_team','away_team',
            'key','title','last_update']

    predictors = [x for x in data.columns if x not in drop+target+IDcol]


    X = data[predictors]


    #Scale each variable
    sc_X = StandardScaler()
    X2 = pd.DataFrame(sc_X.fit_transform(X))

    X2.columns = X.columns.values
    X2.index = X.index.values
    X = X2

    # make predictions
    chosen_model = choose_model()
    y_pred = chosen_model.predict(X)

    # Line up predictions with the dataset
    data['predictions'] = np.round(y_pred)

    # Create new dataset with just the date, the teams, the bet spread, and predicted spread
    d2 = data[['commence_time','last_update','home_team','away_team','key', 'team1_price','team1_point', 'predictions']]
    d2['hometeam-cover-predictions'] = np.where(d2.predictions < d2.team1_point, "Fail to Cover", "Cover")
    # Decline bet if it's within 2 points of odds
    #d2['should_you_bet'] = abs(d2['team1_price']) + 100
    
    # keep track of all models / date run / current RMSE / 
    # come up with performance tracker?
    # cleanup
    print("Model Choosing Complete. Execution time : %.2fs" % (time() - t0))
    return d2
    
    

