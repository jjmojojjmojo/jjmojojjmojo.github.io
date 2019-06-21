State And Events In CircuitPython: Part 4: Polymorphism And Analog Events
#########################################################################
:date: 2018-06-11 15:07
:author: jjmojojjmojo
:category: tutorial
:tags: circuitpython; python; hardware; state;
:slug: circuitpython-state-part-4
:status: draft

.. include:: ../emojis.rst

This is the **fourth** part of a multi-part series exploring the concept of state, what it can do for you (like non-blocking button debounce) and how to track it in CircuitPython.

In this part, we explore tracking state for analog inputs, and dig into more object-oriented features, particularly *polymorphism*: method overriding, and class inheritance.

As a bonus, we'll explore a few interesting things about *voltage dividers*, a super useful electronic circuit. |unicorn|

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

.. image:: {static}/images/nonblocking-state-flowchart.png
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

| An **event** is when state changes over time. We can **handle** events with code.

State will change over time. We can detect those changes and take action. We call those changes *events* and when we take action, we refer to it as *handling an event*.

We talked about events in terms of buttons: *press*, *release*, *hold*, but we also made it a point to talk about how any change in state can be an event: changes in readings from a sensor, changes in the time of day, and changes to multiple state attributes. What constitutes an event can be very complex.

An Expanded Demo Circuit
========================
We're going to be working with buttons and built-in LEDs, but in the next section we're going to be exploring events using other kinds of sensors, namely a *thermistor* and a *photocell* (technically a *photoresistor*). 

The CircuitPlayground Express already has both sensors built in:

**TODO: Picture of the CPX's sensors here**

For the other boards, we'll need to add the new sensors to our existing demo circuit. We'll use a standard epoxy-coated *thermistor*, and a CdS-type *photoresistor* (aka photocell). We'll also need a resistor for each one. 

I bought these components from the Adafruit shop. Any comparable thermistor and photoresistor (photocell) should work. You may just need to use different values in the software, and/or use different companion resistors when you wire them up.

We're also going to do a simple `voltage divider circuit <https://en.wikipedia.org/wiki/Voltage_divider>`__. It's optional, since it's just for demonstration, but recommended. 

Here's a parts list:
    
    * Materials from the `first installment <{filename}/circuitpython-state-part-1.rst#materials>`__.
    * A CdS-type photocell.
    * A 10K 3950 NTC thermistor.
    * A 10K ohm resistor for the thermistor.
    * A 10K ohm resistor for the photocell.
    
If you choose to build the demo voltage divider:
    
    * An extra breadboard for the voltage divider circuit.
    * A multimeter that can read voltage.
    * Two additional 10K ohm resistors for the voltage divider (you can reuse the ones from the main parts list).
    
If you are using a GEMMA M0, you'll need a few extra components, since it doesn't have enough inputs to support two buttons and two analog sensors:

    * 1 22k ohm resistor
    * 1 2k ohm resistor
    * An additional 10K ohm resistor.
    
I've put together a `wishlist @ Adafruit <https://www.adafruit.com/wishlists/472992>`__ with everything new that you will need.

.. note::
    
    |thinking| Here are some notes about why I chose these particular sensors, and why we're introducing them at this point in the series:
    
    * I want to explore tracking something in state besides boolean (``True``/``False``) values. These analog sensors produce a steady stream of data, and so they are great for this. There's a really good chance you will get variations with every read, and it helps illustrate how using our state model to control the sampling rate helps make a more stable project.
    * It's a good idea to get comfortable with using analog devices - we live in an analog world, after all! (although some folks prefer to spell it *analouge* |grin| ). There are so many applications for analog sensors, from audio and radio signal processing, proximity detection, to light, temperature and moisture sensing, and things I haven't even thought about yet. 
    * Analog devices tend to be simpler, so they're easier to reason about. When you use a digital version of a sensor, a lot of the electronics are hidden from you. This is great when you want a simple solution, but you won't learn as much, and so I like that using these devices forces us to think about basic electronics and practice our electronic theory a little bit.
    * Both sensors are built-in to the CircuitPlayground Express, so they're already available if you are using that board (and that is still **highly recommended** |sparkleheart| )
    * If you aren't using the CircuitPlayground Express, as we'll see in the demo circuits below, they are cheap, easy to obtain, and simple to wire up.
    * Both kinds of sensors have good documentation and support in CircuitPython. There's even a nice `library <https://circuitpython.readthedocs.io/projects/thermistor/en/latest/api.html>`__ for reading thermistors available.
    * The two sensors we're using are similar in that they're both resistive components, yet they work with different values and have different levels of sensitivity. This is good to help drive home the core ideas about state and how we can generalize our thinking of it to write better code. |unicorn|
    * Finally, in this part of the series, we're going to explore some more object-oriented concepts, chiefly *polymorphism*. It's helpful to see how we can consolidate code for many different kinds of inputs into a single base class (lots more on that in the next section!). So having lots of similar, yet different components helps to explain, in practical terms, these somewhat obtuse concepts.
    
Our New Sensors: The Basics
---------------------------
As mentioned, these components are *resistive*: their resistance changes as the thing they are sensing (heat, light), changes.

.. tip::
    
    For in-depth discussion about how to use and test these components, check out the following tutorials:
    
    * `CdS Cells, Photoresistors, & Light Dependent Resistors (LDR) <https://learn.adafruit.com/photocells/overview>`__
    * `Thermistor - Measure temperature using a resistor! <https://learn.adafruit.com/thermistor/>`__
    


We use the variable resistance to measure how much light or heat we're detecting. We can't detect variable resistance with our microcontrollers. We can, however, detect variable **voltage**. Resistors act to limit voltage. If we connect our variable resistor (thermistor, photocell) to a known voltage, as the resistance of the sensor changes, so will the voltage running through it. The voltage will vary in a consistent way, directly in line with the resistance of the sensor, as it reacts to whatever is stimulating it (again, heat or light). To read a variable voltage, we can use an analog input. Our M0/M4 boards allow us to configure analog inputs on *any pin*. So we have plenty of pins to work with.

There is one other component we need to make this work: a *fixed* resistor (also known as "a regular garden-variety resistor"). The two resistors act in consort to provide a consistent voltage to our analog input.

When you use two resistors in this manner, you create what's called a *voltage divider*. This is a special circuit that uses resistance to lower an input voltage. Typically, they aren't variable, and are used when you need to lower the voltage coming from (usually) a foreign source, or sending a signal to one. For example, in the recent past, I've used them to read a 5 volt signal (I needed to drop it down to less than 3.3 volts so my M0 board wouldn't be damaged by it) from an ultrasonic range finder, and to send a 1.5 volt signal to the "hot shoe" on a camera so it would know my project was connected to it. They are a very useful and simple circuit! |unicorn|


.. tip::
    
    Sparkfun has a great `voltage divider tutorial <https://learn.sparkfun.com/tutorials/voltage-dividers/all>`__ if you'd like to dig into the theory and math behind this. 
    

A basic voltage divider consists of an input voltage, and two resistors. One is tied to ground, the other to the input voltage, and if you tap into the circuit between the two, you will get a voltage relative to the resistance of the two resistors. 

To illustrate this, lets build a quick voltage divider and show the voltage changing by using a multimeter.

Here's the circuit, using one of my Trinket M0's as a power source:

**TODO: Photo of voltage divider circuit using the trinket M0**

You can see that we've got one 10K resistor going to ground, and the other going to the positive voltage rail. We've connected the power rails to the ``usb`` pin, which gives us 5 volts from the USB port. I've chosen to use this power supply because when you use 2 10K resistors with 5 volts, you will get about 2.5 volts from your divider. It's a nice demonstration of literally dividing the voltage in half. It's also useful for reading 5 volt inputs on 3.3 volt boards, so it's nice to have in your repertoire.

