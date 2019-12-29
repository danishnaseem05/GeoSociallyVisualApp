# Danish Naseem
# CS 1210
# Lab Section A03
# Homework 10
# 5/5/18
#
#######################################################################################################################################################################

import tkinter
import math
import ssl
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus
import json
import twitteraccess as twitter
import flickraccess as flickr
import webbrowser

# To run the program, call the last function in this file: startGUI().


# The Globals class demonstrates a better style of managing "global variables"
# than simply scattering the globals around the code and using "global x" within
# functions to identify a variable as global.
#
# We make all of the variables that we wish to access from various places in the
# program properties of this Globals class.  They get initial values here
# and then can be referenced and set anywhere in the program via code like
# e.g. Globals.zoomLevel = Globals.zoomLevel + 1
#
class Globals:

    rootWindow = None
    mapLabel = None

    defaultLocation = "Mauna Kea, Hawaii"
    mapLocation = defaultLocation
    mapFileName = 'googlemap.gif'
    mapSize = 400
    zoomLevel = 9

# Given a string representing a location, return 2-element tuple
# (latitude, longitude) for that location
#
# See https://developers.google.com/maps/documentation/geocoding/
# for details
#
def geocodeAddress(addressString):
    urlbase = "https://maps.googleapis.com/maps/api/geocode/json?address="
    url = urlbase + quote_plus(addressString)
    #
    # Google's documentation says that should provide an API key with
    # the URL, and tells you how to register for and obtain a free API key
    # I strongly recommend you get one you and then uncomment the line below and replace
    # YOUR-API-KEY with your key.
    # Get one here:
    #   https://developers.google.com/maps/documentation/geocoding/get-api-key
    # IF YOU DO NOT get an API KEY, this code often still works but sometimes
    # you will get "OVER_QUERY_LIMIT" errors from Google.
    #
    url = url + "&key=" + "AIzaSyA1FjRDCJsu62zurQoKTUMYhsEdpYIh0ww"

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    stringResultFromGoogle = urlopen(url, context=ctx).read().decode('utf8')
    jsonResult = json.loads(stringResultFromGoogle)
    if (jsonResult['status'] != "OK"):
        print("Status returned from Google geocoder *not* OK: {}".format(jsonResult['status']))
        return
    loc = jsonResult['results'][0]['geometry']['location']
    return (float(loc['lat']),float(loc['lng']))


# Contruct a Google Static Maps API URL that specifies a map that is:
# - width-by-height in size (in pixels)
# - is centered at latitude lat and longitude long
# - is "zoomed" to the give Google Maps zoom level
#
# See https://developers.google.com/maps/documentation/static-maps/
#
# YOU WILL NEED TO MODIFY THIS TO BE ABLE TO
# 1) DISPLAY A PIN ON THE MAP
# 2) SPECIFY MAP TYPE - terrain vs road vs ...
#
def getMapUrl(width, height, lat, lng, zoom, maptype):

    urlbase = "http://maps.google.com/maps/api/staticmap?"
    args = "center={},{}&zoom={}&size={}x{}&maptype={}&format=gif".format(lat,lng,zoom,width,height,maptype)

    if SearchTermEntry.get() !='':

        twitter.authTwitter()
        topic = SearchTermEntry.get()
        AllTweets = twitter.searchTwitter(topic, latlngcenter=[lat, lng])
        AllImages = flickr.searchFlickr(topic, geo=(lat, lng))

        #green markers for flickr
        for cod in AllImages:
            flickrLat1, flickrLng1 = flickr.photoLoc(cod)
            args = args + ("&markers=color:green%7C{},{}".format(flickrLat1, flickrLng1))

        #if AllTweets['location'][currentTweetnum] !=[]:
                #currrentLocation = AllTweets['location'][currentTweetnum]
                #Lat, Lng = currentLocation
                #args = args + ("&markers=color:red%7C{},{}".format(Lat, Lng))

        #blue markers for twitter
        if AllTweets['location']!=[]:
            for coord in AllTweets['location']:
                Lat1, Lng1 = coord
                args = args + ("&markers=color:blue%7C{},{}".format(Lat1, Lng1))

    return  urlbase+args

