State And Events In CircuitPython: Part 4: Example Application
##############################################################
:date: 2018-06-11 15:07
:author: lionfacelemonface
:category: tutorial
:tags: tutorial; circuitpython; hardware; state;
:slug: circuitpython-state-part-4
:status: draft

.. include:: ../emojis.rst

Example Application: Blink Controller
=====================================

Now that we've established a pattern for working with state, and have a generic event dispatch class for button presses, we can build a more realistic application. 

This will illustrate how to use the ``ButtonDispatch`` class with your own variation of the ``State`` class to construct a project complex functionality with pretty simplistic code.

.. tip::
   
   An even more elaborate application can be explored in my `touch mouse project <{filename}/touchmouse.rst>`__ |mouse| !
   
We'll use the state object for more than just tracking button state. We'll also use it to handle general on/off, as well regular flashing of two LEDs: the built-in red LED on pin 13, and the onboard RGB NeoPixel or DotStar. We'll also track the color of the NeoPixel/DotStar. 

.. tip::
   
   This is the culmination of all the test and example code we've been using throughout this article. |unicorn|
   
   

Phase 1
-------
For a first pass, lets just control the red LED on pin 13. When the board boots, the LED will blink at a slow rate. If you press button A, the blink rate will increase. There will be 5 blink rates, and when you reach the fastest rate, pressing the A button again will reset back to the slowest one. 

The B button will enable/disable the LED, but won't affect the blink rate.

In our new ``State`` class, we'll be tracking the status of the LED, its current blink rate, whether the LED should be on or off (enabled), and the last time we flashed it. 

We'll be using the same technique to flash the LED that we use to debounce the buttons - stash the current value ``time.monotonic()`` in a variable, and every cycle compare that variable to the latest value. When enough time has elapsed, toggle the LED on or off, and update the variable.

We'll continue using the ``__call__()`` method to handle updating the state, but this time we'll be deciding whether the LED should be on or off based on the ``enabled`` attribute and the flashing logic outlined above.

We're going to make a slight change to the ``ButtonDispatcher`` class, to accommodate the fact that our state object is no longer a dictionary. We have to use the ``getattr()`` and ``setattr()`` functions to alter the state object. These functions let you access arbitrary attributes (properties) on an object, so we can use the ``token`` property to dynamically alter the state object.

We also changed from calling the button state slots "A-holding" and "B-holding" to "A_holding" and "B_holding", since dashes are not valid in attribute names in Python.

.. code-block:: python
    
    import time
    from setup import led, rgb, check
    
    class State:
        def __init__(self):
            self.A = False
            self.B = False
            self.A_holding = False
            self.B_holding = False
            self.led = False
            self.flash = 2
            self.last_flash = time.monotonic()
            self.enabled = True
    
        def __call__(self):
            if not self.enabled:
                self.led = False
                return
    
            if self.flash:
                if time.monotonic() - self.last_flash > self.flash:
                    self.led = not self.led
                    self.last_flash = time.monotonic()
            else:
                self.led = False
    
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
            return getattr(self._state, "{}_holding".format(self.token))
    
        @holding.setter
        def holding(self, value):
            setattr(self._state, "{}_holding".format(self.token), value)
        
        @property
        def state(self):
            return getattr(self._state, self.token)
        
        @state.setter
        def state(self, value):
            setattr(self._state, self.token, value)
        
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
    
    state = State()
    
    def value(token, state):
        return check(token)
    
    def increase_flash(state):
        state.flash -= 0.4
        if state.flash < 0:
            state.flash = 2
    
        print("Flash: ", state.flash)
    
    def release(token, state):
        if token == "A":
            increase_flash(state)
        if token == "B":
            state.enabled = not state.enabled
            ﻿print("Enabled? ", state.enabled)
    
    buttons = [
        ButtonDispatch("A", value, state, None, release),
        ButtonDispatch("B", value, state, None, release)
    ]
    
    while True:	
        for dispatch in buttons:
            dispatch()
            
        state()
    
        led.value = state.led
        
    
