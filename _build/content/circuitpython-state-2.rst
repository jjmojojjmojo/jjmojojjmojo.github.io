State And Events In CircuitPython: Part 2: Exploring State And Debouncing The World
###################################################################################
:date: 2018-06-11 15:07
:author: lionfacelemonface
:category: tutorial
:tags: tutorial; circuitpython; hardware; state;
:slug: circuitpython-state-part-2
:status: draft

.. include:: ../emojis.rst

The Problem: Debouncing For Fun And Profit
==========================================
Most projects will have to deal with "bouncy" inputs, buttons in particular.

"Bounce", in this sense, is essentially a noisy signal. Logically, you would think that if a button was pressed, that it would be a simple boolean value - it's "on" or "off". "HIGH" or "LOW", ``True`` or ``False``. 

In reality, these values refer to a voltage, or the lack of a voltate. For our boards that voltage is 3.3 volts. When the voltage is at 3.3 volts (plus/minus some wiggle room), the pin will read ``True`` or "HIGH". The voltage is "on".

When there's no voltage (plus or minus some wiggle room), the pin will read ``False`` or "LOW". The voltage is "off".

An ideal button being pressed and released might look something like this if we graphed the voltage:

.. image:: {filename}/images/nonblocking-button-bounce-ideal.png
   :width: 80%
   :align: center
   

The problem is that you will rarely ever get such straightforward readings. You'll instead get what looks like many pressings in quick succession:

.. image:: {filename}/images/nonblocking-button-bounce-reality.png
   :width: 80%
   :align: center
   

What causes this? It's due to the realities of turning physical interactions into digital signals: when a button is pressed, a piece of metal crosses two contacts, completing a circuit. The microcontroller has an internal threshold that decides how much current constitutes "on" (or HIGH), and how much constitutes "off" (or LOW) - the aforementioned "wiggle room". That threshold can be shockingly large - sometimes what you would think is a "weak" signal, the microcontroller interprets as "HIGH".

Then there's the buttons themselves. Most buttons are composed of two pieces of metal that are separated by a physical gap. When you press the button, the metal pieces are brought into physical contact, causing current to flow through them as if they were a solid conductive element (like a piece of wire or a copper trace on a PCB). 

Since electricity *really* wants to flow, if given sufficient current and a short enough distance, it will jump through the air. When this happens inside of a button, it causes current to flow momentarily before the contacts are fully *in contact*, possibly causing a spike in the current being read from the microcontroller pin. 

Further, inconsistencies in the metal due to manufacturing or wear can cause multiple subsequent spikes to be sent to the microcontroller prior to the most "solid" one. Even when continually holding down a button, the strength of the signal can vary quite a bit. Sometimes it varies enough to be noticed by the microprocessor. 

As the button is released, the same issues happen *again*. 

In the case of a capacitive input, the capacitance that is increased by the user interacting with it is detectable long before the user has contacted the pad. It's not always possible to determine precisely when someone has contacted the pad, or we're just detecting a change in capacitance because someone is simply near it (we can use this to our advantage in some applications). There's also potential issues with interference that can make the signal more noisy than it should be.

So where you think you can use a logical check of a pin's status (``if pin.value``) in your code to determine if the button is pressed, and execute some code, it's not that simple. Without smoothing out the signal from the pin, your code will end up executing many times before the button is even fully pressed down. The number of times will vary from button to button, and can even vary from day to day. 

Maybe for some applications, like turning on an LED while a button is pressed, it's not really a problem. But if pressing that button has *side effects* it can be really, really bad.

.. note::
   
   For an in-depth analysis of *button* bounce and possible solutions, check out `A Guide To Debouncing <http://www.ganssle.com/debouncing.htm>`__ from the `Ganssle Group <http://www.ganssle.com/>`__. It's the best discussion I've found in my research, and often cited by other tutorials that you run into on the subject.
   
There's more to it than just noisy buttons, though. There are other "bouncy" signals that aren't quite as chaotic as button bounce, but need to be dealt with in the same way. 

Remember, your main loop is executing many thousands of times per second. If you check a pin's status every loop, even if the button attached to it is fully "debounced", your code will still get called many, many times. A perfectly clean signal will still trigger your code to run over and over and over.

The easiest way to deal with this both of these issues, and the most common seen in "getting started" tutorials is to "sleep" the processor, to *block* for a few fractions of a second before checking an input's value.

"Blocking" is when you tie up the processor, preventing any code from executing, while you wait for something to happen. 

We've already looked at code that blocks in the `Testing <{filename}/circuitpython-state-1.rst#Testing>`__ section of the first article in this series. We're using a Python function called ``time.sleep()`` that pauses processing for a given period of time (provided in seconds). 

This approach effectively smoothes out the signal from our inputs, by reducing the frequency at which we check the status of the button. Instead of checking *48 million times* every second (the clock frequency of the M0), we're only checking *5 times* per second. We'll miss any variations in the signal that happen while the button "settles" after its pressed.

.. note::
   
   The actual number of times your code runs is limited by many things, and even in an ideal situation will likely never *actually* run 48 million times per second. It might get close, 30 million, 10 million... 
   
   
The problem is that while code is blocking, *nothing else can happen*. 

This severely limits what we can do in our projects. Its harder to read from multiple inputs and write to multiple outputs. We become fixed to a set interval to do anything, because we physically *can't* do anything while the processor is sleeping.

So what can we do instead? 

We have a few viable options:

#. For buttons, we can use an `R/C filter circuit <https://en.wikipedia.org/wiki/RC_circuit>`__ to clean the input (a.k.a. *hardware debouncing*).
#. We can use an IC that does debouncing for us.
#. We can use `interrupts <https://www.sparkfun.com/tutorials/326>`__.
#. We can create a data structure that tracks the *state*, or status, of our inputs.

