from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from huey import crontab
from huey.contrib.djhuey import periodic_task

class Major(models.Model):
	name = models.CharField(max_length=50)
	def __str__(self):
		return self.name


class Minor(models.Model):
	name = models.CharField(max_length=50)
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

# user automatically made permanently inactive on day 1 of month after graduation month
@periodic_task(crontab(day='0 0 * * *')) # Check daily at midnight
def graduation_check():
    user_list = User.objects.filter(is_active=True, is_superuser=False)
    today = datetime.date.today()
    for user in range(len(user_list)):
        inactive_date = datetime.date(user.graduation_year, user.graduation_month+1, 1)
        if inactive_date < today:
            user.status_active=False
            user.is_active=False
    print('blah')

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

	graduation_month = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(12)])
	graduation_year = models.PositiveIntegerField(default=current_year()+4, validators=[min_value_current_year, max_value_in_four_years])

	picture = models.ImageField(blank=True, upload_to='images/')

	majors = models.ManyToManyField(Major, blank=True)
	minors = models.ManyToManyField(Minor, blank=True)
	skills = models.ManyToManyField(Skill, blank=True)
	interests = models.ManyToManyField(Interest, blank=True)
	courses = models.ManyToManyField(Course, blank=True)
	activities = models.ManyToManyField(Activity, blank=True)

	# potential saved users/friends field can be added later (ManyToManyField or ForeignKey)
	# consider using django-friendship or other open source apps to implement relationships between Users

	# posts (like a blog) can be added here as a ManyToManyField, referencing a separate Post model