.. explanation::
    
    On **lines 4-25**, we have our *fully encapsulated* state class. This is very similar to what we've used in previous sections, except that it's tracking different things.
    
    Note the state attributes (**lines 6-13**):
    * ``A`` and ``B`` are the state of each button. These names come from the ``token`` that gets passed to the ``ButtonDispatch`` constructor.
    * ``A_holding`` and ``B_holding`` track whether the buttons are being held down. These names are also generated based on the ``token`` passed to the ``ButtonDispatch`` constructor. Note that these differ from the key names we used for the same purpose in the last example (``A-holding`` and ``B-holding``). We've replaced the dash (``-``) with an underscore (``_``) because dashes are not valid in variable names.
    * ``led`` tracks the state of the red LED on pin 13.
    * ``flash`` tracks the blinking rate of the red LED, in seconds. This is a *delay*, so larger numbers mean a slower blink/flash rate.
    * ``last_flash`` is our clock check-in attribute specifically for the flashing of the LED. This attribute is used in consort with ``flash`` to blink the LED at the set rate.
    * Finally, ``enabled`` tracks whether the LED should be blinking or not. It acts like an on/off switch, but it doesn't interrupt the flashing sequence - this is necessary because blinking the LED is really just turning it on and off - we need to be able to separately track turning the *whole sequence* on and off. 
    
    In ``__call__()`` (**lines 15-25**), we handle all of the logic necessary to blink the LED. 
    
    **Lines 16-18** handle the on/off state of the whole sequence. If ``enabled`` is ``False``, the method sets the ``led`` state to ``False`` and then *short circuits* - by calling ``return`` on **line 18**, the method immediately exits.
    
    Blinking is handled by **lines 20-25**. The logic is nearly identical to the button debouncing logic we've used before (and in fact, you will typically see similar blocking code to our original blocking debounce using ``time.sleep()`` in "getting started" projects that blink an LED). We check if enough time has passed. If it has, we toggle the LED: we use the ``not`` operator to negate the current state of the LED on **line 22**. We then reset by updating ``last_flash`` to the current value of ``time.monotonic()``.
    
    ``ButtonDispatch``, defined on **lines 27-113** has not changed from the last example, except to handle a class instance (object) instead of a dictionary. These changes happen on **lines 52, 56, 60, and 64**. We make use of the built-in Python functions ``getattr()`` and ``setattr()``. These functions allow us to access (``getattr()``) and store (``setattr()``) values on a class instance using a *string*. This allows us to create dynamic attributes, as we're doing here. We construct the attribute where we store the button state or holding status based on the ``token`` attribute of the ``ButtonDispatch`` instance.
    
    We have a generic *release* event handler, and a helper function that manipulates the state defined on **lines 120-132**. 
    
    ``increase_flash()`` looks at the state object and cycles through the various blink rates available. We've decided to flash between 2 and 0.4 seconds, in 0.4 second intervals - that equates to 5 distinct flashing rates. 
    
    Every time ``increase_flash()`` is called, it decreases the ``state.flash`` value by 0.4 seconds. If this value drops below 0, the function resets it back to the default, 2 seconds. 
    
    On **line 125**, we print the current value of the ``flash`` state attribute so we can see what's going on.
    
    We define our *release* event handler on **lines 127-132**. If the "A" button triggered the event, we call ``increase_flash()``. If the "B" button triggered the event, we turn on or off the blinking by toggling ``state.endabled``. Printing the current value of ``state.enabled`` on **line 132** helps us ensure something is happening. This is especially important with the enable/disable feature, since the LED blinking looks a lot like turning it on and off (well, because that's what blinking is |thinking| ). By printing to the console, we can be sure our event is firing and the state is changing the way we intend.
    
    Finally, **Lines 135 and 136** are worth noting because they show one way to bypass setting a certain event handler, by passing ``None`` for the ``press`` argument. Another way to do this would be with *keyword arguments*.
    
    Throughout this tutorial, we've been using *positional* arguments. We specify just the values when we call a function/method, and we *must* put them in the correct order. 
    
    Keyword arguments specify the name of the argument from the function/method definition, followed by an equals sign, and the value you want to set. By using them, you can skip optional arguments, and the order isn't important.
    
    You can mix the two, you just need to be sure to put the positional arguments *before* any keyword arguments.
    
    Here's a couple of other ways we could have instantiated the ``ButtonDispatch`` class for the "A" button:
    
    .. code-block:: python
       :linenos: none
       
       # using nothing but keyword arguments
       ButtonDispatch(token="A", check=value, state=state, release=release)
       
       # using a mixture - keyword arguments must come *after* positional ones
       # note how the order of keyword arguments doesn't matter.
       ButtonDispatch("A", value, release=release, state=state)
       
    

Here's the code in action on my Trinket M0:

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/blink-controller-demo-trinket-01.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/blink-controller-demo-trinket-01.mp4">link to the video</a> instead.</p>
       </video>
   </div>

Phase 2
-------

Now, lets add in the RGB LED and some more complex behavior. 

First, lets move our ``ButtonDispatch`` code into its own module. We'll do this for three reasons. 

#. It will make the code examples shorter. 
#. This code is stable so we shouldn't have to mess with it. 
#. We may run into memory issues and the easiest way to save some memory is to `compile this complex code into an MPY file <{filename}/circuitpython-state-5.rst#Compile Modules Into MPY Files>`__. 

We should get in the habit of doing this when we have well defined code, this is a great place to start. 

.. tip::
   
   Just bear in mind that if you do compile ``dispatch.py`` into an ``.mpy`` file, you won't be able to edit it directly (you'll have to edit it outside of your board, compile it, and copy it over again), so only do this when the code is *rock solid* and you need the extra memory. 
   

