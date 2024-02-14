import numpy as np
import tensorflow as tf
import pandas as pd
import math
from time import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential

from utils.helper_functions import read_file

def model_predict(model, X, y):
    test_mae = []
    test_rmse =  []
    trained_models = []

    for i in range(10):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=i)
            
        #Scale each variable
        sc_X = StandardScaler()
        X_train2 = pd.DataFrame(sc_X.fit_transform(X_train))
        X_test2 = pd.DataFrame(sc_X.fit_transform(X_test))
        X_train2.columns = X_train.columns.values
        X_test2.columns = X_test.columns.values
        X_train2.index = X_train.index.values
        X_test2.index = X_test.index.values
        X_train = X_train2
        X_test = X_test2

        if isinstance(model, Sequential):  # Check if it's a Keras Sequential model
            
            # Train the model
            model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
            
            # Make predictions against the test data
            y_pred = model.predict(X_test)

        else:  # Handle scikit-learn models
            model_fit = model.fit(X_train, y_train)
            y_pred = model_fit.predict(X_test)

        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = math.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)

        test_mae.append(mae)
        test_rmse.append(rmse)
        trained_models.append(model)

    print(model)
    print("rmse : %.3f +/- %.3f" % (np.mean(test_rmse),np.std(test_rmse)))
    print("mae : %.3f +/- %.3f" % (np.mean(test_mae),np.std(test_mae)))
    
    return np.mean(test_rmse), trained_models

def choose_model():
    t0 = time()
    df = read_file("games")
    rolling_szn_avgs = pd.read_csv(r'data/result_array_avgs.csv')

    df2 = df.copy()
    df2 = df2[['GAME_ID','HOME_TEAM_ID','VISITOR_TEAM_ID', 'HOME_TEAM_WINS']]

    # Merge df with home stats
    df2 = df2.merge(rolling_szn_avgs, how='left', left_on=['GAME_ID','HOME_TEAM_ID'], right_on=['GAME_ID','TEAM_ID'])
    df2 = df2[~df2['TEAM_ID'].isnull()].drop(['TEAM_ID'], axis=1)

    # Merge df with away stats
    df2 = df2.merge(rolling_szn_avgs, how='left', left_on=['GAME_ID','VISITOR_TEAM_ID'], right_on=['GAME_ID','TEAM_ID'], suffixes=('_HOME','_AWAY'))
    df2 = df2[~df2['TEAM_ID'].isnull()].drop(['TEAM_ID'], axis=1)

    # Since we are working with averages, drop all rows where avg was 0 for either home or away team
    df2 = df2[~((df2['PTS_HOME']==0)|(df2['PTS_AWAY']==0))]

    # Create target variable point differential
    df['HOME_PT_DIFF'] = df['PTS_home'] - df['PTS_away']
    df2 = df2.merge(df[['GAME_ID','HOME_PT_DIFF']], on='GAME_ID', how='left')
    
    #Drop Unnecessary Fields
    drop = ['HOME_TEAM_WINS',
            'SEASON_HOME', 'SEASON_AWAY',
            'GAME_DATE_EST_HOME', 'GAME_DATE_EST_AWAY', 
            'date_rank_HOME', 'date_rank_AWAY',
            'PTS_HOME', 'PTS_AWAY']

    target = ['HOME_PT_DIFF']
    IDcol = ['GAME_ID', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID']
    predictors = [x for x in df2.columns if x not in drop+target+IDcol]

    # Sample data X and y
    X = df2[predictors]
    y = df2[target]

    mse_linear, trained_linear_models = model_predict(LinearRegression(), X, y)

    seq_model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(units=20, input_dim=X.shape[1], kernel_initializer='normal', activation='relu'),
        tf.keras.layers.Dense(units=5, kernel_initializer='normal', activation='relu'),
        tf.keras.layers.Dense(1, kernel_initializer='normal')
    ])
    seq_model.compile(loss='mean_squared_error', optimizer='adam')

    mse_sequential, trained_sequential_models = model_predict(seq_model, X, y)

    # Choose the model with the lowest MSE
    if mse_sequential < mse_linear:
        print("Sequential model has the lowest MSE.")
        chosen_model = trained_sequential_models[0]
    else:
        print("Linear regression model has the lowest MSE.")
        chosen_model = trained_linear_models[0]

    print("Model Choosing Complete. Execution time : %.2fs" % (time() - t0))
    # Use the chosen model for further processing
    return chosen_model