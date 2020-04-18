#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 00:15:55 2020

@author: daviesb
"""


import pandas as pd
import numpy as np
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords


def get_topics(df, num_topics):
    
    ### get stop words from NLTK
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
    
    data = df.title.values.tolist()
    # data_summary = df.summary.values.tolist()
    # for summary in data_summary:
    #     data.append(summary)
    
    ### tokenize words and clean up
    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True)) # deacc=True removes punctuation
            
    data_words = list(sent_to_words(data))
    
    ### creating bigrams, trigrams, and more
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold means fewer phrases
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
    
    ### faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    
    
    ### define functions for stopwords, bigrams, trigrams, and lemmatization
    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]
    
    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]
    
    def make_trigrams(texts):
        return [trigram_mod[bigram_mod[doc]] for doc in texts]
    
    
    ### calling functions
    data_words_nostops = remove_stopwords(data_words)
    data_words_bigrams = make_bigrams(data_words_nostops)
    data_words_trigrams = make_trigrams(data_words_bigrams)
    
    
    ### create dictionary and corpus
    id2word = corpora.Dictionary(data_words_trigrams)
    texts = data_words_trigrams
    corpus = [id2word.doc2bow(text) for text in texts]
    
    # Human readable format of corpus (term-frequency)
    # [[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]
        

    ### build LDA model
    # num_topics = 4
    lda_model = gensim.models.ldamodel.LdaModel(
        corpus = corpus,
        id2word = id2word,
        num_topics = num_topics,
        random_state = 100,
        update_every = 1,
        chunksize = 100,
        passes = 10,
        alpha = 'auto',
        per_word_topics = True)
    
    # pprint(lda_model.print_topics())
   
    
    ### model perplexity and coherence
    # print('Perplexity: ', lda_model.log_perplexity(corpus)) # a measure of how good the model is. lower is better.
    
    # coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words_trigrams, dictionary= id2word, coherence='c_v')
    # coherence_lda = coherence_model_lda.get_coherence()
    # print('Coherence Score: ', coherence_lda)
    
    
    ### take the messy output of top words in each of the topics and convert it to one data frame
    df_topics = pd.DataFrame(columns=['Score', 'Word', 'Topic'])
    for num_topic in range(num_topics):
        df_temp = pd.DataFrame(lda_model.top_topics(corpus)[num_topic][0], columns=('Score', 'Word'))
        df_temp['Topic'] = num_topic
        df_topics = df_topics.append(df_temp, ignore_index=True)
    ### exclude words that come up often but are not included in stopwords dictionary
    exclude = ['new', 'could', 'need', 'say', 'calls', 'help', 'get', 'stay', 'despite', 'says', 'would', 'show', 'gets', 'things', \
               'stop', 'amid', 'people', 'name', 'cases', 'us']
    df_topics = df_topics[df_topics['Word'].isin(exclude) == False]
        
        
    ### this while loop extracts the top X words (one form each topic), based on num_topics
    website_topics = []
    while len(website_topics) < num_topics:
        website_topics.append(df_topics['Word'][df_topics['Score'].argmax()]) # get highest score and return word
        df_topics = df_topics[df_topics['Topic'] != df_topics['Topic'][df_topics['Score'].argmax()]] ### remove topic where word was taken from
        df_topics = df_topics[df_topics['Word'].isin(website_topics) == False].reset_index(level=0, drop=True)
    
    ### title case and change underscore to space
    website_topics = [item.title() for item in website_topics]
    website_topics = [item.replace("_", " ") for item in website_topics]
    ### print topics
    print('Top ' + str(num_topics) + ' topics:\n')
    for topic in website_topics:
        print(topic)
        
    
    
    ### create empty dataframe to hold css_topic
    css_topic = pd.DataFrame(index=range(0, len(df)), columns=['css_topic'])
    css_topic = css_topic.replace(np.nan, '', regex=True)
    ### generate JavaScript classes in css_topic
    df.reset_index(drop=True, inplace=True)
    for index, row in css_topic.iterrows():
        for topic in range(num_topics):
            if website_topics[topic].lower() in df['title'][index].lower():
                css_topic['css_topic'][index] = css_topic['css_topic'][index] + "topic-" + str(topic) + " "
                # print(str(index) + " contains " + str(website_topics[topic]))
    
    ### append css_topic to df
    df = pd.concat([df, css_topic], axis=1)
    

    # ### append True/False for whether or not topic appears in each title (or summary if it's included earlier in script)
    # for topic in range(num_topics):
    #     df.insert(2, website_topics[topic], df['title'].str.lower().str.contains(website_topics[topic].lower()))
        
    return df, website_topics