from argparse import ArgumentParser
import pickle
import csv

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

def writeToCSV(file_name, data):
    PATH = "./data"
    file_name = "{}/{}.csv".format(PATH, file_name)

    with open(file_name, mode='w') as csv_file:
        field_names = ['keyword', 'emotion', 'score']
        print("- csv file headers: {}".format((", ").join(field_names)))
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        writer.writeheader()
        for keyword_object in data:
            writer.writerow(keyword_object)


def get_strongest_emotion(emotion_dict):
    max_score = 0
    max_label = ""
    for label, score in emotion_dict.items():
        if score > max_score:
            max_score = score
            max_label = label

    return max_label, max_score

def executionFlow(opinion):
    # 1) Read input data from file
    print("1) Read input data from file analyzed_{}_tweets.pkl".format(opinion))
    analyzed_tweets = readFromFile('analyzed_{}_tweets'.format(opinion))
    print("- number of tweets to analyze keywords for: {}".format(len(analyzed_tweets)))

    # 2) Structure the data and prepare for further processing (pick only most important emotion)
    print("2) Structure the data and prepare for further processing (pick only most important emotion)")
    structured_data = []
    for tweet_analysis in analyzed_tweets:
        # tweet_analysis contains ultiple keyword objects in an array
        for keyword_analysis in tweet_analysis:
            strongest_emotion_label, strongest_emotion_score = get_strongest_emotion(keyword_analysis['emotion'])

            structured_data.append({
                'keyword': keyword_analysis['keyword'],
                'emotion': strongest_emotion_label,
                'score': strongest_emotion_score,
            })
    print("- number of keywords: {}".format(len(structured_data)))

    # 3) Save to CSV file
    csv_file_name = "keywords_{}".format(opinion)
    print("3) Save to CSV file: {}.csv".format(csv_file_name))
    writeToCSV(csv_file_name, structured_data)
    print("- {} rows written".format(len(structured_data)))



# MAIN
parser = ArgumentParser()
parser.add_argument("-o", "--opinion", dest="opinion",
                    help="provide opinion regarding what analyzed data you want to structure: remain/no_deal/deal", metavar="FILE")
args = parser.parse_args()

if args.opinion == None or (args.opinion != "remain" and args.opinion != "no_deal" and args.opinion != "deal"):
    print(args.opinion)
    print("You need to provide opinion regarding what analyzed data you want to structure: [remain|no_deal|deal].\nUSAGE: 2_3_structure_and_save_keyword_analysis_to_csv.py -o [remain|no_deal|deal]")
else:
    executionFlow(args.opinion)