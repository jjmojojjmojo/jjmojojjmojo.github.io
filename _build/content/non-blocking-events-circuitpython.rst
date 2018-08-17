Exploring State: Non-Blocking Events In CircuitPython
#####################################################
:date: 2018-06-11 15:07
:author: lionfacelemonface
:category: tutorial
:tags: tutorial; circuitpython; hardware; state;
:slug: non-blocking-events-in-circuitpython
:status: draft

.. include:: ../emojis.rst

In this article we'll cover dealing with state and working with events in a non-blocking way in `CircuitPython <https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython>`__, `Adafruit's <https://adafruit.com>`__ port of `MicroPython <https://micropython.org/>`__ for the  `ATSAMD21 Cortex M0 microprocessor <https://www.microchip.com/wwwproducts/en/ATSAMD21G18>`__.

We'll explore the most common use case for state, *button debouncing*, but also explore state as a concept, and discuss patterns for dealing with it in a microcontroller environment.

While the code is being developed for CircuitPython, the concepts and patterns are universal, and apply to any microcontroller (and even some applications outside of embedded platforms). 

.. PELICAN_END_SUMMARY

.. tip::
   
   At the time of writing, Adafruit has just released/announced the first boards in it's M4 line based on the  ATSAMD51 Cortex M4 chip! (namely the `ItsyBitsy M4 Express <https://blog.adafruit.com/2018/06/12/new-product-adafruit-itsybitsy-m4-express-featuring-atsamd51/>`__ and `Feather M4 Express <https://blog.adafruit.com/2018/06/27/coming-soon-adafruit-feather-m4-express-featuring-atsamd51-cortex-m4/>`__). 

The Project, The Platform
=========================
All of the code and thought that in this article has its roots in a personal project. I wanted to make a low-impact tool to help me mouse more efficiently.

I found the answer in `capacative touch <https://en.wikipedia.org/wiki/Capacitive_sensing>`__. This is the same technology behind modern cellphones and touchscreens. 

I was psyched when I found out that the Adafruit M0 series of microcontroler boards provided up to `7 touch capable pins <https://learn.adafruit.com/adafruit-feather-m0-express-designed-for-circuit-python-circuitpython/circuitpython-cap-touch>`__ *and* they can become USB interface devices that can emulate a mouse or keyboard (and more). With these boards, there's no need for an external board or IC for touch or USB control, all I need is an M0, some conductive objects, and some code and I can do `some insanely cool stuff <https://learn.adafruit.com/capacitive-touch-unicorn-horn/introduction>`__.

.. warning::
   
   The M4 boards **do not** support capacitive touch.
   

These boards also provide power management either built-in or it can be `easily added <https://www.adafruit.com/product/2124>`__. It makes it easy to build a portable project that runs off of batteries, but still can be powered from the USB port (and in the case of a rechargable LiPoly battery pack, the USB port can be used to charge it as well). 

What makes these boards a really killer platform for hobby projects is that the M0/M4 series also support **CircuitPython**, Adafruit's fork of MicroPython for these particular ARM controllers. It's *Python*, and one of the languages I'm most comfortable with. 

Besides my personal preference, Python is a great language for learning, rapid prototyping, and general computing.

CircuitPython is being developed with the express goal of making MicroPython more accessible to new programmers. Because of this, it diverges a bit from MicroPython. MicroPython has already diverged a bit from standard Python as well.

The differences aren't significant enough to hinder people new to Python and/or microcontrollers, but if you already know MicroPython, or Python it might be a bit of an adjustment. 

.. tip::
    
    The full list of differences: 
    
    * `CircuitPython vs MicroPython <https://circuitpython.readthedocs.io/en/3.x/#differences-from-micropython>`__
    * `MicroPython vs Python <https://docs.micropython.org/en/latest/pyboard/genrst/index.html>`__
    
That aside, this is a really exciting platform. It stands to provide a gateway for non-programmers to get into computer science and electrical engineering. It's a great time to be alive!

It's not all |rainbow|'s and |unicorn|'s though. In spite of generally being a great platform, CircuitPython has some limitations, that everyone should be aware of. A much more powerful processor is required to run any flavor of MicroPython. Even with more power, the interpreted nature of Python makes code run, overall, slower than comparable compiled Arduino code. 

Because a Python interpreter has to be constructed to execute Python code, the platform is also very RAM (`random access memory <https://en.wikipedia.org/wiki/Random-access_memory>`__) intensive. RAM is a precious resource on any microcontroller, and CircuitPython eats up a lot of working memory before our program even runs. People experienced with microcontrollers will be used to dealing with this, but because of the interpreter, you're at a disadvantage before your code is even loaded. Programs will start to run out of memory when they approach 150-200 lines of code. That includes external libraries. That's not a lot to work with.

.. tip::
   
   We'll cover ways of reducing our memory footprint in this article. It's actually not as bad as it might seem.
   

Further, Python code, especially raw text, takes up a lot of space in another precious resource, *flash memory*. This is where our program code is stored. Again, this is nothing shocking if we've done any embedded development before, but using Python puts us at a bit of a disadvantage - our code can only be compiled down to an intermediary format, it can't be turned into compact machine code, so we have a lot less space to work with.

