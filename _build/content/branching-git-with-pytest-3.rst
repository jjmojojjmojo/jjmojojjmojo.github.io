Branching With Git And Testing With Pytest: A Comprehensive Guide: Part 3
#########################################################################
:date: 2019-04-26 9:00
:author: jjmojojjmojo
:category: tutorial
:tags: python; git; branching; development process
:slug: branching-git-with-pytest-3
:status: draft

.. include:: ../emojis.rst

In the final part of this guide, we'll simulate two developers working concurrently, in their own branches, on source that ends up causing a conflict. We'll learn how to resolve a conflict.

Setup
=====
As with the last section, you will need to make sure you've got everything set up as outlined in `part 1 <{filename}/branching-git-with-pytest.rst>`__.

.. tip::
    
    It's a good idea to review the steps below, but if you want to skip ahead, or you are only interested in this section and want to hit the ground running, you can run the following script:
    
    .. code-block:: console
        
        $ scripts/setup-part3.sh
        
    

Here's a condensed summary:

#. Ensure you have git, python 3.7+, and venv installed.
#. Make a bare clone of the base repository to act as our *remote*:
   
   .. code-block:: console
       
       $ git clone --bare git@github.com:jjmojojjmojo/random_quote.git random_quote_remote
   
#. Clone our remote:
   
   .. code-block:: console
   
       $ git clone random_quote_remote random_quote
   
#. Initialize the virtual environment, and install our requirements and project:
   
   .. code-block:: console
        
        $ cd random_quote
        $ python -m venv .
        $ source bin/activate
        (random_quote) $ pip install -r requirements.txt
        (random_quote) $ pip install -e .
   
#. Initialize the database, add some randomly generated quotes:
   
   .. code-block:: console
        
        (random_quote) $ python scripts/generate_quotes.py
        (random_quote) $ python
        >>>
   
   .. code-block:: pycon
        
        >>> from random_quote import util
        >>> util.init("test.db")
        util.ingest("quotes.csv", "test.db")
   
#. Add the changes from `part 1 <{filename}/branching-git-with-pytest.rst>`__ and `part 2 <{filename}/branching-git-with-pytest-2.rst>`__. If you had trouble or would like to skip all of that, you can simply copy the following files from :code:`scripts/state/part2`:
   
   .. code-block:: console
        
        (random_quote) $ cp scripts/state/part2/setup.py src/random_quote/
        (random_quote) $ cp scripts/state/part2/conftest.py src/random_quote/tests/
        (random_quote) $ cp scripts/state/part2/test_manager.py src/random_quote/tests/
        (random_quote) $ cp scripts/state/part2/test_wsgi.py src/random_quote/tests/
        
#. :code:`git commit` and :code:`git push` all of the changes so they'll be available for this part of the guide:
   
   .. code-block:: console
        
        (random_quote) $ git commit -a -m"Getting up to speed from the last two sections of the guide."
        (random_quote) $ git push origin master
        


Let's Add A Feature, Fix Another Bug, and *Step On Some Toes*!
==============================================================

In this part of the guide, we're going to simulate two developers working on different tasks in the same code base.

Developer **"A"** will be adding a new feature: "Quote of the Day".

This feature has the following requirements:

* Each day, a new random quote is selected, and made available at :code:`/`
* The quote is saved, and a list of historical quotes can be seen at :code:`/qotd`

Developer **"B"** will be fixing a bug: "Root is a 404".

This bug is more of an oversight. Remember when we first tested the app, visiting http://127.0.0.1:8080 would return a 404 "Not Found" error. This is not a great practice, even though it's technically true - we aren't putting anything at the "root" (or :code:`/`) location.

Ideally, we'd see some useful information there instead. So to fix this bug, developer B will be writing up a little info about what endpoints are available to be served when a request for :code:`/` comes in.

The astute reader might notice that these two tasks are in *conflict*. Both developers are changing what a request for :code:`/` returns.

This is good for us, because this makes it possible to walk through how to deal with conflicts |grin|.

.. note::
    
    In real life, this situation would have been avoided through basic communication. 
    
    The API is something that shouldn't be altered lightly, and so a discussion amongst developers *should* happen whenever it's going to change.
    
    However, things like this do happen from time to time. As you'll see below, the process we're using makes these issues a lot less of a problem, when they do crop up. |unicorn|
    

Before we begin, lets deactivate our virtual environment:

.. code-block:: console
    
    (random_quote) $ deactivate
    $ 
    

Clone Two Copies Of The Repository
==================================
To get started, lets clone two fresh copies of our :code:`random_quote_remote` bare repository that we made earlier. We'll call them simply :code:`a` and :code:`b` so we don't get confused |cool|.

First, make sure we're in the correct directory.

.. code-block:: console
    
    $ cd ..
    $ ls
    random_quote
    random_quote_remote
    
We can see from the output of :code:`ls` that our original checkout is present, and the special bare copy we made to use as a remote is there as well.

Next, :code:`git clone` the remote twice.

Make a copy for developer **A**:

.. code-block:: console
    
    $ git clone random_quote_remote a
    Cloning into 'a'...
    done.
    
And another for developer **B**:
    
.. code-block:: console
    
    $ git clone random_quote_remote b
    Cloning into 'b'...
    done.
    
.. tip::
    
    We're going to work on the feature first, then the bug, so things shouldn't be too confusing. But it might be a good idea to open two terminal windows, and tweak the settings so that they use different titles, or background colors, to help reinforce what's what.
    

Develper *A* Builds A New Feature: Quote Of The Day
===================================================
As touched on earlier, we want our code to have an end point that will always return the "quote of the day" for each 24-hour period. We'd also like to keep a historical record of all the previous quotes that were saved.

There are a few ways to approach this, but there are two main aspects that need to be designed:

#. Generating a random quote every day.
#. Keeping historical records of past quotes.

First, Lets Branch
------------------
In repository :code:`a`, create a new branch called :code:`qotd`:

.. code-block:: console
    
    $ cd a
    $ git checkout -b qotd
    Switched to a new branch 'qotd'
    

Init
----
Remember that since this is a fresh clone, we'll need to initialize the virtual environment.

.. code-block:: console
    
    $ python -m venv .
    $ source bin/activate
    (a) $ pip install -r requirements.txt
    (a) $ pip install -e .
    

Next, copy the database file from your other clone:

.. code-block:: console
    
    (a) $ cp ../random_quote/test.db .
    

Design: Daily Quotes
--------------------
Off hand, a few possibilities exist for handling this:

We could:

#. Define a process, that, at midnight each night, uses the :code:`RandomQuoteManager` to select a random quote. This would happen outside of the application or people using it. It could be a manual process, or `automated as a scheduled job or task <https://en.wikipedia.org/wiki/Cron>`__.
#. Write a function that will pre-generate random quotes for each day of a given time period. This could also be run by a human, or automated to happen on a given interval (once a year, once a month, etc).
#. Wait until a quote of the day is requested, generate it on demand and return it, or return the current quote of the day if it's already been generated.

