# Lucky 13 Skill Matching Platform

Have you ever wanted a way to find classmates who have a particular skill and are willing to help out other folks in need? Lucky 13 is a web app where UVA students can create an account and post information about themselves, from what skills and expertise they have, to what courses they are taking. Other students can search on tags that will match up students with people that may be able to help. 

Some key features of Lucky 13 are being able to set up one’s own profile and to search for other users through an array of different filters. Users can also create posts, like posts, comment on posts, and search through all posts by keywords and other filters.

## Using Lucky 13 on Heroku
You may either use our live heroku deployment of Lucky 13 [here](https://lucky-13.herokuapp.com/), or read on to learn how to set up the project locally. Note that to login on Heroku and locally, you must be either a UVA student (and using an @Virginia.edu email) or Professor Mark Sherriff, and to access the features detailed below, you must be signed in.

### Admin access
You can access Lucky 13's [admin page](https://lucky-13.herokuapp.com/admin) through the following credentials:

Username: admin

Password: password

### Setting up your profile
After logging in, you can use the navigation bar to go to your profile page. Here, you and other users can see your profile information and posts. You can click the Edit Profile button to add information about yourself to your profile.

### Searching within users
You can navigate to the Search page from the navigation bar. Here, you can use a variety of filters to find other students that match your needs.

### Creating a Post
You can also create a post by navigating to the Create Post page from the navigation bar. Enter a title and message, then click submit! Your post will be visible to all Lucky 13 users.

### Browsing the home page
On the home page, you can browse by default all posts by Lucky 13 users chronologically. You can like and comment posts, and additionally see who has liked the post and what they have commented. You can also filter through posts by author, keyword, among other options.

## Setting up your own Lucky 13

These instructions will help guide you in getting a copy of the Lucky 13 project up and running on your local machine if you so wish.

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

This project, at the time of writing, is being deployed on Heroku [here](https://lucky-13.herokuapp.com/). Note that you must be a UVA student to sign in.

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
