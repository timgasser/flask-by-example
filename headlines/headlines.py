# Headlines app

import feedparser
from flask import Flask

app = Flask(__name__)

RSS_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}

ARTICLE_TEMPLATE = """<html>
        <body>
            <h1>Headlines </h1>
            <b>{0}</b> <br/>
            <i>{1}</i> <br/>
            <p>{2}</p> <br/>
        </body>
    </html>"""

class ArticleParser(object):
    """
    Takes an RSS address and returns articles
    """
    def __init__(self, rss):
        self.rss = rss
        self.feed = None # Lazy load the feed when needed

    def get_article(self, index):
        """
        Returns an article at the given index
        """
        if self.feed is None:
            self.feed = feedparser.parse(RSS_FEED[self.rss])

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
@app.route("/bbc")
def get_bbc_news():
    # parser = ArticleParser('bbc')
    article_sections = ArticleParser('bbc').get_article_sections(0)
    return ARTICLE_TEMPLATE.format(*article_sections)

@app.route("/fox")
def get_fox_news():
    # parser = ArticleParser('fox')
    article_sections = ArticleParser('fox').get_article_sections(0)
    return ARTICLE_TEMPLATE.format(*article_sections)

@app.route("/cnn")
def get_cnn_news():
    # parser = ArticleParser('cnn')
    article_sections = ArticleParser('cnn').get_article_sections(0)
    return ARTICLE_TEMPLATE.format(*article_sections)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
