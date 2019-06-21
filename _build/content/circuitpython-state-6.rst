State And Events In CircuitPython: Addendum: What To Do When You Run Out Of Memory
##################################################################################
:date: 2018-06-11 15:07
:author: jjmojojjmojo
:category: tutorial
:tags: tutorial; circuitpython; python; hardware; state;
:slug: circuitpython-state-addendum
:status: draft

.. include:: ../emojis.rst


What To Do When You Run Out Of Memory
=====================================
Occasionally, especially as a project grows in complexity, you will run into an exception:

.. code-block:: pycon
    
    #Traceback (most recent call last):
      File "code.py", line 122, in <module>
    MemoryError: memory allocation failed, allocating 4096 bytes
    

This happens when you have exhausted the available memory on your CircuitPython board. As discussed earlier, running Python on a microcontroller comes at a cost, and the biggest cost is reduced memory available for your programs.

This section covers some strategies that can help reduce your memory footprint.

The most prominent way to reduce memory usage is using less code, since lines of code are the biggest consumers of memory.

Note that the optimizations discussed here almost all put limitations on your code, and shouldn't be used without need, or careful consideration.

That brings up a really important point, and something that a lot of new programmers don't learn early enough: be careful not to fall into a common programming trap: *pre-emptive optimization*. 

Typically, you'll only need to optimize for memory consumption when you see the dreaded ``MemoryError`` exception. It can be stressful - you think you have completed your project, or found the perfect library to add the functionality you need and *wham*, you're out of memory. But resist the temptation to try to head this off by obsessing about memory consumption before you actually run out. 

Most of the time, its best to focus on finishing your project, not solving problems you don't have!

.. note::
   
   If you have other tips or tricks, or improvements to the techniques explored below, please `contact the author! <{filename}/pages/contact.rst>`__.
   
For comparison's sake, we're using the following code to test:

.. code-block:: python
    
    import time
    import gc
    from setup import led, rgb, check
    
    class State:
        def __init__(self):
            self.button = False
            self.led = False
            self.checkin = time.monotonic()
            
        def __call__(self):
            if self.button and not check("A"):
                if time.monotonic() - self.checkin >= 0.2:
                    self.button = False
                    self.checkin = time.monotonic()
                    print("Button pressed")
                
            if not self.button and check("A"):
                if time.monotonic() - self.checkin >= 0.05:
                    self.button = True
                    self.checkin = time.monotonic()
                    print("Button released")
                    
            if state.button:
                state.led = True
            else:
                state.led = False
    
    state = State()
    print(gc.mem_free())
    
    while True:
        state()
                
        if state.led:
            led.value = True
        else:
            led.value = False
            
On my GEMMA M0, it prints ``8944`` when it starts up. That's the number we'll be comparing other approaches to.

.. note::
   
   This is including our `setup.py module <{filename}/circuitpython-state-1.rst#Abstractions: Keeping The Code Simple>`__ - so we're also loading the DotStar library and setting up both buttons, even though neither are necessary for this code. 
   

Bear in mind though that these comparisons are just to ensure we're *actually* saving memory, it's not an evaluation of the effectiveness of a particular approach. The amount of savings and how significant it might be will entirely depend on your specific situation. 

Also keep in mind that memory is periodically cleaned up. Every so often the so-called "garbage collector" clears unused values and temporary variables from memory. So over time, the amount of memory you use can and will change. 

However, we don't have to think about that *too* much in our case, since our state objects will not typically change in a way that the garbage collector will affect - we're just replacing the initial values as the state changes. So checking the memory consumption at start up will give us an adequate amount of insight into how memory-intensive our state object might be.

Keeping An Eye On Memory Consumption
------------------------------------
We can use the ``gc`` module to tell us how much memory our project is using. The function we care about is ``gc.mem_free()``. 

This will be a fairly static value in most cases, so you can just print it before the main loop:

.. code-block:: python
    
    import gc
    
    ... 
    
    print(gc.mem_free())
    
    while True:
    ...
    

