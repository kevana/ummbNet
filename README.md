#ummbNet

A web app for the University of Minnesota Pep Bands. It serves as a request board for members to easily trade performance spots while keeping the directors informed of who will be at each event.

It started as an independent study project to dive into Python web development. The first version with minimal functionality is live now. As time permits, a long list of security and usability changes will be implemented. It is very much a work in progress.

ummbNet is built with Flask and SQLAlchemy. The deployed version (at [ummb.net](http://ummb.net)) runs through uWSGI behind nginx with a Postgres database.

##Getting Started

###Dependencies:

+ Python 2.7+
+ `pip`

###Installation:
First, rename `sample-config.py	` to `config.py`. You will need to change the settings to match your database and mail server configuration, and change `SECRET_KEY` to a real secret key.

Run the following commands:

    $ git clone https://github.com/kevana/ummbNet.git
    $ cd ummbNet
    $ mkdir log
    $ mkdir tmp
    $ pip install -r requirements.txt
    $ python create_db.py
    $ python main.py

`requirements.txt` includes psycopg2 for use with a Postgres database. To use a different database system you will need to install the DBAPI for it (e.g. mysql-python for MySQL).

Optional: `load_test_data.py` contains dummy data (users, events, requests) to see how it looks with content.

    $ python load_test_data.py

If you follow those steps you should have a copy of ummbNet running at `http://localhost:5000/`. There is currently no way to create a new user with admin or director privileges through the web interface. You can create users programmatically in a python interpreter using the `is_admin` and `is_director` flags. 

Example:

    $ cd ummbNet
    $ source env/bin/activate
    (env)$ python
    >>> from main import *
    >>> admin = User(username='admin', \
    ...              email='admin@example.com', \
    ...              password='PASSWORD', \
    ...              is_admin=True, \
    ...              is_director=True)
    ...
    >>> db.session.add(admin)
    >>> db.session.commit()

###Testing

ummbNet uses python's `unittest` module. Tests are in the `testing` subfolder, split into separate files nominally by feature. To run all test cases and generate a code coverage report at `tmp/coverage/index.html` use the main test module:

    $ python testing/test-main.py

This may take a fair amount of time to run. To run individual test cases, call the test case file directly:

    $ python testing/sub_module_tests.py

# Toolbox

What I've used to make ummbNet so far. 

Flask extensions:
* Flask-Bcrypt
* Flask-Login
* Flask-Mail
* Flask-Migrate
* Flask-SQLAlchemy
* Flask-WTF

UI eye candy: Twitter's [Bootstrap](http://getbootstrap.com/)

##License

All source code is released under the MIT License. All user content is owned by its respective creator.

See `LICENSE` for more information.
