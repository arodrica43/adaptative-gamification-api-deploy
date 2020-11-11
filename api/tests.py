from django.test import TestCase, client
# Create your tests here.
from . import models as mod

class UserModelTest(TestCase):

    def setUp(self):
        self.test_user = mod.User(email="prueba@prueba.com", username='test_user')
        self.test_user.save()

    def test_something(self):
        pass

    def tearDown(self):
        self.test_user.delete()

class UserClientTest(TestCase):

    def setUp(self):
        self.client = client.Client()

    def test_get(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)

    
    def test_post(self):

        response = self.client.post('/api/users/',{'username':'test_user'})
        print(response.content)
        self.assertEqual(response.status_code, 201)

    def tearDawn(self):
        pass
    

class LeaderboardTestCase(TestCase):
    def setUp(self):
        mod.Leaderboard.objects.create(title = "TestLeaderboard", length = 4, sort_by = "a")     

    def test_leaderboard_leadders(self):
        """Function to test leadderboard"""
        pass

