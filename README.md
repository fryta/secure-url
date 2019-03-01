# sercure-url
This project is a system for sending URLs and files between people in a secure way (protected by password).
It was created as a recruitment task to show my coding skills. 
Hope you will like it and find it useful :)

## Actors in the system
* Simple system user (can upload a file / url and manage his items - this user has its own credentials in system)
* System beneficiary (can download file or can be redirected to protected url knowing password)
* Admin user (can manage user accounts / can manage users' urls/files)
* Stats user (can fetch statistics via API)

## Use cases
* As a simple system user I need to have a web form where I can login into the system in order to have access to restricted resources.
* As a simple system user I need to have a web form which is accessible after login where I can upload a file or put URL in order to generate a secured access URL with password which I can share within 24 hours.
* As a simple system user I need to be able to fulfill abovementioned Use Cases via API in order to be able to integrate the system with any interface (e.g. mobile app).  
* As a system beneficiary I need to have a form where I can put password after accessing secured URL in order to get access to restricted resource (URL or file).
* As a system beneficiary I need to be able to fulfill abovementioned Use Case via API in order to be able to integrate the system with any interface (e.g. mobile app).
* As an admin user I need to be have access to admin panel in order to manage all users' accounts (create / edit them).
* As an admin user I need to be have access to admin panel in order to manage all uploaded files and urls (i. e. browse them and optionally change password).
* As a stats user I need to have access to restricted by authorization endpoint which will provide me a daily stats about unique visits to secured URL with files and links. 

## other requirements
* User Agent of last user's visit should be remembered (actually we keep the full history of user's User Agent)
* Part of code providing and restricting access to secured URL within 24 hours should be covered with tests.

## Installation
* `git clone https://github.com/fryta/secure-url.git`
* `mkvirtualenv secure-url` (use Python 3)
* `pip install -r requirements.txt`
* `python manage.py collectstatic`
* `python manage.py migrate`
* `python manage.py runserver` (for development) or `gunicorn config.wsgi` (for production / staging)

## Tests
* `python manage.py test` (make sure you've run `python manage.py collectstatic` before)

## API
* API url: `http://secure-url.herokuapp.com/api/`
* When entering API url you will see full documentation of the api (please login with demo admin credentials to see
all available endpoints). 
* Alternatively you can use djangorestframework UI to browse API, just enter any available URL, e.g.: 
`https://secure-url.herokuapp.com/api/secure-url/`

## Demo
Live demo is available here: `https://secure-url.herokuapp.com`

Example login data:

* for admin: 
    * login - `admin`
    * password: `123qweasdsecure-url`
* for regular user: 
    * login - `user`
    * password: `user123qweasdsecure-url`

Admin panel: `https://secure-url.herokuapp.com/admin/`

### Known issues in demo
Demo is hosted on heroku so it has some drawbacks:

* instance is running with `DEBUG=True` in order to use django static server -- this should not happen on production 
  environments but `secure-url` is a recruitment project and its not the main goal to check administrative skills
    * solution: https://devcenter.heroku.com/articles/django-assets
* uploaded media files are removed on each deploy or when heroku dyno is being freezed
    * solution: https://devcenter.heroku.com/articles/s3
* djangorestframework UI for browsing API is not disabled for demo purposes

## Know issues in project
 * uploaded files are now kept in public location defined by `MEDIA_ROOT` and are accessible by `MEDIA_URL`. 
   That's make them actually... not secured at all
    * possible solutions:
        * https://github.com/edoburu/django-private-storage
        * https://github.com/johnsensible/django-sendfile
