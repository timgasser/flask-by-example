# Headlines app

import feedparser
from flask import Flask
from flask import render_template
from flask import request

import json
# import urllib3
import urllib.parse
import urllib.request

app = Flask(__name__)

RSS_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}

DEFAULTS = {'publication': 'bbc',
            'city': 'London, UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'}

URLS = {'weather': "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=8579abcf4e30ce45e4e58d1d9f30acfd",
        'currency': "https://openexchangerates.org//api/latest.json?app_id=d769de3fba994e0b8147cc01b5aaa542"}

class ArticleParser(object):
    """
    Takes an RSS address and returns articles
    """ 
    def __init__(self, rss):
        self.rss = rss
        self.feed = None # Lazy load the feed when needed

    def lazy_feed(self):
        if self.feed is None:
            self.feed = feedparser.parse(RSS_FEED[self.rss])

    def articles(self):
        """
        Returns a list of all articles
        """
        self.lazy_feed()
        return self.feed['entries']

    def get_article(self, index):
        """
        Returns an article at the given index
        """
        self.lazy_feed()
        entry_count = len(self.feed['entries'])
        assert index < entry_count, 'Article {} of {} not available'.format(index, entry_count)
        return self.feed['entries'][index]

    def get_article_sections(self, index):
        """
        Returns an article at the given index
        """
        article = self.get_article(index)
        return (article.get("title"),
                article.get("published"),
                article.get("summary"))

@app.route("/")
def home():
    # Publication options
    query = request.args.get("publication")
    if query is None or query.lower() not in RSS_FEED:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    articles = ArticleParser(publication).articles()

    # Weather options    
    weather_city = request.args.get("city")    
    if weather_city is None:
        weather_city = DEFAULTS['city']
    weather = get_weather(weather_city)

    # Currency options
    currency_from = request.args.get("currency_from")
    if currency_from is None:
        currency_from = DEFAULTS['currency_from']
    
    currency_to = request.args.get("currency_to")
    if currency_to is None:
        currency_to = DEFAULTS['currency_to']

    rate, currencies = get_currency(currency_from, currency_to)

    # return ARTICLE_TEMPLATE.format(*article_sections)
    return render_template("home.html",
                           articles=articles,
                           weather=weather,
                           currencies=currencies,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=round(rate, 2))

def get_weather(query):
    api_url = URLS['weather']
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    # print('Parsed:\n{}'.format(parsed))
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   'country': parsed['sys']['country']}
    return weather

def get_currency(frm, to):
    currency_data = urllib.request.urlopen(URLS['currency']).read()

    parsed = json.loads(currency_data).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


if __name__ == '__main__':
    app.run(port=5000, debug=True)
