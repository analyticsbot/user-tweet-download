"""Please refer to https://github.com/analyticsbot/user-tweet-download/blob/master/README.md for instru
ctions to the run the code and understand the variables.

Author: analyticsbot

Objective: Download a user's tweet, avoiding the 3200 limit imposed by Twitter API

Returns: Excel csv with user tweet with corresponding values
"""

## imports
import tweepy
from selenium import webdriver
import time
import pandas as pd
from datetime import datetime, timedelta
from sys import platform
import zipfile
import requests
import configparser
from dateutil.parser import parse
import multiprocessing
import sys
import pytz
import helpers
import random
from importlib import reload
reload( helpers )

## determine the platform and bit of the platform, load the config file

if platform == "linux" or platform == "linux2":
    sys_platform = 'linux'
elif platform == "darwin":
    sys_platform = 'macos'
elif platform == "win32":
    sys_platform = 'windows'

config = configparser.ConfigParser()
config.read('config.py')

## parse the config variables

DATE_IN_PAST = config['DEFAULT']['DATE_IN_PAST']
DAYS_IN_PAST = config['DEFAULT'].getint('DAYS_IN_PAST')
NUM_TWEETS_TO_DOWNLOAD = config['DEFAULT'].getint('NUM_TWEETS_TO_DOWNLOAD')
OUTPUT_FILE_NAME_SUFFIX = config['DEFAULT']['OUTPUT_FILE_NAME_SUFFIX']
TIME_SLEEP = config['DEFAULT'].getint('TIME_SLEEP')
TIME_SLEEP_BROWSER_CLOSE = config['DEFAULT'].getint('TIME_SLEEP_BROWSER_CLOSE')

# [TWITTER]
TWITTER_USER_NAME = config['TWITTER']['TWITTER_USER_NAME']
CONSUMER_KEY = config['TWITTER']['CONSUMER_KEY']
CONSUMER_SECRET = config['TWITTER']['CONSUMER_SECRET']
ACCESS_TOKEN = config['TWITTER']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = config['TWITTER']['ACCESS_TOKEN_SECRET']
TWITTER_URL = "https://twitter.com/search?q=(from%3A{TWITTER_USER_NAME})%20until%3A{until}%20since%3A{since}&src=typed_query&f=live"
TWITTER_URL = TWITTER_URL.replace('{TWITTER_USER_NAME}', TWITTER_USER_NAME)

# [CHROME]
# if None, it will download from the Internet
CHROME_GECKODRIVER_LOCATION = config['CHROME']['CHROME_GECKODRIVER_LOCATION']
USE_CHROME = config['CHROME'].getboolean('USE_CHROME')
NUM_THREADS_CHROME = config['CHROME'].getint('NUM_THREADS_CHROME')

# [FIREFOX]
# if None, it will download from the Internet
FIREFOX_GECKODRIVER_LOCATION = config['FIREFOX']['FIREFOX_GECKODRIVER_LOCATION']
USE_FIREFOX = config['FIREFOX'].getboolean('USE_FIREFOX')
NUM_THREADS_FIREFOX = config['FIREFOX'].getint('NUM_THREADS_FIREFOX')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Check authentication went okay

assert api.verify_credentials()
try:
    api.verify_credentials()
    print("Authentication OK")
except Exception as e:
    print("Error during authentication", str(e))

## logic to determine the until when the data is to be parsed

USER_CREATED_DATE = parse(api.get_user(TWITTER_USER_NAME)._json['created_at'])
TODAY_DATE = datetime.now(USER_CREATED_DATE.tzinfo)

if not DATE_IN_PAST and not str(DAYS_IN_PAST).isdigit():
    print ('Either DATE_IN_PAST or DAYS_IN_PAST need to be given')
    sys.exit(1)

try:
    DATE_IN_PAST_PARSED = parse(DATE_IN_PAST)
    DATE_IN_PAST_PARSED = pytz.utc.localize(DATE_IN_PAST_PARSED)
except Exception as e:
    print (str(e))
    DATE_IN_PAST_PARSED = False
