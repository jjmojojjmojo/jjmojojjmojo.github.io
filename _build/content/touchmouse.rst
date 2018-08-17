TouchMouse: A CircuitPython Project To Reduce Input Fatigue
###########################################################
:date: 2018-06-11 15:07
:author: lionfacelemonface
:category: tutorial
:tags: tutorial; circuitpython; hardware;
:slug: touchmouse
:status: draft

.. include:: ../emojis.rst

I had a need for creating a custom peripheral, a computer mouse |mouse| that would require as little force as possible to click, and scroll. 

I found the tech I needed in the Adafruit M0 series of development boards. They include both USB HID functionality *and* capacitive touch capabilities. 

They can be programmed with CircuitPython, Adafruit's fork of MicroPython for the chip that the M0 boards run (the `ATSAMD21 Cortex M0 microprocessor <https://www.microchip.com/wwwproducts/en/ATSAMD21G18>`__). I've got extensive Python experience, so it was an obvious choice for my platform.

This article chronicles my first-pass in designing and building a touch-based device that takes the place of the mouse buttons and scroll wheel.

.. PELICAN_END_SUMMARY

Overview
========

Requirements
============

Materials List
==============

The Touchmouse Project: The Touch Board
=======================================
While the touch inputs can be anything conductive, fruit, pieces of metal, even a bare wire works, or you can just just the pins or pads on the microcontroller. However, this is a great use for copper foil tape with conductive adhesive. 

I have two widths, 2 inch and 1/4 inch. I use the 2 inch to make large touch pads, and the 1/4 inch to run traces from the pads to the edges of the substrate so the alligator clips can clip on securely.

Alternatively, you could solder wires between the traces or pads and the microcontroller, but we should reserve this for when we're building our final project. 

I used a piece of corrugated plastic I had on hand as a substrate. Whatever you use, try to select something that is electrically inert, and thick enough (or insulating enough) that you can utilize both sides simultaneously. This gives you much more flexibility when routing your connections. 

Some other good choices include:

* cardboard
* foamcore
* mat board
* book board
* MDF
* plywood

Be sure to choose something that can resist high temperatures if you plan on making the board a permanent part of your project by soldering leads to it.

It may take some trial and error to choose a substrate that fits your application.

.. tip::
   
   The "end game" for these sort of user interfaces is to use printed circuit board (PCB) material  - copper clad fiberglass (most commonly the type designated 'FR4'). You can use an acid etching process in concert with a laser printer (or even permanent marker) and do this yourself, or you can use a low-run PCB manufacturing service to do the work for you.
   
Mockup
------
   
I initially mocked up my touch pads using green masking tape. In laying out the pads, the primary goal is to put the touch-sensitive areas in logical and convenient locations. Secondarily, they can't be too close together, or we can get crosstalk between the pads. The final concern is placement of the leads that connect to the microcontroller.

It's important that the leads won't be accidentally grazed by our hands. We also don't want them to be awkwardly placed - our microcontroller board needs to comfortably connect and, especially in the case of this project, it needs to be visible. 

.. image:: {filename}/images/touchmouse-prototype-front.png
   :width: 80%

As you can see in the photograph, I've set up 4 touch pads. The two larger ones on the left (yellow) and right (green) will be left and right mouse clicks, respectively. We'll also trigger a middle click if both pads are touched at the same time. 

The two middle pads will emulate the scroll wheel on a typical mouse. The top pad (blue) will scroll up, and the bottom (white) will scroll down. 

I settled on connecting the leads to the top edge of the panel. This works well for the scroll up, left and right pads, but we'll need to run a trace to connect the scroll down pad to the top edge. 

We could run the trace on the front side of the panel - we have room under the right or left click pads after all. This isn't the best idea though. When we add more conductive material to a pad, even if it's for the sake of connecting it to our microcontroller, we are essentially making the pad *bigger*. Even the alligator clips we're using will become part of each of our pads. So it's possible that we'd accidentally graze the trace when touching the click pads, inadvertently sending a scroll command to the computer when we're trying to click. This is especially possible (and problematic!) when we're trying to do something like a click-drag. 

So what I did to avoid this was run the trace on the obverse side of the panel:

.. image:: {filename}/images/touchmouse-prototype-back.png
   :width: 80%
   
Note that I was careful to avoid crossing the left click pad on the other side of the panel. This is to ensure we don't accidentally activate both pads. Capacative touch is pretty amazing in that it works even at a slight distance. We can take advantage of this to do some cool things, like creating a grid of touch inputs using a limited number of pins, but it's not what we want here.

.. tip::
   This is how projected capacitive multi-touch monitors work. 
   


Granted, this plastic material I'm using is a really good insulator (it's mostly air), so it's not big concern, but it's best to be conservative. 

The Overlay
===========

I opted to create an overlay for the touch pads. 

This gives us the opportunity to add more visual indicators as to where the pads are, and what each pad does. It also prevents tarnishing of the pads from oils in your skin.

I ended up using it as the guide for applying the conductive materials as well.

I used some light cardstock that I had on hand. I cut the cardstock with a utility knife and a straight edge and glued the pieces together with a glue stick. 

