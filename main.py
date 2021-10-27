import requests
from bs4 import BeautifulSoup

'''
## WHOSAMPLED SCRAPER ##

to-do:
    - implement a function that fetches info if n_tracks < 5
    - argparse
    - automatic formating of artist and title
    - implement search function

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
    
    def fetch(self, url):

        songs = []

        for page in range(4):
            print(page)
            urls = url + str(page)

            r = self.req.get(urls)
            search_page_soup = BeautifulSoup(r.content, 'html.parser')

            for a in search_page_soup.find_all('div'):
                links = a.find_all('a', {'class': 'trackName playIcon'})
                for link in links:
                    title = link.get('title')
                    songs.append(title)
        
        return set(songs)

    def get_tracks(self, artist, title):
        types = ['covered', 'remixed', 'sampled']
        response = []
        for type in types:
            url = f'https://www.whosampled.com/{artist}/{title}/{type}/?cp='.format(artist = artist, title = title, type = type)

            response.append(s.fetch(url))

        return response[0], response[1], response[2]
    
    def generate_output(self, artist, title):
        
        covers, remixes, sampled = s.get_tracks(artist, title)

        print("{} - {}".format(artist, title))
        print(str(len(covers)) + " Covers\n")
        print(covers)
        print("\n")
        print(str(len(remixes)) + " Remixes\n")
        print(remixes)
        print("\n")
        print("Sampled in {} tracks\n". format(len(sampled)))
        print(sampled)
        print("\n")

if __name__ == "__main__":

    s = Scraper(3)

    s.generate_output('Donna-Summer', 'I-Feel-Love')
    s.generate_output('Elvis-Presley', 'A-Little-Less-Conversation')
