=================
JJMOJOJJMOJO Blog
=================

This repository contains the source and HTML for my blog. It is written mostly in ReStructuredText, and converted to HTML using Pelican.

The HTML output is located in *this* directory. The source code and build tools are located in ``_build``.


Check-out Notes
===============
After the initial clone, you will have to run the following commands to get the sub-modules::
	
	$ git submodule init
	$ git submodule update

Development Setup
=================

This blog was developed using Python 3.6.

If you wish to rebuild the source or work on the content, you will need to install the dependencies in ``requirements.txt``. 

This can be done in a virtual environment (recommended, I use virtualenv), or system-wide.

Here's how you would do things with virtualenv::
    
    $ virutalenv .
    $ source bin/activate
    $ pip install -r requirements.txt
    
Third-Party Plugins
===================
This site uses a couple of third-party pelican plugins. They are installed via git submodules. This was done to keep the code fresh, but also to avoid any problems with viral licensing (pelican-toc is GPL licensed).


Building
========
The HTML is built using make. Once you've activated the virtual environment, enter the ``_build`` diretory, run ``make html``. It's a good idea to turn debugging on most of the time. The process looks like this::
    
    $ source bin/activate
    $ cd _build
    $ make DEBUG=1 html
    
Development Services
====================
Pelican comes with a development server that will serve the content and automatically regenerate it when files are changed. 

I had some problems with it, so I use a combination of a WSGI app I built, based on webob.FileApp, and watchmedo to accomplish the same thing.

The webserver provides directory listings (useful for looking at the drafts folder). Since it's a WSGI app, you can run it in any WSGI server. Gunicorn is included in ``requirements.txt``.

To run the webserver::
    
    $ source bin/activate
    $ cd _build
    $ gunicorn wsgi:app
    
The server listens on localhost, port 8000 by default.

To monitor the files with watchmedo::
    
    $ source bin/activate
    $ cd _build
    $ watchmedo shell-command -c "make DEBUG=1 html" -p "*.rst;*.html;*.js;*.css;*.py" -W -R -D .
    
    
.. note::
    
    The command-line options for watchmedo forget multiple events. So if you save a file while the site is being built, that event will be ignored.
    


Post-Processing Script
======================

.. warning::
    
    This script is **experimental**.
    
I've added a script that does some post-processing, chiefly to make the site more responsive on different devices. 

Currently, it does the following:

* Collect all full-size images, converts them to JPEG
* Cleans the exif data, adds copyright notice
* Creates multiple resized copies of each image.
* Alters the HTML of all image tags to make them responsive (adds ``srcset`` and ``sizes``), pointing to the resized copies.
* Wraps all source code listings in an extra div so overflow on narrower devices can scroll.

The main script is ``responsive_postprocess.py``. It requires the Wand ImageMagick library (and ImageMagick to be installed), lxml, and piexif.

After generating the HTML, run ``responsive_postprocess.py`` from the ``_build`` directory::
    
    $ source bin/activate
    $ cd _build
    $ python responsive_postprocess.py
    
Note that every time the build runs, the HTML files will need to be reprocessed.