Beyond this, Adafruit has made it pretty clear that CircuitPython is geared toward *beginners*, and as such their priorities for adding features and the general design of the platform has that audience at the forefront. This can cause some frustration if you want to use a MicroPython or Arduino feature that hasn't been ported to CircuitPython, access an on-board peripheral or use an external IC/breakout board that Adafruit doesn't yet support.

.. note::
    
    This sounds way more dire than it is, and is changing all the time. CircuitPython is still relatively new and is under constant development. |sparkleheart| Adafruit has done an amazing job of supporting the onboard peripherals and the chips and breakout boards they sell in CircuitPython. 
    
    I don't want to downplay what they've accomplished, but if you are coming from other MicroPython boards or the Arduino, or you aspire to build projects that use the full capacity of your microcontroller, you should be aware of what you're getting into.
    

With all that in mind, I'm happy to say Adafruit has done a great job overcoming the worst of these limitations with their M0 boards. Using the ARM based processors means much faster processor cycles - the M0 runs at 48Mhz, the M4 at 120Mhz (verses 8Mhz or 16Mhz for most common Arduino-compatible boards). There's a slowdown running Python on these boards, but for most applications it won't even be remotely noticeable.

These chips have a large amount of RAM to begin with, 32kb for the M0 and a whopping *192kb* for the M4 (compared to 2Kb for most common/classic Arduino chips). 

To address the issue of flash memory, Adafruit provides the *express* series of M0/M4 boards - they add in 2MB of extra flash memory that *just works* for storing Python code (you can use it as general storage as well).

In practice, with the right development boards, the advantages of CircuitPython far outweigh the downsides. In exchange for slightly more expensive components, limited low-level accessibility, and sometimes having to write less-than-elegant Python, we get an incredibly powerful platform for rapid prototyping. I've been using it for a few months now and have found it to be exceedingly capable. 

What makes most of these concerns completely moot is that Adafruit's CircuitPython-compatible boards fully support the Arduino IDE. So if we can't work within the limitations of CircuitPython, we can always switch to the Arduino tooling, and unlock the full potential of the M0/M4 chips.

Audience
========
This guide is written for people who know basic Python, and have done rudimentary things with microcontrollers, like control LEDs and read from momentary switches. 

It doesn't assume you are a Python expert, or have done anything too elaborate with microcontrollers - but it will expose you to some advanced concepts.

It's a good idea to work through `Adafruit's "Welcome To CircuitPython" <https://learn.adafruit.com/welcome-to-circuitpython/overview>`__ guide before trying to dig into the topics covered here, but it's not necessary.

.. tip::
   
   It wouldn't hurt to also work through `CircuitPython Essentials <https://learn.adafruit.com/circuitpython-essentials>`__ as well!
   

This article does dive really deep into details when exploring the concepts behind the code being developed. It also provides line-by-line explanations of each code example. So don't be afraid to give this guide a shot, even if you're really new to microcontrollers. 

Please feel free to `contact the author <{filename}/pages/contact.rst>`__ with questions, corrections, or suggestions on how to make this article more accessible!

Demo Project
============
To illustrate state in action, I've devised a simple, but not overly contrived demonstration project. 

It consists of two buttons, a single one-color LED, and a single "addressable" RGB LED. I've chosen these particular components because they are easy to obtain and hook up. In fact, the single LED and RGB LED (a DotStar or NeoPixel depending on the board) come integrated on all CircuitPython-capable boards.

.. container:: centered
    
    .. image:: {filename}/images/circuitplayground-express-closeup-neopixel-marked.png
          :width: 20%
       
    .. image:: {filename}/images/itsybitsy-m0-express-closeup-dotstar-marked.png
          :width: 20%
       
    .. image:: {filename}/images/trinket-m0-closeup-dotstar-marked.png
       :width: 20%
       
    .. image:: {filename}/images/gemma-m0-closeup-dotstar-marked.png
       :width: 20%
    

.. tip::
   
   On the CircuitPlayground, even the buttons are already integrated!
   

The features of the demo project are as follows:

Phase 1:
    * One button will control the rate of blink of the red LED.
    * The other button will turn the red LED on or off - it will not affect the blink rate.

Phase 2:
    * The functionality of Phase 1 will continue, except the RGB LED will blink as well. The "rate button" will change the blink rate of both LEDs.
    * Pressing both buttons will change the color of the RGB LED.
    
Phase 3:
    * Functionality of Phase 2 will persist, except holding the other button will determine if the rate button is changing the blink rate of the RGB LED or the red LED. If it's held, the RGB LED rate is changed. If It's not held, the red LED rate is changed.
    
This is a fairly simple project but because of the complex button logic, it will really put our state and event code through its paces. 

Materials
=========
If you'd like to follow along, you will need the following items:

* A CircuitPython-capable development board (M0/M4 series, express recommended).
* Two momentary switches (buttons).
* A micro-USB cable.
* Connectors (jumper cables, alligator clips, solid-core wire; specifics will depend on which board you are using).
* A breadboard.

You can get all of these items from Adafruit, `here's a list <https://www.adafruit.com/wishlists/467781>`__.