if DATE_IN_PAST_PARSED:
    if (TODAY_DATE - DATE_IN_PAST_PARSED).days > DAYS_IN_PAST:
        NEW_DAYS_IN_PAST = (TODAY_DATE - DATE_IN_PAST_PARSED).days
    else:
        NEW_DAYS_IN_PAST = DAYS_IN_PAST
    if (TODAY_DATE - USER_CREATED_DATE).days < (TODAY_DATE - DATE_IN_PAST_PARSED).days:
        NEW_DAYS_IN_PAST = (TODAY_DATE - USER_CREATED_DATE).days
    else:
        NEW_DAYS_IN_PAST = (TODAY_DATE - DATE_IN_PAST_PARSED).days
    if (TODAY_DATE - USER_CREATED_DATE).days > DAYS_IN_PAST:
        NEW_DAYS_IN_PAST = DAYS_IN_PAST
    else:
        NEW_DAYS_IN_PAST = (TODAY_DATE - USER_CREATED_DATE).days

## get most recent 3200 tweets via Twitter API

tweet_objects = []

for page in tweepy.Cursor(api.user_timeline, id=TWITTER_USER_NAME, tweet_mode='extended', \
                          count=NUM_TWEETS_TO_DOWNLOAD).pages():
    tweet_objects.append(page)

## convert the API response to a CSV file

tweets_column = ['screen_name', 'text', 'created_date', 'retweet_count', 'favorite_count', \
                 'replies_count', 'tweet_url', 'language', 'video_url', 'video_views']

def tweet_object(tweet_objects):
    df = pd.DataFrame(columns=tweets_column)
    count_tweets = 0
    break_loop = False

    for tweet_object in tweet_objects:
        if break_loop:
            break
        for tweet in tweet_object:
            count_tweets +=1
            if count_tweets > NUM_TWEETS_TO_DOWNLOAD:
                break_loop = True
                break
            tweet = dict(tweet._json)
            try:
                screen_name = tweet['user']['screen_name']
            except:
                screen_name = 'NA'
            try:
                text = tweet['full_text']
            except:
                text = 'NA'
            try:
                created_date = tweet['created_at']
            except:
                created_date = 'NA'
            try:
                retweet_count = tweet['retweet_count']
            except:
                retweet_count = 'NA'
            try:
                favorite_count = tweet['favorite_count']
            except:
                favorite_count = 'NA'
            try:
                replies_count = tweet['created_at']
            except:
                replies_count = 'NA'
            try:
                tweet_url = 'https://twitter.com/' + screen_name + '/status/' + tweet['id_str']
            except:
                tweet_url = 'NA'
            try:
                language = tweet['lang']
            except:
                language = 'NA'
            try:
                video_url = tweet['entities']['urls'][0]['expanded_url']
            except:
                video_url = 'NA'
            try:
                video_views = 'NA'
            except:
                video_views = 'NA'

            df.loc[df.shape[0]+1] = [screen_name, text, created_date, retweet_count, favorite_count, \
                     replies_count, tweet_url, language, video_url, video_views]

    return df


df_api = tweet_object(tweet_objects)

df_api.shape

df_api.head()

## logic to find the last tweet's date from the API response

last_tweet_date = parse(df_api.loc[df_api.shape[0]]['created_date'])

if OUTPUT_FILE_NAME_SUFFIX == 'None':
    OUTPUT_FILE_NAME_SUFFIX = ''

if NUM_TWEETS_TO_DOWNLOAD < 3200:
    df_api.to_csv(TWITTER_USER_NAME + '_' + OUTPUT_FILE_NAME_SUFFIX + '_TWEETS.csv', index=False)
    print ('Tweets for user = ', TWITTER_USER_NAME, 'downoaded. Filename = ', TWITTER_USER_NAME + '_' + OUTPUT_FILE_NAME_SUFFIX + '_TWEETS.csv')
    print ('Total tweets downloaded', df_api.shape[0])
    START_DAY = 0
    END_DAY = NEW_DAYS_IN_PAST
    GET_REPLIES_COUNT = True

else:
    START_DAY = 0
    END_DAY = NEW_DAYS_IN_PAST
    GET_REPLIES_COUNT = False

## number of the firefox, chrome threads

print (NUM_THREADS_FIREFOX, NUM_THREADS_CHROME)

## logic to handle number of threads depending on the config file. More in the Readme file
## https://github.com/analyticsbot/user-tweet-download/blob/master/README.md

driver_paths = helpers.getPathDriver(config, sys_platform)

if driver_paths['chrome']:
    if NUM_THREADS_CHROME == 0:
        NUM_THREADS_CHROME = 1
else:
    NUM_THREADS_CHROME = 0

if driver_paths['firefox']:
    if NUM_THREADS_FIREFOX == 0:
        NUM_THREADS_FIREFOX = 1
else:
    NUM_THREADS_FIREFOX = 0

def split(seq, num):
    avg = len(seq)/ float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last+=avg
    return out

## distribute the selenium work into number of threads

