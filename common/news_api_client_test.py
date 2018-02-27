import news_api_client as client

# Todo: add tests to handle 404/ url errors, etc.
def test_basic():
    news = client.get_news_from_source()
    print news
    assert len(news) > 0
    news = client.get_news_from_source(sources=['bbc-news'])
    assert len(news) > 0
    print 'test_basic passed!'

if __name__ == "__main__" :
    test_basic()
