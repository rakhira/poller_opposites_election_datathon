import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import cross_val_score, train_test_split
import string
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from nltk.stem import porter
from nltk.stem.util import suffix_replace, prefix_replace
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import SnowballStemmer
import unicodedata
import datetime
import seaborn as sns

from sklearn.decomposition import NMF as NMF_sklearn

def topic_model(df, cluster_num):
    content = df['clean_text']
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, min_df=10)
    X = vectorizer.fit_transform(content)
    features = vectorizer.get_feature_names()
    nmf = NMF_sklearn(n_components=10, max_iter=100, random_state=12345, alpha=0.0)
    W = nmf.fit_transform(X)
    H = nmf.components_

    avg_sent = df['sent'].mean()
    avg_trump_sent = df[df['trump_mentioned_cnt'] > 0]['sent'].mean()
    avg_biden_sent = df[df['biden_mentioned_cnt'] > 0]['sent'].mean()
    print(f'Sentiment for Cluster {cluster_num} is: \n Average Sentiment: {avg_sent} \n Biden Sentiment:  {avg_biden_sent} \n Trump Sentiment:{avg_trump_sent}')
    for i, row in enumerate(H):
        top_ten = np.argsort(row)[::-1][:10]
        print(np.array(features)[top_ten])






if __name__ == '__main__':
    
    final_df = pd.read_json('/Users/lesropro/the_dive/DATAthon/poller_opposites_election_hackathon/ignorefiles/dfs/sentiment_whole.json')

    clus0 = final_df[final_df['cluster_labels'] == 0]
    clus1 = final_df[final_df['cluster_labels'] == 1]
    clus2 = final_df[final_df['cluster_labels'] == 2]
    clus3 = final_df[final_df['cluster_labels'] == 3]
    clus4 = final_df[final_df['cluster_labels'] == 4]
    clus5 = final_df[final_df['cluster_labels'] == 5]
    clus6 = final_df[final_df['cluster_labels'] == 6]