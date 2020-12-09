import json
import re
import redis

rc = redis.StrictRedis(host='localhost', port=6379, db=0)

def hashtagAnalysis(data):
    final_data = json.loads(data)
    text = final_data['text']
    result = re.findall(r'[#]\w+', text)
    if(len(result)>0):
        for item in result:
            rc.zincrby('hashtag', 1, item)









