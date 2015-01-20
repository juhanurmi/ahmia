Ahmia - Tor Hidden Service Search
=================================

![https://ahmia.fi/](https://raw.githubusercontent.com/juhanurmi/ahmia/master/ahmia/static/images/ahmia_logo.png)

https://ahmia.fi/

Compatibility
-------------

Ahmia requires Python 2.7+ and Django 1.6+

The crawler is called Onionbot and it requires Apache Solr for the data.

Installation
------------

- Currently, ahmia is listening Solr from http://127.0.0.1:33433/
- HTTP server is required
- Please see /apache2/ to setup to run with Apache HTTP server
- Note the crontabs. The order of the task is important
- See crontabs file. It is strongly recommended to put crontask to another server than the web-server itself

##### Install depencies:

```sh
$ apt-get install libxml2-dev libxslt-dev python-dev
$ apt-get install libpq-dev
$ apt-get install python-socksipy python-psycopg2 libapache2-mod-wsgi
$ apt-get install libffi-dev
```

```sh
$ pip install -r requirements.txt
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

##### Move the Apache settings and adjust WSGI processes=X threads=Y

Upper limit to memory that Apache needs is X*Y*8MB. For instance, 4*16*8MB = 513MB.

```sh
cp apache2/sites-available/django-ahmia /etc/apache2/sites-available/django-ahmia
/etc/init.d/apache2 restart
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
$ pylint --rcfile=pylint.rc ./ahmia/python_code_file.py
```

and fix the major problems.
