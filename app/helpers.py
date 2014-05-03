import requests
import unicodedata 
import string 
from termcolor import colored
import simplejson as json
import csv 
from operator import itemgetter
from bs4 import BeautifulSoup


default = ""


def main(name, filename): 
    print "Big Move"
    hashtag_list = []
    hashtag_dict = {}
    sorted_hashtag_list = []    
    name = name.strip()
    url = 'http://instagram.com/' + name
    response = requests.get(url)
    html_content = response.text 
    soup = BeautifulSoup(html_content)
    JSON = "";

    for n in soup.find_all('script'):
        n = str(unicode(n))
        if ('window._sharedData' in n):
            JSON = n

    length = len(JSON)
    JSON = JSON[52:length-10]


    temp = json.loads(JSON)


    """
    json_file = open("sophia.json", "w")
    json_file.write(JSON)
    """

    photos = temp['entry_data']['UserProfile'][0]["userMedia"]



    for index, photo in enumerate(photos):
        likes = processLikes(photo)
        caption = processCaption(photo)
        location = processLocation(photo)
        hashtags = processHashtags(photo, hashtag_list)
        addToDict(likes, hashtags, hashtag_dict)

    sorted_hashtag_list = sorted(hashtag_dict.items(), key=itemgetter(1))
    sorted_hashtag_list.reverse()
    print sorted_hashtag_list
    writeToCSV(name, sorted_hashtag_list, filename)
    hashtag_list = []
    hashtag_dict = {}
    sorted_hashtag_list = []

def writeToCSV(user, sorted_hashtag_list, filename):
    csv_name = 'csvs/' + filename + '.csv'
    with open(csv_name, 'ab') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #writer.writerow(['#'] + ['likes'] + ['caption'] + ['location'] + ['hashtags'])
        print type(sorted_hashtag_list)
        print len(sorted_hashtag_list)
        writer.writerow([user])
        for index, hashtag_tuple in enumerate(sorted_hashtag_list):
            print hashtag_tuple
            writer.writerow([str(index+1)] + [str(hashtag_tuple[0])] + [str(hashtag_tuple[1])])
        writer.writerow([])


def checkUnicode(str):
	if str is None:
		return ""
	if (not str):
		return ""
	if type(str) == str:
	    str = unicode(str, "utf-8", errors="ignore")
	else:
	    str = unicode(str)
	return unicodedata.normalize('NFKD', str).encode('ascii', 'ignore')


def processLikes(photo):
    return checkUnicode([photo["likes"]["count"]])

def processCaption(photo):
    if (photo["caption"] is None):
        caption = ""
    else: 
        caption = checkUnicode([photo["caption"].get("text", default)])
    return caption	

def processLocation(photo):
    if (photo["location"] is None):
        location = ""
    else:
        location = checkUnicode([photo["location"].get("name", default)])
    return location	

def processHashtags(photo, hashtag_list):
    caption = processCaption(photo)
    if caption == "":
        return []
    caption = caption[3:len(caption)-2]
    words = caption.split(' ')

    [word.strip() for word in words]

    hashtags = []
    for word in words:
        if len(word) == 0:
            continue
        if word[0] == '#':
            word = cleanWord(word)
            hashtags.append(word)
            hashtag_list.append(word)
    return hashtags

def addToDict(likes, hashtags, hashtag_dict):
    likes = int(likes[1:len(likes)-1])
    for ht in hashtags:
        if hashtag_dict.has_key(ht):
            hashtag_dict[ht] += likes
        else:
            hashtag_dict[ht] = likes

def cleanWord(word):
    separators = ['\\', ',', '.', '"']
    for sep in separators:
        word = word.split(sep, 1)[0]
    return word.lower()