I've also sourced them and similar ones from Mouser, to give you some idea of possible substitutions: `shared cart <https://www.mouser.com/ProjectManager/ProjectDetail.aspx?AccessID=b9d0704608>`__.

Amazon resellers will generally carry most of these things, even the Adafruit boards. It's a good idea to shop around, since there's a large gradient between cost, available options, shipping, and quality.

.. note::
   
   **I do not do affiliate links and do not endorse any particular storefront.**
   
   My point in providing saved carts and wishlists is to help you find what you need.
   
   |sparkleheart| That said, if given the opportunity, I will go on about Adafruit's quality and fast shipping, and this is based soley on my personal experiences with their online store and products. |unicorn| |sparkleheart|
   




The Development Board
---------------------
Any of the M0 or M4 based boards `sold by Adafruit <https://www.adafruit.com/category/957>`__ should be compatible with the code in this article. 

I am fortunate to own, in part due to recent attendance at PyCon 2018, *four* examples of the M0 boards, and have tested the code on each:

.. image:: {filename}/images/nonblocking-m0-boards-2.png
   :width: 80%
   :align: center
   
From left to right, we have 
the `CircuitPlayground Express <https://www.adafruit.com/product/3333>`__,  
the `ItsyBitsy M0 Express <https://www.adafruit.com/product/3727>`__, 
the `Trinket M0 <https://www.adafruit.com/product/3500>`__,
and the `GEMMA M0 <https://www.adafruit.com/product/3500>`__. There's also a `quarter <https://en.wikipedia.org/wiki/Quarter_(United_States_coin)>`__ for scale. On the whole, these things are *tiny*.

.. note::
   
   .. image:: {filename}/images/gemma-m0-closeup-obverse.png
      :width: 20%
      :align: right   
   
   The GEMMA M0 I have is a special edition that was included in the SWAG bag at PyCon 2018 in Cleveland Ohio. It's functionally identical to the GEMMA you get from the Adafruit shop but it's a different color and has a special Pycon 2018 marking on the back.
   
   There was not a lot of fanfare about it, but I did find a `video by Dan Bader <https://www.youtube.com/watch?v=71eAnJeQu2U>`__ talking about it, and a great `blog post by Les Pounder <https://bigl.es/friday-fun-adafruit-gemma-m0-and-neopixels/>`__ putting it through its paces.
   
   

Which board should you use? It depends on your application, as each board has it's strengths.

The GEMMA, for example, is designed for wearable tech projects - it has a battery hookup and power regulator, as well as an on/off switch. The Trinket is absolutely lilliputian in its scale and a farily basic board. Both the GEMMA and Trinket have limited pins available. The ItsyBitsy and CircuitPlayground, being express boards, have extra flash memory. The CircuitPlayground has wearable features like the GEMMA, but it has a million nifty peripherals built in. It exposes a relatively small number of pins. In contrast, the ItsyBitsy is fairly barebones like the Trinket but has a *lot* of pins available. 

The `Feather boards <https://www.adafruit.com/category/946>`__ (not pictured) have a ton of great built-in peripherals provide a standard platform for expansion boards called "`wings <https://www.adafruit.com/category/945>`__". They are a great, super-compact alternative to the old-school Arduino and Arduino Shield platform. I have an ESP8266-based Feather and one based on the ATmega32u4 with bluetooth LE, and really like the platform. 

Speaking of Arudino shields, Adafruit also makes an M0 board that's in the same form factor as the original Arduino, called the `Metro M0 Express <https://learn.adafruit.com/adafruit-metro-m0-express-designed-for-circuitpython>`__. If you've already invested in a lot of Arduino shields, this is the board for you.

In any case, **I would highly recommend doing any initial development on the CircuitPlayground Express**. It has a dizzying array of peripherals built in, plus battery and power regulation, along with a large number of easy-to-work-with pads - it's appropriate for wearable projects as well as more traditional applications. It's easy to migrate to a smaller/less featureful board when a project starts to really come together.

.. tip::
   
   If your budget allows, and especially if you are just starting out, I'd suggest springing for the `Circuit Playground Express Advanced Pack <https://www.adafruit.com/product/2769>`__. I had a couple of M0 boards and a lot of miscellaneous breakout boards before I picked up this kit, and I wish I had started with it instead.
   
   It gives you everything you need to explore the possibilities of the platform (save maybe some wire and a breadboard or two), without having to solder anything!
   

A few things to keep in mind with regard to the "lilypad" style boards (GEMMA, CircuitPlayground; so-called after one of the first "wearable" platforms, `The Adruino LilyPad <https://store.arduino.cc/usa/lilypad-arduino-main-board>`__) verses the "standard" ones (Trinket, ItsyBitsy):

* Lilypad-style boards do not require any soldering or other assembly - you can just unpack them, plug in a USB cable, and start coding. You will typically use alligator clips, or conductive thread, to connect them to other components.
* Standard boards will require some soldering. You'll either have to solder wires directly to the pin pads on the perimeter of the board, or use the provided headers.
* You can, however, solder things to the lilypad-style pads for a sturdier connection.

Connectors
----------