Use More Efficient Data Types (or: Don't Use A State Object |heartbreak|)
-------------------------------------------------------------------------
One of the more drastic, ways of slashing memory use is to switch from using an instance of a custom state class to using other data structures. Lets start with simple variables:

.. code-block:: python
    
    ﻿import time
    import gc
    from setup import led, rgb, check
    
    state_button = False
    state_led = False
    state_checkin = time.monotonic()
    
    print(gc.mem_free())
    
    while True:
        if state_button and not check("A"):
            if time.monotonic() - state_checkin >= 0.2:
                state_button = False
                state_checkin = time.monotonic()
                print("Button pressed")
    
        if not state_button and check("A"):
            if time.monotonic() - state_checkin >= 0.05:
                state_button = True
                state_checkin = time.monotonic()
                print("Button released")
    
        if state_button:
            state_led = True
        else:
            state_led = False
    
        if state_led:
            led.value = True
        else:
            led.value = False
            
This uses 9888 bytes of memory on my GEMMA. This approach gets messy quickly, but is still pretty easy to read.

Lets try a method that's a bit less readable but should save some memory: we'll use a single list to store our state:

.. code-block:: python
    
    import time
    import gc
    from setup import led, rgb, check
    
    #        button   led      checkin
    state = [False,   False,   time.monotonic()]
    
    print(gc.mem_free())
    
    while True:
        if state[0] and not check("A"):
            if time.monotonic() - state[2] >= 0.2:
                state[0] = False
                state[2] = time.monotonic()
                print("Button pressed")
    
        if not state[0] and check("A"):
            if time.monotonic() - state[2] >= 0.05:
                state[0] = True
                state[2] = time.monotonic()
                print("Button released")
    
        state[1] = state[0]
    
        if state[1]:
            led.value = True
        else:
            led.value = False

Using a list instead, my GEMMA reports 9984 bytes of free memory.

Here's what the same code looks like using a dictionary. It uses a tiny bit more memory, but it's quite a bit more readable:

.. code-block:: python
    
    import time
    import gc
    from setup import led, rgb, check
    
    state = {
        "button": False,
        "led": False,
        "checkin": time.monotonic()
    }
    
    print(gc.mem_free())
    
    while True:
        if state["button"] and not check("A"):
            if time.monotonic() - state["checkin"] >= 0.2:
                state["button"] = False
                state["checkin"] = time.monotonic()
                print("Button pressed")
    
        if not state["button"] and check("A"):
            if time.monotonic() - state["checkin"] >= 0.05:
                state["button"] = True
                state["checkin"] = time.monotonic()
                print("Button released")
            
        state["led"] = state["button"]
        
        if state["led"]:
            led.value = True
        else:
            led.value = False
            

The dictionary version leaves 9808 bytes of free RAM.

For simple state like this, using a dictionary is probably the best way to go. If other parts of your project are memory intensive, or you need to use a lot of heavy third-party libraries, it's better to use less elegant code to deal with state than detract from core functionality.

CircuitPython and Python-proper provide other data structures that *may* save some memory, depending on the circumstances. 

The one worth taking a look at is the ``array``. Python lists are dynamic - they can contain any kind of value: strings, integers, other lists, dictionaries, objects, anything. 

Arrays are different. The ``array.array`` class provides a more memory efficient kind of list that can only contain one type of data. 

Here's our same state code, refactored to use an array of *unsigned short integers*:

.. code-block:: python
    
    ﻿import time
    import gc
    import array
    from setup import led, rgb, check
    
    #                         button   led      checkin
    state = array.array("H", [0, 0, round(time.monotonic()*100)])
    
    print(gc.mem_free())
    
    while True:
        if state[0] and not check("A"):
            if round(time.monotonic()*100) - state[2] >= 20:
                state[0] = 0
                state[2] = round(time.monotonic()*100)
                print("Button pressed")
    
        if not state[0] and check("A"):
            if round(time.monotonic()*100) - state[2] >= 5:
                state[0] = 1
                state[2] = round(time.monotonic()*100)
                print("Button released")
    
        state[1] = state[0]
    
        if state[1]:
            led.value = True
        else:
            led.value = False
            
My GEMMA reports ``9760`` bytes of free memory. That's over 100 bytes *worse* than the dictionary version. However, some of that is due simply to the extra code brought in with the ``array`` module. The savings might add up with more complex projects, especially when tracking many more state values.

Finally, we can try using what's called a *bitmask*. This is mostly useful for storing boolean values - things that can be either ``True`` or ``False``. 

Bits are the building blocks of all data and logic in computing. A bit represents a single binary value - 1 or 0. This equates to true or false, on or off, up or down, etc. 

You can make larger number by arranging the 1's and 0's in sequence, just like decimal (base 10) numbers - except instead of using the numbers between 0 and 9, you can only use 0 or 1. 

For example, the decimal number **15** has a 1 in the "tens" place, and a 5 in the "ones" place. 15 is 10 + 5. 

The number 15 in binary is **1111**. There's a 1 in the ones place, a 1 in the *twos* place, a 1 in the *fours* place, and a 1 in the *eights* place. 1111 is 15, because 8 + 4 + 2 + 1 = 15.

.. tip::
   
   The nuances and amazing properties of the binary number system and doing binary math is beyond the scope of this article. 
   
   Here are a couple of videos worth checking out that explain things:
   
   **TBD: more/better explanations!!!**
   
   * `James May's Q&A (Ep 11100) <https://youtu.be/kcTwu6TFZ08>`__
   
You can treat a binary number like an array of switches, and using binary math, flip each switch (bit) on or off to indicate a true or false state. This way you can store 32 state values in a single 32-bit integer. One variable that takes up as much space as the number 15 can store up to *32 values*. 

.. note::
   
   The exact number of possible values depends on how Python is storing the number and the specific platform you are running on.
   
   It's also unclear if using the same number of variables with Python's booleans (``True``/``False``) is less efficient.
   

The basic technique is to use what's called a "bitwise and" operation (in python we use the ``&`` symbol) - you give it two numbers, and it will return a number where all of its bits are the product of a logical "and" - if a bit is 0 in the first number, and 0 in the second, that bit will be 0 in the result. If a bit is 1 in the first number, and 0 in the second, the bit will be 0 in the result. If a bit is 1 in the first number and 1 in the second, the bit will be 1 in the result. 

This ends up giving us a value that will be 0 if the bit we are interested in is 0, and something bigger than zero (depending on the location of the bit) if the bit is 1. This is something we can treat as a boolean value. It acts like a filter, giving us only the bits we have indicated as relevant in the second number.

Then, to change the bits (update our state), we use three different techniques:

#. We use the "exclusive or" (xor) bitwise operator ``^`` to "flip" a bit - given two numbers, the xor operator will return number where, if there's a 1 in a given position in both numbers, a 0 will be set, otherwise, 1 will be set. 
#. We use "bitwise or" (``|``) to *set* a specific bit. Given two numbers, bitwise or returns a number where, if there's a 1 in a given position in either number, a 1 will be set. If there's a 1 in both numbers, or a 0 in both numbers, a 0 will be set.
#. We use a combination of "bitwise and" and "bitwise negation" (``&`` and ``~``) to *unset* a specific bit. Negation will invert every bit (``0110`` becomes ``1001``), and bitwise and acts as our filter as explained earlier.

.. code-block:: python
    
    ﻿import time
    import gc
    from setup import led, rgb, check
    
    # 0b10 = button
    # 0b01 = led
    state = 0b00
    
    checkin = time.monotonic()
    
    print(gc.mem_free())
    
    while True:
        if not state & 0b10 and check("A"):
            if time.monotonic() - checkin >= 0.2:
                state = state ^ 0b10
                checkin = time.monotonic()
                print("Button pressed", state)
    
        if state & 0b10 and not check("A"):
            if time.monotonic() - checkin >= 0.05:
                state = state ^ 0b10
                checkin = time.monotonic()
                print("Button released", state)
        
        if state & 0b10:
            state = state | 0b01
        else:
            state = state & ~0b01
    
        if state & 0b01:
            led.value = True
        else:
            led.value = False
            
So this also doesn't seem to save us much memory. My GEMMA reports ﻿9872 bytes free. However this could be much more significant if we were tracking many, many boolean values.

Drop Features
-------------
Sometimes you will have to give up some functionality in order to work within the limitations of your platform. 

Start with the lowest priority features - the once you might call "nice to have". 

Sometimes you can change the project's scope, instead of dropping features. Try not to do too much. Remove unnecessary flexibility. 

An example: you have a component (a potentiometer or something) that lets the user control the brightness of an LED, and you're running out of memory. 

Some things to ask yourself: 

* Is it really necessary to control the brightness dynamically? 
* Could the brightness be controlled through some other means that would require less code? 
* Is the logic controlling it overly complex?
* Is it too user friendly?
* Am I using a library for the pot to function that I could implement differently?

Pre-calculate Values
--------------------
Using external libraries is a big source of extraneous code that can eat into our available memory. 

Sometimes we're using an external library just to calculate a value that doesn't change, or isn't based on anything that couldn't be reduced to a fixed set of values. 

Here's an example that flashes the RGB LED instead of the red one, changing the color every time. This version uses the `FancyLED <https://learn.adafruit.com/fancyled-library-for-circuitpython/overview>`__ library to do the math:

.. note::
   
   Make sure you have copied ``adafruit_fancyled`` folder to the ``lib`` directory on your CircuitPython board.
   

.. code-block:: python
    
    import board
    import time
    import gc
    from setup import led, rgb, check
    
    rgb.brightness = 1.0
    
    import random
    import adafruit_fancyled.adafruit_fancyled as fancy
    
    def random_color():
        return (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    
    class State:
        def __init__(self):
            self.brightness = 0.5
            self.button = False
            self.led = False
            self.checkin = time.monotonic()
            self.color = fancy.gamma_adjust(fancy.CRGB(255, 255, 255), brightness=self.brightness).pack()
    
        def __call__(self):
            if self.button and not check("A"):
                if time.monotonic() - self.checkin >= 0.2:
                    self.button = False
                    self.checkin = time.monotonic()
                    print("Button pressed")
    
            if not self.button and check("A"):
                if time.monotonic() - self.checkin >= 0.05:
                    self.button = True
                    self.checkin = time.monotonic()
                    self.color = fancy.gamma_adjust(fancy.CRGB(*random_color()), brightness=state.brightness).pack()
                    print("Button released")
    
            if state.button:
                state.led = True
            else:
                state.led = False
    
    state = State()
    print(gc.mem_free())
    
    while True:
        state()
    
        if state.led:
            rgb[0] = state.color
        else:
            rgb[0] = 0
            
So every time we press the button, we get a new, random, gamma-corrected color on our DotStar. 

But you will notice that the remaining RAM is pretty low, at 2752 bytes. 

How do we keep the same basic functionality while reducing our memory usage, using pre-calculation? 

First, lets reduce our scope a little bit. Do we really need *any* random color in the whole possible range? No, and in fact, most of the colors in the range are not super pretty or very bright, and a lot aren't that different from each other.

To solve that problem, lets establish a fixed set of colors we like, and only choose one of them at random.

.. code-block:: python
    
    # -- snip --
    
    colors =   ((255, 0, 0),      # red
                (226, 87, 30),    # orange-red
                (255, 127, 0),    # orange
                (255, 255, 0),    # yellow
                (0, 255, 0),      # green
                (150, 191, 51),   # blue-green
                (0, 0, 255),      # blue
                (75, 0, 130),     # indigo
                (139, 0, 255),    # violet
                (255, 255, 255))  # white
    
    def random_color():
        return random.choice(colors)
        
    # -- snip --
            
    
Now, we've limited ourselves to only 10 colors, but our available RAM has gone up to 4688 bytes, and we haven't even done any real pre-calculation yet!

Next, you may note that all FancyLED is doing for us is some math, and that math really won't change - the variables involved are our color and the brightness level, and all of those values are fixed.

So instead of doing those calculations on the fly, we can instead do them ahead of time, and eliminate the FancyLED library altogether. 

To precalculate the values, we can use a quick script that just prints them out for us:

.. code-block:: python
    
    import adafruit_fancyled.adafruit_fancyled as fancy
    
    brightness = 0.5
    
    colors = (
        ("white", fancy.gamma_adjust(fancy.CRGB(255, 255, 255), brightness=brightness).pack()),
        ("violet", fancy.gamma_adjust(fancy.CRGB(148, 0, 211), brightness=brightness).pack()),
        ("purple", fancy.gamma_adjust(fancy.CRGB(255, 0, 255), brightness=brightness).pack()),
        ("blue", fancy.gamma_adjust(fancy.CRGB(0, 0, 255), brightness=brightness).pack()),
        ("blue_green", fancy.gamma_adjust(fancy.CRGB(150, 191, 51), brightness=brightness).pack()),
        ("green", fancy.gamma_adjust(fancy.CRGB(0, 255, 0), brightness=brightness).pack()),
        ("red", fancy.gamma_adjust(fancy.CRGB(255, 0, 0), brightness=brightness).pack()),
        ("orange_red", fancy.gamma_adjust(fancy.CRGB(226, 87, 30), brightness=brightness).pack()),
        ("orange", fancy.gamma_adjust(fancy.CRGB(255,140,0), brightness=brightness).pack()),
        ("yellow", fancy.gamma_adjust(fancy.CRGB(255, 255, 0), brightness=brightness).pack())
    )
    print("colors = (")
    for color, value in colors:
        print("{:>10},    # {}".format(value, color))
    print(")")
    
Now we can run this on our board, and copy what we see in the console into our code. We can then remove the dependency on FancyLED.

.. code-block:: python
    
    import board
    import time
    import gc
    from setup import led, rgb, check
    
    rgb.brightness = 1.0
    
    import random
    import adafruit_fancyled.adafruit_fancyled as fancy
    
    colors = (
           8421504,    # white
           1900620,    # violet
           8388736,    # purple
               128,    # blue
           1980929,    # blue_green
             32768,    # green
           8388608,    # red
           6031104,    # orange_red
           8395008,    # orange
           8421376,    # yellow
    )
    
    def random_color():
        return random.choice(colors)
    
    class State:
        def __init__(self):
            self.brightness = 0.5
            self.button = False
            self.led = False
            self.checkin = time.monotonic()
            self.color = random.choice(colors)
    
        def __call__(self):
            if self.button and not check("A"):
                if time.monotonic() - self.checkin >= 0.2:
                    self.button = False
                    self.checkin = time.monotonic()
                    print("Button pressed")
    
            if not self.button and check("A"):
                if time.monotonic() - self.checkin >= 0.05:
                    self.button = True
                    self.checkin = time.monotonic()
                    self.color = random_color()
                    print("Button released")
    
            if state.button:
                state.led = True
            else:
                state.led = False
    
    state = State()
    print(gc.mem_free())
    
    while True:
        state()
    
        if state.led:
            rgb[0] = state.color
        else:
            rgb[0] = 0
            
This version of the code shows 8480 bytes free - a really big improvement. 

You can take this approach a lot further than you might think. Brightness is a factor in Fancy's gamma correction algorithm. Lets say your project lets the user adjust brightness. Instead of calculating the gamma on the fly, if you use a fixed set of brightness levels, you can precalculate every possible color/brightness combination, and store them in a list of tuples, or a tuple for every brightness level. 

It can seem like a lot of data, but tuples of integers are really compact.

.. tip::
   
   The `array module <https://circuitpython.readthedocs.io/en/3.x/docs/library/array.html>`__ can be used to even *more* efficiently store your precalculated values.
   

You will always have to balance memory used for lines of code verses memory used to store pre-calculated values, but it's a great way to save memory.

Compile Modules Into MPY Files
------------------------------
MicroPython provides a tool called ``mpy-cross`` that can take a python module and compile it into an intermediate form that takes up less memory. These files have the ``.mpy`` suffix.

Adafruit has just recently begun distributing a precompiled version of this tool with new versions of CircuitPython. 

To compile your code, you will first need to download the appropriate version of ``mpy-cross`` from `the distribution page <https://github.com/adafruit/circuitpython/releases/>`__, for both your operating system and the version of CircuitPython you are using. 

Place the tool in a directory in your ``$PATH``, or some place where you will be able to access it. You may need to make it executable (``chmod +x``). 

Once you have the tool, you will want to move some of your code into a separate module, and then import it into ``code.py``.

Given the example we've been using, you could break it up into the following files:

.. code-block:: python
    
    # save as state.py
    from setup import check
    import time
    
    import random
    
    colors = (
           8421504,    # white
           1900620,    # violet
           8388736,    # purple
               128,    # blue
           1980929,    # blue_green
             32768,    # green
           8388608,    # red
           6031104,    # orange_red
           8395008,    # orange
           8421376,    # yellow
    )
    
    def random_color():
        return random.choice(colors)
    
    class State:
        def __init__(self):
            self.brightness = 0.5
            self.button = False
            self.led = False
            self.checkin = time.monotonic()
            self.color = random.choice(colors)
    
        def __call__(self):
            if self.button and not check("A"):
                if time.monotonic() - self.checkin >= 0.2:
                    self.button = False
                    self.checkin = time.monotonic()
                    print("Button pressed")
    
            if not self.button and check("A"):
                if time.monotonic() - self.checkin >= 0.05:
                    self.button = True
                    self.checkin = time.monotonic()
                    self.color = random_color()
                    print("Button released")
    
            if self.button:
                self.led = True
            else:
                self.led = False
            
.. code-block:: python
    
    # save as code.py
    import board
    import time
    import gc
    from setup import led, rgb
    
    from state import State
    
    rgb.brightness = 1.0
    
    state = State()
    print(gc.mem_free())
    
    while True:
        state()
    
        if state.led:
            rgb[0] = state.color
        else:
            rgb[0] = 0
            

Be careful to import any necessary libraries in your new module. 

Next, you use the ``mpy-cross`` tool to convert your code into an mpy file. 

It's a good idea to set up a special working directory for this purpose, there isn't a tool to "decompile" the code, and you will want to delete the original module from your board. 

The process, in the terminal on a MacOS computer, looks like this:

.. code-block:: console
    
    $ mkdir ~/circuitpython-working
    $ cp /Volumes/CIRCUITPY/state.py ~/circuitpython-working
    $ cd ~/circuitpython-working
    $ mpy-cross state.py
    $ rm /Volumes/CIRCUITPY/state.py
    $ mv state.mpy /Volumes/CIRCUITPY/
    
Before compiling the module, ``gc.mem_free()`` returned 8160 bytes. After, it returns 8048. I'm not sure why this happened, I believe its because there are so many extra modules because of our ``setup.py`` abstraction to make working with multiple boards in the examples easier. 

You will typically see a difference, especially when compiling more complex code.

This is best saved for code that is really solid, since you can no longer edit the code right on your board.

Avoid Operations That Create Temporary Variables
------------------------------------------------
There are many places where Python will create a temporary variable. Temporary variables are used for only an instant, but can persist for a while before they are garbage collected. 

Further, if the temporary variable is large or complex, it can eat up a lot of memory.

A few common places we'll discuss here are *string addition* and *list slicing*. 

Strings are *immutable*, which means that they cannot be changed. String operations always return a new string, they never alter the string *in place*. 

There are several ways you can combine strings in Python.

.. code-block:: python
    
    import gc
    
    free = gc.mem_free()
    
    # string interpolation (classic way)
    print("memory free %d" % (free,))
    
    # format() method (newer way)
    print("memory free {}".format(free))
    
    # string addition
    print("memory free "+str(free))
    
    # multiple parameters to print()
    print("memory free", free)
    
The first two ways avoid excess memory issues. String addition creates an implicit temporary variable. It's worse here, since we also have to do a conversion ourselves from the int we have to a string.

I also included the last way, which isn't technically combining strings, but might not be obvious if you aren't familiar with modern Python: the ``print()`` function takes a variable number of arguments, and it will print each one separated by a space. 

The last version is the most memory efficient, especially if all your doing is printing some debugging text to the console. 

The NeoPixel library supports all of the fancy slicing and other special indexing capabilities of Python's ``list``. However, behind the scenes using those features can be memory intensive. 

Here's a simple "chaser" light display using all 10 NeoPixels on the CircuitPlayground Express, using slicing:

.. code-block:: python
    
    import board
    import time
    import neopixel 
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)
    rgb.brightness = 0.3
    
    import gc
    
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    while True:
        rgb[::2] = [white, white, white, white, white]
        rgb[::-2] = [black, black, black, black, black]
        rgb.show()
        time.sleep(0.2)
        rgb[::-2] = [white, white, white, white, white]
        rgb[::2] = [black, black, black, black, black]
        rgb.show()
        time.sleep(0.2)
        print(gc.mem_free())

The solution, if this becomes an issue, is to assign a color to each index  directly:

.. code-block:: python
    
    import board
    import time
    import neopixel 
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)
    rgb.brightness = 0.3
    
    import gc
    
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    while True:
        rgb[0] = white
        rgb[1] = black
        rgb[2] = white
        rgb[3] = black
        rgb[4] = white
        rgb[5] = black
        rgb[6] = white
        rgb[7] = black
        rgb[8] = white
        rgb[9] = black
        rgb.show()
        time.sleep(0.2)
        rgb[0] = black
        rgb[1] = white
        rgb[2] = black
        rgb[3] = white
        rgb[4] = black
        rgb[5] = white
        rgb[6] = black
        rgb[7] = white
        rgb[8] = black
        rgb[9] = white
        rgb.show()
        time.sleep(0.2)
        print(gc.mem_free())
        
