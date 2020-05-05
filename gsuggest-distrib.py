import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

from sklearn.cluster import KMeans

import json
import requests
import time
#import pandas as pd

headers = {'User-agent':'Mozilla/5.0'}

def gSuggest(kw):
    googleSuggestURL="https://suggestqueries.google.com/complete/search?hl=fr&client=firefox&q="
    response = requests.get(googleSuggestURL+kw, headers=headers)
    result = json.loads(response.content.decode('utf-8'))
    result = result[1]
    return result

def suggest(keyword, depth):
    data = gSuggest(keyword)
    data.remove(data[0])
    for i in range(0, depth):
        for suggestion in data:
            print(suggestion)
            time.sleep(0.2)
            data = data+gSuggest(suggestion)
    return data

def distribution(suggests, nbResult=40, kwToRemove=''):
    tokenized_sentence=sent_tokenize(' '.join(suggests))
    tokenized_word=word_tokenize(', '.join(tokenized_sentence).replace(kwToRemove+' ', ''))
    fdist = FreqDist(tokenized_word)

    return fdist
    #plt.show()


def df_suggest(df, _type='liste', kwToRemove=[]):
    data = {}
    liste = list(df.unique())
    #print(liste)
    for expression in liste:
        data[expression] = suggest(expression, 1)
    print(data)

KW = 'audi tt rs'
max_depth = 3 #ne poussez pas trop le bouchon 4 ou 5 max

_suggest = suggest(KW,max_depth)
_suggest # données GSuggest

distribution(_suggest, kwToRemove=KW) # données à exporter

fdist = distribution(_suggest, kwToRemove=KW)
max_KW_to_graph = 40 #nombre de KW à afficher sur le graph

plt = fdist.plot(max_KW_to_graph,cumulative=False, title='"'+KW+'" - Distrib. Google Suggest')
