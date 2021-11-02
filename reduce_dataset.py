import pandas as pd
import numpy as np
import os

def reduce(dataset):
    df = pd.read_csv(dataset)

    before_len = len(df)

    df = df.drop(['search_term'], axis = 1)
    df.dropna(subset=['sample_data_location'], inplace=True)

    after_len = len(df)

    filename = str(os.path.splitext(dataset)[0]) + "_reduced.csv"
    df.to_csv(filename)

    print("Dataset reduced from {} to {}, {} songs did not have a remix.".format(before_len, after_len, (before_len - after_len)))
    
    return df

if __name__ == "__main__":
    reduce("Data\genres_csv\electronic_analyzed.csv")