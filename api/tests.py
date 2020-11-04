from django.test import TestCase

# Create your tests here.
from . import models

class LeaderboardTestCase(TestCase):
    def setUp(self):
        models.Leaderboard.objects.create(title = "TestLeaderboard", length = 4, sort_by = "a")     

    def test_leaderboard_leadders(self):
        """Function to test leadderboard"""
        pass