# Retrieve a map image via Google Static Maps API:
# - centered at the location specified by global propery mapLocation
# - zoomed according to global property zoomLevel (Google's zoom levels range from 0 to 21)
# - width and height equal to global property mapSize
# Store the returned image in file name specified by global variable mapFileName
#
def retrieveMapFromGoogle():

    def MapType():
        if maptype_value.get()==0:
            return "roadmap"
        elif maptype_value.get()==1:
            return "satellite"
        elif maptype_value.get()==2:
            return "terrain"
        elif maptype_value.get()==3:
            return "hybrid"

    maptype = MapType()

    lat, lng = geocodeAddress(Globals.mapLocation)
    url = getMapUrl(Globals.mapSize, Globals.mapSize, lat, lng, Globals.zoomLevel, maptype)
    urlretrieve(url, Globals.mapFileName)

##########
#  basic GUI code

def displayMap():
    retrieveMapFromGoogle()
    mapImage = tkinter.PhotoImage(file=Globals.mapFileName)
    Globals.mapLabel.configure(image=mapImage)
    # next line necessary to "prevent (image) from being garbage collected" - http://effbot.org/tkinterbook/label.htm
    Globals.mapLabel.mapImage = mapImage

def setCurrentFlickrImage(num):
    global CurrentImageUrl

    topic = SearchTermEntry.get()
    lat, lng = geocodeAddress(Globals.mapLocation)
    resultList = flickr.searchFlickr(topic, geo=(lat, lng))

    currentImagenum = num

    CurrentImageUrl=flickr.photoURL(resultList[currentImagenum])

def displayCurrentImage():
    webbrowser.open(CurrentImageUrl)

def setCurrentTweetUrls(num):
    global currentUrl
    global currentExpandedUrl       
    global currentDisplayUrl

    currentUrlnum = num

    currentUrl = AllTweets['Urls']['url'][currentUrlnum]
    currentExpandedUrl = AllTweets['Urls']['expanded_url'][currentUrlnum]
    currentDisplayUrl = AllTweets['Urls']['display_url'][currentUrlnum]

    UrlText.configure(state=tkinter.NORMAL)
    UrlText.delete(1.0, tkinter.END)
    UrlText.insert(tkinter.INSERT, 'Url: '+currentUrl+'\n')
    UrlText.insert(tkinter.INSERT, 'Expanded Url: '+currentExpandedUrl+'\n')
    UrlText.insert(tkinter.INSERT, 'Display Url: '+currentDisplayUrl+'\n')
    UrlText.configure(state=tkinter.DISABLED)

def openUrl():
    webbrowser.open(currentUrl)
def openExpandedUrl():
    webbrowser.open(currentExpandedUrl)
def openDisplayUrl():
    webbrowser.open(currentDisplayUrl)

def setCurrentTweet(num):
    global AllTweets

    num = int(num)+1
    currentTweetnum = num -2
    twitter.authTwitter()
    twts = SearchTermEntry.get()
    lat, lng = geocodeAddress(Globals.mapLocation)

    AllTweets = twitter.searchTwitter(twts, latlngcenter=[lat, lng])
    currentTweet = AllTweets['texts'][currentTweetnum]

    TweetText.configure(state=tkinter.NORMAL)
    TweetText.delete(1.0, tkinter.END)
    TweetText.insert(tkinter.INSERT, currentTweet)
    TweetText.configure(state=tkinter.DISABLED)

    setCurrentTweetUrls(currentTweetnum)
    setCurrentFlickrImage(currentTweetnum)

