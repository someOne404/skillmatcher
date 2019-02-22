from django.test import TestCase
from social_match.models import *
from django.urls import reverse

# Create your tests here.
class UserModelTest(TestCase):

	def create_test_user(self):
		return User.objects.create(
			first_name="Test",
			last_name="User",
			phone="+1234567890",
			class_standing=User.first_year,
			graduation_year=2019,
			email='test@virginia.edu',
		)

	def test_create_user(self):
		u = self.create_test_user()
		self.assertTrue(isinstance(u, User))