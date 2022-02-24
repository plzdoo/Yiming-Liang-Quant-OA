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

import request


os.environ['TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAAodZQEAAAAAUGkzpw2W%2BsKQceSFaXjrQNb2jD4%3DWxHtFPZhjz0fsvUIe6vr6dwXJUfLGODkyTH7XKm26EAtNxRqHR'



def auth():
    return os.environ.get("TOKEN")


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


bearer_token = auth()
headers = create_headers(bearer_token)
username = "elonmusk"


search_url = "https://api.twitter.com/2/users/by"
query_params = {'usernames': username,
                'expansions':'pinned_tweet_id',
                'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',}

# def connect_to_endpoint(url, headers, params):
#     response = requests.request("GET", url, headers=headers,params=params)
#     print("Endpoint Response Code: " + str(response.status_code))
#     if response.status_code != 200:
#         raise Exception(response.status_code, response.text)
#     return response.json()

# json_response = connect_to_endpoint(search_url,headers, query_params)

response = requests.request("GET", 'https://api.twitter.com/2/tweets/search/recent?query=from%3Atwitterdev&tweet.fields=public_metrics', headers=headers)


print(response.json())