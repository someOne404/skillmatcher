from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

class Major(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Minor(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Course(models.Model):
    department = models.CharField(max_length=10) # abbreviation of department, usually found with course number
    number = models.IntegerField(validators=[MaxValueValidator(9999), MinValueValidator(100)])
    name = models.CharField(max_length=200)
    def __str__(self):
        return "{} {}".format(self.department, self.number)


class Skill(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Activities" # this appears on the admin menu


# helper functions to get correct graduation year options
def current_year():
    return datetime.date.today().year


def min_value_current_year(value):
    return MinValueValidator(current_year())(value)


def max_value_in_four_years(value):
    return MaxValueValidator(current_year()+4)(value)

class User(AbstractUser):
    # define adjustable status (is_active is always true)
    status_active = models.BooleanField(default=True)

    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=16, blank=True)

    # define choices for class standing
    first_year = '1st'
    second_year = '2nd'
    third_year = '3rd'
    fourth_year = '4th'
    graduate = '5th'
    class_standing_choices = (
        (first_year, 'First Year'),
        (second_year, 'Second Year'),
        (third_year, 'Third Year'),
        (fourth_year, 'Fourth Year'),
        (graduate, 'Graduate'),
    )
    class_standing = models.CharField(
        max_length=3,
        choices=class_standing_choices,
        default=first_year
    )

    graduation_year = models.PositiveIntegerField(default=current_year()+4, validators=[min_value_current_year, max_value_in_four_years])
    picture = models.ImageField(blank=True, upload_to='images/')
    majors = models.ManyToManyField(Major, blank=True)
    minors = models.ManyToManyField(Minor, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    courses = models.ManyToManyField(Course, blank=True)
    activities = models.ManyToManyField(Activity, blank=True)


    def __str__(self):			# error in admin
        return str(self.username) # computing ID

    # potential saved users/friends field can be added later (ManyToManyField or ForeignKey)
    # consider using django-friendship or other open source apps to implement relationships between Users

    # posts (like a blog) can be added here as a ManyToManyField, referencing a separate Post model

class Post(models.Model):
    post_active = models.BooleanField(default=True)
    post_edited = models.BooleanField(default=False)

    headline = models.CharField(max_length=50)
    message = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date posted', blank=True)
    date_edited = models.DateTimeField('date edited', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.headline

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', blank=True)
    text = models.CharField(max_length=250)
    date = models.DateTimeField('date commented', blank=True)

    def __str__(self):
        return self.text
