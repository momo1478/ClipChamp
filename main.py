from Comment import Comment

import requests
import json

from pprint import pprint
import os.path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

import time

clientID = "chl2lhgpv1bjhmzwsjy9iuxpv5zejd"
vodID = "354278744"
end = 'eyJpZCI6ImE2ZjkxZDJlLWZmNzYtNDNiOS1hZGY3LTFlZGQ4YTI1YTExYiIsImhrIjoiYnJvYWRjYXN0OjMyMDM3Njc3NjE2Iiwic2siOiJBQUFTQjJVVjBvQVZkelRqODFsdmdBIn0b'

windowTime = 30 #seconds

def get(path : str, params : dict = {}):
    headers = { "Client-ID" : clientID, "Accept" : "application/vnd.twitchtv.v5+json" }
    response = requests.get(path,headers=headers,params=params)

    if response.status_code != 200:
        print("Non 200 status code recieved")
    
    return response

def get_emotes_list(setNumber : int = 0):
    url = "https://api.twitch.tv/kraken/chat/emoticon_images?emotesets=%d" % setNumber
    emoteList = get(url).json()['emoticon_sets']['0']
    ids =   [emote['id'] for emote in emoteList]
    names = [emote['code'] for emote in emoteList]
    return dict(zip(ids, names))

def get_chat_fragment(vodID : str, cursor : str = ''):
    url = "https://api.twitch.tv/kraken/videos/%s/comments" % vodID
    return get(url,params={'cursor' : cursor}).json()

def download_chat_to_file(vodID : str):
    comments = []
    fragment = { '_next' : '' }

    while '_next' in fragment:
        fragment = get_chat_fragment(vodID,fragment['_next'])
        for comment in fragment['comments']:
            comments.append(Comment(comment))
        print("downloaded up to " + str(fragment['comments'][0]['content_offset_seconds']) + " seconds")

    with open('VOD#' + str(vodID), 'w') as outfile:
        json.dump(comments, outfile,default=Comment.toJSON,indent=4)
    
    perform_analytics(comments, vodID)

def read_chat_from_file(vodID : str):
    comments = None
    with open('VOD#' + str(vodID), 'r') as comment_data:
        comments = json.load(comment_data, object_hook=Comment.fromJSON)
    perform_analytics(comments, vodID)

def perform_analytics(comments : list, vodID : str):
    window = []
    commentsInWindow = {}
    for comment in comments:
        newTime = comment.time
        window.append(newTime)
        window = [time for time in window if newTime - time < windowTime]
        commentsInWindow[newTime] = len(window)
    
    plot_data(commentsInWindow, vodID)

def plot_data(data : dict, vodID : str):
    x = list(data.keys())
    y = list(data.values())

    fig, ax = plt.subplots()

    plt.plot(x, y)

    formatter = mticker.FuncFormatter(lambda hms, x: time.strftime('%H:%M:%S', time.gmtime(hms)))
    ax.xaxis.set_major_formatter(formatter)

    numComments = len(data)
    lastComment = time.strftime('%H:%M:%S', time.gmtime(x[-1]))

    plt.title("VOD#" + str(vodID) + (" (%d comments in %s )" % (numComments,lastComment) ) )
    plt.xlabel("Time into VOD")
    plt.ylabel("Comments in " + str(windowTime) + " second window.")

    plt.show()

def analyze_VOD(vodID):
    if os.path.isfile('VOD#' + str(vodID)):
        read_chat_from_file(vodID)
    else:
        download_chat_to_file(vodID)

# emotes = get_emotes_list()
# pprint(emotes)
# analyze_VOD(vodID)
analyze_VOD(371095364)