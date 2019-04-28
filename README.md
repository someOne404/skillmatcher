# Lucky 13 Skill Matching Platform

Have you ever wanted a way to find classmates who have a particular skill and are willing to help out folks in need? Lucky 13 is a web app where UVA students can create an account and post information about themselves, including what skills/expertise they have. Other students can search on "tags" that will match up students with people that may be able to help. 

Some key features of Lucky 13 is being able to set up one’s own profile and search for other users through an array of filters. 
Users can also create posts, provide tags for posts, like posts, comment on posts, and search through all posts by keywords or other filters.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You must have Python installed. Setting up a virtual environment might also be a good idea, but it is not necessary.

All other requirements are listed in the requirements.txt file. Depending on your IDE, you may be able to install these prerequisites very simply (such as when using PyCharm),  or you may have to install them manually like so:

```
pip install django==2.1.7
```

### Installing

If you need a more detailed step by step on installing Python and Django on windows, [this](https://www.codingforentrepreneurs.com/blog/install-python-django-on-windows) is a good guide to get started with.

## Running locally

You can run this web app locally offline.

### Migrations
Be sure to take care of migrations beforehand first by running these commands when necessary while in the project-101-lucky-13/ folder:

```
python manage.py makemigrations
python manage.py migrate
```

### Launching Locally
When you are ready to launch the app locally, run this command while in the project-101-lucky-13/ folder:

```
python manage.py runserver
```

Your app will be by default running at [http://127.0.0.1:8000](http://127.0.0.1:8000).


## Running the tests

Numerous tests are included within this app already. They can be found in the project-101-lucky-13/social_match/tests.py file.

This file can be edited to add more tests, and all the tests can be run using this command while in the project-101-lucky-13/ folder:

```
python manage.py test
```

## Deployment

This project, at the time of writing, is being deployed on Heroku [here](https://social-match-lucky13.herokuapp.com/). Note that you must be a UVA student to sign in.

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Heroku](https://rometools.github.io/rome/) - The cloud app deployment service used
* [Travis CI](https://maven.apache.org/) - The continuous integration service used

## Contributors

* **Vivian Lin** - *Scrum Master* - [vwl4ac](https://github.com/vwl4ac)
* **Sung Joon Park** - *Requirements Manager* - [sp3bk](https://github.com/sp3bk)
* **Stephen Shamaiengar** - *Software Architect* - [sshamaiengar](https://github.com/sshamaiengar)
* **Burgard Lu** - *Configuration Manager* - [someOne404](https://github.com/someOne404)
* **Angelica Lavan** - *Testing Manager* - [AngelicaLavan](https://github.com/AngelicaLavan)

## Acknowledgments

* Thank you to Professor Mark Sherriff for inspiring this project and to all our TAs and friends who supported us along the way.
