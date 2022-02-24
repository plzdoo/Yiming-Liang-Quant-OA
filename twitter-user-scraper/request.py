import fileinput
# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time
import sys
# From dotenv import load_dotenv
# load_dotenv()
import heapq
from collections import defaultdict








def auth():
    return os.environ.get("TOKEN")


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers
#
# this function connect to the endpoint that you want to connected to
#
def connect_to_endpoint(url, headers, params, method="GET", next_token=None):
    params['pagination_token'] = next_token
    response = requests.request(method, url, headers=headers, params=params, timeout=10)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#
# this function get all the properties of a twitter by passing in the username of a user
#

def get_properties(usernames):
    user_url = "https://api.twitter.com/2/users/by"
    params = {'usernames':usernames,
             'user.fields':'public_metrics,id'}
    headers = create_headers(auth())

    response = connect_to_endpoint(user_url,headers,params)
    return response

#
# this function return the information of top 5 most retweet post of a user and top 5 most-retweeted posts that the user retweets.
#

def get_tweet(input):
    tweet = []
    retweet = []
    url = "https://api.twitter.com/2/users/%s/tweets" % input

    headers = create_headers(auth())
    next_token = None 
    flag = True
    d = defaultdict(int)
    max_result = 0
    while flag:
        params = {'tweet.fields':'public_metrics,entities',
              'max_results':'100'}
        response = connect_to_endpoint(url, headers, params, next_token=next_token)
        result_count = response['meta']['result_count']
        if result_count != 0:
            for i in response['data']:
                text = i['text']
                if text.startswith("RT @") != True:
                    count = i['public_metrics']['retweet_count']
                    if len(tweet) > 5:
                        heapq.heappushpop(tweet, (count, text))
                    else:
                        heapq.heappush(tweet, (count, text))
                    if 'entities' in 'hashtags':
                        if 'hashtags' in i['entities']:
                            d[i['entities']['hashtags']['tag']] += 1
                else:
                    count = i['public_metrics']['retweet_count']
                    if len(retweet) > 5:
                        heapq.heappushpop(retweet, (count, text))
                    else:
                        heapq.heappush(retweet, (count, text))

            if 'next_token' in response['meta']:
                next_token = response['meta']['next_token']
            else:
                flag = False
        max_result += result_count
        if max_result > 3000:
            break
    return [tweet, retweet,d]
