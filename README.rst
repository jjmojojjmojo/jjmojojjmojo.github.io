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

This blog was developed using Python 3.6.

If you wish to rebuild the source or work on the content, you will need to install the dependencies in ``requirements.txt``. 

This can be done in a virtual environment (recommended, I use virtualenv), or system-wide.

Here's how you would do things with virtualenv::
    
    $ python -m venv .
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

The webserver provides directory listings (useful for looking at the drafts folder). Since it's a WSGI app, you can run it in any WSGI server. `chaussette <https://chaussette.readthedocs.io/>`__ is included in ``requirements.txt``.

To run the development services::
    
    $ source bin/activate
    $ cd _build
    $ circusd circus.ini
    
The server listens on localhost, port 8000 by default.

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