.. image:: {filename}/images/touchmouse-overlay-tools.png
   :width: 80%

Here's the finished product, laying on top of the masking tape mock-up:

.. image:: {filename}/images/touchmouse-overlay.png
   :width: 80%
   
After making sure everything lined up properly, I took a final finishing touch and ran the overlay through my trusty Scotch TL901 laminator. 

.. image:: {filename}/images/touchmouse-laminator.png
   :width: 80%

I laminated the overlay for a couple of reasons. First, it will make the overlay more durable - it will be water-proof, so it will resist spills and can easily be cleaned by wiping it down with a damp cloth. 

Second, it adds a little bit of extra insulation - my hands are a bit shaky, and the little bit of extra buffer makes my touches more accurate (we'll dig into that more a bit later). 

Finally, it allows me to use water soluble markers to add notes or legends to my overlays, that can be easily changed.

.. image:: {filename}/images/touchmouse-overlay-laminated-markedup.png
   :width: 80%

I used Staedtler Lumocolor "correctable" markers, but there are other brands, like the Expo® Vis-a-vis®. They work a lot like dry-erase markers, except they are a bit more durable. They resist minor friction well. They are erasable with water. 

When I was younger they were the mainstay of any teacher using an overhead projector. The color markers are transparent, so the color shows through when back-lit. 

They also work great as semi-permanent markings for whiteboards.

.. tip::
   
   If you need something more durable but still temporary, you can use a *china marker*. These are wax crayons used for marking pottery (that's where "china" in the name comes from). They erase from a smooth surface with alcohol (hand sanitizer works great in a pinch).
   
The Pads
--------
   
Before I laminated it, I used my overlay as a guide to lay out the front pads on the panel:

.. image:: {filename}/images/touchmouse-overlay-lineup.png
   :width: 80%
   
Then I cut my pads out of 2" copper foil tape, using the same stright edge and utility knife, and laid them out to make sure everything was OK:

.. image:: {filename}/images/touchmouse-overlay-front-mockup.png
   :width: 80%
   
Copper foil tape has a paper backing. Once everything looked good I removed it, and applied it to the panel. I used my overlay again as a guide:

.. image:: {filename}/images/touchmouse-overlay-and-front-pads.png
   :width: 80%
   
The copper is pretty pure, so it's malleable - it's pretty easy to "nudge" if you need to, but it's also easy to tear, so be careful. 

You will want to lightly burnish the foil with a fingernail or bone folder just to ensure good adhesion. This is especially important if you are layering the foil over something conductive (for example, other layers of copper foil tape).

Next, I held the panel up to a lamp and marked where the pads were so I could apply the copper trace on the back side that takes the "scroll down" pad and brings it up to the top edge:

.. image:: {filename}/images/touchmouse-overlay-lineup-back-trace.png
   :width: 80%

I cut pieces of 1/4" copper foil tape for the main part of the trace, and I found a piece of scrap from the other pads to use for connecting the back of the panel to the "scroll down" pad on the front:

.. image:: {filename}/images/touchmouse-back-trace-mockup.png
   :width: 80%
   
I ran the tape as close to the edge as I could without touching it, and then up on the right side far away from the "left click" pad.
   
When I applied the tape to the back panel, I had two problems. I was a little bit short, since I wanted to wrap the 1/4" tape around the top to the front side so I could see it easily for connecting an alligator clip. The other problem is that I tore the tape a little bit running the trace up to the top.

The solution to both problems was to cut up some more scrap foil and apply it to the problem areas:

.. image:: {filename}/images/touchmouse-back-trace-patch.png
   :width: 80%
   
I was sure to burnish the foil down securely.
   
.. image:: {filename}/images/touchmouse-back-trace-complete.png
   :width: 80%
   
Here's what the pads look like from the front, now that everything is complete:

.. image:: {filename}/images/touchmouse-overlay-front-complete.png
   :width: 80%
   
Testing
-------
For a basic test of our pad, we'll simply test *continuity*. Continuity tells us if two points on a circuit are connected. 

.. tip::
   
   For some more detail and how to get into continuity mode on several multimeters, `Adafruit has a nice article <https://learn.adafruit.com/multimeters/continuity>`__ you should check out.
   
First, we'll change our multitester into continuity or "diode test" mode:

.. image:: {filename}/images/touchmouse-testing-pads.png
   :width: 80%
   
When there is no continuity (a.k.a. "open loop"), the meter will read 1. Otherwise, it will show the voltage running between the leads. It takes a second or two to settle down, and in the case of a short circuit (if you touch the leads together, or touch them to the same piece of metal), you'll see a very low number.

It's not important which lead is used where in this case - we're just checking if there's continuity, so polarity doesn't factor in.

Here's a video showing how I tested the pads. Note that I also checked to be sure the pads weren't accidentally connected, by touching one probe to one pad and the other to a separate one. 

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{filename}/images/IMG_6777.webm" type="video/webm">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{filename}/images/IMG_6777.webm">link to the video</a> instead.</p>
       </video>
   </div>

The most important test is the "scroll down" pad, since that's the most likely pad to be messed up given it's a series of separate layered pieces of foil, that run over quite a bit of distance. I placed one lead on the pad, and the other on the spot where I intend to hook up the aligator clip. As you can see from the video, there's a solid connection there. 

Finishing Up
------------
I used a couple of wide rubber bands to hold the overlay onto the touch panel. This secures the overlay well, and also provides a non-slip surface to keep the panel from sliding around during use.

.. image:: {filename}/images/touchmouse-overlay-final.png
   :width: 80%


Wiring - CircuitPlayground
==========================
Since the neopixels, DAC, and speaker are all built in to the CircuitPlayground, wiring it up is really simple - we just need to connect the aligator clips to the pads on the CircuitPlayground. 

We can use any pads marked A1-A7 (A0 will be used to drive the speaker). 

.. warning::
   Before connecting the wires, make sure the USB cable is *unplugged*. There are a couple of reasons for this. 
   
   First, we don't want to accidentally short anything. This is good practice in general.
   
   Second, and this is specific to our project, the touch pads are calibrated when the board first boots up. We want to let it do that properly.

I've evenly spaced the connections around the CircuitPlayground to reduce stress on the clips. My aligator clips are a bit long, so I also had to twirl the leads a bit so the CircuitPlayground was as close to the touch panel as possible. 

.. image:: {filename}/images/touchmouse-circuitplayground-wiring.png
   :width: 80%

In close-up, you can see that I've connected the alligator clips as follows:

* Scroll Down, white, is connected to A7.
* Left Click, yellow, is connected to A4.
* Scroll Up, blue, is connected to A1.
* Right Click, green, is connected to A3.

.. image:: {filename}/images/touchmouse-circuitplayground-wiring-closeup.png
   :width: 80%

Testing - Touch Pads
--------------------
To ensure everything is hooked up correctly, we'll run some testing code. This is the bare minimum code needed to work with touch interfaces.

.. code-block:: python
    
    ﻿# save as code.py
    import board
    import time
    import touchio
    
    scroll_down = touchio.TouchIn(board.A7)
    left_click = touchio.TouchIn(board.A4)
    scroll_up = touchio.TouchIn(board.A1)
    right_click = touchio.TouchIn(board.A3)
    
    ﻿while True:
        if scroll_down.value:
            print("Scroll down pressed")
            
        if left_click.value:
            print("Left click pressed")
            
        if scroll_up.value:
            print("Scroll up pressed")
            
        if right_click.value:
            print("Right click pressed")
            
        time.sleep(0.2)

Here's a video of the code in action:

.. raw:: html
   
   <div class="video-container">
   <strong>VIDEO TBD</strong>
   </div>
   
This code is blocking, so it's not the way we want to work long-term, but it's acceptible for just verifying that the touch interface works. It's also useful for debugging if we run into trouble later.
   
Testing - Neopixels
-------------------
Now that the basic touch interface is built and working, we can verify the neopixels are functional.

In the CircuitPlayground, the neopixel ring is wired to digital pin 17, but we will use the safer ``board.NEOPIXEL`` object that CircuitPython provides - this also makes porting our code a little easier, but bare in mind that on Adafruit's  CircuitPython boards, ``board.NEOPIXEL`` maps to a single onboard neopixel used for status.

This is bare-minimum code to verify all 10 built-in neopixels are working. It also shows off the very clever list-like interface that the ``NeoPixel`` object provies, and gives you visual confirmation of the *order* that the pixels are addressed. In the case of the CircuitPlayground, the first neopixel is to the left of the micro-USB jack, just below the green "on" LED.

.. code-block:: python
    
    ﻿# save as code.py
    import board
    import time
    import neopixel
    
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)
    pixels.fill(black)
    
    pixels[::] = [red, white, blue, white, blue, white, blue, white, blue, white]
    
    while True:
        pixels[::] = [pixels[-1]] + pixels[0:-1]
        time.sleep(0.5)
    

Here's a video of the code in action:

.. raw:: html
   
   <div class="video-container">
   <strong>VIDEO TBD</strong>
   </div>

.. tip::
   You may notice, especially at lower brightness levels, that the colors seem a little off. This is due to the slight variance in the wavelengths of the three LEDs that make up each neopixel. This can be accounted for, and we'll be dealing with that later, using the `FancyLED library <https://learn.adafruit.com/fancyled-library-for-circuitpython/overview>`__.
   
   
Testing - Audio
---------------
CircuitPlayground has a built-in speaker and DAC connected to pin ``A0``.

We'll test the built-in speaker with some simple code that will play a WAV file. 

.. tip::
   We could also generate a noise ourselves, as shown in `the Adafruit docs <https://learn.adafruit.com/adafruit-circuit-playground-express?view=all#basic-tones>`__. This is worth checking out because it's super simple and has some really cool possibilities (want to make your own synthesizer? theramin? this is what you need)
   
   So, this would be the best way to test this, given it doesn't require any external files. However, we're going to use WAV files in our final project, so it's more prudent to create a slightly more realistic testing scenario.
   
The first thing we'll need to do is procure a couple of properly-formatted WAV files to play. The requirements and process are described `here <https://learn.adafruit.com/adafruit-wave-shield-audio-shield-for-arduino/convert-files>`__. I've found some files from `freesound.org <http://www.freesound.org>`__, and converted them to the right format. 

`This <{filename}/images/coin.wav>`__ file is an "8-bit coin sound". Before running the code below, copy it to the root folder of the CircuitPlayground.

This code will play that sound once when the board first boots:

.. code-block:: python
    
    ﻿# save as code.py
    import audioio
    import board
    from digitalio import DigitalInOut, Direction
    
    # enable the speaker
    spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
    spkrenable.direction = Direction.OUTPUT
    spkrenable.value = True
    
    filename = "coin.wav"
    
    print("playing file " + filename)
    f = open(filename, "rb")
    a = audioio.AudioOut(board.A0, f)
    a.play()
    
.. tip::
   The example code on the `Adafruit site <https://learn.adafruit.com/adafruit-circuit-playground-express?view=all#playing-audio-files>`__ blocks - this isn't necessary, it's just so they can log "finished" after the wav is complete. The ``audioio`` library is non-blocking.
   
Here's what it looks/sounds like:

.. raw:: html
   
   <div class="video-container">
   <strong>VIDEO TBD</strong>
   </div>
   
Testing - Mouse Interface
-------------------------
The mouse and keyboard functionality of the M0 boards is really straightforward.

Here's some code that turns the A and B buttons into a left and right mouse
click, respectively.

.. code-block:: python
   
    # save as code.py
    ﻿import board
    import time
    from adafruit_hid.mouse import Mouse
    from digitalio import DigitalInOut, Direction, Pull
    
    mouse = Mouse()
    a_button = DigitalInOut(board.D4)
    a_button.direction = Direction.INPUT
    a_button.pull = Pull.DOWN
    
    b_button = DigitalInOut(board.D5)
    b_button.direction = Direction.INPUT
    b_button.pull = Pull.DOWN
    
    while True:
        if a_button.value:
            mouse.click(Mouse.LEFT_BUTTON)
    
        if b_button.value:
            mouse.click(Mouse.RIGHT_BUTTON)
            
        time.sleep(0.2)
        
You'll note that while clicks work in the typical way, it's not possible to
emulate full mouse functionality using simply the ``mouse.click()`` method - in
particular, dragging doesn't work with the code above. 

When we implement this in our final project, we'll make use of our generic state
code to send a ``mouse.press()`` when the given touch pad is pressed, and
``mouse.release()`` when it's released. This will provide full mouse
functionality.

Wiring - ItsyBitsy
==================

Getting Fancy: Gamma Correction For Neopixels
=============================================
Given that capacative touch doesn't provide any tactile feedback, I want to give
the user other forms of feedback. The first is visual. 

To do so, I'm using LEDs, namely *NeoPixels*. We've got 10 built in to the
CircuitPlayground, and they are easy to add to other platforms. 

NeoPixels, AdaFruit's brand of addressable LEDs, are composed of three (or four, in the case of RGBW pixels) micro-sized LED elements, attached to a tiny microcontroller, housed in a surface-mount package. 

They operate in a manner very similar to "traditional" RGB LEDs, in that they have a common power supply, a red, green, and blue LED element, and each LED element can be controlled independently. Pulse-width-modulation is possible as well, but in the case of NeoPixels, the PWM of each LED element is controlled by the onboard microcontroller. NeoPixels also provide a means of communication such that they only require one wire to connect to a microcontroller (besides ground and power), and can be daisy-chained practically to infinity, yet stll individually addressed. This greatly simplifies adding them to a project - where adding a single RGB LED would require 3 digital, PWM-capable inputs, adding a string of, say, 10, or several dozen, NeoPixels only requires *one pin*. 

.. tip::
   
   Adafruit has an amazing, comprehensive `NeoPixels Überguide <https://learn.adafruit.com/adafruit-neopixel-uberguide/the-magic-of-neopixels>`__ that is **required reading** if you plan to do much work with these little marvels.
   

.. note::
   
   NeoPixels can consume a *lot* of power. If you are using more than 10 or so in your project, you will want to consider using an external power supply. 
   

With most neopixels, you can (theorhetically) create 16,581,375 unique colors. 

However, this assumes that the wavelengths of light emitted from each element are as broad as the spectrum of light we get from standard lightbulbs, or our sun. 

Since they aren't, colors don't quite mix as simply as we would expect.

This code illustrates the problem:

.. code-block:: python
    
    # save as code.py
    ﻿import board
    import neopixel
    
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)
    
    red = (255, 0, 0)
    ornangeish_red = (226, 87, 30)
    orange = (255, 127, 0) 
    yellow = (255, 255, 0) 
    green = (0, 255, 0)
    bluegreen = (150, 191, 51)
    blue = (0, 0, 255)
    indigo = (75, 0, 130)
    violet = (139, 0, 255)
    white = (255, 255, 255)
    
    
    pixels[::] = (red, ornangeish_red, orange, yellow, green, bluegreen, blue, indigo, violet, white)
    
    
