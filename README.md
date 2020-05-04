# user-tweet-download

<img src="Narendra Modi Twitter page.png" alt="Narendra Modi Twitter page">
<img src="Donald Trump home page snapshot.png" alt="Donald Trump home page snapshot">

<p><strong>Note: </strong>Please use at your own discretion. I used this code to pull data for 2 twitter handles for research purposes. Twitter provides API to download tweets</p>
<p><strong>Download User tweets</strong></p>
<p>This code can be used to download a User's weets from Twitter.com. This can help to bypass the 3200 limit that is put in by the Twitter API. The code is provided as a Jupyter notebook and as Python file.</p>
<p><strong>Requirements</strong></p>
<ul>
<li>requests</li>
<li>tweepy</li>
<li>selenium</li>
<li>pandas</li>
</ul>
<h4>How to Run?</h4>
<ul>
<li>Install the necessary dependencies</li>
<li>Create a folder with the twitter user name or any suitable name</li>
<li>Copy all files into the same directory</li>
<li>Make changes to the config.py files - </li>
<li>Run the program - download_tweets_user.ipynb or download_tweets_user.py</li>
</ul>
<p><strong>What happens when the program is run?</strong></p>
<p>The code first uses the API to fetch the most recent 3200 tweets and then uses selenium to distribute any other tweets on the worker nodes based on the dates</p>
<h4>What datapoints are provided?</h4>
<ul>
<li>
<pre>Tweet text - denoted by text</pre>
</li>
<li>
<pre>Number of replies to the tweet - denoted by replies_count</pre>
</li>
<li>
<pre>Number of retweets to the tweet - denoted by retweet_count</pre>
</li>
<li>
<pre>Number of times this tweet has been favorited - denoted by favorite_count</pre>
</li>
<li>
<pre>Url of the tweet - denoted by tweet_url</pre>
</li>
<li>
<pre>Creation date/time of the tweet - denoted by created_date</pre>
</li>
<li>
<pre>If a video was attached to the tweet, what is the url - denoted by video_url</pre>
</li>
<li>
<pre>If a video was attached to the tweet, how many times it is viewed - denoted by video_views</pre>
</li>
<li><pre>The twitter username - denoted by screen_name</pre></li>
<li><pre>The language of the tweet - denoted by language</pre></li>
</ul>
<h4>Tradeoffs</h4>
<p>Chrome and Firefox, both can be used to download the selenium part of the tweets. Adding more threads to them can make the process faster, but can give rise to issues such as getting throttled by Twitter or too many browsers eating a lot of RAM. The number of threads need to be optimized for the workload as explained below</p>
<h4>Default</h4>
<table>
<tbody>
<tr>
<th>Variable Name</th>
<th>Description</th>
<th>Default value</th>
</tr>
<tr>
<td>DATE_IN_PAST</td>
<td>Download tweets until this date in the past, if available. This data should be at least the creation date of the account. Defaults to creation date if earlier than creation date</td>
<td>01-01-2020</td>
</tr>
<tr>
<td>DAYS_IN_PAST</td>
<td>
<p>Download tweets untils these many days in past. This is similar to DATE_IN_PAST.</p>
<p>The earlier of&nbsp;DATE_IN_PAST and&nbsp;DAYS_IN_PAST is used</p>
</td>
<td>5</td>
</tr>
<tr>
<td>NUM_TWEETS_TO_DOWNLOAD</td>
<td>
<p>Number of tweets to download for the user.&nbsp;</p>
<p>The earlier of&nbsp;</p>
<p>NUM_TWEETS_TO_DOWNLOAD, DATE_IN_PAST and&nbsp;DAYS_IN_PAST is used when there is a conflict</p>
</td>
<td>100</td>
</tr>
<tr>
<td>OUTPUT_FILE_NAME_SUFFIX</td>
<td>Add any suffix name to the file</td>
<td>None</td>
</tr>
<tr>
<td>TIME_SLEEP</td>
<td>Time to sleep between each page load in Selenium. This is to avoid any detection from the server and thus throttling the connection requests. Ideally this should be kept keeping in mind the total number of tweets of the user and the time that should be spent to download the tweets</td>
<td>5</td>
</tr>
<tr>
<td>TIME_SLEEP_BROWSER_CLOSE</td>
<td>The selenium browser is closed and opened to delete any possible cookies. Other details as above</td>
<td>2</td>
</tr>
</tbody>
</table>
<p><strong>Twitter</strong></p>
<table>
<tbody>
<tr>
<th>Variable Name</th>
<th>Description</th>
<th>Default value</th>
</tr>
<tr>
<td>TWITTER_USER_NAME</td>
<td>The twitter username without quotes</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>CONSUMER_KEY</td>
<td>The consumer key of the Twitter developer API</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>CONSUMER_SECRET</td>
<td>The consumer secret of the Twitter developer API</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>ACCESS_TOKEN</td>
<td>The access token of the Twitter developer API</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>ACCESS_TOKEN_SECRET</td>
<td>The access token secret of the Twitter developer API</td>
<td>&nbsp;</td>
</tr>
</tbody>
</table>
<p><strong>Chrome</strong></p>
<table>
<tbody>
<tr>
<th>Variable Name</th>
<th>Description</th>
<th>Default value</th>
</tr>
<tr>
<td>CHROME_GECKODRIVER_LOCATION</td>
<td>The location of already downloaded chromedriver from&nbsp;<a href="https://chromedriver.chromium.org/downloads">https://chromedriver.chromium.org/downloads</a>, else it is downloaded from the web based on the operating system</td>
<td>None</td>
</tr>
<tr>
<td>USE_CHROME</td>
<td>Use chrome to download the tweets via selenium (bool)</td>
<td>0</td>
</tr>
<tr>
<td>NUM_THREADS_CHROME</td>
<td>
<p>Number of threads to use. Each thread will have it's own chrome browser. This should depend on the number of tweets to download, the urgency, and the capacity of the system</p>
<p>&nbsp;</p>
<p>If&nbsp;USE_CHROME is True and&nbsp;NUM_THREADS_CHROME is 0,&nbsp;NUM_THREADS_CHROME defaults to 1</p>
</td>
<td>1</td>
</tr>
<tr>
<td>linux64</td>
<td>Edit the URL if your system is a linux based system</td>
<td>https://chromedriver.storage.googleapis.com/83.0.4103.14/chromedriver_linux64.zip</td>
</tr>
<tr>
<td>windows</td>
<td>Edit the URL if your system is a windows based system</td>
<td>https://chromedriver.storage.googleapis.com/83.0.4103.14/chromedriver_win32.zip</td>
</tr>
<tr>
<td>macos</td>
<td>Edit the URL if your system is a mac based system</td>
<td>https://chromedriver.storage.googleapis.com/83.0.4103.14/chromedriver_mac64.zip</td>
</tr>
</tbody>
</table>
<p><strong>Firefox</strong></p>
<table>
<tbody>
<tr>
<th>Variable Name</th>
<th>Description</th>
<th>Default value</th>
</tr>
<tr>
<td>FIREFOX_GECKODRIVER_LOCATION</td>
<td>The location of already downloaded geckodriver from&nbsp;<a href="https://github.com/mozilla/geckodriver/releases">https://github.com/mozilla/geckodriver/releases</a>, else it is downloaded from the web based on the operating system</td>
<td>None</td>
</tr>
<tr>
<td>USE_FIREFOX</td>
<td>Use firefox to download the tweets via selenium (bool)</td>
<td>1</td>
</tr>
<tr>
<td>NUM_THREADS_FIREFOX</td>
<td>
<p>Number of threads to use. Each thread will have it's own firefox browser. This should depend on the number of tweets to download, the urgency, and the capacity of the system</p>
<p>&nbsp;</p>
<p>If&nbsp;USE_FIREFOX is True and&nbsp;NUM_THREADS_FIREFOX is 0,</p>
<p>NUM_THREADS_FIREFOX defaults to 1</p>
</td>
<td>1</td>
</tr>
<tr>
<td>macos</td>
<td>Edit the URL if your system is a mac based system</td>
<td>https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-macos.tar.gz</td>
</tr>
<tr>
<td>linux32</td>
<td>Edit the URL if your system is a linux 32 bit based system</td>
<td>https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux32.tar.gz</td>
</tr>
<tr>
<td>linux64</td>
<td>Edit the URL if your system is a linux 64 bit based system</td>
<td>https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz</td>
</tr>
<tr>
<td>windows32</td>
<td>Edit the URL if your system is a windows 32 bit based system</td>
<td>https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win32.zip</td>
</tr>
<tr>
<td>windows64</td>
<td>Edit the URL if your system is a windows 64 bit based system</td>
<td>https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip</td>
</tr>
</tbody>
</table>
<p><strong>Discuss</strong></p>
<p>Feel free to post any questions or comments or bugs. Twitter UI changes from time to time and hence the selenium part might break</p>
