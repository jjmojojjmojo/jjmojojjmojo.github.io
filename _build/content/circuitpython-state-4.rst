State And Events In CircuitPython: Part 4: A Generic State Dispatcher
#####################################################################
:date: 2018-06-11 15:07
:author: lionfacelemonface
:category: tutorial
:tags: tutorial; circuitpython; hardware; state;
:slug: circuitpython-state-part-4
:status: draft

.. include:: ../emojis.rst

This is the **fourth** part of a multi-part series exploring the concept of state, what it can do for you (like non-blocking button debounce) and how to track it in CircuitPython.

In this part, we'll take the object-oriented bull by the horns and implement a **fully encapsulated event dispatcher**. 

Building on what we've learned previously, we'll create a lightweight, reusable class that can detect button events and call code we associate with a given event at runtime. 

.. tip::
    
    Since we're pretty deep into the series now, I've set up a `landing page <{filename}/pages/circuitpython-state.rst>`__ |sparkleheart|. Check it out if you'd like to catch up or review previous installments.
    


.. PELICAN_END_SUMMARY

A Brief Review
==============
Let's recap and summarize what we've learned so far.

What is state?
--------------

| **State** is a collection of values, that we call **attributes**, that represent the status or phase of our project at a given time. 

Remember the analogies we used:

* Matter has state (but in physics they are usually called "phases"). Water has different properties (attributes) when it's liquid, when it's steam, or when it's ice.
  
  Matter has multiple attributes when it's in a certain state, and new attributes can emerge. 
  
  For example, when water is "steam", not only is its temperature attribute at 100° C, can freely fill an open space. It becomes less dense. When water is "ice", it's temperature attribute is below 0° C, but it also forms crystals, and becomes more dense. 
  
  Steam and ice can both be used to do physical work, but they act in very different manners and have very different applications.
  
* Simple state can be thought of like a simple scorecard from a gymnastics match. One value, stored once for a given event and participant. 
  
* Other kinds of state, especially global state, can be thought of like a scoreboard at a stadium. 
      
  The values change over time, and we just look at the scoreboard to see what the current state is.

Remember how we mapped those analogies to our electronics projects:

* We track the state of physical things, like buttons and LEDs
* We also track values that we need to affect physical things, like the random color we generated for the RGB LED.
* We used a global state **object**, defined in the ``State`` class, to work with those values.

Recall the **three phases of working with state**:

.. image:: {filename}/images/nonblocking-state-flowchart.png
   :width: 60%
   :align: center

* We start by establishing **default** state.
* Then, we **assess** real life.
* Next, we **reconsider** the state values.
* Finally, we **reconcile** the state values with real life again.
* `Lather, rinse, and repeat <https://en.wikipedia.org/wiki/Lather,_rinse,_repeat>`__ (or *assess*, *reconsider*, *reconcile* and *loop*) |grin| .
   
How Do We Model State
---------------------

| Since state is a **collection of data**, we can use any Python data type, or combination of types to model and track it.

We explored using simple variables, dictionaries, lists of dictionaries, and finally **classes**.

Remember that classes give us a few interesting features that make them especially attractive:

* Classes are like **blueprints** for our data. We can define what the structure looks like once, and use that structure over and over, when we make **instances**.
* Classes can have **methods** that let us give our data it's own unique functionality.
* Classes are **encapsulated**, so we can keep all of our state processing code with our state data, and out of the way of our other code.

.. tip::
    
    In this installment of the series, we'll dig into some of the more advanced things you can do with classes in Python. When we start utilizing these aspects, classes really start to shine. |unicorn|
    
We Can Track Changes In State (Events)
--------------------------------------
boo

Event Dispatch In A Nutshell
============================


A Generic State Dispatcher
==========================
Having established a way of tracking state over time, and the concept of *events*, we can generalize the button logic into a *dispatcher* - code that detects the events and then dispatches to pre-defined *handlers*. In other words, it detects an event, and runs code for us.

We can take the ``State`` class that we've been working on and extend it to detect the three most common button events: *press*, *release*, and *hold*. 

We can then take advantage of a key feature of Python to make the handlers really flexible. In Python, functions are *first class objects*. This means that they can be assigned to variables, and passed around just like an integer or list.

Using this feature, we can configure our state class when we instantiate it, by passing function names to the constructor. We can store the functions as instance attributes and execute them later when we need to dispatch an event. 

The first step is to specify the events we want to detect in terms of what conditions must occur for them to be triggered. 

We're going to focus on button events here, but remember events can be whatever we want.

Event 1: Press
--------------
Recall from the last section that a *press* event happens when the button *wasn't* pressed, and now it is. 

But lets be very specific so we can make sure we've covered all of the conditions in our code. That means we also have to take into account button debounce.

So, for a *press* event to occur: 

* The button pin has gone from "LOW" to "HIGH" (``False`` to ``True``).
* The button pin has read "HIGH" (``True``) for more than 0.2 seconds.

Let's review the logic for this event:

