#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import requests

from credentials import access_token, access_token_secret, consumer_key, consumer_secret

print access_token

#Appbase credentials
user = "4Qrd6fbNm"
password = "566891a4-c54c-4066-a87b-3f89acb13240"
app = "twitter-hashtags"
# Auth call
auth_url = "https://"+user+":"+password+"@scalr.api.appbase.io/"+app
res = requests.post(auth_url, headers={})

"""
curl -N -XPOST https://$user:$pass@scalr.api.appbase.io/$app/hashtags/_search?stream=true --data-binary '{"query": {"match_all":{}}}'
"""

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        json_data = json.loads(data)
        try:
            hashtags = json_data["entities"]["hashtags"]
            for hashtag in hashtags:
                hashtag_text = str(hashtag["text"])
                store_url = auth_url + "/hashtags/"
                hashtag_data = { "hashtag" : hashtag_text }
                print hashtag_text
                res = requests.post(store_url, data=json.dumps(hashtag_data), headers={"Content-type": "application/json"})
            return True
        except UnicodeEncodeError, KeyError:
            return True
        # print json.dumps(json_data, indent=4, sort_keys = True)

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'ruby', 'javascript'])