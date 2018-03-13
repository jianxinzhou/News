import news_recommendation_service_client as client

def test_basic():
    res = client.getPreferenceForUser("test_user")
    print res
    assert res is not None

if __name__ == '__main__':
    test_basic()