.. code-block:: python
    
    # WARING: pseudo(ish) code
    
    button = # digital pin object
    
    # is the button pressed or not
    state = False
    
    if state is False and button.value is True:
        if debounce time has passed:
            # button has been pressed
            state = True
        
        
Event 2: Release
----------------
A *release* event occurs when the user stops pressing the button. This usually happens immediately after a *press* event, but this is not always the case - there may be a delay if the button was held down.

Specifically, a release event has occurred when:

* The button pin has gone from "HIGH" to "LOW" (``True`` to ``False``).

Debouncing can sometimes be required but for the most part, considering the event triggered at the first notice of the pin reading "LOW" will be sufficient.

Here's what the logic looks like:

Let's review the logic for this event:

.. code-block:: python
    
    # WARING: pseudo(ish) code
    
    button = # digital pin object
    
    # is the button pressed or not
    state = False
    
    if state is True and button.value is False:
        # button has been released
        state = False

Event 3: Hold
-------------
This is a new event we haven't covered before. *Hold* can be looked at in two different ways. The first way is to consider a hold event as a one-time occurance, where a hold event has occurred after a *release* event that follows a *press* event and a set period of time has passed between the two.

The second way, is to think of a *hold* an event that happens over and over every so often while a button is being held down.

It's a bit easier to explain the difference between the two in code.

The first way would look something like this:

.. code-block:: python
    
    # warning: pseudo(ish) code!
    
    import time
    
    button = # properly configured digital pin
    
    # is the button pressed or not
    state = False
    
    # time that we started holding
    held_since = time.monotonic()
    
    # remember the following is being run with a delay for debounce
    every debounce: 
        if state is False and button.value is True:
            # button has been pressed
            state = True
            held_since = time.monotonic()
            
        if state is True and button.value is False:
            # button has been released
            state = False
            
            if time.monotonic() - held_since > some_threshold:
                # button has been held
        
Contrast that with treating a hold event as a recurring event:

.. code-block:: python
    
    # warning: pseudo(ish) code!
    
    import time
    
    button = # properly configured digital pin
    
    # is the button pressed or not
    state = False
    
    # is the button being held
    holding = False
    
    # checkin to detect a hold
    hold_check = time.monotonic()
    
    # remember the following is being run with a delay for debounce
    every debounce: 
        if state is False and button.value is True:
            # button has been pressed
            state = True
            hold_check = time.monotonic()
            
        if state is True and time.monotonic() - hold_check > some_hold_threshold:
            holding = True
            
        if holding is True:
            # dispatch the hold event
            # this will happen every time we debounce
            
        if state is True and button.value is False:
            # button has been released
            state = False
            holding = False
            
Both approaches are valid, and which one to use will depend on your application.

The first approach works well when we don't need to do anything *during* the time a button is being held down. An example of a use case for this would be holding a button for, say 2 seconds to change into a different *mode*, or holding the button in for 5 seconds to power the project off.

The second approach allows us to take action while the button is being pressed and held. Examples of use cases for this include holding a button to advance a clock to set the time and emulating the scroll wheel on a mouse. It has the advantage over the first approach, besides continuing to act, of being able to take the number of times the hold event has fired into account. This allows us to do things like accelerate the rate of increase on the clock or move the scroll wheel faster the longer the button is held. 

For this article, we'll implement the second approach, since the project that inspired this article uses it.

So, to quantify our event, a *hold* occurs when:

* The button pin has gone from "LOW" to "HIGH" (``False`` to ``True``), or a *press* event has previously occurred.
* The button pin has read "HIGH" (``True``) for more than 0.4 seconds. 
* The event continues to occur every 0.4 seconds until a *release* event occurs.

The Code
========
As mentioned earlier, Python allows functions to be passed around like any other value. We can leverage that fact to make a dispatcher that is very flexible.

In the code below, we pass a series of predefined functions to our dispatcher constructor that it will use to determine what the current value of the button is, and call when each type of event is detected.

While we develop the generic dispatcher, we'll just print the events to the console to keep things simple. 

We're going to focus on just handling button-related events. We'll rename the class from ``State`` to ``ButtonDispatch``. We're only going to deal with one button at a time. We'll also remove the state attributes and methods that aren't button-related (``rgb``, ``led``, ``random_color()``, etc). This way we can use a separate ``ButtonDispatch`` object for every button we have, instead of adding a lot of complexity to a single class to handle many different buttons.

We've also moved the logic from the ``update()`` method to ``__call__()`` - this is a special ("magic") method you can define to make an object *callable*, like a function. 

