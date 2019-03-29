from argparse import ArgumentParser
from twitter import TwitterHTTPError
import pickle

# Twitter API keys
import config

import twitter
# Twitter Authentication
auth = twitter.oauth.OAuth(config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET, config.CONSUMER_KEY, config.CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


def saveToFile(file_name, data):
    """
    Sava Tweets texts to pickled file.

    Args:
        file_name
        data
    """
    PATH = "./data"
    file_name = "{}/{}.pkl".format(PATH, file_name)

    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


def readFromFile(file_name):
    """
    Loads data prom pickled file. File name: {politician_id}.pkl
    
    Args:
        file_name: int    user_id of the account to get the followers list for.

    Returns:
        list(user_id: int)    Array of integers, which are the followers of the account defined in parameter.
    """
    PATH = "./data"
    file_name = "{}/{}.pkl".format(PATH, file_name)
    
    with open(file_name, 'rb') as f:
        data = pickle.load(f)

    return data

def users_for_tweets(opinion, scored_users):    
    selected_users = []

    limit = 10000
    print("! Set limit to {} users".format(limit))
    
    for user_id, scores_dict in scored_users.items():
#         print("{}: {}".format(user_id, scores_dict))
        if scores_dict[opinion] > 3:
            selected_users.append(user_id)
        
        if len(selected_users) >= limit:
            break
    
    return selected_users


def get_user_tweets(user_id):
    try:
        data = twitter_api.statuses.user_timeline(user_id=user_id)
    except TwitterHTTPError as e:
        # if e['error'] != 'Not authorized.':
        #     print(e)
        return []
    
    tweets_texts = []
    for tweet_object in data:
        if tweet_object['lang'] != 'en':
            continue
        
        tweets_texts.append(tweet_object['text'])
    
    return tweets_texts

# USAGE
# data = get_user_tweets(960089177105760256)
# print(data)

def tweets_for_list_of_users(user_list):
    tweet_text_list = []
    
    user_list_length = 1000
    counter = 1
    for user_id in user_list:
        if counter % 25 == 0:
            print("progress: {}%\t{}/{}".format(counter/user_list_length*100, counter, user_list_length))
        if counter % user_list_length == 0:
            break
        
        single_users_tweets_list = get_user_tweets(user_id)
        tweet_text_list.extend(single_users_tweets_list)
        
        counter += 1
        
    return tweet_text_list


def filterKeywors(tweet):
    politicians = ['@FionaMcleodHill',
        '@DavidDavisMP',
        '@RuthDavidsonMSP',
        '@NicolaSturgeon',
        '@SCrabbPembs',
        '@PhilipHammondUK',
        '@theresa_may',
        '@EstherMcVey1',
        '@BorisJohnson',
        '@Nigel_Farage',
        '@Jeremy_Miles',
        '@SeumasMilne',
        '@Keir_Starmer',
        '@tom_watson',
        '@jeremycorbyn',
        '@rosaltmann',
        '@edvaizey',
        '@normanlamb',
        '@sarahwollaston',
        '@ChrisLeslieMP',
        '@labourlewis',
        '@SadiqKhan']
    key_words = ['brexit', 'no-deal', 'no deal', 'nodeal', 'politics', 'government', 'economy', 'prime minister', 'wto', 'article 50', 'efta', 'parties', 'referendum']
    key_words.extend(politicians)
    
    #  modifications: lowercast tweet text and remove "#" and "RT"
    if any(keyword in tweet.lower() for keyword in key_words):
        return True
    else:
        return False

def cleanTweets(tweets):
    return [tweet.lower().replace('#', '').replace('rt ', '') for tweet in tweets]

def filterTweets(tweets):
    """
    Filter provided list of tweets for keywords and politicians twitter handles. Additionaly clean the text of the tweets.
    
    Args:
        tweets: [string]    list of strings (tweets texts)
    
    Return:
        tweets: [string]    filtered list of strings (tweets texts)
    """
    filtered_tweets = list(filter(filterKeywors, tweets))
    filtered_tweets = cleanTweets(filtered_tweets)
    return filtered_tweets

def collectForOpinion(opinion):
    # Create twitter users list (by opinion)
    print("~~~ 1) Create twitter users list (by opinion)")
    scored_users_db = readFromFile('scored_users_not_norm')

    selected_users = users_for_tweets(opinion=opinion, scored_users=scored_users_db)
    print("# {}: {}".format(opinion, len(selected_users)))

    # Get the tweets for the particular opinion from the selected users
    print("~~~ 2) Get the tweets for the {} opinion from the selected users".format(opinion))
    tweets = tweets_for_list_of_users(selected_users)
    print("\t~Tweets fetched")
    print("\t~Filter tweets")
    filtered_tweets = filterTweets(tweets)
    print("\t~saving to file deal_tweets.pkl")
    file_name = '{}_tweets'.format(opinion)
    saveToFile(file_name=file_name, data=filtered_tweets)

    print("{} tweets: {}".format(opinion, len(filtered_tweets)))

# MAIN
parser = ArgumentParser()
parser.add_argument("-o", "--opinion", dest="opinion",
                    help="provide opinion you wish to collect data for: remain/no_deal/deal", metavar="FILE")
args = parser.parse_args()

if args.opinion == None or (args.opinion != "remain" and args.opinion != "no_deal" and args.opinion != "deal"):
    print(args.opinion)
    print("You need to provide opinion you want to collect data for [remain|no_deal|deal].\nUSAGE: 2_1_prepare_tweets_for_sentiment_analysis.py -o [remain|no_deal|deal]")
else:
    collectForOpinion(args.opinion)