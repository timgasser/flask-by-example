from urllib.request import urlopen
import json

TOKEN = "829260ae1309cc081a47ee21e15cf0ede340aa9d"
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"

class BitlyHelper(object):

    def shorten_url(self, longurl):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN, longurl)
            # print('url: {}'.format(url))
            response = urlopen(url).read()
            # print('response: {}'.format(response))
            jr = json.loads(response)
            # print('jr: {}'.format(jr))
            return jr['data']['url']

        except Exception as e:
            print(e)
            