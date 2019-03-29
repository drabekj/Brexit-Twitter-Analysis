# Brexit-Twitter-Analysis
Analysis of the followers of 21 of the most prominent British politicians and their followers. Calculating the preferences score towards opinion on the Brexit situation: Deal, No-Deal, Remain. On top of that, sentiment analysis of the most common keywords ind the users political tweets and their sentiment.

## Users political opinion
Get followers for the 21 most prominentBritish politicians and based on who they follow assign a preferences score towards opinion on the Brexit situation: Deal, No-Deal, Remain.

### 1) run 1_1_download_followers.py
Download followers ids for a politician. This script needs to be executed for each of the politicians by providing their twitter user id.
- USAGE: python3 1_1_download_followers.py -id {politician_id}
- OUTPUT: file {politician_id}.pkl in data/followers folder with list of follower ids

### 2) run 1_2_build_user_follows_dict.py
Build a dictioonary of users and the politicians who they follow.
- USAGE: python3 1_2_build_user_follows_dict.py
- INPUT: reads all the files in data/followers folder
- OUTPUT: file user_follows_politicians_dict.pkl in data folder with list of follower ids
  - format: distionary where key={user_id} value=[list of politicians the user follows]

### 3) run 1_3_create_politicians_metadata.py
Create metadata file with followers count for: opinion (remain, no_deal, deal), individual politicians. Having this makes the execution of the next step much faster.
- USAGE: python3 1_3_create_politicians_metadata.py
- OUTPUT: file followers_metadata.pkl in data folder

### 4) run 1_4_calc_scores.py
Calculates the preferences score towards opinion on the Brexit situation: Deal, No-Deal, Remain for every single user that was identified as a follower of any of the politiians.
- USAGE: python3 1_4_calc_scores.py
- INPUT:
  - user_follows_politicians_dict.pkl from Step 2)
  - followers_metadata.pkl from Step 3)
- OUTPUT: scored_users.pkl file containing list of user ids each with assigned score for every opinion (deal, no_deal, remain).

## Keyword Analysis (Sentiment Analysis)
How to run the scripts
### 1) run 2_1_prepare_tweets_for_sentiment_analysis.py -o [deal|no_deal|remain]
Input:
- argument -o [deal|no_deal|remain]
- "scored_users_not_norm.pkl"
Output:
- file with relevant tweets for each opinion: "deal_tweets.pkl", "no_deal_tweets.pkl", "remain_tweets.pkl"

What does it do?
- !!! this scipt should be run 3 times (once for every opinion category deal|no_deal|remain)
  - because of API limits, wait 15 mins between individual executions
- based on "scored_users_not_norm.pkl" input file creates a list of twitter users that represent each opinion (not politicians)
- downloads the tweets of these users if possible
- !!! filters the downloaded tweets and keeps only the political onse
  - containing specified keywords, and politicians twitter handles
- saves into a pockeled file "deal_tweets.pkl", "no_deal_tweets.pkl", "remain_tweets.pkl"

### 2) run 2_2_analyze_tweets_for_keywords.py
Input:
- MANUALLY:
  - change the variable 'opinion_to_analyze' to one of [deal|no_deal|remain]
  - subset variable (if you don't want to run the analysis on all the tweets)
- based on previous choice reads file [deal_tweets.pkl|no_deal_tweets.pkl|remain_tweets.pkl]
Output:
  - based on previous choice reads file [analyzed_tweets_deal.pkl|analyzed_tweets_no_deal.pkl|analyzed_tweets_remain.pkl]

What does it do?
- Queries the IBM watson for the selected subset of tweets, one by one (tweets are provided form input file)
- Saves keyword analysis as list of lists of keyword_analysis objects into a file [analyzed_tweets_deal.pkl|analyzed_tweets_no_deal.pkl|analyzed_tweets_remain.pkl]


### 3) run 2_3_structure_and_save_keyword_analysis_to_csv.py
Input:
- MANUALLY:
  - change the variable 'opinion_to_analyze' to one of [deal|no_deal|remain]
Output:
- csv file (keyword, emotion, score):  [keywords_deal.csv|keywords_no_deal.csv|keywords_remain.csv]

What does it do?
- From the provided input file takes the analysis and picks out the most important information (like the strongest emotion associated with each keyword)
- Saves the most important information to a csv file [keywords_deal.csv|keywords_no_deal.csv|keywords_remain.csv]
