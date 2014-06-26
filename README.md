Ahmia - Tor Hidden Service Search
=================================

![https://ahmia.fi/](https://github.com/juhanurmi/ahmia/blob/master/ahmia/static/images/ahmia_logo.png)

https://ahmia.fi/

Compatibility
-------------

Ahmia requires Python 2.7+ and Django 1.6+ and YaCy

Installation
------------

- Currently, ahmia is listening YaCy from 10.8.0.10:8090.
- The YaCy connection is defined in settings.py.
- HTTP server is required.
- Please see /apache2/ to setup to run with Apache HTTP server.
- Note the crontabs. The order of the task is important.
- See crontabs file. It is strongly recommended to put crontask to another server than the web-server itself.

##### Install depencies:

```sh
$ pip install -r requirements.txt
$ apt-get install python-socksipy python-psycopg2 libapache2-mod-wsgi
```

##### Furthermore, you will need to set the rights to the tools:

```sh
$ chmod -R ugo+rx /usr/local/lib/ahmia/tools/
```

##### And to Apache:

```sh
$ chown -R www-data:www-data /usr/local/lib/ahmia/
$ chmod -R u=rwX,g=rX,o=rX /usr/local/lib/ahmia/
```

##### And after creating the SQLite database:

```sh
$ chown www-data:www-data /usr/local/lib/ahmia
$ chown www-data:www-data /usr/local/lib/ahmia/ahmia_db
```

##### Not required, but recommended for better system performance:

- Install haveged - A simple entropy daemon
- Edit the process and threads parameters of the WSGIDaemonProcess in apache2/sites-available/django-ahmia
- Use PostgreSQL
- Install PgBouncer: a lightweight connection pooler for PostgreSQL

Features
--------

- Search engine for Tor hidden services.
- Privacy: ahmia saves no IP logs.
- Filtering child abuse.
- Popularity tracking from Tor2web nodes, public WWW backlinks and the number of clicks in the search results.
- P2P YaCy backend.
- Hidden service online tracker.

Demo
----

You can try the demo by cloning this repository and running the test server with provided data:

```sh
$ python manage.py syncdb
$ python manage.py loaddata ahmia/fixtures/initial_data.json
$ python manage.py runserver
```

Then open your browser to http://localhost:8000

Tests
-----

Unittests:

```sh
$ python manage.py test ahmia/tests/
```

For developers
--------------

Please, at least, validate your Python code with:

```sh
$ pylint --rcfile=pylint.rc /ahmia/python_code_file.py
```

and fix the major problems.