.. tip::
    
    This particular circuit, using 2 10K resistors is a useful setup if you have to read from a 5 volt sensor on a 3.3 volt input, like the ones in our M0/M4 boards. 2.5 volts low enough to protect the microcontroller from damage, but high enough for the microcontroller to detect. Most older components, and most things built for Arduino, will communicate in 5 volt bursts.
    
    The voltage used for communication is referred to as the *logic level*. Most Arduinos have a *5 volt logic level*, and our CircuitPython boards have a *3.3 volt logic level*.
    
    A voltage divider is the simplest way to be able to use sensors with 5-volt logic on our 3.3 volt boards. 
    
    We can also use integrated circuits called "logic level shifters" to do the same thing. 
    
    Both approaches have their use cases. Sparkfun has a `nice overview <https://learn.sparkfun.com/tutorials/logic-levels/all>`__ of the science behind these terms.
    
    
.. note::
    
    We're using the Trinket M0 for this, but we're *only* using its power regulator. Any 5v power supply would work, just note that the pin may be marked ``vout`` on some of the M0 boards like the CircuitPlayground Express and GEMMA M0. 
    
    **TODO: photo of the Vout pads on the GEMMA and CPX**
    
    The power regulators in these Adafruit boards are very good, but you may want to use a separate power supply to reduce the risk of damaging your boards when you are experimenting with circuits like this.
    
    A *bench-top power supply* would probably be ideal, but I have had a good experience using one of these "breadboard power supplies" that came in a kit I picked up from Amazon.com:
    
    **TODO: photo of the breadboard power supply**
    
    For most projects, you'll want a power supply that provides 5 and 3.3 volts at a minimum. 12v, 9v, and other arbitrary voltages are useful as well, but 5 and 3.3 are the most common needed for microcontroller work.
    
We'll need to set our multimeter to the "voltage" setting, and unless you have an "auto-ranging" multimeter, you'll have to choose a scale that 2.5-5 volts will fit within. On mine, it's the ``20`` mark:

**TODO: photo of settings on the multimeter**

.. tip::
    
    If you are new to multimeters, Adafruit has a `nice tutorial <https://learn.adafruit.com/multimeters/>`__ you should check out.
    
    
Now, lets test the power rails to make sure we know our starting voltage is correct. Make sure your board is plugged in to a USB port (computer or wall adapter will work). Then place the black, negative probe on the blue negative rail, and the red, positive probe on the red, positive rail, like this:

**TODO: photo of multimeter probes on the breadboard. Closeup of output**

The meter should read somewhere around 5 volts. If it doesn't, try changing the range and double-checking your wiring.

Now, if we keep the black, negative probe on the negative rail, and poke the red, positive probe into the breadboard between the resistors, the meter will read around 2.5 volts. 

**TODO: photo of multimeter probes, and closeup of output showing 2.5**

We've built a working voltage divider! |unicorn| As a bonus, we got some experience with the multimeter, and now know how to verify our wiring for our new sensors. 

As such, we're now ready to wire up our new components.

ItstyBitsy M0 Express
---------------------
The ItsyBitsy has a wealth of pins available, so we can easily wire up our original buttons from the first demo circuit, and the two new components. Since we're building onto the previous demo circuit, I've cut jumper wires from solid-core wire to hook things up:

**TODO: photo of the itsybitsy m0 express with the new components**

Trinket M0
----------
The Trinket M0 has a few less pins, but enough for all of the components we're using. As before, I'll use pre-made flexible jumper cables to make the connections. You can really see the trade-offs in using them exclusively on a project that is this complex.

**TODO: photo of the trinket m0 with new components**

GEMMA M0
--------
Being a super compact board, the GEMMA doesn't have enough pins (pads) for us to wire up both sensors and both buttons. We've only got three pins available in total. Any of them can be analog or digital inputs, but we will need four inputs for both buttons and sensors. 

We could use something like the `Adafruit SeeSaw <https://learn.adafruit.com/adafruit-seesaw-atsamd09-breakout>`__, or any other sort of I2C port expander - the GEMMA supports I2C pretty well, just bear in mind that using I2C means giving up two pins, so whatver you choose has to provide whatever sort of inputs you need (in our case, something like the SeeSaw is ideal because it gives us enough analog *and* digital pins for our project). 

Since we've been doing a lot with resistors, and any of the GEMMA's pads can be analog inputs, lets take advantage of that to "multiplex" a single analog input with both of our buttons. Then we'll have the other two pins to use for the thermistor and photocell. 

By wiring both buttons to the same analog pin, but using a resistor of a different value for each one, we will get a different, and consistent, reading depending on which button is pressed. We should also get (close to) a 0 reading if neither button is pressed. 

.. tip::
    
    |thinking| Guess what? This is another application of a **voltage divider**!! |unicorn|
    

Because this is a voltage divider, we'll need a second resistor in the circuit. We'll use a 10K ohm resistor, since we probably already have a handful.

The other two resistors just need to be different, and large enough that, in combination with the 10K resistor, they will produce a voltage we can anticipate. 

The analog-to-digital converter (ADC) in our M0 chip is very precise, so we can detect small changes in voltage. However, we will want the values to be pretty different so it will be easy to tell them apart.

.. tip::
    
    You can use an online `voltage divider circuit calculator <http://www.ohmslawcalculator.com/voltage-divider-calculator>`__ to figure out what resistors to use. Start with what you have on hand, and input various values until you come up with something that looks reasonable.
    
I chose to use a 22k resistor for button "A", and a 2k resistor for button "B". 

Here's what the new wiring looks like:

**TODO: photo of the GEMMA button multiplexer setup**

To do basic testing of our 'multiplexed' button, we'll just print the current voltage of the input pin (in the circuit above, we've used ``A0``):

.. code-block:: python
    
    import time
    import board
    ﻿from analogio import AnalogIn
    
    ﻿buttons = AnalogIn(board.A0)
    
    ﻿def getVoltage(pin):
        return round((pin.value * 3.3) / 65536, 1)
        
    ﻿while True:
        print(getVoltage(buttons))
        
        time.sleep(0.2)
        
**TODO: video of the button test code in action**
        
You can see how stable the input voltage is (note that the use of ``round()`` helps smooth out some of the minor variations). 

In order to tell if one of our buttons is pressed, we just need to compare the voltage of the pin against the output we see in the console.

A New External Library: adafruit_thermistor
===========================================

Updating Our Abstraction Library
================================
Now we have even more variance between our development boards. This is where the utility of the abstraction module we built, ``setup.py`` starts to really become apparent.

GEMMA M0
--------
Because we've taken advantage of voltage dividers to 'multiplex' the buttons onto a single analog input, our ``setup.py`` has to make some fairly substantial changes:

.. code-block:: python
    
    ﻿# save as setup.py
    import board
    from digitalio import DigitalInOut, Direction, Pull
    import adafruit_dotstar
    import analogio
    import adafruit_thermistor
    
    thermistor = adafruit_thermistor.Thermistor(board.A1, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)
    photocell = analogio.AnalogIn(board.A2)
    
    led = DigitalInOut(board.D13)
    led.direction = Direction.OUTPUT
    
    rgb = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
    rgb.brightness = 0.3
    
    buttons = analogio.AnalogIn(board.A0)
    
    def getVoltage(pin):  # helper
        return round((pin.value * 3.3) / 65536, 2)
    
    def check(token):
        print(getVoltage(buttons))
        if token == "A" and abs(getVoltage(buttons) - 1.0) < 0.1:
            return True
            
        if token == "B" and abs(getVoltage(buttons) - 2.8) < 0.1:
            return True
        
        return False  
    