.. code-block:: python
    
    # save as dispatch.py
    import time
    
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
            return getattr(self._state, "{}_holding".format(self.token))
    
        @holding.setter
        def holding(self, value):
            setattr(self._state, "{}_holding".format(self.token), value)
        
        @property
        def state(self):
            return getattr(self._state, self.token)
        
        @state.setter
        def state(self, value):
            setattr(self._state, self.token, value)
        
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
    

For this phase, we'll just work in the state and activation logic for the RGB LED, and flash it right along with the red one on pin 13:

.. code-block:: python
    
    # save as code.py
    import time
    from setup import led, rgb, check
    from dispatch import ButtonDispatch
    
    class State:
        def __init__(self):
            self.A = False
            self.B = False
            self.A_holding = False
            self.B_holding = False
            self.led = False
            self.rgb = False
            self.led_flash = 2
            self.last_led_flash = time.monotonic()
            self.rgb_flash = 2
            self.last_rgb_flash = time.monotonic()
            self.rgb_color = (255, 255, 255)
            self.enabled = True
    
        def __call__(self):
            if not self.enabled:
                self.led = False
                self.rgb = False
                return
    
            if self.led_flash:
                if time.monotonic() - self.last_led_flash > self.led_flash:
                    self.led = not self.led
                    self.last_led_flash = time.monotonic()
            else:
                self.led = False
    
            if self.rgb_flash:
                if time.monotonic() - self.last_rgb_flash > self.rgb_flash:
                    self.rgb = not self.rgb
                    self.last_rgb_flash = time.monotonic()
            else:
                self.rgb = False
    
    state = State()
    
    def increase_flash(state, which="led"):
        if which == "rgb":
            state.rgb_flash -= 0.4
            if state.rgb_flash < 0:
                state.rgb_flash = 2
        else:
            state.led_flash -= 0.4
            if state.led_flash < 0:
                state.led_flash = 2
    
        print("LED Flash:", state.led_flash, "RGB Flash:", state.rgb_flash)
    
    def value(token, state):
        return check(token)
    
    def release(token, state):
        if token == "A":
            increase_flash(state, "rgb")
            increase_flash(state, "led")
        if token == "B":
            state.enabled = not state.enabled
            print("Enabled? ", state.enabled)
    
    
    buttons = [
        ButtonDispatch("A", value, state, None, release),
        ButtonDispatch("B", value, state, None, release)
    ]
    
    
    while True:	
        for dispatch in buttons:
            dispatch()
            
        state()
    
        led.value = state.led
        
        if state.rgb:
            rgb[0] = state.rgb_color
        else:
            rgb[0] = (0, 0, 0)
                
            
.. explanation::
    
    The logic here is identical as the last example, except we've duplicated the state attributes and on/off logic for the RGB led, and had to rename some things to differentiate between the two (``flash`` has become ``led_flash`` and ``rgb_flash``). 
    
    We've added ``rgb_color`` to the ``State`` class to track the color of the RGB led. This isn't used just yet, but will come in handy in the future.
    

            
