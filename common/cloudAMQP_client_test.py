from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://gvwcyjgr:vIm9ENUbKHvXkctC2HZMD1oxHL8yxv25@sidewinder.rmq.cloudamqp.com/gvwcyjgr"
TEST_QUEUE_NAME = "test"


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
