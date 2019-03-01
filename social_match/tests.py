from django.test import TestCase
from social_match.models import *
from social_match.filters import *
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
            username='Test',
        )

    def create_test_user_inactive(self):
        return User.objects.create(
            first_name="Inactive",
            last_name="User",
            phone="+1234567890",
            class_standing=User.first_year,
            graduation_year=2019,
            email='inactive@virginia.edu',
            status_active='False',
            username='Inactive',
        )

    def create_test_user_superuser(self):
        return User.objects.create(
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
        self.create_test_user()
        self.create_test_user_inactive()
        self.create_test_user_superuser()

        GET={'title': 'test'}
        user_list=User.objects.all()
        user_filter = UserFilter(GET, queryset=user_list)

        user_list_ideal = User.objects.filter(status_active='True', is_superuser='False')
        self.assertQuerysetEqual(user_filter.qs, user_list_ideal, transform=lambda x: x)


#class SearchingTest(TestCase):

    #def test_first_name(self):