As you can see, the colors aren't quite what we expect. This is especially noticable at lower brightness levels.

AdaFruit has a CircuitPython port of an Arduino library called FastLED that they call FancyLED, that solves this problem.

The way it solves the problem is by adjusting each color by a known offset based on the wavelengths of each LED element. 

Here's the same code, using FancyLED:

.. code-block:: python
    
    # save as code.py
    ﻿import board
    import neopixel
    import adafruit_fancyled.adafruit_fancyled as fancy
    
    brightness = 0.1
    
    ﻿pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=brightness)
    
    fancy_red = fancy.gamma_adjust(fancy.CRGB(255, 0, 0), brightness=brightness).pack()
    fancy_ornangeish_red = fancy.gamma_adjust(fancy.CRGB(226, 87, 30), brightness=brightness).pack()
    fancy_orange = fancy.gamma_adjust(fancy.CRGB(255, 127, 0), brightness=brightness).pack() 
    fancy_yellow = fancy.gamma_adjust(fancy.CRGB(255, 255, 0), brightness=brightness).pack() 
    fancy_green = fancy.gamma_adjust(fancy.CRGB(0, 255, 0), brightness=brightness).pack()
    fancy_bluegreen = fancy.gamma_adjust(fancy.CRGB(150, 191, 51), brightness=brightness).pack()
    fancy_blue = fancy.gamma_adjust(fancy.CRGB(0, 0, 255), brightness=brightness).pack()
    fancy_indigo = fancy.gamma_adjust(fancy.CRGB(75, 0, 130), brightness=brightness).pack()
    fancy_violet = fancy.gamma_adjust(fancy.CRGB(139, 0, 255), brightness=brightness).pack()
    fancy_white = fancy.gamma_adjust(fancy.CRGB(255, 255, 255), brightness=brightness).pack()
    
    pixels[::] = (fancy_red, fancy_ornangeish_red, fancy_orange, fancy_yellow, fancy_green, fancy_bluegreen, fancy_blue, fancy_indigo, fancy_violet, fancy_white)
    
