import requests
import json
import argparse
import pathlib
import re
import os

from bs4 import BeautifulSoup

from spotify_fetch import fetch as spotify_fetch
'''
## WHOSAMPLED SCRAPER ##

Author: Jari Burgers
Course: SuperCrunchers - JADS Den Bosch

This Scraper fetches all remixes, covers and sampled track for a given track.
For each remix, cover or sample, track information is scraped from spotify.
For each track, a json file is created containing the information for each song.

'''

class Scraper:
    '''
    Class: Scraper

    This class contains all functions needed to retrieve track info from WhoSampled

    '''

    def __init__(self, verbosity=0):
        # create a session to manage lifetime of self.requests and skip auto-reject from
        # whosampled; seems pretty unfriendly to block self.request's default headers.
        self.verbosity = verbosity
        self.directions = None
        self.base_url = 'https://whosampled.com'
        self.req = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=10)
        self.req.mount('https://', adapter)
        self.req.mount('http://', adapter)
        self.req.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
        }
    
    def search(self, song_title): #function from samplify
        """ Queries whosampled.com for song, returns relevant links
        Description:
        - Builds query string with `song_title` and `artist_name`
        - whosampled is doing the heavy lifting for 'relevance',
          as only the top result for a given query is taken
        Parameters:
          song_title:
          - <str> song title, e.g 'Teenage Love'
          artist_name:
          - <str> artist name, e.g 'Slick Rick'
        """

        query = song_title.replace(' ', '%20')
        url = f'https://www.whosampled.com/search/tracks/?q={query}'
        r = self.req.get(url)
        search_page_soup = BeautifulSoup(r.content, 'html.parser')
        search_results = search_page_soup.findAll(
            'li', attrs={'class': "listEntry"})

        if not search_results:
            return None, None

        # return first result
        link = [i.a for i in search_results][0].get('href')

        link_r = list(filter(None, link.split('/')))

        return link_r[0], link_r[1]
        
    def fetch(self, url):

        songs = []

        for page in range(8): #only 15 songs per page, iterate over pages

            urls = url + str(page)
            r = self.req.get(urls)
            search_page_soup = BeautifulSoup(r.content, 'html.parser')

            for a in search_page_soup.find_all('div'):

                links = a.find_all('a', {'class': 'trackName playIcon'})
                for link in links:
                    title = link.get('title')
                    songs.append(title)

        return songs

    def fetch_main_page_info(self, url):

        cover  = []
        remix  = []
        sample = []

        r = self.req.get(url)
        search_page_soup = BeautifulSoup(r.content, 'html.parser')

        for a in search_page_soup.find_all('div'):
            links = a.find_all('a', {'class': 'trackName playIcon'})
            for link in links:
                title = link.get('title')
                href = link.get('href')

                if href.startswith('/sample'):
                    sample.append(title)
                elif href.startswith('/remix'):
                    remix.append(title)
                elif href.startswith('/cover'):
                    cover.append(title)
                else:
                    print('source unknown')

        return  cover, remix, sample
        

    def get_tracks(self, artist, title):
      
        s = Scraper(3)

        response_cov = []
        response_rem = []
        response_sam = []

        url_main = f'https://www.whosampled.com/{artist}/{title}/'.format(artist = artist, title = title)
        cover, remix, sample = s.fetch_main_page_info(url_main)
        response_cov.append(cover)
        response_rem.append(remix)
        response_sam.append(sample)

        url = f'https://www.whosampled.com/{artist}/{title}/covered/?cp='.format(artist = artist, title = title)
        response_cov.append(s.fetch(url))

        url = f'https://www.whosampled.com/{artist}/{title}/remixed/?cp='.format(artist = artist, title = title)
        response_rem.append(s.fetch(url))

        url = f'https://www.whosampled.com/{artist}/{title}/sampled/?cp='.format(artist = artist, title = title)
        response_sam.append(s.fetch(url))

        cov = set([item for sublist in response_cov for item in sublist])
        rem = set([item for sublist in response_rem for item in sublist])
        sam = set([item for sublist in response_sam for item in sublist])

        return cov, rem, sam
    
    def generate_output(self, input, nr, nr_last, len_df, verbose):
        
        if nr > nr_last:
            
            s = Scraper(3)

            artist, title = s.search(input)
            
            if artist == None and title == None:
                print("{} not found on WhoSampled".format(input))
            else:
                print("Retrieving data for {} - {}".format(artist, title))

            location = "Data/json/{}_{}.json".format(artist, title)
            print("\n\n###################\n\n")
            print(str(nr) + "/" + str(len_df))
            print("\n\n###################\n\n")
            
            if not os.path.exists(location):
                if not artist == None:
                
                    covers, remixes, sampled = s.get_tracks(artist, title)

                    covers_dict = {x: spotify_fetch(x) for x in covers}
                    remixes_dict = {x: spotify_fetch(re.sub(r'^.*?\'s ', ' ', x)) for x in remixes} #remixes get found better without original artist on spotify
                    samples_dict = {x: spotify_fetch(x) for x in sampled}

                    data = {}
                    data['Artist'] = artist
                    data['title'] = title
                    data['Metrics'] = []
                    data['Metrics'].append({
                        'n_covers': len(covers),
                        'n_remixes': len(remixes),
                        'n_sampled': len(sampled) 
                    })
                    data['covers'] = covers_dict
                    data['remixes'] = remixes_dict
                    data['sampled'] = samples_dict
                    data['spotify_data'] = spotify_fetch(artist + ' ' + title)

                    with open(location, "w") as f:
                        json.dump(data, f)

                    if verbose:
                        print(json.dumps(data, indent = 4))
                    
                    print("{} created".format(location))
                    return location
                
                else:
                    print("no info found on spotify for {}".format(input))
                    return None
            
            else:
                print("{} already created.".format(location))
                return location


if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, 
        description = "A tool which retrieves all samples, remixes and covers for a given song from WhoSampled.com",
        epilog = "Example call: python whosampled.py 'donna summer i feel love'") #default will be shown using the --help command
    parser.add_argument("title", type = str, help = "Title of the song")
    parser.add_argument('--verbose', '-v', dest='verbose', action='store_true', help='Be verbose')
    args = parser.parse_args()

    s = Scraper(3)

    pathlib.Path("Data/").mkdir(exist_ok = True)
    pathlib.Path("Data/json/").mkdir(exist_ok = True)

    s.generate_output(args.title, args.verbose)

    #s.generate_output('Donna-Summer', 'I-Feel-Love')
    #s.generate_output('Elvis-Presley', 'A-Little-Less-Conversation')