Hardware debouncing is only really useful in situations where the debouncing needs to be *rock solid*. It requires more components, which increases the cost (something more of an issue in industry) and introduces more complexity (more of an issue for us as hobbyists). Even with really solid hardware debouncing, we still need to be concerned with button state - remember what feels like a momentary press for a human being is an event that lasts many many processor cycles - if the action triggered by the button runs every cycle and if we aren't being conscious of the button state, we're in trouble.

Debouncing ICs are rare and tend to be expensive. We could program another microcontroller to do debouncing for us, but again, its more expensive and adds complexity. And *yet again* we still have to be conscious of button state - it just might be happening in our "daughter" microcontroller instead of our main one.

Interrupts are extremely cool - you can configure the processor such that when a pin reads "HIGH", it triggers the execution of a predetermined chunk of code. Our M0 boards allow for interrupts on nearly every pin. However, interrupt functionality is not currently exposed in CircuitPython |heartbreak|, so it's a non-starter for us.

Ultimately, tracking *state* is really the best option most of the time - and as we've seen, even with other debouncing methods, we will still need to deal with it. Not sure what *state* even means? The next section will go into great detail.

Basics Of State
===============
Let's start with basic definitions. *State* is simply the status or phase of something. It's how you would describe something that can *transition*.

For example, water has three common states: gas (steam), solid (ice), liquid (usually just called *water*). State is a way to refer to attributes of that thing at a given time. When water is brought to its boiling point of 100° C (212° F), it becomes less dense, and given the opportunity, it will disperse throughout a space. When water is taken down to 0° C (32° F), it freezes, becoming more dense, and solid. It will expand. At other temperatures between 0°C and 100°C, water is a liquid. It flows.

Note how water has multiple properties in each state. We could record each of those properties numerically - the temperature, the volume, the density - even attributes that are more binary (true/false) like "solid" and "liquid". Keep this in the back of your mind for now.

Lets look at another example, this time from a area of life that lives and breathes metrics: sports.

Keeping score during a sporting event is a way of tracking state. A performance happens, a ball is hit, a race ends, and the score is recorded. 

Here's a common scoreboard for sports like gymnastics:

.. image:: {filename}/images/nonblocking-state-examples-01.png
   :width: 80%
   :align: center
   
It's a single score, from a single judge. This scoreboard scores from 1-10, with down to hundredths of a point. This score is 9.70.

If we modeled the scoreboard in Python, we could use a single variable to store the score:

.. image:: {filename}/images/nonblocking-state-examples-02.png
   :width: 80%
   :align: center
   
Here, we simply name the variable ``score``. If we were modeling a real gymnastics match, we might want to differentiate between different scores, since there will be one for each judge, and each participant:

.. code-block:: python
    
    entrant1_judge1 = 9.70
    entrant1_judge2 = 9.45
    entrant1_judge3 = 10.0
    
    entrant2_judge1 = 8.75
    entrant2_judge2 = 9.00
    entrant2_judge3 = 8.80
    
    entrant3_judge1 = 10.0
    entrant3_judge2 = 9.99
    entrant3_judge3 = 9.98
    

This straight-forward, but a bit unwieldy. We're only set up for three judges, and three entrants, and a *single* match. In a tournament there may be 10 matches, and there could be dozens of entrants. That's a lot of variables to track, and all we're tracking is the scores. Imagine if we also wanted to give the entrants a name or id number, or track their vital statistics!

We can simplify and generalize things a bit by using Python's built-in data structures.

.. tip::
    
    If you aren't familiar with Python's built-in data structures, Adafruit has put together a `simple guide <https://learn.adafruit.com/basic-datastructures-in-circuitpython/overview>`__.
    
    

There are many, many ways to model a match like this, here's just one using lists and dictionaries:

.. code-block:: python
    
    matches = [
        [
            {
             "judge1": 9.70,
             "judge2": 9.45,
             "judge3": 10.0
            }, 
            {
             "judge1": 8.75,
             "judge2": 9.00,
             "judge3": 8.80
            }, 
            {
             "judge1": 10.0,
             "judge2": 9.99,
             "judge3": 9.98
            }
        ]
    ]
    
To access the second judge's score for the third entrant in the first match (remember list indexes start with 0):

.. code-block:: python
    
    matches[0][2]["judge2"]
    

So that works for modeling something like a gymnastics match, where you have somewhat similar data, but it is recorded multiple times. 

In a microcontroller project, we're dealing more with what's called *global state* - state that is used by the whole project. We need to track our buttons and digital pins and sensors in one place, and use the values throughout our project.

A better analogy for our needs is the *scoreboard* from a team-based sport. A sports arena/field will have one giant board that tracks the state of the entire game - all relevant information you need to understand the progress of the game is available in one place. It's globally accessible, you can see it from any seat - you just need to look at it. 

Here's a contrived example of a typical scoreboard from an American baseball stadium:

.. tip::
    
    The nuances and rules for American baseball are not relevant to this article, but if you aren't familiar and want to dig in, the `wikipedia article <https://en.wikipedia.org/wiki/Baseball>`__ is the place to start.
    

.. image:: {filename}/images/nonblocking-state-examples-03.png
   :width: 80%
   :align: center

It has various regions with indicators, usually lights, and numbers representing the state of the game. Each one represents an independent piece of important information. That information changes as the game progresses. Outs are made, points (runs) are scored, innings go by (there are 9 in a typical baseball game).

We can model a scoreboard as a series of variables, like we did initially for the gymnastics match:

.. image:: {filename}/images/nonblocking-state-examples-04.png
   :width: 80%
   :align: center
   
This is totally viable, and less problematic than doing the same thing for a gymnastics tournament, since these variables, collectively, are a single, central point of reference for what state the game is at, at any given moment.

