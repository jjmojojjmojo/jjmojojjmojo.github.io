Site-wide Conventions Explained
###############################
:date: 2015-01-17 11:41
:author: lionfacelemonface
:category: tutorials
:tags: about, conventions
:slug: conventions

This page contains an overview of conventions used in this website.

.. PELICAN_END_SUMMARY

Source Code Examples
====================

Code examples and command-line interactions are provided with syntax-highlighting and line numbers.

Example 1, clojure code
-----------------------

.. code-block:: clojure
   
   (defn add-it-up
     [&args]
     (apply + args))
     
Example 2, command-line interaction
-----------------------------------

.. code-block:: console
   :linenos: none
   
   $ mkdir -p ~/newdir
   $ touch ~/newdir/newfile
   $ rm -rf ~/newdir
   $ echo $HOME
   /home/jj
   $ sudo su
   # whoami
   root
   
Note how we differentiate doing something as root and as a regular user by changing the prompt from :code:`$` to :code:`#`. 

Explainations
=============
Where applicable, each example is discussed in great detail below it - these explanations are hidden by default so as not to distract from the flow of the article, when such discussion would be a distraction:

.. code-block:: python
   
   def some_function(arg1, arg2, **kwargs):
       print(arg1)
       print(arg2)
       for key in kwargs:
           print("%s: %s" % (key, kwargs[key]))
           

.. explanation::
   
   Overview
        A standard python function that takes a few positional arguments, and any number of keyword arguments, and prints the result.
        
   Line 1
        Standard python function definition. The first two arguments :code:`arg1` and :code:`arg2` are *positional* arguments. They do not have default values, so they must be specified, and in the given order.
        
        The special form :code:`**kwargs` collects any given keyword arguments into a dictionary. 
        
   Line 2 and 3
        Print the values of :code:`arg1` and :code:`arg2` to standard out (STDOUT). Note that this is using the Python 3 form of the print statement. To use this code in recent versions of python 2, you must add :code:`from __future__ import print_function` at the top of your script.
        
   Line 4
        Loop over each key in the :code:`kwargs` dictionary, setting the name of the key to a string variable called :code:`key`. 
        
   Line 5
        With each iteration of the for loop, print the key and it's value in the :code:`kwargs` dictionary. Here we are combining the two values into a single string, separated by a colon, using *string interpolation*. The special :code:`%s` tokens are place holders for the values passed in the tuple that follows the interpolation character (:code:`%`). The :code:`s` is significant, in that python will cast the value to a string before interpolating it.
        
   
   Example
   
   .. code-block:: pycon
      :linenos: none
      
      >>> def some_function(arg1, arg2, **kwargs):
      ...        print(arg1)
      ...        print(arg2)
      ...        for key in kwargs:
      ...            print("%s: %s" % (key, kwargs[key]))
      ...
      >>> some_function("boo")
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
      TypeError: some_function() missing 1 required positional argument: 'arg2'
      >>> some_function("boo", "foo")
      boo
      foo
      >>> some_function("boo", "foo", kw1="value 1", kw4="value 5")
      boo
      foo
      kw4: value 5
      kw1: value 1
      

You can click on the book icon |CLOSED_BOOK_ICON| to show an explanation. Clicking on the open book icon |OPEN_BOOK_ICON| will close it.

.. |CLOSED_BOOK_ICON| image:: {static}/images/book.svg
   :align: middle

.. |OPEN_BOOK_ICON| image:: {static}/images/book-open.svg
   :align: middle
