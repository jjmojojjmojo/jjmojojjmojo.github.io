=================
JJMOJOJJMOJO Blog
=================

This repository contains the source and HTML for my blog. 

Building
========
All sources, pelican plugins, and such are in the _build directory.

To build, go into that directory and run make html. The output will be put into this directory (the root of the repo).

Dev Setup
=========
If you wanted to build a local copy of this blog, you'd first need to install pellican. It was developed using python 3.6.

A virtualenv is reccomended.

There is one external plugin used, that you will have to add yourself, since it's GPL licensed, and I didn't want to have to GPL my entire blog. I'm also not a lawyer, so that may not be entirely true, but it's better to be safe than sorry. 

After cloning this repository, you will then want to clone the pelican-toc repo into _build/plugins/pelican_toc::
    
    $ git clone git@github.com:ingwinlu/pelican_toc.git _build/plugins/pelican-toc
    
Then you will need to install pelican-toc's one dependency, bs4 (Beautiful Soup)::
    
    $ pip install bs4
    