The first two have advantages when the historical listing of previous quotes of the day is important - there will be a quote for every day, and if users need that, those approaches are more useful. There will never be a day (unless the process or function doesn't run or cover a particular day) where a quote isn't generated.

On the other hand, generating quotes on demand means that we'll only ever have quotes for days when *at least one user* requested a quote of the day. The advantage to this is that we never use more data than we needed.

There are other considerations as well. Generating the quote on demand means that the quote generation happens at most once per day (but also *at least* once per day), whereas the other two options can batch the load of generating quotes. In option 2, we could generate *thousands* of days of quotes if we wanted to, all at once. In this way, pre-populating the quotes takes the burden of generating a quote out of the process of a user requesting a quote of the day.

Our app is doing simple things and generating a random quote is a pretty quick process. So the impact on users, even if the quote of the day was generated for every single one, would be minimal. But in other cases, pre-loading is preferred, because the cost of generating the data that's being provided to the user is higher and can impact their ability to effectively use the application.

All that considered, our use case is pretty simple, and our process for making a quote of the day is lightweight, so we'll opt to generate our quote of the day on the fly, as needed. We'll build the functionality such that it's easy to automate this process later if generating a quote becomes more expensive, thus getting the best of both worlds.

.. tip::
    
    One other thing we can do that might help is use `the HTTP caching headers <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control>`__ to tell clients that they only need to make a new request to the quote of the day endpoint once per day.
    
    This is out of scope for this guide, but something to always consider when building web applications. |rainbow|
    

Design: Past Quotes Of The Day
------------------------------
The other aspect of this feature is concerned with keeping old quotes around after the day they're generated. 

Since we're already using a relational database, it's a good candidate for storing quotes of the day.

.. note::
    
    This may seem obvious, but it's another important thing to remember: just because we're already using a certain pattern or method of storing data, it doesn't automatically make it the *best* pattern or method. |cool|
    

We can add a new table, called :code:`quote_of_the_day` to store each generated quote. We'll query that database table and use SQL to return the right quote for the current day.

.. tip::
    
    We are building a rudimentary `cache <https://en.wikipedia.org/wiki/Cache_(computing)>`__ here. This approach is extremely useful in application development, especially web development.
    
    Now, we *could* use an outside mechanism to cache this information - a tool like `varnish <https://varnish-cache.org/>`__  (and `many others <https://en.wikipedia.org/wiki/Web_cache#Web_caching_software>`__) can be configured to cache a certain end point such that it refreshes at a given interval, like say, once a day.
    

Here's our updated ER diagram:

.. figure:: {filename}/images/branching-git-pytest/er-diagram-second-pass.png
   :align: center
   :figwidth: 80%
    
The new :code:`quote_of_the_day` table consists of four columns:

* :code:`quote_id`, an integer, the ID of the quote that was selected. We'll put a `foreign key constraint <https://en.wikipedia.org/wiki/Foreign_key>`__ on the :code:`id` column in the :code:`quotes` table

The other three columns will encode the day, month and year:

* :code:`day`, integer, the day of the year (1-31)
* :code:`month`, integer, the month (1-12)
* :code:`year`, integer, the year (e.g. 2019)

We'll put a `unique constraint <https://en.wikipedia.org/wiki/Unique_key>`__ on these three columns - this prevents anyone from inserting a second quote of the day for any given month/day/year.

By using three columns, we have a few benefits:

* integers are (usually) stored in a form that takes up less space/memory.
* we can easily get all the quotes for a given month, or year by just using a :code:`WHERE` clause:
  .. code-block:: sql
        
        -- Get all quote id's from March of 2025
        SELECT quote_id FROM qote_of_the_day WHERE month=3, year=2025
        
* we don't have to worry about the *time* portion of the typical date-time storage format (ISO8601, Julian, Unix). This means we don't have to worry about timezones, or what happens when a locale makes a date occur on a different day.

The SQL needed to generate the new table looks like this:

.. code-block:: sql
    
    CREATE TABLE IF NOT EXISTS quote_of_the_day (
        quote_id INTEGER NOT NULL,
        day INTEGER NOT NULL,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
        FOREIGN KEY(quote_id) REFERENCES quotes(id)
        UNIQUE(day, month, year)
    );
    

Design: API Endpoints
---------------------
Our new feature will require two new endpoints:

* a GET request to :code:`/` will show the quote of the day (and create it if it's not present), as a single JSON object.
* a GET request to :code:`/qotd` will return a JSON list of quote objects that were previously generated.

Implementation: Quote Of The Day API
------------------------------------
We'll opt to create a new psuedo-manager class, called :code:`QuoteOfTheDay`. It will be responsible for retrieving a quote for a given day. It will retrieve an existing quote if one is present, generate a new one and save it if not.

For convenience, we'll add an instance of :code:`QuoteOfTheDay` to :code:`RandomQuoteManager`, as the :code:`qotd` property.

.. figure:: {filename}/images/branching-git-pytest/application-overview-second-pass.png
   :align: center
   :figwidth: 80%

Before we start, we need to add the new table to our :code:`test.db` file. First, add the following to :code:`src/random_quote/schema.sql`:

.. code-block:: sql
    :linenostart: 11
    
    CREATE TABLE IF NOT EXISTS quote_of_the_day (
        quote_id INTEGER NOT NULL,
        day INTEGER NOT NULL,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
        FOREIGN KEY(quote_id) REFERENCES quotes(id)
        UNIQUE(day, month, year)
    );
    

Next we'll use our :code:`util.init()` function, as we did when originally setting up the database:

.. code-block:: console
    
    (a) $ python
    >>> from random_quote.util import init
    >>> init("test.db")
    >>> quit()
    

.. note::
    
    We can re-run :code:`init()` as often as we like because of the :code:`IF NOT EXISTS` clause in :code:`CREATE TABLE` and :code:`CREATE INDEX`. Otherwise, we'd have to either :code:`DROP` the old tables/index first, or run each :code:`CREATE` statement separately.
    

Now we can add the code for our :code:`QuoteOfTheDay` class. We'll place this in a new :code:`src/random_quote/qotd.py` module.

Here's the code you need to add.

.. code-block:: python
    
    """
    Generate a random quote of the day.
    """
    import sqlite3
    import datetime
    
    from . import util
    
    class QuoteOfTheDay:
        def __init__(self, db_filename, manager=None):
            if manager is None:
                from .manager import RandomQuoteManager
                self.manager  = RandomQuoteManager(db_filename)
            else:
                self.manager = manager
            
            self.conn = util.connection(db_filename)
            
        def _date_parts(self, date=None):
            """
            Helper method to convert a date to the day/month/year that is
            stored in the database.
            """
            if date is None:
                date = datetime.datetime.now()
                
            return (date.day, date.month, date.year)
        
        def get(self, date=None):
            """
            Return the quote of the day for a given date, or the current date
            if one isn't specified.
            
            If no quote exists for that date, one is generated and saved.
            """
            day, month, year = self._date_parts(date)
            
            c = self.conn.cursor()
            
            c.execute("""
                      SELECT quotes.quote,
                             quotes.created,
                             qotd.quote_id, 
                             qotd.day, 
                             qotd.month, 
                             qotd.year
                        FROM quotes, quote_of_the_day as qotd
                       WHERE quotes.id = qotd.quote_id 
                         AND day=? 
                         AND month=? 
                         AND year=?
                      """, 
                      (day, month, year))
            
            result = c.fetchone()
            
            if result is None:
                return self.add(date)
            else:
                return dict(result)
        
        def add(self, date=None):
            """
            Add a quote of the day for a given date, or the current date
            if one isn't specified.
            """
            day, month, year = self._date_parts(date)
            
            quote = self.manager.random()
            
            c = self.conn.cursor()
            
            c.execute("""
                INSERT INTO quote_of_the_day 
                            (quote_id, day, month, year) 
                     VALUES (?, ?, ?, ?)
               """, 
               (quote["id"], day, month, year))
            
            self.conn.commit()
            
            return {
                'quote_id': quote['id'],
                'quote': quote['quote'],
                'created': quote['created'],
                'day': day,
                'month': month,
                'year': year
            }
            
        def all(self):
            """
            Retrieve all existing quotes of the day.
            """
            c = self.conn.cursor()
            
            c.execute("""
                      SELECT quotes.quote,
                             quotes.created,
                             qotd.quote_id, 
                             qotd.day, 
                             qotd.month, 
                             qotd.year
                        FROM quotes, quote_of_the_day as qotd
                       WHERE quotes.id = qotd.quote_id
                    ORDER BY qotd.year, qotd.month, qotd.day
                      """)
            
            result = []
            
            for row in c.fetchall():
                result.append(dict(row))
                
            return result
            

.. explanation::
    
    **TODO**
    

The implementation is fairly straightforward, with the exception of the constructor. We're doing a conditional import to avoid circular imports because of the way the API is set up. This is sub-optimal, but the typical use case will be to provide a :code:`manager` object, so it's more there for the sake of completeness.

We'll also need to add an import to :code:`src/random_quote/__init__.py`, so we can access :code:`QuoteOfTheDay` from the :code:`random_quote.qotd` module:

.. code-block:: python
    :hl_lines: 4
    
    from . import manager
    from . import wsgi
    from . import util
    from . import qotd
    

Next we'll add the :code:`qotd` property to :code:`RandomQuoteManager` via it's constructor, in :code:`src/random_quote/manager.py`:

.. code-block:: python
    :hl_lines: 8 14 15 16 17 18 19
    
    """
    API code for dealing with the quote database.
    """
    
    import datetime
    import random
    from . import util
    from .qotd import QuoteOfTheDay
    
    RAND_MIN = -9223372036854775808
    RAND_MAX = 9223372036854775807
    
    class RandomQuoteManager:
        def __init__(self, db_filename, qotd=None):
            self.conn = util.connection(db_filename)
            if qotd is None:
                self.qotd = QuoteOfTheDay(db_filename, self)
            else:
                self.qotd = qotd
                
    ...
    

Note that we've allowed for an optional :code:`qotd` object to be passed to the constructor. If it's not passed, we create a new :code:`QuoteOfTheDay` object. We do this to allow flexibility in terms of re-using objects during testing.

It's a good idea to make a commit after this work is done. This should be second nature by now, but lets walk through the steps, since we're doing something new: adding an untracked file.

.. code-block:: console
    :hl_lines: 14
    
    (random_quote) $ git status
    On branch qotd
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)
    
        modified:   src/random_quote/__init__.py
        modified:   src/random_quote/schema.sql
        modified:   src/random_quote/manager.py
    
    Untracked files:
      (use "git add <file>..." to include in what will be committed)
    
        src/random_quote/qotd.py
        test.db
    
    no changes added to commit (use "git add" and/or "git commit -a")
    
Note that we now have a file we care about in the :code:`Untracked files` section, :code:`src/random_quote/qotd.py`.

We have to :code:`git add` it in order to get it into our commit:

.. code-block:: console
    
    (random_quote) $ git add src/random_quote/qotd.py
    
Now, :code:`git status` shows :code:`src/random_quote/qotd.py` as a new file:

.. code-block:: console
    :hl_lines: 6
    
    (random_quote) $ git status
    On branch qotd
    Changes to be committed:
      (use "git reset HEAD <file>..." to unstage)
    
        new file:   src/random_quote/qotd.py
    
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)
    
        modified:   src/random_quote/__init__.py
        modified:   src/random_quote/manager.py
        modified:   src/random_quote/schema.sql
    
    Untracked files:
      (use "git add <file>..." to include in what will be committed)
    
        test.db

