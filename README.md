#ummbNet


##What

This is web-app for the University of Minnesota Pep Bands. It will serve as a request board for members to "trade shifts", picking up events when they want to, and finding others to take their place at events.


##Why

Each section has their own system for finding subs. Some sections use Facebook groups, the trumpets use an email listserv. It's not efficient, we get a lot of emails, and older requests get lost.


##How

Flask, SQLAlchemy, Postgres, running through uWSGI behind an nginx frontend. The maximum anticipated scale is ~350 total (not concurrent) users. But hey, we'll make it relatively scalable for fun.


##Who

Anyone who wants to help. I'll be upfront, I am receiving independent study credits for this, but if you want to help feel free.


##When

Right now.


##Getting Started

Dependencies:

+ Python 2.7+
+ `pip`
+ Flask

Run the following commands:

    $ git clone https://github.com/aterlumen/ummbNet.git
    $ cd ummbNet
    $ pip install -r requirements.txt
    $ python createDb.py
    $ python ummbNet.py
    
If you follow those steps you should have a copy of ummbNet running at `http://localhost:5000/`. 

To avoid extra configuration, the repo uses `sqlite` by default. If you'd like to use a different database system just change the line in `ummbNet.py` from:

`app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'`

to match your config.


##REST?

That's the plan. In case there's ever an urge to make iPhone and Android apps for this, the backend will be structured as a RESTful API. The web interface will add some quirks, but I plan to make sure they don't interfere with a clean RESTful interface.

##License

All source code is open source and released under the MIT License. All user content is owned by its respective creator.

See `LICENSE` for more information.