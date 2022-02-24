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
# From dotenv import load_dotenv
# load_dotenv()





os.environ['TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAAodZQEAAAAAUGkzpw2W%2BsKQceSFaXjrQNb2jD4%3DWxHtFPZhjz0fsvUIe6vr6dwXJUfLGODkyTH7XKm26EAtNxRqHR'



def auth():
    return os.environ.get("TOKEN")


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


bearer_token = auth()
headers = create_headers(bearer_token)
keyword = "ps5 lang:en"
start_time = "2021-03-01T00:00:00.000Z"
end_time = "2021-03-31T00:00:00.000Z"
max_results = 500
username = "elonmusk"



def create_url(keyword, start_date, end_date, max_results = 10):
    search_url = "https://api.twitter.com/2/users/by"
    # query_params = {'query': keyword,
    #                 'start_time': start_date,
    #                 'end_time': end_date,
    #                 'max_results': max_results,
    #                 'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
    #                 'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
    #                 'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
    #                 'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
    #                 'next_token': {}}
    query_params = {'usernames': username}

    return (search_url, query_params)



def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def append_to_csv(json_response, fileName):
    counter = 0

    csvFile = open(filename, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    for tweet in json_response['data']:
        author_id = tweet['author_id']

        created_at = dateutil.parser.parse(tweet['created_at'])

        if ('geo' in tweet):
            geo = tweet['geo']['place_id']
        else:
            geo = ""

        tweet_id = tweet['id']

        lang = tweet['lang']

        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']

        source = tweet['source']

        text = tweet['text']

        res = [author_id, created_at, geo, tweet_id, lang, like_count, quote_count, reply_count, retweet_count, source, text]

        csvWriter.writerow(res)
        counter += 1

    csvFile.close()

    print("# of Tweets added from this response: ", counter)





total_tweets = 0

csvFile = open("data.csv", "a", newline="", encoding='utf-8')
csvWriter = csv.writer(csvFile)

csvWriter.writerow(['author id', 'created_at', 'geo', 'id','lang', 'like_count', 'quote_count', 'reply_count','retweet_count','source','tweet'])
csvFile.close()

count = 0
max_count = 100
flag = True
next_token = None




# while flag:
#     if count >= max_count:
#         break
#     print("--------------")
#     print("Token: ", next_token)

#     url = create_url(keyword, start_time, end_time, max_results)
#     json_response = connect_to_endpoint(url[0], headers, url[1], next_token)

#     result_count = json_response['meta']['result_count']

#     if 'next_token' in json_response['meta']:
#         next_token = json_response['meta']['next_token']
#         print("Next Token: ", next_token)

#         if result_count is not None and result_count > 0 and next_token is not None:
#             append_to_csv(json_response, "data.csv")
#             count += result_count
#             total_tweets += result_count
#             time.sleep(5)

#     else:
#         if result_count is not None and result_count > 0:
#             append_to_csv(json_response, "data.csv")

#             count += result_count
#             total_tweets += result_count
#             time.sleep(5)

#         flag = False

#         next_token = None


#     time.sleep(5)

