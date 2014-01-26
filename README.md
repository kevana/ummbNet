#ummbNet

This is web-app for the University of Minnesota Pep Bands. It will serve as a request board for members to "trade shifts", picking up events when they want to, and finding others to take their place at events.


Each section has their own system for finding subs. Some sections use Facebook groups, the trumpets use an email listserv. It's not efficient, we get a lot of emails, and older requests get lost.


ummbNet is built with Flask and SQLAlchemy, it is web-server and database agnostic. The deployed version will be using Postgres, running through uWSGI behind nginx.


Anyone who wants to help is welcome. I am receiving independent study credits for this, but feel free to contribute.


##Getting Started

###Dependencies:

+ Python 2.7+
+ `pip`

###Installation:
First, rename `sample-config.py	` to `config.py`. You will need to change the settings to match your database and mail server configuration, and change `SECRET_KEY` to a real secret key.

Run the following commands:

    $ git clone https://github.com/aterlumen/ummbNet.git
    $ cd ummbNet
    $ mkdir log
    $ mkdir tmp
    $ pip install -r requirements.txt
    $ python create_db.py
    $ python main.py

`load_test_data.py` contains dummy data (users, events, requests) you can load into your db. Do not load this in production.

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

ummbNet uses python's `unittest` module. Tests are in the `testing` subfolder, split into separate files by test contents. To run all test cases and generate a code coverage report at `tmp/coverage/index.html` use the main test module:

    $ python testing/test-main.py

This may take a fair amount of time to run. To run individual test cases, call the test case file directly:

    $ python testing/sub_module_tests.py

##API

This is on the back burner until the web interface is more mature.


##License

All source code is open source and released under the MIT License. All user content is owned by its respective creator.

See `LICENSE` for more information.