ALL_DAYS = range(START_DAY, END_DAY)

NUMBER_THREADS = NUM_THREADS_CHROME + NUM_THREADS_FIREFOX
distributed_days = split(ALL_DAYS, NUMBER_THREADS)
BROWSER_TYPE = ['chrome']*NUM_THREADS_CHROME + ['firefox']*NUM_THREADS_FIREFOX


ALL_DAYS, NUMBER_THREADS, distributed_days, BROWSER_TYPE

## function to download tweet data using selenium

def get_data_twitter_selenium(DAYS_THREAD, BROWSER, driver_path, TIME_SLEEP, TIME_SLEEP_BROWSER_CLOSE, THREAD):
    """
    Args:
        DAYS_THREAD - Range of days for which this thread has to function
        BROWSER - Browser type (chrome or firefox)
        driver_path - path of the driver
        TIME_SLEEP - sleep time between url loads
        TIME_SLEEP_BROWSER_CLOSE - sleep time between browser exit and start
        THREAD - thread number

    Returns:
        None

    Output:
        CSV file containing data acquired by this thread
    """
    if BROWSER == 'chrome':
        browser = webdriver.Chrome(executable_path = driver_path)
    else:
        browser = webdriver.Firefox(executable_path = driver_path)

    df = pd.DataFrame(columns=['tweet_text_material', 'text', 'replies_count', 'retweet_count', 'favorite_count', 'tweet_url',\
                        'created_date', 'video_url', 'video_views'])
    df_url = pd.DataFrame(columns=['screen_name', 'url', 'start_date', 'end_date'])
    filename = 0
    num_tweets = 0
    for days_to_subtract in DAYS_THREAD:
        until = (datetime.today() - timedelta(days=days_to_subtract)).strftime('%Y-%m-%d')
        since = (datetime.today() - timedelta(days=days_to_subtract+1)).strftime('%Y-%m-%d')
        NEW_TWITTER_URL = TWITTER_URL.replace('{until}', until).replace('{since}', since)
        print (NEW_TWITTER_URL)

        if (days_to_subtract+1)%5==0:
            browser.close()
            time.sleep(TIME_SLEEP_BROWSER_CLOSE)
            if BROWSER == 'chrome':
                browser = webdriver.Chrome(executable_path = driver_path)
            else:
                browser = webdriver.Firefox(executable_path = driver_path)

        browser.get(NEW_TWITTER_URL)
        time.sleep(TIME_SLEEP)

        last_20_tweets = ['NA']*20
        for i in range(10):
            tweet_div = browser.find_elements_by_css_selector('.css-1dbjc4n.r-my5ep6.r-qklmqi.r-1adg3ll')
            tweet_div_other = browser.find_elements_by_css_selector('.css-4rbku5.css-18t94o4.css-901oao.r-1re7ezh.r-1loqt21.r-1q142lx.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0')
            length = len(tweet_div_other)
            break_ = False

            for i in range(length):
                num_tweets+=1
                tweet_text_material = tweet_div[i].text
                if tweet_text_material in last_20_tweets:
                    break_ = True
                    break

                last_20_tweets[1:] = last_20_tweets[:-1]
                last_20_tweets[0] = tweet_text_material

                tweet_text, replies, rts, favs = ' '.join(tweet_text_material.split('\n')[4:-4]), tweet_text_material.split('\n')[-3], tweet_text_material.split('\n')[-2], tweet_text_material.split('\n')[-1]
                tweet_url = tweet_div_other[i].get_attribute('href')
                tweet_date = tweet_div_other[i].get_attribute('title')


                try:
                    video_views = tweet_div[i].find_element_by_css_selector('.css-901oao.css-16my406.r-lrvibr').text
                except:
                    video_views = 'None'
                try:
                    video_url = tweet_div[i].find_element_by_tag_name('video').get_attribute('src')
                except:
                    video_url = 'None'

                df.loc[df.shape[0]+1] = [tweet_text_material, tweet_text, replies, rts, favs, tweet_url, tweet_date, video_url, video_views]

                if df.shape[0]>200:
                    df['screen_name'] = tweet_text_material.split('\n')[1][1:]
                    df['language'] = ''
                    df.drop_duplicates(inplace=True)
                    df.to_csv(TWITTER_USER_NAME + '_' + OUTPUT_FILE_NAME_SUFFIX + '_' + str(filename) +  '_TWEETS_BROWSER.csv', index=False)
                    filename+=1
                    df = pd.DataFrame(['tweet_text_material', 'text', 'replies_count', 'retweet_count', 'favorite_count', 'tweet_url',\
                        'created_date', 'video_url', 'video_views'])
            if break_:
                break

            browser.execute_script("return document.body.scrollHeight")
            time.sleep(6)


            if random.randint(1,100)==9:
                print (THREAD, 'alive....')
        df_url.loc[df_url.shape[0]+1] = [tweet_text_material.split('\n')[1][1:], NEW_TWITTER_URL, since, until]
    df['screen_name'] = tweet_text_material.split('\n')[1][1:]
    df['language'] = ''
    df.drop_duplicates(inplace=True)
    df.to_csv(TWITTER_USER_NAME + '_' + OUTPUT_FILE_NAME_SUFFIX + '_' + str(filename) +  '_TWEETS_BROWSER.csv', index=False)
    df_url.to_csv(TWITTER_USER_NAME + '_' + OUTPUT_FILE_NAME_SUFFIX + '_TWEETS_BROWSER_URLS.csv', index=False)
    browser.close()

