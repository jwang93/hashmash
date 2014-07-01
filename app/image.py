import urllib2
import urllib
import simplejson
import cStringIO
from PIL import Image

def read():
    f = open("hashtags.txt", "r")
    text = f.read()
    arr = text.split(',')
    print arr

    for term in arr:
        fetcher = urllib2.build_opener()
        startIndex = 0
        searchUrl = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + term + "&start=" + str(startIndex)
        f = fetcher.open(searchUrl)
        a = simplejson.load(f)  
        imageUrl = a['responseData']['results'][0]['unescapedUrl']
        print imageUrl
        fl = cStringIO.StringIO(urllib.urlopen(imageUrl).read())
        img = Image.open(urllib.urlopen(imageUrl).read())
        img.show()
        # imageUrl = a['responseData']['results'][0]['unescapedUrl']
        # file = cStringIO.StringIO(urllib.urlopen(imageUrl).read())
        # img = Image.open(file)

read()