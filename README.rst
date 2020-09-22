=================
JJMOJOJJMOJO Blog
=================

This repository contains the source and HTML for my blog. It is written mostly in ReStructuredText, and converted to HTML using Pelican.

The HTML output is located in *this* directory. The source code and build tools are located in ``_build``.

Editing Content
===============
All content has it's status set to :code:`draft` by default. Draft pages can be linked, and are accessible via the :code:`drafts` folder. This folder does not have an index page on it by default, so the draft content is not "live".

In order for content to show up, you must add the :code:`:status: published` metadata tag to the content.

Special Features
================

Notice
------
There is a special template named :code:`notice.html`, that is used by :code:`base.html` to display a notice after the banner on each page.

The notice will be shown/hidden depending on the value of :code:`SHOW_NOTICE` in :code:`pelicanconf.py`.

Table Of Contents
-----------------
This blog uses the `pelican-toc <https://github.com/ingwinlu/pelican-toc>`__ plugin. You can turn off the table of contents on a given page or article by setting the metadata :code:`toc_run` to :code:`False`.

Check-out Notes
===============
After the initial clone, you will have to run the following commands to get the sub-modules::
	
	$ git submodule init
	$ git submodule update

Development Setup
=================

This blog was developed using Python 3.6+ (currently 3.8).

If you wish to rebuild the source or work on the content, you will need to install the dependencies in ``requirements.txt``. 

This can be done in a virtual environment, or system-wide.

Basic setup::
    
    $ python -m venv .
    $ source bin/activate
    $ pip install -r requirements.txt
    
Third-Party Plugins
===================
This site uses a couple of third-party pelican plugins. They are installed via git submodules. This was done to keep the code fresh, but also to avoid any problems with viral licensing (pelican-toc is GPL licensed).

Building
========
Once you've activated the virtual environment, enter the ``_build`` diretory, run ``pelican`` with the given CLI parameters blow. It's a good idea to turn debugging on most of the time. The process looks like this::
    
    $ source bin/activate
    $ cd _build
    $ pelican -s pelicanconf.py --fatal errors -D
    
This will put the output in the staging area, ``output``. This folder is in ``.gitignore``, and should not be added to the git repository.

Publishing
==========
Once the content looks good, you need to do two things. First, re-generate the output but point the ``pelican`` tool to the parent directory::
    
    $ cd _build
    $ pelican -s pelicanconf.py --fatal errors -D -o ../
    
Next, make sure you run the `Post-Processing Script`_::
    
    $ python responsive_postprocess.py
    
It's a good idea to run the preview web server and make sure everything looks OK before continuing::
    
    $ chaussette --port 8080 --backend tornado wsgi:preview
    
Take a look at http://127.0.0.1:8080

To make the changes live, ``git commit``, then ``git push``. Be sure to use helpful commit log messages.

Web Server
==========
To view the current state of the generated HTML you will need to run a web server.

Two WSGI applications are provided. One (``dev``) serves the files in ``output``, the other (``preview``) serves the "live" content in the main directory. 

`chaussette <https://chaussette.readthedocs.io/en/latest/>`__ is provided by the ``requirements.txt``. Any WSGI webserver will work. Here's how to run the dev server::
    
    $ chaussette --port 8000 --backend tornado wsgi:dev
    
And the preview server::
    
    $ chaussette --port 8080 --backend tornado wsgi:preview
    
Note that both services are run by the `Development Services`_ below.

Development Services
====================
Pelican comes with a development server that will serve the content and automatically regenerate it when files are changed. 

I had some problems with it, so I use a combination of a WSGI app I built, based on `webob.FileApp <https://docs.pylonsproject.org/projects/webob/en/stable/api/static.html>`__, and watchmedo (from the `watchdog <https://github.com/gorakhargosh/watchdog>`__ library) to accomplish the same thing.

Watchmedo runs the build command mentioned above every time a file changes. This includes source files, and changes to the theme and most static files.

The webserver provides directory listings (useful for looking at the drafts folder, since it's not directly served by normal web servers (like github pages)).

To run the development services::
    
    $ source bin/activate
    $ cd _build
    $ circusd circus.ini
    
As mentioned above, two services are started. On port ``8000``, the content currently in development (located in ``output``) is served.

On port ``8080``, the content that will be published (located in the root of this repository) is served.

Post-Processing Script
======================
I've added a script that does some post-processing, chiefly to make the site more responsive on different devices. 

Currently, it does the following:

* Collect all full-size images, converts them to JPEG
* Creates multiple resized copies of each image.
* Alters the HTML of all image tags to make them responsive (adds ``srcset`` and ``sizes``), pointing to the resized copies.
* Wraps all source code listings in an extra div so overflow on narrower devices can scroll.

The main script is ``responsive_postprocess.py``. It requires the Wand ImageMagick library (and ImageMagick to be installed), lxml, and piexif.

After generating the HTML, run ``responsive_postprocess.py`` from the ``_build`` directory::
    
    $ source bin/activate
    $ cd _build
    $ python responsive_postprocess.py
    
Note that every time the build runs, the HTML files will need to be reprocessed.