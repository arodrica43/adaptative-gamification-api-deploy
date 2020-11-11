from django.test import TestCase, client
# Create your tests here.
from . import models as mod

class TestException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'An exception while executing a test function occurred. {0} '.format(self.message)
        else:
            return 'An exception while executing a test function occurred.'

class ModelTest(TestCase):

    instance = None

    def subsetUp(self):
        pass

    def setUp(self):
        self.subsetUp()
        self.instance.save()

    def suptearDown(self):
        pass

    def tearDown(self):
        self.suptearDown()
        self.instance.delete()

class ClientTest(TestCase):

    urls = []
    requests = ["GET", "HEAD", "OPTIONS", "POST", "PUT" ]

    def subsetUp(self):
        pass

    def setUp(self):
        print("")
        self.subsetUp()
        self.client = client.Client()
        self.request_functions = [self.client.get, self.client.head, self.client.options, self.client.post, self.client.put]
        self.write_data = {}

    def test_http_requests(self):
        for i in range(len(self.requests)):
            for url in  self.urls:            
                httpf =  self.request_functions[i]
                if(self.requests[i] == "POST" or self.requests[i] == "PUT"):
                    response = self.request_functions[i](url, self.write_data)
                else:
                    response = self.request_functions[i](url)
                assert(100 < response.status_code and response.status_code < 400)
                print("Testing " + self.requests[i] + " request on URL '" + url + "'")
             
    def tearDawn(self):
        self.urls = []
        pass

class UserClientTest(ClientTest):

    def subsetUp(self):
        self.write_data = {"username" : "test_user"}
        self.urls = ["/api/users"]

class GamerClientTest(ClientTest):

    def subsetUp(self):
        self.write_data = {"username" : "test_user"}
        self.urls = ["/api/gamers"]

class GMechanicClientTest(ClientTest):

    def subsetUp(self):
        self.write_data = {"title" : "test_gmechanic"}
        self.urls = ["/api/g_mechanics"]