There are alternative ways of modeling global state, however. The two primary ones are: using a *dictionary* and using a *class*. 

A dictionary in Python is a key-value mapping, also known as an *associative array*, *hash*, or *hashmap*. Data is stored by name in a simple table. Here's what our scoreboard looks like as a dictionary:

.. code-block:: python
    
    scoreboard = {
        "ball": 1,
        "out": 1,
        "strike": 2, 
        "guest_score": 5,
        "inning": 2,
        "home_score": 10
    }
    
We access the various values like this:

.. code-block:: python
    
    outs = scoreboard["out"]
    scoreboard["inning"] += 1
    scoreboard["guest_score"] = 6
    
So we have a single, global variable, ``scoreboard``, that contains all of the information about the game. As the game progresses, ``scoreboard``'s members are updated.

This has the advantage over using a series of variables in that it is more compact, but flexible - we're only using up one variable name, and the names of our state attributes can be almost anything - words with spaces, dashes, even other objects.

.. note::
    
    For an object to be used as a dictionary key, it must be `hashable <https://docs.python.org/3.6/glossary.html#term-hashable>`__. 
    
    
Dictionaries are limited in that they are strictly mappings of some key to some value. There are times when you will need to add more functionality, and that's where *classes* come in. 

A *class*, in the simplest terms, is a data structure that contains variables (called *attributes* or *properties*), and functions (called *methods*). 

What makes classes special is that they are used as a blueprint for creating new objects. You define what your class looks like once, and then create *instances* of your class that store your data. 

.. tip::
    
    There is a *ton* more to classes in Python. This is called `Object-Oriented Programming <https://en.wikipedia.org/wiki/Object-oriented_programming>`__ (OOP), and is a whole school of thought unto itself in programming (or *paradigm*).
    
    I'm not going to go into too much detail here, since there is much to discuss. 
    
    A good place to start is `the python OOP tutorial <https://docs.python.org/3/tutorial/classes.html>`__.
    
For our purposes, classes provide a way of reasoning about state in a self-contained manner. The class contains all of our state variables, and it has methods that operate on it. We can extend the class if we need to, and can even use it to handle global state for multiple similar parts of our project.

Here's a simple example of a class that represents our scoreboard:

.. code-block:: python
    
    class ScoreBoard:
        def __init__(self):
            self.scores = {
                "guest": 0,
                "home": 0
            }
            
            self.inning = 1
            self.out = 0
            self.ball = 0
            self.strike = 0
            self.extra_innings = False
            
        def tied(self):
            return self.scores["home"] == self.scores["guest"]
            
        def next_inning(self):
            if self.out == 3:
                self.inning += 1
                
                if self.inning > 9 and not self.tied():
                    print("Game is over")
                else:
                    self.extra_innings = True
                
            
.. explanation::
   
   This is a standard class definition. 
   
   **Line 1** sets the name of the class. 
   
   Every method defined in the class will be passed at least one parameter, ``self``. ``self`` is a reference to the current instance of the class.
   
   **Lines 2-12** define the *constructor* of the class, which is always named ``__init__()``. This method is called only once, when the class instance is initially created. 
   
   In Python, a class method name surrounded by two underscores on each side is considered "magic" - it has special meaning, like how this method is the constructor. 
   
   .. tip::
      
      Magic methods are a extremely useful feature of Python, and are worth researching fully. 
      
      Check out this `comprehensive view of magic methods in Python <https://rszalski.github.io/magicmethods/>`__ for more information.
      
   
   The constructor is used to establish all of the default values for the instance attributes. That's what's occurring on **lines 3-12**.
   
   *Instance methods* are defined on **lines 14-15** (``tied()``), and **17-24** (``next_inning()``). 
   
   Instance methods are methods that operate on an instance of a class. A reference to the instance is passed to all instance methods, named ``self``. We call them *instance* methods to differentiate them from *class methods*. Class attributes are explained a bit later on in this article. The thing to know about class *methods* is that instead of the first parameter being a reference to the *instance*, its a reference to the *class*. 
   
   .. tip::
       
       Most of the time you won't have to deal with class methods. In fact, to use them, you must decorate a method with the special ``@classmethod`` decorator. 
       
   
   ``tied()`` will returns ``True`` if the game is tied, and ``False`` if not.
   
   ``next_inning()`` advances the inning, and ends the game when we reach inning number 9. That is, unless its a tied game, then it sets ``self.extra_innings`` to ``True``, and continues counting. 
   
   ``tied()`` is a typical utility method, used by either someone interacting with the instance, or by the instance itself, to do some calculations based on the current values of the instance attributes.
   
   ``next_inning()`` is used to *encapsulate* all of the logic that goes into determining if the game has ended or not, as well as doing any accounting necessary to move on to the next inning.
                    
Here's how we interact with it:

.. code-block:: pycon
    
    >>> board = ScoreBoard()
    >>> board.out = 3
    >>> board.next_inning()
    >>> board.inning
    2
    >>> board.tie()
    False
    >>> board.scores["guest"] = 8
    >>> board.scores["home"] = 8
    >>> board.tie()
    True
    >>> board.next_inning()
    >>> board.next_inning()
    >>> board.next_inning()
    >>> board.next_inning()
    >>> board.next_inning()
    >>> board.next_inning()
    >>> board.next_inning()
    >>> board.next_inning()
    >>> board.inning
    10
    >>> board.extra_innings
    True
    >>> board.scores["home"] = 9
    >>> board.next_inning()
    Game is over
    

When we call the ``next_inning()`` method, we have some logic to check if the game is tied at the 10th inning. If it is, the ``extra_innings`` flag is set to ``True``. Otherwise, the game is over.  

This is something special that classes give us over other ways of modeling state. We have a fully *encapsulated* state object - everything we do with state, and all the data we care about, lives inside that object, represented by the ``ScoreBoard`` class. 