The colors are about the same brightness, but the colors are much more true to
our intent - this is epseically apparent in the "in-between" colors like
"orangeish red", blue green, and indigo. 

Bringing It All Together
========================
At this point we have all of the elements worked out. 

We have:
* A well engineered state and event dispatch pattern
* A nice low-tech touchpad.
* Code that allows us to read touch inputs.
* Code that can play sounds.
* Code that can turn on neopixels.
* Code that can gamma-correct neopixels so the colors look right.
* Code for sending mouse events to the computer.

All of the elements are here, so lets dig into the precise functionality that our touch mouse will provide:

#. **Basic Mouse Functionality.** We have four pads, and they will provide left click, right click, scroll up and scroll down mouse actions. It will support click-drag, and will scroll faster the longer you hold your finger on the scroll up/down pads. If the left and right pads are pressed at the same time, it will be interpreted as a middle-click.
#. **Audio Feedback.** When a pad is touched, the touchmouse will play a sound.
#. **Visual Feedback.** When a pad is touched, the touchmouse will light up its neopixels. The patterns will change depending on which touch pad was pressed:
    
    * The top half will light up when scrolling up.
    * The bottom half will light up when scrolling down.
    * The left half will light up when the left pad is being pressed.
    * The right half will light up when the right pad is being pressed.
    
    The exact colors and/or patterns will be determined by the asetic choices of the programmer.
    
