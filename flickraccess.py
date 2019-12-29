# Danish Naseem
# CS 1210
# Lab Section A03
# Homework 10
# 5/5/18
#
# ######################################################################################################################################################################

import json
import ssl
import webbrowser
from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen, urlretrieve

flickrAPIKey = "068036131629b5dcdea557b5ed4a6566"

# Try things like:
#
# resultList = searchFlickr("kitten")
# showFlickrPhoto(resultList[0])
# showFlickrPhotoPage(resultList[0])
#
# resultList = searchFlickr("herky", geo=(41.6611277, -91.5301683))
# showFlickrPhoto(resultList[0])
# showFlickrPhotoPage(resultList[0])
# photoLoc(resultList[0])

def search_flickr(topic, geo = None, maxNum = 20, radius = 2):
    global url, resultFromFlickr, jsonresult, flickrPhotos
    base = "https://api.flickr.com/services/rest/?"
    args = "method = flickr.photos.search&format = json&per_page = {}&nojsoncallback = 1".format(maxNum)
    topicPart = "&text = " + quote_plus(topic)

    noVerifyContext = ssl.create_default_context()
    noVerifyContext.check_hostname = False
    noVerifyContext.verify_mode = ssl.CERT_NONE

    url = base + args + topicPart + "&api_key = " + flickrAPIKey
    if geo != None:
        geoPart = "&lat = {}&lon = {}&radius = {}".format(geo[0], geo[1], radius)
        url = url + geoPart

    resultFromFlickr = urlopen(url, context = noVerifyContext).read().decode('utf8')
    jsonresult = json.loads(resultFromFlickr)
    if jsonresult['stat'] == 'ok':
        flickrPhotos = jsonresult['photos']['photo']
        print("{} photos found".format(len(flickrPhotos)))
        return flickrPhotos
    else:
        print("status returned from Flickr not ok")

def photo_url(photoListItem):
    farmId = photoListItem['farm']
    serverId = photoListItem['server']
    photoId = photoListItem['id']
    secret = photoListItem['secret']
    url = "https://farm{}.staticflickr.com/{}/{}_{}.jpg".format(farmId, serverId, photoId, secret)
    return url

def photo_loc(photoListItem):
    global photoI
    base = "https://api.flickr.com/services/rest/?"
    args = "method = flickr.photos.getInfo&format = json&nojsoncallback = 1"
    idPart = "&photo_id = " + photoListItem['id']
    url = base + args + idPart + "&api_key = " + flickrAPIKey
    noVerifyContext = ssl.create_default_context()
    noVerifyContext.check_hostname = False
    noVerifyContext.verify_mode = ssl.CERT_NONE
    resultFromFlickr = urlopen(url, context = noVerifyContext).read().decode('utf8')
    photoI = json.loads(resultFromFlickr)
    photoI = photoI['photo']
    loc = photoI['location']
    lat = float(loc['latitude'])
    lon = float(loc['longitude'])
    return (lat, lon)

def photo_info(photoListItem):
    global photoI
    base = "https://api.flickr.com/services/rest/?"
    args = "method = flickr.photos.getInfo&format = json&nojsoncallback = 1"
    idPart = "&photo_id = " + photoListItem['id']
    url = base + args + idPart + "&api_key = " + flickrAPIKey
    noVerifyContext = ssl.create_default_context()
    noVerifyContext.check_hostname = False
    noVerifyContext.verify_mode = ssl.CERT_NONE
    resultFromFlickr = urlopen(url, context = noVerifyContext).read().decode('utf8')
    photoI = json.loads(resultFromFlickr)
    return photoI

def show_flickr_photo(photoListItem):
    webbrowser.open(photo_url(photoListItem))

def show_flickr_photo_page(photoListItem):
    pI = photo_info(photoListItem)
    pageURL = pI['photo']['urls']['url'][0]['_content']
    print(pageURL)
    webbrowser.open(pageURL)