Now lets look at how we can work this concept into a microcontroller project. We'll start by bringing things back to basics. 

State And Microcontrollers
--------------------------

Lets apply state tracking to our `testing  code <{filename}/circuitpython-state-1.rst#Testing>`__. Recall that to test our board, we set up a simple project that has the following functionality:

* While button "A" is pressed, the built-in red LED lights up.
* While button "B" is pressed, the built-in NeoPixel or DotStar lights up in white.

We'll extend this a little bit and:

* Every time button "B" is pressed, the built-in RGB LED (NeoPixel or DotStar) will light up in a *different color*.

To make this work, here is the state we have to track:

* the value of button "A"
* the value of button "B"
* should the LED be on or off?
* should the RGB LED be on or off?
* what color should the RGB LED be?

Again, we can simply use multiple variables to hold various state values, but we'll see how convoluted this can get:

.. tip::
    
    Remember this code is assuming you have created a ``setup.py`` file as explained `in the previous article <{filename}/circuitpython-state-1.rst#abstractions: keeping the code simple>`__.
    
    

.. code-block:: python
    
    import time
    from setup import led, rgb, check
    
    # review of what the setup module does for us:
    # 
    #   - led is our digital pin object connected to pin 13
    #   - rgb is our DotStar or NeoPixel
    #   - check() is a function that handles differences between button wiring
    
    # these state variables need specific names
    led_state = False
    button_a_state = False
    button_b_state = False
    rgb_state = False
    rgb_color = (255, 255, 255)
    
    while True:
        button_a_state = check("A")
        button_b_state = check("B")
        
        if button_a_state:
            led_state = True
        else:
            led_state = False
            
        if button_b_state:
            rgb_state = True
        else:
            rgb_state = False
            
        led.value = led_state
        
        if rgb_state:
            rgb.fill(rgb_color)
        else:
            rgb.fill((0, 0, 0))
            
        time.sleep(0.2)
    
.. explanation::
    
    **Line 1 and 2** are our standard imports.
    
    **Line 11-15** is where we define each of our state variables, and set their default state. Note that we had to use some inelegant names because we already have some objects that might conflict.
    
    **Line 17-38** is our main loop.
    
    **Line 18 and 19** read the button pins and update the button state variables.
    
    **Lines 21-19** update the LED and RGB pixel state variables based on the state of the buttons.
    
    **Line 33-36** uses the state variables to affect the real world, by turning on or off the LED and RGB pixel.
    
    Finally, on **line 38**, we sleep for 0.2 seconds to debounce the buttons.
    

Before we go much further, lets draw an important distinction. Unlike a physical scoreboard at a baseball stadium, which acts as part of the experience of watching the game, our state merely *reflects* our reality. 