Now :code:`git commit`:

.. code-block:: console
    
    (random_quote) $ git commit -a -m"Added first-pass of quote of the day functionality"
    [qotd 53ae911] Added first-pass of quote of the day functionality
     4 files changed, 132 insertions(+), 3 deletions(-)
     create mode 100644 src/random_quote/qotd.py
    

Back-End API Tests
------------------
We'll put the main quote of the day tests in :code:`src/random_quote/tests/test_qotd.py`. 

We'll make use of the :code:`preconfigured_manager()` fixture. This will use :code:`fix_random()`, and populate the database with some quotes for us.

Then add the tests to :code:`src/random_quote/tests/test_qotd.py`:

.. code-block:: python
        
    """
    Test the "Quote of the day" functionality.
    """
    
    import pytest
    import sqlite3
    import datetime
    
    def get_quote_id(conn, day, month, year):
        """
        Helper function to get a quote id for the given day/month/year
        """
        c = conn.cursor()
    
        c.execute("SELECT quote_id FROM quote_of_the_day WHERE day = ? AND month = ? AND year = ?", (day, month, year))
    
        result = c.fetchone()
    
        return result[0]
    
    def test_add_qotd(preconfigured_manager):
        """
        Add a new quote of the day, for the current day.
        """
        today = datetime.datetime.now()
    
        quote = preconfigured_manager.qotd.add()
    
        check = get_quote_id(preconfigured_manager.conn, today.day, today.month, today.year)
    
        assert check == quote["quote_id"]
    
    def test_add_qotd_with_date(preconfigured_manager):
        """
        Add a new quote of the day, for a given day.
        """
        date = datetime.datetime(day=1, year=2025, month=3)
    
        quote = preconfigured_manager.qotd.add(date)
    
        check = get_quote_id(preconfigured_manager.conn, 1, 3, 2025)
    
        assert check == quote["quote_id"]
    
    def test_add_duplicate(preconfigured_manager):
        """
        Try to add an additional quote of the day.
        """
        date = datetime.datetime(day=1, year=2025, month=3)
    
        preconfigured_manager.qotd.add(date)
    
        with pytest.raises(sqlite3.IntegrityError):
            preconfigured_manager.qotd.add(date)
    
    def test_get_without_date(preconfigured_manager):
        """
        Get a quote of the day, no date specified. Should create a new QOTD.
        """
        today = datetime.datetime.now()
    
        quote = preconfigured_manager.qotd.get()
    
        check = get_quote_id(preconfigured_manager.conn, today.day, today.month, today.year)
    
        assert check == quote["quote_id"]
    
    def test_get_with_date(preconfigured_manager):
        """
        Get a quote of the day, for a specified date. Should create a new QOTD.
        """
        date = datetime.datetime(day=1, year=2025, month=3)
    
        quote = preconfigured_manager.qotd.get(date)
    
        check = get_quote_id(preconfigured_manager.conn, 1, 3, 2025)
    
        assert check == quote["quote_id"]
    
    def test_all(preconfigured_manager):
        """
        Add and retrieve several quotes of the day.
        """
        date1 = datetime.datetime(day=1, year=2025, month=3)
        date2 = datetime.timedelta(days=1) + date1
        date3 = datetime.timedelta(days=1) + date2
    
        quote1 = preconfigured_manager.qotd.add(date1)
        quote2 = preconfigured_manager.qotd.add(date2)
        quote3 = preconfigured_manager.qotd.add(date3)
    
        result = preconfigured_manager.qotd.all()
    
        assert result[0] == quote1
        assert result[1] == quote2
        assert result[2] == quote3
        
    

Lets also add a new test case to :code:`src/random_quote/tests/test_manager.py` to make sure that the :code:`qotd` property exists:
     
.. code-block:: python
    :linenostart: 75
    
    def test_qotd(preconfigured_manager):
        """
        Ensure the qotd property exists.
        """
        from random_quote.qotd import QuoteOfTheDay
        
        assert isinstance(preconfigured_manager.qotd, QuoteOfTheDay)
        

Run the tests:

.. code-block:: console
    
    (a) $ pytest src
    ============================== test session starts ==============================
    platform darwin -- Python 3.7.3, pytest-4.6.2, py-1.8.0, pluggy-0.12.0
    rootdir: /Volumes/Untitled/Projects/branching-with-git-pytest/a
    collected 17 items
    
    src/random_quote/tests/test_manager.py .......                            [ 41%]
    src/random_quote/tests/test_qotd.py ......                                [ 76%]
    src/random_quote/tests/test_wsgi.py ....                                  [100%]
    
    =========================== 17 passed in 0.20 seconds ===========================
    

Now, :code:`git add` the :code:`src/random_quote/tests/test_qotd.py` file, and commit.

Implementation: Web API Endpoints
---------------------------------

Here's the updated path map:

.. figure:: {filename}/images/branching-git-pytest/path-map-second-pass.png
   :align: center
   :figwidth: 80%
   


To implement the quote of the day functionality in :code:`RandomQuoteApp`, we'll add the methods :code:`qotd()` and :code:`qotd_listing()` which will return the current quote of the day, or all quotes of the day, respectively:

.. code-block:: python
    :linenostart: 93
    
        def qotd(self, request):
            """
            Return today's quote of the day.
            """
            response = Response()
            
            response.json = self.manager.qotd.get()
            response.content_type = "application/json"
            
            return response
            
        def qotd_listing(self, request):
            """
            List all existing quotes of the day.
            """
            response = Response()
            
            response.json = self.manager.qotd.all()
            response.content_type = "application/json"
            
            return response
            
