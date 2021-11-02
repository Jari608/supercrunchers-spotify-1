from whosampled import Scraper
import pathlib
import os
import pandas as pd
import argparse

def rowIndex(row):
    return row.name

def analyse_list(csv_loc):



    print("started")
    s = Scraper(3)

    genre_df = pd.read_csv(csv_loc)
    #genre_df = genre_df.head(10)
    genre_df['search_term'] = genre_df[['firstartist', 'trackname']].apply(lambda x: ' '.join(x), axis =1)
    genre_df['rowIndex'] = genre_df.apply(rowIndex, axis=1)
    genre_df['sample_data_location'] = genre_df.apply(lambda x: s.generate_output(x['search_term'], x['rowIndex'], True), axis = 1)

    print(genre_df)

    filename = str(os.path.splitext(csv_loc)[0]) + "_analyzed.csv"
    genre_df.to_csv(filename)

    print("finished")

    return 0

if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, 
        description = "A tool which retrieves all samples, remixes and covers for a spotify dataset",
        epilog = "Example call: python main.py Data\genres_csv\avant-garde.csv") #default will be shown using the --help command

    parser.add_argument("csv_file", type = str, help = "The csv file containing a compiled spotify dataset")
    args = parser.parse_args()

    pathlib.Path("Data/").mkdir(exist_ok = True)
    pathlib.Path("Data/json/").mkdir(exist_ok = True)
    
    analyse_list(args.csv_file)