A few noteworthy changes:

* We've added different state for both the RGB and red LED. This isn't necessary at this point. We're adding it in now in preparation for when we're controlling the blink rate of each LED independently.
* We're tracking the desired color of the RGB LED in our ``State`` class - this is not necessary at this point either, but this new state attribute will be used when we add color-changing functionality.
* We've altered ``increase_flash()`` to work for both LEDs by adding a new parameter, ``which`` - a string indicating which LED you want to adjust the flashing rate for.
* The standard red LED has two states, *on* and *off*. However, the DotStar/NeoPixel is actually 3 states, times the number of pixels: one each for Red, Green, and Blue. To turn it off, we can't just set it to ``False``, we instead have to write a "black" color - zero red, zero green, and zero blue.

Here's what that looks like running on my Trinket M0:
            
.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/blink-controller-demo-trinket-02.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/blink-controller-demo-trinket-02.mp4">link to the video</a> instead.</p>
       </video>
   </div>

Phase 3
-------

Next, we'll add in multiple-button logic similar to what we did previously and add a new feature to rotate through a set of predetermined colors when both buttons are pressed.

We'll make use of the `FancyLED library <https://learn.adafruit.com/fancyled-library-for-circuitpython/overview>`__ to gamma-correct the RGB LED so the colors look nicer. 

We'll also the brightness level, since we need it for the gamma-correction calculation.

.. note::
   
   Make sure you've copied the ``adafruit_fancyled`` library folder over to your ``CIRCUITPY`` drive. Place it in the ``lib`` folder.
   

.. code-block:: python
    
    import time
    from setup import led, rgb, check
    from dispatch import ButtonDispatch
    
    import adafruit_fancyled.adafruit_fancyled as fancy
    
    rgb.brightness = 1.0
    
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
    
    class State:
        def __init__(self):
            self.A = False
            self.B = False
            self.A_holding = False
            self.B_holding = False
            self.both = False
            
            self.led = False
            self.last_led_flash = time.monotonic()
            self.led_flash = 2
            
            self.rgb = False
            self.rgb_flash = 2
            self.last_rgb_flash = time.monotonic()
            
            self.rgb_color = (255, 255, 255)
            
            self._color_index = -1
            self.cycle_color()
            
            self.brightness = 0.5
            
            self.enabled = True
    
        def cycle_color(self):
            self._color_index += 1
    
            if self._color_index > len(colors)-1:
                self._color_index = 0
    
            self.rgb_color = colors[self._color_index]
    
        def __call__(self):
            if not self.enabled:
                self.led = False
                self.rgb = False
                return
    
            if self.led_flash:
                if time.monotonic() - self.last_led_flash > self.led_flash:
                    self.led = not self.led
                    self.last_led_flash = time.monotonic()
            else:
                self.led = False
    
            if self.rgb_flash:
                if time.monotonic() - self.last_rgb_flash > self.rgb_flash:
                    self.rgb = not self.rgb
                    self.last_rgb_flash = time.monotonic()
            else:
                self.rgb = False
    
    state = State()
    
    def value(token, state):
        return check(token)
    
    def increase_flash(state, which="led"):
        if which == "rgb":
            state.rgb_flash -= 0.4
            if state.rgb_flash < 0:
                state.rgb_flash = 2
        else:
            state.led_flash -= 0.4
            if state.led_flash < 0:
                state.led_flash = 2
    
        print("LED Flash:", state.led_flash, "RGB Flash:", state.rgb_flash)
    
    ﻿def hold(token, hold_count, state):
        print(token, "held. Count:", hold_count)
        
    def press(token, state):
        if state.A and state.B:
            state.both = True
            print("Both buttons are being pressed")
        elif not state.both:
            print(token, "button being pressed")
    
    def release(token, state):
        if not state.both:
            if token == "A" and not state.A_holding:
                increase_flash(state, "led")
            if token == "B":
                state.enabled = not state.enabled
                print("Enabled? ", state.enabled)
        else:
            if token == "B" and state.A_holding:
                increase_flash(state, "rgb")
                state.both = False
    
    buttons = [
        ButtonDispatch("A", value, state, press, release, hold),
        ButtonDispatch("B", value, state, press, release, hold)
    ]
    
    while True:	
        for dispatch in buttons:
            dispatch()
            
        state()
    
        led.value = state.led
        
        if state.rgb:
            rgb[0] = fancy.gamma_adjust(fancy.CRGB(*state.rgb_color), brightness=state.brightness).pack()
        else:
            rgb[0] = (0, 0, 0)   
            
.. explanation::
    
    We have a few new state attributes to deal with our new functionality.
    
    On **line 26**, we've introduced the state attribute ``both``, used to indicate when we've detected that both buttons have been pressed.
    
    On **line 7**, we've set the ``brightness`` attribute on the NeoPixel/DotStar object from our ``setup`` module to ``1.0``. These pixels are *bright*, so we normally won't use them at full brightness. However, setting the brightness to "full blast" here is necessary for getting the best results from the FancyLED library. 
    
    Note that this value must be a *float* - you will get somewhat odd errors if you set it to an integer (so be sure to set it to ``1.0`` not ``1``).
    
    We define our list of possible colors as a "tuple of tuples" on **lines 9-18**. Tuples work just like lists, except they are *immutable* - you can't change them once they're defined. This is perfect for our list of colors, since we have no need to change it.
    
    .. tip::
        
        The colors were chosen by searching for "RGB rainbow" and grabbing a few triplets that looked good. The exact colors could use some adjustment. If you try this code on different boards, you'll notice some variation between pixels, especially between DotStars and NeoPixels - this is expected. The electronics involved are different, and will produce slightly different wavelengths of light for each of the red, green, and blue elements. 
        
    We've added new state attributes to handle the cycling of colors on **lines 38 and 39**. 
    
    Brightness is now being tracked on **line 41**. This value could be defined outside of our ``State`` class, since we're not altering it in this project. However, a handy feature you could add would be allowing the user to change the brightness, and that would require keeping in the state object. 
    
    We have a new method defined on **lines  45-51**, ``cycle_color()``, that handles changing the state to the next color in the global tuple we defined on **lines 9-18**. 
    
    ``cycle_color()`` keeps track of which color was last used, by *index* (``_color_index``). To choose a color, it simply uses that attribute as the index of the ``colors`` tuple (**line 51**).
    
    ``_color_index`` defaults at -1 - this way, when ``cycle_color()`` is first called, it will start with the first member of the ``colors`` tuple (index 0). 
    
    To cycle to the next color, it just increments ``_color_index`` (**line 46**). To avoid increasing ``_color_index`` to a number higher than the highest index of ``colors``, and to start over at the first color,  ``cycle_color()`` uses a little bit of math (**line 48**): after incrementing ``_color_index``, it checks to see if it's higher than the length of the ``colors`` tuple *minus one*. Since tuple indexes start at 0, the highest index number is always the length of the tuple minus one (this is true for lists as well). We can add and remove colors to the ``colors`` tuple and ``cycle_color()`` will automatically adjust.
    
    In our event handlers (**lines 90-116**), we've added some logic to handle multiple button presses. We've also implemented a handler for the *hold* event (``hold()``, **lines 90-91**). This handler mostly serves for debugging purposes. We need to make sure that when we're pressing multiple buttons, the proper events are being triggered. Sometimes a *hold* might be triggered in error, and we need to see that.
    
    Our ``press()`` function is in charge of detecting when we're pressing *both* buttons. It's only function is to see if ``state.A`` and ``state.B`` are ``True`` (both buttons have been pressed), and change ``state.both`` to ``True``. We've added some debugging help by printing to the console if both buttons *weren't* pressed (**line 98**).
    
    ``release()`` is where all of the functionality of our LED blinker is really happening - **lines 101-105**, we detect when both buttons have been released. This occurs when ``state.both`` is ``True``, and ``state.A`` and ``state.B`` are both ``False``. So we've had a *press* event occur where both buttons were pressed, and now, both buttons are no longer pressed.
    When this occurs, we clear the ``state.both`` attribute by setting it to ``False``.
    
    But before clearing the ``state.both`` attribute, ``release()`` calls ``state.cycle_color()`` (**line 102**) so that the next time the RGB LED is turned on, it will use the next color in the ``colors`` tuple.
    
    **Lines 107-116** handle the actions that need to be taken when either a single button has been released, or both buttons have been released. 
    
    The main logic branch (**line 107**) depends on the value of ``state.both`` - if it's ``True`` (both buttons have been pressed), then the multi-button logic kicks in. If it's ``False``, then the single-button logic is evaluated.
    
    If both buttons are not being pressed (``state.both`` is ``False``), we first look at the ``token``. If it's "A", we check to be sure "A" isn't also being held down (``state.A_holding``, **line 108**). If that's the case, we take action, increasing the blink rate of the *LED*. This means that if you just press "A", it increases the blink rate of the red LED - this is the previous functionality of the "A" button. 
    
    If both buttons are not being pressed, and the button that triggered the event is "B" (``token == "B"``, **line 110**), we toggle the ``enabled`` state attribute (this is the also the functionality that just pressing "B" had in the last iteration). 
    
    If both buttons *are* being pressed (``state.both`` is ``True``, handled by the ``else`` statement on **line 113**), we then look to see which button has been released (which button triggered the *release* event). If it was the "B" button, and we're holding the "A" button (the ``token`` is "B" and ``state.A_holding`` is ``True``, **line 114**), we'll take action, increasing the blink rate of the *RGB led*. This is new functionality - if you hold down the "A" button, and press "B", it increases the RGB blink rate.
    
    The last thing that ``released()`` does in this branch of the logic, is clear the ``state.both`` attribute by setting it to ``False``. This prevents any more logic regarding both buttons from happening. We're essentially saying "it's cool, we've handled this particular event, everyone else stand down".  
    
    Finally, the other noteworthy change is that we've employed the FancyLED library to gamma-correct the RGB LED color (**line 132**) so it looks nicer, especially at lower brightness levels. To explain this line, lets refactor it into separate statements, using some intermediate, temporary variables:
    
    .. code-block:: python
    
        fancy_color = fancy.CRGB(*state.rgb_color)
        adjusted_fancy_color = fancy.gamma_adjust(fancy_color, brightness=state.brightness)
        
        rgb[0] = adjusted_fancy_color.pack()
        
    So first, we convert our ``rgb_color`` state attribute, stored as a 3-member tuple of (red, green, blue), into a ``CRGB`` object. ``CRGB`` is a class that FancyLED uses for its calculations. All operations in the library work on these objects. 
    
    The constructor for ``CRGB`` takes three arguments: ``red``, ``green``, and ``blue``, in that order. We use a nifty feature of Python called *argument unpacking* to expand our ``rgb_color`` tuple into three separate values, and pass them as the three required arguments that ``CRGB`` is expecting. Here's another way to look at it:
    
    .. code-block:: python
        
        red = state.rgb_color[0]
        green = state.rgb_color[1]
        blue = state.rfb_color[2]
        
        fancy_color = fancy.CRGB(red, green, blue)
        
    Once we have a ``CRGB`` object (``fancy_color``), we can do calculations on it. We pass that object to ``fancy.gamma_adjust()``, along with the brightness level we want. ``fancy.gamma_adjust()`` returns another ``CRGB`` object, which we've named ``adjusted_fancy_color``. 
    
    The NeoPixel and DotStar libraries don't understand ``CRGB`` objects, so we have to convert them to a form that the libraries can understand before setting our pixel to the adjusted color.
    
    There are a couple ways of accomplishing this. The first is to use the ``red``, ``green``, and ``blue`` attributes of the ``adjusted_fancy_color`` object to create a tuple:
    
    .. code-block:: python
        
        ... 
        
        adjusted_fancy_color = fancy.gamma_adjust(fancy_color, brightness=state.brightness)
        
        rgb[0] = (adjusted_fancy_color.red, adjusted_fancy_color.blue, adjusted_fancy_color.green)
        
    The NeoPixel and DotStar libraries can also take an *integer*, instead of a tuple. ``CRGB`` has a ``pack()`` method that will return a compatible integer. So we finally take advantage of that method when we set the pixel.
    
    In the example code, we're doing all of these steps in one line. Whether to do it this way, break it up, or vary the approach in the ways we've just explored is entirely up to you - rarely will one way or the other be any more or less efficient. It really comes down to readability, for the most part. 
    
    .. warning::
        
        This is 100% true in general, and most of the time in CircuitPython projects. But be cautious - every line of code takes up precious memory you may need for your project. Sometimes you may have to make things a little messy to squeeze in a few more bytes so you can get things working.  
       
    

.. note::
    
    If you are more experienced with Python, you may have thought that the ``cycle_color()`` method would be a great usecase for a *generator*.
    
    Generators are functions/methods that maintain some sort of state. Typically any variables defined inside of a function or method are lost when the it ends (or ``return``'s). A generator is different, in that it can be looped over, like a list or tuple (it's *iterable*), and as you loop over it, it calls your function each time, going back to the same point over and over, until it returns. That point is marked by using the special ``yeild`` keyword.
    
    Here's how a color cycling function might look, implemented as a generator:
    
    .. code-block:: python
        
        colors =   ((255, 0, 0),        # red
                    (226, 87, 30),      # orange-red
                    (255, 127, 0),      # orange
                    (255, 255, 0),      # yellow
                    (0, 255, 0),        # green
                    (150, 191, 51),     # blue-green
                    (0, 0, 255),        # blue
                    (75, 0, 130),       # indigo
                    (139, 0, 255),      # violet
                    (255, 255, 255))    # white
                    
        def cycle_colors():
            for color in colors:
                yield color
                    
        cycled_colors = cycle_colors()
                    
    We can use the built-in function ``next()`` to get the next color in the cycle, *for ever*. It will always start back at the beginning - once the colors have all been returned, the ``while`` loop starts the process all over again.
    
    Here's how it looks, interacting with it in the console:
    
    .. code-block:: pycon
        
        >>> next(cycled_colors)
        (255, 0, 0)
        >>> next(cycled_colors)
        (226, 87, 30)
        >>> next(cycled_colors)
        (255, 127, 0)
        >>> next(cycled_colors)
        (255, 255, 0)
        >>> next(cycled_colors)
        (0, 255, 0)
        >>> next(cycled_colors)
        (150, 191, 51)
        >>> next(cycled_colors)
        (0, 0, 255)
        >>> next(cycled_colors)
        (75, 0, 130)
        >>> next(cycled_colors)
        (139, 0, 255)
        >>> next(cycled_colors)
        (255, 255, 255)
        >>> next(cycled_colors)
        (255, 0, 0)
        >>> next(cycled_colors)
        (226, 87, 30)
        
    So why didn't we do it this way? It seems way more elegant, right? Well, this doesn't work well in CircuitPython |heartbreak| . I very quickly ran out of memory when I implemented the generator this way. There are many possible explanations for this, but I bring this all up because generators are *awesome* and you should learn about them, but more importantly, it's an illustration of where the limitations of the platform start to affect how you design and implement your projects.
    
    
