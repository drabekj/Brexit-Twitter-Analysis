import os
import pickle

def saveToFile(file_name, data):
    """
    Saves data using pickle to file. File name: {file_name}.pkl

    Args:
        file_name: sting    the name of the file without .pkl extension
    """
    PATH = "./data"
    file_name = "{}/{}.pkl".format(PATH, file_name)

    with open(file_name, 'wb') as f:
        pickle.dump(data, f, protocol=2)

def readFromFile(politician_id):
    """
    Loads data prom pickled file. File name: {politician_id}.pkl
        Args:
        politician_id: int    user_id of the account to get the followers list for.

    Returns:
        list(user_id: int)    Array of integers, which are the followers of the account defined in parameter.
    """
    PATH = "./data/followers"
    file_name = "{}/{}.pkl".format(PATH, politician_id)

    with open(file_name, 'rb') as f:
        data = pickle.load(f)

    return data


def sum_file_list_lengths(ids_list):
    len_individual = {}
    len_sum = 0
    for politician_id in ids_list:
        data = readFromFile(politician_id)
        len_individual[politician_id] = len(data)
        len_sum += len(data)
    
    return len_sum, len_individual


# MAIN
"""
Creates metadata-file that speeds up the next step of calculating the political opinion scores for every user.
The metadata-file contains information on what is the political opinion of that political account,
how many followers does each opinion have in total (sum across politicians of that opinion) and
how many followers does each individual politician have.
"""

# politicians lists by opinion
politicians_deal = {595416920, 2797521996, 211994193, 160952087, 810372954, 2653613168, 747807250819981312}
politicians_no_deal = {761499948890329088, 3131144855, 19017675, 79801266, 319675272, 2425571623, 14190551, 117777690}
politicians_remain = {22520698, 18096679, 19973305, 460401829, 354911386, 36924726, 19397942}

deal_follower_count, deal_individual = sum_file_list_lengths(politicians_deal)
no_deal_follower_count, no_deal_individual = sum_file_list_lengths(politicians_no_deal)
remain_follower_count, remain_individual = sum_file_list_lengths(politicians_remain)

data = {
    'total_follower_count': {
        'deal': deal_follower_count,
        'no_deal': no_deal_follower_count,
        'remain': remain_follower_count,
    },
    'individual_follower_count': {**deal_individual, **no_deal_individual, **remain_individual}
}

saveToFile('followers_metadata', data)