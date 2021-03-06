from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'localhost'
TEST_QUEUE_NAME = 'test'


def test_basic():
    ''' test cloudAMQP_client basic utility '''
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sent_message = {"test": "test"}
    client.sendMessage(sent_message)
    received_message = client.getMessage()

    assert sent_message == received_message
    print "test_basic passed"


if __name__ == "__main__":
    test_basic()
