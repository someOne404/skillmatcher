from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


# helper functions to get correct graduation year options
def current_year():
	return datetime.date.today().year


def min_value_current_year(value):
	return MinValueValidator(current_year())(value)


def max_value_in_four_years(value):
	return MaxValueValidator(current_year()+4)(value)


class User(AbstractUser):
	phone_regex = RegexValidator(regex=r'^\+??\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
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