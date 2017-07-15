from bs4 import BeautifulSoup
import requests


class Scraper:
    
    register = []
    
    def __init__(self):
        with open('history.dat', 'r') as f:
            saved = f.readlines()
            self.register = [i.strip('\n') for i in saved]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(exc_type, exc_value, traceback)
        with open('history.dat', 'w') as f:
            for tweet in self.register:
                f.write(tweet + '\n')
    
    def get_tweets_for_hashtag(self, key):
        tweets = []
        page = requests.get('https://twitter.com/hashtag/{}?lang=en'.format(key))
        soup = BeautifulSoup(page.content, 'html.parser')
        for post in soup.findAll("div", { "data-permalink-path" : True }):
            if post.get('data-permalink-path') not in self.register:
                tweets.append(post.get('data-permalink-path'))
                self.register.append(post.get('data-permalink-path'))
        return tweets
