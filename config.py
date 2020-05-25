[DEFAULT]
DATE_IN_PAST = 01-01-2020
DAYS_IN_PAST = 5
NUM_TWEETS_TO_DOWNLOAD = 100
OUTPUT_FILE_NAME_SUFFIX = None
TIME_SLEEP = 5
TIME_SLEEP_BROWSER_CLOSE = 2

[TWITTER]
TWITTER_SEARCH_URL = https://twitter.com/search?q=(from%3A{TWITTER_USER_NAME})%20until%3A{until}%20since%3A{since}&src=typed_query&f=live
TWITTER_USER_NAME = xxxxxxxxxxxxxxx
CONSUMER_KEY = xxxxxxxxxxxxxxx
CONSUMER_SECRET = xxxxxxxxxxxxxxx
ACCESS_TOKEN = xxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ACCESS_TOKEN_SECRET = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


[CHROME]
# if None, it will download from the Internet. Make sure the chrome version on your machine matches the version below
# otherwise change it else error
CHROME_GECKODRIVER_LOCATION = None
USE_CHROME = 0
NUM_THREADS_CHROME = 1
linux64 = https://chromedriver.storage.googleapis.com/83.0.4103.14/chromedriver_linux64.zip
windows = https://chromedriver.storage.googleapis.com/83.0.4103.14/chromedriver_win32.zip
macos = https://chromedriver.storage.googleapis.com/83.0.4103.14/chromedriver_mac64.zip

[FIREFOX]
# if None, it will download from the Internet
FIREFOX_GECKODRIVER_LOCATION = None 
USE_FIREFOX = 1
NUM_THREADS_FIREFOX = 1
macos = https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-macos.tar.gz
linux32 = https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux32.tar.gz
linux64 = https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
windows32 = https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win32.zip
windows64 = https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip
