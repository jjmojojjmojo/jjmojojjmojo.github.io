State And Events In CircuitPython: Part 3: State And Microcontrollers And Events (Oh My!)
#########################################################################################
:date: 2018-09-01 15:07
:author: jjmojojjmojo
:category: tutorial
:tags: tutorial; circuitpython; hardware; state;
:slug: circuitpython-state-part-3
:status: published

.. include:: ../emojis.rst

In this part of the series, we'll apply what we've learned about state to our simple `testing code from part one <{filename}/circuitpython-state-1.rst#testing>`__. 

Not only will we debounce some buttons *without blocking*, we'll use state to more efficiently control some LEDs.

We'll also explore what happens when state changes, and how we can take advantage of that to do even more complex things with very little code, using the magic of *event detection* |rainbow| .

All of this will be done in an object-oriented fashion, so we'll learn a lot about OOP as we go along.

.. PELICAN_END_SUMMARY

Revisiting Old Friends
======================

Lets start by applying state tracking to our `testing  code <{filename}/circuitpython-state-1.rst#testing>`__ from the first part of this series. 

For reference, here's one of the example circuits, using the Trinket M0 (see `the demo circuit section in part 1 <{filename}/circuitpython-state-1.rst#the-demo-circuit>`__ for references using other boards):

.. image:: {filename}/images/nonblocking-trinket-demo-circuit.png
   :width: 80%
   :align: center

We have two buttons, and two LEDs - one is the standard red LED on pin 13, the other is a built-in RGB LED, either a NeoPixel or DotStar.
   
Recall that to test our board, we set up a simple project that has the following functionality:

* While button "A" is pressed, the built-in red LED lights up.
* While button "B" is pressed, the built-in NeoPixel or DotStar lights up, in white.

We'll extend this a little bit and:

* Every time button "B" is pressed, the built-in RGB LED (NeoPixel or DotStar) will light up in a *different color*.

We can improve upon the code by building on the concepts of *state* we learned about in the `previous post <{filename}/circuitpython-state-2.rst>`__. We'll see that we can also use the same concepts to remove the blocking code, and add our new feature in an elegant way. |unicorn|

Lets start by refactoring our original code to work just as it did, but using state.

Here are the global state attributes we will need to track:

* the value of button "A"
* the value of button "B"
* should the LED be on or off?
* should the RGB LED be on or off?
* what color should the RGB LED be?

Since this is a first pass, let's start by simply using multiple variables to hold various state values.

.. tip::
    
    Remember this code is assuming you have created a ``setup.py`` file as explained `part 1 <{filename}/circuitpython-state-1.rst#abstractions-keeping-the-code-simple>`__.
    
    

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
    

Managing State: A Three-Phase Process
=====================================

Before we go much further, lets draw an important distinction. Unlike a physical scoreboard at a baseball stadium, which acts as part of the experience of watching the game, our state merely *reflects* our reality. 

The way we work with state is to alter it either *because* something happened (say, a button was pressed, much like scoring a point in a game), or to *cause* something to happen (this is different; like lighting up an LED, or changing a NeoPixel's color).

After some thought and experimentation, I've settled on a three-phase process for handling state in a microcontroller project.

Before we start (maybe this is phase 0, or -1? |thinking| ), we establish the *default* state. This is how we want things to look when the development board boots up. So buttons would be in the "unpressed" state (``False``), an LED might be initially "off", and so on. In the example code, we do this on **lines 11-15**.

Then, in the first phase, real life is *assessed* (checked, or read) - input pins are read, sensors are queried. The state objects are updated to reflect what was observed in real life. This is where we detect that a button has been pressed. In our code above, this is happening on **line 18 and 19**.

The second phase is strictly internal - no interactions with real life will happen. In this phase we *reconsider* the state. Did we read something in the first phase that indicates we need to take some sort of action? Is there cleanup or accounting that has to happen? This is where we would do that in our code. Most of the time, it means we'll be getting ready for the next phase, implementing logic like "if button A has been pressed, then the LED must be turned on". But instead of turning the LED on, we're just updating the LED's state object.

In the example above, this phase is happening on **lines 21 thru 29**. We look at the values stored in ``button_a_state`` and ``button_b_state`` and change the state variables for our LEDs, ``led_state`` and ``rgb_state`` accordingly.

The final pass *reconciles* the state object with reality. Our code looks at the state variables, and then causes any additional *side effects*. This is where we'll actually turn on the LEDs. In the example, this happens on **line 33-38**. 

.. note:: 
   
   In this case, and for our purposes, the side effects usually affect the physical state of our project (the LED lights up). But in programming, side effects can be anything, and usually affect other parts of our code or our data.
   
At that point we hit the end of the ``while`` loop, and start over again. 

Here's a diagram showing how it works:

.. image:: {filename}/images/nonblocking-state-flowchart.png
   :width: 80%
   :align: center

For our simple example, we could shortcut some of these steps. An obvious shortcut would be to directly set the value of the red LED to that of the "A" button: ``led.value = check("A")``. 

But it's important to keep the phases separate when we can. The phases represent logical ways to group code, and as we get more sophisticated, the separation will come in handy. 

Further, the phases are separated in terms of interacting with reality. This is important from a performance standpoint - reading from a sensor or writing to an output can be blocking sometimes. Keeping that code separate from our internal logic helps keep things moving smoothly. Changing variables is fast. If we mix these kinds of code up, we can get somewhat choppy interactions. 

There's a more pressing performance consideration however. It can be hard to visualize, but often the different phases will end up happening many cycles apart, not all at once, as it appears. By keeping the phases separate, we can do one phase, say assessing real life, in one cycle, and then 10 cycles later do the reconsideration phase, and it could be 100 cycles until we are able to reconcile with real life again.

We also incidentally end up separating multiple sub-phases: we'll read button "A" in one cycle, then 20 cycles later read button "B". We'll update state for button "B" 3 cycles later, and update the state for button "A" 30 cycles later.

*Inbetween all these gaps*, we are able to handle other state phases, and sub-phases. It all interleaves, sort of like the teeth in a zipper, or cars merging on a highway.

This all appears instantaneous for us, even giving the appearance of different lines of code running simultaneously, since cycles are millionths of a second long. 

An RGB LED Of A Different Color: Getting Classy
===============================================
Now that we have a clear pattern for working with state, lets add our new feature, and make the RGB LED change colors every time its pressed.

But first, lets refactor our code to use a class to manage state.

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
      :linenos: none
      
      >>> l = [1, 2, "three", 4, 6, 9]
      >>> l
      [1, 2, 'three', 4, 6, 9]
      >>> state = State()
      >>> state
      <Buttons: False/False, LED: False, RGB: False, Color: (255, 255, 255)>
      >>> state.rgb = True
      >>> state
      <Buttons: False/False, LED: False, RGB: True, Color: (255, 255, 255)>
        
   Here we illustrate the standard Python type behavior by creating and then evaluating a simple list, then instantiate our ``State`` class, evaluate it, change an attribute, and evaluate it again.
   
   It's a good practice to define ``__repr__()`` in your classes, as it helps when debugging.
   
   In our ``__repr__()`` method, we're using the ``.format()`` string method to insert instance values into our return value. 
   
   On **line 15**, we instantiate our ``State`` instance for use in our main loop.
   
   In our main loop on **lines 17-41**, the logic is exactly the same as before, except we are accessing attributes of our ``state`` object.
   

Interacting with the one ``state`` object is a lot cleaner than dealing with five separate variables. But what's really cool about using a class like this is that we can give our ``state`` object its own unique *functionality*.

Lets illustrate this by taking the "different" from our requirement of a "different color" quite literally. 

We'll add a method to the ``State`` class that generates a totally **random** color. 

The method will then assign it to the ``color`` state attribute.

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
   

Now, we can change the logic in our main loop to use the new ``State.random_color()`` method to generate a random color.

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
 
Using a method in this way keeps the state-related code with the state-related data. This is a good example of *encapsulation*. Since we have no other need to generate random colors, beyond changing our state, putting it in the class gets it out of the way of the rest of the main loop logic. 

This also helps preserve the separation of our phases working with state that we outlined above.

**A few notes:**

* With every loop, we call ``state.random_color()`` whenever the "B" button is not being pressed. This means the color of the pixel is always changing, even when the RGB pixel isn't illuminated. This is sub-optimal. We never want to do work when we don't have to. We'll address this situation in the next section when we start dealing with *events*.
* There's an added ``print()`` each time the state changes. This serves two purposes. First, it can be hard to see LEDs working in the video below, so I'll also demonstrate with a screen grab of `Mu's <https://codewith.mu/>`__ console. Second, there are times when we'll be doing things repetitively and not realize it. Remember how our code gets interleaved like cars merging? If we're triggering some action more often then we intend to, or in an unexpected order, it could be a bug. Calling ``print()`` will let us see this in the console, even if we can't see it in our hardware. 

Here's a video of this code running on my Trinket M0:

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/state-demo-trinket-01.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/state-demo-trinket-01.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

Before we move on, lets *refactor* our code yet again, but this time, just a little bit. Since ``State`` is our keeper of state for our project, lets move **all** of the code that changes state into to a method of the ``State`` class:

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

Note how simplistic our main loop is becoming. This is good! |unicorn| Since we've factored the work of updating the state object into the ``State`` class, it tidies things up a lot. Code that is concerned with state stays with the class, along with the state data. 

Our main loop can focus on things that are more relevant to the core functionality of our project - in this case, inspecting the state and affecting change in the real world (blinking the LEDs).

Another thing that using a class gives us, that we aren't taking advantage of just yet, is that we can now create multiple instances of the ``State`` class, and deal with multiple groups of similar state data, if we needed to. This will make more sense if we think about it in terms of encapsulating state and state methods for say, each button, or each LED - since we have more than one of each, we could have a new ``LEDState`` or ``ButtonState`` class that just deals with generic state for LEDs or buttons, and create an instance for each button and/or LED that we have.

.. tip::
    
    We will be doing something along these lines in a future installment of this series. Stay tuned!
    

Now that we've explored what state is, and looked at how we can write code to deal with it, we have opened ourselves up to some really neat possibilities. But since we're using ``time.sleep()``, our code is still *blocking*, and we're still limited by that. The next step is to utilize our new understanding of state to debounce our buttons *without* blocking.

Unblocking Our Debouncing: Using State To Avoid Blocking
========================================================
The next step is to get rid of that blocking code. This is another thing our ``State`` class can handle for us. 

As discussed earlier, the reason why we block is to keep our code from running too fast. This keeps our signals from our buttons smooth, avoiding bouncing.  

Another way to look at it is that we've introduced the passage of *time* into our main loop. We're fixing our code to run at an interval of 0.2 seconds, so we can wait until a button is completely pressed or released before we act, and so that our code won't run over and over without reason. 

Earlier we likened it to reducing the *sampling frequency* of our input - we're checking the state of the button every ``0.2`` seconds, instead of 45 million times every second. Blocking was a simple way to achive this. Its possible, however, to run the code *every* cycle, and count how much time has elapsed, *then* act when enough time has passed.

This is a textbook use case for the state concept we've been exploring. 

If we store some sort of time reference in our state object, when can then track the passage of time from cycle to cycle. It's okay that this code runs millions of times a second - we will inspect the state object every time (which is fast and doesn't block) and only act when enough time has passed (which is usually fast but could block sometimes - and the side effects might be bad).

In fact, this can give us much more granularity, and our code can be much more responsive, beyond not blocking - we're now working at the full resolution made possible by the processor. And the best part, we are able to perform tasks while we wait for the time to pass.

The State-Time Continuum
------------------------

The basic process is to first mark a starting time in our state object, and then, every loop, compare that mark to the current time - when we see that enough seconds (0.2 to match our blocking code) have passed, then we can act.

The time we last looked at the clock will be stored as a new state attribute. We'll use the methods of our state object to handle time-related calculations.

But maybe we're getting ahead of ourselves a bit. How exactly do we track passing time? Most microcontrollers don't have true built-in clocks like PCs.

Most computers have what's called a "`real-time clock <https://en.wikipedia.org/wiki/Real-time_clock>`__", or RTC. It's typically an integrated circuit that counts time in a highly accurate way using some sort of oscillating crystal. A battery is used to keep power to the IC so that it won't loose track of time, especially when the PC is powered off. 

While we can get microcontrollers with RTCs built in, and as add-on boards (Adafruit has several in their shop that have `CircuitPython support <https://learn.adafruit.com/adafruit-pcf8523-real-time-clock/rtc-with-circuitpython>`__), they are typically reserved for applications where "clock time" is necessary - for example, a digital alarm clock, or logging sensor data. 

.. tip::
    
    RTCs aren't the only way you can get precise time in an electronic device.
    
    * Cellphones can get the current time from the cell carrier. If you are using some kind of cellular modem in your project, you can ask it for the current date/time with a specific command.
    
    * Other GPS-enabled electronics can get the time from the GPS signal. Again, if you are using one of these modules in your project, you can get this information too.
    
    * If a device has internet access, it can calculate the current time via `NTP <https://en.wikipedia.org/wiki/Network_Time_Protocol>`__.
    
    * In most countries, there is a `radio broadcast that transmits the current time <https://en.wikipedia.org/wiki/Radio_clock>`__, often from a highly accurate source like an `atomic clock <https://en.wikipedia.org/wiki/Atomic_clock>`__. If you can find the right ICs (`it looks like you may have to salvage one from an old clock <https://www.kb6nu.com/how-to-build-a-wwvb-receiver/>`__) or figure out how to receive the signal, you can use it as a reliable clock source. Assuming `your government isn't like mine, trying to stop broadcasting it to save money <https://hackaday.com/2018/08/20/what-will-you-do-if-wwvb-goes-silent/>`__. |heartbreak|
    

Luckily, microcontrollers are in themselves actually a sort of clock, because they operate on a regular processor cycle.

The processor cycles are fixed to a specific rate. For example, our M0 board "clocks" at 48 megahertz (*48,000,000* cycles per second). That's because every second, the processor scans the part of its memory where your program code lives, and executes the instructions it finds *fourty-eight million times*. 

.. note::
   
   The chips in these CircuitPython boards, the ATSAMD21 and ATSAMD51, have a built-in *oscillator*. They have circuitry in the chips that can generate a regular pulse that can be used for clocking the processor. Not all microcontrollers have these. You'll often see a little oblong silver cylinder on the board (a `crystal oscillator <https://en.wikipedia.org/wiki/Crystal_oscillator>`__) - this is the real "clock" in that situation. 
   
   The processor runs at the frequency of the outboard oscillator. In the case of the M0/M4 chips, if you are building a development board, you can choose to use an external oscillator or choose one of several built-in to the chip. 
   

That cycle is very reliable, so it's possible to track it, and with some math, convert cycles to seconds passing over time. 

We could do this tracking and math ourselves, but there's a function in the ``time`` module that does exactly that. It's called ``time.monotonic()``. When called, it returns the number of seconds that have passed since the processor was turned on.

.. tip::
   
   Behind the scenes, CircuitPython is using so-called `timer interrupts <https://learn.adafruit.com/multi-tasking-the-arduino-part-2/timers>`__, features of microcontrollers where you can tell the processor to execute specific code blocks at regular intervals based on processor cycles.
   

``time.monotonic()`` returns a *float*, or `floating-point number <https://en.wikipedia.org/wiki/Floating-point_arithmetic>`__ - essentially a fraction, so it's ideal for our two-tenths-of-a-second debouncing rate. 

.. tip::
    
    The resolution of ``time.monotonic()`` in CircuitPython is somewhat variable and can vary from chip to chip - it's safe to assume hundreths of a second accuracy, but you might not get more than that. Keep that in mind.

Now, let's take advantage of this in our code. 

Making Time Work For Us
-----------------------

First, we'll need to add a new attribute to our ``State`` class. It will represent the last time we looked at the clock, or *checked in* with the processor. As such, we'll call it ``checkin``. 

We'll set the initial value of ``checkin`` to the value of ``time.monotonic()``. By doing this in the constructor (``__init__()``), we are calling ``time.monotonic()`` when we create the ``state`` instance from the ``State`` class. So the initial value of ``state.checkin`` will be the number of seconds from when the board was powered on, until that line of code is executed. It's a safe default that gives us something to compare to.

We'll look at ``checkin`` every loop, and see if the current value of ``time.monotonic()`` is at least 0.2 seconds larger - if this is true, it would mean that 0.2 seconds have elapsed. It's super simple and non-blocking.

At that point we can update our state - the reading from the button should be stable.

As a last step, we need to set ``checkin`` to the new value of ``time.monotonic()``, to mark the last time we checked the clock, and the cycle can start all over again.

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

This code handles debouncing our buttons and doesn't block. |unicorn| We keep things clean by letting the ``State`` class handle tracking the time.

Aside: Class Attributes And Privacy
-----------------------------------

In this iteration of the code, we've introduced a new concept beyond the addition of tracking time. Note the addition of a new variable in the class, defined outside of any methods, called ``_debounce`` (**line 6**). 

``_debounce`` is a *class attribute*, meaning that it belongs to the ``State`` class, and not to the instance object created from ``State``. We can access it from the instance (``self._debounce`` in our methods, or ``state._debounce`` in our main code).

By making ``_debounce`` a class attribute, we are indicating to anyone who uses our class that we don't intend for the value to be changed. However, if we were to change it, we would do so by accessing it as ``State._debounce``. What's really interesting is that changing ``State._debounce`` would change *all* of the instances of ``State`` too.

.. warning::
    
    If you *set* a class variable via the instance, Python thinks you are trying to make a new instance variable, and will essentially disconnect the instance's version of the class variable from the class.
    
    This is the expected behavior we're discussing above:
    
    .. code-block:: pycon
       :linenos: none
       
       >>> class Test:
       ...:    _class_attr = "X"
       ...:
       >>> inst1 = Test()
       >>> inst1._class_attr
       "X"
       >>> Test._class_attr = "Y"
       >>> inst1._class_attr
       "Y"
       >>> inst2 = Test()
       >>> inst2._class_attr
       "Y"
        
        
    This is what happens when you set a class attribute on an instance:
    
    .. code-block:: pycon
       :linenos: none
       
       >>> class Test:
       ...:    _class_attr = "X"
       ...:
       >>> inst1 = Test()
       >>> inst1._class_attr = "Y"
       >>> Test._class_attr
       "X"
       >>> inst1._class_attr
       "Y"
       >>> Test._class_attr = "Z"
       >>> inst1._class_attr
       "Y"
       >>> inst2 = Test()
       >>> inst2._class_attr
       "Z"
     
    This can cause very subtle bugs that are hard to track down. 

As noted in the warning above, there's some nuance to it, but generally speaking, we use class attributes like this when we want to set a value that will rarely, if ever, change. We're using it here like a configuration setting. You can change it in the code, or change it at runtime (``State._debounce = 0.1``, not ``state._debounce = 0.1``) and it will affect any instances of ``State`` that exist, or will be created after the change.

.. tip::
   
   `This post <https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide>`__ does a great job of explaining instance attributes and class attributes in great depth.
   

There's something else noteworthy about ``_debounce``. We've prefixed it with an *underscore*. This indicates that it should be considered a *private* attribute. This means the attribute is intended for use only within the class methods, and it's not to be accessed from outside. 

.. note::
   
   In Python, private attributes and methods are simply a *convention*. You shouldn't peek, but if you do, things will still work. The underscore is just a signal to other programmers that you don't intend the attribute to be used outside of the class.
   
   In other languages, this is not the case - an attribute declared private will not be accessible *at all* outside of the class - it's like it doesn't exist.
   
   Since the concept of "privacy" in Python is merely a convention, it's better to express it not as "hidden" or "forbidden", but more so "an attribute name that I can't promise won't change, so don't count on it being there". 
   
Demo And Conclusion
-------------------

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

Diving Into Events
==================

In order to avoid calling ``random_color()`` every single time we update our state, whether the "b" button was pressed or not, we need to decide when the best time to call ``random_color()`` is. For this example, we were calling ``random_color()`` when the button was unpressed because if we didn't, the color would change every 0.2 seconds that you held the button down (or constantly before we were tracking time). 

So when should we do it, to avoid calling ``random_color()`` too frequently?

Think about how a button, technically a "momentary switch", works. When you press it, the microcontroller pin reads "HIGH" until you remove your finger (or "release" the button). Then it reads "LOW". We can think about these situations as two separate *events* - **press** and **release**. 

* **Press** happens when the button changes from "LOW" to "HIGH" - it wasn't pressed, and now it is. 

* **Release** happens when the button changes from "HIGH" to "LOW" - it *was* pressed, and now *it isn't*. 

In Python, that means the *press* event happens when a pin's ``value`` attribute used to read ``False``, and now it reads ``True``. A *release* event happens when a pin's ``value`` used to read ``True`` and now it's ``False``. 

We know what the previous value was because we've stored in it our ``state`` object. We can use that to detect the change in state by just comparing the current real-life value with the last value we recorded in the state object.

The basic logic looks like this:

.. image:: {filename}/images/basic-button-event-logic.png
   :width: 80%
   :align: center

Now that we can act *only* when the button transitions from one state to the other, we can call ``random_color()`` in a more logical place, like right before we change the RGB pixel's state, when the button is pressed. We could also just do it when the button is released, more in line with the original logic. 

Here's our code again, with the ``random_color()`` call wrapped inside of logic that detects a *press* event:

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



    

.. tip::
    
    This shares a similarity to the time-tracking code we are using for button debounce: we're storing a state value at one point in time, and then comparing it to something that can change. With debounce, it was the elpased time, with our event detection, it's the state of the button.
    
We're now set up to handle even more events, like button holds, and double-clicks. Or even complex events involving multiple buttons (think chords on a piano or "ctrl-c" on a computer keyboard).

If you've done any programming in the past with GUIs, or front-end web application development, this concept may seem very familiar. It's similar to how mouse and keyboard events are handled in these environments. |thinking|

But don't be distracted by this! An event is not inherently tied to human interaction. An event can be *anything*. If a change in state can be detected, we can call it an event, and take action when it happens (or, we can *handle* the event). 

Imagine you have some environmental sensors. Say you can detect UV index, brightness of light, temperature, and relative humidity.

All of the following might be examples of events you could detect:

* The temperature increases by 10 degrees Fahrenheit. 
* The humidity drops by 20%.
* The humidity drops by 20% *over the course of one hour*. 
* The UV index is over 6 and the temperature is over 85 degrees Fahrenheit.
* There is very little light falling on the light sensor - *it's probably night time*.
* It was nighttime, but now it's not, *it's probably sunrise*. 

And you could probably think of a lot more! 

All of these events would be handled by some code: change the color of a status LED, write a log message, send an SMS reminding you to put on some sunscreen, put the CPU into "low power" mode, and so on. If you can detect the event, based on changes in state, you can handle it, taking necessary action.

