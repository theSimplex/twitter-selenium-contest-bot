# Selenium Twitter Contest bot.

Twitter bot to participate in online contests without API interactions.
Made with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and [Selenium](http://www.seleniumhq.org/).
Utilizes 'headless' selenium mode.

## Disclaimer

This bot is written purely for educational purposes. I hold no liability for what you do with this bot or what happens to you by using this bot.

## Installation
 * Make sure you have Python3.6 up and running
 * `git clone` the repository, or download the zip file and unzip it
 * `pip install bs4`
 * [Selenium installation](https://selenium-python.readthedocs.io/installation.html)

 ## Usage
 Create file config.json:
 >**config.json** 
 ```json
 {
        "search-queries": ["query1", "query2"],
        "follow-keywords": ["keyword1", "keyword2"],
        "users": [{"name": "user1",
                  "pwd": "password1"},
                  {"name": "user2",
                  "pwd": "password2"}]
}
``` 