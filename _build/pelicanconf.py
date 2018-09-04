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

CACHE_CONTENT = True
LOAD_CONTENT_CACHE = True
CACHE_PATH = "./cache"

AUTHOR = 'jjmojojjmojo'
SITENAME = 'The Collected Works of jjmojojjmojo'
SITEURL = ''

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["explanation", "pelican_toc", "summary"]

PATH = 'content'

THEME = "themes/simple"

TIMEZONE = 'US/Eastern'

DEFAULT_LANG = 'en'

PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

# Feed generation is usually not desired when developing
# FEED_ALL_ATOM = None
# CATEGORY_FEED_ATOM = None
# TRANSLATION_FEED_ATOM = None
# AUTHOR_FEED_ATOM = None
# AUTHOR_FEED_RSS = None

CATEGORY_FEED_ATOM = 'feeds/category.%s.atom'
FEED_ALL_ATOM = 'feeds/all.atom'
AUTHOR_FEED_ATOM = 'feeds/author.%s.atom'
TAG_FEED_ATOM = 'feeds/tag.%s.atom'


CATEGORY_FEED_RSS = 'feeds/category.%s.rss'
AUTHOR_FEED_RSS = 'feeds/author.%s.rss'
FEED_ALL_RSS = 'feeds/all.rss'
TAG_FEED_RSS = 'feeds/tag.%s.rss'

DISPLAY_PAGES_ON_MENU = False

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

TOC = {
    'TOC_HEADERS': '^h[1-2]',
    'TOC_INCLUDE_TITLE': 'false'
}

TAG_DESCRIPTIONS = {
    'clojure': "Articles relating to the Clojure programming language.",
    'python': "The Python programming language",
    'boot': "The Boot build tool for Clojure",
    'classics': "Revised articles from my old blog",
    'circuitpython': "Adafruit's port of MicroPython for their M0/M4 development boards",
    'hardware': "Electronics projects and articles dealing with physical technology",
    'state': "The concept of 'state' in terms of tracking changes in data over time"    
}

CATEGORY_DESCRIPTIONS = {
    'tutorial': "How-tos, introductions, walk-throughs."
}

STATIC_PATHS = ['images', 'files', 'js', 'videos']

TEMPLATE_PAGES = {'pages.html': 'pages/index.html'}

# DEFAULT_METADATA = {
#     'status': 'hidden'
# }