Alligator Clips
~~~~~~~~~~~~~~~
The CircuitPlayground has everything we need built in. It comes with two buttons soldered to the board (labeled "A" and "B"). So we don't really need any sort of connectors. For any other projects, you will need to pick up some alligator clips, but to follow along with this article, the CircuitPlayground is all you need.

.. image:: {filename}/images/aligator-clips.png
   :width: 80%
   :align: center

Alligator Clip To Jumper Wire
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Gemma will require some Aligator-to-male jumper clips to connect the breadboard where the to the Gemma pads. 

.. image:: {filename}/images/aligator-to-jumper.png
   :width: 80%
   :align: center

Jumper Wires
~~~~~~~~~~~~
Other boards will require the use of jumper wires. For the sake of this article, the pre-made kind or cut pieces of solid-core wire will work. We've used both in the example circuits below.

.. image:: {filename}/images/premade-jumper-wires-organized.png
   :width: 80%
   :align: center
   
.. image:: {filename}/images/solid-core-jumper-wires.png
   :width: 80%
   :align: center
   
.. image:: {filename}/images/nonblocking-lengths-of-wire.png
   :width: 80%
   :align: center

   

The Circuit
-----------
There are different ways you can set up buttons to work with the various M0 boards (save the CircuitPlayground, since it has them built-in), but for this article we'll use a breadboard and jumper wires. 

The circuit ties one side of each button to ground, and then the other side to a pin on the board. This means that the buttons will read "LOW" when pressed. We'll use a "pull up" resistor to keep the high voltage from "floating". The resistor is built in to the microcontroller, so we can just turn them on in software.

I chose this approach for a few key reasons:

* It keeps the component count down - you don't need anything but the buttons and some wire. The other way of hooking up the buttons, where the button is tied to 3V, would require a resistor for each button. Most microcontrollers have pull up resistors built in these days, otherwise we'd also need an additional resistor for each pin as well. 
* It's safer, since we're connecting the buttons, and ultimately the microcontroller pins, to *ground* instead of a live current. We can't do much, if any, damage if we misconfigure the pins in software, or the button is damaged (this is why we need the resistors if we were to wire the buttons up the other way). 
* It's the most commonly used approach in the vast majority of tutorials and documentation these days, because of the previous two points. If you've used momentary switches with a microcontroller before, you're likely already familiar with this type of circuit.

The trade off is that the button logic seems inverted compared to what common sense would dictate: when we press the button, it reads "LOW", and when it's not pressed, it reads "HIGH". 

The CircuitPlayground Express is wired in the reverse configuration, and requires a pull-*down* resistor turned on in software. The logic is also inverted to be "correct". This was done this way to make teaching easier with the board, but it adds an inconsistency in my little platoon of M0 development boards. This will be dealt with below.

.. tip::
   
   `Lady Ada <https://en.wikipedia.org/wiki/Limor_Fried>`__ wrote a `classic tutorial <http://www.ladyada.net/learn/arduino/lesson5.html>`__ on the subject of wiring buttons to digital inputs. It explains everything, including the concept of "floating" really well. Highly recommended reading.
   

I've used three different kinds of breadboards I had on hand, and mixed up the kinds of connectors a bit to illustrate some different ways of wiring up the buttons.

Gemma M0
~~~~~~~~

.. image:: {filename}/images/nonblocking-gemma-demo-circuit.png
   :width: 80%
   :align: center

With the Gemma, I used a "mini" breadboard. These breadboards are split into two halves by the screw holes at the top and bottom, and the "trench" in the middle. The tie points are connected in groups of five, running left to right. I've installed the buttons such that they straddle the trench. This was necessary because of a little plastic bit that sticks out between the pins.

I wanted to make sure I had easy access to the buttons, so I put all of the jumper connections on the left side. On the right side, I made a little ground "bus" by tying together the rows where I needed to connect the buttons to ground with some solid-core wire. I tied the ground jumper/alligator clip to the "bus" using a little piece of wire over the screw hole.

I clipped the black alligator clip to ground, the white one (button "A") to "D1" (also marked "A0" if you use it as an analog pin), and the yellow clip/button to "D0" ("A2").

ItsyBitsy M0 Express
~~~~~~~~~~~~~~~~~~~~

.. image:: {filename}/images/nonblocking-itsybitsy-demo-circuit.png
   :width: 80%
   :align: center

For the ItsyBitsy, I used a full-sized breadboard. On these breadboards, they have a similar split and trench down the middle. They also have a long bus on each side (top and bottom in this picture) marked negative and positive. Each group of tie points are connected. We've used them to run power from the ItsyBitsy to the rest of the board.

.. tip::
   
   The buses can be removed and multiple breadboards can be connected to form larger areas to work with.
   