.. code-block:: python
    
    import time
    from setup import led, rgb, check
    
    import random
    
    class ButtonDispatch:
        _debounce = 0.2
        _hold_threshold = 0.4
        
        def __init__(self, check, press=None, release=None, hold=None):
            # state
            self.checkin = time.monotonic()
            self.holding = False
            self.hold_count = 0
            self.state = False
            
            # get the state of the button
            self.get_value = check
            
            # event handlers
            self.onpress = press
            self.onrelease = release
            self.onhold = hold
            
        def release(self):
            self.state = False
            
            if self.onrelease is not None:
                self.onrelease()
            
            self.hold_count = 0
            self.holding = False
            self.checkin = time.monotonic()
    
        def check(self):
            return self.get_value()
    
        def hold(self):
            self.hold_count += 1
    
            if self.onhold is not None:
                self.onhold(self.hold_count)
    
            self.checkin = time.monotonic()
    
        def press(self):
            self.state = True
                
            if self.onpress is not None:
                self.onpress()
            
            self.checkin = time.monotonic()
    
        def __call__(self):
            current = time.monotonic()
    
            # button has been held
            if self.state and current - self.checkin >= self._hold_threshold:
                self.holding = True
                self.hold()
    
            # button has been pressed
            if not self.state and self.check():
                if current - self.checkin >= self._debounce:
                    self.press()
    
            # button has been released
            if self.state and not self.check():
                self.release()
    
        def __repr__(self):
            return  "<Check: {}, State: {} Checkin: {}>".format(self.check(), self.state, self.checkin)
    
    def value():
        reutrn check("A")
            
    def press():
        print("Button A pressed!")
    
    def release():
        print("Button A released!")
    
    def hold(count):
        print("Button A held for ", count)
    
    dispatch = ButtonDispatch(value, press, release, hold)
    
    while True:
        dispatch()
    
.. explanation::
    
    There's a lot of new code here, so lets take this example line by line, from the top.
    
    **Lines 1-4** are the imports we need from external libraries, including ``time`` to track the passing of time, the ``setup`` module to abstract away differences between our boards, and ``random`` to generate random colors.
    
    **Lines 6-72** define our ``ButtonDispatch`` class.
    
    **Lines 7 and 8** are global configuration variables, defined as *class attributes*, and intended for "private" use. The ``_debounce`` attribute is used to set how frequently the state object checks the button (avoiding button bouncing). 
    
    The ``_hold_threshold`` value is new, and is used to determine the difference between simply pressing the button, and holding it down. We need this because we are handling both the *press* and *hold* events in our dispatcher.
    
    On **line 10**, the constructor takes some arguments. 
    
    * ``self`` is automatically passed to any instance method. It references the instance that this method is being called on. 
    * ``check``, is a function that will be called to read the button pin. It's expected to return ``True`` if the button is pressed, and ``False`` if it's not. ``check`` is a required argument.
    * ``press`` is a function that will be called whenever a *press* event is detected. It is expected to take no attributes. Its return value isn't used by the ``ButtonDispatch`` class. This is a optional argument, and will default to ``None``.
    * ``release`` is a function that will be called whenever a *release* event is detected. It is also expected to take no attributes, and its return value isn't used by the dispatcher. It's also optional, and defaults to ``None``.
    * Finally, ``hold`` is a function that will be called multiple times (every ``_hold_threshold`` seconds) when the button is being held down. It differs a bit from the other two functions in that it is required to take a single argument, which will be the number of times the *hold* event was detected in a row. It is also an optional argument, defaulting to ``None``.
    
    These functions would typically be considered *event handlers* in most event dispatch contexts. 
    
    **Lines 12-15** establish the default state attributes the dispatcher uses to do its work. ``checkin`` is the time keeping attribute. ``holding`` is used to indicate if the button is currently being held. ``hold_count`` tracks how many times the *hold* event has been detected. Finally ``state`` is the state of the button, the last time it was read.
    
    **Line 18** stashes the ``check`` function passed to the constructor in an instance variable (``get_value``) so it can be used later. This is a really cool feature of Python: you can pass functions around like any other kind of data. This means you can pass them to a constructor and assign them to an instance attribute like we've done here. To call the ``check`` function passed in the constructor, we can call ``self.get_value()``. 
    
    .. tip::
       
       This can be a little confusing, since this looks a lot like an instance method. The way to tell the difference is that an instance method always receives a ``self`` attribute as its first argument.
       
    **Lines 21-23** assign the event handlers to instance attributes in the same way. We've named the instance attributes ``onpress``, ``onrelease`` and ``onhold`` - these names are a call back to event handlers in HTML. They are named such to differentiate them from the instance methods that are called when events are detected.
    
    The ``release``, ``check``, ``hold``, and ``press`` methods defined on **lines 25-52** are proxies for the functions that were passed in the constructor. With the exception of ``check``, they all follow the same pattern. They first update any state attributes required because of the event detection. Then they check if the handler was defined (``is not None``), and if it was, they call it. Finally, they update the ``checkin`` time. 
    
    .. tip::
        
        It may seem a little odd that these functions are so simplistic. But the structure of the class has a specific purpose.
        
        The dispatcher has been constructed this way so that you could build one with the *same* API, that doesn't rely on external functions being passed into the constructor. 
        
        You can instead hard-code what you want to happen in each event. To do different things for different buttons, you can use `class inheritence <https://www.python-course.eu/python3_inheritance.php>`__ to add in the special functionality. 
        
        I find passing functions into the constructor to be much more flexible and straightforward, but the other approach is valid too, so I designed the class to be compatible with it.
        
    On **lines 54-69**, the ``__call__()`` 'magic' method makes instances of ``ButtonDispatch`` *callable* - they can be invoked just like a function (we utilize this on **line 89**). When they are invoked that way, the ``__call__()`` method is called. We use this as a central access point for making the event dispatch work.
    
    ``__call__()`` starts by logging the current time in a variable called ``current`` on **line 55**. We do this to avoid multiple calls to ``time.monotonic()``, so the following logic will be cleaner, and also more consistent (time will pass from line to line of the code as it's running).
    
    **Lines 68-60** detects and handles the *hold* event. Here, *hold* has occurred every time the button state is ``True``, and it's been ``_hold_threshold`` seconds since the last check-in. On **line 59** the ``holding`` attribute is set to ``True``, and then **line 60** calls the ``hold()`` instance method.
    
    **Lines 63-65** detect and handle the *press* event. *Press* happens when the state of the button is ``False`` but the button pin reads ``True`` *and* it's been ``_debounce`` seconds since the last check-in.
    
    The *release* event is detected and handled on **lines 68 and 69**. *Release* happens when the state of the button is ``True``, but the pin reads ``False``. We could debounce here as well, but I haven't seen a need in my projects.
    
    **Lines 71-72** provide a ``__repr__()`` method for easier debugging.
    
    **Lines 74-83** define the functions we will pass to ``ButtonDispatch`` on **line 86**. 
    
    ``value()`` is a simple wrapper for our ``check`` function from the ``setup`` module. 
    
    The rest of the functions are event handlers. They simply print something out to the console to indicate that the event occurred. 
    
    Finally, on **lines 86-89**, the ``ButtonDispatch`` class is instantiated, and our main loop is run. The main loop just calls the ``dispatch`` object on each iteration. It's a lot less complex because we've moved *all* of the logic into the ``ButtonDispatch`` class, and all of the actions that we need to take when the button is pressed into the event handlers. 
    
    

Since the function used to check the physical state of the button is configured by creating a function and passing it to the constructor, we can use the same dispatcher for multiple kinds of inputs besides buttons - touch pads, rotary encoders, etc.

We can opt to skip certain events by passing ``None`` to the constructor for the handlers we don't want to implement.

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/dispatcher-demo-trinket-01.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/dispatcher-demo-trinket-01.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

   
.. tip::
   
   This implementation is designed to still do the *accounting* for each event even if no event is set - it may be more efficient to avoid calling the press/hold/release method if one isn't provided.
   
   You may also want to consider removing events, such as *hold*, if you aren't using them in your project.
   

Events Across Multiple Buttons
==============================

When transitioning our ``State`` class to our generic event dispatcher, we lost the ability to track both buttons. 

The utility of using a class for our dispatcher code starts to really shine as we use more buttons - all we need to do is create a ``ButtonDispatch`` instance for each button. 

We'll just need to write a duplicate of ``value()`` that returns the value for the correct button, and duplicate the handlers so we can do something different for each button.

We can put our ``ButtonDispatch`` objects into a list to make them easier to work with.

Here's what the code looks like (the ``ButtonDispatch`` class doesn't change):