The way we work with state is to alter it either *because* something happened (say, a button was pressed, much like scoring a point in a game), or to *cause* something to happen (this is different; like lighting up an LED, or changing a NeoPixel's color).

It's a three-pass system. First, state is assessed - input pins are read, sensors are queried. The state object is updated to reflect what was observed in real life. 

The second pass involves looking at the state object and changing state based solely on that - something happened during the first pass that requires the state to change. A button's state has changed, so we need to update the state of the LED.

The final pass reconciles the state object with reality. This is where you would buzz a piezo speaker, update a display, or turn on an LED. These are considered *side effects* - when we execute code, like setting a digital pin to ``True``, our code has had effects outside of its scope. 

.. note:: 
   
   In this case, and for our purposes, the side effects usually affect the physical state of our project (the LED lights up). But in programming, side effects can be anything, and are usually affecting other parts of our code or our data.
   

Here's a diagram showing how it works:

.. image:: {filename}/images/nonblocking-state-flowchart.png
   :width: 80%
   :align: center

.. tip::
   For our simple example, we can shortcut some of these steps (for example, just directly set the value of the led to that of its button). But it's good to think about things in this multiple-pass manner, since it makes more complex things much easier to reason about.
   

We need to add our "different color" feature. Before we do that, lets refactor our state variables into a class:

.. code-block:: python
    
    import time
    from setup import led, rgb, check
    
    class State:
        def __init__(self):
            self.led = False
            self.button_a = False
            self.button_b = False
            self.rgb = False
            self.color = (255, 255, 255)
            
        def __repr__(self):
        return "<Buttons: {}/{}, LED: {}, RGB: {}, Color: {}>".format(self.button_a, self.button_b, self.led, self.rgb, self.color)
    
    state = State()
    
    while True:
        # first pass: check real life
        state.button_a = check("A")
        state.button_b = check("B")
        
        # second pass: assess state
        if state.button_a:
            state.led = True
        else:
            state.led = False
            
        if state.button_b:
            state.rgb = True
        else:
            state.rgb = False
            
        # third pass: reconcile state
        led.value = state.led
        
        if state.rgb:
            rgb.fill(state.color)
        else:
            rgb.fill((0, 0, 0))
            
        time.sleep(0.2)
        
.. explanation::
   
   This code is identical to the last example, except that we've replaced the state variables with a single state class, called ``State``.
   
   The ``State`` class, defined on **lines 4-13**, has two defined methods. The first is ``__init__()``, the constructor. It sets up the default values of all of the attributes of the ``State`` instance.
   
   The second defined method, ``__repr__()`` is also special, like ``__init__()`` - it is called whenever you need a *representation* of an instance object. It serves two purposes. 
   
   First, it can be used to return valid Python code that could be used to recreate your object. 
   
   The other purpose to provide a quick glance into what data the object holds - in this case it doesn't have to be valid Python - we indicate that we're using this purpose by wrapping our return value in angle brackets (``<>``).
   
   Every standard Python data type implements this method. Its what you see when you just evaluate an object:
   
   .. code-block:: pycon
        
        >>> l = [1, 2, "three", 4, 6, 9]
        >>> l
        [1, 2, 'three', 4, 6, 9]
        >>> state = State()
        >>> state
        <Buttons: False/False, LED: False, RGB: False, Color: (255, 255, 255)>
        >>> state.rgb = True
        >>> state
        <Buttons: False/False, LED: False, RGB: True, Color: (255, 255, 255)>
        
   Here we illustrate the standard Python type behavior by creating an then evaluating a simple list, then instantiate our ``State`` class, evaluate it, change an attribute, and evaluate it again.
   
   It's a good practice to define ``__repr__()`` in your classes, as it helps when debugging.
   
   In our ``__repr__()`` method, we're using the ``.format()`` string method to insert instance values into our return value. 
   
   On **line 15**, we instantiate our ``State`` instance for use in our main loop.
   
   In our main loop on **lines 17-41**, the logic is exactly the same as before, except we are accessing attributes of our ``state`` object.
   

Interacting with the one ``state`` object is a lot cleaner than dealing with five disparate variables. But what's really cool about using a class like this is that we can give our ``state`` object its own *functionality*.

We do this by adding a method. As we covered earlier, methods are just functions that are part of a class. What sets them apart is their context. A function runs within the module where its defined. A method runs within the instance of the class where it was defined. 

We'll take the "different" part of our feature requirement to an extreme, and add a method to the ``State`` class that generates a totally *random* color:

.. code-block:: python
    
    import time
    import random
    from setup import led, rgb, check
    
    class State:
        def __init__(self):
            self.led = False
            self.button_a = False
            self.button_b = False
            self.rgb = False
            self.color = (255, 255, 255)
        
        def random_color(self):
           self.color = (
                random.randrange(0, 255),
                random.randrange(0, 255),
                random.randrange(0, 255)
           )
            
        def __repr__(self):
        return "<Buttons: {}/{}, LED: {}, RGB: {}, Color: {}>".format(self.button_a, self.button_b, self.led, self.rgb, self.color)
    
    state = State()
    
    # -- snip --
    
.. explanation::
   
   This code replaces the first lines of the previous example. Everything from the initial imports, through to instantiating the ``state`` object is replaced with the above, up to the ``# -- snip --`` comment. 
   
   The first difference is that we've imported the ``random`` module, on **line 2**. This is a standard Python module that provides an interface with a `psuedo-random number generator <https://en.wikipedia.org/wiki/Pseudorandom_number_generator>`__.
   
   The other change is the implementation of the ``random_color()`` method on **lines 13-18**. This method uses the ``randrange()`` function from the ``random`` module to select three random numbers between 0 and 255 (the range of valid red, green, and blue amounts), and set ``self.color`` to a tuple containing them.
   
   So every time the ``random_color()`` method is called, a new random color is generated and stored in the state object.
   

Now we can change the logic in our ``while True`` loop to generate a random color.

.. code-block:: python
    
    import time
    import random
    from setup import led, rgb, check
    
    class State:
        def __init__(self):
            self.button_a = False
            self.button_b = False
            self.led = False
            self.rgb = False
            self.color = (255, 255, 255)
    
        def random_color(self):
            self.color = (
                 random.randrange(0, 255),
                 random.randrange(0, 255),
                 random.randrange(0, 255)
            )
    
        def __repr__(self):
            return "<Buttons: {}/{}, LED: {}, Color: {}>".format(self.button_a, self.button_b, self.led, self.color)
    
    state = State()
    
    while True:
        # update the state
        state.button_a = check("A")
        state.button_b = check("B")
        
        # take action - change the state
        if state.button_a:
            print("LED: on")
            state.led = True
        else:
            state.led = False
            
        if state.button_b:
            print("RGB on. Color: {}".format(state.color))
            state.rgb = True
        else:
            state.rgb = False
            state.random_color()
            
        # take action - do things that cause side effects
        led.value = state.led
        
        if state.rgb:
            rgb[0] = state.color
        else:
            rgb[0] = (0, 0, 0)
        
        time.sleep(0.2)

.. explanation::
    
    Everything here has been explained before, with the exception of the following:
    
    * We call the ``random_color()`` method on **line 42**, so now we get a new color every time the button is not pressed.
    
    * We've added some debugging helpers, ``print()`` calls, on **lines 32 and 38**. This way when watching the Python console, we can see what's going on, and keep an eye on how our state is changing.
    

A few notes:

* With every loop, if the "b" button is not pressed, we call ``state.random_color()``. This means the color of the pixel is always changing, even when the RGB pixel isn't illuminated. This is sub-optimal. We never want to do work when we don't have. We'll address this situation in the next section when we start dealing with *events*.
* There's an added ``print()`` each time the state changes. This serves two purposes. First, it can be hard to see LEDs working in the video below, so I'll also demonstrate with a screen grab of Mu's console. Second, there are times when we'll be doing things repetitively and not realize it. If we're triggering some action more often then we intend to, it could be a bug. Calling ``print()`` will let us see this in the console, even if we can't see it in our hardware. 

Here's a video of this code running on my Trinket M0:

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/state-demo-trinket-01.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/state-demo-trinket-01.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

Before we move on, lets *refactor* our code again, but just a little bit. Since ``State`` is our keeper of state for our project, lets move **all** of the code that changes state into to a method of the ``State`` class:

.. code-block:: python
    
    import time
    import random
    from setup import led, rgb, check
    
    class State:
        def __init__(self):
            self.button_a = False
            self.button_b = False
            self.led = False
            self.rgb = False
            self.color = (255, 255, 255)
    
        def random_color(self):
            self.color = (
                 random.randrange(0, 255),
                 random.randrange(0, 255),
                 random.randrange(0, 255)
            )
            
        def update(self):
            self.button_a = check("A")
            self.button_b = check("B")
            
            if self.button_a:
                print("LED on")
                self.led = True
            else:
                self.led = False
                
            if self.button_b:
                print("RGB on. Color: {}".format(state.color))
                self.rgb = True
            else:
                self.rgb = False
                self.random_color()
    
        def __repr__(self):
            return "<Buttons: {}/{}, LED: {}, Color: {}>".format(self.button_a, self.button_b, self.led, self.color)
    
    state = State()
    
    while True:
        # update the state
        state.update()
            
        # take action - do things that cause side effects
        led.value = state.led
        
        if state.rgb:
            rgb[0] = state.color
        else:
            rgb[0] = (0, 0, 0)
        
        time.sleep(0.2)
        
.. explanation::
    
    This code is identical to the last example, except for the addition of the ``update()`` method to the ``State`` class.
    
    ``update()`` is defined starting on **line 20**. It's simply a copy/paste of the logic from the main loop in the last example, just altered so it references ``self`` instead of ``state``.
    
    We've added a call to ``state.update()`` on **line 44**, to invoke the code that we moved into the ``update()`` method.
    

Now the ``State`` class is truly the authority for all things state-related. In OOP terms, it's *fully encapsulated*. 

Now that we've explored what state is, and how we can write code to deal with it, we have opened ourselves up to some really neat possibilities. But since we're using ``time.sleep()``, our code is still blocking, and we're still limited by that. The next step is to utilize our new understanding of state to debounce without blocking.

Using State To Avoid Blocking
-----------------------------
The next step is to get rid of that blocking code. This is another thing our ``State`` class can handle for us. 

As discussed earlier, the reason why we block is to keep our code from running too fast. This keeps our signals from our buttons smooth, avoiding bouncing.  

Another way to look at it is that we've introduced the passage of time into our main loop. We're fixing our code to an interval of 0.2 seconds, so we can wait until a button is completely pressed or released before we act, and so that our code won't run over and over without reason.

We can accomplish the same goal in a different way using state. Instead of putting a full stop on all of our code for 0.2 seconds, we can instead look at a some sort of clock at the start of every loop, and only *act* every 0.2 seconds. While we're waiting for time to pass, other code can run, getting rid of the blocking.

This means that the time we looked at the clock is a *new state attribute*. We can reference this new attribute to decide when to act.

So how do we track passing time? Most microcontrollers don't have true built-in clocks like PCs. Most computers have what's called a "`real-time clock <https://en.wikipedia.org/wiki/Real-time_clock>`__", or RTC. It's typically an integrated circuit that counts time in a highly accurate way using some sort of oscillating crystal. A battery is used to keep power to the IC so that it won't loose track of time, especially when the PC is powered off. 

While we can get microcontrollers with RTCs built in, and as add-on boards (Adafruit has several in their shop that have `CircuitPython support <https://learn.adafruit.com/adafruit-pcf8523-real-time-clock/rtc-with-circuitpython>`__), they are typically reserved for applications where "clock time" is necessary - for example, a digital alarm clock, or logging sensor data. 

Luckily, microcontrollers are in themselves a sort of *pseudo-clock*, because they operate on a regular processor cycle. 

The processor cycles are fixed to a specific rate. For example, our M0 board "clocks" at 48 megahertz (*48,000,000* cycles per second). That means that every second, the processor scans the part of its memory where your program code lives, and executes the instructions it finds *fourty-eight million times*. 


.. note::
   
   The chips in these CircuitPython boards, the ATSAMD21 and ATSAMD51, have a built-in *oscillator*. They have circuitry in the chips that can generate a regular pulse that can be used for clocking the processor. Not all microcontrollers have these. You'll often see a little oblong silver cylinder on the board (a `crystal oscillator <https://en.wikipedia.org/wiki/Crystal_oscillator>`__) - this is the real "clock" in that situation. 
   
   The processor runs at the frequency of the outboard oscillator. In the case of the M0/M4 chips, you can choose to use an external oscillator or choose one of several built-in to the chip.
   

That cycle is very reliable, so it's possible to track it, and with some math, convert cycles to seconds passing over time. 

There's a function in the ``time`` module that does just that. It's called ``time.monotonic()``. When called, it returns the number of seconds that have passed since the processor was turned on. 

.. tip::
   
   Behind the scenes, CircuitPython is using so-called `timer interrupts <https://learn.adafruit.com/multi-tasking-the-arduino-part-2/timers>`__, features of microcontrollers where you can tell the processor to execute specific code blocks at regular intervals based on processor cycles.
   

``time.monotonic()`` returns a *float*, or `floating-point number <https://en.wikipedia.org/wiki/Floating-point_arithmetic>`__ - essentially a fraction, so it's ideal for our two-tenths-of-a-second debouncing rate.

Now, let's take advantage of this in our code. 

First, we'll need to add a new attribute to our ``State`` class. It will represent the last time we looked at the clock, or *checked in* with the processor. We'll call it ``checkin``. 

Initially, we'll set it to the value of ``time.monotonic()``. By doing this in the constructor (``__init__()``), we are calling ``time.monotonic()`` when we create the ``state`` variable from the ``State`` class. So the initial value of ``state.checkin`` will be the number of seconds from when the board was powered on, until that line of code is executed.

We'll look at ``checkin`` every loop, and see if the current value of ``time.monotonic()`` is at least 0.2 seconds larger - this would mean that 0.2 seconds have elapsed. 

At that point we can update our state, in our case read the buttons.

Finally we need to set ``checkin`` to the current value of ``time.monotonic()``, to mark the last time we checked the clock, and the cycle can start all over again.

.. code-block:: python
    
    
    import time
    import random
    from setup import led, rgb, check
    
    class State:
        _debounce = 0.2
        
        def __init__(self):
            self.button_a = False
            self.button_b = False
            self.led = False
            self.rgb = False
            self.color = (255, 255, 255)
            self.checkin = time.monotonic()
    
        def random_color(self):
            self.color = (
                 random.randrange(0, 255),
                 random.randrange(0, 255),
                 random.randrange(0, 255)
            )
            
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                self.button_a = check("A")
                self.button_b = check("B")
                
                if self.button_a:
                    print("LED on")
                    self.led = True
                else:
                    self.led = False
                    
                if self.button_b:
                    ﻿print("RGB on. Color: {}".format(self.color))
                    self.rgb = True
                else:
                    self.rgb = False
                    self.random_color()
                    
                self.checkin = time.monotonic()
    
        def __repr__(self):
            return "<Buttons: {}/{}, LED: {}, Color: {}>".format(self.button_a, self.button_b, self.led, self.color)
    
    state = State()
    
    while True:
        # update the state
        state.update()
            
        # take action - do things that cause side effects
        led.value = state.led
        
        if state.rgb:
            rgb[0] = state.color
        else:
            rgb[0] = (0, 0, 0)
    
.. explanation::
    
    Changes in this iteration:
    
    * On **line 6**, we introduce the concept of a *private class attribute*, called ``_debounce`` (class attributes and 'privacy' are discussed below). We're using it to hold the number of seconds we want to wait before deciding if a button was pressed or not.
    
    * On **Line 14**, the new ``checkin`` attribute is established, and its default value is set to ``time.monotonic()`` - so it will be a float of the number of seconds since the board was powered on (roughly). The specific default value will be the number of seconds since the board was powered on *when the class is instantiated* on **line 46**. As discussed above, this gives us a reference point for debouncing. 
    
    * The ``update()`` method has been altered to both utilize the ``checkin`` attribute to only change the state every 0.2 seconds (**line 24**), and update the ``checkin`` value after its done doing that (**line 41**).
           

We've introduced a new concept beyond the addition of tracking time. Note the addtion of a variable in the class, defined outside of any methods, called ``_debounce``. 

``_debounce`` is a *class attribute*, meaning that it belongs to the ``State`` class, and not to the instance object created from ``State`` (in our code, the instance is named ``state``), even though we can access it from the instance (``self._debounce`` in our methods, or ``state._debounce`` in our main code). 

By making ``_debounce`` a class attribute, we are indicating to anyone who uses our class that we don't intend for the value to be changed. However, if we were to change it, we would do so by accessing it as ``State._debounce``. What's really interesting is that changing ``State._debounce`` would change *all* of the instances of ``State`` too. 

There's some nuance to it, but generally speaking, we use class attributes like this when we want to set a value that will rarely, if ever, change. We're using it here like a configuration setting.

.. tip::
   
   `This post <https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide>`__ does a great job of explaining instance attributes and class attributes in great depth.
   

There's something else noteworthy about ``_debounce``. We've prefixed it with an *underscore*. This indicates that it should be considered a *private* attribute. This means the attribute is intended for use only within the class methods, and it's not to be accessed from outside. 

.. note::
   
   In Python, private attributes and methods are simply a *convention*. You shouldn't peek, but if you do, things will still work. The underscore is just a signal to other programmers that you don't intend the attribute to be used outside of the class.
   
   In other languages, this is not the case - an attribute declared private will not be accessible *at all* outside of the class - it's like it doesn't exist.
   
   Since the concept of "privacy" in Python is merely a convention, it's better to express it not as "hidden" or "forbidden", but more so "an attribute name that I can't promise won't change, so don't count on it being there". 
   

The changes are pretty subtle, but here's another video showing this version running on my Trinket M0:
   
.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/state-demo-trinket-02.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/state-demo-trinket-02.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   
At this point we've "unblocked" our code, and crafted a really clean way of working with state.

There is a small flaw here, as touched on earlier. The ``random_color()`` method is being called nearly every 0.2 seconds, whether the button has been pressed or not. This is better than the first version of the code, where it was running almost every single loop, but it's still unnecessary. 

What we want, is for the color to change only once, when you stop pressing the button. Or even when you first press it, before the ``rgb`` state attribute is set to ``True``.

What that means is we want to detect when a button's state has changed from ``True`` to ``False``, or ``False`` to ``True``, and then take action.

What we want to do is called *event detection*.

Events
------
In order to avoid calling ``random_color()`` every single time we update our state whether the "b" button was pressed or not, we need to decide when the best time to call ``random_color()`` is. For this example, we were calling ``random_color()`` when the button was unpressed because if we didn't, the color would change every 0.2 seconds that you held the button down (or constantly before we were tracking time). 

So when should we do it, to avoid calling ``random_color()`` too frequently?

Think about how a button works. When you press it, the pin reads "HIGH" until you remove your finger (or "release" the button). Then it reads "LOW". These are two separate *events* - **press** and **release**. 

* **Press** happens when the button changes from "LOW" to "HIGH" - it wasn't pressed, and now it is. 

* **Release** happens when the button changes from "HIGH" to "LOW" - it *was* pressed, and now *it isn't*. 

In Python, that means the *press* event happens when a pin's ``value`` attribute used to read ``False``, and now it reads ``True``. A *release* even happens when a pin's ``value`` used to read ``True`` and now it's ``False``. 

We know what the previous value was because we've stored in it our ``state`` object. We can use that to detect the change in state.

The basic logic looks like this:

.. image:: {filename}/images/basic-button-event-logic.png
   :width: 80%
   :align: center

Now that we can act *only* when the button transitions from one state to the other, we can call ``random_color()`` in a more logical place, like right before we change the RGB pixel's state, when the button is pressed. We could also just do it when the button is released, more in line with the original logic. 

Here's our code again, with the ``random_color()`` call wrapped inside of a *press* event:

.. code-block:: python
    
    ﻿import time
    from setup import led, rgb, check
    
    import random
    
    class State:
        _debounce = 0.2
    
        def __init__(self):
            self.button_a = False
            self.button_b = False
            self.led = False
            self.rgb = False
            self.color = (255, 255, 255)
            self.last_color = (255, 255, 255)
            self.checkin = time.monotonic()
    
        def random_color(self):
            print("Generating random color")
            self.color = (
                 random.randrange(0, 255),
                 random.randrange(0, 255),
                 random.randrange(0, 255)
            )
    
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                self.button_a = check("A")
    
                # b button was pressed
                if not self.button_b and check("B"):
                    print("B button pressed")
                    self.random_color()
                    self.button_b = True
                else:
                    self.button_b = False
    
                self.checkin = time.monotonic()
    
                if self.button_a:
                    print("LED on")
                    self.led = True
                else:
                    self.led = False
    
                if self.button_b:
                    print("RGB on. Color: {}".format(self.color))
                    self.rgb = True
                else:
                    self.rgb = False
    
        def __repr__(self):
            return "<Buttons: {}/{}, LED: {}, Color: {}>".format(self.button_a, self.button_b, self.led, self.color)
    
    state = State()
    
    while True:
        # update the state
        state.update()
    
        # take action - do things that cause side effects
        led.value = state.led
    
        if state.rgb:
            rgb[0] = state.color
        else:
            rgb[0] = (0, 0, 0)
    
            
.. explanation::
    
    This is a major shift in how our code works, but it's accomplished with a very minor change. 
    
    On *line 31*, we compare the current physical state of the button with the value we've stored in our state object. If it's changed from "not pressed" (``self.button_b`` is ``False``) to "pressed" (``check("B")`` returns ``True``), then we've detected the *press* event. 
    
    We only change the color to a new random one (call ``self.random_color()``, **line 33**) when the button state has changed, instead of calling it whenever the button is being pressed.

We're now set up to handle even more events, like button holds. Or even complex events like pressing multiple buttons at once.

If you've done any programming in the past with GUIs, or front-end web application development, this may seem very familiar. It's very similar to how mouse and keyboard events are handled in these environments. 

But don't be distracted by this! An event is not inherently tied to human interaction. An event can be *anything*. If it can be detected, we can call it an event, and take action when it happens (we can *handle* the event). 

Imagine you have some environmental sensors. You can detect UV index, brightness of light, temperature, and relative humidity.

All of the following would be examples of events:

* The temperature increases by 10 degrees Fahrenheit. 
* The humidity drops by 20%.
* The humidity drops by 20% *over the course of one hour*. 
* The UV index is over 6 and the temperature is over 85 degrees Farenheit.
* There is very little light falling on the light sensor - *it's probably night time*.
* It was nighttime, but now it's not, *it's probably sunrise*. 

You get the idea - all of these events would be handled by some code - change the color of a status LED, write a log message, send an SMS reminding you to put on some sunscreen, put the CPU into "low power" mode, etc. 

You gain a lot of insight when you start to look at coding a microcontroller project as a problem of *managing state*. Changes in state trigger *events*. You *handle* those events with code. Very complex problems become very easy to reason about and debug.

State: Considerations
=====================
There are many benefits to modeling our project code around state:

* We have ultimate flexibility. When it comes to debouncing or otherwise detecting events, we can avoid blocking. Generally speaking, managing state lets us decide what data care about, and define our own events based on what the state object looks like.
* We can separate our concerns. Instead of mixing complex logic and interacting with components and peripherals, we can do one, then the other.
* We have good transparency. It's obvious what data we care about, since it's all wrapped up in the state object. Using a global state object, we can inspect the state anywhere in our code.
* The code can be factored in such a way that it is very simple to reason about. With a few rules attached to the state variables, we can condense a complex series of if/else statements into just a few that are easy to wrap our heads around.
* Events are easy to detect, since we have a record of what things looked like in the past.

This is great, but there are some drawbacks:

* We will ultimately end up using more memory. This isn't too big of a concern on a beefy platform like the M0 Express boards, but we still have limits to how much memory we can use and have to remain conscious of this. 

.. tip::
   
   There is an excellent article series over on `Hackaday <https://hackaday.com/2015/12/09/embed-with-elliot-debounce-your-noisy-buttons-part-i/>`__ that covers debouncing in depth and illustrates a solution for the Arduino platform that is *extremely* memory efficient. Something like this could be adapted to CircuitPython if our state keeping variable got to be too memory intensive.

* The timing is likely to be ever-so-slightly inaccurate. While processor cycles are very consistent, counting them tends to loose accuracy over time (in PCs this is called "clock drift"). This is also due to the math being done - counting millions of cycles and dividing that by seconds and rounding to the precision available causes rounding errors.
* There can still be blocking code, and aspects of Python (like `the GIL <https://wiki.python.org/moin/GlobalInterpreterLock>`__) that can further throw off your timing, especially when your code is running for long periods of time (days). 
* The precision of ``time.monotonic()`` is pretty shallow compared to the counters that CircuitPython uses behind the scenes to calculate it. Its typically only going to give you precision to hundredths of a second. Perfectly adequate for our purposes, but it could become an issue in some contexts (video games, for example).

So there are things to be concerned about, but nothing that detracts from the utility of this approach.

.. tip::
    
    At the time of writing, there is an `open issue <https://github.com/adafruit/circuitpython/issues/519>`__ addressing the inaccuracy of ``time.monotonic()`` in the CircuitPython github with a promising pull request attached. Worth keeping an eye on, and here's hoping that it gets more attention.
    

In the following sections, we'll take this approach further, and create an easy-to-use state object that will execute arbitrary code when certain things happen, particularly button events.
