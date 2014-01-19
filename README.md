#ummbNet


##What

This is web-app for the University of Minnesota Pep Bands. It will serve as a request board for members to "trade shifts", picking up events when they want to, and finding others to take their place at events.


##Why

Each section has their own system for finding subs. Some sections use Facebook groups, the trumpets use an email listserv. It's not efficient, we get a lot of emails, and older requests get lost.


##How

Flask, SQLAlchemy, Postgres, running through uWSGI behind an nginx frontend.


##Who

Anyone who wants to help. I am receiving independent study credits for this, but if you want to help feel free.


##Getting Started

Dependencies:

+ Python 2.7+
+ `pip`

First, rename `sample-config.py	` to `config.py`. You will need to change the settings to match your database and mail server configuration, and change `SECRET_KEY` to a real secret key.

Run the following commands:

    $ git clone https://github.com/aterlumen/ummbNet.git
    $ cd ummbNet
    $ pip install -r requirements.txt
    $ python create_db.py
    $ python main.py
    
If you follow those steps you should have an empty copy of ummbNet running at `http://localhost:5000/`. There is currently no way to create a user with admin or director privileges through the web interface. You can create users programmatically in a python interpreter using the `is_admin` and `is_director` flags. 

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


##API

This is on the back burner until the web interface is more mature,


##License

All source code is open source and released under the MIT License. All user content is owned by its respective creator.

See `LICENSE` for more information.