.. code-block:: python
    
    # -- snip --
    
    def value_a():
        return check("A")
    
    def press_a():
        print("Button A pressed!")
    
    def release_a():
        print("Button A released!")
    
    def hold_a(count):
        print("Button A held for ", count)
    
    def value_b():
        return check("B")
    
    def press_b():
        print("Button B pressed!")
    
    def release_b():
        print("Button B released!")
    
    def hold_b(count):
        print("Button B held for ", count)
    
    buttons = [
        ButtonDispatch(value_a, press_a, release_a, hold_a),
        ButtonDispatch(value_b, press_b, release_b, hold_b),
    ]
    
    while True:
        for dispatch in buttons:
            dispatch()
            
    

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/dispatcher-demo-trinket-02.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/dispatcher-demo-trinket-02.mp4">link to the video</a> instead.</p>
       </video>
   </div>

As you can see, things can get a little complex though when dealing with multiple actions for multiple events. We just have two buttons here, imagine if we had 10! That would be 30 event handlers!

There are a couple of strategies we can take. 

First, it may not even be a real concern. Most of the time, we won't need handlers for every event for every button. Second, the buttons and the functionality they invoke will be separated. 

In practice, most code will look more like this:

.. code-block:: python
    
    # ... snip ...
    
    def value_a():
        return check("A")
        
    def value_b():
        return check("B")
    
    def say_hey():
        print("HEYDIE HEYDIE HEYDIE HEY")
        
    def say_ho():
        print("HIDIE HIDIE HIDIE HO")
    
    buttons = [
        ButtonDispatch(value_a, None, say_hey),
        ButtonDispatch(value_b, None, say_ho)
    ]
    
    while True:
        for dispatch in buttons:
            dispatch()
            

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/dispatcher-demo-trinket-03.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/dispatcher-demo-trinket-03.mp4">link to the video</a> instead.</p>
       </video>
   </div>
            