## distribute work using multiprocessing

threads = []
for i in range(NUMBER_THREADS):
    th = multiprocessing.Process(target = get_data_twitter_selenium, kwargs = {'DAYS_THREAD': distributed_days[i],\
                                                                              'BROWSER': BROWSER_TYPE[i],\
                                                                              'driver_path': driver_paths[BROWSER_TYPE[i]],\
                                                                              'TIME_SLEEP': TIME_SLEEP,\
                                                                              'TIME_SLEEP_BROWSER_CLOSE':TIME_SLEEP_BROWSER_CLOSE,\
                                                                              'THREAD': i+1})
    threads.append(th)
    th.start()

for th in threads:
    th.join()

## merge the selenium csv files into one file

df_browser = pd.DataFrame(columns=['tweet_text_material', 'text', 'replies_count', 'retweet_count', 'favorite_count', 'tweet_url',\
                        'created_date', 'video_url', 'video_views', 'screen_name', 'language'])
files = os.listdir('.')
for f in files:
    if f.startswith(TWITTER_USER_NAME) and f.endswith('BROWSER.csv') and any([i.isalpha() for i in f]):
        temp = pd.read_csv(f)
        try:
            temp.drop('Unnamed: 0', inplace=True, axis=1)
        except:
            pass
        try:
            temp.drop('Unnamed: 0.1', inplace=True, axis=1)
        except:
            pass

        df_browser = pd.concat([df_browser, temp], axis=0)

df_browser.to_csv(TWITTER_USER_NAME + '_' + OUTPUT_FILE_NAME_SUFFIX +  '_TWEETS_BROWSER.csv', index=False)


# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

## merge API csv file and browser file

if GET_REPLIES_COUNT:
    df_api['tweet_id'] = df_api['tweet_url'].apply(lambda x:int(x.split('/')[-1][:-1]))
    df_browser['tweet_id'] = df_browser['tweet_url'].apply(lambda x:int(x.split('/')[-1][:-1]))
    df_api = df_api.join(df_browser[['replies_count', 'tweet_url']], how='inner', on=['tweet_id'], lsuffix='_api', rsuffix='_browser')

    df_api.to_csv(TWITTER_USER_NAME + '_' + OUTPUT_FILE_NAME_SUFFIX +  '_TWEETS_API.csv', index=False)
else:
    tweet_urls = df_browser['tweet_url'].tolist()
    tweet_urls = [t.split('/')[1] for t in tweet_urls]
    idx=0
    df_api_2 = pd.DataFrame(columns=tweets_column)
    while True:
        statuses = tweet_urls[idx*100:(idx+1)*100]
        idx+=1
        if len(statuses)==0:
            break
        tweets = api.statuses_lookup(id_=statuses, tweet_mode='extended')
        tweets_df = tweet_object(tweet_objects)
        df_api_2 = pd.concat([df_api_2, tweets_df], axis=0)

df_api_2['tweet_id'] = df_api_2['tweet_url'].apply(lambda x:int(x.split('/')[-1][:-1]))
df_browser['tweet_id'] = df_browser['tweet_url'].apply(lambda x:int(x.split('/')[-1][:-1]))
df_api_2 = df_api_2.join(df_browser[['replies_count', 'tweet_id']], how='inner', on='tweet_id', lsuffix='api', rsuffix='browser_')
df_browser.to_csv(TWITTER_USER_NAME + '_' + OUTPUT_FILE_NAME_SUFFIX +  '_TWEETS_API_BROWSER.csv', index=False)

