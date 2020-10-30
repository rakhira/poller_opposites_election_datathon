def prepare_tweet(tweet) -> str:
  ''' 
  Takes a string, removes punctuation, non-ascii, and stems remaining text.
  
  Input:
    str tweet: a string representing a tweet's text
  Output:
    str tweet: a stemmed tweet with no punctuation or non-ascii characters
  '''
  tweet = tweet.translate(str.maketrans('','',string.punctuation))
  tweet = str(tweet.encode("ascii","ignore"))[2:-1]
  stemmer = EnglishStemmer()
  tokens = word_tokenize(tweet)
  tweet = ''
  for token in tokens:
    tweet = tweet+stemmer.stem(token)+" "
  return tweet[:-1]

def tfidf(df) -> NPArray:
    '''
    Creates a tfidf matrix of the text column of a dataframe with 1-3grams.
    
    Input:
        DataFrame df of tweets
    Output:
        NParray tfidf matrix of text
    '''
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    return tf.fit_transform(df['stem_text_plus'])

def cluster(df, tfidfmatrix) -> DataFrame:
    '''
    Creates 7 KMeans clusters based on the tfidf matrix of a dataframe with text and aooends the label to that dataframe.
    
    Input:
        DataFrame df
        NParray tfidf_matrix
    Output:
        DataFrame df labelled df
    '''
    nmf = NMF(n_components=20, init = "random", shuffle = True)
    reduced_matrix = nmf.fit_transform(tfidf_matrix)
    tfidf_df = pd.DataFrame(reduced_matrix)
    kmeans = KMeans(n_clusters=7, random_state=0).fit(tfidf_df)
    df['cluster_labels'] = kmeans.labels_
    return df