For ease of access, I've tied the left and right power rails together using some solid-core wire (far left). This isn't necessary for this project (we're only tying things to ground and pins on the ItsyBitsy), but it's a useful setup so I added it for demonstration purposes.

I've seated the ItsyBitsy, fitted with the supplied headers, into the top of the breadboard (row one, on the far right). I've tied it's 3V pin (positive 3.3 volts) to the top positive bus rail, and its G pin (negative, ground) to the negative rail on the bottom. 

Because of the connections on the far left, all of the rails are live and connected like one big bus.

I've connected the buttons to ground on the top rail (rows 21, and 28).

I've connected button "A" (the grey button, white wire, row 23) to pin 11 on the ItsyBitsy (row 6 - "D11" in software). 

I've connected button "B" (the yellow button, yellow wire, row 30) to pin 7 on the ItsyBitsy (row 9 - "D9" in software).

Trinket M0
~~~~~~~~~~

.. image:: {filename}/images/nonblocking-trinket-demo-circuit.png
   :width: 80%
   :align: center

For the Trinket, I used a standard "half-sized" breadboard. It's just like the "full sized" on I used for the ItsyBitsy, but it's... half the size |thinking|.

For this circuit, I used pre-made jumper wires exclusively. 

.. tip::
    
    It's a little messier using all jumpers, but it's really easy to change things up. In fact, I originally had the buttons wired to pins on the other side of the Trinket, but it was hard to see what was going on in the pictures. It was trivial to rearrange things to make it easier to see what's what.
    
    It's always a good idea to use jumper wires to start a project, and as things take shape, slowly replace them with solid-core wires. |unicorn|
    

I seated the Trinket with attached headers on row 1 (far right). I tied its ground ('Gnd' pin) to the left ground rail (-, in this picture it's on the top).

The buttons are tied to ground on the left side (rows 13 and 19).

The "A" button (grey, white jumper) is attached to pin "~1" (row 3, "D1" in software - this pin can also be an analog output, that's why it's marked with a tilde).

The "B" button (yellow, yellow jumper) is tied to pin 2 (row 4, "D2" in software). 

CircuitPlaground Express: Problem Child
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Doing things this way with the standard boards presents a problem with our rockstar board: the CircuitPlayground Express has its buttons wired in the other manner. They require a pull-*down* resistor turned on in software, and will read "HIGH" when pressed.

Further, the pin assignments are different for every single board, and the boards differ in what kind of RGB LED they have onboard. In the next section, we'll address these minor differences with some clever Python code and the power of *abstraction*.

Abstractions: Keeping The Code Simple
=====================================
Because there are minor differences between the different boards, we're going to abstact them away using a python module. We'll call it ``setup.py``.

In programming, *abstraction* is providing an indirect way to work with something. That something might be code, concepts, a service like a database, or something physical like different development boards, as we're abstracting here.

Abstraction helps by providing a single, simplified *interface* to do things that may have a lot of complexity. 

For example, instead of building an abstraction module like we're doing below, we could have a bunch of ``if`` statements that, given we have a way to figure out what board we're running our code on, set up the right pins or pixels for us.

Something like this:

.. code-block:: python
  
  # psuedo code!
  
  if itsy-bitsy:
    set up dotstar
    use pins D7 and D11
    set up led on pin D13
  elif circuit-playground:
    set up neopixel
    use pins D4 and D5
    set up led on pin D13
  elif trinket:
    set up dotstar
    use pins D1 and D2
    set up led on pin D13
  elif gemma:
    set up dotstar
    use pins D0 and D1
    set up led on pin D13
  

The problem with this approach is that, besides being messy, it's adding a lot of extra places where our code could break. And every new board you want to use adds more complexity.

But more importantly, you have to know *every detail* of *every board* you might use. Maybe someone wants to use our code and their LED is on pin 3. Maybe they are using touch pads instead of buttons. Maybe there's some new-fangled RGB LED product (we'll call them SunSpots |trademark| |winking|) that someone wants to use. 

If we have this chain of ``if``'s, its up to *us* to add in support for these different ways of doing what we want to do. 

In an abstraction, we decide on a standard way of accessing the code, or *interface*. That means we decide that variables and functions will be named a certain way. Functions will take certain parameters and return specific kinds of values. 

.. tip::
   
   Like many terms in technology, *interface* has multiple meanings in different contexts. 
   
   We're using the term in the sense of an `application programming interface <https://en.wikipedia.org/wiki/Application_programming_interface>`__, usually abbreviated as *API*. 
   
   Be careful when searching |grin|.
   

Another term for this, that you'll hear used sometimes in computer science, is *contract*. I think that describes what the abstraction does a bit more concisely - you are saying to someone who wants to use your code "I promise that you can rely on my code working this way", and the user is saying "I agree to do things your way". 

As long as the code for each board follows the contract, and anyone using the board-specific code does so through the interface, everything works in an interchangeable way.

I like to think about the interface in terms of the actual variables and functions you use, and the contract as the understanding of what inputs and outputs the interface uses, as well as the things the interface does when you call the functions or access the variables:

.. image:: {filename}/images/abstraction-explained-1.png
   :width: 80%
   :align: center

For this simple abstraction, I've decided to make five Python objects that define our interface:

* A pixel object (``rgb``)
* The built-in RED LED, represented by a ``DigitalInOut`` object (``led``)
* 2 buttons, represented by ``DigitalInOut`` objects (``a_button``, ``b_button``)
* A function that returns the value of a button (``check()``).

These are the bits of code used by the demo project that will be different from board to board. 

We'll put them into a Python module called ``setup``. Python modules are usually just Python files, so we'll store our abstraction in a file called ``setup.py``. 

To use our abstraction, we just need to ``import setup`` and then we can access, for example, ``setup.rgb`` to mess with the RGB pixel. That actual variable might be a NeoPixel. It might be a DotStar. It might be something we've never heard of (like a SunSpot |trademark|). It could be wired to any pin, configured any way. It doesn't matter. As long as that ``rgb`` object works the same way (has the same interface) as a DotStar or NeoPixel, it complies with the *contract* and everything works:

.. image:: {filename}/images/abstraction-explained-2.png
   :width: 80%
   :align: center

|unicorn| There's even a nested abstraction here. Adafruit has already abstracted the pixel code away for us, by giving the ``DotStar`` and ``NeoPixel`` classes the same interface. So we can interact with a string of NeoPixels in the same way we can interact with a string of DotStars.

.. tip::
   
   If someone wanted to use a different kind of RGB LED (SunSpots |trademark|), as long they adhere to the interface of the abstraction Adafruit has provided, our code will still work. In fact, the SunSpots |trademark| library would work *anywhere* ``DotStar`` or ``NeoPixel`` are used.
   

Now anyone who wants to follow this article, but maybe has a `pyboard <https://store.micropython.org/product/PYBv1.1>`__ or an `ESP8266 <https://www.espressif.com/en/products/hardware/esp8266ex/overview>`__-based board can follow along without having to constantly adapt the code to their situation. All they have to do is write a ``setup.py`` module and make sure it has the expected objects.

So here's the code for each of the boards I have. 

.. note::
   
   If you are using a board that has a built-in NeoPixel, but *isn't* a CircuitPlayground, use the DotStar code, but replace the DotStar lines (lines 3, 8 and 9) with the NeoPixel code from the CircuitPlayground example.
   

For the CircuitPlayground
-------------------------

.. code-block:: python
    
    # save as setup.py
    import board
    import neopixel
    from digitalio import DigitalInOut, Direction, Pull
    
    led = DigitalInOut(board.D13)
    led.direction = Direction.OUTPUT
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 1)
    rgb.brightness = 0.3
    
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
            
.. explanation::
    
    This file will need to be saved on your ``CIRCUITPY`` drive as ``setup.py``.
    
    **Lines 2-4** import external libraries needed for this module to function.
    
    The ``board`` library contains variables that are related to your specific development board. It contains all of the pin assignments, including some handy aliases for the built-in components (like the ``board.NEOPIXEL`` variable used on **line 9**).
    
    The ``neopixel`` library gives us a way to control the 10 RGB LEDs that surround the CircuitPlayground. Depending on how your CircuitPython was installed, you may have to install this library yourself. This process is covered in detail on the `CircuitPython Libraries section <https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries>`__ of the "Welcome To CircuitPython" guide. 
    
    The basics of the ``neopixel`` library, specifically for this board, are disucessed in the `documentation <https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-neopixel>`__.
    
    NeoPixels are a hugely cool peripheral, and you are not limited to just using the ones on your CircuitPlayground Express. Check out the `NeoPixel Überguide <https://learn.adafruit.com/adafruit-neopixel-uberguide/the-magic-of-neopixels>`__ for comprehensive information about them.
    
    On **line 4**, we import a few things from the ``digitalio`` library. This library contains classes, variables and functions useful for reading and writing to digital pins (buttons, LEDs, etc). We're only importing the objects that we need to set up the buttons and built-in LED, ``DigitalInOut``, ``Direction``, and ``Pull``. Their purpose will be explained shortly.
    
    **Lines 6 and 7** set up the built-in red LED. It's attached to digital pin 13, so we pass ``board.D13`` to the ``DigitalInOut`` constructor. On **Line 7**, we set the *direction* of the pin to be an *output* - this means the pin is only going to be used for sending information, on in this case, sending power to the pin to turn on the LED.
    
    ``led`` is now a ``DigitalInOut`` object we can write to by setting its ``value`` attribute to a boolean value (``True`` or ``False``).
    
    **Lines 9 and 10** configure the NeoPixel. We call the NeoPixel object simply ``rgb`` to keep it as generic as possible. When we call the NeoPixel constructor, ``neopixel.NeoPixel``, we pass the pin where our pixels are installed (``board.NEOPIXEL``), and the number of pixels we want to illuminate. We have 10 pixels available, but since we are mimicking a board with just one built-in, we pass ``1`` to the constructor.
    
    On **Line 10** we set the brightness of the pixel to ``0.3``. The brightness is a float between ``0`` and ``1.0``. These pixels are *incredibly* bright, feel free to lower this to ``0.1`` if ``0.3`` is too intense, or increase it if you want to really light up your life. |grin|
    
    **Lines 12-14** and **lines 16-18** set up our buttons. In the case of the CircuitPlayground, these are the built-in buttons, and need a pull-down resistor turned on to function. The pins are supplied via the ``board`` module. The direction is set just like the ``led`` on **line 6**, but in this case the direction is set to ``Direction.INPUT``, because these are pins to be *read* from, instead of written to. Finally on **lines 14 and 18**, we enable the pull-down resistor using the ``pull`` property and the ``Pull`` object from the ``digitalio`` module.
    
    Finally, on **lines 20-24**, we define a function called ``check()``. The purpose of this function is to abstract away the differences between how these various boards are wired up. In the case of the CircuitPlayground, the onboard buttons are wired in the "sane" manner such that pressing the button causes the pin to read ``True``, and not pressing the button, causes the pin to read ``False``. This is the opposite of how the other boards are configured. 
    
    This function will always return ``True`` if the button is pressed, and ``False`` if it's not, regardless of how the buttons are set up. 
    
    ``check()`` takes a single parameter, ``token``, which is used to indicate which button you want to check the value of. It's a simple string - when it's set to "A", ``check()`` returns the value of the "A" button (``button_a``), and when it's set to "B", ``check()`` returns the value of the "B" button (``button_b``). 
    
    
