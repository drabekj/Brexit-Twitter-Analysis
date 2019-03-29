import pickle

def readFromFile(file_name):
    """
    Loads data from pickled file. File name: {politician_id}.pkl
        Args:
        politician_id: int    user_id of the account to get the followers list for.

    Returns:
        list(user_id: int)    Array of integers, which are the followers of the account defined in parameter.
    """
    
    with open(r"../data" + "/" + file_name, 'rb') as f:
        data = pickle.load(f)

    return data

data = readFromFile("user_follows_politicians_dict.pkl")
print(data)