The exact voltage amount can vary a little bit from press to press of the buttons, so we've added a threshold - if the voltage is within 0.1 volts, we consider that "pressed".

This is a really great example of the power of abstraction! Any code we have already written that uses the ``check()`` function will still work without *any* modification, even though the wiring and code is radically different.

.. tip::
    
    There are two parts of our original API that we've lost here, ``button_a`` and ``button_b``. 
    
    None of the code in this tutorial series uses those objects directly, but if you happen to have written some that does, this change *breaks the API*. 
    
    Essentially, we've violated the contract by not including those two objects. |heartbreak|
    
    For the sake of this project, it's not a big deal. As I mentioned earlier, the two missing objects are not used directly. For the sake of this tutorial, we can just ignore this issue.
    
    However, it's good practice to fix issues like this so don't confuse anyone (other people using your code, or your future self!). We have three primary options:
    
    #. We can `retcon <https://en.wikipedia.org/wiki/Retroactive_continuity>`__ the API, or *retroactively change the documentation so it's as if these objects never existed*. I'd go back into part 1 and remove all references to ``button_a`` and ``button_b``.
    #. We can change the documentation to explain there is an exception. I'd go back to part 1 and add something along the lines of "if you are using the GEMMA M0 and are using the specialized button multiplexer, you will not have the ``button_a`` and ``button_b`` objects in ``setup.py``.
    #. We can go ahead and implement something that provides the API as described.
    
    There's no perfect answer here. Changing documentation, especially documentation that isn't labeled with a version number (like this series) is always risky. There could be a lot of users out there who wrote code according to the old docs, and now, if someone who followed the newer version tries to use their code, things get weird (errors, unexpected behavior).
    
    On the other hand, implementing API objects that really aren't used is probably a waste of time. In some cases it could be a large investment. In our case, our objects have their own separate API that we might need to implement.  In fact, if you look at the `DigitalIO API <https://circuitpython.readthedocs.io/en/3.x/shared-bindings/digitalio/DigitalInOut.html>`__, there's a lot of extra things we'd need to provide that probably don't really matter. If you aren't sure there are people depending on the original API that you violated, it's time you could be spending on something else.
    
    So it's always a judgement call. It helps to have open communication with your users so that you know who's relying on what. Overall, it's best to wait to publish an API until you've finished your blog series and realize that you broke things |winking|.
    
    For the sake of completeness and illustration, here's an implementation that would provide a usable ``DigitalIO`` interface for our multiplexed ``AnalogIO`` buttons:
    
    .. code-block:: python
        
        class MultiplexedIO:
            def __init__(self, token):
                self.token = token
                self.pull = None
                self.direction = None
                self.drive_mode = None
                
            @property
            def value(self):
                return check(self.token)
                
            def switch_to_output(self, *args, **kwargs):
                pass
                
            def switch_to_input(self, *args, **kwargs):
                pass
                
            def deinit(self):
                pass
            
            def __enter__(self):
                pass
                
            def __exit__(self):
                pass
                
        button_a = MultiplexedIO("A")
        button_b = MultiplexedIO("B")
    


CircuitPython M0 Express
------------------------
The CircuitPython M0 Express has everything built in, and the internal pins are assigned via the ``board`` module.

.. code-block:: python
    
    ﻿import board
    import neopixel
    import adafruit_thermistor
    from digitalio import DigitalInOut, Direction, Pull
    import analogio
    
    thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)
    photocell = analogio.AnalogIn(board.LIGHT)
    
    led = DigitalInOut(board.D13)
    led.direction = Direction.OUTPUT
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10)
    rgb.brightness = 0.5
    
    a_button = DigitalInOut(board.D4)
    a_button.direction = Direction.INPUT
    a_button.pull = Pull.DOWN
    
    b_button = DigitalInOut(board.D5)
    b_button.direction = Direction.INPUT
    b_button.pull = Pull.DOWN
    
    def check(token):
        if token == "A":
            return a_button.value
        if token == "B":
            return b_button.value
    
    


ItsyBitsy/Trinket M0
--------------------

.. note::
    
    Be sure to change the pin numbers as needed to reflect how your boards are wired up.
    

.. code-block:: python
    
    ﻿import board
    from digitalio import DigitalInOut, Direction, Pull
    import analogio
    import adafruit_dotstar
    import adafruit_thermistor
    
    thermistor = adafruit_thermistor.Thermistor(board.A1, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)
    photocell = analogio.AnalogIn(board.A2)
    
    led = DigitalInOut(board.D13)
    led.direction = Direction.OUTPUT
    
    rgb = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
    rgb.brightness = 0.3
    
    a_button = DigitalInOut(board.D11)
    a_button.direction = Direction.INPUT
    a_button.pull = Pull.UP
    
    b_button = DigitalInOut(board.D7)
    b_button.direction = Direction.INPUT
    b_button.pull = Pull.UP
    
    def check(token):
        if token == "A":
            return not a_button.value
        if token == "B":
            return not b_button.value

Sampling Analog Signals
=======================
When we worked with digital inputs, we dealt with the dreadded "bounce" by reducing the sample rate. 

Lets run some bare-minimum code to make sure our sensors are functioning properly. For the sake of illustration, lets look at the raw values we're getting from the analog pins.

.. code-block:: python
        
    ﻿import time
    from setup import thermistor, photocell
    
    while True:
        print("Thermistor:",thermistor.pin.value, "Photocell:", photocell.value)
        time.sleep(0.1)
    
        
Here's a video of the values changing:

**TODO: video of the values changing in Mu, overlayed with how I'm manipulating the CPX or whatever board with lights, canned air, etc.**

You'll notice how the values jump around a lot, even when everything is stable - we're not shining a light on the photocell and the temperature is not changing. Yet the values "wiggle" - sometimes it can be quite drastic (relatively speaking). If you were to remove the sleep, you'd see it was even worse.

This happens for a lot of reasons. First, lets dive into how analog signals are read.

Why We Need Sampling
--------------------

Analog signals have a range that, in practical terms, goes from zero to our working voltage (3.3 volts). The resolution is basically *infinite*. 

In an *analog* circuit, you can tie the value of a resistor to an analog voltage. Imagine a incandescent light that dims when you turn a dial. The dial is actually sort of a dynamic resistor (called a `potentiometer <https://en.wikipedia.org/wiki/Potentiometer>`__) that changes its resistance as its turned, letting more or less electricity to the bulb. Imagine the dial was replaced with a thermistor and companion resistor. The temperature that the sensor is detecting would *directly* control the intensity of the bulb. 

**TODO: would it be worth it to get a little incandescent bulb and do a demo of this?**

Another, more common example is how audio is recorded and played back. Before digital recording, the entire process was analog: the microphone was an analog device where a diaphragm vibrated and generated a variable voltage, that voltage was cut into a record by a needle that vibrated to the voltage, and when you play back a record, a different needle would vibrate based on the grooves cut previously, generating a voltage that would go to a speaker, which is a device that takes electrical voltage and vibrates another diaphragm which pushes air around to make sound. 

.. note::
    
    This is a gross simplification! As much as audio is a big part of our lives, I'm hesitant to talk about it much here. The reason is that while audio is an analog medium, and it can be recorded as a variable voltage, there's a lot of very specific aspects of audio that are huge rabbit holes that risk distracting us from our task at hand. 
    
    In particular, audio sampling and production systems are geared toward *human* sensitivity. There's a lot of extra information that is involved in the discussion that has nothing to do with reading analog signals in general. There *are* concepts that come into play though, like encoding schemes, packing data into signals, and so on, that can be really useful in microcontroller projects. 
    
    **TODO: Find some good links for more info, probably Technology Connections**

