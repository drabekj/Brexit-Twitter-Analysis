import sys
import os
import time
import twitter
from twitter import TwitterHTTPError
import pickle
from argparse import ArgumentParser

# Twitter API keys
import config

auth = twitter.oauth.OAuth(config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET, config.CONSUMER_KEY, config.CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


def saveToFile(politician_id, data):
    """
    Saves data using pickle to file. File name: {politician_id}.pkl

    Args:
        politician_id: int    user_id of the account to get the followers list for.
    """
    PATH = "./data/followers"
    file_name = "{}/{}.pkl".format(PATH,politician_id)

    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


def get_followers(politician_id):
    """Get a list of all the users ids that follow the account defined by 'politician_id' parameter.

    Args:
        politician_id: int    user_id of the account to get the followers list for.

    Returns:
        list(user_id: int)    Array of integers, which are the followers of the account defined in parameter.
    """
    full_list = []
    print("politician_id: " + str(politician_id))
    
    # get all of the pages of followers user_id s for 
    cursor = -1
    counter = 1
    while cursor != 0:
        try:
            search_results = twitter_api.followers.ids(user_id=politician_id, cursor=cursor)
        except TwitterHTTPError as error:
            print(error)
            return {
                'error': error,
                'counter': counter,
                'unsuccessful_cursor': cursor,
                'incomplete_list': full_list,
            }

        full_list.extend(search_results['ids'])
        cursor = search_results['next_cursor']
        print("#{}\tnext_cursor: {}".format(counter, cursor))

        time.sleep(61) # wait 1 minute, 1 second
        counter += 1
    
    print("~~~ OK ~~~")
    print("~~~ Followers of politician_id={} fetched!".format(politician_id))
    
    # save to file
    print("~~~ saving to file {}.pkl".format(politician_id))
    saveToFile(politician_id=politician_id, data=full_list)
    print("~~~ saved ~~~")
    
    return full_list


# MAIN
parser = ArgumentParser()
parser.add_argument("-id", "--politician_id", dest="id",
                    help="provide politician twitter user id", metavar="FILE")
args = parser.parse_args()

if args.id == None:
    print("You need to provide politician twitter id.\nUSAGE: downloadPfollowers.py -id {politician_id}")
else:
    get_followers(args.id)





