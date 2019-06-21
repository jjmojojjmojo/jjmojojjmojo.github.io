StringList - Is It A String? Is It A List? Depends On How You Use It!
#####################################################################
:date: 2013-10-23 19:39
:author: jjmojojjmojo
:category: Uncategorized
:tags: code, github, jjmojojjmojo, lis, list, magic methods, python, string
:slug: stringlist-is-it-a-string-is-it-a-list-depends-on-how-you-use-it
:status: draft

At my job, I had an API problem: I had a object property that could
contain one or more strings. I assumed it would be a list, some of my
users felt that ``['value',]`` was harder to write than ``'value'``. I
found myself making the same mistake. So, I solved the problem, then I
took the rough class I wrote and polished it. It's up on my github, at
https://github.com/jjmojojjmojo/stringlist

So what is it?
==============

It's a class that tries to make a slick API when there can be one, or
many values for a property. The class can be instantiated with either a
single value or many. If you use many, it will act like a list. If you
use a single value (a string), it will act like a string. If it's a
string, and you use the ``.append()`` method, it becomes a list. Bam.

How would I use it?
===================

Like so (see the
`README <https://github.com/jjmojojjmojo/stringlist#stringlist>`__\ for
a more detailed example, and the
`tests <https://github.com/jjmojojjmojo/stringlist/tree/master/tests>`__
for comprehensive usage):

::

    class Thing(object):
        """
        Arbitrary class representing a single thing with one or more roles.
        """

        role = StringList()

        def __init__(self, role=None):
            self.role = role

    # initialize with a single string value        
    obj = Thing('single role')

    # initialize with multiple string values
    obj = Thing(('one', 'two', 'three'))

    # set to a single string value
    obj.roles = 'new role'

    # set to many string values
    obj.roles = 'primary', 'secondary'

    # when it's a string, it works like a string
    obj = Thing('role1')

    # ROLE1
    obj.roles = obj.upper()

    # convert to a list using .append()
    obj.roles.append('role2')

    # now its a list
    obj.roles[1] == 'role2'

Notes
=====

-  The module sports 100% test coverage.
-  There is a buildout in the repo. Just run
   ``python bootstrap.py; bin/buildout`` and then you can run the tests
   with ``bin/nosetests``
-  It was originally developed to avoid ``['h', 'e', 'l', 'l', 'o']``
   mistakes when a single string was used instead of a list.
-  This is the first time I've used
   `descriptors <http://docs.python.org/2/howto/descriptor.html>`__ in
   Python. Very cool.
-  It would not have been possible without `this marvelous post about
   Python's magic
   methods <http://www.rafekettler.com/magicmethods.html>`__ (big thanks
   to Rafe Kettler).
-  Some things were not as straight-forward as they could have been,
   given Python's string implementation. Of special interest is the
   implementation of the
   ```__delitem__`` <https://github.com/jjmojojjmojo/stringlist/blob/master/stringlist.py#L64>`__
   and
   ```__iter__`` <https://github.com/jjmojojjmojo/stringlist/blob/master/stringlist.py#L70>`__
   methods. In both cases, the base ``str`` class doesn't have either
   method, so instead of doing the sane thing and proxying the call, I
   had to fall back to re-doing the operation in the method.