In a microcontroller, we're working with *digital* circuitry. Our "language" is essentially "on" and "off" (``HIGH`` and ``LOW``, 1 and 0). If the voltage is over a threshold, an input reads "on". If it's below the threshold, the input reads "off". Analog signals can be anything between 0 and the maximum voltage. If we wired up a variable voltage to a "regular" digital pin, it would read "on" a percentage of the time, and "off" the rest of the time. This doesn't help us determine *how much* voltage is coming in. Quantifying the amount of voltage is how we can interpret the voltage and covert it to meaningful units like degrees and lumens. 

So how can we properly read an analog signal? |thinking|

This is where an `analog to digital converter (ADC) <https://en.wikipedia.org/wiki/Analog-to-digital_converter>`__ comes into play. ADCs measure the voltage level of an input at a regular interval (or *sample* the signal), and map that to a value you can read in software between 0 and some maximum number. If you were to look at it on a graph, the ADC turns a wave into a series of numbers, turning a smooth hill and valley into a stair-step pattern. 

**TODO: illustration of how sampling works**

The ADC fixes the resolution of the analog voltage to a certain amount (instead of infinity), because it's *sampling* the voltage, and because the value is converted to an integer within a fixed range. This is referred to as the *sample rate*. 

.. tip::
    
    Sample rates are commonly expressed in terms of "bit depth" and "sample frequency". You may have heard that CD audio recorded at "16-bit/44.1kHz". This means it samples 16-bit (0-65536) values 441,000 times a second.
    
Jitter, Wobble, And Weird Readings
----------------------------------
Now lets get back to the main topic: what causes the analog readings to be so "twitchy"?

Our boards have an ADC built into the microcontroller. When we assign a pin to be an analog input (when we create an ``﻿analogio.AnalogIn`` object), CircuitPython "turns on" the ADC and connects it to a given pin. Our microcontrollers are configured with 16-bit channels, so our analog inputs produce numbers from 0 to 65536 (the maximum value of a 16-bit unsinged integer). 

We take samples at an undetermined rate, but lets assume it's the clock frequency of our board. In the case of the M0, that's 48kHz, so our sample rate is 16-bit/48kHz. 

This is where our first bit of wobble or jitter comes from in our CircuitPython readings. We've cut the resolution down from infinity to 16 bits per sample. This means we have to mush the voltage reading into one of 65,536 values. There's no in-between. So a value could "jump" from say, 12432 to 12433 if it actually falls somewhere in-between.

.. note::
    
    I say the rate is "undetermined", because the data sheet for the SAMD21 in our M0 boards shows that the sample rate of the ADC is highly configurable. There are a *lot* of variables. The actual ADC is 12 bit, but it can do some tricks to get higher sample frequencies. I'm not close enough with the CircuitPython source code (yet) to say how exactly things are done, and it could vary from board to board. For the sake of this tutorial, assuming a sample rate of 16/48 is sufficient for explaining things, and it might be close, but it's probably not accurate **at all**. 
    

Beyond the function of an ADC, we're really getting into the physics of the specialized materials in our sensors. They can be extremely sensitive. In one instance, there may be 8 photons (fake number) hitting our photocell. In the next, it may be 9, or 10. It varies. Temperature is the same. 

We also have to take into account the *environment*. A breeze can change the resistance of a thermistor enough to make the reading change. A reflection or shadow can do the same for a photocell, *even if a person could never feel or see a difference*. Other environmental factors include the board itself - the chips we're using are very efficient, but all integrated circuits produce heat - that heat can impact the temperature reading. That heat varies a lot depending on what the microcontroller is doing at any given time. Built-in neopixels can put off enough light to bounce back onto our photocell. 


We can, of course, mitigate environmental issues in some ways (move sensors away from the microcontroller or LEDs for one), but not in all of them. 

Yet another issue is "settling". The materials in our sensors (usually) react *really* fast to changes in temperature or light, but not instantaneously. This can cause some issues if someone, say, waves their hand in front of our photocell - the reading will dip, but it might not recover as quickly as we moved our hand.

The best approach to address all of these issues is very similar to how we avoided the dreaded "button bounce" in previous sections, it involves *sampling at a reduced rate*, but since our readings are so variable, we also need to *manipulate the data* so it properly smooths out.

An Extreme Example: A CircuitPlayground Express Nightlight
==========================================================

Lets build a quick project using our demo circuits that illustrates the sampling problem in a visual way, and then we'll discuss some useful techniques for fixing it.

.. tip::
    
    The following code will work on any of the demo circuits we've built, but it's most illustrative of our problems on the CircuitPlayground Express, especially if you have all 10 neopixels turned on.
    
Quick Overview
--------------
The basic functionality of a nightlight is:

* Turn on when the ambient light is low.
* Turn off when the ambient light is normal or higher.

We'll use the built-in neopixel or dotstar as the light.

We'll add two more functions to help illustrate the problem, and make the code more interesting:

* Button "B" will turn the nightlight on or off.
* Button "A" will toggle the color of the nightlight between 6 pre-determined colors.

One final addition, for the sake of usability:

* The built-in red LED on pin 13 will be used to indicate whether the nightlight is enabled or not.

Initial Version: Flickering Illustrated
---------------------------------------

.. code-block:: python
        
    ﻿import time
    from setup import thermistor, photocell, rgb, led, check
    
    colors = ((255, 255, 255),
              (255, 255, 0),
              (255, 0, 0),
              (0, 255, 0),
              (0, 0, 255),
              (0, 255, 255))
    
    class State:
        _debounce = 0.2
    
        def __init__(self):
            self.button_b = False
            self.button_a = False
            self.ambient_light = photocell.value
            self.enabled = False
            self.on = False
            self._color = 0
            self.button_checkin = time.monotonic()
        
        @property
        def color(self):
            if not self.on or not self.enabled:
                return (0, 0, 0)
                
            return colors[self._color]
        
        def change(self):
            if self.enabled:
                if self._color >= 5:
                    self._color = 0
                else:
                    self._color += 1
        
        def update_ambient_light(self):
            self.ambient_light = photocell.value
        
        def update_buttons(self):
            if time.monotonic() - self.button_checkin > self._debounce:
                # b button was pressed            
                if not self.button_b and check("B"):
                    print("B button pressed")
                    self.button_b = True
                    self.enabled = not self.enabled
                else:
                    self.button_b = False
                    
                if not self.button_a and check("A"):
                    print("A button pressed")
                    self.button_a = True
                    self.change()
                else:
                    self.button_a = False
    
                self.button_checkin = time.monotonic()
        
        def on_off_based_on_ambient_light(self):
            if self.enabled:
                if self.ambient_light > 2000:
                    self.on = False
                else:
                    self.on = True
        
        def update(self):
            self.update_buttons()
            if self.enabled:
                self.update_ambient_light()
                self.on_off_based_on_ambient_light()
            
        def __repr__(self):
            return "<State Color:{}, Enabled:{}>".format(self.color, self.enabled)
    
    state = State()
    while True:
        state.update()
        rgb.fill(state.color)
        led.value = state.enabled


This code is very similar to the button-debounce code we've written before. In addition to the button states and the desired RGB LED color, we're tracking the current value of the photocell (``ambient_light``) and whether the project is "turned on" or not (``enabled``). 

The primary change is that we've factored the functionality of the ``update()`` method into separate methods (``update_buttons()``, ``update_ambient_light()``, and ``on_off_based_on_ambient_light()``. 


