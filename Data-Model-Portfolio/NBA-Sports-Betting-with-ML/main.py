import pandas as pd
import datetime

from utils.config import pathname
from utils.config import email
from src.data_preprocessing import prepare_data
from src.predict_spread import predict_new_data
from src.send_email import send_predictions


today = datetime.date.today().strftime('%Y-%m-%d')
client_secret = pd.read_json("data/client_secret.json")

def main():
    # preprocess the data
    prepare_data()

    # predict the spread of upcoming games
    predict_new_data()

    # send an email with the data
    send_predictions(email, today)

if __name__ == "__main__":
    main()