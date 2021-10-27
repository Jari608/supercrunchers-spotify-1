from whosampled import Scraper
import pathlib
import os
import pandas as pd

def analyse_list(csv_loc):
    s = Scraper(3)

    genre_df = pd.read_csv(csv_loc)
    genre_df = genre_df.head(10)
    genre_df['search_term'] = genre_df[['firstartist', 'trackname']].apply(lambda x: ' '.join(x), axis =1)
    genre_df['sample_data_location'] = genre_df.apply(lambda x: s.generate_output(x['search_term'], False), axis = 1)

    print(genre_df)

    filename = str(os.path.splitext(csv_loc)[0]) + "_analyzed.csv"
    genre_df.to_csv(filename)

    return 0

if __name__ == "__main__":

    pathlib.Path("Data/").mkdir(exist_ok = True)
    pathlib.Path("Data/json/").mkdir(exist_ok = True)
    
    analyse_list('Data\genres_csv\electronic.csv')