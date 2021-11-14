import os
import pandas as pd
import json

def getKey(item):
    return item[0]

def get_feature(location, column, nr, min_remix, category):
    
    ids = []

    with open(location) as json_file:
        data = json.load(json_file)

    for song in data[category]:
        if not data[category][song] == None:
            ids.append((data[category][song]['popularity'], data[category][song][column]))
    
    ids = sorted(ids, key = getKey, reverse = True)

    if not len(ids) < min_remix:
        if not ids == []:
            return ids[nr][1]


def add_top_n(dataset, min_remix, category):

    #load Dataset
    df = pd.read_csv(dataset)

    #Remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    column_set = []
    
    for idx in range(min_remix):
        column_set.append(['id_{}'.format(idx + 1), ['track_id', idx]])
        column_set.append(['trackname_{}'.format(idx + 1), ['track_name', idx]])
        column_set.append(['popularity_{}'.format(idx + 1), ['popularity', idx]])
        column_set.append(['preview_url{}'.format(idx + 1), ['preview_url', idx]])
        column_set.append(['track_number{}'.format(idx + 1), ['track_number', idx]])
        column_set.append(['firstartist{}'.format(idx + 1), ['first_artist', idx]])
        column_set.append(['imageurl{}'.format(idx + 1), ['image_url', idx]])
        column_set.append(['spotifyurl{}'.format(idx + 1), ['spotify_url', idx]])
        column_set.append(['acousticness{}'.format(idx + 1), ['acousticness', idx]])
        column_set.append(['danceability{}'.format(idx + 1), ['danceability', idx]])
        column_set.append(['duration_ms{}'.format(idx + 1), ['duration_ms', idx]])
        column_set.append(['energy{}'.format(idx + 1), ['energy', idx]])
        column_set.append(['instrumentalness{}'.format(idx + 1), ['instrumentalness', idx]])
        column_set.append(['key{}'.format(idx + 1), ['key', idx]])
        column_set.append(['liveness{}'.format(idx + 1), ['liveness', idx]])
        column_set.append(['speechiness{}'.format(idx + 1), ['speechiness', idx]])
        column_set.append(['tempo{}'.format(idx + 1), ['tempo', idx]])
        column_set.append(['time_signature{}'.format(idx + 1), ['time_signature', idx]])
        column_set.append(['valence{}'.format(idx + 1), ['valence', idx]])
  
    for column_s in column_set:

        name_df = column_s[0]
        name_json = column_s[1][0]
        rank = column_s[1][1]

        df[name_df] = df.apply(lambda x: get_feature(x['sample_data_location'], name_json, rank, min_remix, category), axis = 1)

    df = df.dropna()

    return df

def merge_datasets(min_remix, category, file_name):

    final_df = pd.DataFrame()

    mypath = 'Data/genres_csv/'

    files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    files = list(filter(lambda k: 'reduced' in k, files))

    for file in files:
        print(file)
        final_df = final_df.append(add_top_n(file, min_remix, category))

    print(final_df)

    final_df.to_csv('Data/genres_csv/{}.csv'.format(file_name))

if __name__ == "__main__":
    '''
    merge_datasets(3, 'covers', 'final_set_covers_top3')
    merge_datasets(2, 'covers', 'final_set_covers_top2')
    merge_datasets(1, 'covers', 'final_set_covers_top1')
    
    merge_datasets(3, 'remixes', 'final_set_remixes_top3')
    merge_datasets(2, 'remixes', 'final_set_remixes_top2')
    merge_datasets(1, 'remixes', 'final_set_remixes_top1')
    '''
    merge_datasets(3, 'sampled', 'final_set_sampled_top3')
    merge_datasets(2, 'sampled', 'final_set_sampled_top2')
    merge_datasets(1, 'sampled', 'final_set_sampled_top1')
    