def readEntriesSearchTwitterAndDisplayMap():
    #### you should change this function to read from the location from an Entry widget
    #### instead of using the default location

    zoomScale.set(Globals.zoomLevel)
    maplocation = writeEntry.get()
    Globals.mapLocation = maplocation
    displayMap()

def initializeGUIetc():
    global zoomScale
    global writeEntry
    global maptype_value
    global SearchTermEntry
    global TweetText
    global TweetScale
    global UrlText
    global urlButton
    global extendedurlButton
    global displayurlButton
    global ShowFlickrImageButton

    Globals.rootWindow = tkinter.Tk()
    Globals.rootWindow.title("HW10")

    mainFrame = tkinter.Frame(Globals.rootWindow)
    mainFrame.pack()

    # until you add code, pressing this button won't change the map.
    # you need to add an Entry widget that allows you to type in an address
    # The click function should extract the location string from the Entry widget
    # and create the appropriate map.
    maptype_value= tkinter.IntVar()
    maptype_value.set(0)
    maptypes = [("Road",1),("Satellite",2),("Terrain",3),("Hybrid",4)]

    for val, maptype1 in enumerate(maptypes):
        tkinter.Radiobutton(mainFrame,text=maptype1,indicatoron=0,width=20,padx=20,variable=maptype_value,value=val,command=readEntriesSearchTwitterAndDisplayMap).pack(anchor=tkinter.CENTER)

    def zoom(newvalue):
        Globals.zoomLevel=newvalue
        readEntriesSearchTwitterAndDisplayMap()

    zoomScale = tkinter.Scale(mainFrame, orient = tkinter.HORIZONTAL, from_ = 0, to = 21, command=zoom)

    SearchTermLabel = tkinter.Label(mainFrame, text = "Enter the search term: ")
    SearchTermEntry = tkinter.Entry(mainFrame)
    writeEntry = tkinter.Entry(mainFrame)
    EntryLabel = tkinter.Label(mainFrame, text = "Enter the location: ")
    readEntryAndDisplayMapButton = tkinter.Button(mainFrame, text="Show me the map!", command=readEntriesSearchTwitterAndDisplayMap)
    EntryLabel.pack()
    writeEntry.pack()
    SearchTermLabel.pack()
    SearchTermEntry.pack()
    readEntryAndDisplayMapButton.pack()

    TweetText = tkinter.Text(mainFrame, width =30, height = 10)
    TweetScale = tkinter.Scale(mainFrame, orient = tkinter.VERTICAL, command = setCurrentTweet)
    TweetScale.set(0)
    TweetText.pack(side = tkinter.LEFT)
    TweetText.configure(state=tkinter.DISABLED)
    UrlText = tkinter.Text(mainFrame, width = 30, height = 10)
    UrlText.pack(side = tkinter.LEFT)
    UrlText.configure(state=tkinter.DISABLED)
    urlButton = tkinter.Button(mainFrame, text= 'Url', command = openUrl)
    extendedurlButton = tkinter.Button(mainFrame, text= 'Extended Url', command = openExpandedUrl)
    displayurlButton = tkinter.Button(mainFrame, text = 'Display Url', command = openDisplayUrl)
    TweetScale.pack(side = tkinter.LEFT)
    # we use a tkinter Label to display the map image
    Globals.mapLabel = tkinter.Label(mainFrame, width=Globals.mapSize, bd=2, relief=tkinter.FLAT)
    Globals.mapLabel.pack(side = tkinter.RIGHT)
    zoomScale.pack(side=tkinter.BOTTOM)
    urlButton.pack(side=tkinter.LEFT)
    extendedurlButton.pack(side=tkinter.LEFT)
    displayurlButton.pack(side=tkinter.LEFT)
    ShowFlickrImageButton = tkinter.Button(mainFrame, text = 'Current Flickr Image', command = displayCurrentImage)
    ShowFlickrImageButton.pack()

def startGUI():
    initializeGUIetc()
    displayMap()
    Globals.rootWindow.mainloop()
