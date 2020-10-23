import praw
import json
import nltk
import re
from googlesearch import search

# The subreddit where comments are pulled from
subreddit = "politics"

# How often the subreddit will be re-read
timeout = 60

# Maximum number of comments pulled
limit = 10


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

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_user_agent(self):
        return self.user_agent


def login():
    reddit = praw.Reddit(
        client_id=reader.get_client_id(),
        client_secret=reader.get_client_secret(),
        username=reader.get_username(),
        password=reader.get_password(),
        user_agent=reader.get_user_agent()
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
    # Read the json file

    # Tokenize the data

    # Normalize the data

    # Remove noise from the data

    # Find word density

    # Prepare the data for the model


if __name__ == '__main__':
    # Empty the output file to ensure data cleanliness
    open('CommentBodies', 'w').close()
    reader = CommentReader()
    bot = login()
    extract(bot)
    analyse()
