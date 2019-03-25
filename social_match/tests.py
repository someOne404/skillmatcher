from django.test import TestCase
from social_match.filters import *
from social_match.forms import *
from django.urls import reverse
from django.shortcuts import render

from django.utils import timezone
import datetime

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
        User.objects.create(
            first_name="Reactivated",
            last_name="User",
            phone="+1234567890",
            class_standing=User.first_year,
            graduation_year=2019,
            email='reactivated@virginia.edu',
            status_active='False',
            username='Reactivated',
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

    def test_inactivated_user_not_search_results(self):
        self.create_regular_inactive_and_super_users()

        user_reactivate = User.objects.filter(username='Test')
        user_reactivate.status_active = 'False'

        GET={'title': 'test'}
        user_list=User.objects.all()
        user_filter = UserFilter(GET, queryset=user_list)

        user_list_ideal = User.objects.filter(status_active='True', is_superuser='False')
        self.assertQuerysetEqual(user_filter.qs, user_list_ideal, transform=lambda x: x)

    def test_reactivated_user_in_search_results(self):
        self.create_regular_inactive_and_super_users()

        user_reactivate = User.objects.filter(username='Reactivated')
        user_reactivate.status_active = 'True'

        GET={'title': 'test'}
        user_list=User.objects.all()
        user_filter = UserFilter(GET, queryset=user_list)

        user_list_ideal = User.objects.filter(status_active='True', is_superuser='False')
        self.assertQuerysetEqual(user_filter.qs, user_list_ideal, transform=lambda x: x)

# class SecurityTest(TestCase):
#     def create_test_user(self):
#         return User.objects.create(
#             first_name="Test",
#             last_name="User",
#             phone="+1234567890",
#             graduation_year=2019,
#             class_standing=User.first_year,
#             email='test@virginia.edu',
#         )
#
#     def create_post(self):
#         headline = 'headline'
#         message = 'message'
#         user = self.create_test_user
#         time = timezone.now()
#         return Post.objects.create(headline=headline, message=message, user=user, date=time)
#
#     # tests
#     def test_home_is_secure(self):
#         template = './social_match/home.html'   # home
#         page_ideal = render(None, template)
#         response = self.client.get('/home', follow=True)
#         self.assertEquals(page_ideal.content, response.content)
#
#     def test_createpost_is_secure(self):
#         template = './social_match/createpost.html' # createpost
#         page_ideal = render(None, template)
#         self.assertEquals(page_ideal.content, response.content)
#         response = self.client.get('/createpost', follow=True)
#     def test_posts_is_secure(self):
#
#         self.assertEquals(page_ideal.content, response.content)
#         response = self.client.get('/myposts', follow=True)
#         template = './social_match/home.html'  # posts
#         page_ideal = render(None, template)
#
#     def test_profile_is_secure(self):
#         template = './social_match/home.html'  # profile
#         page_ideal = render(None, template)
#         response = self.client.get('/profile', follow=True)
#         self.assertEquals(page_ideal.content, response.content)
#
#     def test_search_is_secure(self):
#         template = './social_match/search.html'  # search
#         page_ideal = render(None, template)
#         response = self.client.get('/search', follow=True)
#         self.assertEquals(page_ideal.content, response.content)
#
#     def test_myposts_is_secure(self):
#         template = './social_match/myposts.html'  # myposts
#         page_ideal = render(None, template)
#         response = self.client.get('/myposts', follow=True)
#
#         self.assertEquals(page_ideal.content, response.content)

#         #editposts
class ProfileTest(TestCase):

    def create_test_user(self):
        return User.objects.create(
            first_name="Test",
            last_name="User",
            phone="+1234567890",
            class_standing=User.first_year,
            graduation_year=2019,
            email='test@virginia.edu',
            username='testuser',
            password='password'
        ), 'testuser', 'password'



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

    #def test_view_user_profile(self):
        #user, _, _ = self.create_test_user()
        #response = self.client.get('/profile/{}/'.format(user.id))
        #self.assertContains(response, "Test User")

    #def test_view_nonexistent_user(self):
        #response = self.client.get('/profile/1/')
        #expected_404 = render(None, "social_match/404.html")
        #self.assertEqual(response.content, expected_404.content)

    def test_logged_in_user_profiles_identical(self):
        user, username, pw = self.create_test_user()
        self.client.login(username=username, password=pw)
        response1 = self.client.get('/profile/{}'.format(user.id))
        response2 = self.client.get('/profile/')
        self.assertEqual(response1.content, response2.content)


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

    def test_search_by_first_name2(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(first_name="Test2")
        self.assertFalse(u1 in user_list_filter)

    def test_search_by_first_name3(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(first_name="")
        self.assertFalse(u1 in user_list_filter)

    def test_search_by_last_name(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(last_name="User2")
        self.assertFalse(u1 in user_list_filter)

    def test_search_by_last_name2(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(last_name="User1")
        self.assertTrue(u1 in user_list_filter)

    def test_search_by_phone(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(phone="+1234567890")
        self.assertTrue(u1 in user_list_filter)

    def test_search_by_phone2(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(phone="+1234567899")
        self.assertFalse(u1 in user_list_filter)

    def test_search_by_phone3(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(phone="+911")
        self.assertFalse(u1 in user_list_filter)

    def test_search_by_class_standing(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(class_standing=User.second_year)
        self.assertFalse(u1 in user_list_filter)

    def test_search_by_class_standing2(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(class_standing=User.first_year)
        self.assertTrue(u1 in user_list_filter)

    def test_search_by_graduation_year(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(graduation_year=2019)
        self.assertTrue(u1 in user_list_filter)

    def test_search_by_graduation_year2(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(graduation_year=2020)
        self.assertFalse(u1 in user_list_filter)

    def test_search_by_email(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(email="test1@virginia.edu")
        self.assertTrue(u1 in user_list_filter)

    def test_search_by_email2(self):
        u1 = self.create_test_user1()
        user_list_filter = User.objects.filter(email="not_test1@virginia.edu")
        self.assertFalse(u1 in user_list_filter)

    def test_non_existent_user(self):
        user_list_filter = User.objects.filter(email="nonexistent@virginia.edu")
        self.assertFalse(user_list_filter.exists())

    # def test_search_by_major(self):
    #     u1 = self.create_test_user1()
    #     user_list_filter = User.objects.filter(major='Computer Science')
    #     self.assertTrue(u1 in user_list_filter)

def create_post(headline, message, user, days):
    """
    Create a post with the given 'post_headline', 'post_message', and published
    the given numbers of 'days' offset to now (negative for posts published
    in the past, positive for posts that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(headline=headline, message=message, user=user, date=time)

def create_many_posts(headline, message, user, num_posts):
    for i in range(num_posts):
        create_post(headline, message, user, (-1*num_posts))

class PostTest(TestCase):
    def create_test_user(self):
        return User.objects.create(
            first_name="Test",
            last_name="User",
            phone="+1234567890",
            class_standing=User.first_year,
            graduation_year=2019,
            email='test@virginia.edu',
        )

    # tests
    def test_post_form_no_inputs(self):
        form_data = {'headline':'', 'message':''}
        form = PostForm(data = form_data)
        self.assertFalse(form.is_valid())

    def test_post_form_valid_inputs(self):
        form_data = {'headline':'headline', 'message':'message'}
        form = PostForm(data = form_data)
        self.assertTrue(form.is_valid())

    def test_no_posts(self):
        response = self.client.get(reverse('social_match:home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_past_post(self):
        headline = 'Past post'
        message = 'should appear in home page'
        user = self.create_test_user()
        create_post(headline=headline, message=message, user=user, days=-30)
        response = self.client.get(reverse('social_match:home'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            ['<Post: Past post>']
        )

    def test_current_post(self):
        headline = 'posted today'
        message = 'should appear in home page'
        user = self.create_test_user()
        create_post(headline=headline, message=message, user=user, days=0)
        response = self.client.get(reverse('social_match:home'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            ['<Post: posted today>']
        )

    def test_future_post(self):
        headline = 'Future post'
        message = 'should not appear in home page'
        user = self.create_test_user()
        create_post(headline=headline, message=message, user=user, days=30)
        response = self.client.get(reverse('social_match:home'))
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_future_post_and_past_post(self):
        user = self.create_test_user()
        create_post(
            headline='Past post',
            message = 'should appear in home page',
            user = user,
            days = -30
        )
        create_post(
            headline='Future post',
            message = 'should not appear in home page',
            user = user,
            days = 30
        )
        response = self.client.get(reverse('social_match:home'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            ['<Post: Past post>']
        )

    def test_first_20_of_21_questions_appear_in_home(self):
        headline = '21 posts'
        message = 'message'
        user = self.create_test_user()
        create_many_posts(headline, message, user, 21)
        response = self.client.get(reverse('social_match:home'))

        list = []
        for i in range(20):
            list.append('<Post: ' + headline + '>')

        self.assertQuerysetEqual(response.context['post_list'], list)

    def test_no_likes_on_new_Post(self):
        headline = 'headline'
        message = 'message'
        user = self.create_test_user()
        days = 0
        post = create_post(headline, message, user, days)
        self.assertEquals(post.likes.count(), 0)

    def test_like_post(self):
        headline = 'headline'
        message = 'message'
        self.user = self.create_test_user()
        days = 0
        post = create_post(headline, message, self.user, days)
        post.likes.add(self.user.id)
        self.assertEquals(post.likes.count(), 1)

    def test_unlike_post(self):
        headline = 'headline'
        message = 'message'
        self.user = self.create_test_user()
        days = 0
        post = create_post(headline, message, self.user, days)
        post.likes.add(self.user.id)
        self.assertEquals(post.likes.count(), 1)
        post.likes.remove(self.user.id)
        self.assertEquals(post.likes.count(), 0)

    def test_comment_post_form_no_inputs(self):
        form_data = {'text':''}
        form = CommentPostForm(data = form_data)
        self.assertFalse(form.is_valid())

    def test_comment_post_form_valid_inputs(self):
        form_data = {'text':'text'}
        form = CommentPostForm(data = form_data)
        self.assertTrue(form.is_valid())