For the other boards with DotStars
----------------------------------

.. note::
   
   Be sure to change the pin numbers to reflect how you wired up your buttons.
   

.. code-block:: python
    
    # save as setup.py
    import board
    import adafruit_dotstar
    from digitalio import DigitalInOut, Direction, Pull
    
    led = DigitalInOut(board.D13)
    led.direction = Direction.OUTPUT
    
    rgb = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
    rgb.brightness = 0.3
    
    a_button = DigitalInOut(board.D4)
    a_button.direction = Direction.INPUT
    a_button.pull = Pull.UP
    
    b_button = DigitalInOut(board.D3)
    b_button.direction = Direction.INPUT
    b_button.pull = Pull.UP
    
    def check(token):
        if token == "A":
            return not a_button.value
        if token == "B":
            return not b_button.value 
            
            
.. explanation::
    
    This file will need to be saved on your ``CIRCUITPY`` drive as ``setup.py``.
    
    **Lines 2-4** import external libraries needed for this module to function.
    
    The ``board`` library contains variables that are related to your specific development board. It contains all of the pin assignments, including some handy aliases for the built-in components (like the ``board.APA102_SCK`` variable used on **line 9**).
    
    The ``adafruit_dotstar`` module provides a way to control DotStars. DotStars are like NeoPixels, but use a different protocol. The differences are explained on `the DotStar LED docuemntation page <https://learn.adafruit.com/adafruit-dotstar-leds/overview>`__. 
    
    You will have to install the ``adafruit_dotstar`` library. This process is covered in detail on the `CircuitPython Libraries section <https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries>`__ of the "Welcome To CircuitPython" guide. 
    
    The details of working with the DotStar library in CircuitPython is covered in `the CircuitPython DotStar section <https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar>`__ of the CircuitPython Essentials document.
    
    On **line 4**, we import a few things from the ``digitalio`` library. This library contains classes, variables and functions useful for reading and writing to digital pins (buttons, LEDs, etc). We're only importing the objects that we need to set up the buttons and built-in LED, ``DigitalInOut``, ``Direction``, and ``Pull``. Their purpose will be explained shortly.
    
    **Lines 6 and 7** set up the built-in red LED. It's attached to digital pin 13, so we pass ``board.D13`` to the ``DigitalInOut`` constructor. On **Line 7**, we set the *direction* of the pin to be an *output* - this means the pin is only going to be used for sending information, on in this case, sending power to the pin to turn on the LED.
    
    ``led`` is now a ``DigitalInOut`` object we can write to by setting its ``value`` attribute to a boolean value (``True`` or ``False``).
    
    **Lines 9 and 10** configure the DotStar. We call the DotStar object simply ``rgb`` to keep it as generic as possible. DotStars are connected via `SPI <https://en.wikipedia.org/wiki/Serial_Peripheral_Interface>`__, so they require two pins to be specified in the constructor. We use the ``board`` library to provide the two built-in pins that are pre-wired to all built-in DotStars, ``board.APA102_SCK`` and ``board.APA102_MOSI``. Finally we pass ``1`` to the constructor, to let the library know we are only controlling the single DotStar.
    
    On **Line 10** we set the brightness of the pixel to ``0.3``. The brightness is a float between ``0`` and ``1.0``. These pixels are *incredibly* bright, feel free to lower this to ``0.1`` if ``0.3`` is too intense, or increase it if you want to really light up your life. |grin|
    
    **Lines 12-14** and **lines 16-18** set up our buttons. The pins are supplied via the ``board`` module. The direction is set just like the ``led`` on **line 6**, but in this case the direction is set to ``Direction.INPUT``, because these are pins to be *read* from, instead of written to. On these boards, we've wired all of the buttons so they connect to ground when pressed, so we have to use a pull up resistor so they function properly (**lines 14 and 18**) . This also means that our logic will be inverted relative to other wirirings (and common sense) - when the button is pressed, the pin will read ``False``, and when it's not pressed, it will read ``True``.  
    
    Finally, on **lines 20-24**, we define a function called ``check()``. The purpose of this function is to abstract away the differences between how these various boards are wired up. On **lines 22 and 24**, we use the ``not`` operator to negate whatever we got from the button pin. This normalizes the output between these boards, and boards like the CircuitPlayground that are wired in the opposite manner.
    
    This function will always return ``True`` if the button is pressed, and ``False`` if it's not, regardless of how the buttons are set up. 
    
    ``check()`` takes a single parameter, ``token``, which is used to indicate which button you want to check the value of. It's a simple string - when it's set to "A", ``check()`` returns the value of the "A" button (``button_a``), and when it's set to "B", ``check()`` returns the value of the "B" button (``button_b``).