But in the event that we really need to handle many buttons in an efficient way (imagine building a 101 key keyboard), we can consolidate handlers such that a single function can handle the same event for many buttons. We just need to differentiate between buttons when the handler is dispatched.

Consolidating Handlers
======================

To address that, we can add a *token* to the ``ButtonDispatch`` class that each instance stores, identifying which button caused an event. The token gets passed to the event functions. Since the token indicates which button was pressed, the event function can take different action depending on which button invoked it.

Here's what that looks like:

.. code-block:: python
    
    # save as code.py
    import time
    from setup import led, rgb, check
    
    import random
    
    class ButtonDispatch:
        _debounce = 0.2
        _hold_threshold = 0.4
        
        def __init__(self, token, check, press=None, release=None, hold=None):
            # state
            self.token = token
            self.checkin = time.monotonic()
            self.holding = False
            self.hold_count = 0
            self.state = False
            
            # get the state of the button
            self.get_value = check
            
            # event handlers
            self.onpress = press
            self.onrelease = release
            self.onhold = hold
            
        def release(self):
            self.state = False
            
            if self.onrelease is not None:
                self.onrelease(self.token)
            
            self.hold_count = 0
            self.holding = False
            self.checkin = time.monotonic()
    
        def check(self):
            return self.get_value(self.token)
    
        def hold(self):
            self.hold_count += 1
    
            if self.onhold is not None:
                self.onhold(self.token, self.hold_count)
    
            self.checkin = time.monotonic()
    
        def press(self):
            self.state = True
                
            if self.onpress is not None:
                self.onpress(self.token)
            
            self.checkin = time.monotonic()
    
        def __call__(self):
            current = time.monotonic()
    
            # button has been held
            if self.state and current - self.checkin >= self._hold_threshold:
                self.holding = True
                self.hold()
    
            # button has been pressed
            if not self.state and self.check():
                if current - self.checkin >= self._debounce:
                    self.press()
    
            # button has been released
            if self.state and not self.check():
                self.release()
    
        def __repr__(self):
            return  "<Button {}|Check: {}, State: {} Checkin: {}>".format(self.token, self.check(), self.state, self.checkin)
    
    def value(token):
        return check(token)
            
    def press(token):
        print("Button {} pressed!".format(token))
    
    def release(token):
        print("Button {} released!".format(token))
        
        if token == "A":
            print("HEYDIE HEYDIE HEYDIE HEY")
            
        if token == "B":
            print("HIDIE HIDIE HIDIE HO")
        
    def hold(token, count):
        print("Button {} held for {}".format(token, count))
    
    buttons = [
        ButtonDispatch("A", check, press, release, hold),
        ButtonDispatch("B", check, press, release, hold)
    ]
    
    while True:
        for dispatch in buttons:
            dispatch()
     

.. explanation::
    
    This code hasn't changed much from the last version. Here are the changes that were made to allow the same handlers to be used for multiple buttons:
    
    * The ``ButtonDispatch`` constructor (**Line 11**) now has *two* required arguments, ``token`` and ``check``. ``token`` is used to differentiate between different buttons. We've used a string here, but it really could be anything, as long as the event handler functions understand it. The token is stored as an instance attribute on **line 13**.
    
    * The token (``self.token``) is passed to the event handlers and ``check`` function (**lines 31, 38, 44 and 52**).
    
    * The handlers and check function defined on **lines 76-92** all take ``token`` as their first argument.
    
    * In the case of ``value()`` (**line 76**), the ``token`` is just passed along to the ``check()`` function from our ``setup`` abstraction module.
    
    * The handlers all print out the ``token`` (**lines 80, 83 and 92**).
    
    * The ``release()`` handler actually has some logic in it so that it behaves differently depending on the value of ``token`` (or which button was pressed), additionally printing a different message. 
    
    * Finally, you can see how the ``token`` is passed when the  ``ButtonDispatch`` objects are instantiated on **lines 95 and 96**.
    

Here's a video of this code running, again on my Trinket M0:

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/dispatcher-demo-trinket-04.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/dispatcher-demo-trinket-04.mp4">link to the video</a> instead.</p>
       </video>
   </div>

The primary difference here is just the addition of the ``token`` property, and the added requirement that it is now a parameter of each event handler function.

Now using only three event functions, we can handle events for many, many buttons. Each event will produce a different effect depending on which button triggered it (in this case different messages will be printed to the console).

The token has also been passed to the ``check()`` function, so that has been centralized as well.

This is a common pattern in programming, a form of `message passing <https://en.wikipedia.org/wiki/Message_passing>`__.

You may also have noticed that you can press both buttons *simultaneously*. The events are not actually firing at the same time, however, they are firing one after the other. It just happens so quickly that they appear to be simultaneous.

Muti-Button Events
==================
This is a great accomplishment, and will work well for even quite complex projects. However, we have painted ourselves into a corner of sorts. We can fire two different events when buttons are pressed at the same time, but we can't see the state of one button from the event of the others. This becomes problematic if we want one button to affect the actions of another. 

