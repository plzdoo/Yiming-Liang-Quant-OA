from request import get_tweet
from request import get_properties
import sys
import time
import csv
import os


os.environ['TOKEN'] = sys.argv[2]

print(os.environ.get("TOKEN"))

class User:


    def __init__(self,username,followers,name, uid):
        self.username = username
        self.id = uid
        self.followers = followers
        self.name = name
        
        self.top_5_posts = get_tweet(uid)[0]
        self.top_5_retweet = get_tweet(uid)[1]
        

def append_to_csv(users, filename):
    csvFile = open(filename, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    for user in users:


        username = user.username
        uid = user.id
        top_5_posts = user.top_5_posts
        top_5_retweet = user.top_5_retweet
        followers = user.followers
        name = user.name


        res = [username, uid, top_5_posts, top_5_retweet, followers, name]
        csvWriter.writerow(res)

    csvFile.close()




users = []
infile = sys.argv[1]
with open(infile, 'r') as i:
    lines = i.readlines()
rtn = []
for i in lines:
    rtn.append(i.strip())
toR = ""
for j in rtn:
    toR += (j + ',')
usernames = toR.rstrip(toR[-1])



properties = get_properties(usernames)

for user in properties['data']:
    if 'name' in user:
        users.append(User(user['username'], user['public_metrics']['followers_count'], user['name'], user['id']))
        time.sleep(5)

filename = "data.csv"
if len(sys.argv) == 4:
    filename = sys.argv[3]

csvFile = open(filename, "a", newline="", encoding='utf-8')
csvWriter = csv.writer(csvFile)
if os.stat(filename).st_size == 0:
    csvWriter.writerow(['username', 'uid', 'top_5_posts', 'top_5_retweet', 'followers', 'name'])
csvFile.close()


append_to_csv(users, filename)




