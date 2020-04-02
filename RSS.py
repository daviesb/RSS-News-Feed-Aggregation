# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 16:24:10 2020

@author: daviesb
"""

import feedparser
from dateutil import parser
import re



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
    ### todo: proper exception handling
    def parse(self):
        print('parsing...' + self.source)
        try:
            self.feed = feedparser.parse(self.url)
        except:
            pass
        for article in self.feed.entries:
            try:
                self.title.append(article.title)
            except:
                self.title.append('no title')
            try:
                self.link.append(article.link)
            except:
                self.link.append('no link')
            try:
                self.published.append(parser.parse(article.published).strftime("%h %d, %Y at %H:%M"))
            except:
                self.published.append('')
            try:
                self.author.append(article.author)
            except:
                self.author.append('(no author provided)')
            try:
                self.summary.append(re.sub('<[^>]*>', '', article.summary))
            except:
                self.summary.append('no summary')

    def print(self):
        print(self.title + ' was printed on ' + self.published)
        print('-------------summary--------------')
        print(self.summary)
        print('#################################################')
        print('')