Then we need to update the routing, in :code:`__call__()`:

.. code-block:: python
    :linenostart: 25
    :hl_lines: 2 3 4 5 6
    
            try:
                if request.path == "/":
                    response = self.qotd(request)
                elif request.path == "/qotd":
                    response = self.qotd_listing(request)
                elif request.path == "/quotes":
                    response = self.listing(request)
                elif request.path.startswith("/quote"):
                    response = self.get(request)
                elif request.path == "/random":
                    response = self.random(request)
                else: 
                    raise HTTPNotFound()
                    
We can run the http server again and try it out in our browser:

.. code-block:: console
    
    (a) $ gunicorn -b 127.0.0.1:8080 -t 9999999 -w 1 --reload wsgi:app
    
If you look at http://127.0.0.1:8080, you'll notice a quote of the day is returned, instead of a 404:

.. figure:: {filename}/images/branching-git-pytest/screen-cap-root-second-pass.png
   :align: center
   :figwidth: 80%

And loading http://127.0.0.1:8080/qotd returns a list, showing the quote that was just generated:

.. figure:: {filename}/images/branching-git-pytest/screen-cap-qotd-first-pass.png
   :align: center
   :figwidth: 80%

Tests For The Web API
---------------------
Now we need to add tests to :code:`src/random_quote/tests/test_wsgi.py`. First we need to add a necessary import, since we're going to be using some functions from :code:`datetime`:

.. code-block:: python
    :hl_lines: 6
    
    """
    Functional tests of the WSGI application.
    """
    
    import pytest
    import datetime
    

Then add three new tests to the bottom of the file:

.. code-block:: python
    :linenostart: 68
    
    def test_get_root(preconfigured_wsgi_app):
        """
        Make a GET request for /
        """
        response = preconfigured_wsgi_app.get("/")
        
        json_quote = response.json
        
        today = datetime.datetime.now()
        quote = preconfigured_wsgi_app.app.manager.qotd.get(today)
        
        assert json_quote == quote
        
    def test_qotd_empty(preconfigured_wsgi_app):
        """
        Request the list of quotes of the day at /qotd - no existing quotes
        """
        response = preconfigured_wsgi_app.get("/qotd")
        
        quotes = response.json
        
        assert quotes == []
        
    def test_qotd(preconfigured_wsgi_app):
        """
        Request the list of quotes of the day at /qotd
        """
        today = datetime.datetime.now()
        quote1 = preconfigured_wsgi_app.app.manager.qotd.get(today)
        quote2 = preconfigured_wsgi_app.app.manager.qotd.get(datetime.datetime(year=2048, month=2, day=26))
        
        response = preconfigured_wsgi_app.get("/qotd")
        
        quotes = response.json
        
        assert len(quotes) == 2
        assert quotes[0] == quote1
        assert quotes[1] == quote2

.. tip::
    
    To quit :code:`gunicorn`, type control-C.
    

Running the tests, we see the new ones have been picked up:

.. code-block:: console
    :hl_lines: 25 26 27
    
    (a) pytest -v src
    ============================== test session starts ==============================
    platform darwin -- Python 3.7.3, pytest-4.6.2, py-1.8.0, pluggy-0.12.0 -- /Volumes/Untitled/Projects/branching-with-git-pytest/a/bin/python
    cachedir: .pytest_cache
    rootdir: /Volumes/Untitled/Projects/branching-with-git-pytest/a
    collected 20 items
    
    src/random_quote/tests/test_manager.py::test_add_quote PASSED             [  5%]
    src/random_quote/tests/test_manager.py::test_get_quote PASSED             [ 10%]
    src/random_quote/tests/test_manager.py::test_remove_quote PASSED          [ 15%]
    src/random_quote/tests/test_manager.py::test_all PASSED                   [ 20%]
    src/random_quote/tests/test_manager.py::test_random_quote PASSED          [ 25%]
    src/random_quote/tests/test_manager.py::test_unknown_id PASSED            [ 30%]
    src/random_quote/tests/test_manager.py::test_qotd PASSED                  [ 35%]
    src/random_quote/tests/test_qotd.py::test_add_qotd PASSED                 [ 40%]
    src/random_quote/tests/test_qotd.py::test_add_qotd_with_date PASSED       [ 45%]
    src/random_quote/tests/test_qotd.py::test_add_duplicate PASSED            [ 50%]
    src/random_quote/tests/test_qotd.py::test_get_without_date PASSED         [ 55%]
    src/random_quote/tests/test_qotd.py::test_get_with_date PASSED            [ 60%]
    src/random_quote/tests/test_qotd.py::test_all PASSED                      [ 65%]
    src/random_quote/tests/test_wsgi.py::test_get_quote PASSED                [ 70%]
    src/random_quote/tests/test_wsgi.py::test_all_quotes PASSED               [ 75%]
    src/random_quote/tests/test_wsgi.py::test_random_quote PASSED             [ 80%]
    src/random_quote/tests/test_wsgi.py::test_get_quote_unknown_id PASSED     [ 85%]
    src/random_quote/tests/test_wsgi.py::test_root PASSED                     [ 90%]
    src/random_quote/tests/test_wsgi.py::test_qotd_empty PASSED               [ 95%]
    src/random_quote/tests/test_wsgi.py::test_qotd PASSED                     [100%]
    
    =========================== 20 passed in 0.52 seconds ===========================
    
Commit your changes.

Version Bump
------------
As we did in `part 2 <{filename}/branching-git-with-pytest-2.rst>`__, change the version in :code:`setup.py`. This time, set the version to :code:`0.2.0`, since we have a new feature that is backwards-compatible with the :code:`0.1.0` version.

Don't forget to re-install (:code:`pip install -e .`), re-run the tests (:code:`pytest src`), and :code:`git commit` your changes.

Rebase To :code:`master`
------------------------
Since we've only done this process once, lets walk through it again.

First we need to :code:`git fetch` any outstanding remote changes:

.. code-block:: console
    
    (a) $ git fetch origin master
    
Next, interactive :code:`git rebase`:

.. code-block:: console
    
    (a) $ git rebase -i master
    
Be sure to :code:`pick` the oldest (first) commit, and :code:`squash` the rest. Don't forget to write a nice log entry when :code:`git rebase` gives you the chance.

You can try preserving the old commit messages and adding a summary on the first line:

.. code-block:: text
    
    FEATURE: Quote Of The Day
    
    Added first-pass of quote of the day functionality
    Added tests for Quote Of The Day feature
    Added HTTP API support for the quote of the day
    Set version to 0.2.0
    

Re-run the tests to make sure nothing went wrong (there should be 20 passing tests):

.. code-block:: console
    
    (a) $ pytest src
    ============================== test session starts ==============================
    platform darwin -- Python 3.7.3, pytest-4.6.2, py-1.8.0, pluggy-0.12.0
    rootdir: /Volumes/Untitled/Projects/branching-with-git-pytest/a
    collected 20 items
    
    src/random_quote/tests/test_manager.py .......                            [ 35%]
    src/random_quote/tests/test_qotd.py ......                                [ 65%]
    src/random_quote/tests/test_wsgi.py .......                               [100%]
    
    =========================== 20 passed in 0.61 seconds ===========================
    

Checkout And Merge :code:`master`
---------------------------------
First, :code:`git checkout` the :code:`master` branch:

.. code-block:: console
    
    (a) $ git checkout master
    Switched to branch 'master'
    Your branch is up to date with 'origin/master'.
    
Then :code:`git merge` to your :code:`qotd` feature branch:

.. code-block:: console
    
    (a) $ git merge qotd
    Updating c2a655e..150ba38
    Fast-forward
     src/random_quote/__init__.py           |   3 +-
     src/random_quote/manager.py            |   9 ++-
     src/random_quote/qotd.py               | 114 ++++++++++++++++++++++++++++++++++
     src/random_quote/schema.sql            |  11 +++-
     src/random_quote/tests/conftest.py     |  26 +++++++-
     src/random_quote/tests/test_manager.py |  10 ++-
     src/random_quote/tests/test_qotd.py    |  96 ++++++++++++++++++++++++++++
     src/random_quote/tests/test_wsgi.py    |  42 ++++++++++++-
     src/random_quote/wsgi.py               |  29 ++++++++-
     9 files changed, 332 insertions(+), 8 deletions(-)
     create mode 100644 src/random_quote/qotd.py
     create mode 100644 src/random_quote/tests/test_qotd.py

