# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 20:39:50 2019


@author: daviesb
"""

import feedparser
import re
import pandas as pd
import json
from dateutil import parser

### RSS Class that handles all RSS feed parsing, currently only brings in most recent article
class RSS():
    
    def __init__(self, source, url):
        
        self.feed = feedparser.parse(url)
        self.source = source
        self.title = self.feed.entries[0].title
        self.link = self.feed.entries[0].link
        self.published = parser.parse(self.feed.entries[0].published).strftime("%h %d, %Y at %H:%M")
        try:
            self.author = self.feed.entries[0].author
        except AttributeError:
            self.author = ''
        self.summary = re.sub('<[^>]*>', '', self.feed.entries[0].summary)
        
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

### combine into one list
rss_feed = [rss_NYT, rss_CNN, rss_Hill, rss_WSJ, rss_FOX, rss_Politico, rss_Alternet, rss_OAN]

### create DF and assign col names
df_rss = pd.DataFrame([feed.source, feed.title, feed.summary, feed.author, feed.link, feed.published] for feed in rss_feed)
df_rss.columns = ['source', 'title', 'summary', 'author', 'link', 'published']

### bring in bias measures from external source
df_bias = pd.read_csv('path to Overall-Source-Ratings-October-2019.csv', sep=',')
df_bias['bias_normalized'] = (df_bias.Bias - df_bias.Bias.mean()) / df_bias.Bias.std()
df_bias['bias_minmax'] = (df_bias.Bias - df_bias.Bias.min()) / (df_bias.Bias.max() - df_bias.Bias.min())

### merge bias measures with RSS feed data
df_rss = pd.merge(df_rss, df_bias, on='source', how='left')
df_rss.sort_values(['published'], ascending=False, inplace=True)
df_rss.reset_index(drop=True, inplace=True)


### write to json
df_rss.to_json(r'path to write json')
json_rss = json.loads(df_rss.to_json())
print(json.dumps(json_rss, indent=4, sort_keys=True))

