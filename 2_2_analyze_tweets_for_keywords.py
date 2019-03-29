from argparse import ArgumentParser
import pickle

def saveToFile(file_name, data):
    """
    Saves data using pickle to file. File name: {file_name}.pkl

    Args:
        file_name: int    user_id of the account to get the followers list for.
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


# Watson
import json
import config
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, KeywordsOptions
from watson_developer_cloud.watson_service import WatsonApiException

## Watson API
# Watson Tone Analyzer
api_key_tone = config.api_key_tone
service_url_tone = config.service_url_tone

# Watson Natural Language Understanding
api_key_keywords = config.api_key_keywords
service_url_keywords = config.service_url_keywords

def aggregateKeywordAnalysis(analysis):
    keywords = []
    
    for keyword_object in analysis['keywords']:
        if keyword_object['relevance'] < 0.05:
            continue
    
        strongest_emotions = {}
        for emotion, score in keyword_object['emotion'].items():
            if score < 0.20:
                continue
            strongest_emotions[emotion] = score
        
        keywords.append({'keyword': keyword_object['text'], 'emotion': strongest_emotions, 'sentiment': keyword_object['sentiment']['label']})
    
    return keywords   


def getKeywordsWithEmotion(tweet):
    """Watson API call, analyzes text at the word level. Identifies keywords, analyzes their relevance,
    emotion (anger, joy, sadness, fear, disgist) with number <0,1> and
    sentiment with label (positive/negative) and score <-1,1>.
    
    FREE API LIMIT 30,000 NLU Items Per Month
        NOTE: A NLU item is based on the number of data units enriched and the number of enrichment features applied. A data unit is 10,000 characters or less. For example: extracting Entities and Sentiment from 15,000 characters of text is (2 Data Units * 2 Enrichment Features) = 4 NLU Items.
    
    TODO
    1. escape ' characters
    2. remove # from hashtags, otherwise they will be not identified as keywords

    Args:
        tweet: string -> tweet text

    Returns:
        [{'keyword': string, 'emotion': {emotion1: int, emotion2: int}}, ...]

        Returns list of objects, each object contains the string which is the keyword under key 'keyword' and object 'emotion' consisting of keys of strongest emotions and their score.
    """
    NLU = NaturalLanguageUnderstandingV1(
        version = '2018-11-16',
        iam_apikey = api_key_keywords,
        url = service_url_keywords
    )

    try:
        keyword_analysis = NLU.analyze(
            text = tweet,
            features = Features(keywords=KeywordsOptions(emotion=True, sentiment=True))
        ).get_result()
    except WatsonApiException:
        return []
    
#     print(json.dumps(keyword_analysis, indent=2))
    
    return aggregateKeywordAnalysis(keyword_analysis)


def analyze_tweets_for_keywords(tweets):
    keyword_analysis = []

    tweets_count = len(tweets)
    counter = 1
    for tweet in tweets:
        if counter % 20 == 0:
            print("progress: {}%\t{}/{}".format(counter/tweets_count*100, counter, tweets_count))
        keyword_analysis.append(getKeywordsWithEmotion(tweet))

        counter += 1

    return keyword_analysis

def executionFlow(opinion):
    # 1) open downloaded tweets file
    file_name = '{}_tweets'.format(opinion)
    print("Analyzing {}".format(file_name))
    all_tweets = readFromFile(file_name)

    print("All {} count: {}".format(file_name, len(all_tweets)))
    # 2) take a subset
    tweets = all_tweets[:300]
    print("Taken subset count: {}".format(len(tweets)))
    # 3) produce analysis for them
    data = analyze_tweets_for_keywords(tweets)
    # 4) save to file
    saveToFile(file_name='analyzed_{}'.format(file_name), data=data)


# MAIN
parser = ArgumentParser()
parser.add_argument("-o", "--opinion", dest="opinion",
                    help="provide opinion you wish to analyze data for: remain/no_deal/deal", metavar="FILE")
args = parser.parse_args()

if args.opinion == None or (args.opinion != "remain" and args.opinion != "no_deal" and args.opinion != "deal"):
    print(args.opinion)
    print("You need to provide opinion you want to analyzes the data for: [remain|no_deal|deal].\nUSAGE: 2_2_analyze_tweets_for_keywords.py -o [remain|no_deal|deal]")
else:
    executionFlow(args.opinion)