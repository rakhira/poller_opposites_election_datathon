import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_analyzer_scores(sentence):
    '''
    Returns the sentiment score for the sentence.
    Input:
    -----
    sentence : str
               single tweet
    
    Output:
    ------
    score : dct
            positive, negative, neutral and compound scores.
    '''
    score = analyser.polarity_scores(sentence)
#     print(f"{sentence:-<40} {score}")
    return score

def compound_score(document):
    '''Returns compound score 
    Input:
    -----
    document : str
    
    Output:
    ------
    score_dct['compound'] : float
                            Compound score
    '''
    
    score_dct = sentiment_analyzer_scores(document)
    return score_dct['compound']

def is_trump(document):
    '''Checks if word Trump is in the tweet and counts occurences'''
    return document.lower().count('trump')

def is_biden(document):
    '''Checks if word Biden is in the tweet and counts occurences'''
    return document.lower().count('biden')

# def is_trumpdisgrace(document):
#     tot = document.lower().count('#trumpisanationaldisgrace')
#     return -tot

# def is_creepyjoe(document):
#     tot = 0
#     tot += document.lower().count('#creepyjoe')
#     tot += document.lower().count('#creepyjoebiden')
#     tot += document.lower().count('#sleepyjoe')
#     tot += document.lower().count('#sleepyjoebiden')
#     return -tot

def categorize_sent(sent_val, th = threshold):
    '''Categorizes sent column'''
    if sent_val < -threshold:
        return -1
    elif (sent_val >= -threshold) & (sent_val <= threshold):
        return 0
    elif sent_val > threshold:
        return 1

def summary(df, th = threshold):
    '''Summarizes dataframe and returns count of each polarity in a dict format'''
    dct = {'neu': 0, 'pos': 0, 'neg': 0}
    dct['neu'] = df[(df['sent'] >= -th) & (df['sent'] <= th)]['sent'].count()
    dct['pos'] = df[df['sent'] > th]['sent'].count()
    dct['neg'] = df[df['sent'] < - th]['sent'].count()
    return dct

if __name__ == __main__:
    clean_df = pd.read_json('clean_df.json')
    analyser = SentimentIntensityAnalyzer()

    threshold = 0.05
    clean_df['trump_mentioned_cnt'] = clean_df['full_text'].apply(is_trump)
    clean_df['biden_mentioned_cnt'] = clean_df['full_text'].apply(is_biden)
    # clean_df['#_sent_trumpdisgrace'] = clean_df['full_text'].apply(is_trumpdisgrace)
    # clean_df['#_sent_creepyjoe'] = clean_df['full_text'].apply(is_creepyjoe)
    clean_df['sent'] = clean_df['full_text'].apply(compound_score)
    clean_df['sent_cat'] = clean_df['sent'].apply(categorize_sent)

    trump_df = clean_df[(clean_df['trump_mentioned_cnt'] > 0) 
                        & (clean_df['biden_mentioned_cnt'] == 0)]
    biden_df = clean_df[(clean_df['biden_mentioned_cnt'] > 0) 
                        & (clean_df['trump_mentioned_cnt'] == 0)]
    trump_biden_df = clean_df[(clean_df['biden_mentioned_cnt'] > 0) 
                              & (clean_df['trump_mentioned_cnt'] > 0)]

    trump_nums = summary(trump_df)
    biden_nums = summary(biden_df)
    trump_biden_nums = summary(trump_biden_df)

    print(f'Total number of tweets {clean_df.shape[0]}')
    print(f'Trump\'s total numbers: {trump_nums}')
    print(f'Biden\'s total numbers: {biden_nums}')
    print(f'Trump+Biden\'s total numbers: {trump_biden_nums}')

    clean_df.to_json('sentiment_whole.json')
    trump_df.to_json('trump.json')
    biden_df.to_json('biden.json')
    trump_biden_df.to_json('trump_biden.json')
