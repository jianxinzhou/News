# -*- coding: utf-8 -*-
"""后端起rpc server，供前端rpc client调用"""

import pyjsonrpc
import json
import os
import sys

from bson.json_util import dumps

#import common package in parent dictionary
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client


SERVER_HOST = 'localhost'
SERER_PORT = 4040

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ RPC request handler """
    @pyjsonrpc.rpcmethod
    def add(self, num1, num2):
        """ Test method """
        print "add is called with %d and %d" % (num1, num2)
        return num1 + num2

    @pyjsonrpc.rpcmethod
    def getNews(self):
        db = mongodb_client.get_db()
        # db['news'].find() returns iterable type, switch it to list to return
        news = list(db['news'].find())
        # we get bson format from mongodb server, dumps what we get to string,
        # then turns it to be json format by json.loads mehtod is needed
        return json.loads(dumps(news))


# Threading HTTP Server
HTTP_SERVER = pyjsonrpc.ThreadingHttpServer(
    server_address=(SERVER_HOST, SERER_PORT),
    RequestHandlerClass=RequestHandler
)

print "Starting HTTP server on %s%d" % (SERVER_HOST, SERER_PORT)

HTTP_SERVER.serve_forever()
