import pandas as pd
from utils.config import pathname

def read_file(str_name):
    df = pd.read_csv(pathname + str_name + ".csv")
    return df