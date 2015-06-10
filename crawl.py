# -*-coding: utf-8 -*-
import os
import sys
import time
from urllib import FancyURLopener
import urllib
import urllib2
import json

# Define search term
searchTerm = u'mapodoufu'

# Replace spaces ' ' in search term for '%20' in order to comply with request
searchTerm = searchTerm.replace(' ','%20')


# Start FancyURLopener with defined version 
class MyOpener(FancyURLopener): 
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
myopener = MyOpener()

# Set count to 0
count= 64

for i in range(0,100):
    # Notice that the start changes for each iteration in order to request a new set of images for each loop
    url = (u'https://ajax.googleapis.com/ajax/services/search/images?' + u'v=1.0&q='+searchTerm+u'&start='+str(64+i*4)+u'&userip=MyIP')
    print url
    #url = url.encode('utf-8')
    #print 'utf8:', url
    request = urllib2.Request(url, None, {'Referer': 'testing'})
    response = urllib2.urlopen(request)

    # Get results using JSON
    results = json.load(response)
    data = results['responseData']
    dataInfo = data['results']

    # Iterate for each result and get unescaped url
    for myUrl in dataInfo:
        count = count + 1
        print myUrl['unescapedUrl']

        myopener.retrieve(myUrl['unescapedUrl'], str(count)+'.jpg')

    # Sleep for one second to prevent IP blocking from Google
    time.sleep(1)