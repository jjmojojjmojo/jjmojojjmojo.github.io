=================
JJMOJOJJMOJO Blog
=================

This repository contains the source and HTML for my blog. 

Building
========
To build, go into the ``_build`` directory and run ``make html``. The output will be put into *this* directory (the root of the repo).

Dev Setup
=========
If you wanted to build a local copy of this blog, you'd first need to install pelican. It was developed using python 3.6.

A virtualenv is recommended.

There is are a few external plugins used, that you will have to add yourself. 

One is GPL licensed, and I didn't want to have to GPL my entire blog. I'm also not a lawyer, so that may not be entirely true, but it's better to be safe than sorry.

After cloning this repository, you will then want to clone the pelican-toc repo into _build/plugins/pelican_toc::
    
    $ git clone git@github.com:ingwinlu/pelican_toc.git _build/plugins/pelican-toc
    
Then you will need to install pelican-toc's one dependency, bs4 (Beautiful Soup)::
    
    $ pip install bs4
    
The ``summary`` plugin is part of the Pelican community's `plugin repo <https://github.com/getpelican/pelican-plugins>`__. To install it, check out the repo to a known location (I'm using ``~/Projects/pelican-plugins``), and copy the ``summary.py`` file over to the ``plugins`` directory::
    
    $ cp ~/Projects/pelican-plugins/summary/summary.py ./_build/plugins/
    
    
Notes
=====

Web Server
----------
.. code:: console
    
    $ cd _build
    $ pip install gunicorn webob
    $ gunicorn wsgi:app
    

Watchmedo
---------

.. code:: console
    
    $ cd _build
    $ watchmedo shell-command -c "make DEBUG=1 html" -p "*.rst;*.html;*.js;*.css;*.py" -W -R -D .
    
