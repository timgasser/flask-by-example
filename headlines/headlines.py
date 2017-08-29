# Headlines app

import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}

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
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEED:
        publication = "bbc"
    else:
        publication = query.lower()
    
    articles = ArticleParser(publication).articles()
    # return ARTICLE_TEMPLATE.format(*article_sections)
    return render_template("home.html", articles=articles)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