.. note::
   
   While this fixed a memory issue I had in the past, I can't make sense of the readings I get from ``gc.mem_free()`` - the amount of available memory slowly winds down with each loop until the garbage collector runs and its recovered.
   
   This will require more research |thinking|.
   


Remove Debugging/Comments
-------------------------
Any line of code counts toward your memory count. Removing the two debugging print statements in the sample above saved 96 bytes of memory. 

This technique should be left as a final pass step, after you've exhausted other ideas and your code is solid. Most of the time you won't have your CircuitPython board connected to a computer, so printing to the console is useless. However, during development, or when debugging, console access is a necessity. Working around a few helpful debugging statements is worth it so you have the memory overhead available to make fixing a problem easier.

Offload To External Boards/ICs
------------------------------
Sometimes trying to do too much on one microcontroller is just *too much*. So finding another component, IC, or even another microcontroller to offload the work to is a very viable option.

A good example is audio. On the M0/M4 boards, it's possible to play 16-bit monaural audio samples. It's a great feature to have built-in. However, audio samples are large, and playing them takes up a lot of memory that you may need for other tasks.

Luckily, you can get sound boards like the Adafruit AudioFX series to play  audio clips by writing to digital pins - all the loading and DAC work is done by the sound board, and that frees up your main M0 board for other things.

