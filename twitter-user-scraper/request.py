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

def connect_to_endpoint(url, headers, params, method="GET", next_token=None):
    params['pagination_token'] = next_token
    # try:
    response = requests.request(method, url, headers=headers, params=params, timeout=10)
    # except requests.exceptions.Timeout as e:
    #     print(e)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def parse_json(response):
    rtn = []
    for user in response['data']:
        id = user['id']
        # follwers = user['followers_count']
        rtn.append(id)
    return rtn

def test(usernames):
    user_url = "https://api.twitter.com/2/users/by"
    # usernames = parse_input()
    params = {'usernames':usernames,
             'user.fields':'public_metrics,id'}
    headers = create_headers(auth())

    response = connect_to_endpoint(user_url,headers,params)
    return response


def get_tweet(input):
    tweet = []
    retweet = []
    url = "https://api.twitter.com/2/users/%s/tweets" % input
    # params = {'tweet.fields':'public_metrics',
    #           'max_results':'5'}

    headers = create_headers(auth())
    next_token = None 
    flag = True
    d = defaultdict(int)
    max_result = 0
    while flag:
        params = {'tweet.fields':'public_metrics,entities',
              'max_results':'100'}
            #   'pagination_token':next_token
        response = connect_to_endpoint(url, headers, params, next_token=next_token)
        
        # print(response)
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




def parse_input():
    infile = sys.argv[1]
    with open(infile, 'r') as i:
        lines = i.readlines()
    rtn = []
    for i in lines:
        rtn.append(i.strip())
    toR = ""
    for j in rtn:
        toR += (j + ',')
    toR = toR.rstrip(toR[-1])
    return(toR)

