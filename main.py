import requests
import json

clientID = "chl2lhgpv1bjhmzwsjy9iuxpv5zejd"
vodID = "359709522"
end = 'eyJpZCI6ImE2ZjkxZDJlLWZmNzYtNDNiOS1hZGY3LTFlZGQ4YTI1YTExYiIsImhrIjoiYnJvYWRjYXN0OjMyMDM3Njc3NjE2Iiwic2siOiJBQUFTQjJVVjBvQVZkelRqODFsdmdBIn0b'

def download_chat_to_file(vodID):
    url = "https://api.twitch.tv/kraken/videos/%s/comments" % vodID
    
    headers = { "Client-ID" : clientID, "Accept" : "application/vnd.twitchtv.v5+json" }
    body = { '_next' : '' }
    cursor = ''

    while '_next' in body:
        response = requests.get(url,headers=headers,params={'cursor' : cursor})
        body = response.json()

        for comment in body['comments']:
            print("%s <%d> : %s" % (comment['commenter']['display_name'] ,\
                                   comment['content_offset_seconds'] ,\
                                   comment['message']['body']))
        
        cursor = body['_next'] if '_next' in body else ''

download_chat_to_file(vodID)