import requests
import unicodedata 
import string 
from termcolor import colored
import simplejson as json
import csv 
from operator import itemgetter
from bs4 import BeautifulSoup


ENGAGEMENT_SCALE = 130
EMPTY_STRING = ""
USER_DNE_ERROR = "<Response [404]>"
DEFAULT_URL = 'http://instagram.com/'

# return -1 if there is an error accessing the Instagram account 
def main(name, filename): 
    hashtag_list = []
    hashtag_dict = {}
    weightedAveDict = {}
    sorted_hashtag_list = []  

    # build URL and get response   
    url =  DEFAULT_URL + name
    response = requests.get(url)
    # error checking is user invalid 
    if (str(response) == USER_DNE_ERROR):
        return -1

    # scrape HTML for the photos data
    photos = scrapeHTML(response.text)
    if (len(photos) == 0): # response was empty, so user is private
        return -1

    for index, photo in enumerate(photos):
        comments = processComments(photo)
        likes = processLikes(photo)
        caption = processCaption(photo)
        location = processLocation(photo)
        hashtags = processHashtags(photo, hashtag_list)
        addToDict(comments, likes, hashtags, hashtag_dict)

    weightedAveDict = computeWeightedAve(weightedAveDict, hashtag_dict)
    sorted_hashtag_list = sorted(weightedAveDict.items(), key=itemgetter(1))
    sorted_hashtag_list.reverse()
    writeToCSV(name, sorted_hashtag_list, filename, hashtag_dict, getMaxEngagement(sorted_hashtag_list))
    hashtag_list = []
    hashtag_dict = {}
    sorted_hashtag_list = []

# use BeautifulSoup to scrape the raw HTML, return photo information as list
def scrapeHTML(response):
    html_content = response 
    soup = BeautifulSoup(html_content)
    JSON = EMPTY_STRING;

    for n in soup.find_all('script'):
        n = str(unicode(n))
        if ('window._sharedData' in n):
            JSON = n

    length = len(JSON)
    JSON = JSON[52:length-10]
    temp = json.loads(JSON)
    return temp['entry_data']['UserProfile'][0]["userMedia"]    

# return the largest engagement score of all hashtags
def getMaxEngagement(sorted_hashtag_list):
    if sorted_hashtag_list:
        return sorted_hashtag_list[0][1]
    else:
        return 1

def writeToCSV(user, sorted_hashtag_list, filename, hashtag_dict, max_engagement):

    hashtag = ""
    
    for i in range(0, 5):
        hashtag += sorted_hashtag_list[i][0] + ","
    
    hashtag = hashtag[:-1]
    text_file = open("output.txt", "w")
    text_file.write(hashtag)
    text_file.close()
    csv_name = 'csvs/' + filename + '.csv'



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


def computeWeightedAve(weightedAveDict, hashtag_dict):
    for entry in hashtag_dict:
        weightedAveDict[entry] = hashtag_dict[entry][0] + (hashtag_dict[entry][1] * ENGAGEMENT_SCALE)
    return weightedAveDict

def processComments(photo):
    return checkUnicode([photo["comments"]["count"]])

def processLikes(photo):
    return checkUnicode([photo["likes"]["count"]])

def processCaption(photo):
    if (photo["caption"] is None):
        caption = ""
    else: 
        caption = checkUnicode([photo["caption"].get("text", EMPTY_STRING)])
    return caption	

def processLocation(photo):
    if (photo["location"] is None):
        location = ""
    else:
        location = checkUnicode([photo["location"].get("name", EMPTY_STRING)])
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

def addToDict(comments, likes, hashtags, hashtag_dict):
    likes = int(likes[1:len(likes)-1])
    comments = int(comments[1:len(comments)-1])
    for ht in hashtags:
        if hashtag_dict.has_key(ht):
            hashtag_dict[ht] = tuple(map(lambda x, y: x + y, hashtag_dict[ht], (likes, comments)))
        else:
            hashtag_dict[ht] = (likes, comments)

def cleanWord(word):
    separators = ['\\', ',', '.', '"']
    for sep in separators:
        word = word.split(sep, 1)[0]
    return word.lower()
