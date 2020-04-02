#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 20:39:50 2019


@author: daviesb
"""

import pandas as pd
import json
import datetime
import sys
sys.path.append('/home/daviesb/Documents/viz.news-scripts/')
from RSS import RSS
#from FTP import FTP_Connect
        

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
rss_DailyKos = RSS('Daily Kos', 'https://www.dailykos.com/blogs/main.rss')
rss_WaPo = RSS('Washington Post', 'http://feeds.washingtonpost.com/rss/politics')
rss_NewYorker = RSS('The New Yorker', 'https://www.newyorker.com/feed/news/news-desk')
rss_Slate = RSS('Slate', 'https://slate.com/feeds/news-and-politics.rss')
rss_Vox = RSS('Vox', 'https://www.vox.com/rss/policy-and-politics/index.xml')
rss_AmCon = RSS('American Conservative', 'https://www.theamericanconservative.com/articles/feed/')
rss_Axios = RSS('Axios', 'https://api.axios.com/feed/politics')
rss_NPR = RSS('NPR', 'https://www.npr.org/rss/rss.php?id=1014')
rss_Breitbart = RSS('Breitbart', 'http://feeds.feedburner.com/breitbart')
rss_CSM = RSS('Christian Science Monitor', 'https://rss.csmonitor.com/feeds/politics')
rss_TPM = RSS('Talking Points Memo', 'https://talkingpointsmemo.com/feed/atom')
rss_Reuters = RSS('Reuters', 'http://feeds.reuters.com/reuters/politicsNews')
rss_WasMon = RSS('Washington Monthly', 'http://feeds.feedburner.com/washingtonmonthly/rss')
rss_WasExa = RSS('Washington Examiner', 'https://www.washingtonexaminer.com/tag/news.rss')
rss_DailySig = RSS('Daily Signal', 'https://www.dailysignal.com/feed')
rss_WashTimes = RSS('Washington Times', 'https://www.washingtontimes.com/rss/headlines/news/politics/')
rss_Newsmax = RSS('Newsmax', 'https://www.newsmax.com/rss/Politics/1/')
rss_Economist = RSS('The Economist', 'https://www.economist.com/united-states/rss.xml')
#rss_BR = RSS('Bipartisan Report', 'https://bipartisanreport.com/feed/')
#rss_Gateway = RSS('The Gateway Pundit', 'https://www.thegatewaypundit.com/feed/')
#rss_Wonkette = RSS('Wonkette', 'https://www.wonkette.com/feeds/feed.rss')
#rss_InfoWars = RSS('InfoWars', 'https://www.infowars.com/feed/')
#rss_Vice = RSS('Vice', 'https://www.vice.com/en_us/rss')
#rss_AP = RSS('AP', 'http://twitrss.me/twitter_user_to_rss/?user=AP_politics')
#rss_CNBC = RSS('CNBC', 'https://www.cnbc.com/id/10000113/device/rss/rss.html')

### combine into one list and parse each feed
rss_feed = [rss_NYT, rss_CNN, rss_Hill, rss_WSJ, rss_FOX, rss_Politico, rss_Alternet, rss_OAN, rss_AmSpec, rss_DailyBeast, rss_NYPost, \
            rss_NatReview, rss_HuffPo, rss_MoJo, rss_DailyKos, rss_WaPo, rss_NewYorker, rss_Slate, rss_Vox, rss_AmCon, rss_Axios, rss_NPR, \
            rss_Breitbart, rss_CSM, rss_TPM, rss_Reuters, rss_WasMon, rss_WasExa, rss_DailySig, rss_WashTimes, rss_Newsmax]
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
df_bias = pd.read_csv('/home/daviesb/Documents/viz.news/sources/Overall-Source-Ratings-October-2019.csv', sep=',')
df_bias = df_bias[df_bias.Quality >= 21]
df_bias['bias_normalized'] = (df_bias.Bias - df_bias.Bias.mean()) / df_bias.Bias.std() # normalized bias scores
df_bias['bias_minmax'] = (df_bias.Bias - df_bias.Bias.min()) / (df_bias.Bias.max() - df_bias.Bias.min()) # 0/1 min max scores

### scores below to be used for css settings on webpage. bias_css determins the x coordinate of where the article appears. quality_css determines the font size
df_temp_left = df_bias[df_bias.Bias <= 0]
left_min = 0
left_max = 0.4
df_temp_left['bias_css'] = (left_max - left_min) * (df_temp_left.Bias - df_temp_left.Bias.min()) / (left_max - df_temp_left.Bias.min()) + left_min

df_temp_right = df_bias[df_bias.Bias > 0]
right_min = 0.4
right_max = 0.8
df_temp_right['bias_css'] = (right_max - right_min) * (df_temp_right.Bias) / (df_temp_right.Bias.max()) + right_min

df_bias = pd.merge(df_bias, df_temp_left[['source', 'bias_css']], on='source', how='left')
df_bias = pd.merge(df_bias, df_temp_right[['source', 'bias_css']], on='source', how='left')
df_bias.bias_css_x.update(df_bias.pop('bias_css_y'))
df_bias.rename(columns={'bias_css_x':'bias_css'}, inplace=True)

#scale_min = 0
#scale_max = 0.8
#df_bias['bias_css'] = (scale_max - scale_min) * (df_bias.Bias - df_bias.Bias.min()) / (df_bias.Bias.max() - df_bias.Bias.min()) + scale_min
scale_min_quality = 0.8
scale_max_quality = 1.1
df_bias['quality_css'] = (scale_max_quality - scale_min_quality) * (df_bias.Quality - df_bias.Quality.min()) / (df_bias.Quality.max() - df_bias.Quality.min()) + scale_min_quality

### join bias data with rss data
df_rss = pd.merge(df_rss, df_bias, on='source', how='left')
df_rss = df_rss[df_rss['published_sort'].notnull()] # remove articles with no published date
two_days_ago = datetime.datetime.today() - datetime.timedelta(days=2) + datetime.timedelta(hours=5)
one_day_ago = datetime.datetime.today() - datetime.timedelta(days=1) + datetime.timedelta(hours=5)
df_rss = df_rss[df_rss['published_sort'] > one_day_ago] # filter out articles that are max 24 (or 48) hours old


### function to assign color values for modular css generation
def create_css_fill(df):
    if df.Bias >=19:
        return 'background-image: linear-gradient(#BF2200, #BF2200);', 'mouseover-white', 'link-light' # dark red
    elif df.Bias >= 10:
        return 'background-image: linear-gradient(#EC7063, #EC7063);', 'mouseover-black', 'link-light' # red
    elif df.Bias >= 4:
        return 'background-image: linear-gradient(#F2D7D5, #F2D7D5);', 'mouseover-black', 'link-dark' # light red
    elif df.Bias <= -19:
        return 'background-image: linear-gradient(#1C2ACD, #1C2ACD);', 'mouseover-white', 'link-light' # dark blue
    elif df.Bias <= -10:
        return 'background-image: linear-gradient(#00BCFF, #00BCFF);', 'mouseover-black', 'link-light' # blue
    elif df.Bias <= -4:
        return 'background-image: linear-gradient(#D6F4FF, #D6F4FF);', 'mouseover-black', 'link-dark' # light blue
    else: 
        return 'background-image: linear-gradient(#EEEEEE, #EEEEEE);', 'mouseover-black', 'link-dark' # slight gray - neutral
      
### apply function
df_rss['css_fill'], df_rss['css_text'], df_rss['css_link_text'] = zip(*df_rss.apply(create_css_fill, axis=1))



### function to truncate long summaries
def truncate(text):
    return (text[:320] + '...') if len(text) > 300 else text

df_rss.summary = df_rss.summary.apply(truncate)

### some double quotes are not being escaped properly, so switch all double quotes in summary field to single quotes
df_rss.summary.replace({'"': '\''}, regex=True, inplace=True)

### drop duplicate rows
df_rss.drop_duplicates(inplace=True)

#### AP feed is coming from twitter, remove url
#df_rss.title[df_rss.source=='AP'] = df_rss.title[df_rss.source=='AP'].apply(lambda x: x.split('http', 1)[0])


json_rss = df_rss.to_json(orient='records')
json_to_ftp = json.dumps(json_rss)

with open('/home/daviesb/Documents/viz.news/json/rss_records.json', 'w') as json_file:
    json.dump(json_rss, json_file)

df_rss.to_json('/home/daviesb/Documents/viz.news/json/rss.json')


today = datetime.datetime.today() + datetime.timedelta(hours=5)
timestamp = today.strftime('Last updated at %H:%M GMT on %b %d, %Y')
with open('/home/daviesb/Documents/viz.news/txt/timestamp.txt', 'w') as text_file:
    text_file.write(timestamp)


#FTP_Connect()


## connecting to FTP and autouploading files
from ftplib import FTP_TLS
import ssl
import time

### FTP code here

print('The average bias is ' + str(round(df_rss.Bias.mean(), 2)) + ', where negative is more liberal')
print('{0:.0%}'.format(df_rss.Bias[df_rss.Bias < 0].count() / df_rss.Bias.count()) + ' of sources are left of center')