You may have run into an application of this problem: holding down one button makes the meaning of another button change. Here's an example from an old digital alarm clock:

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/blink-controller-alarm-clock-example.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/blink-controller-alarm-clock-example.mp4">link to the video</a> instead.</p>
       </video>
   </div>

So we have the "mode" of one button changing because another button was held down.

This is again something that can (and should) be handled in different ways, depending on the situation. 

The simplest way to deal with this is to use the ``state`` and ``holding`` properties of each ``ButtonDispatch`` object. If the first button's ``state`` is ``True``, and the second button's ``holding`` property is also ``True``, then we have a alarm clock-setting style event occurring.

To make it work, we just have to track our own checkin time to further debounce the simultaneous press events:

.. code-block:: python
    
    # ... snip ...
    
    ﻿checkin = time.monotonic()    
    while True:
        current = time.monotonic()
        
        for dispatch in buttons:
            dispatch()
            
        if buttons[0].state and buttons[1].state:
            if current - checkin >= 0.2:
                print("Both buttons pressed!")
                checkin = time.monotonic()
                buttons[0].state = False
                buttons[1].state = False
                
.. explanation::
    
    Here, we're tracking some external state values in global variables so we don't have to modify the ``ButtonDispatch`` class to get what we want.
    
    **Line 10** looks at the state of both buttons - if they're both pressed (the ``state`` attribute is ``True``), then both buttons must have been pressed and debounced. 
    
    We have to do a further debounce (**line 11**) because they may have not been pressed together - if they are pressed slightly out of sync, we can get a false reading as one button is being released, and the other is being pressed.
    
    On **lines 14 and 15** we set the state of both buttons to ``False``. This ensures that the press or hold events won't be fired again now that we've handled them on our buttons' behalf.
    

This will cover most use cases. As mentioned before, complex button pressing scenarios are not common - they are necessary sometimes when there are a limited number of buttons, or the greater functionality of the project is rather complex (playing chords on a musical instrument for example).

.. note::
   
   This code prevents the *release* events from firing, and doesn't cover the *both buttons released* event. Handling this would require some refactoring and additional logic. It was left out of this example for the sake of simplicity - the technique covered next is the best way to handle anything more complex than a simple *both buttons pressed* sort of event as illustrated above.
   

When this extra complexity is necessary, it's best to separate the state of each button into a central state object, like we did earlier. We can either access that global object directly in our handlers, or pass it as an additional argument to them.

This will allow for more complex behaviors, like holding one button and pressing the other.

A Quick Note About Getters and Setters
======================================

The code below introduces the concept from object-oriented programming called *getters* and *setters*. 

The basic idea is that, instead of accessing a property of an object directly, you set up a method to retrieve the value (*get* it), and to store the value (*set* it). 

In Python, its usually not necessary, unless you want to provide a convenient way of getting/setting a value that may be a little complex otherwise. 

Here's a simple example, that illustrates the syntax used to do this in Python:

.. code-block:: python
    
    # save as state.py
    class State:
        def __init__(self):
            # private attribute used to store the actual
            # integer value
            self._day_of_week = 0
            
        # getter - returns a string based on the integer stored
        @property
        def day_of_week(self):
            if self._day_of_week == 0:
                return "Sunday"
            
            if self._day_of_week == 1:
                return "Monday"
                
            if self._day_of_week == 2:
                return "Tuesday"
                
            if self._day_of_week == 3:
                return "Wednesday"
                
            if self._day_of_week == 4:
                return "Thursday"
                
            if self._day_of_week == 5:
                return "Friday"
            
            if self._day_of_week == 6:
                return "Saturday"
                
            return "Unknown"
                
        # setter - takes a string and stores an integer
        @day_of_week.setter
        def day_of_week(self, value):
            if value.lower() == "sunday":
                self._day_of_week = 0
            elif value.lower() == "monday":
                self._day_of_week = 1
            elif value.lower() == "tuesday":
                self._day_of_week = 2
            elif value.lower() == "wedsnday":
                self._day_of_week = 3
            elif value.lower() == "thursday":
                self._day_of_week = 4
            elif value.lower() == "friday":
                self._day_of_week = 5
            elif value.lower() == "saturday":
                self._day_of_week = 6
            else:
                raise ValueError("No idea what day '{}' is".format(value))
                
