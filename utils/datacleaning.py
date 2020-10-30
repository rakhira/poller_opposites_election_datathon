def prepare_tweet(tweet) -> str:
  ''' 
  Takes a string, removes punctuation, non-ascii, and stems remaining text
  input:
    str tweet: a string representing a tweet's text
  output:
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

  def drop_invalid_rows(df):
    df.drop(axis=0, labels=[110181,110182], inplace=True)
    return df

def create_columns(df):
'''
Takes in dataframe with of user column and creates new columns with subset of information within the column.
input:
    pandas dataframe: 
output:
    dataframe with new columns 
'''
df['clean_text'] = df['full_text'].apply(prepare_tweet)
df['description'] = df['user'].apply(lambda X: X[X.find("'description': ")+16:X.find(", 'url':")-1])
df['location'] = df['user'].apply(lambda X: X[X.find("'location': ")+13:X.find(", 'description': ")-1])
df['language'] = df['user'].apply(lambda X: X[X.find("'lang': ")+9:X.find(", 'contributors_enabled': ")-1])
df['followers'] = df['user'].apply(lambda X: X[X.find("'followers_count': ")+19:X.find(", 'friends_count': ")-1])
df['friends'] = df['user'].apply(lambda X: X[X.find("'friends_count': ")+18:X.find(", 'listed_count': ")-1])
return df

def device(x):
    '''
    Identifies the type of device used to send the tweet.
    input:
        string: 
    output:
        string:
    '''

    devices = ['iPhone','iPad','Android','Web App', 'Media Studio', 'Echofon','TweetDeck', 'viriya', 'Twibble.io', 'dlvr.it', 'Tweetbot','TwitPanePlus','SocialFlow', 'News Aggregator', 'Instagram', 'Bot', 'bot', 'iphone','android','web app','News','news']

    for dev in devices:
        if dev in str(x):
            return dev
        else:
            continue


def create_device_column(df):
    '''
    Converts the created_at column into datetime and creates new columns for time-series analysis.
    input:
        pandas dataframe: 
    output:
        dataframe with new columns 
    '''
    df['device'] = df['source'].apply(device)
    return df

def convert_datetime(df):
    '''
    Converts the created_at column into datetime and creates new columns for time-series analysis.
    input:
        pandas dataframe: 
    output:
        dataframe with new columns 
    '''
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['hour'] = df.created_at.apply(lambda x: x.hour)
    df['date'] = df.created_at.apply(lambda x: x.date)
    df['month'] = df.created_at.apply(lambda x: x.month)
    df['dayofweek'] = df.created_at.apply(lambda x: x.dayofweek)
    return df

def location_clean(x):

    if x == 'United States':
        return 'USA'
    elif x == 'USA':
        return 'USA'
    elif x == 'America':
        return 'USA'
    elif x == 'United States of America':
        return 'USA'
    elif x == ' USA':
        return 'USA'
    elif x == 'U.S.A.':
        return 'USA'
    elif x == 'Los Angeles':
        return 'CA'
    elif x == 'Boston':
        return 'MA'
    elif x == 'Chicago':
        return 'IL'
    elif x == 'Seattle':
        return 'WA'
    elif x == 'USA ':
        return 'USA'
    elif x == 'UNITED STATES':
        return 'USA'
    else:
        for sl, sa in zip(state_long, state_abbv):
            if sl in x or sa in x:
                return sa
            else:
                continue

def create_location(df):
    '''
    creates a new column for locations by states and corrects for edge cases.
    
    input:
        pandas dataframe: 
    output:
        dataframe with new columns 
    '''
    df['clean_loc'] = df['location'].apply(location_clean)
    return df


def create_clean_tweets(df):
    '''
    creates a new column with cleaned up tweets and combines the description of the user to the tweet.
    
    input:
        pandas dataframe: 
    output:
        dataframe with new columns 
    '''
    df['clean_description'] = df['description'].apply(prepare_tweet)
    df['combined_text'] = df['clean_text'] + df['clean_description']
    return df

def save_final_df(df, save_as ,ext):
    '''
    saves final dataframe into specified file extension.
    
    input:
        pandas dataframe, pandas save method (to_json, to_csv, etc.)
        
    '''
    df.save_as('final_df.{ext}')

if __name__ == '__main__':
state_long = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']

state_abbv = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
