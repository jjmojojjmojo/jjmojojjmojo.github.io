#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from num2words import num2words

def my_plural(amount, single, plural):
    """
    Filter to pluralize a grouping word, like so:
    
        We have {{ count|pluralize:article,articles }}.
       
    Produces:
        
        We have one article.
        
        We have ten articles.
        
    inspired by: https://stackoverflow.com/a/11715582
    """
    
    amount = int(amount)
    
    if amount == 1 or amount == 0 or amount == -1:
        suffix = single
    else:
        suffix = plural
        
    amount = num2words(amount)
        
    return f"{amount} {suffix}"

JINJA_FILTERS = {
    'pluralize': my_plural
}

AUTHOR = 'jjmojojjmojo'
SITENAME = 'The Collected Works of Jjmojojjmojo'
SITEURL = ''

PLUGIN_PATHS = ["plugins", "/srv/pelican/plugins"]
PLUGINS = ["explanation", "pelican_toc"]

PATH = 'content'

THEME = "themes/simple"

TIMEZONE = 'US/Eastern'

DEFAULT_LANG = 'en'

PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DISPLAY_PAGES_ON_MENU = False

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

TOC = {
    'TOC_HEADERS': '^h[1-2]',
    'TOC_INCLUDE_TITLE': 'false'
}

TAG_DESCRIPTIONS = {
    'clojure': "Articles relating to the Clojure programming language."
}

CATEGORY_DESCRIPTIONS = {
    'tutorials': "How-tos, introductions, walk-throughs."
}

STATIC_PATHS = ['images', 'files', 'js']