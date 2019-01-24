import json

class Comment():
    def __init__(self,packet):#,user,time,comment):
        self.json = packet
        self.user = packet['commenter']['display_name']
        self.time = packet['content_offset_seconds']
        self.comment = packet['message']['body']


    def __repr__(self):
        return str(self.json)
        #return "%s <%d> : %s" % (self.user,self.time,self.comment)
    
    @staticmethod
    def toJSON(obj):
        return obj.json
        #return {'user' : obj.user , 'time' : obj.time, 'comment' : obj.comment}
    
    @staticmethod
    def fromJSON(dic):
        if 'channel_id' in dic:
            return Comment(dic)
        else:
            return dic
        #return Comment(user=dic['user'],time=dic['time'],comment=dic['comment'])