.. explanation::
    
    Most of the basics of making a class have been well explained in other examples. However, this example introduces some new concepts:
    
    *Line 6* establishes a "private" instance attribute called ``_day_of_week`` - this is the attribute where the "real" value representing the day of the week is stored, as an *integer*. The name is intentionally the same as the getter/setter code below it, so you know that those methods are proxies for this value.
    
    On *line 9*, we use the ``@property`` decorator to transform the method defined below it (``day_of_week()``) into a special kind of object. From the instances' perspective, ``day_of_week`` will be an instance attribute just like any other - but when you access it (``self.day_of_week``, or ``state.day_of_week``), it transparently invokes the ``day_of_week()`` *method*. 
    
    ``@property`` allows us to create dynamic instance attributes. It's especially useful in situations like this where we want to present an API that looks like a "regular" instance, but does more behind the scenes.
    
    After the definition of ``day_of_week()`` on **line 32**, its passed to the ``@property`` decorator and obtains new attributes. We use one of them ``setter`` as a second decorator to indicate our next method, also called ``day_of_week()``, will be called when you assign a value to the ``day_of_week`` attribute. 
    
    It may seem a little weird that we're naming the two methods the same. First, we want to make it clear to anyone reading the code that these two methods are related, and that together they define the ``day_of_week`` attribute. We can give them the same name because technically, we're not defining two instance methods in the ``State`` class. In reality, we're defining a ``@property`` object, assigning it to the ``day_of_week`` name, and then creating two *functions* that it will use to handle setting and getting of tat ``day_of_week`` attribute for the instance. 
    
    The final thing that is worth pointing out is the error handling on **lines 32 and 52**. 
    
    The ``day_of_week()`` getter looks at the value of ``self._day_of_week``, and returns a string corresponding to the English weekday of the stored value. If the value doesn't correspond to any expected numbers, the word ``Unknown`` is returned instead, on **line 32**. 
    
    The ``day_of_week()`` setter takes the ``value`` argument and based on its content, sets the ``self._day_of_week`` attribute to a corresponding number. 
    
    If the content of ``value`` doesn't match any of the known English days of the week, the setter throws a ``ValueError`` (**line 52**). When this happens the user will get an exception, and will see the message ``No idea what day 'XXX' is`` (replacing ``XXX`` with whatever the user passed in). 
    
    This is an advantage of using getters and setters in Python - you can do data *marshalling* where you translate a value from one kind to another (like the getter does), set *sane defaults* (like returning ``Unknown`` when the day of the week is wrong in the getter) and you can do *validation* so that the user can't store bad data (like throwing the exception in the setter). 
    

Here's how you'd work with it in the console:

.. code-block:: pycon
    
    >>> from state import State
    >>> s = State()
    >>> s.day_of_week
    'Sunday'
    >>> s.day_of_week = "Friday"
    >>> s._day_of_week
    5
    >>> s.day_of_week
    'Friday'
    >>> s.day_of_week = "Munundununceday"
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "state.py", line 47, in day_of_week
        raise ValueError("No idea what day '{}' is".format(value))
    ValueError: No idea what day 'Munundununceday' is
    
    
So internally, we're storing the day of the week as an integer, but when you access ``day_of_week``, it returns a string. If we want to set the day of the week, we provide a string and it is translated into a integer for internal storage. We are able to add some error handling in the setter, that we wouldn't be able to do easily if we weren't using one.

Dispatch Using A Global State Object
====================================
Now that we understand how getters and setters work, we can use them to provide a simple way of accessing the external global state:

.. code-block:: python
    
    # save as code.py
    import time
    from setup import led, rgb, check
    
    class ButtonDispatch:
        _debounce = 0.2
        _hold_threshold = 0.4
        
        def __init__(self, token, check, state, press=None, release=None, hold=None):
            # global state object
            self._state = state
            
            # state
            self.token = token
            self.checkin = time.monotonic()
            self.holding = False
            self.hold_count = 0
            self.state = False
            
            # get the state of the button
            self.get_value = check
            
            # event handlers
            self.onpress = press
            self.onrelease = release
            self.onhold = hold
        
        @property
        def holding(self):
            return self._state["{}-holding".format(self.token)]
        
        @holding.setter
        def holding(self, value):
            self._state["{}-holding".format(self.token)] = value
        
        @property
        def state(self):
            return self._state[self.token]
        
        @state.setter
        def state(self, value):
            self._state[self.token] = value
        
        def release(self):
            self.state = False
            
            if self.onrelease is not None:
                self.onrelease(self.token, self._state)
            
            self.hold_count = 0
            self.holding = False
            self.checkin = time.monotonic()
    
        def check(self):
            return self.get_value(self.token, self._state)
    
        def hold(self):
            self.hold_count += 1
    
            if self.onhold is not None:
                self.onhold(self.token, self.hold_count, self._state)
    
            self.checkin = time.monotonic()
    
        def press(self):
            self.state = True
                
            if self.onpress is not None:
                self.onpress(self.token, self._state)
            
            self.checkin = time.monotonic()
    
        def __call__(self):
            current = time.monotonic()
    
            # button has been held
            if self.state and current - self.checkin >= self._hold_threshold:
                self.holding = True
                self.hold()
    
            # button has been pressed
            if not self.state and self.check():
                if current - self.checkin >= self._debounce:
                    self.press()
    
            # button has been released
            if self.state and not self.check():
                self.release()
    
        def __repr__(self):
            return  "<Button {}|Check: {}, State: {} Checkin: {}>".format(self.token, self.check(), self.state, self.checkin)
    
    def value(token, state):
        return check(token)
            
    def hold(token, count, state):
        print("Button {} held for {}".format(token, count))
    
    def multi_press(token, state):
        if token != "A" and state['A-holding']:
            print("A is holding while {} was pressed!".format(token))
    
        if state['A'] and state['B']:
            state["both"] = True
            print("Both buttons are being pressed")
    
    def multi_release(token, state):
        if not state["both"] and token != "A" and state['A-holding']:
            print("A is holding and {} has been released".format(token))
    
        if not state['A'] and not state['B'] and state["both"]:
            print("Both buttons released")
            state["both"] = False
    
    state = {
        "A": False,
        "B": False,
        "A-holding": False,
        "B-holding": False,
        "both": False
    }
    
    buttons = [
        ButtonDispatch("A", value, state, multi_press, multi_release, hold),
        ButtonDispatch("B", value, state, multi_press, multi_release, hold)
    ]
    
    while True:	
        for dispatch in buttons:
            dispatch()
    

