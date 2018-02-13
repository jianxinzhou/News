import mongodb_client as client


def test_basic():
    ''' test basic mongodb client utility '''
    db = client.get_db('test')
    db.test_collection.drop()
    assert db.test_collection.count() == 0
    db.test_collection.insert({'test': 123, 'hello': 'world'})
    assert db.test_collection.count() == 1
    db.test_collection.drop()
    assert db.test_collection.count() == 0
    print 'test_basic passed.'


if __name__ == '__main__':
    test_basic()
