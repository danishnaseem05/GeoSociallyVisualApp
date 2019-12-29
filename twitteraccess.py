# Danish Naseem
# CS 1210
# Lab Section A03
# Homework 10
# 5/5/18
#
# ######################################################################################################################################################################

import json
from urllib.parse import quote_plus
import oauth2 as oauth

#
# The code in this file won't work until you set up your Twitter "app"
# at https://dev.twitter.com/apps
# After you set up the app, copy the four long messy strings and put them here.
#

CONSUMER_KEY = "gNNmgjK3JhXx6zOylHT9q0ZuA"
CONSUMER_SECRET = "RQSkRdchVFS7DJZYv2jK9m9SgtvAFNXAJfTASn2y0uTufvwFvj"
ACCESS_KEY = "349904406-JoTypeDjILuFJtbQ9RjOVbKxcMw7odBC37Li28uX"
ACCESS_SECRET = "xrGt7tEXNRPwxezbtypmgITCCC9eVHgGWkTxkkrf0kvrF"

# Call this function after starting Python.  It creates a Twitter client object (in variable client)
# that is authorized (based on your account credentials and the keys above) to talk
# to the Twitter API. You won't be able to use the other functions in this file until you've
# called authTwitter()
#
def auth_twitter():

    global client
    consumer = oauth.Consumer(key = CONSUMER_KEY, secret = CONSUMER_SECRET)
    access_token = oauth.Token(key = ACCESS_KEY, secret = ACCESS_SECRET)
    client = oauth.Client(consumer, access_token)


# Study the documenation at https://dev.twitter.com/rest/public/search
# to learn about construction Twitter queries and the format of the results
# returned by Twitter
#

# Try:
#       searchTwitter("finals")
#
# Iowa City's lat/lng is [41.6611277, -91.5301683] so also try:
#      searchTwitter("finals", latlngcenter=[41.6611277, -91.5301683])
#
def search_twitter(searchString, count = 20, radius = 2, latlngcenter = None):
    global query
    global response
    global data
    global resultDict
    global tweets

    query = "https://api.twitter.com/1.1/search/tweets.json?q = " + quote_plus(searchString) + "&count = " + str(count)

    if latlngcenter != None:
        query = query + "&geocode = " + str(latlngcenter[0]) + ", " + str(latlngcenter[1]) + ", " + str(radius) + "km"

    response, data = client.request(query)
    data = data.decode('utf8')
    resultDict = json.loads(data)

    # The key information in resultDict is the value associated with key 'statuses' (Twitter refers to
    # tweets as 'statuses'
    Result = {}
    tweets = resultDict['statuses']
    for tweet in tweets:
        if Result == {}:
            Result['texts'] = []
            Result['location'] = []
            Result['Urls'] = {'url':[], 'expanded_url':[], 'display_url':[]}
        else:
            if tweet['coordinates'] != None:
                Result['location'].append(tweet['geo']['coordinates'])
                Result['texts'].append(printable(tweet['text']))
                if tweet['entities']['urls'] != None:
                    for d in tweet["entities"]["urls"]:
                        Result['Urls']['url'].append(printable(d['url']))
                        Result['Urls']['expanded_url'].append(printable(d['expanded_url']))
                        Result['Urls']['display_url'].append(printable(d['display_url']))
            else:
                Result['texts'].append(printable(tweet['text']))
                if tweet['entities']['urls'] != None:
                    for d in tweet["entities"]['urls']:
                        Result['Urls']['url'].append(printable(d['url']))
                        Result['Urls']['expanded_url'].append(printable(d['expanded_url']))
                        Result['Urls']['display_url'].append(printable(d['display_url']))
    return Result

def who_is_followed_by(screenName):
    global response
    global resultDict

    query = "https://api.twitter.com/1.1/friends/list.json?&count = 50"
    query = query + "&screen_name = {}".format(screenName)
    response, data = client.request(query)
    data = data.decode('utf8')
    resultDict = json.loads(data)
    for person in resultDict['users']:
        print(person['screen_name'])

def get_my_recent_tweets():
    global response
    global data
    global statusList
    query = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    response, data = client.request(query)
    data = data.decode('utf8')
    statusList = json.loads(data)
    for tweet in statusList:
        print(printable(tweet['text']))
        print()

def printable(s):
    result = ''
    for c in s:
        result = result + (c if c <= '\uffff' else '?')
    return result