As a first pass, we'll set up all of our objects and inputs and stub out our functionality, printing to the console instead of sending mouse events. 

.. code-block:: python
    
    # save as code.py
    ﻿import board
    import time
    import neopixel
    import audioio
    import touchio
    from dispatch import ButtonDispatch
    from adafruit_hid.mouse import Mouse
    import adafruit_fancyled.adafruit_fancyled as fancy
    from digitalio import DigitalInOut, Direction
    
    class State:
        def __init__(self):
            self.left = False
            self.right = False
            self.up = False
            self.down = False
            self.left_holding = False
            self.right_holding = False
            self.up_holding = False
            self.down_holding = False
            self.brightness = 0.1
    
    state = State()
    
    spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
    spkrenable.direction = Direction.OUTPUT
    spkrenable.value = True
    
    mouse = Mouse()
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=state.brightness)
    
    pads = {
        "down": touchio.TouchIn(board.A7),
        "left": touchio.TouchIn(board.A4),
        "up": touchio.TouchIn(board.A1),
        "right": touchio.TouchIn(board.A3)
    }
    
    def check(token, state):
        return pads[token].value
        
    ﻿def up_press(token, state):
        print("Up press")
        
    def down_press(token, state):
        print("Down press")
        
    def scroll_up(token, hold_count, state):
        print("Scrolling up")
        
    def scroll_down(token, hold_count, state):
        print("Scrolling down")
        
    def left_press(token, state):
        print("Left press")
        
    def left_release(token, state):
        print("Left release")
        
    def right_press(token, state):
        print("Right press")
        
    def right_release(token, state):
        print("Right release")
    
    buttons = [
        ButtonDispatch("down", check, state, down_press, None, scroll_down),
        ButtonDispatch("up", check, state, up_press, None, scroll_up),
        ButtonDispatch("left", check, state, left_press, left_release),
        ButtonDispatch("right", check, state, right_press, right_release)
    ]
    
    while True:
        for dispatch in buttons:
            dispatch()
            