Run the tests again (:code:`pytest src`)
     
Push
----
Finally, publish the changes using :code:`git push`:

.. code-block:: console
    
    (a) $ git push origin master
    Enumerating objects: 25, done.
    Counting objects: 100% (25/25), done.
    Delta compression using up to 8 threads
    Compressing objects: 100% (13/13), done.
    Writing objects: 100% (14/14), 3.44 KiB | 3.44 MiB/s, done.
    Total 14 (delta 6), reused 0 (delta 0)
    To /Volumes/Untitled/Projects/branching-with-git-pytest/random_quote_remote
       c2a655e..150ba38  master -> master
       

Developer *B* Fixes A Bug And Deals With a Git Conflict
=======================================================

Now, switch to the :code:`b` clone. We're going to pretend that developer **B** is doing their bug-fix concurrently with the feature that developer **A** just pushed.

First, :code:`deactivate` the virtual environment:

.. code-block:: console
    
    (a) $ deactivate
    $
    
Then change into the :code:`b` directory:

.. code-block:: console
    
    $ cd ../b
    
Initialize, activate, install, run the tests:

.. code-block:: console
    
    $ python -m venv .
    $ source bin/activate
    (b) $ pip install -r requirements.txt
    (b) $ pip install -e .
    (b) $ pytest src
    ============================== test session starts ==============================
    platform darwin -- Python 3.7.3, pytest-4.6.2, py-1.8.0, pluggy-0.12.0
    rootdir: /Volumes/Untitled/Projects/branching-with-git-pytest/b
    collected 10 items
    
    src/random_quote/tests/test_manager.py ......                             [ 60%]
    src/random_quote/tests/test_wsgi.py ....                                  [100%]
    
    =========================== 10 passed in 0.49 seconds ===========================
    
Note there are only 10 tests. This is because our copy of :code:`master` is from *before* developer **A** did their work.

