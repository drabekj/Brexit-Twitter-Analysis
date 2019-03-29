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
        
# USAGE:
# saveToFile(file_name=79801266, data=followers_list)

def readFromFile(file_name):
    """
    Loads data from pickled file in the directory ./data
    
    Args:
        file_name: string

    Returns:
        data
    """
    PATH = "./data"
    file_path = "{}/{}".format(PATH, file_name)
    with open(file_path, 'rb') as f:
        data = pickle.load(f)

    return data

def formula(user_follows_opinion, total_followers_opinion, metadata):
    """
    Calculate the score for single user for one opinion. All data in this function should be regarding only one single opinion (deal, no_deal, remain).
    
    Args:
        user_follows_opinion:    [politician_id: int]    list of politician ids OF THE ONE OPINION the user follows
        total_followers_opinion: int                     total followers of all the politicians of THAT ONE OPINION
    
    Return:
        score: int    Preference score of that user of that single opinion.
    """
    score = 0

    for politician in user_follows_opinion:
        score += 1 - (metadata['individual_follower_count'][politician]/total_followers_opinion)
    return score


def user_preferences(follows, metadata):
    """
    Calculate the preference score for each of the opinions.
    
    Args:
        follows:  [politician_id1, ...]    List of all the politician ids the person follows.
        metadata: object defined as below
            {
                'total_follower_count': {
                    'deal': int,
                    'no_deal': int,
                    'remain': int,
                },
                'individual_follower_count': {politician_id: followers}
            }
    
    Return:
        {deal, no_deal, remain}:    {float, float, float}    Returns deict of normalized preference score for the 3 opinions.
    """
    follows = set(follows)
    politicians_deal = {595416920, 2797521996, 211994193, 160952087, 810372954, 2653613168, 747807250819981312}
    politicians_no_deal = {761499948890329088, 3131144855, 19017675, 79801266, 319675272, 2425571623, 14190551, 117777690}
    politicians_remain = {22520698, 18096679, 19973305, 460401829, 354911386, 36924726, 19397942}
    deal_total_followers = metadata['total_follower_count']['deal']
    no_deal_total_followers = metadata['total_follower_count']['no_deal']
    remain_total_followers = metadata['total_follower_count']['remain']
    
    # separate follows into the 3 buckets (find intersections)
    follows_deal = set.intersection(follows, politicians_deal)
    follows_no_deal = set.intersection(follows, politicians_no_deal)
    follows_remain = set.intersection(follows, politicians_remain)
    
    # deal score
    score_deal = formula(
        user_follows_opinion=follows_deal,
        total_followers_opinion=deal_total_followers,
        metadata=metadata
    )
#     print("deal_score:\t{}".format(score_deal))
    
    # no_deal score
    score_no_deal = formula(
        user_follows_opinion=follows_no_deal,
        total_followers_opinion=no_deal_total_followers,
        metadata=metadata
    )
#     print("score_no_deal:\t{}".format(score_no_deal))
    
    # remain score
    score_remain = formula(
        user_follows_opinion=follows_remain,
        total_followers_opinion=remain_total_followers,
        metadata=metadata
    )
#     print("score_remain:\t{}".format(score_remain))
    
    # normalize
    # score_total = score_deal + score_no_deal + score_remain
    # score_deal_n = score_deal / score_total
    # score_no_deal_n = score_no_deal / score_total
    # score_remain_n = score_remain / score_total
    
#     print("normalized: deal={}\tno_deal={}\tremain={}".format(score_deal_n, score_no_deal_n, score_remain_n))
    return {
        'deal': score_deal,
        'no_deal': score_no_deal,
        'remain': score_remain,
    }


def calc_preferences(data, metadata):
    """
    For every user in the data structure, calculate the preference scores for all 3 options.
    
    Args:
        data: object        array of key,value pairs, where key  is the user_id and value is an array of the politician ids the user follows.
        metadata: object    contains information about total followers across opinions and follower counts of individual politicians (from file).
        
    Return:
        data: object {user_id: {remain: float, no_deal: float, deal: float}, ...}
            Scores of remain, no_deal, deal are normalized from interval <0,1>
    """
    scored_users = {}
    data_len = len(data)
    
    counter = 0
    for user_id, follows_array in data.items():
        if counter % 100000 == 0:
            print("progress: {:.2f}% \t{}/{}".format(counter/data_len*100, counter, data_len))

#         print('id: {}\tfollows:{}'.format(user_id, follows))
        scores = user_preferences(follows_array, metadata)
        scored_users[user_id] = scores
        counter += 1
    
    return scored_users


def calc_and_save_preference_scores(data_file_name):
    """
    Calculates the scores from all the provided users (with follows array) and saves it into a file 'scored_users.pkl'.
    """
    # get data from file 'user_follows_politicians_dict.pkl'
    data = readFromFile(data_file_name)

    # "res" is testing dummy data 
    # data = {
    #     123124135: [211994193, 2797521996, 595416920, 761499948890329088],
    #     931847831: [19017675],
    #     240958912: [460401829, 2797521996, 19397942, 761499948890329088],
    # }
    
    metadata = readFromFile('metadata')
    scored_users_array = calc_preferences(data, metadata)
    saveToFile(file_name='scored_users_not_norm', data=scored_users_array)
    
# usage calc_and_save_preference_scores(data)


# MAIN
file_name = 'user_follows_politicians_dict.pkl'
print("~~~ Starting to calculate scores ~~~")
calc_and_save_preference_scores(file_name)
print("~~~ Scores calculated & saved to file scored_users.pkl ~~~")