Next, we'll add the button click sound effect:

.. code-block:: python
    
    ﻿# ... snip ...
    
    def click_sound():
        filename = "click.wav"
        print("Playing sound {}".format(filename))
        
        f = open(filename, "rb")
        a = audioio.AudioOut(board.A0, f)
        a.play()
    
    def up_press(token, state):
        click_sound()
        print("Up press")
        
    def down_press(token, state):
        click_sound()
        print("Down press")
        
    def scroll_up(token, hold_count, state):
        click_sound()
        print("Scrolling up")
        
    def scroll_down(token, hold_count, state):
        click_sound()
        print("Scrolling down")
        
    def left_press(token, state):
        click_sound()
        print("Left press")
        
    def left_release(token, state):
        print("Left release")
        
    def right_press(token, state):
        click_sound()
        print("Right press")
        
    def right_release(token, state):
        print("Right release")
    
    buttons = [
        ButtonDispatch("down", check, state, down_press, None, scroll_down),
        ButtonDispatch("up", check, state, up_press, None, scroll_up),
        ButtonDispatch("left", check, state, left_press, left_release),
        ButtonDispatch("right", check, state, right_press, right_release)
    ]
    
    while True:
        for dispatch in buttons:
            dispatch()
            
            
Next, we'll add the neopixels:

.. code-block:: python
   
   # code here that adds neopixels but fails because of memory issues
   
Addressing Memory Issues
------------------------

* Consolidate functions
* Move code into mpy libraries
* Avoid array slicing
* Get rid of unnecessary dependencies
* Precalculate values
* Remove debugging/comments
* Only update objects when necessary
* Drop features
* Offload to external boards (e.g. use the audioFX board instead of onboard audio playback). Can we also use a smaller/cheaper board like the Gemma or trinket to do some of the stuff, like running the neopixels and communicate over SPI or I2C?
* Switch to Arduino (CircuitPython is designed for "beginners", if we're having memory issues it may be a sign that we have "grown out" of the platform).

Code With Neopixels And Sound
-----------------------------

.. code-block:: python
    
    ﻿import board
    import time
    import neopixel
    import audioio
    import touchio
    from dispatch import ButtonDispatch
    from adafruit_hid.mouse import Mouse
    from digitalio import DigitalInOut, Direction
    
    class State:
        def __init__(self):
            self.left = False
            self.right = False
            self.up = False
            self.down = False
            self.left_holding = False
            self.right_holding = False
            self.up_holding = False
            self.down_holding = False
            self.brightness = 0.1
            self.colors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    state = State()
    
    spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
    spkrenable.direction = Direction.OUTPUT
    spkrenable.value = True
    
    mouse = Mouse()
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=state.brightness, auto_write=False)
    
    f = open("click.wav", "rb")
    a = audioio.AudioOut(board.A0, f)
    
    pads = {
        "down": touchio.TouchIn(board.A7),
        "left": touchio.TouchIn(board.A4),
        "up": touchio.TouchIn(board.A1),
        "right": touchio.TouchIn(board.A3)
    }
    
    black = 0
    violet = 327695
    purple = 1638425
    blue = 25
    green = 6400
    red = 1638400
    orange = 1639680
    yellow = 1644800
    
    def clear(token, state):
        state.colors = [black, black, black, black, black, black, black, black, black, black]
    
    def up_rainbow(state):
        state.colors = [green, blue, purple, black, black, black, black, red, orange, yellow]
        
    def down_rainbow(state):
        state.colors = [black, black, purple, blue, green, yellow, orange, red, black, black]
        
    def right_green(state):
        state.colors = [black, black, black, black, black, green, green, green, green, green]
        
    def left_green(state):
        state.colors = [green, green, green, green, green, black, black, black, black, black]
    
    def check(token, state):
        return pads[token].value
    
    def click_sound():  
        a.play()
    
    def up_press(token, state):
        up_rainbow(state)
        click_sound()
        print("Up press")
        
    def down_press(token, state):
        down_rainbow(state)
        click_sound()
        print("Down press")
        
    def scroll_up(token, hold_count, state):
        print("Scrolling up")
        
    def scroll_down(token, hold_count, state):
        print("Scrolling down")
        
    def left_press(token, state):
        left_green(state)
        click_sound()
        print("Left press")
        
    def left_release(token, state):
        clear(token, state)
        print("Left release")
        
    def right_press(token, state):
        right_green(state)
        click_sound()
        print("Right press")
        
    def right_release(token, state):
        clear(token, state)
        print("Right release")
    
    buttons = [
        ButtonDispatch("down", check, state, down_press, clear, scroll_down),
        ButtonDispatch("up", check, state, up_press, clear, scroll_up),
        ButtonDispatch("left", check, state, left_press, left_release),
        ButtonDispatch("right", check, state, right_press, right_release)
    ]
    
    while True:
        for dispatch in buttons:
            dispatch()
        
        for i, color in enumerate(state.colors):
            pixels[i] = color
            
        pixels.write()

