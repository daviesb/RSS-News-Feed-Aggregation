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
    
    def parse(self):
        print('parsing...' + self.source)
        self.feed = feedparser.parse(self.url)
        for article in self.feed.entries:
            self.title.append(article.title)
            self.link.append(article.link)
            try:
                self.published.append(parser.parse(article.published).strftime("%h %d, %Y at %H:%M"))
            except AttributeError:
                self.published.append('')
            try:
                self.author.append(article.author)
            except AttributeError:
                self.author.append('(no author provided)')
            self.summary.append(re.sub('<[^>]*>', '', article.summary))

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
rss_Politico = RSS('Politico', 'https://www.politico.com/rss/politics08.xml')
rss_Alternet = RSS('Alternet', 'https://www.alternet.org/category/trump/feed/')
rss_OAN = RSS('One America News', 'https://www.oann.com/category/newsroom/feed/')

### combine into one list and parse each feed
rss_feed = [rss_NYT, rss_CNN, rss_Hill, rss_WSJ, rss_FOX, rss_Politico, rss_Alternet, rss_OAN]
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
    
df_rss['published_sort'] = pd.to_datetime(df_rss.published)
df_rss.sort_values(['published_sort'], ascending=False, inplace=True)
df_rss.reset_index(drop=True, inplace=True)



df_bias = pd.read_csv(r'C:\Users\daviesb\Desktop\encent\Overall-Source-Ratings-October-2019.csv', sep=',')
df_bias['bias_normalized'] = (df_bias.Bias - df_bias.Bias.mean()) / df_bias.Bias.std()
df_bias['bias_minmax'] = (df_bias.Bias - df_bias.Bias.min()) / (df_bias.Bias.max() - df_bias.Bias.min())
scale_min = 0
scale_max = 0.8
df_bias['bias_css'] = (scale_max - scale_min) * (df_bias.Bias - df_bias.Bias.min()) / (df_bias.Bias.max() - df_bias.Bias.min()) + scale_min


df_rss = pd.merge(df_rss, df_bias, on='source', how='left')
df_rss = df_rss[df_rss['published_sort'].notnull()]
two_days_ago = datetime.datetime.today() - datetime.timedelta(days=2) + datetime.timedelta(hours=5)
one_day_ago = datetime.datetime.today() - datetime.timedelta(days=1) + datetime.timedelta(hours=5)
df_rss = df_rss[df_rss['published_sort'] > one_day_ago]



json_rss = df_rss.to_json(orient='records')


with open(r'C:\Users\daviesb\Desktop\encent\json\rss_records.json', 'w') as json_file:
    json.dump(json_rss, json_file)

df_rss.to_json(r'C:\Users\daviesb\Desktop\encent\json\rss.json')