Next, copy the database file again, from your original :code:`random_quote` checkout (you could also re-inialize it if you'd like):

.. code-block:: console
    
    (a) $ cp ../random_quote/test.db .
    

Design
------
This bug fix is simply just returning *something* when an HTTP client makes a GET request for :code:`/`.

We'll add a static HTML file to the source that will provide links to, and useful info about, each of the API endpoints. It will be served when a GET request is made for :code:`/`.

We'll use the :code:`webob.static.FileApp` class to serve the file. This handles buffering and streaming properly for us.

Make The Branch
---------------
Lets check out and create our branch. We'll call this one :code:`index-info`:

.. code-block:: console
    
    (b) $ git checkout -b index-info
    Switched to a new branch 'index-info'
    

Fix The Bug
-----------
Lets construct a simple `HTML5 <https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5>`__ file that has the information about the API within it. The links will be *relative*. This allows for flexibility in how we host the API. We'll put it in a special directory within the source.

First, create the new :code:`src/random_quote/static` directory:

.. code-block:: console
    
    (b) $ mkdir src/random_quote/static
    
We're using this name because it indicates there are files that need to be served without being processed. We're setting up an entire directory to give us some flexibility in the future. We may want to add some additional static assets (such as images or CSS files) to our API documentation, or build some sort of front-end for the browser. We can switch to using the :code:`webob.static.DirectoryApp` class and serve the entire directory at once.

Add the following to :code:`src/random_quote/static/index.html`:

.. code-block:: html
    
    <!DOCTYPE html>
    <html>
    <head>
        <title>Random Quote API</title>
    </head>
    <meta charset="UTF-8">
    <body>
    <h1>Random Quote API</h1>
    <p>Welcome to the Random Quote API. This API provides random quote functionality via HTTP.</p>
    
    <h2>API Endpoints</h2>
    <p><em>All endpoints only work with GET requests. All responses are JSON</em></p>
    <dl>
        <dt><a href="quote/1">/quote/1</a></dt>
        <dd>Retrieve a specific quote by its ID. In this example, we are retrieving quote #1.</dd>
        <dt><a href="quotes">/quotes</a></dt>
        <dd>Retrieve all quotes.</dd>
        <dt><a href="random">/random</a></dt>
        <dd>Retrieve a random quote</dd>
    </dl>
    </body>
    </html>
    

Naming this file :code:`index.html` is a signal to other developers that this file is intended to be the default file served up when the :code:`/` (or *root* path) is requested. This is a convention that goes back to the early days of HTTP servers, and is still in use today.

We need a way to figure out where :code:`src/random_quote/static` lives. When this application is deployed as a python egg, it could be installed anywhere, and :code:`gunicorn` (or whatever WSGI server we use) could be running, again, anywhere. We need to find an absolute path to the :code:`src/random_quote/static` directory.

We have an example of how to do this already, in :code:`src/random_quote/util.py`, in the :code:`schema()` function:

.. code-block:: python
    :linenostart: 14
    
    def schema():
        """
        Return the location of the SQL schema.
        """
        return os.path.join(os.path.dirname(__file__), "schema.sql")
        
Here we use Python's built-in special :code:`__file__` variable that returns the path to the currently executing file (`more detail <http://www.blog.pythonlibrary.org/2013/10/29/python-101-how-to-find-the-path-of-a-running-script/>`__). We then use a couple of functions from the `os.path <https://docs.python.org/3/library/os.path.html>`__ module to construct a path in a system-agnostic way.

.. note::
    
    Python runs on many platforms, and most code you will write is compatible with all of them. It's best practice to construct paths using :code:`os.path` (or `pathlib <https://docs.python.org/3/library/pathlib.html#module-pathlib>`__). This abstracts away differences like using forward slashes (:code:`/`, unix-like systems) and backward slashes (:code:`\\`, windows), making it easy to switch platforms or run code in different developer environments.
    
We can do the same thing with our new :code:`static` directory. But since we may be using it to serve multiple files, we'll add a little extra functionality to request a more specific path if needed. We'll call the function :code:`static()`. Add the following to the end of :code:`src/random_quote/util.py`:

.. code-block:: python
    :linenostart: 58
    
    def static(path=None):
        """
        Return the full path to a file the static directory.
        """
        static = os.path.join(os.path.dirname(__file__), "static")
        
        if path:
            return os.path.join(static, path)
        else:
            return static
            
If we don't pass a :code:`path` argument, we get the path to just the :code:`static` directory, otherwise, the :code:`path` is added to the end.

.. tip::
    
    We're adding this flexibility because it's likely we'll want to serve other static files, like images, CSS, javascript, etc.
    

Next, we need to add an import for :code:`webob.static.FileApp`, and our new :code:`util.static()` function, to :code:`src/random_quote/wsgi.py`:

.. code-block:: python
    :hl_lines: 5 8
    
    """
    WSGI Applications
    """
    from . import manager
    from . import util
    from webob import Request, Response
    from webob.exc import HTTPError, HTTPNotFound, HTTPMethodNotAllowed, HTTPBadRequest
    from webob.static import FileApp
    import re
    
    class RandomQuoteApp:
    ...
    
And alter the routing:

.. code-block:: python
    :linenostart: 27
    :hl_lines: 2 3 4
    
            try:
                if request.path == "/":
                    response = FileApp(util.static("index.html"))
                elif request.path == "/quotes":
                    response = self.listing(request)
                elif request.path.startswith("/quote"):
                    response = self.get(request)
                elif request.path == "/random":
                    response = self.random(request)
                else: 
                    raise HTTPNotFound()
                    
                return response(environ, start_response)
            except HTTPError as error_response:
                return error_response(environ, start_response)
                

Lets start up the web server, and take a quick look:

.. code-block:: console
    
    (b) $ gunicorn -b 127.0.0.1:8080 -t 9999999 -w 1 --reload wsgi:app
    
If we visit http://127.0.0.1:8080 in a browser, we will see the new landing page. We can click the links and they should work.

.. figure:: {filename}/images/branching-git-pytest/screen-cap-root-third-pass.png
   :align: center
   :figwidth: 80%

Committing our changes is just like we've done before. Be sure to :code:`git add` the :code:`src/random_quote/static/index.html` file.

.. tip::
    
    Git is a bit odd about how it looks at files and directories. You may notice that running :code:`git status` lists the :code:`src/random_quote/static` directory, but not :code:`index.html` specifically.
    
    You can go ahead and :code:`git add` the :code:`src/random_quote/static` directory if you want. Just be aware that :code:`git add` will add *any* files it finds in that directory or its subdirectories. 
    

Test For The New Index Page
---------------------------

The test for this fix is pretty simplistic. We just need to make sure there isn't a 404 when making a GET request for :code:`/`. We can use :code:`TestApp` to do this, via the :code:`preconfigured_wsgi_app()` fixture established in :code:`src/random_quote/tests/conftest.py`.

We should also make sure we're getting the right *kind* of content, by checking the `Content-Type header <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type>`__.

Here's the most basic kind of test that meets these criteria. Add it to the end of :code:`src/random_quote/tests/test_wsgi.py`:

.. code-block:: python
    :linenostart: 67
    
    def test_get_root(preconfigured_wsgi_app):
        """
        Make a GET request for the root path.
        """
        response = preconfigured_wsgi_app.get("/")
        assert response.content_type == 'text/html'
        

.. tip::
    
    We could go further with this, and ensure the links actually work. `WebTest's response objects have a click() method <https://docs.pylonsproject.org/projects/webtest/en/latest/api.html#webtest.response.TestResponse.click>`__ that could be used to be a bit more thorough. 
    
We run the tests again to make sure our new case was picked up, and that we didn't break anything else:

.. code-block:: console
    :hl_lines: 19
    
    (b) $ pytest -v src
    
    ============================== test session starts ==============================
    platform darwin -- Python 3.7.3, pytest-4.6.2, py-1.8.0, pluggy-0.12.0 -- /Volumes/Untitled/Projects/branching-with-git-pytest/b/bin/python
    cachedir: .pytest_cache
    rootdir: /Volumes/Untitled/Projects/branching-with-git-pytest/b
    collected 11 items
    
    src/random_quote/tests/test_manager.py::test_add_quote PASSED             [  9%]
    src/random_quote/tests/test_manager.py::test_get_quote PASSED             [ 18%]
    src/random_quote/tests/test_manager.py::test_remove_quote PASSED          [ 27%]
    src/random_quote/tests/test_manager.py::test_all PASSED                   [ 36%]
    src/random_quote/tests/test_manager.py::test_random_quote PASSED          [ 45%]
    src/random_quote/tests/test_manager.py::test_unknown_id PASSED            [ 54%]
    src/random_quote/tests/test_wsgi.py::test_get_quote PASSED                [ 63%]
    src/random_quote/tests/test_wsgi.py::test_all_quotes PASSED               [ 72%]
    src/random_quote/tests/test_wsgi.py::test_random_quote PASSED             [ 81%]
    src/random_quote/tests/test_wsgi.py::test_get_quote_unknown_id PASSED     [ 90%]
    src/random_quote/tests/test_wsgi.py::test_get_root PASSED                 [100%]
    
    =========================== 11 passed in 0.20 seconds ===========================
    
Commit the tests.

Version Bump
------------
We've fixed a bug, and so we need to change the version number in :code:`setup.py` again. This time, it will be :code:`0.1.2`:

.. code-block:: python
    :hl_lines: 4
    
    from setuptools import setup, find_packages
    setup(
        name="random_quote",
        version="0.1.2",
        packages=['random_quote'],
        package_dir={'':'src'},
        install_requires=['webob'],
        include_package_data=True
    )
    

Be sure to :code:`pip install -e .` again and re-run the tests before committing your changes.
    
.. note::
    
    You'll notice that our version is now a whole rev behind the version we set when adding the "Quote of the day" feature. Remember, in our "b" repository, we're unaware those changes have been made.
    

Rebase
------

Lets proceed to do the rebase as usual.

First, we need to :code:`git fetch` any remote changes we haven't seen yet:

.. code-block:: console
    
    (b) $ git fetch
    remote: Enumerating objects: 29, done.
    remote: Counting objects: 100% (29/29), done.
    remote: Compressing objects: 100% (16/16), done.
    remote: Total 17 (delta 8), reused 0 (delta 0)
    Unpacking objects: 100% (17/17), done.
    From /Volumes/Untitled/Projects/branching-with-git-pytest/random_quote_remote
       c2a655e..9057fd0  master     -> origin/master
       
Unlike the last couple of times we called :code:`git fetch`, we actually have changes to download. This is evidenced by the output above.

When we run :code:`git rebase -i master`, it works as usual. Be sure to run the tests again (there should still only be *11* tests).

Merge, Now With *Problems*
==========================
Now we need to merge :code:`master` with our local :code:`index-info` branch.

First, we need to check out :code:`master`

.. code-block:: console
    
    (b) $ git checkout master
    Switched to branch 'master'
    Your branch is behind 'origin/master' by 1 commit, and can be fast-forwarded.
      (use "git pull" to update your local branch)
      
Note that git tells us that our branch is behind :code:`origin/master` by 1 commit, and suggests that we use :code:`git pull` to update. :code:`git pull` is like doing a :code:`fetch` followed by :code:`git merge`. 

Remember, this isn't *our* branch, all of our changes are still within the :code:`index-info` branch. We're just doing an update of changes to :code:`master`, that should merge without incident.

Lets do a :code:`git pull`:

.. code-block:: console
    
    (b) $ git pull
    Updating fa45753..5e45295
    Fast-forward
     setup.py                               |   2 +-
     src/random_quote/__init__.py           |   3 +-
     src/random_quote/manager.py            |   7 ++-
     src/random_quote/qotd.py               | 114 +++++++++++++++++++++++++++++++++++++++++++++++
     src/random_quote/schema.sql            |  11 ++++-
     src/random_quote/tests/test_manager.py |  10 ++++-
     src/random_quote/tests/test_qotd.py    |  96 +++++++++++++++++++++++++++++++++++++++
     src/random_quote/tests/test_wsgi.py    |  42 ++++++++++++++++-
     src/random_quote/wsgi.py               |  28 +++++++++++-
     9 files changed, 306 insertions(+), 7 deletions(-)
     create mode 100644 src/random_quote/qotd.py
     create mode 100644 src/random_quote/tests/test_qotd.py
     
You see we've pulled in the changes made to master while we were working. This doesn't affect our code in our local :code:`index-info` branch. For that, we need to :code:`git merge`:

.. code-block:: console
    
    (b) $ git merge index-info
    Auto-merging src/random_quote/wsgi.py
    CONFLICT (content): Merge conflict in src/random_quote/wsgi.py
    Auto-merging src/random_quote/tests/test_wsgi.py
    CONFLICT (content): Merge conflict in src/random_quote/tests/test_wsgi.py
    Auto-merging setup.py
    CONFLICT (content): Merge conflict in setup.py
    Automatic merge failed; fix conflicts and then commit the result.
    
**Oh no!** We have some *conflicts*. This means there are areas of files that git couldn't merge. Typically this means files where the changes are diffuse, or specific lines can't be matched up.

It's important to note that the files that are in conflict get marked up to preserve the conflict.

If you look into :code:`src/random_quote/tests/test_wsgi.py`, you can see what that looks like:

.. code-block:: python
    :linenostart: 68
    :hl_lines: 3 40 45
    
    def test_get_root(preconfigured_wsgi_app):
        """
    <<<<<<< HEAD
        Make a GET request for /
        """
        response = preconfigured_wsgi_app.get("/")
    
        json_quote = response.json
    
        today = datetime.datetime.now()
        quote = preconfigured_wsgi_app.app.manager.qotd.get(today)
    
        assert json_quote == quote
    
    def test_qotd_empty(preconfigured_wsgi_app):
        """
        Request the list of quotes of the day at /qotd - no existing quotes
        """
        response = preconfigured_wsgi_app.get("/qotd")
    
        quotes = response.json
    
        assert quotes == []
    
    def test_qotd(preconfigured_wsgi_app):
        """
        Request the list of quotes of the day at /qotd
        """
        today = datetime.datetime.now()
        quote1 = preconfigured_wsgi_app.app.manager.qotd.get(today)
        quote2 = preconfigured_wsgi_app.app.manager.qotd.get(datetime.datetime(year=2048, month=2, day=26))
    
        response = preconfigured_wsgi_app.get("/qotd")
    
        quotes = response.json
    
        assert len(quotes) == 2
        assert quotes[0] == quote1
        assert quotes[1] == quote2
    =======
        Make a GET request for the root path.
        """
        response = preconfigured_wsgi_app.get("/")
        assert response.content_type == 'text/html'
    >>>>>>> index-info

    

Now :code:`git status` shows the conflicting files:

.. code-block:: console
    :hl_lines: 5 17 18 19
    
    (b) git status
    On branch master
    Your branch is up to date with 'origin/master'.
    
    You have unmerged paths.
      (fix conflicts and run "git commit")
      (use "git merge --abort" to abort the merge)
    
    Changes to be committed:
    
        new file:   src/random_quote/static/index.html
        modified:   src/random_quote/util.py
    
    Unmerged paths:
      (use "git add <file>..." to mark resolution)
    
        both modified:   setup.py
        both modified:   src/random_quote/tests/test_wsgi.py
        both modified:   src/random_quote/wsgi.py
    
    Untracked files:
      (use "git add <file>..." to include in what will be committed)
    
        test.db


Taking a look at the the other two files in question, we see that the primary issue arises because we're doing two different actions when an HTTP client makes a GET request for :code:`/`. The secondary issue is that we have conflicting version numbers in :code:`setup.py`:

:code:`src/random_quote/wsgi.py`:

    .. code-block:: python
        :linenostart: 27
        
                try:
                    if request.path == "/":
        <<<<<<< HEAD
                        response = self.qotd(request)
                    elif request.path == "/qotd":
                        response = self.qotd_listing(request)
        =======
                        response = FileApp(util.static("index.html"))
        >>>>>>> index-info
    
:code:`setup.py`:

    .. code-block:: python
        
        from setuptools import setup, find_packages
        setup(
            name="random_quote",
        <<<<<<< HEAD
            version="0.2.0",
        =======
            version="0.1.2",
        >>>>>>> index-info
            packages=['random_quote'],
            package_dir={'':'src'},
            install_requires=['webob'],
            include_package_data=True
        )
        

Before we can resolve these conflicts, we need to make a decision about what's the *right* thing to do when a GET request is made for :code:`/`, and what the *correct* version number should be.

The "Quote Of The Day" feature added a quote of the day at :code:`/`. Our "API Index Information" bug fix added documentation at the same location.

.. note::
    
    This is **not** a conversation that should happen in a vacuum. This is a major API change, and as we mentioned before, ideally it would have been settled before the two developers even started working.
    
    Communication is key to avoid these conflicts, and it's the only way to get past them when they manage to get through.
    
    The first thing you should always do when a merge conflict happens is **reach out to the other developer** and make sure you're all on the same page.
    

Thinking about it objectively, it's probably best to keep the documentation at :code:`/`. That's the most useful for our users. 

Now, we need to figure out *how* one would request a quote of the day. 

The Quote Of The Day feature put the listing of all quotes of the day on :code:`/qotd`, but that endpoint is probably better suited for returning the today's quote of the day. 

So, now we just need a way to present all quotes of the day, so lets do that at :code:`/qotd-history`.

Here's an updated path map to show how things route:

.. figure:: {filename}/images/branching-git-pytest/path-map-third-pass.png
   :align: center
   :figwidth: 80%

    
Next, we need to decide which version number to use. In this case, we should consider the *end result* of our merge. 

Developer **B's** version is **0.1.2**, and developer **A's** is **0.2.0**. 

What we'll do is do the next *bug fix* version of the *API update*, which gives us **0.2.1**.

.. note::
    
    This has the advantage of also preserving any tags that were made for the two versions. We skipped that step here for the sake of brevity, but having three tags, one for **0.1.2**, **0.2.0** and **0.2.1** means we can deploy any of those three versions independently. This gives us a great deal of flexibility. |unicorn|
    

Lets fix :code:`setup.py` first. We just need to take out the markers (:code:`=====` and :code:`>>>>`) and any duplicated lines, leaving only the stuff we need. When you're finished, :code:`setup.py` will look like this:

.. code-block:: python
    
    from setuptools import setup, find_packages
    setup(
        name="random_quote",
        version="0.2.1",
        packages=['random_quote'],
        package_dir={'':'src'},
        install_requires=['webob'],
        include_package_data=True
    )
    

Now lets fix :code:`src/random_quote/wsgi.py`. The conflict is in :code:`__call__()`, in the routing.

.. code-block:: python
    :linenostart: 27
    
            try:
                if request.path == "/":
    <<<<<<< HEAD
                    response = self.qotd(request)
                elif request.path == "/qotd":
                    response = self.qotd_listing(request)
    =======
                    response = FileApp(util.static("index.html"))
    >>>>>>> index-info
                elif request.path == "/quotes":
                response = self.listing(request)
            elif request.path.startswith("/quote"):
                response = self.get(request)
            elif request.path == "/random":
                response = self.random(request)
            else: 
                raise HTTPNotFound()

To fix this, we need to preserve the case when the request looks for :code:`/`, but also add the new paths we discussed above.

.. code-block:: python
    :linenostart: 27
    
            try:
                if request.path == "/":
                    response = FileApp(util.static("index.html"))
                elif request.path == "/qotd":
                    response = self.qotd(request)
                elif request.path == "/qotd-history":
                    response = self.qotd_listing(request)
                elif request.path == "/quotes":
                    response = self.listing(request)
                elif request.path.startswith("/quote"):
                    response = self.get(request)
                elif request.path == "/random":
                    response = self.random(request)
                else: 
                    raise HTTPNotFound()
                    
                return response(environ, start_response)
            except HTTPError as error_response:
                return error_response(environ, start_response)
                

.. tip::
    
    You can use a `diff tool <https://en.wikipedia.org/wiki/Comparison_of_file_comparison_tools>`__ to fix merge conflicts in an interactive way. 
    
    Check out `git mergetool <https://git-scm.com/docs/git-mergetool>`__ for details.
    

Before we can do a manual test, we need to add the changes to the database schema. This is done using :code:`util.init()`, run from the interpreter:

.. code-block:: console
    
    (b) $ python
    Python 3.7.3 (default, Mar 30 2019, 03:37:43)
    [Clang 10.0.0 (clang-1000.11.45.5)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>
    

.. code-block:: pycon
    
    >>> from random_quote.util import init
    >>> init("test.db")
    

Now we can start up :code:`gunicorn` again:

.. code-block:: console
    
    (b) $ gunicorn -b 127.0.0.1:8080 -t 9999999 -w 1 --reload wsgi:app
    
And open http://127.0.0.1:8080,

    .. figure:: {filename}/images/branching-git-pytest/screen-cap-root-third-pass.png
       :align: center
       :figwidth: 60%
   
http://127.0.0.1:8080/qotd,
   
    .. figure:: {filename}/images/branching-git-pytest/screen-cap-qotd-second-pass.png
       :align: center
       :figwidth: 60%
   
And http://127.0.0.1:8080/qotd-history
   
    .. figure:: {filename}/images/branching-git-pytest/screen-cap-qotd-history.png
       :align: center
       :figwidth: 60%

The next conflict is in one of the test files, :code:`src/random_quote/tests/test_wsgi.py`. Lets fix that next.

The only conflict is near the bottom, where the 'qotd' tests step on the 'index-info' tests. We can fix this by moving some code around and changing the requested paths:

.. code-block:: python
    :linenostart: 68
    
    def test_get_root(preconfigured_wsgi_app):
        """
        Make a GET request for the root path.
        """
        response = preconfigured_wsgi_app.get("/")
        assert response.content_type == 'text/html'
    
    def test_qotd_empty(preconfigured_wsgi_app):
        """
        Request the list of quotes of the day at /qotd-history - no existing quotes
        """
        response = preconfigured_wsgi_app.get("/qotd-history")
    
        quotes = response.json
    
        assert quotes == []
    
    def test_qotd_listing(preconfigured_wsgi_app):
        """
        Request the list of quotes of the day at /qotd-history
        """
        today = datetime.datetime.now()
        quote1 = preconfigured_wsgi_app.app.manager.qotd.get(today)
        quote2 = preconfigured_wsgi_app.app.manager.qotd.get(datetime.datetime(year=2048, month=2, day=26))
    
        response = preconfigured_wsgi_app.get("/qotd-history")
    
        quotes = response.json
    
        assert len(quotes) == 2
        assert quotes[0] == quote1
        assert quotes[1] == quote2
    
    def test_qotd(preconfigured_wsgi_app):
        """
        Retrieve the current quote of the day
        """
        response = preconfigured_wsgi_app.get("/qotd")
    
        json_quote = response.json
    
        today = datetime.datetime.now()
        quote = preconfigured_wsgi_app.app.manager.qotd.get(today)
    
        assert json_quote == quote
    def test_get_root(preconfigured_wsgi_app):
        """
        Make a GET request for the root path.
        """
        response = preconfigured_wsgi_app.get("/")
        assert response.content_type == 'text/html'
    
    def test_qotd_empty(preconfigured_wsgi_app):
        """
        Request the list of quotes of the day at /qotd-history - no existing quotes
        """
        response = preconfigured_wsgi_app.get("/qotd-history")
    
        quotes = response.json
    
        assert quotes == []
    
    def test_qotd_listing(preconfigured_wsgi_app):
        """
        Request the list of quotes of the day at /qotd-history
        """
        today = datetime.datetime.now()
        quote1 = preconfigured_wsgi_app.app.manager.qotd.get(today)
        quote2 = preconfigured_wsgi_app.app.manager.qotd.get(datetime.datetime(year=2048, month=2, day=26))
    
        response = preconfigured_wsgi_app.get("/qotd-history")
    
        quotes = response.json
    
        assert len(quotes) == 2
        assert quotes[0] == quote1
        assert quotes[1] == quote2
    
    def test_qotd(preconfigured_wsgi_app):
        """
        Retrieve the current quote of the day
        """
        response = preconfigured_wsgi_app.get("/qotd")
    
        json_quote = response.json
    
        today = datetime.datetime.now()
        quote = preconfigured_wsgi_app.app.manager.qotd.get(today)
    
        assert json_quote == quote
        
Now we can run the tests to make sure everything still works:

.. code-block:: console
    
    (b) $ pytest src
    ================================ test session starts =================================
    platform darwin -- Python 3.7.3, pytest-4.6.3, py-1.8.0, pluggy-0.12.0
    rootdir: /Volumes/Untitled/Projects/branching-with-git-pytest/b
    collected 21 items
    
    src/random_quote/tests/test_manager.py .......                                 [ 33%]
    src/random_quote/tests/test_qotd.py ......                                     [ 61%]
    src/random_quote/tests/test_wsgi.py ........                                   [100%]
    
    ============================= 21 passed in 0.36 seconds ==============================
        

Before we proceed, we have one last thing to do: we need to update the web API documentation at :code:`/` to reflect the new API endpoints that we added as part of resolving the conflicts.

Documentation Update
--------------------
Add the following links to :code:`src/random_quote/static/index.html`:

.. code-block:: html
    :linenostart: 20
    
        <dt><a href="qotd">/qotd</a></dt>
        <dd>Retrieve today's "Quote of the day."</dd>
        <dt><a href="qotd-history">/qotd-history</a></dt>
        <dd>Retrieve all previous "Quote of the day." entries.</dd>
        
    
Start up :code:`gunicorn` again:

.. code-block:: console
    
    (b) $ gunicorn -b 127.0.0.1:8080 -t 9999999 -w 1 --reload wsgi:app
    
If we open http://127.0.0.1:8080 in a browser, the new page is shown, and the links do what they're supposed to.

.. figure:: {filename}/images/branching-git-pytest/screen-cap-root-fourth-pass.png
   :align: center
   :figwidth: 80%

Complete the merge
------------------
Now that we've untangled this mess, we need to finish up the merge.

:code:`git status` reminds us that we're in the middle of merging:

.. code-block:: console
    
    (b) $ git status
    On branch master
    Your branch is up to date with 'origin/master'.
    
    You have unmerged paths.
      (fix conflicts and run "git commit")
      (use "git merge --abort" to abort the merge)
    
    Changes to be committed:
    
        new file:   src/random_quote/static/index.html
        modified:   src/random_quote/util.py
    
    Unmerged paths:
      (use "git add <file>..." to mark resolution)
    
        both modified:   setup.py
        both modified:   src/random_quote/tests/test_wsgi.py
        both modified:   src/random_quote/wsgi.py
    
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)
    
        modified:   src/random_quote/static/index.html
    
    Untracked files:
      (use "git add <file>..." to include in what will be committed)
    
        test.db

To finish the merge, we first need to let git know the conflicted files are fixed. We do this by using :code:`git add`:

.. code-block:: console
    
    (b) $ git add src/random_quote/tests/test_wsgi.py
    (b) $ git add src/random_quote/wsgi.py
    (b) $ git add setup.py
    
Now :code:`git status` tells us what we need to do next:

.. code-block:: console
    :hl_lines: 5 6
    
    (b) $ git status
    On branch master
    Your branch is up to date with 'origin/master'.
    
    All conflicts fixed but you are still merging.
      (use "git commit" to conclude merge)
    
    Changes to be committed:
    
        modified:   setup.py
        new file:   src/random_quote/static/index.html
        modified:   src/random_quote/tests/test_wsgi.py
        modified:   src/random_quote/util.py
        modified:   src/random_quote/wsgi.py
    
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)
    
        modified:   src/random_quote/static/index.html
    
    Untracked files:
      (use "git add <file>..." to include in what will be committed)
    
        test.db
        

Now to finish the merge, we just need to do what :code:`git status` is telling us: :code:`git commit`:

.. code-block:: console
    
    (b) $ git commit -a -m"Resolved API endpoint conflicts"
    [master 36c0796] Resolved API endpoint conflicts
    
Now we can :code:`git push` our changes to the remote:

.. code-block:: console
    
    (b) $ git push origin master
    Enumerating objects: 37, done.
    Counting objects: 100% (36/36), done.
    Delta compression using up to 8 threads
    Compressing objects: 100% (18/18), done.
    Writing objects: 100% (23/23), 2.59 KiB | 2.59 MiB/s, done.
    Total 23 (delta 12), reused 0 (delta 0)
    To /Volumes/Untitled/Projects/branching-with-git-pytest/random_quote_remote
       9057fd0..5ccabd1  master -> master
       
Tag The Fixed Version
=====================

As a last step, we just need to :code:`git tag` our new version, and push it to the remote:

.. code-block:: console
    
    (b) $ git tag v0.2.1
    (b) $ git push origin v0.2.1
    Total 0 (delta 0), reused 0 (delta 0)
    To /Volumes/Untitled/Projects/branching-with-git-pytest/random_quote_remote
     * [new tag]         v0.2.1 -> v0.2.1
     
Conclusion
==========
In this final section, we covered resolving merge conflicts.

Now, you should be well-versed in working with git branches and using pytest to ensure you don't break things. |unicorn|

If you have any ideas, problems, or suggestions, don't hesitate to `contact the author <{filename}/pages/contact.rst>`__. 

Resources, What To Do If You Messed Up
======================================
Feel free to `contact the author <{filename}/pages/contact.rst>`__ if you have any problems with this guide. 

Check out http://sethrobertson.github.io/GitFixUm/fixup.html for a nice general git troubleshooting guide! It's extremely well done. 