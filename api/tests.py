from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
# Create your tests here.
from . import models as mod
from . import views as vws
import webbrowser as wb

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

# class ModelTest(TestCase):

#     def subsetUp(self):
#         pass

#     def setUp(self):
#         self.instance = mod.User(username = "Francisco")
#         self.subsetUp()
#         self.instance.save()
#         print(mod.User.objects.all())

#     def subtearDown(self):
#         pass

#     def tearDown(self):
#         self.subtearDown()
#         self.instance.delete()

# class RequestTest(TestCase):

#     def subsetUp(self):
#         pass

#     def setUp(self):
#         self.client = client.Client()
#         self.url = "/api/users"
#         self.data = {}
#         self.mode = self.client.get
#         self.expected_result = lambda r : (100 < r.status_code and r.status_code < 400)
#         self.subsetUp() # Here we can change default args
    
#     def test_things(self):
#         self.response = self.mode(self.url, data = self.data)
#         print(self.response.status_code)
#         assert(self.expected_result(self.response))
#         print(self.response.request)
  
#     def subtearDown(self):
#         pass

#     def tearDown(self):
#         self.subtearDown()

class AGAlgorithmTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = mod.User.objects.create(username="user_test1")
        pass

    def test_X(self):

        data = {"username":"user_test2"}
         # Create an instance of a GET request.
        request = self.factory.post('/api/gamers', data= data)

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = AnonymousUser()
        response = vws.GamerViewSet.as_view({'post' : 'create'})(request,data)
        # Use this syntax for class-based views.
        print(response)
        print(mod.Gamer.objects.all())
        #self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass

   


      

    