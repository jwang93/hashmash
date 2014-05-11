import requests
import unicodedata 
import string 
from termcolor import colored
import simplejson as json
import csv 
from operator import itemgetter
from bs4 import BeautifulSoup


default = ""
ENGAGEMENT_SCALE = 130
USER_DNE_ERROR = "<Response [404]>"


# return -1 if there is an error accessing the Instagram account 
def main(name, filename): 
    hashtag_list = []
    hashtag_dict = {}
    weightedAveDict = {}
    sorted_hashtag_list = []    
    name = name.strip()
    url = 'http://instagram.com/' + name
    response = requests.get(url)

    print str(response)
    if (str(response) == USER_DNE_ERROR):
        return -1

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
        comments = processComments(photo)
        likes = processLikes(photo)
        caption = processCaption(photo)
        location = processLocation(photo)
        hashtags = processHashtags(photo, hashtag_list)
        addToDict(comments, likes, hashtags, hashtag_dict)

    weightedAveDict = computeWeightedAve(weightedAveDict, hashtag_dict)
    sorted_hashtag_list = sorted(weightedAveDict.items(), key=itemgetter(1))
    sorted_hashtag_list.reverse()
    print sorted_hashtag_list
    writeToCSV(name, sorted_hashtag_list, filename, hashtag_dict, getMaxEngagement(sorted_hashtag_list))
    hashtag_list = []
    hashtag_dict = {}
    sorted_hashtag_list = []

def getMaxEngagement(sorted_hashtag_list):
    return sorted_hashtag_list[0][1]

def writeToCSV(user, sorted_hashtag_list, filename, hashtag_dict, max_engagement):
    csv_name = 'csvs/' + filename + '.csv'
    with open(csv_name, 'ab') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #writer.writerow(['#'] + ['likes'] + ['caption'] + ['location'] + ['hashtags'])
        print type(sorted_hashtag_list)
        print len(sorted_hashtag_list)
        writer.writerow([user])
        writer.writerow([""] + [""] + ["engagement_score"] + ["num_likes"] + ["num_comments"])
        for index, hashtag_tuple in enumerate(sorted_hashtag_list):
            print hashtag_tuple
            hashtag = str(hashtag_tuple[0])
            weightedAve = str(hashtag_tuple[1] / float(max_engagement))
            likes = str(hashtag_dict[hashtag][0])
            comments = str(hashtag_dict[hashtag][1])
            writer.writerow([str(index+1)] + [hashtag] + [weightedAve] + [likes] + [comments])
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

def addToDict(comments, likes, hashtags, hashtag_dict):
    likes = int(likes[1:len(likes)-1])
    comments = int(comments[1:len(comments)-1])
    for ht in hashtags:
        if hashtag_dict.has_key(ht):
            hashtag_dict[ht] = tuple(map(lambda x, y: x + y, hashtag_dict[ht], (likes, comments)))
        else:
            hashtag_dict[ht] = (likes, comments)
    print hashtag_dict

def cleanWord(word):
    separators = ['\\', ',', '.', '"']
    for sep in separators:
        word = word.split(sep, 1)[0]
    return word.lower()
