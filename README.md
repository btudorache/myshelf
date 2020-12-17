# Myshelf

A *social platform* and *book database* for people who love reading. Built with **Django** and **Bootstrap**. 

## Setup - Ubuntu/MacOS

**Requirements: Python3, Pip**

Clone the repository locally:

```
cd myshelf
pip3 install virtualenv                         # install virtualenv package
virtualenv venv                                 # create virtual env
source venv/bin/activate                        # activate venv 
pip3 install -r requirements.txt                # install requirements
python3 manage.py migrate                       # create database tables/fields
python3 manage.py loaddata db.json              # load initial data
python3 manage.py runserver                     # run local server
```

## Features

Some of the main features of the app:
* login, register and other account related functionalities
* follow system and action feed
* book database with rating and review functionalities
* 'shelf' where you can store read books, currently reading books and other custom categories

## Testing

Run the entire test suite with the following command:

```
python3 manage.py test
```

**Note:** test *test_book_with_custom_cover()* in the books app works only on Windows systems.

For the functional tests in *functional_tests*, **Selenium** and **GeckoDriver** is also required:

```
python3 manage.py test functional_tests
```