from django.test import TestCase, Client
from social_match.models import *
from social_match.filters import *
from django.urls import reverse
from django.shortcuts import render
import requests
import socket

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
            username='Test',
        )

    def create_regular_inactive_and_super_users(self):
        User.objects.create(
            first_name="Test",
            last_name="User",
            phone="+1234567890",
            class_standing=User.first_year,
            graduation_year=2019,
            email='test@virginia.edu',
            username='Test',
        )
        User.objects.create(
            first_name="Inactive",
            last_name="User",
            phone="+1234567890",
            class_standing=User.first_year,
            graduation_year=2019,
            email='inactive@virginia.edu',
            status_active='False',
            username='Inactive',
        )
        User.objects.create(
            first_name="Super",
            last_name="User",
            phone="+1234567890",
            class_standing=User.first_year,
            graduation_year=2019,
            email='superuser@virginia.edu',
            is_superuser='True',
            username='Superuser',
        )

    def test_create_user(self):
        u = self.create_test_user()
        self.assertTrue(isinstance(u, User))

    def test_inactive_and_superuser_not_in_search_results(self):
        self.create_regular_inactive_and_super_users()

        GET={'title': 'test'}
        user_list=User.objects.all()
        user_filter = UserFilter(GET, queryset=user_list)

        user_list_ideal = User.objects.filter(status_active='True', is_superuser='False')
        self.assertQuerysetEqual(user_filter.qs, user_list_ideal, transform=lambda x: x)

class SecurityTest(TestCase):

    def test_pages_are_secure(self): # add to this test when more secure pages are created
        template = './social_match/home.html'   # home
        page_ideal = render(None, template)
        response = self.client.get('/home', follow=True)
        self.assertEquals(page_ideal.content, response.content)

        template = './social_match/createpost.html' # createpost
        page_ideal = render(None, template)
        response = self.client.get('/createpost', follow=True)
        self.assertEquals(page_ideal.content, response.content)

        template = './social_match/posts.html'  # posts
        page_ideal = render(None, template)
        response = self.client.get('/posts', follow=True)
        self.assertEquals(page_ideal.content, response.content)

        template = './social_match/profile.html'  # profile
        page_ideal = render(None, template)
        response = self.client.get('/profile', follow=True)
        self.assertEquals(page_ideal.content, response.content)

        template = './social_match/search.html'  # search
        page_ideal = render(None, template)
        response = self.client.get('/search', follow=True)
        self.assertEquals(page_ideal.content, response.content)

class ProfileTest(TestCase):

    def create_authenticated_active_user(self):
        user = 'testuser'
        pw = 'password'
        self.user=User.objects.create_user(username=user, password=pw)
        self.client.login(username=user, password=pw)
        return user, pw

    def create_authenticated_inactive_user(self):
        user = 'testuser'
        pw = 'password'
        self.user=User.objects.create_user(username=user, password=pw, status_active=False)
        self.client.login(username=user, password=pw)
        return user, pw

    def test_make_inactive(self):
        user, pw = self.create_authenticated_active_user()
        self.client.post('/profile/', {'change_status': 'Change status'})
        userQS = User.objects.filter(username=user)
        user = userQS[0]
        self.assertFalse(user.status_active)

    def test_make_active(self):
        user, pw = self.create_authenticated_inactive_user()
        self.client.post('/profile/', {'change_status': 'Change status'})
        userQS = User.objects.filter(username=user)
        user = userQS[0]
        self.assertTrue(user.status_active)


class SearchingTest(TestCase):

    def create_test_user1(self):
        return User.objects.create(
            first_name="Test",
            last_name="User1",
            phone="+1234567890",
            class_standing=User.first_year,
            graduation_year=2019,
            email='test1@virginia.edu',
        )

    def test_search_by_first_name(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(first_name="Test")
        self.assertTrue(u1 in user_list_filter)

    def test_search_by_last_name(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(last_name="User2")
        self.assertFalse(u1 in user_list_filter)

    def test_search_by_phone(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(phone="+1234567890")
        self.assertTrue(u1 in user_list_filter)

    def test_search_by_class_standing(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(class_standing=User.second_year)
        self.assertFalse(u1 in user_list_filter)

    def test_search_by_graduation_year(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(graduation_year=2019)
        self.assertTrue(u1 in user_list_filter)

    def test_search_by_email(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(email="test1@virginia.edu")
        self.assertTrue(u1 in user_list_filter)