There are other applications involving driving LEDs, controlling LCD displays, handling large amounts of NeoPixels, and so on. 

Frequently boards will communicate via I2C or SPI. You can implement those protocols yourself to get two M0 boards to talk to each other, sharing the load of your project. 

.. note::
   
   I hope to explore cross-board communication with I2C and SPI in depth in a future blog post!
   
   
Switch To Arduino
-----------------
Finally, there are times when your application is just too much for the CircuitPython platform. That's where the Arduino toolchain comes into play.

You can program your M0/M4 boards using the Arduino IDE just like any other compatible board. Most Arduino sketches will work without modification.

Adafruit has an `overview of the process <https://learn.adafruit.com/adafruit-feather-m0-basic-proto/using-with-arduino-ide>`__ of getting set up, as well as some `porting notes <https://learn.adafruit.com/adafruit-feather-m0-basic-proto/adapting-sketches-to-m0>`__ for running Arduino sketches on the M0/M4 series boards. 

.. note::
   
   The links above are in the documentation for a specific product, the `Feather M0 Basic Proto <https://www.adafruit.com/product/2772>`__, but they are completely generic. Sadly, they were the only docs the author could find at the time of writing. |heartbreak|
   
.. note::
   
   The author has not had a chance to do much with M0 boards and the Arduino IDE yet, but hopes to explore the topic thoroughly in a future blog post. A gentle `shout out <{filename}/pages/contact.rst>`__ might motivate him to do so sooner rather than later |winking|. 
   
   
Refactor State Logic Into Dispatcher
------------------------------------
* Instead of passing the event handlers as functions, we can instead implement them as overrides in a in herited class.
* Generalize the code even more - hard-code the event handlers inside of the ``ButtonDispatch`` class based on the token.

Use ints instead of strings
---------------------------
* instead of "BUTTON1", set BUTTON1 = 1

Use const()
-----------