Here's the functionality in action:

**TODO: video of the nightlight, showing normal operation and the flickering.**

Note how the light will flicker when I activate the buttons from the top of the CPX. This is mostly because the light from the neopixel is reflecting into the photocell, located just below it (but it's also due to the issues explained in the last section). 

Revision #1: Basic Sampling
---------------------------

The first thing we might try is to take the same approach we've taken with the buttons. The logic we discussed in **TODO: link to right section** is still sound - if we set the value of ``ambient_light`` less frequently (*lower the sample rate*), we can combat this, right?

Here's the code:

.. code-block:: python
    
    ﻿import time
    from setup import thermistor, photocell, rgb, led, check
    
    colors = ((255, 255, 255),
                (255, 255, 0),
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (0, 255, 255))
    
    class State:
        _debounce = 0.2
        _light_sample = 0.1
    
        def __init__(self):
            self.button_b = False
            self.button_a = False
            self.ambient_light = photocell.value
            self.enabled = False
            self.on = False
            self._color = 0
            self.button_checkin = time.monotonic()
            self.light_checkin = time.monotonic()
        
        @property
        def color(self):
            if not self.on or not self.enabled:
                return (0, 0, 0)
                
            return colors[self._color]
        
        def change(self):
            if self.enabled:
                if self._color >= 5:
                    self._color = 0
                else:
                    self._color += 1
        
        def update_ambient_light(self):
            if time.monotonic() - self.light_checkin > self._light_sample:
                self.ambient_light = photocell.value
                self.light_checkin = time.monotonic()
        
        def update_buttons(self):
            if time.monotonic() - self.button_checkin > self._debounce:
                # b button was pressed            
                if not self.button_b and check("B"):
                    print("B button pressed")
                    self.button_b = True
                    self.enabled = not self.enabled
                else:
                    self.button_b = False
                    
                if not self.button_a and check("A"):
                    print("A button pressed")
                    self.button_a = True
                    self.change()
                else:
                    self.button_a = False
    
                self.button_checkin = time.monotonic()
        
        def on_off_based_on_ambient_light(self):
            if self.enabled:
                if self.ambient_light > 2000:
                    self.on = False
                else:
                    self.on = True
        
        def update(self):
            self.update_buttons()
            if self.enabled:
                self.update_ambient_light()
                self.on_off_based_on_ambient_light()
            
        def __repr__(self):
            return "<State Color:{}, Enabled:{}>".format(self.color, self.enabled)
    
    state = State()
    while True:
        state.update()
        rgb.fill(state.color)
        led.value = state.enabled

Here's what it looks like in action:

**TODO: video of the CPX nightlight showing the slower flicker**

So we still have flicker, but it takes a lot more to make it happen: I need to bring my finger *very* close to the photocell now. The flicker is also more regular, which is less annoying |grin|.

This might be adequate for most things, but the light will still flash when I'm cycling through colors. 

We could increase the interval, but we will make the nightlight less responsive - what if we wanted to use the nightlight as an emergency light? We wouldn't want it to delay when the power goes out, someone could get hurt.

Claiming Our Inheritance
========================
Once an event is detected, some action is taken. So far in this series, that action is code that lives right along with the event.

Let's revisit with a new example. In this state class, we're going to track the value of a temperature sensor. When the temperature is between 0° and 15° C, the neopixel/dotstar will be illuminated blue. When it's between 16° and 25° C, the pixel will be illuminated green (indicating optimal temperature for human comfort, according to `wikipedia <https://en.wikipedia.org/wiki/Room_temperature>`__). If the temperature climbs above 25° C, the pixel will turn red, indicating that it's really hot.

Here's some code that accomplishes that, using a state class in the style of previous examples:

.. code-block:: python
    
    import time
    from setup import led, rgb, check, thermistor
    
    class State:
        _debounce = 0.2
    
        def __init__(self):
            self.temperature = thermistor.temperature
            self.color = (0, 0, 0)
            self.checkin = time.monotonic()
    
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                self.temperature = thermistor.temperature
    
                if self.temperature < 15:
                    self.color = (0, 0, 255)
                elif 15 < self.temperature < 25:
                    self.color = (0, 255, 0)
                elif self.temperature > 25:
                    self.color = (255, 0, 0)
    
    state = State()
    
    while True:
        state.update()
    
        rgb[0] = state.color
        
So this is a pretty useful state class. We can imagine using it for other sensors. Anything that gives us readings we can translate to multiple colors can be represented with this class. We can copy and paste the code, and create new state classes for each sensor we want to support. 

Let's do that, for the photocell we've wired up earlier. The code is identical, except

* The object used for the value is a simple AnalogIn pin
* The values are different, since we're working with the raw values from the ADC in the range of 0-65535.
* We'll change the colors so it's easier to see the difference between the different readings. In the case of the photocell, purple will represent low light, orange will be "medium" light, and the RGB LED will turn white when the light is in the higher end of the range. 

Let's also use one of the buttons to switch between temperature and light sensing.

.. code-block:: python
    
    import time
    from setup import led, rgb, check, thermistor, photocell
    
    class State:
        _debounce = 0.2
        
        def __init__(self):
            self.value = False
            self.checkin = time.monotonic()
            self.mode = "light"
            
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                self.value = check("A")
                
                if self.value:
                    if self.mode == "light":
                        self.mode = "temp"
                    else:
                        self.mode = "light"
                
                self.checkin = time.monotonic()
    
    class TemperatureStatus:
        _debounce = 0.2
    
        def __init__(self):
            self.temperature = round(thermistor.temperature)
            self.color = (0, 0, 0)
            self.checkin = time.monotonic()
    
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                print(self.temperature)
                self.temperature = round(thermistor.temperature)
    
                if self.temperature <= 15:
                    self.color = (0, 0, 255)
                elif 15 < self.temperature <= 25:
                    self.color = (0, 255, 0)
                elif self.temperature > 25:
                    self.color = (255, 0, 0)
    
                self.checkin = time.monotonic()
    
    class LightStatus:
        _debounce = 0.2
    
        def __init__(self):
            self.amount = photocell.value
            self.color = (0, 0, 0)
            self.checkin = time.monotonic()
    
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                print(self.amount)
                self.amount = photocell.value
    
                self.checkin = time.monotonic()
    
            if self.amount < 20460:
                self.color = (255, 0, 255)
            elif 20460 < self.amount < 40920:
                self.color = (255,140,0)
            else:
                self.color = (255, 255, 255) 
    
    light = LightStatus()
    temp = TemperatureStatus()
    state = State()
    
    while True:
        light.update()
        temp.update()
        state.update()
        
        if state.mode == "light":
            rgb[0] = light.color
        else:
            rgb[0] = temp.color
            
Here's what that looks like in action:

**TODO: video of the code in action**

Depending on your ambient temperature, light, and the particular components you have, you may notice that there is some flicker when the temperature or light crosses the threshold. This flicker happens because the input is rapidly fluctuating between values right around the barrier between regions. 

**TODO: try to get a video of the flicker in action**

This happens for a lot of reasons. Temperature and light are both relative and additive properties. They are relative in the sense that the temperature being read is affected by the environment the sensor is in. They are additive in that the temperature of the CPU on the board, or the light coming from the RGB LED, can impact the ambient temperature or light reading.

The other factor is that there are several instances of rounding happening. Since these are both analog inputs, the values are read in the range from 0 to 65535. True analog signals have essentially infiniate *resulution*. The lower and upper limits are based on the chemical and physical properties of the sensors, but the values in between can vary by tiny amounts. The analog-to-digital converter (ADC) in our M0/M4 chips can only detect voltage changes, and only in the range of 0 to 65535 (voltage also has an infinite resolution). This is the first place where our value is rounded. 

Our ADC can detect between 0 and 3.3 volts. The microcontroller has to scale the range of 0-65535 onto a range of 0-3.3 volts. 0.001 will likely register as 0 volts, due to this scaling. As will 0.002, 0.003, and so on.

In the case of our temperature sensor, there's another mathematical operation happening, where the ``adafruit_thermistor`` module is converting the number reported by the ADC into a temperature in degrees Celsius. That's another, smaller range, from 0-100. We go a step further and round *that* value again to a whole number. This can cause weird rounding errors where a value is sort of close to the threshold but it gets rounded up during one 0.2 second interval, and rounded down during the next, causing the code to think that we've gone from "high" temperature to "medium" and then back again very quickly.

There is a better way to approach this problem, that lets us reuse as much code as possible. It also sets the stage for us to tackle the flicker issue as well, when we start looking at changes from one value range to another as an *event*.

Object-oriented programming introduces us to the concept of *inheritance*. In the simplest terms, its a way to re-use common code in many classes. It's a bit like the Python interpreter is doing the copy and paste for you - you inherit from another class, and then edit the parts you want to change. 

It's a concept that's best illustrated with an example. Lets refactor our classes to use inheritance. 

The first step is to figure out what code is common to both "status" classes. 

There are obvious things, like both classes have an ``update()`` method, ``checkin`` and ``color`` instance attributes, and a ``_debounce`` class attribute. 

But some similarities require a bit of critical thought. Here are the less obvious things both classes have in common:

* They both track the state of an analog signal. In the ``TemperatureStatus`` class, it's called ``temperature``. In the ``LightStatus`` class, it's called ``amount``. 
* They both check a sensor for a value and update their state.
* They both change color based on the state. 

It's also important to think about what's different:

* The ways that the analog signal is read is different. ``TemperatureStatus`` uses ``﻿thermistor.temperature``. ``LightStatus`` uses ``﻿photocell.value``.
* ``TemperatureStatus`` has to convert the recorded value to an integer (note the use of ``round()``). ``LightStatus`` gets an integer from the ``photocell`` pin object.
* In ``TemperatureStatus``, the color changes to blue below 15, green between 15 and 25, and red beyond 25.
* In ``LightStatus``, the color changes to purple below ﻿20460, orange between ﻿20460 and ﻿40920, and white above ﻿40920.

We can think about the common and differing functionality in terms of actions - the status object reads the sensor, the status object updates the state, the status object changes the color. The way the status object does each of these things is slightly different. So we can factor out that functionality from the ``update()`` method, into additional methods that ``update()`` can call. This way, the ``update()`` method from the base class can handle most use cases. We can provide a new implementation for any methods that require specialized functionality in child classes. When ``update()`` calls the factored out methods, it will call the code from the child class.

.. tip::
    
    When we create a method in a child class that has the same name as one in the parent class, the child class' method is used when the method is called. This is a core OOP concept called `method overriding <https://en.wikipedia.org/wiki/Method_overriding>`__. 
    
    Method overriding and class inheritance are fundamental features of `polymorphism <https://en.wikipedia.org/wiki/Polymorphism_(computer_science)>`__, a key aspect of object-oriented programming. The finer details are beyond the scope of this series, but it's worth reading about. 
    
    I suggest waiting to dig into that information until *after* you finish this part of the CircuitPython state series. In my experience, it can be a bit obtuse in the abstract, and having some practical experience with polymorphism without the theory might make the computer science bits easier to absorb |mortarboard|.

We'll put all of the common functionality into one *base class*. This base class will exist solely to be extended.
    
We'll call this new base class ``Status``:

.. code-block:: python
    
    ﻿class Status:
        _debounce = 0.2
        
        def __init__(self):
            self.value = 0
            self.color = (0, 0, 0)
            self.checkin = time.monotonic()
            
        def read_input(self):
            pass
            
        def set_color(self):
            pass
        
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                self.read_input()
                self.set_color()
                self.checkin = time.monotonic()
                

.. note::
    
    This is, in practical terms, an **abstract base class** (or `abstract type <https://en.wikipedia.org/wiki/Abstract_type>`__). However, Python doesn't provide true abstract types. In languages that do, you *cannot* instantiate a class that is marked as abstract. It causes a syntax error. 
    
    You will also get errors from the compiler if you try to extend an abstract class and don't implement all of the abstract methods.
    
    In Python, there isn't a language-level concept of *abstract*, so you can instantiate "abstract" base classes without causing any direct errors (depending on how they are constructed, they may cause secondary errors though). You can fail to fully implement the abstract parts, and it's totally cool |cool|.
    
    In the standard library, there is, however, a module called `abc <https://docs.python.org/3/library/abc.html>`__ that uses `metaprogramming <https://en.wikipedia.org/wiki/Metaprogramming>`__ to implement functionality similar to true abstract types. It can be useful if you have a need to enforce the "abstractness" of a class like the one we're creating below. 
    
    |heartbreak| However, the ``abc`` module is not included in MicroPython or CircuitPython. There are other techniques you can use to get close, but not this module |heartbreak|
                
We've kept the common ``color`` and ``checkin`` attributes, but we've created a new, more generic common attribute called ``value``, that will store the last value read from the sensor. 

Note the two new methods, ``read_input()`` and ``set_color()``. These handle the functionality that is different in each case. The way we update the state attribute and the way we decide what color the LED should be both differ between the temperature and light detecting classes. This is *method overriding* in action. 

.. tip::
    
    Since this is just a base class, we're not actually doing anything in these methods. We've employed the ``pass`` keyword to allow us to make a valid function that doesn't do anything (also known as a `no-op <https://en.wikipedia.org/wiki/NOP>`__). 
    
    Another, better way we can accomplish the same effect is have an empty method body, but add a `docstring <https://en.wikipedia.org/wiki/Docstring>`__. This has the added benefit of documenting what the method is supposed to do. 
    
    It looks something like this:
    
    .. code-block:: python
        
        def read_input(self):
            """
            This method reads a value from some kind of input and sets 
            self.value. The exact value set is dependent on what set_color() 
            needs to make its decision.
            
            Returns: None.
            """
            
        def set_color(self):
            """
            Using self.value, this method will set self.color to an appropriate
            value. 
            
            Returns: None.
            """
            
    |unicorn| It's really best practice to use docstrings in every method, but we have to limit their use in CircuitPython because docstrings take up precious memory, especially when the code has not been compiled into bytecode.

The ``update()``, and ``__init__()`` methods now contain all of the common logic that the two previous classes share. 

``__init__()`` sets the default values of the instance attributes.

``update()`` now calls ``read_input()`` and ``set_color()`` instead of directly reading the input object and using a series of ``if``/``else`` statements to set the color. 

When we extend the ``Status`` class, we will write our own implementations, *overriding*, the ``read_input()`` and ``set_color()`` methods. 

Because of the way class inheritance works, the code that we override will be executed in our class, and the code that we don't override will be executed in the base class. So unless we write our own ``__init__()`` and ``update()`` methods, the code for those methods will execute in the ``Status`` class.

Lets look at a graphic that illustrates this concept in generic terms.

.. image:: {static}/images/polymorphism-explained.png
   :width: 80%
   :align: center
   
In our implementation, we'll be overriding the ``read_input()`` and ``set_color()`` methods in each of our classes. The other methods, ``__init__()`` and ``update()``, and the one class property ``_debounce``, will share the implementation in the base class.

Lets take the temperature sensor class, which we'll call ``TemperatureStatus``, as an example. If we modeled it in the style of the concept drawing above, it would look like this:

.. image:: {static}/images/nonblocking-polymorphism.png
   :width: 80%
   :align: center
   
Our other class, which we'll name ``LightStatus``, would look identical if it were illustrated in the same manner. 

So this should give us a proper mental model for how polymorphism is working for us in our class hierarchy. 

Now we can look at the completed code with the two derived classes fully implemented:

.. code-block:: python
    
    import time
    from setup import led, rgb, check, thermistor, photocell
    
    class State:
        _debounce = 0.2
        
        def __init__(self):
            self.value = False
            self.checkin = time.monotonic()
            self.mode = "light"
            
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                self.value = check("A")
                
                if self.value:
                    if self.mode == "light":
                        self.mode = "temp"
                    else:
                        self.mode = "light"
                
                self.checkin = time.monotonic()
    
    class Status:
        _debounce = 0.2
    
        def __init__(self):
            self.value = 0
            self.color = (0, 0, 0)
            self.checkin = time.monotonic()
    
        def read_input(self):
            pass
    
        def set_color(self):
            pass
    
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                self.read_input()
                self.set_color()
                self.checkin = time.monotonic()
    
    class TemperatureStatus(Status):
        def read_input(self):
            self.value = round(thermistor.temperature)
    
        def set_color(self):
            if self.value <= 15:
                self.color = (0, 0, 255)
            elif 15 < self.value <= 25:
                self.color = (0, 255, 0)
            elif self.value > 25:
                self.color = (255, 0, 0)
    
    class LightStatus(Status):
        def read_input(self):
            self.value = photocell.value
    
        def set_color(self):
            if self.value < 20460:
                self.color = (255, 0, 255)
            elif 20460 < self.value < 40920:
                self.color = (255,140,0)
            else:
                self.color = (255, 255, 255) 
    
    
    light = LightStatus()
    temp = TemperatureStatus()
    state = State()
    
    while True:
        light.update()
        temp.update()
        state.update()
        
        if state.mode == "light":
            rgb[0] = light.color
        else:
            rgb[0] = temp.color
            
This is quite clean, well-organized code. This pattern can be used anywhere that you need to track state for multiple, similar sensors that need to be handled differently.

But lets refactor things again so that the code defines *events* for subclasses to *handle*.

Moving Code Into Its Own Modules
================================
As a project grows, it's a good idea to organize source code in a logical way.

Python provides the concept of *modules* and *packages* to help with this.

Our code in this series is on the verge of growing more complex, and we will have a lot of code that won't change. So lets move some code around and make a new module.

.. tip::
    
    It also makes it possible to compile this unchanging code into ``.mpy`` files to save space/memory. More on this later!
    

We've already done this with our ``setup`` module, holding our board-to-board abstraction objects. 

The concept is the same - you put the code you want to execute, and all of the variable definitions, in a file that ends in ``.py``. We then import the objects we care about into our main ``code.py`` file.

The code we want to move at this point is the ``State`` class. It won't be changing at all for the next several examples. 

There's something else we can do that is kind of interesting - we can use the module to instantiate the state object for us! This happens because code in a module is executed *when its first imported*. This is already happening in ``setup``, when we create the various API objects (``rgb``, ``led``, ``check()``, etc).
     

The first step is to remove the ``State`` class, and the line where it's instantiated (``state = State()``) from ``code.py``, and put that code into a new file, we'll call ``state.py``. Then add the necessary imports (``time``, ``setup``) to the top of the file:

.. code-block:: python
    
    # -- save as state.py --
    
    ﻿import time
    from setup import check
    
    class State:
        _debounce = 0.2
    
        def __init__(self):
            self.value = False
            self.checkin = time.monotonic()
            self.mode = "light"
    
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                self.value = check("A")
    
                if self.value:
                    if self.mode == "light":
                        self.mode = "temp"
                    else:
                        self.mode = "light"
                self.checkin = time.monotonic()
                
    state = State()
    
Then, in ``code.py``, we just need to add:

.. code-block:: python
    
    from state import state
    
.. tip::
    
     This is probably the simplest possible way to implement the `Singleton Pattern <https://en.wikipedia.org/wiki/Singleton_pattern>`__ in Python |thinking|
     


Event Planning: Not Just For Parties Anymore
============================================
There's a different way we can look at our example code. Currently, in both status classes, we're changing the ``color`` state attribute right after we read from the input. 

We can look at this from an *event detection* perspective, as we did for buttons in the last installment. 

Instead of changing the ``color`` attribute every time we check the input, we can instead *only* change the color when the input's state has changed. We can even define different events based on the amount of change. 

Let's implement this in a very simplistic manner first, so we can make sure we understand the basics of how we're defining and detecting events. We'll just write the code for reading the thermistor to keep things simple.
 

.. code-block:: python
    
    import time
    from setup import led, rgb, check, thermistor
    
    class TemperatureStatus:
        _sample_rate = 0.5
        _event_check = 1.0
        _threshold = 2
        
        def __init__(self):
            self.checkin = time.monotonic()
            self.value = round(thermistor.temperature)
            self.previous = self.value
            self.event_checkin = time.monotonic()
            self.color = (0, 0, 0)
            
            self.dispatch()
        
        def dispatch(self):
            print("Dispatching", self.previous, self.value)
            if self.value <= 15:
                if self.color != (0, 0, 255):
                    print("Low level event")
                    self.color = (0, 0, 255)
            elif 15 < self.value <= 25:
                if self.color != (0, 255, 0):
                    print("Medium level event")
                    self.color = (0, 255, 0)
            elif self.value > 25:
                if self.color != (255, 0, 0):
                    print("High level event")
                    self.color = (255, 0, 0)
        
        def update(self):
            if time.monotonic() - self.checkin > self._sample_rate:
                self.value = round(thermistor.temperature)
                self.checkin = time.monotonic()
                
            if time.monotonic() - self.event_checkin > self._event_check:
                if abs(self.previous - self.value) > self._threshold:
                    self.dispatch()
                    self.previous = self.value
                self.event_checkin = time.monotonic()  
    
    temp = TemperatureStatus()
    
    while True:
        temp.update()
        rgb[0] = temp.color
        
        
There are a couple of major differences here, compared to the previous example and to the button-related event work we did in the previous installment.

The biggest difference is that we're tracking two different time intervals. First, we're sampling the value of the therimistor every 0.5 seconds. Then, once per second, we're comparing the value of the thermistor with the value it was one second ago. This gives us a really low overall sample rate, which "smoothes out" the values. But it also gives us a way to compare previous state with current state.

The goal is to only fire the events - changing the color for each "level" of temperature - when things have changed, and when they've changed significantly.

As a first pass, we keep track of the short-term temperature by updating ``self.value`` every 0.5 seconds. We keep track of a longer-term temperature by updating ``self.previous`` every 1.0 seconds. Then, we can compare ``self.value`` to ``self.previous``, and determine if there's significant change. 

The other major change occurs when a possible event is detected. A possible event happens when ``self.previous`` is more than ``self._threshold`` degrees larger or smaller than ``self.value``. From there, we call the ``dispatch()`` method, which decides what the value represents. 

The second pass is to then *only* consider an event has occurred *if* the current temperature is in a different range from the range that we're currently in. Put differently, we're asking the question, "should the color change?", and only changing it when necessary. We know what the previous state is by looking at the current value of ``self.color``.

.. note::
    
    This is a bit convoluted! I wanted to stick to the original approach as much as we could at this stage, so we can better see how things will change when we simplifying the code shortly. |unicorn|
    

Why do we need this two-pass approach? In this project, we have events that change a simple state value (the color). It only makes sense to change the color when the temperature crosses from one range to another. But in other projects, we may want to take action every time the value changes. In that case, our ``dispatch()`` method would look very different. Instead of only changing the state if the current temperature reading would cause the state to change, it could act every time. 

By approaching it in two passes, we have a lot of flexibility in how we handle our events. 

Now that we have the basic concept illustrated, we can apply this new event-driven approach to our ``Status`` and ``LightStatus`` classes:

.. code-block:: python
    
    import time
    from setup import led, rgb, check, thermistor, photocell
    
    from state import state
    
    class Status:
        _sample_rate = 0.5
        _event_check = 1.0
        _threshold = 2
        
        def __init__(self):
            self.checkin = time.monotonic()
            
            self.read_input()
            self.previous = self.value
            
            self.event_checkin = time.monotonic()
            self.color = (0, 0, 0)
            self.level = None
            
            self.dispatch()
            
        def read_input(self):
            pass
            
        def high(self):
            pass
            
        def medium(self):
            pass
            
        def low(self):
            pass
        
        def set_level(self):
            pass
        
        def dispatch(self):
            previous_level = self.level
            
            self.set_level()
            
            if self.level != previous_level:
                if self.level == "low":
                    self.low()
                elif self.level == "medium":
                    self.medium()
                elif self.level == "high":
                    self.high()
                
        def update(self):
            if time.monotonic() - self.checkin > self._sample_rate:
                self.read_input()
                self.checkin = time.monotonic()
                
            if time.monotonic() - self.event_checkin > self._event_check:
                if abs(self.previous - self.value) > self._threshold:
                    self.dispatch()
                    self.previous = self.value
                self.event_checkin = time.monotonic()  
    
    class TemperatureStatus(Status):
        _sample_rate = 0.5
        _event_check = 1.0
        _threshold = 2
        
        def high(self):
            self.color = (255, 0, 0)
            
        def medium(self):
            self.color = (0, 255, 0)
            
        def low(self):
            self.color = (0, 0, 255)
            
        def read_input(self):
            self.value = round(thermistor.temperature)
            
        def set_level(self):
            if self.value <= 15:
                self.level = "low"
            elif 15 < self.value <= 25:
                self.level = "medium"
            elif self.value > 25:
                self.level = "high"
                
    class LightStatus(Status):
        _sample_rate = 0.5
        _event_check = 1.0
        _threshold = 200
        
        def high(self):
            self.color = (255, 255, 255)
            
        def medium(self):
            self.color = (255,140,0)
            
        def low(self):
            self.color = (255, 0, 255)
            
        def read_input(self):
            self.value = photocell.value
            
        def set_level(self):
            if self.value < 20460:
                self.level = "low"
            elif 20460 < self.value < 40920:
                self.level = "medium"
            else:
                self.level = "high"
                
    temp = TemperatureStatus()
    light = LightStatus()
    
    while True:
        light.update()
        temp.update()
        state.update()
    
        if state.mode == "light":
            rgb[0] = light.color
        else:
            rgb[0] = temp.color
    

In this version, we've broken out the events into their own methods (``low()``, ``medium()``, and ``high()``), so they can be overridden in child classes. If you don't care about a certain event, you can just neglect to implement it. Since the event methods are no-ops in the base class, they'll get called, but nothing will happen.

Now, if we wanted something special to happen when a given event is detected, we just need to add that to the given event method in the child class. Some ideas: 

* Using a transistor or a relay, We could turn on/off a fan or heater when the temperature hits certain ranges. Since we have events for both "high" and "low", we could do both!
* With our photocell, we could turn on/off a bunch of neopixels, so it acts like a night-light.
* We could use other sorts of sensors, and do things like proximity detection.

This is a really useful pattern that is easy to extend and refine for any particular use case.

There is one more enhancement we can make. You'll notice that our current child classes, ``TemperatureStatus`` and ``LightStatus``, both do very similar things in their ``set_level()`` and event methods. We can factor that functionality into the base class. We just need to add a few more properties that will define what colors correspond with which ranges. Here's one way of accomplishing that:

.. code-block:: python
    
    import time
    from setup import led, rgb, check, thermistor, photocell
    
    from state import state
    
    class Status:
        _sample_rate = 0.5
        _event_check = 1.0
        _threshold = 1
        
        _colors = {
            'low': (0, 0, 255),
            'medium': (0, 255, 0),
            'high': (255, 0, 0)
        }
        
        _ranges = {
            'low': (0, 20460),
            'medium': (20460, 40920),
            'high': (40920, None)
        }
        
        def __init__(self):
            self.checkin = time.monotonic()
            
            self.read_input()
            self.previous = self.value
            
            self.event_checkin = time.monotonic()
            self.color = (0, 0, 0)
            self.level = None
            
            self.dispatch()
            
        def set_level(self):
            for level, params in self._ranges.items():
                start, end = params
                
                if end is None:
                    if self.value > start:
                        self.level = level
                        break
                else:
                    if start < self.value <= end:
                        self.level = level
                        break
        
        def dispatch(self):
            previous_level = self.level
            
            self.set_level()
            
            if self.level != previous_level:
                self.color = self._colors[self.level]
                
                if self.level == "low":
                    self.low()
                elif self.level == "medium":
                    self.medium()
                elif self.level == "high":
                    self.high()
        
        def read_input(self):
            pass
            
        def high(self):
            pass
            
        def medium(self):
            pass
            
        def low(self):
            pass
        
        def update(self):
            if time.monotonic() - self.checkin > self._sample_rate:
                self.read_input()
                self.checkin = time.monotonic()
                
            if time.monotonic() - self.event_checkin > self._event_check:
                if abs(self.previous - self.value) > self._threshold:
                    self.dispatch()
                    self.previous = self.value
                self.event_checkin = time.monotonic()  
    
    class TemperatureStatus(Status):
        _threshold = 2
        
        _ranges = {
            'low': (0, 15),
            'medium': (15, 25),
            'high': (25, None)
        }
            
        def read_input(self):
            self.value = round(thermistor.temperature)
                
    class LightStatus(Status):
        _threshold = 200
        
        _colors = {
            'low': (255, 0, 255),
            'medium': (255,140,0),
            'high': (255, 255, 255)
        }
            
        def read_input(self):
            self.value = photocell.value
                
    temp = TemperatureStatus()
    light = LightStatus()
    
    while True:
        light.update()
        temp.update()
        state.update()
    
        if state.mode == "light":
            rgb[0] = light.color
        else:
            rgb[0] = temp.color
            
            
Summary And What's Next
=======================
Now, we have a base class that handles dispatching to methods, but also does the color changes for us. We just had to provide the parameters in the form of additional class attributes. The default colors and ranges are based on what we think might be pretty common - the colors are red, green, and blue, and the ranges divide the range of the analog values on our boards roughly into thirds. For most sensors we work with, the default will be adequate. But as you can see in both of our child classes, it's easy to tweak the colors or ranges to suit our needs. This version of the code gives us some background functionality - we might be building what amounts to a thermistat or nightlight, but by using this ``Status`` base class, we automatically have a status light that uses the built-in neopixel or dotstar to give us some useful information about what's going on without having to plug our board into a computer.

There are other approaches to this same problem, however. Writing a new child class every time we want to implement a minor change in functionality might be overkill. In the next installment, we'll explore ways we can control how an object functions by passing configuration values to its constructor (the ``__init__()`` method). We'll also utilize a very interesting pattern called *dependency injection* to create more complex functionality, tracking more complex state, but in a very straight-forward way. 

