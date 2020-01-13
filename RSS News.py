# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 20:39:50 2019


@author: daviesb
"""

import feedparser
import re
import pandas as pd
import json
import datetime
from dateutil import parser


### RSS Class that handles all RSS feed parsing
class RSS():
    
    def __init__(self, source, url):
        self.url = url
        self.source = source
        self.feed = ''
        self.title = []
        self.link = []
        self.published = []
        self.author = []
        self.summary = []
    
    ### parsing function to extract data from XML RSS Feeds
    def parse(self):
        print('parsing...' + self.source)
        try:
            self.feed = feedparser.parse(self.url)
        except:
            pass
        for article in self.feed.entries:
            try:
                self.title.append(article.title)
            except AttributeError:
                self.title.append('no title')
            try:
                self.link.append(article.link)
            except AttributeError:
                self.link.append('no link')
            try:
                self.published.append(parser.parse(article.published).strftime("%h %d, %Y at %H:%M"))
            except AttributeError:
                self.published.append('')
            try:
                self.author.append(article.author)
            except AttributeError:
                self.author.append('(no author provided)')
            try:
                self.summary.append(re.sub('<[^>]*>', '', article.summary))
            except AttributeError:
                self.summary.append('no summary')

    def print(self):
        print(self.title + ' was printed on ' + self.published)
        print('-------------summary--------------')
        print(self.summary)
        print('#################################################')
        print('')
        

### list of sources and RSS feeds, init an RSS object for each
rss_NYT = RSS('New York Times', 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml')
rss_CNN = RSS('CNN', 'http://rss.cnn.com/rss/cnn_allpolitics.rss')
rss_Hill = RSS('The Hill', 'https://thehill.com/taxonomy/term/1132/feed')
rss_WSJ = RSS('Wall Street Journal', 'https://feeds.a.dj.com/rss/RSSOpinion.xml')
rss_FOX = RSS('Fox News', 'http://feeds.foxnews.com/foxnews/politics')
rss_Politico = RSS('Politico', 'https://www.politico.com/rss/congress.xml')
rss_Alternet = RSS('Alternet', 'https://www.alternet.org/category/trump/feed/')
rss_OAN = RSS('One America News', 'https://www.oann.com/category/newsroom/feed/')
rss_AmSpec = RSS('American Spectator', 'https://spectator.org/feed/')
rss_DailyBeast = RSS('Daily Beast', 'https://feeds.thedailybeast.com/summary/rss/politics')
rss_NYPost = RSS('New York Post', 'https://nypost.com/opinion/feed/')
rss_NatReview = RSS('National Review', 'https://www.nationalreview.com/corner/feed/')
rss_HuffPo = RSS('Huffington Post', 'https://www.huffpost.com/section/politics/feed')
rss_MoJo = RSS('Mother Jones', 'https://www.motherjones.com/politics/feed/')
rss_Gateway = RSS('The Gateway Pundit', 'https://www.thegatewaypundit.com/feed/')
rss_DailyKos = RSS('Daily Kos', 'https://www.dailykos.com/blogs/main.rss')
rss_WaPo = RSS('Washington Post', 'http://feeds.washingtonpost.com/rss/politics')
rss_Wonkette = RSS('Wonkette', 'https://www.wonkette.com/feeds/feed.rss')
rss_InfoWars = RSS('InfoWars', 'https://www.infowars.com/feed/')
rss_NewYorker = RSS('The New Yorker', 'https://www.newyorker.com/feed/news/news-desk')
rss_Slate = RSS('Slate', 'https://slate.com/feeds/news-and-politics.rss')
rss_Vox = RSS('Vox' , 'https://www.vox.com/rss/policy-and-politics/index.xml')
rss_AmCon = RSS('American Conservative', 'https://www.theamericanconservative.com/articles/feed/')
rss_Axios = RSS('Axios', 'https://api.axios.com/feed/politics')
rss_NPR = RSS('NPR', 'https://www.npr.org/rss/rss.php?id=1014')
rss_Breitbart = RSS('Breitbart', 'http://feeds.feedburner.com/breitbart')
rss_CSM = RSS('Christian Science Monitor', 'https://rss.csmonitor.com/feeds/politics')
rss_TPM = RSS('Talking Points Memo', 'https://talkingpointsmemo.com/feed/atom')
rss_BR = RSS('Bipartisan Report', 'https://bipartisanreport.com/feed/')
rss_Reuters = RSS('Reuters', 'http://feeds.reuters.com/reuters/politicsNews')
rss_Vice = RSS('Vice', 'https://www.vice.com/en_us/rss')
rss_WasMon = RSS('Washington Monthly', 'http://feeds.feedburner.com/washingtonmonthly/rss')
rss_WasExa = RSS('Washington Examiner', 'https://www.washingtonexaminer.com/tag/news.rss')
#rss_AP = RSS('AP', 'http://twitrss.me/twitter_user_to_rss/?user=AP_politics')
#rss_CNBC = RSS('CNBC', 'https://www.cnbc.com/id/10000113/device/rss/rss.html')
#rss_Economist = RSS('The Economist', 'https://www.economist.com/united-states/rss.xml')


### combine into one list and parse each feed
rss_feed = [rss_NYT, rss_CNN, rss_Hill, rss_WSJ, rss_FOX, rss_Politico, rss_Alternet, rss_OAN, rss_AmSpec, rss_DailyBeast, rss_NYPost, \
            rss_NatReview, rss_HuffPo, rss_MoJo, rss_Gateway, rss_DailyKos, rss_WaPo, rss_Wonkette, rss_InfoWars, rss_NewYorker, rss_Slate, \
            rss_Vox, rss_AmCon, rss_Axios, rss_NPR, rss_Breitbart, rss_CSM, rss_TPM, rss_BR, rss_Reuters, rss_Vice, rss_WasMon, rss_WasExa]
df_rss = pd.DataFrame(columns=['source', 'title', 'summary', 'author', 'link', 'published'])
for feed in rss_feed:
    feed.parse()
    titles = [title for title in feed.title]
    links = [link for link in feed.link]
    published = [published for published in feed.published]
    authors = [author for author in feed.author]
    summaries = [summary for summary in feed.summary]
    df_temp = pd.DataFrame({'source': feed.source, 'title':titles, 'link':links, 'published':published, 'author':authors, 'summary':summaries})
    df_rss = pd.concat([df_rss, df_temp], sort=False)
    
### sort by published date (NOTE: need to flag time zone and articles with incorrect date)    
df_rss['published_sort'] = pd.to_datetime(df_rss.published)
df_rss.sort_values(['published_sort'], ascending=False, inplace=True)
df_rss.reset_index(drop=True, inplace=True)

### import bias and quality ratings from AdFontes Media
df_bias = pd.read_csv(r'C:\Users\daviesb\Desktop\encent\Overall-Source-Ratings-October-2019.csv', sep=',')
df_bias['bias_normalized'] = (df_bias.Bias - df_bias.Bias.mean()) / df_bias.Bias.std() # normalized bias scores
df_bias['bias_minmax'] = (df_bias.Bias - df_bias.Bias.min()) / (df_bias.Bias.max() - df_bias.Bias.min()) # 0/1 min max scores
### scores below to be used for css settings on webpage. bias_css determins the x coordinate of where the article appears. quality_css determines the font size
scale_min = 0
scale_max = 0.8
df_bias['bias_css'] = (scale_max - scale_min) * (df_bias.Bias - df_bias.Bias.min()) / (df_bias.Bias.max() - df_bias.Bias.min()) + scale_min
scale_min_quality = 0.7
scale_max_quality = 1
df_bias['quality_css'] = (scale_max_quality - scale_min_quality) * (df_bias.Quality - df_bias.Quality.min()) / (df_bias.Quality.max() - df_bias.Quality.min()) + scale_min_quality

### join bias data with rss data
df_rss = pd.merge(df_rss, df_bias, on='source', how='left')
df_rss = df_rss[df_rss['published_sort'].notnull()] # remove articles with no published date
two_days_ago = datetime.datetime.today() - datetime.timedelta(days=2) + datetime.timedelta(hours=5)
one_day_ago = datetime.datetime.today() - datetime.timedelta(days=1) + datetime.timedelta(hours=5)
df_rss = df_rss[df_rss['published_sort'] > one_day_ago] # filter out articles that are max 24 (or 48) hours old


### function to assign color values for modular css generation
def create_css_fill(df):
    if df.Bias >= 20:
        return 'background-image: linear-gradient(#BF2200, #BF2200);', 'mouseover-white', 'link-light' # dark red
    elif df.Bias >= 10:
        return 'background-image: linear-gradient(#EC7063, #EC7063);', 'mouseover-black', 'link-light' # red
    elif df.Bias >= 5:
        return 'background-image: linear-gradient(#F2D7D5, #F2D7D5);', 'mouseover-black', 'link-dark' # light red
    elif df.Bias <= -20:
        return 'background-image: linear-gradient(#1C2ACD, #1C2ACD);', 'mouseover-white', 'link-light' # dark blue
    elif df.Bias <= -10:
        return 'background-image: linear-gradient(#00BCFF, #00BCFF);', 'mouseover-black', 'link-light' # blue
    elif df.Bias <= -5:
        return 'background-image: linear-gradient(#D6F4FF, #D6F4FF);', 'mouseover-black', 'link-dark' # light blue
    else: 
        return 'background-image: linear-gradient(#EEEEEE, #EEEEEE);', 'mouseover-black', 'link-dark' # slight gray - neutral
      
### apply function
df_rss['css_fill'], df_rss['css_text'], df_rss['css_link_text'] = zip(*df_rss.apply(create_css_fill, axis=1))



### function to truncate long summaries
def truncate(text):
    return (text[:320] + '..') if len(text) > 300 else text

df_rss.summary = df_rss.summary.apply(truncate)

### some double quotes are not being escaped properly, so switch all double quotes in summary field to single quotes
df_rss.summary.replace({'"': '\''}, regex=True, inplace=True)

### drop duplicate rows
df_rss.drop_duplicates(inplace=True)

#### AP feed is coming from twitter, remove url
#df_rss.title[df_rss.source=='AP'] = df_rss.title[df_rss.source=='AP'].apply(lambda x: x.split('http', 1)[0])


json_rss = df_rss.to_json(orient='records')

with open(r'C:\Users\daviesb\Desktop\encent\json\rss_records.json', 'w') as json_file:
    json.dump(json_rss, json_file)

df_rss.to_json(r'C:\Users\daviesb\Desktop\encent\json\rss.json')

print('The average bias is ' + str(round(df_rss.Bias.mean(), 2)) + ', where negative is more liberal')
print('{0:.0%}'.format(df_rss.Bias[df_rss.Bias < 0].count() / df_rss.Bias.count()) + ' of sources are left of center')