This iteration brings the following notable changes:

* We've brought in logic to cover pressing both buttons. This required adding a handler for the *press* event, and the addition of the ``both`` state variable.
* The possible colors have been stored in a tuple of tuples called ``colors``.
* We're rotating through the colors using a method of the state object called ``cycle_color()``. It uses a new state variable, ``_color_index`` to keep track of the location within the ``color`` tuple of the color that was last used. ``cycle_color()`` resets ``_color_index`` to zero when it reaches the maximum index of ``colors``.
* We're using `FancyLED <https://learn.adafruit.com/fancyled-library-for-circuitpython/overview>`__ to adjust the colors to better reflect our expectations. It has a lot more functionality than that, we're just scratching the surface.

And the requisite video of this code in action on my Trinket M0:

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/blink-controller-demo-trinket-04.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/blink-controller-demo-trinket-04.mp4">link to the video</a> instead.</p>
       </video>
   </div>

Conclusion
----------
Now, we've added some very complex functionality to our project without having to write a lot of complex code. Further, we're not blocking to handle button debounce.

Ultimately, what we've learned here is a very useful *pattern* for writing embedded applications. Resist the urge to just grab the ``ButtonDispatch`` class and use it without thinking about your use case. Implement your own version that only does what you need.

The last section outlines strategies to deal with running out of memory. As discussed earlier, memory can be a scarce resource on the CircuitPython platform, and while we've constructed quite a slick, neat codebase, we've added a lot of code to the mix that will eat into our available memory. You will run into memory issues with CircuitPython, it's just a matter of time, but using state the way we have, abstracting it away into really nice classes, can make that happen a little sooner than if we hadn't. 