.. explanation::
    
    On **line 9**, we are now requiring an argument called ``state``. This is assumed to be a dictionary. It can contain anything you'd like, and the ``ButtonDispatch`` class with add in its own keys for the state and holding status of its button. The key holding the state of the button will simply be named whatever was passed for ``token``. The holding status will be stored in a string, combining the ``token`` with ``-holding``.
    
    The ``state`` argument is stored in an instance variable called ``_state`` on **line 11**.
    
    **Lines 28-42** contain the most drastic changes of this iteration. Here we use the ``@property`` decorator so that any manipulation of ``self.holding``, or ``self.state`` actually alters the global state object passed to the constructor.
    
    All of the dispatch methods (``release()``, ``check()``, ``hold()`` and ``press()``, **lines 54-71**) now pass two arguments to the event handlers (or three in the case of ``hold()``) - the token and the global state object (``hold()`` also passes the number of times the event has occurred). 
    
    Notice how none of the other code had to change. The interface, all of the attribute and method names, have remained the same and function exactly like they did before.
    
    The event handlers on **lines 93-113** now take the global state object. The new ``multi_press()`` and ``multi_release()`` functions use the global state to add new multi-button functionality. 
    
    ``multi_press()`` prints ``"A is holding while B was pressed!"`` if the ``token`` is not "A" (so, it's "B"), and the holding indicator stored in ``state["A-holding"]`` is ``True``. 
    
    If both buttons are pressed (``state['A']`` and ``state['B']`` are ``True``), ``multi_press()`` sets the ``state['both']`` variable to ``True``, indicating to other handlers that both buttons are pressed. It then takes action, printing ``""Both buttons are being pressed"`` to the console.
    
    ``multi_release()`` prints ``"A is holding and B has been released"`` if the button that triggered the event is *not* the "A" button (``token``), the "A" button is currently being held (``state['A-holding']``), and both buttons haven't been pressed (``state['both']`` is ``False``).
    
    If both buttons have been released, indicated by ``state['both']`` being ``True``, and the state of each button being ``False`` (``state['A']`` and ``state['B']``), ``multi_release()`` prints ``"Both buttons released"`` to the console and sets ``state['both']`` to ``False``.
    
    Finally, we see the ``state`` object, implemented here as a dictionary, with the default values, defined on **lines 115-121**.


A few key differences to note:

* We are again using a global ``state`` object, in this case a dictionary instead of a class for illustration purposes. While the state tracked in ``ButtonDispatch`` is sufficient for almost all of the state we need for this example, in most applications, tracking would be necessary anyway. Having the button state outside of the ``ButtonDispatch`` class also separates the button state tracking from the event detection and handling, but sharing the variable means we can keep all state in one place.
* As mentioned earler, we're taking advantage of Python's *getters* and *setters* functionality so that when you change the ``ButtonDispatch`` object's state, it's actually changing our ``state`` dictionary. This is an example of the `Proxy Pattern <https://en.wikipedia.org/wiki/Proxy_pattern>`__ in action. 
* We've taken advantage of our new ``state`` dictionary to track whether or not both buttons are pressed (the ``both`` key). This acts as a *guard* so that we can differentiate between events.
* We've been able to handle some very complex situations in a very simple way - we cover the *both buttons pressed*, *both buttons released*, *b button pressed while a button is held* and *b button released while a button is held* events without a lot of code.

Here's a video of this code running on my Trinket M0:

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/dispatcher-demo-trinket-05.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/dispatcher-demo-trinket-05.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

There are many different ways of manipulating global (in the sense of application-wide) state, but this way is the least hard-coded - we take advantage of the fact that Python passes objects *by reference*, and pass the state object around, as opposed to relying on a global (in the sense of variable scope) object.

When something is *passed by reference*, it means that the original object isn't copied when it's passed to a function or assigned to another variable. This is more efficient, since only one copy of the object is used in many parts of the code. The side effect of this is that changes to the object, even when it's in a different scope, called by a different name, will affect the original object.

We take advantage of that so that our ``ButtonDispatch`` class uses the passed-in ``state`` dictionary to store its internal state. This effectively *externalizes* the state, and separates our concerns nicely.
