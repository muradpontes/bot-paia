import tweepy
import logging
import configparser
from time import sleep
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live

config = configparser.ConfigParser()
config.read('auth.conf')

consumer_key = config['KEYS']['consumer_key']
consumer_secret = config['KEYS']['consumer_secret']
access_token = config['KEYS']['access_token']
access_token_secret = config['KEYS']['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
console = Console()
logging.basicConfig(filename='bot-paia.log', level=logging.INFO, format='%(asctime)s %(message)s')

def buscar(query):
    count = 0
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang='pt', tweet_mode='extended').items(1)
    
    for tweet in tweets:
        try:
            username = tweet.user.screen_name
            if query not in username.lower():
                api.retweet(tweet.id)
                count+=1
                texto = tweet.full_text
                print(f"\n@{tweet.user.screen_name}\ntweet: '{texto}'\n\033[92mretweetado com sucesso!\n")
                logging.info(f"\n@{tweet.user.screen_name}\ntweet: '{texto}'\nretweetado com sucesso!\n")

        except tweepy.TweepyException as e:
            if '327' in str(e):
                print(f'\n\033[91múltimo tweet com a palavra {query} já retweetado!\n')

            else:
                print(e)
                sleep(60)

if __name__ == "__main__":
    while True:
        spinner = Spinner('dots')
        with Live(spinner, refresh_per_second=12):
            spinner.text = 'procurando tweets...'
            buscar('paia')
            sleep(60)