Code That Prevents Errant Pad Activation
========================================
I noticed that sometimes, when I was pressing a certain touch pad my finger would graze another pad, causing an errant press event. 

To fix this, I added the concept of a "lock" attribute in the ``State`` class. When the ``state.lock`` attribute is ``True``, press events are not acted upon.

It was a simple 2 line change in ``ButtonDispatch``:

.. code-block:: python
    :hl_lines: 59 60
    
    import time
    
    class ButtonDispatch:
        hold_threshold = 0.4
        debounce = 0.2
    
        def __init__(self, token, check, state, press=None, release=None, hold=None):
            self.token = token
            self._state = state
            self.checkin = time.monotonic()
            self.holding = False
            self.hold_count = 0
    
            self.get_value = check
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
    
        def __repr__(self):
            return  "<{} Check: {}, State: {} Checkin: {}>".format(self.token, self.check(), self.state, self.checkin)
    
        def release(self):
            if self.onrelease is not None:
                self.onrelease(self.token, self._state)
    
            self.state = False
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
            if self._state.lock:
                return
            
            if self.onpress is not None:
                self.onpress(self.token, self._state)
    
            self.state = True
            self.holding = True
            self.checkin = time.monotonic()
    
        def __call__(self):
            current = time.monotonic()
            
            # button has been held
            if self.state and self.holding:
                if current - self.checkin >= self.hold_threshold:
                    self.hold()
    
            # button has been pressed
            if not self.state and self.check():
                if current - self.checkin >= self.debounce:
                    self.press()
    
            # button has been released
            if self.state and not self.check():
                if current - self.checkin >= self.debounce:
                    self.release()
        
Then, I just had to change that state attribute when necessary:

.. code-block:: python
    
    ﻿import board
    import time
    import neopixel
    import audioio
    import touchio
    from dispatch import ButtonDispatch
    from adafruit_hid.mouse import Mouse
    from digitalio import DigitalInOut, Direction
    
    class State:
        def __init__(self):
            self.left = False
            self.right = False
            self.up = False
            self.down = False
            self.left_holding = False
            self.right_holding = False
            self.up_holding = False
            self.down_holding = False
            self.brightness = 0.4
            self.colors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.lock = False
    
    state = State()
    
    spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
    spkrenable.direction = Direction.OUTPUT
    spkrenable.value = True
    
    mouse = Mouse()
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=state.brightness, auto_write=False)
    
    f = open("click.wav", "rb")
    a = audioio.AudioOut(board.A0, f)
    
    pads = {
        "down": touchio.TouchIn(board.A7),
        "left": touchio.TouchIn(board.A4),
        "up": touchio.TouchIn(board.A1),
        "right": touchio.TouchIn(board.A3)
    }
    
    black = 0
    white = 6710886
    violet = 1507389
    purple = 6684774
    blue = 102
    blue_green = 1584641
    green = 26112
    red = 6684672
    ornange_red = 4785408
    orange = 6689792
    yellow = 6710784
    
    def clear(state):
        state.colors = [black, black, black, black, black, black, black, black, black, black]
    
    def up_rainbow(state):
        state.colors = [green, blue, purple, black, black, black, black, red, orange, yellow]
    
    def down_rainbow(state):
        state.colors = [black, black, purple, blue, green, yellow, orange, red, black, black]
    
    def right_green(state):
        state.colors = [black, black, black, black, black, green, green, green, green, green]
    
    def left_green(state):
        state.colors = [green, green, green, green, green, black, black, black, black, black]
        
    def middle_stripes(state):
        state.colors = [violet, orange, violet, orange, violet, orange, violet, orange, violet, orange]
    
    def check(token, state):
        return pads[token].value
    
    def click_sound():
        a.play()
    
    def up_press(token, state):
        up_rainbow(state)
        click_sound()
        state.lock = True
        print("Up press")
        
    def up_release(token, state):
        clear(state)
        print("Down release")
        state.lock = False
    
    def down_press(token, state):
        down_rainbow(state)
        click_sound()
        state.lock = True
        print("Down press")
        
    def down_release(token, state):
        clear(state)
        print("Down release")
        state.lock = False
    
    def scroll_up(token, hold_count, state):
        print("Scrolling up")
    
    def scroll_down(token, hold_count, state):
        print("Scrolling down")
    
    def both_press(token, state):
        state.lock = True
        middle_stripes(state)
        click_sound()
        print("Both press")
    
    def left_press(token, state):
        if state.right:
            left_release(token, state)
            both_press(token, state)
        else:
            left_green(state)
            click_sound()
            print("Left press")
    
    def left_release(token, state):
        clear(state)
        print("Left release")
        state.lock = False
    
    def right_press(token, state):
        if state.left:
            right_release(token, state)
            both_press(token, state)
        else:
            right_green(state)
            click_sound()
            print("Right press")
    
    def right_release(token, state):
        clear(state)
        print("Right release")
        state.lock = False
    
    buttons = [
        ButtonDispatch("down", check, state, down_press, down_release, scroll_down),
        ButtonDispatch("up", check, state, up_press, up_release, scroll_up),
        ButtonDispatch("left", check, state, left_press, left_release),
        ButtonDispatch("right", check, state, right_press, right_release)
    ]
    
    while True:
        for dispatch in buttons:
            dispatch()
    
        for i, color in enumerate(state.colors):
            pixels[i] = color
    
        pixels.write()
        