How It Works
------------
To use this in our other code (``code.py``), we just need to use Python's ``import`` statement:

.. code-block:: python
    
    from setup import led, rgb, check
    
    
Now, in our code, we use the ``led`` variable to turn the red LED on/off, and use ``rgb`` to control the NeoPixel/DotStar. We will use the ``check()`` function to see if a button is being pressed, like this:

.. code-block:: python
    
    if check("A"):
        print("Button A has been pressed")
    else:
        print("Button A has not been pressed")
        
    if check("B"):
        print("Button B has been pressed")
    else:
        print("Button B has not been pressed")
        

    
Testing
=======
Before digging into state and other fun stuff, its a good idea to run some super simple code to ensure that everything is wired up properly. I've written some minimalistic code you can use to verify everything is set up.

What this code does is turn the on the onboard LED when button "A" is pressed, and the RGB LED (either a dotstar for the ItsyBitsy, Trinket, or GEMMA boards, or a NeoPixel in the case of the CircuitPlayground) when button "B" is pressed.

.. tip::
   
   For details about controlling the onboard RGB LEDs, see `Adafruit's excellent documentation on the subject <https://learn.adafruit.com/circuitpython-essentials/circuitpython-internal-rgb-led>`__.
   

Before running this code, make sure you've copied the proper RGB LED library over to your board, in the ``lib`` folder.

.. tip::
   
   If you aren't familiar with this process, check out the `CircuitPython Libraries <https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries>`__ section of the `"Welcome To CircuitPython" <https://learn.adafruit.com/welcome-to-circuitpython/overview>`__ guide.
   
Also make sure you have created a ``setup.py`` module, as explained in `the last section <Abstractions: Keeping The Code Simple_>`__. 

.. code-block:: python
    
    import time
    from setup import led, rgb, check
    
    while True:
        led.value = check("A")
        
        if check("B"):
            rgb[0] = (255, 255, 255)
        else:
            rgb[0] = (0, 0, 0)
        
        time.sleep(0.2)
        
.. explanation::
   
   * **Lines 1 and 2** import the necessary external objects and modules we need.
   * The `time <https://circuitpython.readthedocs.io/en/3.x/shared-bindings/time/__init__.html>`__ module provides functions related to the passage of time, usually in terms of seconds.
   * **Line 4** starts off the standard "main loop" where our code runs. 
   * On **Line 5**, we set the value of the ``led`` object, or the red LED wired to pin 13, to whatever the value of the "A" button happens to be at that moment. If the value is ``True`` (the button is pressed), the LED will turn on. If it's ``False`` (the button is not pressed), the LED will turn off.
   
   **Lines 7-10** have a similar function to line 5, except that the RGB LEDs are not simple on/off devices. They must have a color of some kind written to them, usually a tuple of three integers, each ranging from 0 to 255. Each integer in the tuple corresponds to a red, green, and blue LED element in the pixel (respectively), and sets its intensity level.
   
   The NeoPixel and DotStar libraries provide an interface such that you can treat the pixel object like a standard Python list. This is how we are able to write a color to the first pixel using list indexing on **lines 8 and 10**.
   
   In the case of **line 10**, we're writing "black" to the pixel by setting the red, green and blue values to 0 (by passing the tuple ``(0, 0, 0)``). This has the effect of turning it off, in the same way that setting the ``led.value`` property to ``False`` turns the red LED on pin 13 off.
   
   Finally on **line 12**, we call ``time.sleep()`` to pause the program for 0.2 seconds. This provides simple button debouncing (much more about button bounce will be discussed in the rest of this article, stay tuned).
   

Here's a short video demonstrating the test code and demo circuit on each of the boards I have:
        
.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/videos/non-blocking-events-circuitpython/test-circuit-demo-all-boards.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/videos/non-blocking-events-circuitpython/test-circuit-demo-all-boards.mp4">link to the video</a> instead.</p>
       </video>
   </div>


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

We've already looked at code that blocks in the `Testing`_ section above. We're using a Python function called ``time.sleep()`` that pauses processing for a given period of time (provided in seconds). 

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

Lets apply state tracking to our `testing code <Testing_>`__. Recall that to test our board, we set up a simple project that has the following functionality:

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
    
    Remember this code is assuming you have created a ``setup.py`` file as explained `earlier <Abstractions: Keeping The Code Simple_>`__.
    
    

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
--------
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
--------------------------------------
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
------------------------------------
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
#. We may run into memory issues and the easiest way to save some memory is to `compile this complex code into an MPY file <Compile Modules Into MPY Files_>`__. 

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
   
   This is including our `setup.py module <Abstractions: Keeping The Code Simple_>`__ - so we're also loading the DotStar library and setting up both buttons, even though neither are necessary for this code. 
   

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


