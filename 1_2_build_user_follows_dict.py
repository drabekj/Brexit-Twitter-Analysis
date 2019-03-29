import os
import pickle


def read_pickles():
    users=[]
    for fi in os.listdir(r"./data/followers"):
        users.extend(readFromFile(fi))
    
    return list(set(users))
       

def readFromFile(file_name):
    """
    Loads data from pickled file. File name: {politician_id}.pkl
        Args:
        politician_id: int    user_id of the account to get the followers list for.

    Returns:
        list(user_id: int)    Array of integers, which are the followers of the account defined in parameter.
    """
    
    with open(r"./data/followers" + "//" + file_name, 'rb') as f:
        data = pickle.load(f)

    return data



def saveToFile(data):
    """
    Saves data using pickle to file. File name: {politician_id}.pkl

    """
    PATH = "./data"
    file_name = "{}/user_follows_politicians_dict.pkl".format(PATH)

    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


def merge_followers(users):
    """
    Reads the political followers files for user ids and aggregates them into a distionary where
    the key is the user id and the value is a list of politicians ids the user follows.
    """
    result={}    
    pol_followers={} # dictionary key={file_name} value={list of followers}
    for fi in os.listdir(r"./data/followers"):
        pol_followers[os.path.splitext(fi)[0]]=set(readFromFile(fi))
    
    print("~~~ start looking through sets")
    counter=0
    for u in users:
        if counter % 10000 == 0:
            print("progress: {:.2f}% \t{}/{}".format(counter/len(users)*100, counter, len(users)))

        for pol in pol_followers.keys():
            if u in pol_followers[pol]:
                try:
                    result[u].append(pol)
                except KeyError:
                    result[u]=[pol]
        counter+=1
    
    print("progress: 100%")
    return result



all_users=read_pickles()
res=merge_followers(all_users)
saveToFile(res)



