import requests
import json
from Comment import Comment

import matplotlib.pyplot as plt

clientID = "chl2lhgpv1bjhmzwsjy9iuxpv5zejd"
vodID = "354278744"
end = 'eyJpZCI6ImE2ZjkxZDJlLWZmNzYtNDNiOS1hZGY3LTFlZGQ4YTI1YTExYiIsImhrIjoiYnJvYWRjYXN0OjMyMDM3Njc3NjE2Iiwic2siOiJBQUFTQjJVVjBvQVZkelRqODFsdmdBIn0b'

windowTime = 30 #seconds

def get(path , params):
    headers = { "Client-ID" : clientID, "Accept" : "application/vnd.twitchtv.v5+json" }
    response = requests.get(path,headers=headers,params=params)

    if response.status_code != 200:
        print("Non 200 status code recieved")
    
    return response

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

    with open('VOD#' + vodID, 'w') as outfile:
        json.dump(comments, outfile,default=Comment.toJSON,indent=4)
    
    perform_analytics(comments)

def read_chat_from_file(vodID : str):
    comments = None
    with open('VOD#' + vodID, 'r') as comment_data:
        comments = json.load(comment_data, object_hook=Comment.fromJSON)
    perform_analytics(comments)
    
def perform_analytics(comments : list):
    window = []
    commentsInWindow = {}
    for comment in comments:
        newTime = comment.time
        window.append(newTime)
        window = [time for time in window if newTime - time < windowTime]
        commentsInWindow[newTime] = len(window)
    
    plot_data(commentsInWindow)

def plot_data(data : dict):
    x = list(data.keys())
    y = list(data.values())

    plt.plot(x, y)

    plt.show()

download_chat_to_file(vodID)
#read_chat_from_file(vodID)