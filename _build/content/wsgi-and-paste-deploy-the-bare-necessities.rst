WSGI and Paste Deploy: The Bare Necessities
###########################################
:date: 2011-03-30 17:03
:author: lionfacelemonface
:category: Uncategorized
:slug: wsgi-and-paste-deploy-the-bare-necessities

Using paster to create layouts for various types of projects is great,
especially when you need to get up and running quickly. The downside, is
that that sometimes the hand-holding, even along with some `amazing
documentation <http://docs.pylonsproject.org/docs/pyramid.html>`__,
doesn't give you the whole story.

I'm in the planning stages for a new project, and although I'm still on
the fence as to what we'll use to develop it, I'm sweet on
`Pyramid <http://pylonsproject.org/>`__. However, I'm also a WSGI n00b,
and haven't used the paste stack for anything beyond building plone
buildouts and archetypes boilerplate. That means that
`PasteDeploy <http://pythonpaste.org/deploy/>`__ is not in my playbook.
There are some great `PasteScript <http://pythonpaste.org/script/>`__
templates provided by the Pyramid project to get started quickly, but I
didn't see any good explanation of *why* the files were created, and how
they actually worked, even in the super-awesome Pyramid docs.

*Disclaimer: I didn't look that hard. :P*

So, to ease my pain, I got back to basics. I started with a fresh egg,
the PasteDeploy documentation and `PEP
333 <http://www.python.org/dev/peps/pep-0333/>`__. I came up with the
absolute, bare-minimum code, setup, and config necessary to produce a
functioning (albeit boring) WSGI application, and the necessary glue to
run it via PasteDeploy.

If you're the type that doesn't need much explaination and just want to
look at the code, go `right to the
source <http://code.google.com/p/lionfacelemonface/source/browse/trunk/pastedeploy-minimal/trunk>`__
(`checkout
instructions <http://code.google.com/p/lionfacelemonface/source/checkout>`__)

Prerequisites
-------------

You'll need, at minimum, a modern version of python (I used the 2.6
version that ships with Debian Squeeze),
`virtualenv <http://pypi.python.org/pypi/virtualenv>`__, and some way to
`install virtualenv <http://pypi.python.org/pypi/pip>`__.

I'll leave getting virtualenv installed as an exercise for the reader :)

I'm going to assume you're in a Linux environment in the few times we
need to interact with the operating system. As far as I know, this
should work on any operating system Python runs on, but as always, your
mileage may vary.

Environment
-----------

::

    $ virtualenv fun-minimal-wsgi
    $ cd fun-minimal-wsgi
    $ source bin/activate
    (fun-minimal-wsgi)$ easy_install PasteScript PasteDeploy

| 
|  If for some reason you're not familiar with virtualenv (and if you're
  a python developer, you really should be, it's great), these commands:

#. Sets up a sandbox python environment (but will use system packages if
   they exist and haven't been overridden locally)
#. Puts you into that environment
#. Installs PasteDeploy

To get out of the environment, you can type ``deactivate``:

::

    (fun-minimal-wsgi)$ deactivate

Bare-Minimum Egg
----------------

We'll store our WSGI code in a simple python egg, that is
setuptools-enabled (pretty much the standard). This requires a couple of
directories, and some special files (I based this off of output of the
PasteScript 'basic\_namespace' template, for details about what this
means, see `the setuptools
docs <http://peak.telecommunity.com/DevCenter/setuptools>`__).

| Here's what the layout looks like:

::

    fun-minimal-wsgi\
    --> minimal\
    -----> minimal\
    ---------> __init__.py
    -----> setup.py