Adding In Mouse Actions
=======================
        

Acellerated Scrolling
---------------------

Code
====

.. code-block:: python
    
    import touchio
    import board
    import time
    import math
    import neopixel
    import adafruit_fancyled.adafruit_fancyled as fancy
    from adafruit_hid.mouse import Mouse
    
    class State:
        def __init__(self, threshold=0.5, hold_threshold=0.125):
            self.threshold = threshold
            self.hold_threshold = hold_threshold
            self.state = []
            
        def add(self, pin, callback_up=None, callback_down=None, callback_hold=None):
            pin = touchio.TouchIn(pin)
            pin.threshold += 400
            #       pin  state  checkin           button rel    button press  when held      held?  latch count
            info = [pin, False, time.monotonic(), callback_up, callback_down, callback_hold, False, 0]
            self.state.append(info)
        
        def __call__(self):
            current = time.monotonic()
            for i in range(len(self.state)):
                # if this button is beign held
                if self.state[i][0].value and self.state[i][6]:
                    if current - self.state[i][1] >= self.hold_threshold:
                        if self.state[i][5]:
                            print("time to run latch for ", i)
                            self.state[i][7] += 1
                            self.state[i][5](self.state[i][7])
                            self.state[i][1] = current
                
                # transition from not pressed to pressed
                if self.state[i][0].value and not self.state[i][1]:
                    if current - self.state[i][1] >= self.threshold:
                        if self.state[i][4]: 
                            self.state[i][4]()
                            
                        if self.state[i][5]:
                            print("Latching ", i)
                            self.state[i][6] = True
                            
                        self.state[i][1] = True
                        self.state[i][2] = current
                
                # transition from pressed to not pressed
                if not self.state[i][0].value and self.state[i][1]:
                    if current - self.state[i][1] >= self.threshold:
                        if self.state[i][3]: 
                            self.state[i][3]()
                        
                        print("Un-Latching ", i)
                        self.state[i][6] = False
                        self.state[i][7] = 0
                        
                        self.state[i][1] = False
                        self.state[i][2] = current
    
    brightness = 0.1
    violet = fancy.gamma_adjust(fancy.CRGB(148, 0, 211), brightness=brightness).pack()
    purple = fancy.gamma_adjust(fancy.CRGB(255, 0, 255), brightness=brightness).pack()
    blue = fancy.gamma_adjust(fancy.CRGB(0, 0, 255), brightness=brightness).pack()
    green = fancy.gamma_adjust(fancy.CRGB(0, 255, 0), brightness=brightness).pack()
    red = fancy.gamma_adjust(fancy.CRGB(255, 0, 0), brightness=brightness).pack()
    orange = fancy.gamma_adjust(fancy.CRGB(255,140,0), brightness=brightness).pack()
    yellow = fancy.gamma_adjust(fancy.CRGB(255, 255, 0), brightness=brightness).pack()
    
    up_rainbow = (green, blue, purple, red, orange, yellow)
    down_rainbow = (purple, blue, green, yellow, orange, red)
    
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1)
    pixels.fill((0,0,0))
    pixels.show()
    
    mouse = Mouse()
    pads = State()
    
    def scale_scroll(count):
        amount = math.floor(math.log(count, 2))
        if amount >= 8:
            return 8
        else:
            return amount
    
    def scroll_up(count=0):
        pixels[:3] = up_rainbow[:3]
        pixels[7:] = up_rainbow[3:]
        pixels.show()
        amount = scale_scroll(count)
        mouse.move(wheel=amount)
    
    def clear_pixels():
        pixels.fill((0,0,0))
        
    def scroll_down(count=0):
        pixels[2:8] = down_rainbow
        pixels.show()
        amount = scale_scroll(count)*-1
        mouse.move(wheel=amount)
        
       
    def left_hold():
        pixels[0:5] = (green, green, green, green, green)
        pixels.show()
        mouse.press(Mouse.LEFT_BUTTON)
        
    def left_release():
        pixels.fill((0, 0, 0))
        pixels.show()
        mouse.release(Mouse.LEFT_BUTTON)
        
    def right_hold():
        pixels[5:] = (red, red, red, red, red)
        pixels.show()
        mouse.press(Mouse.RIGHT_BUTTON)
        
    def right_release():
        pixels.fill((0, 0, 0))
        pixels.show()
        mouse.release(Mouse.RIGHT_BUTTON)
    
    pads.add(board.A1, clear_pixels, None, scroll_up)
    pads.add(board.A2, clear_pixels, None, scroll_down)
    pads.add(board.A3, left_release, left_hold)
    pads.add(board.A4, right_release, right_hold)
    
    while True:
        pads()
