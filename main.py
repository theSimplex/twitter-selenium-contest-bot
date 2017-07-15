import json
import os
import signal
import subprocess
import time
import requests
from functools import reduce

from api import Scraper
from ui_driver import Driver

TOKEN = "313726066:AAFKTQjDAixSqdxiO16sl11BMIyfBjGpYKA"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
url = 'https://postmates.com/chicago'



def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    if len(updates["result"]) > 0:
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)
    else:
        return None, None


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def sendText(body):
    text, chat = get_last_chat_id_and_text(get_updates())
    if text is not None and chat is not None:
        send_message(body, chat)
        print(body)

with open('/home/simplex/python/selenium/config.json') as f:
    config = json.load(f)
timings = []
def run():
    tweets = []
    for query in config['search-queries']:
        with Scraper() as page:
            tweets = tweets + page.get_tweets_for_hashtag(query)
    if len(tweets) == 0:
        print('No new tweets discovered.')
        return
    for user in config['users']:
        with Driver(user['name'], user['pwd']) as driver:
            for tweet in tweets:
                time_ = time.time()
                driver.process(tweet)
                timings.append(time.time() - time_)
    print('Avarage tweet process time : {}s'.format(reduce(lambda x, y: x + y, timings) / len(timings)))


sendText('started selenium bot')
while True:
    try:
        run()
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if 'chrom' in str(line) or '800x800' in str(line):
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
        time.sleep(900)
    except:
        pass