Here's a quick list of commands to create an empty version of that
layout (assume that we're still in the ``fun-minimal-wsgi`` directory):

::

    (fun-minimal-wsgi)$ mkdir minimal
    (fun-minimal-wsgi)$ touch minimal/setup.py
    (fun-minimal-wsgi)$ mkdir minimal/minimal
    (fun-minimal-wsgi)$ touch minimal/minimal/__init__.py

The basic idea here is we have an egg source directory ``minimal``,
containing a ``setup.py`` file, used to install and configure it, and a
singular package, also called ``minimal`` (coincidentally... what it's
named is not a requirement of setuptools).

Now for the contents of ``setup.py``:

::

    from setuptools import setup, find_packages
    import os

    version = '1.0'

    setup(name='minimal',
          version=version,
          description="",
          long_description="""
             Very, very minimal example of a WSGI application and middleware.
          """,
          # Get more strings from
          # http://pypi.python.org/pypi?:action=list_classifiers
          classifiers=[
            "Programming Language :: Python",
            ],
          keywords='',
          author='Josh Johnson',
          author_email='none of your beeswax@somehost.com',
          url='http://lionfacelemonface.wordpress.com',
          license='BSD',
          include_package_data=True,
          packages=['minimal',],
          zip_safe=False,
          install_requires=[
              'setuptools',
          ],
          entry_points="""
          """,
          )

This is, at its bare minimum, all you need to say you've got an egg. :)

You could run ``python setup.py develop`` and start using it in your
virtual environment (but don't yet), not that it does anything yet :)

Bare-Minimum WSGI App
---------------------

This code goes into ``minimal/minimal/__init__.py``. This is right out
of PEP 333, with a couple of changes to take out any logic, and show all
of the possible ways to create a WSGI app, and WSGI middleware.

::

    # simple_app and AppClass are right out of PEP 333
    def simple_app(environ, start_response):
        """Simplest possible application object"""
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello world!\n']
        
    class AppClass:
        """Produce the same output, but using a class

        (Note: 'AppClass' is the "application" here, so calling it
        returns an instance of 'AppClass', which is then the iterable
        return value of the "application callable" as required by
        the spec.

        If we wanted to use *instances* of 'AppClass' as application
        objects instead, we would have to implement a '__call__'
        method, which would be invoked to execute the application,
        and we would need to create an instance for use by the
        server or gateway.
        """

        def __init__(self, environ, start_response):
            self.environ = environ
            self.start_response = start_response

        def __iter__(self):
            status = '200 OK'
            response_headers = [('Content-type', 'text/plain')]
            self.start_response(status, response_headers)
            yield "Hello world!\n"

    # not in PEP 333, but mentioned in the comments to AppClass
    class AlternateAppClass:
        def __call__(self, environ, start_response):
            status = '200 OK'
            response_headers = [('Content-type', 'text/plain')]
            start_response(status, response_headers)
            return ['Hello world!\n']

    class MinimalMiddleware:
        """
        Bare-minimum, doesn't do anything at all, middleware.
        """
        def __init__(self, application):
            self.application = application
            
        def __call__(self, environ, start_response):
            return self.application(environ, start_response)

    class SimpleMiddleware:
        """
        Takes a prefix, and appends it to each line in the response.
        """
        def __init__(self, application, prefix):
            self.application = application
            self.prefix = prefix

        def __call__(self, environ, start_response):
            response = self.application(environ, start_response)
            return ['%s %s' % (self.prefix, s) for s in response]

| 
|  Read PEP 333 for full explainations, but here's the gist:

**WSGI apps** are super simple. At minimum, they're a simple function
(``simple_app``), and at their most complex, a simple that implements
the iterator protocol (``AppClass``). The function, or the ``__call__``
method (in the case of ``AppClass``, ``__init__`` is standing in for
``__call__``) take a '``start_response``\ ' callable and a dictionary
with environment information (think CGI variables). They then use the
callable to set the necessary response code and headers (in our case
'200 OK' and 'Content-Type: text/plain'), then return an iterable, where
each member is a line in the output to send to the browser.

The ``AppClass`` example is probably a good way to implement a WSGI app
class, but it's not the simplest. What's required is a callable, so any
object that implements a ``__call__`` method and returns an iterable.
``AppClass`` implements the iterator protocol and short-circuits the
need for instantiation. For the sake of clarity and throughness, I added
the ``AlternateAppClass`` class to illustrate this.

We'll see the functional difference later when it's being wired up for
use by PasteDeploy.

**WSGI Middleware** works like a bucket-brigade. An application object
is passed from middleware class to middleware class until all are
called. The middleware is instantiated with an application object, and
when called is expected to return a response. I've included a simplified
minimal implementation (``MinimalMiddleware``), and an implementation
that manipulates the request before returning it (SimpleMiddleware).

**Note:** In the event that you're trying to jump ahead, this code might
not run out of the box. I'm allowing a configuration option to be passed
to ``SimpleMiddleware``, and since it's required, it would fail.

PasteDeploy Configuration - Application
---------------------------------------

| Now for the server part. You'll need to call this file something
  useful and put it somewhere you can get to (I've put it in the egg,
  ``minimal/minimal.ini``).

::

    [app:main]
    use = egg:minimal

    [server:main]
    use = egg:Paste#http
    host = 0.0.0.0
    port = 6543

This does two things. It tells PasteDeploy to look in the egg called
'minimal' for an 'app-factory' *entry point* called *main* (more on this
in a bit). It then configures the server.

Glue - Application
------------------

Before we can run the server we have to do three things: create an
application factory, add the entry point specified in ``minimal.ini``,
and then install the egg.

The factory is simply a callable that returns a WSGI application. We'll
add this to ``minimal/minimal/__init__.py``.

::

    ...
    def main(global_config, **settings):
        # settings comes from paste deploy, whatever values were in the section of the 
        # deployment config file
        if settings.get('use_class', False):
            return AppClass
        elif settings.get('use_alt_class', False):
            return AlternateAppClass()
        else:
            return simple_app
    ...

An application factory, for PasteDeploy, is a callable that takes a
config object (the contents of the whole config file), and any number of
keyword arguments, which correspond to the other options mentioned in
the config file (in our case, had we put ``toggle = True`` in
``[app:main]``, that argument would be passed along to our factory)

I've added a few config options that the factory can respond to, to make
it easy to try out the different ways of implementing the same WSGI
application.

Now for the entry point, the real glue that ties PasteDeploy with our
code.

| We'll add the following to ``setup.py`` in the call to ``setup()``:

::

    ...
          entry_points="""
          [paste.app_factory] 
          main = minimal:main
          """,
    ...

Note that ``minimal:main`` maps directly to the ``main()`` function we
created as our application factory. Had we named it something else, or
if we wanted to provide multiple app factories for whatever reason, we
could specify them one after the other, the name of the entry point
(what we'd reference in ``minimal.ini``), and a path to the function.
The name ``main`` is just the default, and used as a
convention/convienence. Here are some other examples:

-  Put ``use = egg:minimal#otherapp`` in ``minimal.ini``, and
   ``otherapp = minimal:some_other_function_in_init`` in ``setup.py``
-  Put ``use = egg:minimal#main`` in ``minimal.ini``, and
   ``main = minimal.some_package:other_function`` in ``setup.py``
-  Put ``use = egg:minimal#other`` in ``minimal.ini``, and
   ``main = minimal.some_package.package_deeper:other_function`` in
   ``setup.py``

You get the idea.

Install the Egg
---------------

We'll want to install this in *develop* mode, so changes to the code
will be reflected as soon as they are made.

**Note:** entry points are only updated when the egg is installed, so
you'll have to repeat this procedure every time you make a change to
them in your egg.

*Make sure you've activated your virtual environment before you do
this!*

::

    (fun-minimal-wsgi)$ cd minimal
    (fun-minimal-wsgi)$ python setup.py develop
    (fun-minimal-wsgi)$ cd ..

Starting The Server
-------------------

Now we should be able to start the server using the ``paster serve``
command.

::

    (fun-minimal-wsgi)$ paster serve minimal/minimal.ini --reload

You can now navigate to http://127.0.0.1:6543 and you should see 'hello
world'

Since we specified ``--reload``, we should be able to make changes to
the application code and ``minimal.ini`` and the server will reload for
us (remember the note about entry points though).

PasteDeploy Configuration - Middleware
--------------------------------------

Things will change a little bit now:

::

    [app:minimal_app]
    use = egg:minimal

    [filter:middleware]
    use = egg:minimal
    prefix = yikes:

    [pipeline:main]
    pipeline =
        middleware
        minimal_app
    ...

Here we changed the ``[app:main]`` heading to an easy-to-refer-to name.
We then defined the middleware part (middleware is called 'filters' in
PasteDeploy configs), and a ``pipeline``, which links up the middleware
and the application.

The middleware specified here is also called 'main'.

Note we've also specified a parameter to the middleware. If we didn't
need to, we could have just used ``egg:minimal`` in the
``[pipeline:main]`` section, in replace of ``[middleware]``

**Note:** This will break your running server instance, since we are
referring to a filter factory that doesn't exist.

Glue - Middleware
-----------------

Now to make the middleware work. We'll need to a new entry point to
``minimal/setup.py``, so it now looks like this:

::

    ...
          entry_points="""
          [paste.app_factory] 
          main = minimal:main
          
          [paste.filter_factory]
          main = minimal:middleware
          """,
    ...

Again, the name of the entry point is not significant, and ``main`` is
used as the default so we don't have to specify it in the ini file.

Now for the filter factory in ``minimal/minimal/__init__.py``:

::

    ...
    # middleware factory for paste deploy
    def middleware(global_config, **settings):
        prefix = settings.get('prefix', 'Booyeah:')
        
        def factory(app):
            return SimpleMiddleware(app, prefix)
        
        return factory

Here, we're using the ``SimpleMiddleware`` class, and finally
utilizing/providing the ``prefix`` parameter.

Now we can re-install the egg (to get the new entry point) and restart
the server.

::

    (fun-minimal-wsgi)$ cd minimal
    (fun-minimal-wsgi)$ python setup.py develop
    (fun-minimal-wsgi)$ cd ..
    (fun-minimal-wsgi)$ paster serve minimal/minimal.ini --reload

Now, visiting http://127.0.0.1:6543 will look a little different.

The same middleware can be added to the pipeline multiple times as well,
try adding another copy of ``middleware`` to ``[pipeline:main]`` and see
what happens. You could also add another section referencing the same
filter factory, but call it something else, and use a different setting
for the prefix.

Conclusion
----------

So, this helped me understand how WSGI works, and how PasteDeploy is
used to serve it. This is the foundation of what Pylons, TurboGears and
Pyramid use, and so it's important to understand to help understand the
mentality behind everything else these frameworks do.

Please feel free to comment! Any feedback is appreciated, this was
primarily a learning exercise for me :)
