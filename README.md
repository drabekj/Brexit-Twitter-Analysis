# Brexit-Twitter-Analysis
Analysis of the followers of 21 of the most prominent British politicians and their followers. Calculating the preferences score towards opinion on the Brexit situation: Deal, No-Deal, Remain. On top of that, sentiment analysis of the most common keywords ind the users political tweets and their sentiment.


## Keyword Analysis (Sentiment Analysis)
How to run the scripts
## 1) run 2_1_prepare_tweets_for_sentiment_analysis.py -o [deal|no_deal|remain]
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

## 2) run 2_2_analyze_tweets_for_keywords.py
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


## 3) run 2_3_structure_and_save_keyword_analysis_to_csv.py
Input:
	- MANUALLY:
                - change the variable 'opinion_to_analyze' to one of [deal|no_deal|remain]
Output:
	- csv file (keyword, emotion, score):  [keywords_deal.csv|keywords_no_deal.csv|keywords_remain.csv]

What does it do?
- From the provided input file takes the analysis and picks out the most important information (like the strongest emotion associated with each keyword)
- Saves the most important information to a csv file [keywords_deal.csv|keywords_no_deal.csv|keywords_remain.csv]
