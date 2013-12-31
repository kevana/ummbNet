#ummbNet


##What

This is web-app for the University of Minnesota Pep Bands. It will serve as a request board for members to "trade shifts", picking up events when they want to, and finding others to take their place at events.

----
##Why

Each section has their own system for finding subs. Some sections use Facebook groups, the trumpets use an email listserv. It's not efficient, we get a lot of emails, and older requests get lost.

----
##How

Flask, SQLAlchemy, Postgres, running through uWSGI behind an nginx frontend. The maximum anticipated scale is ~350 total (not concurrent) users. But hey, we'll make it relatively scalable for fun.

----
##Who

Anyone who wants to help. I'll be upfront, I am receiving independent study credits for this, but if you want to help feel free.

----
##When

Right now.

----
##REST?

That's the plan. In case there's ever an urge to make iPhone and Android apps for this, the backend will be structured as a RESTful API. The web interface will add some quirks, but I plan to make sure they don't interfere with a clean RESTful interface.
