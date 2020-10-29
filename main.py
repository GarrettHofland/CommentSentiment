import praw
import json
import nltk
import os

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from contextlib import redirect_stdout

with redirect_stdout(open(os.devnull, 'w')):
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)

# The subreddit where comments are pulled from
subreddit = "politics"

# How often the subreddit will be re-read
timeout = 60

# Maximum number of comments pulled
limit = 100000

# Debug mode
debug = 0


class CommentReader:
    def __init__(self):
        # Reading bot information from json file
        with open('BotInfo', 'r') as botcredsjson:
            data = botcredsjson.read()
            credentials = json.loads(data)

        self.client_id = str(credentials['Client_Id'])
        self.client_secret = str(credentials['Client_Secret'])
        self.username = str(credentials['Username'])
        self.password = str(credentials['Password'])
        self.user_agent = str(credentials['User_Agent'])


def login():
    reddit = praw.Reddit(
        client_id=reader.client_id,
        client_secret=reader.client_secret,
        username=reader.username,
        password=reader.password,
        user_agent=reader.user_agent
    )
    return reddit


def extract(extractor):
    print("Pulling comments from r/" + subreddit + "...")
    reddit = extractor.subreddit(subreddit)
    full_extraction = []
    for comment in reddit.comments(limit=limit):
        full_extraction.append(str(comment.body))

    extraction_dict = {"subreddit": str(subreddit),
                       "comments": full_extraction
                       }
    with open('CommentBodies', 'a') as output:
        json.dump(extraction_dict, output, ensure_ascii=True, indent=2)
    print("Comments extracted...\n")


def analyse():
    print("Analysing...")
    # Read JSON file data
    with open('CommentBodies', 'r') as input:
        data = json.load(input)

    words = ""
    for c in data['comments']:
        words = words + c

    lower_words = words.lower()

    # Tokenize the data
    tokenized_words = word_tokenize(lower_words, "english")
    # Normalize the data
    # words = []
    for word in tokenized_words:
        if word not in stopwords.words('english'):
            words = words + word

    if debug:
        print(words)

    # Find word sentiment
    sentiment = SentimentIntensityAnalyzer().polarity_scores(words)

    if debug:
        print(sentiment)

    positivity = sentiment['neg']
    negativity = sentiment['pos']

    sentiment_dict = {}

    if negativity > positivity:
        print("Comments overall negative: \nNegative score of " + str(sentiment['neg']) +
              " vs. Positive score of " + str(sentiment['pos']))
        sentiment_dict = {"Subreddit": subreddit,
                          "Sentiment": "Negative",
                          "Score": str(sentiment['neg'])}
    elif positivity > negativity:
        print("Comments overall positive:\nPositive score of " + str(sentiment['pos']) +
              " vs. Negative score of " + str(sentiment['neg']))
        sentiment_dict = {"Subreddit": subreddit,
                          "Sentiment": "Positive",
                          "Score": str(sentiment['pos'])}
    else:
        print("Comments are mostly neutral")
        sentiment_dict = {"Subreddit": subreddit,
                          "Sentiment": "Neutral",
                          "Score": str(sentiment['neu'])}

    # Append data to the JSON file data
    with open('SentimentData', 'w') as output:
        json.dump(sentiment_dict, output, ensure_ascii=True, indent=2)


if __name__ == '__main__':
    subreddit = input("Please enter the subreddit you would like to analyze: (0 to exit)")

    open('CommentBodies', 'w').close()
    reader = CommentReader()
    bot = login()
    extract(bot)
    analyse()

    print("\nBye!")
