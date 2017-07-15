from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        WebDriverException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from pyvirtualdisplay import Display


class Driver:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __enter__(self):
        display = Display(visible=0, size=(1920, 1080))  
        display.start()
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("start-maximized")
        prefs = {"profile.managed_default_content_settings.images": 2,
                'profile.managed_default_content_settings.javascript': 2}
        chrome_options.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)  # 
        self.login(self.username, self.password)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.close()


    def login(self, username, password):
        try:
            self.auth_(username, password)
        except:
            print('Retrying to login.')
            self.auth_(username, password)

    def auth_(self, username, password):
        self.driver.get('https://twitter.com/')
        if not 'mobile' in self.driver.current_url:
            login_button = self.driver.find_element_by_class_name('StreamsLogin')
            login_button.click()
        print('Loging in as {}'.format(username))
        username_ = self.driver.find_element_by_name('session[username_or_email]')
        username_.send_keys(username)
        password_ = self.driver.find_element_by_name('session[password]')
        password_.send_keys(password)
        username_.submit()
        
    def clean_username(self, username):
        for sym in ['@', '!', '.', ',', ')', '(']:
            username = username.replace(sym, '').split('\n')[0]
        return username

    def follow_user(self, username):
        if username:
            try:
                url = 'https://twitter.com/' + username
                self.driver.get(url)
                follow_button = self.driver.find_element_by_class_name('follow-button')
                if follow_button.text == 'Following':
                    print('Already following {}'.format(username))
                    return
                elif follow_button.text == 'Follow':
                    follow_button.click()
                    print('Followed {}'.format(username))
            except(NoSuchElementException, WebDriverException):
                print('Failed to follow {}.'.format(username))

    def follow_user_nojs(self, username):
        if username:
            try:
                url = 'https://mobile.twitter.com/' + username
                self.driver.get(url)
                follow_button = self.driver.find_element_by_xpath('.//input[@value = "Follow"]')
                if follow_button.get_attribute('value') == 'Following':
                    print('Already following {}'.format(username))
                    return
                elif follow_button.get_attribute('value') == 'Follow':
                    follow_button.click()
                    print('Followed {}'.format(username))
            except(NoSuchElementException, WebDriverException):
                print('Failed to follow {}.'.format(username))

    def retweet(self, tweet_url):
        try:
            retweet_icon = self.driver.find_element_by_xpath('.//button[@class = "ProfileTweet-actionButton  js-actionButton js-actionRetweet"]')
            if retweet_icon.is_displayed():
                retweet_icon.click()
                self.driver.find_element_by_xpath('.//button[@class = "EdgeButton EdgeButton--primary retweet-action"]').click()
                print('Retweeted. ({})'.format(tweet_url))
            else:
                print('Tweet already retweeted. ({})'.format(tweet_url))
            self.driver.find_element_by_xpath('//span[text()="Follow"]').click()
        except(NoSuchElementException, WebDriverException):
            print('Failed to retweet tweet.')

    def retweet_nojs(self, tweet_url):
        try:
            retweet_icon = self.driver.find_element_by_xpath('.//span[@title = "Retweet"]')
            self.follow_user_nojs(self.driver.find_element_by_xpath('.//span[@class = "username"]').text.replace('@', ''))
            if retweet_icon.is_displayed():
                retweet_icon.click()
                self.driver.find_element_by_xpath('.//input[@value = "Retweet"]').click()
                print('Retweeted. ({})'.format(tweet_url))
            else:
                print('Tweet already retweeted. ({})'.format(tweet_url))
        except(NoSuchElementException, WebDriverException):
            print('Failed to retweet tweet.')

    def parse_text(self, text):
        users = [i for i in text.split(' ') if i.startswith('@')]
        return users

    def process(self, tweet_url):
        if 'mobile' in self.driver.current_url:
            self.driver.get('https://mobile.twitter.com{}'.format(tweet_url))
            text = self.driver.find_element_by_class_name('tweet-text').text
            follow = self.parse_text(text)
            self.retweet_nojs(tweet_url)
            for user in follow:
                self.follow_user_nojs(self.clean_username(user))
        else:
            self.driver.get('https://twitter.com{}'.format(tweet_url))
            text = self.driver.find_element_by_class_name('TweetTextSize').text
            follow = self.parse_text(text)
            self.retweet(tweet_url)
            for user in follow:
                self.follow_user(self.clean_username(user))