You gain a lot of insight when you start to look at coding a microcontroller project as a problem of *managing state*. Then you can think about changes in state as triggering *events*. You can *handle* those events with code. Very complex problems become very easy to reason about, and easier to debug.

State: Considerations
=====================
There are many benefits to modeling our project code around state:

* We have ultimate flexibility. When it comes to debouncing buttons or otherwise detecting events, we can avoid blocking. Generally speaking, managing state lets us decide what data we care about, and we can define our own events based on what's important to our project.
* We can separate our concerns. Instead of mixing complex logic and interacting with components and peripherals, we can do one, then the other. This makes our code cleaner, less bug prone, and better performing.
* We have good transparency. By looking at the class definition, it's obvious what data we care about. 
* At the same time, we can treat state objects as if they were *opaque*. We can interact with them without being concerned about the fine details about how events are detected or data is stored.
* The code can be factored in such a way that it is very simple to reason about. With a few rules attached to the state variables, we can condense a complex series of if/else statements into just a few that are easy to wrap our heads around.
* Events become possible to detect, since we're tracking state over time.

This is all great, but there are some drawbacks:

* We will ultimately end up using more memory. This isn't too big of a concern on a beefy platform like the M0/M4 boards, but we still have limits to how much memory we can use and have to remain conscious of this. 

  This is especially true for CircuitPython and hobbyists like us - we will often rely heavily on 3rd party libraries, and every line of code we add to our project eats up a small amount of memory.

  .. tip::
     
     There is an excellent article series over on `Hackaday <https://hackaday.com/2015/12/09/embed-with-elliot-debounce-your-noisy-buttons-part-i/>`__ that covers debouncing in depth and illustrates a solution for the Arduino platform that is *extremely* memory efficient. Something like this could be adapted to CircuitPython if our state keeping variable got to be too memory intensive.
     
  .. note::
      
      We will be covering techniques for reducing our memory footprint at the end of this series. Stay tuned!
  

* The timing is likely to be *ever-so-slightly* inaccurate. While processor cycles are very consistent, counting them tends to be less accurate over time (this is called "clock drift"). This is aggravated by the math being done - counting millions of cycles, dividing that by seconds, then rounding will cause further errors over time.
* There can still be blocking code, and aspects of Python (like `the GIL <https://wiki.python.org/moin/GlobalInterpreterLock>`__) that can further throw off your timing, especially when your code is running for long periods of time (days). 
* The precision of ``time.monotonic()`` is pretty shallow compared to the counters that CircuitPython uses behind the scenes to calculate it. Its typically only going to give you precision to hundredths of a second. Perfectly adequate for our purposes, but it could become an issue in some contexts (video games, for example).

So there are things to be concerned about, but nothing that detracts from the utility of this approach.

.. tip::
    
    At the time of writing, there is an `open issue <https://github.com/adafruit/circuitpython/issues/519>`__ addressing the inaccuracy of ``time.monotonic()`` in the CircuitPython github with a promising pull request attached. Worth keeping an eye on, and here's hoping that it gets more attention.
    
    
Conclusions And What's Next
===========================
So, now we know what a great tool state is, and how to wield it like a pro.

And building on that, we've explored the fundamentals of events, and we can think about things like pressing a button as a series of state changes. We can detect these changes and take action.

As a side effect, we've also gotten a pretty good introductory overview of object-oriented programming, and how to use it in Python. I feel a bit sneaky |grin|. Usually, OOP introductions are hardly practical, and it's really cool that we're able to do something real thanks to this awesome platform we have! |sparkleheart|

In the next installment, we'll take this approach further. We'll create an easy-to-use class that will track button state and handle event detection for us. We'll do some more cool things with OOP Python, and adapt this new class to our test code, in preparation for building the more complex project described in `part 1 <{filename}/circuitpython-state-1.rst>`__.
