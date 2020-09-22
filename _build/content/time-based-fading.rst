Time-Based NeoPixel Fading In Circuitpython With FancyLED
#########################################################
:date: 2020-09-21 10:54
:author: jjmojojjmojo
:category: tutorial
:tags: circuitpython; python; hardware; state;
:slug: time-based-fading
:status: published
:social_image: /images/time-based-fading/banner.jpg

.. include:: ../emojis.rst


.. image:: {static}/images/time-based-fading/banner.gif
   :width: 10em
   :align: right

Fading makes LEDs look really cool. It's a less abrupt way of transitioning from off to on, or from one color to the next. Even with Neopixels built-in drivers it can still be daunting, and a source of slowdowns in your code. In this tutorial, we'll explore the considerations for fading, walk through a few different approaches, and present a final approach that works especially well with CircuitPython.

.. PELICAN_END_SUMMARY

Materials
=========
* A `CircuitPlayground Express <https://www.adafruit.com/product/3333>`__, or `CircuitPlayground Bluefruit <https://learn.adafruit.com/adafruit-circuit-playground-bluefruit>`__.
* A micro USB cable.
* A computer with a USB port.


.. figure:: {static}/images/time-based-fading/cpx_cpb_glamour_shot.png
   :width: 100%
   :figwidth: 80%
   :align: center
   
   Left: CircuitPlayground Bluefruit. Right: CircuitPlayground Express.

.. note::
    
    The two boards pictured function in the same way (with the same pinout and peripherals), but they are powered by different chips. The key difference is that the CircuitPlayground Bluefruit can communicate over bluetooth.
    
    Beyond this, their clock frequency is different and the Bluefruit is a slightly more powerful board.
    
.. tip::
    
    .. image:: {static}/images/time-based-fading/cpx-and-bluefruit-in-cases.png
       :width: 50%
       :align: left
       
    
    A handy accessory that is also highly recommended is the `Adafruit Circuit Playground Express or Bluefruit Enclosure <https://www.adafruit.com/product/3915>`__. You'll see the above boards in their cases in the videos throughout this tutorial.
    


Screen shots of code samples and running code were taken from `Mu <https://codewith.mu/>`__. Not required to follow along but highly recommended!

.. note::
    
    We'll show some example circuits and modified code in the appendix if you don't happen to have a CPX or CPB or would prefer to build some circuits. 
    
    However, it's **highly** recommended to pick up one of the integrated boards, the "playground" aspect is worth the price of admission.
    

Libraries
=========
We'll be using the following external libraries:

* `neopixel <https://circuitpython.readthedocs.io/projects/neopixel/en/latest/>`__
* `adafruit_fancyled <https://circuitpython.readthedocs.io/projects/fancyled/en/latest/index.html>`__

The best way to get these is to download the `latest CircuitPython bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/latest>`__.

To install, unzip the bundle and just copy the :code:`adafruit_fancyled` and :code:`neopixel` folders over to your :code:`CIRCUITPY` drive, under the :code:`lib` folder.

.. tip::
    
    Confused? Check out `this guide <https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries>`__ for more detail.
    


Background Reading
==================
For a full understanding of the underlying concepts we're working with, check out the links below!

* https://learn.adafruit.com/welcome-to-circuitpython/overview
* https://learn.adafruit.com/adafruit-neopixel-uberguide
* https://learn.adafruit.com/fancyled-library-for-circuitpython/overview
* https://learn.adafruit.com/adafruit-circuit-playground-express/overview
* https://learn.adafruit.com/adafruit-circuit-playground-bluefruit

While not required, if you'd like to get more detail about the Python concepts we're using here (time-based events, classes), check out `State and Events In Circuit Python <{filename}/pages/circuitpython-state.rst>`__.


Detour: DIY Diffusers To Save Your Eyes
=======================================
Neopixels are small, but they are *extremely bright*. Staring at them in their raw glory can be headache inducing. This even happens at low brightness settings. **You will see spots**.


.. figure:: {static}/images/time-based-fading/diffusers-no-diffuser.png
   :width: 100%
   :figwidth: 80%
   :align: center
   
   A CircuitPlayground Express with no diffuser. All neopixels are set to maximum levels, resulting in a bright white light. **OUCH**
   

For the sake of your eyes, you will probably want to use some kind of *diffuser* as you walk through this tutorial, or in general when doing projects that use neopixels. 

A diffuser will scatter the light and save your eyes. As an added bonus, it will help to blend the colors more effectively, giving an overall more "pure" tint to the colors, even with gamma correction (more on that later).

Here are a few examples of materials for inspiration. You might have one of these around your house (if not they are inexpensive and easy to find). Each one provides a increasing level of diffusion.

CPX Case
--------

.. figure:: {static}/images/time-based-fading/diffusers-case.png
   :width: 100%
   :figwidth: 80%
   :align: center
   
   A CircuitPlayground Express in one of the swanky cases - it provides a very minimum diffusion because of the thickness of the transparent plastic.

Tracing Paper
-------------

.. figure:: {static}/images/time-based-fading/diffusers-tracing-paper.png
   :width: 100%
   :figwidth: 80%
   :align: center
   
   Common tracing paper, cut into a 3" (7.62cm) square. Can be doubled up if needed. Easy to get at just about any department, drug or art store.
   
Marker Paper
------------

.. figure:: {static}/images/time-based-fading/diffusers-marker-paper.png
   :width: 100%
   :figwidth: 80%
   :align: center
   
   Canson XL marker paper, cut into a 3" (7.62cm) square. Can be doubled up if needed. Plastic based, it's thicker and more diffusing. Also great for drawing with markers, cheap, easy to get at art supply stores.
   
Foam Core Box
-------------

.. figure:: {static}/images/time-based-fading/diffusers-foam-core.png
   :width: 100%
   :figwidth: 80%
   :align: center
   
   Cheap foam core, formed into a crude box. Cut as a rectangle 4.5x3" (11.43x7.62cm). The "legs" were created by scoring the top paper layer 0.5" (1.27cm) from each side. I got this from DollarTree, a "99 cent" store here in the US.
   

   
Neopixel Fading: Basics
=======================
To get ourselves oriented, lets start with the simplest possible fading loop. We'll take the neopixels from off to full red and then back again.

Colors on neopixels are specified as sequences of unsigned 8-bit values, one for each color: red, green and blue. This means we have a possible range of :code:`(0, 0, 0)` to :code:`(255, 255, 255)`.

.. tip::
    
    "8-bit" means a number that, if represented in binary, would be made up of 8 individual 1's and 0's. An *unsigned* 8-bit number will range from 0000000 to 1111111, or 0 to 255. If negative numbers were possible (if they were *signed*), the range would be -127 through 127 - one bit is used to represent the minus sign, so the actual range is 7 bits, 0000000 to 1111111 (the first bit is usually used to store 1 for negative, and 0 for positive)
    

To fade an RGB pixel from black (off) to red, we need to count from :code:`0` to :code:`255`, and assign the value to the red element. We'll do the math on the fly.

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    BRIGHTNESS = 1.0
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=BRIGHTNESS, auto_write=False)
    
    color = [0, 0, 0]
    increment = 1
    while True:
        color[0] += increment
        
        if color[0] >=255:
            color[0] = 255
            increment = -1
            
        if color[0] <= 0:
            color[0] = 0
            increment = 1
        
        rgb.fill(color)
        rgb.write()
        

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0002-slow-red-fading.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0002-slow-red-fading.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

You'll notice how smooth this is, but also how slow it is. This is the CircuitPlayground running at *full speed*. It doesn't mean the CircuitPlayground is slow, it's just that writing to neopixels takes a tiny fraction of a second in each loop. This is because writing to the neopixels is a *blocking* operation. Everything stops as we wait for the neopixels to update.

You may also notice that, as the color changes, it can be hard to tell the difference between  transitional shades of red. This is due to the `relative sensitivity of your eyes to red wavelengths of light <https://en.wikipedia.org/wiki/Color_vision#Wavelength_and_hue_detection_in_humans>`__, but also because the LED elements really can't produce as many specific shades of red as you're requesting.

We can overcome the issue of blocking and the length of the cycle initially by simply *shortening the cycle*! We can't really see all 255 shades of red, so lets reduce that number. How about we try 21(ish) shades instead?

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    BRIGHTNESS = 1.0
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=BRIGHTNESS, auto_write=False)
    
    color = [0, 0, 0]
    increment = 12
    while True:
        color[0] += increment
        
        if color[0] >=255:
            color[0] = 255
            increment = -12
            
        if color[0] <= 0:
            color[0] = 0
            increment = 12
    
        rgb.fill(color)
        rgb.write()
        

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0003-faster-red-fading.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0003-faster-red-fading.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

Much more ominous, but seems just as smooth.

|cool| At this point we've got the basics of fading down. We know that we don't need a full cycle of colors to get a nice smooth result, our eyes aren't perfect, and that writing to neopixels is a *blocking* operation.

There's another issue we should touch on. Lets switch to a mix of colors (we'll mix red and green to make yellow), and slow down the fading so we can better see each color, and see what happens:

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    BRIGHTNESS = 1.0
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=BRIGHTNESS, auto_write=False)
    
    color = [0, 0, 0]
    
    increment = 12
    
    while True:
        if color[0] <= 0:
            color[0] = 0
            color[1] = 0
            increment = 12
            
        if color[0] >= 255:
            color[0] = 255
            color[1] = 255
            increment = -12
        
        rgb.fill(color)
        rgb.write()
        
        color[0] += increment
        color[1] += increment
    
        time.sleep(0.3)
        
    

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0004-yellow-fading-1-greenish.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0004-yellow-fading-1-greenish.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

It may be hard to tell from the video, but if you're following along on your own board, you'll likely note that the 'yellow' color is actually quite green in hue. This is due to the way that the specific wavelengths of red and green light mix. We can get around this using a technique called `gamma correction <https://en.wikipedia.org/wiki/Gamma_correction>`__. 

In simple terms, gamma correction is the application of a mathematical formula to a color value to adjust for the inherent limitations of the light source emitting the color (relative to the human eye). The details of it are fascinating, but out of scope for this tutorial. Fortunately, Adafruit has built a really killer CircuitPython library that has all sorts of useful tools for working with RGB LEDs, including gamma correction. It's called FancyLED, and it's amazing (it's a port of `FastLED <http://fastled.io/>`__).

.. tip:: A Quick Note About Brightness
    
    Up until now, we've been using the :code:`brightness` parameter to the NeoPixel constructor to control how bright we want the NeoPixels to be. We've been using the maximum value, :code:`1.0`. We've been using a *constant*, named :code:`BRIGHTNESS` to set that value.
    
    The maximum value is super bright, like eye-pain-inducing bright (did you `make a diffuser <#detour-diy-diffusers-to-save-your-eyes>`__?). It also draws a lot more power on average then using a lower brightness level. So we'll typically want to use a lower value in most projects.
    
    However, when mixing colors with FancyLED, it's best to set the NeoPixel brightness to maximum, and let the FancyLED API know what brightness we want when calculating colors. This leads to the best looking colors overall.
    
    From here on, we'll be setting :code:`BRIGHTNESS` to :code:`0.4` and passing :code:`1.0` to :code:`neopixel.NeoPixel()`. We've picked :code:`0.4` because it is fairly bright, but not overly so. When brightness is low, the fidelity of the colors produced is a little lower as well.
    
    Feel free to use a different :code:`BRIGHTNESS` level that's best for your comfort!
    

Lets use Fancy to gamma correct the yellow colors:

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    import adafruit_fancyled.adafruit_fancyled as fancy
    
    BRIGHTNESS = 0.4
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    color = [0, 0, 0]
    
    increment = 12
    
    while True:
        if color[0] <= 0:
            color[0] = 0
            color[1] = 0
            increment = 12
            
        if color[0] >= 255:
            color[0] = 255
            color[1] = 255
            increment = -12
        
        adjusted = fancy.gamma_adjust(fancy.CRGB(*color), brightness=BRIGHTNESS)
        rgb.fill(adjusted.pack())
        rgb.write()
        
        color[0] += increment
        color[1] += increment
    
        time.sleep(0.3)
    

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0005-gamma-corrected-yellow-fading.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0005-gamma-corrected-yellow-fading.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   
In the video, it may still look a little greenish, but in real life, the yellow is much more accurate.
   
Fancy provides a few key components for our color-correction purposes. First, the :code:`CRGB` class encapsulates an RGB color sequence into an object with useful methods for color math. Those extra methods are used by the :code:`gamma_adjust` function to do its magic. :code:`gamma_adjust` returns another :code:`CRGB` object. 

When applying the color to our neopixels, we're using the :code:`pack()` method. This method returns a single-value representation of the color sequence.

.. note::
    
    You can access the red, blue, and green elements individually to construct an RGB sequence, however, those values are stored internally as floats from 0 to 1, so they need to be converted:
    
    .. code-block:: python
        
        new_color = (int(adjusted.red*100), int(adjusted.green*100), int(adjusted.blue*100))
        rgb.fill(new_color)
        
    We're using :code:`pack` here for a few key reasons:
    
    * it's a bit cleaner, and more precise - using the component colors looks messy, and there's potential for errors doing the conversion
    * it's more efficient - we're saving lines of code and memory here.
    * we're going to rely heavily on :code:`pack`'s output later in this tutorial.
    


With gamma correction, the color is much closer to "true" yellow. This becomes even more obvious at lower brightness levels. Try the last two examples with :code:`BRIGHTNESS=0.1` and you'll see what I mean.

Gradients With FancyLED
=======================
Now that we have basic color mixing tools at our disposal, lets get a little more fancy (no pun intended). FancyLED provides a gradient mixing feature that we can use to do *all* the math for us, from adjusting the relative brightness to figuring out intermediate colors. Here's what the code from the last section looks like taking full advantage of FancyLED's fanciness:

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    import adafruit_fancyled.adafruit_fancyled as fancy
    
    BRIGHTNESS = 0.4
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    BLACK = fancy.CRGB(0, 0, 0)
    YELLOW = fancy.CRGB(255, 255, 0)
    
    gradient = fancy.expand_gradient([
        (0.0, BLACK), 
        (0.5, YELLOW),
        (1.0, BLACK)
    ], 20)
    
    index = 0
    
    while True:
        color = gradient[index]
        adjusted = fancy.gamma_adjust(color, brightness=BRIGHTNESS)
        rgb.fill(adjusted.pack())
        rgb.write()
        
        index += 1
        if index > len(gradient)-1:
            index = 0
            
        time.sleep(0.3)
        
        
.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0006-fancy-generated-yellow-fade.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0006-fancy-generated-yellow-fade.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

:code:`expand_gradient()` allows us to do *any* sort of gradient, not just simple "fade in, fade out" ones! Lets show some support for the LGBTQA+ community and make a sweet rainbow fader in honor of the `LGBT pride flag <https://en.wikipedia.org/wiki/Rainbow_flag_(LGBT)>`__:

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    import adafruit_fancyled.adafruit_fancyled as fancy
    
    BRIGHTNESS = 0.4
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    WHITE = fancy.CRGB(255, 255, 255)
    BLACK = fancy.CRGB(0, 0, 0)
    RED = fancy.CRGB(255, 0, 0)
    GREEN = fancy.CRGB(0, 255, 0)
    YELLOW = fancy.CRGB(255, 255, 0)
    BLUE = fancy.CRGB(0, 0, 255)
    ORANGE = fancy.CRGB(255, 127, 0)
    VIOLET = fancy.CRGB(139, 0, 255)
    
    gradient = fancy.expand_gradient([
        (0.0, RED),
        (0.16, ORANGE),
        (0.33, YELLOW),
        (0.5, GREEN),
        (0.66, BLUE),
        (0.82, VIOLET),
        (1.0, RED)
    ], 24)
    
    index = 0
    
    while True:
        color = gradient[index]
        adjusted = fancy.gamma_adjust(color, brightness=BRIGHTNESS)
        rgb.fill(adjusted.pack())
        rgb.write()
        
        index += 1
        if index > len(gradient)-1:
            index = 0
        
        time.sleep(0.3)

The primary change here is using :code:`expand_gradient()` instead of doing our own math to fade from one shade to the next. It takes a sequence where each member is a position as a float (the beginning of the gradient is :code:`0.0` and the end is :code:`1.0`) and a :code:`CRGB` color object. It returns a sequence of new :code:`CRGB` objects that we can pass to :code:`gamma_ajust()`, in place of the tuples we used before.
        
.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0007-pride-rainbow-fade.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0007-pride-rainbow-fade.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

Pre-calculated Gradients
========================

There's an added benefit to using :code:`expand_gradient()` as we are here: we can do all of this work *offline* instead of on the fly (or, *at runtime*). Colors are ultimately represented as integers and a palette is just a sequence. This means its possible to represent our ready-to-display fading color series as a simple tuple of integers. This is a boon for a couple of reasons, primarily memory-related ones:

* Tuples of integers are very compact since they are `immutable <https://en.wikipedia.org/wiki/Immutable_object>`__ (once they are created, they cannot be changed, so they can be stored in a special way that is more memory efficient).
* We don't have to ship the FancyLED library with our main application code, saving on flash memory.
* We don't have to load FancyLED either, leaving more memory available for our  main code.

We can refactor the code above into a function that will return a tuple of packed integers representing our gradient. While we're at it, we can figure out each position value with a little math (here we're assuming we want each color to be displayed for the same amount of time, check out `the FancyLED docs <https://learn.adafruit.com/fancyled-library-for-circuitpython/palettes>`__ for more).

We can then print the palette out to the console in a way that can be copy-and-pasted into our project, or another module. Finally, we'll display the gradient on the neopixels as before so we can see it in action:

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    import adafruit_fancyled.adafruit_fancyled as fancy
    
    BRIGHTNESS = 0.4
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    def make_gradient(colors, count=24, cycle=True):
        values = []
        ratio = 1.0/len(colors)
        for index, color in enumerate(colors):
            value = float(index*ratio)
            values.append((value, color))
    
        if cycle:
            values.append((1.0, colors[0]))
    
        palette = []
        for expanded in fancy.expand_gradient(values, count):
            palette.append(fancy.gamma_adjust(expanded, brightness=BRIGHTNESS).pack())
    
        return tuple(palette)
        
    WHITE = fancy.CRGB(255, 255, 255)
    BLACK = fancy.CRGB(0, 0, 0)
    RED = fancy.CRGB(255, 0, 0)
    GREEN = fancy.CRGB(0, 255, 0)
    YELLOW = fancy.CRGB(255, 255, 0)
    MAGENTA = fancy.CRGB(255, 0, 255)
    CYAN = fancy.CRGB(0, 255, 255)
    BLUE = fancy.CRGB(0, 0, 255)
    ORANGE = fancy.CRGB(255, 127, 0)
    VIOLET = fancy.CRGB(139, 0, 255)
    INDIGO = fancy.CRGB(46, 43, 95)
    PINK = fancy.CRGB(255, 127, 127)
    MINT = fancy.CRGB(127, 255, 127)
    ROBIN = fancy.CRGB(127, 127, 255)
    CANARY = fancy.CRGB(255, 255, 127)
    
    gradient = make_gradient([
        RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET 
    ])
    
    print("gradient = ", gradient)
    
    index = 0
    
    while True:
        rgb.fill(gradient[index])
        rgb.write()
        
        index += 1
        if index > len(gradient)-1:
            index = 0
        
        time.sleep(0.2)
        

Lets briefly discuss the :code:`make_gradient()` function.

:code:`make_gradient()` takes three parameters:

* :code:`colors`, a sequence of :code:`CRGB` objects.
* :code:`count`, an integer that sets how many colors to generate.
* :code:`cycle`, a boolean. Controls if the gradient should abruptly end or fade back into itself.

The :code:`count` parameter sets the granularity of the gradient - a higher :code:`count` means a smoother transition. 

You'll want to adjust the :code:`count` to suit your memory requirements and the speed of your animation. You can get a pretty good result with as few as 5 or 10 generated colors if they are displayed quickly enough.

:code:`cycle`'s value depends on the effect you are trying to achieve. Most of the code we've looked at so far fades a color in, then fades it out again. Our pride color fader above keeps cycling smoothly. But there are times when we want a color to simply fade out, or a sequence to dazzle the user and then return to a solid color. In that case, we can set :code:`cycle` to :code:`False`. 

.. note::
    
    We'll see an application of a fade-out gradient later in this tutorial!
    

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0008-print-out-precalc-gradient.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0008-print-out-precalc-gradient.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

Now that we've generated our colors, we can remove Fancy from our board and get rid of the imports and calls to calculate the adjusted gradient colors at runtime, greatly reducing the complexity of our code:

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    gradient =  (6684672, 6684672, 6685184, 6686720, 6689024, 6692864, 6697984, 6705152, 5268992, 2123264, 550400, 26112, 17920, 6664, 1312, 80, 102, 131174, 458854, 1114214, 2031668, 3211281, 4718594, 6684672)
    
    index = 0
    
    while True:
        rgb.fill(gradient[index])
        rgb.write()
    
        index += 1
        if index > len(gradient)-1:
            index = 0
    
        time.sleep(0.2)
        
    


When *Not* To Precalculate
--------------------------
As noted above, we can save a lot of memory and overhead by pre-calculating our gradients. But sometimes it's not the best approach. In particular:

* **When memory is at a premium.** In memory-starved environments, doing calculations inline can be more efficient than storing a pre-calculated pallete. In these situations you would want to look at the FancyLED source and port over the gamma correction algorithm.
* **When you need a lot of gradients.** Even on "beefy" platforms like our CPX/CPB boards, having a lot of pre-calculated gradients will take up precious memory.
* **When you need a really slow, really smooth animation** The gradients get bigger and bigger as you generate more and more intermediate colors. You can easily run out of memory working with longer, smoother gradients.
* **When the duration or color scheme of the gradient animation is variable.** If the rate of the fade,  or the colors used, will change in a dynamic or highly variable way, doing the calculations at runtime will yield a better result. You can compromise, if you have the memory, and generate the same gradient for multiple durations and color combinations (we'll be using this technique later on).

.. tip::
    
    If you *are* doing on-the-fly calculations, Fancy provides a :code:`mix()` function, that will return the color in-between two :code:`CRGB` colors. 
    
    Here's a quick example, re-implementing the ominous red gradient from the beginning of the tutorial, but using :code:`mix()` instead of doing the math ourselves, or using :code:`expand_gradient()`.
    
    .. code-block:: python
        
        ﻿import board
        import neopixel
        import time
        
        import adafruit_fancyled.adafruit_fancyled as fancy
        
        BRIGHTNESS = 0.4
        
        rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
        
        RED = fancy.CRGB(255, 0, 0)
        BLACK = fancy.CRGB(0, 0, 0)
        
        point = 0.0
        increment = 0.05
        
        while True:
            color = fancy.gamma_adjust(fancy.mix(RED, BLACK, point), brightness=BRIGHTNESS)
            
            point += increment
            
            if point >= 1.0 or point <= 0.0:
                increment *= -1
                
            rgb.fill(color.pack())
            rgb.write()
        

Fading Class #1: Looping
========================
Up until now, we've been fading our neopixels in our main :code:`while True` loop. It does the job, but there are some rough edges. Lets prepare to smooth them out by encapsulating our fading logic into a *class*. This way, we can do some very interesting things in the near future (hold tight, it's going to be great!).

For our first pass, we'll simply re-factor the code we were using in the main loop:

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    class LoopFader:
        def __init__(self, palette):
            self.palette = palette
            self.index = 0
            
        @property
        def color(self):
            color = self.palette[self.index]
            self.index += 1
            if self.index > len(self.palette)-1:
                self.index = 0
            return color
    
    pride = (4980736, 4980736, 4981248, 4982272, 4984064, 4986880, 4990720, 4996096, 3951616, 1592320, 412672, 19456, 13312, 5126, 1048, 60, 76, 65612, 327756, 852044, 1507367, 2359309, 3538946, 4980736)
	
    
    fader = LoopFader(pride)
    
    while True:
        rgb.fill(fader.color)
        rgb.write()
        time.sleep(0.1)
        
We've used a couple of notable Python features in our :code:`LoopFader` class:

* We've established a *constructor* method. These are always named :code:`__init__` in Python. We use this method to set up the basic state of our class: set the palette, and set the initial color index. Constructors can take parameters like any other method. We use that to get a hold of the gradient, via the :code:`palette` parameter, and save a reference to it.
* We're using a *decorator*, called :code:`@property`. Decorators allow you to annotate an object with code that enhances its functionality. :code:`@property` is a special built-in decorator that transforms a method (in our case :code:`color()`) into an object attribute. Normally, you'd have a static value for the current color, and when you access it, it would always be the same. Using this decorator, we've created a dynamic attribute! Every time you access :code:`fader.color`, the :code:`color()` method is called, and it returns the next color in the gradient.

.. tip::
    
    If you'd like to dig into everything Python classes have to offer, check out `Introduction To Python: Classes <http://introtopython.org/classes.html>`__! |mortarboard|
    


After the major changes (refactoring the code into a class, using the decorator), the next thing you might notice about this code is that we aren't updating the neopixels after we select the next color in our gradient. This is a concept called *separation of concerns*. What it boils down to is keeping the functionality of any piece of code (class, function, method) as limited as possible, and establishing boundaries between different parts of your application.

Here, we're separating a hardware API from our fading logic. The utility of this will become more apparent in the next example.

So at this point you may be wondering what the point of moving the code around was. We're doing exactly the same thing, but now the code is spread out over the file. What's the benefit? |thinking|

Consider that we may want to use different gradients, or fade in different sequences *per pixel*. 

Because we've encapsulated the fading logic in a class, we can stamp out different instances of that class, each with different attributes. Each different instance can be used for a different purpose, or *use case*.

This leads to much cleaner code, some memory efficiency, and *ease of reuse*. We can take this :code:`LoopFader` class and put it into a module and use it in future projects without copy/paste. We can e-mail it to a friend, or put in version control. The foundation class never has to change.

.. note::
    
    There are a ton of other advantages to using classes. We can even override parts of a class and give the same methods or attributes new meaning. For a quick example of this, called *polymorphism* (aka class inheritance), see `Enhancement: A Fader With A Mode`_.
    

Here's a wacky example showing how we can control individual neopixels in different ways using the same code, since we've encapsulated it into a class:

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    class LoopFader:
        def __init__(self, palette):
            self.palette = palette
            self.index = 0
    
        @property
        def color(self):
            color = self.palette[self.index]
            self.index += 1
            if self.index > len(self.palette)-1:
                self.index = 0
            return color
    
    green_to_off = (19456, 15360, 11520, 8448, 6144, 4096, 2560, 1536, 768, 256, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    pastels = (4983563, 4986133, 4989988, 4995128, 4738120, 3230769, 2051103, 1199122, 936974, 1723418, 2772010, 4148287, 4144972, 2763340, 1710668, 921164, 1184332, 2039628, 3223884, 4737100, 4995128, 4989988, 4986133, 4983563)
    
    halloween = (4983552, 4458752, 3999232, 3540226, 3146500, 2753032, 2359565, 2097172, 1769500, 1507367, 1245236, 1048644, 1048644, 1245236, 1507367, 1769500, 2097172, 2359565, 2753032, 3146500, 3540226, 3999232, 4458752, 4983552)
	
    
    faders = [
        LoopFader(green_to_off),
        LoopFader(pastels),
        LoopFader(green_to_off),
        LoopFader(pastels),
        LoopFader(halloween),
        LoopFader(pastels),
        LoopFader(green_to_off),
        LoopFader(pastels),
        LoopFader(green_to_off),
        LoopFader(halloween)
    ]
    
    while True:
        rgb[::] = [f.color for f in faders]
        rgb.write()
        time.sleep(0.1)

This should be pretty straight forward, but you may have not seen the *slice notation* and *list comprehension* that we use when assigning the colors to the neopixels. Expand the explanation block below for more info. |mortarboard|

.. explanation::
    
    Values in Python :code:`list` objects are typically accessed one at a time, using a specific index:
    
    .. code-block:: pycon
        
        >>> mylist = [1, 2, 3, 4, 5]
        >>> mylist[1]
        2
        >>> mylist[1] = 45
        >>> mylist
        [1, 45, 3, 4, 5]
        
    However, Python also provides *slice notation* as a way to access *multuple* values:
    
    .. code-block:: pycon
        
        >>> mylist = [1, 2, 3, 4, 5]
        >>> mylist[2:]
        [4, 5]
        >>> mylist[2:] = [7, 88]
        >>> mylist
        [1, 2, 3, 7, 88]
        
    The notation allows for up to three values, each separated by a colon. The first value is the start index, the second is the end index, and the third is the step. Step allows you to skip values. Specifying a double colon :code:`::` references the entire list:
    
    .. code-block:: pycon
        
        >>> mylist = [1, 2, 3, 4, 5]
        >>> mylist[::2]
        [2, 4]
        >>> mylist[::2] = ['x', 'x']
        >>> mylist
        [1, 'x', 3, 'x', 5]
        >>> mylist[::]
        [1, 'x', 3, 'x', 5]
        >>> mylist[::] = ['y', 'y', 'y', 'y', 'y']
        >>> mylist
        ['y', 'y', 'y', 'y', 'y']
        
    
    
    .. image:: {static}/images/time-based-fading/green-white-slice-example.png
       :width: 50%
       :align: right
    
    The Neopixel class implements special methods so it can work like a list, and so we use that to assign colors. For example, to assign every even numbered neopixel to white, and all odd neopixels to green, you can do the following:
    
    .. code-block:: python
        
        ﻿rgb[::2] = ((255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255))
        rgb[1::2] = ((0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0))
        
        rgb.write()
    
    A *list comprehension* is a shortcut. It's like a :code:`for` loop that builds a list, but condensed into a single statement. The code in our example:
    
    .. code-block:: python
       
       rgb[::] = [f.color for f in faders]
       
    
    ... is equivalent to:
    
    .. code-block:: python
        
        while True:
            for index, fader in enumerate(faders):
                rgb[index] = fader.color
            
    
    
In the video below, you can see how each gradient operates independently:



.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0009-wacky-example.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0009-wacky-example.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

Wow, so now we have control of fading on a per-pixel basis! This would be an order of magnitude more complex if we had written this without using a class. Next, lets refine how we do our fading animation to make it more efficient.

Fading Class #2: Looping Without Blocking
=========================================
There are two blocking operations in the previous code. The first is writing to the neopixels. We can't do much, if anything about this. The other blocking operation is the call to :code:`time.sleep()`, that we've added to slow things down. This, we can do something about.

The trick here is to use a non-blocking operation to track the passage of time, and then only move the color index forward if the correct amount of time (this case, :code:`0.1` seconds) has passed.

On other embedded platforms, we have access to what are known as *timer interrupts* - sort of like digital stop watches that will run code at a given interval. CircuitPython doesn't currently implement these for us, so we have to use a different tact, and check the time every loop, or *poll* the clock.

.. note::
    
    Polling the clock like this is a great technique to learn! It's useful for any sort of time-based action, including filtering digital input readings. For a deep-deep dive into that subject, see `State And Events In CircuitPython <{filename}/pages/circuitpython-state.rst>`__.
    

Microcontrollers don't normally have a `"real time clock" <https://en.wikipedia.org/wiki/Real-time_clock>`__, like most computers do, so other ways of tracking the passage of time are used. The details aren't super important, just know that a real-time clock will keep consistent time from "tick" to "tick", but the other mechanisms that might be used are tied to the *clock cycle* of the microcontroller, and can "drift". A second on a stopwatch might not match up exactly with a second of time on your CircuitPlayground (but it'll be pretty darn close!).

Anyway, CircuitPython gives us a special function that gives us a time reference we can count on to always be constantly increasing, called :code:`time.monotonic()`. To illustrate its use, lets count the number of times the main :code:`while True` loop runs:

.. code-block:: python
    
    import board
    import time
    
    checkin = time.monotonic()
    counter = 0
    seconds = 0
    
    while True:
        counter += 1
        if time.monotonic() - checkin > 1.0:
            seconds += 1
            print("(approx)", seconds, "seconds have elapsed.", counter, "loops")
            checkin = time.monotonic()
            counter = 0
    


.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0010-timer-example.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0010-timer-example.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

On my board, the while loop is running about 8000 times every second. Not bad. 

You will notice that the exact count is different every time - this is what I was referring to above. Its consistent, but imprecise, so it's not a great way to keep time. Luckily, for fading neopixels we just need to track short periods of time passing, so that drift will be of little consequence.

.. note::
    
    You may be thinking, "Wait, isn't the processor in the CPX (ATSAMD21) clocked at like, 48 *megahertz*? Shouldn't the loop run 48 *million times per second*?!"
    
    Remember that CircuitPython adds a lot of overhead on top of the raw power of the processor. Python is an interpreted language - your code isn't translated directly to instructions the processor can execute so there are a couple of levels of abstraction at play to make the processor do what we want. Those layers eat up some clock cycles every loop.
    

We can check for just about any amount of time elapsing, down to around a hundredth (:code:`0.01`) of a second. The precision of :code:`time.monotonic()` will vary a bit depending on the processor, so you may be able to get finer precision, or you may not be able to get better than a *tenth* (:code:`0.1`) of a second. 

Now we can track the passage of time, and detect that a given period has elapsed. Once we've determined that a period of time has elapsed, we can take action. In the case of our :code:`LoopFader` class, we can advance the counter that tracks which color in the gradient we are currently displaying.

Here's the fading code from the last section refactored to use :code:`time.monotonic()` instead of :code:`time.sleep()`:

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    class LoopFader:
        def __init__(self, palette):
            self.palette = palette
            self.index = 0
            self.checkin = time.monotonic()
    
        @property
        def color(self):
            color = self.palette[self.index]
            
            if time.monotonic() - self.checkin > 0.1:
                self.index += 1
                if self.index > len(self.palette)-1:
                    self.index = 0
                self.checkin = time.monotonic()
                
            return color
    
    pride = (4980736, 4980736, 4981248, 4982272, 4984064, 4986880, 4990720, 4996096, 3951616, 1592320, 412672, 19456, 13312, 5126, 1048, 60, 76, 65612, 327756, 852044, 1507367, 2359309, 3538946, 4980736)
    
    fader = LoopFader(pride)
    
    while True:
        rgb.fill(fader.color)
        rgb.write()
    
We have significantly increased the overall speed of our code. Before, we were locked into one loop every :code:`0.1` seconds. While :code:`time.sleep()` is running, nothing else can happen. With this minor change, we're no longer stopping all activity. This means that we won't get in the way of other actions, like updating the neopixels, reading inputs, or writing to other outputs. This makes our project more responsive. |cool|


One More Thing! (A Minor Reduction In Blocking)
===============================================
Remember earlier when I said that writing to the neopixels was blocking, and there wasn't much we could do about it? Well, there is one minor thing we can do that can ensure we're blocking as little as possible.

In all of our code so far, we've been writing to the neopixels with every iteration of our main `while` loop. However, we're only changing the color every `0.1` seconds. We saw earlier that, on my board, the loop runs ~8000 times every second. That's 8000 writes to the neopixels every second as well. Every write takes a tiny fraction of a second. Just like with our fading code, this blocking means that other things can't happen. 

In our current application, it's not really noticeable, but as we add features it can become a big problem.

This is an easy thing to fix. First, we'll refactor the :code:`LoopFader()` so the :code:`color` attribute is no longer being updated every time it's accessed. Then, we'll move the updating logic into another method, :code:`update()`. Finally, we'll call :code:`update()` every cycle, and (here's the secret sauce) **only write to the neopixels when the color has changed**.

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    class LoopFader:
        def __init__(self, palette):
            self.palette = palette
            self.index = 0
            self.checkin = time.monotonic()
            self.color = None
    
        def update(self):
            if time.monotonic() - self.checkin > 0.1:
                self.index += 1
                if self.index > len(self.palette)-1:
                    self.index = 0
                self.checkin = time.monotonic()
                self.color = self.palette[self.index]
    
    pride = (4980736, 4980736, 4981248, 4982272, 4984064, 4986880, 4990720, 4996096, 3951616, 1592320, 412672, 19456, 13312, 5126, 1048, 60, 76, 65612, 327756, 852044, 1507367, 2359309, 3538946, 4980736)
    
    fader = LoopFader(pride)
    
    previous = None
    while True:
        fader.update()
        if fader.color != previous:
            rgb.fill(fader.color)
            rgb.write()
            previous = fader.color

Fading End Game: Time-based Fading With Dropped Frames
======================================================
We've got a pretty great algorithm for fading our neopixels from one color to the next. We're pre-calculating the gradient values, and changing colors over time without blocking. We have a pretty slick, smooth animation!

However, our :code:`LoopFader` class has to have its :code:`update()` method called to move to the next color in the gradient. If anything prevents that, like blocking code, the gradient will take longer to complete. In other words, it will appear to slow down, and can even look choppy.

Lets add some artifical blocking with :code:`time.sleep()` to see what this looks like:

.. code-block:: python
    :hl_lines: 29
    
    import board
    import neopixel
    import time
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    class LoopFader:
        def __init__(self, palette):
            self.palette = palette
            self.index = 0
            self.checkin = time.monotonic()
            self.color = None
    
        def update(self):
            if time.monotonic() - self.checkin > 0.1:
                self.index += 1
                if self.index > len(self.palette)-1:
                    self.index = 0
                self.checkin = time.monotonic()
                self.color = self.palette[self.index]
    
    pride = (4980736, 4980736, 4981248, 4982272, 4984064, 4986880, 4990720, 4996096, 3951616, 1592320, 412672, 19456, 13312, 5126, 1048, 60, 76, 65612, 327756, 852044, 1507367, 2359309, 3538946, 4980736)
    
    fader = LoopFader(pride)
    
    previous = None
    while True:
        fader.update()
        time.sleep(1.0)
        if fader.color != previous:
            rgb.fill(fader.color)
            rgb.write()
            previous = fader.color
            
    
.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0011-slowed-down-gradient.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0011-slowed-down-gradient.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

The choppiness here is very regular, because our blocking is very regular. In practice, it will look more like a random stutter.

How can we prevent this? Well, we can *drop frames*. Essentially, we can skip colors if our :code:`update()` method isn't run fast enough for our needs. 

Since we have a finite number of colors we want to cycle through, and a specific time in which to complete the cycle, we can use some math to decide which color should be displayed at a given moment based on the time that has elapsed since the cycle was started.

Here's our endgame: a non-blocking gradient loop that will always run in the desired time interval, even if other code gets in the way!

.. code-block:: python
    
    import board
    import neopixel
    import time
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    class Fader:
        def __init__(self, palette, interval=0.1):
            self.checkin = time.monotonic()
            self.color = 0
            self.interval = interval
            self.palette = palette
            self.max = len(self.palette)*interval
            self.epoch = 0
    
        def update(self):
            self.epoch = time.monotonic() - self.checkin
    
            index = round((self.epoch%self.max)/self.interval)
    
            if index > len(self.palette)-1:
                index = 0
                self.checkin = time.monotonic()
    
            self.color = self.palette[index]
            self.last = index
    
    pride = (4980736, 4980736, 4981248, 4982272, 4984064, 4986880, 4990720, 4996096, 3951616, 1592320, 412672, 19456, 13312, 5126, 1048, 60, 76, 65612, 327756, 852044, 1507367, 2359309, 3538946, 4980736)
    
    fader = Fader(pride)
    
    previous = None
    while True:
        fader.update()
        if fader.color != previous:
            rgb.fill(fader.color)
            rgb.write()
            previous = fader.color
            

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0012a-fading-endgame-demo.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0012a-fading-endgame-demo.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

If we add a blocking call to :code:`time.sleep()` after :code:`fader.update()`, you can see that now the number of colors you see drops, but overall the gradient progresses and is pretty smooth. Here, we'll use the :code:`random` module to add a little variety to the slowdown, and print out what the slowdown is so we can make a mental connection:

.. note::
    
    Writing to the console (using :code:`print`) is also a blocking operation; there's buffering in play so it's not as obvious, but it's there.
    

.. code-block:: python
    :hl_lines: 4 33 43 44 45
    
    ﻿import board
    import neopixel
    import time
    import random
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    class Fader:
        def __init__(self, palette, interval=0.1):
            self.checkin = time.monotonic()
            self.color = 0
            self.interval = interval
            self.palette = palette
            self.max = len(self.palette)*interval
            self.epoch = 0
    
        def update(self):
            self.epoch = time.monotonic() - self.checkin
    
            index = round((self.epoch%self.max)/self.interval)
    
            if index > len(self.palette)-1:
                index = 0
                self.checkin = time.monotonic()
    
            self.color = self.palette[index]
            self.last = index
    
    pride = (4980736, 4980736, 4981248, 4982272, 4984064, 4986880, 4990720, 4996096, 3951616, 1592320, 412672, 19456, 13312, 5126, 1048, 60, 76, 65612, 327756, 852044, 1507367, 2359309, 3538946, 4980736)
    
    fader = Fader(pride)
    
    sleep = (0, 0.2, 0.3, 0.6, 0.8, 0.1)
    
    previous = None
    while True:
        fader.update()
        if fader.color != previous:
            rgb.fill(fader.color)
            rgb.write()
            previous = fader.color
        
        to_sleep = random.choice(sleep)
        time.sleep(to_sleep)
        print("sleeping for", to_sleep)

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0012b-random-blocking-dropped-frames.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0012b-random-blocking-dropped-frames.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

The take away from this is that by dropping frames, we can get a pretty good approximation of the intended gradient, even if code has to block.


Enhancement: A Fader With A Mode
================================
Now that we're finished, let's build up some new functionality to illustrate how useful this approach is.

Consider the following use cases:

#. Neopixels are *bright*, and use a lot of power, it might be useful for the user to be able to turn off the pixels. It might not just be through user interaction; it could be that we turn the pixels on or off depending on the ambient light, or input from a relay, etc.
#. Sometimes you just want to turn on a neopixel, and then turn it off. But when you turn it off, it can be nice to do a gentle fade.

Both use cases share a common functionality: the concept of "mode". In either case, the fader can be "on" or "off".

Case #2 is a great case for using a gradient that doesn't "wrap".

Let's cover both use cases! We'll set up the two built-in buttons on our CircuitPlayground. The B button will turn a cycling gradient on and off. The A button will run a slow fade from a solid color to black and then automatically turn off.

We'll borrow an input handling class, :code:`Button` from `State And Events In CircuitPython <{filename}/pages/circuitpython-state.rst>`__. You can ignore the details of that class for now.

.. note::
    
    For a deep dive into how :code:`Button` was built, check out `State And Events In CircuitPython <{filename}/pages/circuitpython-state.rst>`__
    
    Generally speaking, we do something similar with :code:`Button` that we do with :code:`Fader`: we decide if the button has been pressed by tracking the passage of time, and triggering a function when we've detected a button action (press or release). This prevents noisy signals that would cause problems with reading the state of the buttons.
    

.. code-block:: python
    
    import board
    import neopixel
    import time
    from digitalio import DigitalInOut, Direction, Pull
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    class Button:
        _debounce = 0.1
    
        def __init__(self, pin, name, onrelease):
            self.name = name
            self.checkin = time.monotonic()
            self.state = False
            self.onrelease = onrelease
            self.input = DigitalInOut(pin)
            self.input.direction = Direction.INPUT
            self.input.pull = Pull.DOWN
    
        def press(self):
            print(self.name, "pressed")
    
        def release(self):
            print(self.name, "released")
            self.onrelease()
    
        def check(self):
            return self.input.value
    
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                if self.state and not self.check():
                    self.release()
    
                if not self.state and self.check():
                    self.press()
    
                self.state = self.check()
    
                self.checkin = time.monotonic()
    
    class Fader:
        def __init__(self, palette, interval=0.1):
            self.checkin = time.monotonic()
            self.color = 0
            self.interval = interval
            self.palette = palette
            self.max = len(self.palette)*interval
            self.epoch = 0
            self.index = 0
    
        def update(self):
            self.epoch = time.monotonic() - self.checkin
    
            self.index = round((self.epoch%self.max)/self.interval)
    
            if self.index > len(self.palette)-1:
                self.index = 0
                self.checkin = time.monotonic()
    
            self.color = self.palette[self.index]
    
    class ModeFader(Fader):
        def __init__(self, palette, interval=0.1):
            self.on = True
            Fader.__init__(self, palette, interval)
    
        def update(self):
            if not self.on:
                self.color = 0
                return
            
            Fader.update(self)
    
    class AutoOffFader(ModeFader):
        def reset(self):
            self.epoc = 0
            self.checkin = time.monotonic()
            self.on = True
            self.index = 0
        
        def update(self):
            ModeFader.update(self)
            if self.on and self.index == len(self.palette)-1:
                self.on = False
    
    green_to_off = (19456, 15360, 11520, 8448, 6144, 4096, 2560, 1536, 768, 256, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    pride = (4980736, 4980736, 4981248, 4982272, 4984064, 4986880, 4990720, 4996096, 3951616, 1592320, 412672, 19456, 13312, 5126, 1048, 60, 76, 65612, 327756, 852044, 1507367, 2359309, 3538946, 4980736)
    
    auto_off = AutoOffFader(green_to_off, 0.05)
    runner = ModeFader(pride, 0.1)
    
    def fire_auto():
        runner.on = False
        auto_off.reset()
    
    def cycle_toggle():
        auto_off.on = False
        runner.on = not runner.on
    
    button1 = Button(board.D4, "a", fire_auto)
    button2 = Button(board.D5, "b", cycle_toggle)
    
    previous = None
    
    while True:
        if auto_off.on:
            fader = auto_off
        if runner.on:
            fader = runner
    
        button1.update()
        button2.update()
        fader.update()
    
        if fader.color != previous:
            rgb.fill(fader.color)
            rgb.write()
            previous = fader.color

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0013-fader-with-a-mode-demo.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0013-fader-with-a-mode-demo.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

In this example, we've taken advantage of a feature of classes called *inheritance* (related to the concept of *polymorphism*). We are able to reuse code in other classes by *extending* one class in another. This makes our code shorter.

We take our base :code:`Fader` class and enhance it by adding an on/off mode, and setting the color to :code:`0` when the fader is turned off (:code:`ModeFader`)

We then extend the :code:`ModeFader` class as :code:`AutoOffFader`, automatically changing the mode to off when the gradient has completed one cycle. We add a new method called :code:`reset()` to allow us to reset the state so the :code:`AutoOffFader` object can do another cycle the next time the button is pressed.

The major change we had to make to previous code was adding an attribute called :code:`index` to the :code:`Fader` class. This attribute tracks the *index* of the current color in the palette. Previously, we only used that value temporarily in the :code:`update()` method. Now that the attribute is tracked, the :code:`AutoOffFader` class can detect when we've hit the end of the palette, so it knows when change modes to "off". This makes it possible to leave all the color selection logic in the :code:`Fader.update()` method.

Appendix 1: Application: Switching Gradients
============================================
We've got all the pieces in place, lets build something that is *almost* a useful project. In doing so, we'll demonstrate how you can use pre-calculated gradients to provide functionality that lets a user set their preferences. The basic concepts here can be adapted to any project using a fading neopixel animation.

We'll build the following features:

* You can turn the neopixels on or off using the slider switch.
* You can cycle through a few pre-calculated gradients by pressing the A button.
* You can cycle through 6 levels of dimming by pressing the B button.

This time around, we'll break up our code into separate *modules* to make things a bit easier to follow.

First, the button and switch code. On your CircuitPython board, save the following as :code:`button.py`:

.. code-block:: python
    
    import time
    from digitalio import DigitalInOut, Direction, Pull
    
    class Button:
        _debounce = 0.1
    
        def __init__(self, pin, name, onpress=None, onrelease=None):
            self.name = name
            self.checkin = time.monotonic()
            self.onrelease = onrelease
            self.onpress = onpress
            self.input = DigitalInOut(pin)
            self.input.direction = Direction.INPUT
            self.input.pull = Pull.DOWN
            self.state = self.input.value
    
        def press(self):
            print(self.name, "pressed")
            if self.onpress:
                self.onpress()
    
        def release(self):
            print(self.name, "released")
            if self.onrelease:
                self.onrelease()
    
        def check(self):
            return self.input.value
    
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                if self.state and not self.check():
                    self.release()
    
                if not self.state and self.check():
                    self.press()
    
                self.state = self.check()
    
                self.checkin = time.monotonic()
    
    class Switch(Button):
        def __init__(self, pin, name, onpress=None, onrelease=None):
            Button.__init__(self, pin, name, onpress, onrelease)
            self.input.pull = Pull.UP
    

Next, add our fader classes from earlier to :code:`fader.py`:

.. code-block:: python
    
    import time
    
    class Fader:
        def __init__(self, palette, interval=0.1):
            self.checkin = time.monotonic()
            self.color = 0
            self.interval = interval
            self.palette = palette
            self.max = len(self.palette)*interval
            self.epoch = 0
            self.index = 0
    
        def update(self):
            self.epoch = time.monotonic() - self.checkin
    
            self.index = round((self.epoch%self.max)/self.interval)
    
            if self.index > len(self.palette)-1:
                self.index = 0
                self.checkin = time.monotonic()
    
            self.color = self.palette[self.index]
    
    class ModeFader(Fader):
        def __init__(self, palette, interval=0.1):
            self.on = True
            Fader.__init__(self, palette, interval)
    
        def update(self):
            if not self.on:
                self.color = 0
                return
    
            Fader.update(self)
    
    class AutoOffFader(ModeFader):
        def reset(self):
            self.epoc = 0
            self.checkin = time.monotonic()
            self.on = True
            self.index = 0
    
        def update(self):
            ModeFader.update(self)
            if self.on and self.index == len(self.palette)-1:
                self.on = False

Next, set up a few gradients we want to cycle through in a module called :code:`colors.py` (generate these yourself, or copy them from below - note we've built them using brightness values of :code:`(1.0, 0.7, 0.5, 0.3, 0.1, 0.05)`):

.. code-block:: python
    
    ireland = (
        (65280, 130817, 458502, 1376020, 2948908, 5308240, 8716164, 13172680, 16773603, 16763032, 16753504, 16745270, 16738075, 16732170, 16727042, 16722688, 13119488, 8667648, 5265152, 2912256, 1346816, 438016, 120064, 65280),
        (45824, 45824, 307972, 963342, 2011934, 3715896, 6075228, 9221004, 11774110, 11766890, 11760195, 11754534, 11749394, 11745287, 11741697, 11738624, 9183744, 6041088, 3685632, 1986048, 942848, 293376, 38144, 45824),
        (32768, 32768, 229379, 688138, 1474582, 2654248, 4358210, 6586468, 8419441, 8414284, 8409392, 8405275, 8401677, 8398853, 8396289, 8393984, 6559744, 4333824, 2632448, 1456128, 673280, 218880, 27136, 32768),
        (19456, 19456, 150530, 412678, 871437, 1592344, 2575399, 3951676, 4999236, 4996141, 4993308, 4990736, 4988680, 4986883, 4985344, 4984064, 3935744, 2560768, 1579520, 860416, 403968, 144384, 16128, 19456),
        (6400, 6400, 6400, 137474, 268548, 530696, 858381, 1317140, 1644566, 1643535, 1642505, 1641733, 1640962, 1640449, 1639936, 1639424, 1311744, 853504, 526336, 264960, 134656, 4352, 5376, 6400),
        (3072, 3072, 3072, 68609, 134146, 265220, 396294, 658442, 789515, 788999, 788484, 787970, 787713, 787456, 787200, 786944, 655872, 393984, 263168, 132352, 67328, 2048, 2560, 3072),
    )
    pride = (
        (16711680, 16711936, 16713216, 16716800, 16722688, 16732160, 16745216, 16762880, 13172480, 5308160, 1376000, 130816, 44801, 17172, 3664, 200, 255, 327935, 1179903, 2883839, 5111940, 8060972, 11927558, 16711680),
        (11730944, 11730944, 11731968, 11734528, 11738624, 11745280, 11754496, 11766784, 9220864, 3715840, 963328, 45824, 31232, 11790, 2616, 140, 179, 196787, 852147, 1966259, 3539036, 5636126, 8323076, 11730944),
        (8388608, 8388608, 8389376, 8391168, 8393984, 8398848, 8405248, 8414208, 6586368, 2654208, 688128, 32768, 22272, 8458, 1832, 100, 128, 131200, 589952, 1441920, 2555970, 3997718, 5963779, 8388608),
        (4980736, 4980736, 4981248, 4982272, 4984064, 4986880, 4990720, 4996096, 3951616, 1592320, 412672, 19456, 13312, 5126, 1048, 60, 76, 65612, 327756, 852044, 1507367, 2359309, 3538946, 4980736),
        (1638400, 1638400, 1638400, 1638912, 1639424, 1640448, 1641728, 1643520, 1317120, 530688, 137472, 6400, 4352, 1538, 264, 20, 25, 25, 65561, 262169, 458765, 786436, 1179648, 1638400),
        (786432, 786432, 786432, 786688, 786944, 787456, 787968, 788992, 658432, 265216, 68608, 3072, 2048, 769, 4, 10, 12, 12, 12, 131084, 196614, 393218, 589824, 786432),
    )
    halloween = (
        (16721408, 15015424, 13375234, 11931910, 10488846, 9242651, 8062252, 6947651, 5964128, 5111940, 4260015, 3539171, 3539171, 4260015, 5111940, 5964128, 6947651, 8062252, 9242651, 10488846, 11931910, 13375234, 15015424, 16721408),
        (11737856, 10491136, 9375745, 8326148, 7342090, 6423826, 5636894, 4850222, 4194627, 3539036, 3014778, 2490526, 2490526, 3014778, 3539036, 4194627, 4850222, 5636894, 6423826, 7342090, 8326148, 9375745, 10491136, 11737856),
        (8393472, 7474944, 6687489, 5965827, 5244423, 4588557, 3998230, 3473697, 2949168, 2555970, 2097239, 1769585, 1769585, 2097239, 2555970, 2949168, 3473697, 3998230, 4588557, 5244423, 5965827, 6687489, 7474944, 8393472),
        (4983552, 4458752, 3999232, 3540226, 3146500, 2753032, 2359565, 2097172, 1769500, 1507367, 1245236, 1048644, 1048644, 1245236, 1507367, 1769500, 2097172, 2359565, 2753032, 3146500, 3540226, 3999232, 4458752, 4983552),
        (1639168, 1442560, 1311232, 1179904, 1048833, 917506, 786436, 655366, 589833, 458765, 393233, 327702, 327702, 393233, 458765, 589833, 655366, 786436, 917506, 1048833, 1179904, 1311232, 1442560, 1639168),
        (786688, 721152, 655616, 589824, 524288, 458753, 393218, 327683, 262148, 196614, 196616, 131083, 131083, 196616, 196614, 262148, 327683, 393218, 458753, 524288, 589824, 655616, 721152, 786688),
    )
    
Finally, we can tie it all together in :code:`code.py`. We'll use a class to track our global state, called :code:`State`:

            
.. code-block:: python
    
    import board
    import time
    import neopixel
    from fader import Fader
    from button import Button, Switch
    from colors import pride, halloween, ireland
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    class State:
        def __init__(self):
            self.button_a = Button(board.D4, "A", None, self.change)
            self.button_b = Button(board.D5, "B", None, self.dim)
            self.switch = Switch(board.D7, "S", self.on, self.off)
            
            self.switch.update()
            self.enabled = self.switch.state
            
            self.color = 0
            
            self.previous = 0
            
            self.gradients = (
                ireland,
                pride,
                halloween
            )
            
            self.level = len(self.gradients[0])-1
            
            self.fader = Fader(self.gradient, 0.1)
            
        @property
        def gradient(self):
            return self.gradients[self.color][self.level]
            
        def on(self):
            self.enabled = True
            
        def off(self):
            self.enabled = False
        
        def change(self):
            self.color += 1
            if self.color > len(self.gradients)-1:
                self.color = 0
                
            self.fader.palette = self.gradient
                
        def dim(self):
            self.level -= 1
            if self.level < 0:
                self.level = len(self.gradients[0])-1
                
            self.fader.palette = self.gradient
            
        def update(self):
            self.button_a.update()
            self.button_b.update()
            self.switch.update()
            self.fader.update()
            
            if not self.enabled:
                rgb.fill(0)
                rgb.write()
            elif self.fader.color != self.previous:
                rgb.fill(self.fader.color)
                rgb.write()
                self.previous = self.fader.color
          
        
    state = State()
    rgb.fill(0)
    rgb.write()
    while True:
        state.update()

        
Here's what it looks like in action:
        
.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0013-fader-with-a-mode-demo.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0013-fader-with-a-mode-demo.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   

Appedix 2: Using Outboard Neopixels
===================================
If you want to use something besides the CPX or CPB for your projects, or if you want to use more (or less) neopixels, you will need to wire them up yourself.

For complete instructions, see `The Neopixel Überguide <https://learn.adafruit.com/adafruit-neopixel-uberguide>`__, especially the part about `powering neopixels <https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels>`__.

Here, we just want to show a basic wiring setup and what code changes will be needed.

The Example Circuit
-------------------
Lets take a look at a breadboard, featuring an `Adafruit ItsyBitsy M0 Express <https://www.adafruit.com/product/3727>`__, and a `24 NexoPixel ring featuring a fourth pure white pixel <https://www.adafruit.com/product/2862>`__.

Since the itsybitsy doesn't have any built-in buttons, we've added two momentary switches. 


.. image:: {static}/images/time-based-fading/itsy-bitsy-isometric.png
   :width: 80%
   
.. image:: {static}/images/time-based-fading/itsybitsy-demo-circuit.png
   :width: 80%
   

It's all pretty straight forward if you've worked with breadboards before. We've wired up the grey button via the white wire to pin D11, the yellow button via the yellow wire to pin D7, and the data pin of the neopixel strip to D5.

Code Changes
------------

Here, we have the code from `Enhancement: A Fader With A Mode`_ above, modified to use the circuit above, and the modules we created in `Appendix 1: Application: Switching Gradients`_. 

FIrst, lets slightly alter :code:`button.py` to use the correct pull *up* resistor:

.. code-block:: python
    :hl_lines: 14
    
    import time
    from digitalio import DigitalInOut, Direction, Pull
    
    class Button:
        _debounce = 0.1
    
        def __init__(self, pin, name, onpress=None, onrelease=None):
            self.name = name
            self.checkin = time.monotonic()
            self.onrelease = onrelease
            self.onpress = onpress
            self.input = DigitalInOut(pin)
            self.input.direction = Direction.INPUT
            self.input.pull = Pull.UP
            self.state = self.input.value
    
        def press(self):
            print(self.name, "pressed")
            if self.onpress:
                self.onpress()
    
        def release(self):
            print(self.name, "released")
            if self.onrelease:
                self.onrelease()
    
        def check(self):
            return self.input.value
    
        def update(self):
            if time.monotonic() - self.checkin > self._debounce:
                if self.state and not self.check():
                    self.release()
    
                if not self.state and self.check():
                    self.press()
    
                self.state = self.check()
    
                self.checkin = time.monotonic()
    
    class Switch(Button):
        def __init__(self, pin, name, onpress=None, onrelease=None):
            Button.__init__(self, pin, name, onpress, onrelease)
            self.input.pull = Pull.UP

Add two new gradients to :code:`colors.py`, a little different than before but the same idea:

.. code-block:: python
    
    ﻿white_to_off = (
        (16777215, 13158600, 10000536, 7434609, 5263440, 3552822, 2236962, 1315860, 657930, 263172, 65793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (11776947, 9211020, 6974058, 5197647, 3684408, 2500134, 1579032, 921102, 460551, 131586, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (8421504, 6579300, 5000268, 3684408, 2631720, 1776411, 1118481, 657930, 328965, 131586, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (5000268, 3947580, 2960685, 2171169, 1579032, 1052688, 657930, 394758, 197379, 65793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (1644825, 1315860, 986895, 723723, 526344, 328965, 197379, 131586, 65793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (789516, 657930, 460551, 328965, 263172, 131586, 65793, 65793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    )
    

And finally, make the changes to :code:`code.py`. The primary differences here are:

* Importing classes and colors from modules we created.
* Using a single member of the gradients (we've picked level 2, feel free to use whatever brightness level you want)
* Using a different pin for the neopixels (:code:`D5` instead of the playground-specific :code:`NEOPIXEL` alias)
* Specifying the :code:`pixel_order` when creating our :code:`Neopixel` object. This is important, since our neopixel ring has *four* elements instead of three.

.. code-block:: python
    :hl_lines: 3 4 5 7
    
    import board
    import neopixel
    from fader import ModeFader, AutoOffFader
    from button import Button
    from colors import white_to_off, halloween
    
    rgb = neopixel.NeoPixel(board.D5, 24, brightness=1.0, auto_write=False, pixel_order=neopixel.GRBW)
    
    auto_off = AutoOffFader(white_to_off[2], 0.05)
    runner = ModeFader(halloween[2], 0.1)
    
    def fire_auto():
        runner.on = False
        auto_off.reset()
    
    def cycle_toggle():
        auto_off.on = False
        runner.on = not runner.on
    
    button1 = Button(board.D11, "a", fire_auto)
    button2 = Button(board.D7, "b", cycle_toggle)
    
    previous = None
    
    rgb.fill(0)
    rgb.write()
    
    while True:
        if auto_off.on:
            fader = auto_off
        if runner.on:
            fader = runner
    
        button1.update()
        button2.update()
        fader.update()
    
        if fader.color != previous:
            rgb.fill(fader.color)
            rgb.write()
            previous = fader.color
    
And now we can check it out on the ItsyBitsy Express with the 24 neopixel RGBW ring!

.. raw:: html
   
   <div class="video-container">
       <video controls>
          <source src="{static}/videos/time-based-fading/0018-itsybitsy-demo.mp4" type="video/mp4">
          <p>Your browser doesn't support HTML5 video. Here is
             a <a href="{static}/videos/time-based-fading/0018-itsybitsy-demo.mp4">link to the video</a> instead.</p>
       </video>
   </div>
   
You may notice that the extra white pixel is activated when fading from white to off. Very cool |cool|.

Appendix 3: A Bunch Of Pre-Calculated Gradients For Your Enjoyment!
===================================================================
It can be a bit daunting to pre-calculate your gradients if you are new to python, so a small library of fun gradients have been provided to get you up and running quickly.

Each gradient has been generated at 6 different levels, and in sequences of 10, 16, and 24 steps. 

You'll note a lot of the gradients are holiday-themed. This is because this fading code grew out of a project I did - I made macropads for my coworkers out of the `Adafruit PyRuler <https://www.adafruit.com/product/4319>`__. I decided to animate the onboard dotstar in a Christmas theme (red, green, white). I came up with a small suite of holiday and general purpose gradients so they could change thing easily and use their gift all year round.

Code To Generate The Gradients
------------------------------
The gradients provided below were produced using the following script. This builds on what we've done already: uses our :code:`make_gradient()` function to print out a suite of colors defined in a dictionary called :code:`gradients`. Each member of that dictionary is a sequence of :code:`(gradient, wrap)`, indicating the colors to use, and if the gradient should wrap around or not. It cycles through brightness levels listed in :code:`DIM_LEVELS`, and generates the number of colors for each level specified in :code:`COLORS`.

It then prints each gradient out to the console in a way that can be easily copy/pasted, and finally loops through each generated gradient every 4 seconds, displaying it on the neopixels for inspection.

.. code-block:: python
    
    import board
    import neopixel
    from fader import Fader
    import adafruit_fancyled.adafruit_fancyled as fancy
    import time
    
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
    
    DIM_LEVELS = (1.0, 0.7, 0.5, 0.3, 0.1, 0.05)
    COLORS = 24
    
    WHITE = fancy.CRGB(255, 255, 255)
    BLACK = fancy.CRGB(0, 0, 0)
    GRAY = fancy.CRGB(127, 127, 127)
    RED = fancy.CRGB(255, 0, 0)
    GREEN = fancy.CRGB(0, 255, 0)
    YELLOW = fancy.CRGB(255, 255, 0)
    BLUE = fancy.CRGB(0, 0, 255)
    ORANGE = fancy.CRGB(255, 127, 0)
    VIOLET = fancy.CRGB(139, 0, 255)
    INDIGO = fancy.CRGB(46, 43, 95)
    
    PINK = fancy.CRGB(255, 127, 127)
    MINT = fancy.CRGB(127, 255, 127)
    ROBIN = fancy.CRGB(127, 127, 255)
    
    def make_gradient(colors, steps=24, brightness=0.1, wrap=True):
        values = []
        ratio = 1.0/len(colors)
        for index, color in enumerate(colors):
            value = float(index*ratio)
            values.append((value, color))
        
        if wrap:
            values.append((1.0, colors[0]))
    
        palette = []
        for expanded in fancy.expand_gradient(values, steps):
            palette.append(fancy.gamma_adjust(expanded, brightness=brightness).pack())
    
        return tuple(palette)
    
    gradients = {
        'pride': ([RED,ORANGE,YELLOW,GREEN,BLUE,VIOLET], True),
        'halloween': ([ORANGE,VIOLET], True),
        'anna_howard_shaw': ([RED,WHITE,PINK,WHITE], True),
        'pastels': ([PINK,WHITE,MINT,WHITE,ROBIN,WHITE], True),
        'rgb': ([RED, GREEN, BLUE], True),
        'july4': ([RED, WHITE, WHITE, BLUE], True),
        'ireland': ([GREEN, WHITE, ORANGE], True),
        'icy': ([BLUE, ROBIN, WHITE, YELLOW, GRAY, BLUE, ROBIN, WHITE], False),
        'gray': ([WHITE, GRAY, BLACK, GRAY, WHITE], True),
        'white_to_off': ([WHITE, BLACK], False),
        'green_to_off': ([GREEN, BLACK], False),
        'blue_to_off': ([BLUE, BLACK], False),
        'red_to_off': ([RED, BLACK], False),
    }
    
    rgb.fill(0)
    rgb.write()
    
    
    def generate():
        while True:
            for name, data in gradients.items():
                colors, wrap = data
                for brightness in DIM_LEVELS:
                    yield make_gradient(colors, COLORS, brightness, wrap)
    
    cycler = generate()
    
    for name, data in gradients.items():
        colors, wrap = data
        print(name, "= (")
        for brightness in DIM_LEVELS:
            gradient = make_gradient(colors, COLORS, brightness, wrap)
            print("\t", gradient, ",", sep="")
        print(")")
    
    checkin = time.monotonic()
    previous = 0
    
    fader = Fader(next(cycler), 0.1)
    
    rgb.fill(0)
    rgb.write()
    
    while True:
        if time.monotonic() - checkin > 4:
            fader.palette = next(cycler)
            rgb.fill(0)
            rgb.write()
            checkin = time.monotonic()
            time.sleep(1)
    
        fader.update()
    
        if fader.color != previous:
            previous = fader.color
            rgb.fill(fader.color)
            rgb.write()

Rainbow/Pride
-------------
This is the gradient we played with earlier, approximating the pride flag, in celebration of the LBGTQA+ community.

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/pride-24.png
   :height: 2em

.. code-block:: python
    
    pride = (
        (16711680, 16711936, 16713216, 16716800, 16722688, 16732160, 16745216, 16762880, 13172480, 5308160, 1376000, 130816, 44801, 17172, 3664, 200, 255, 327935, 1179903, 2883839, 5111940, 8060972, 11927558, 16711680),
        (11730944, 11730944, 11731968, 11734528, 11738624, 11745280, 11754496, 11766784, 9220864, 3715840, 963328, 45824, 31232, 11790, 2616, 140, 179, 196787, 852147, 1966259, 3539036, 5636126, 8323076, 11730944),
        (8388608, 8388608, 8389376, 8391168, 8393984, 8398848, 8405248, 8414208, 6586368, 2654208, 688128, 32768, 22272, 8458, 1832, 100, 128, 131200, 589952, 1441920, 2555970, 3997718, 5963779, 8388608),
        (4980736, 4980736, 4981248, 4982272, 4984064, 4986880, 4990720, 4996096, 3951616, 1592320, 412672, 19456, 13312, 5126, 1048, 60, 76, 65612, 327756, 852044, 1507367, 2359309, 3538946, 4980736),
        (1638400, 1638400, 1638400, 1638912, 1639424, 1640448, 1641728, 1643520, 1317120, 530688, 137472, 6400, 4352, 1538, 264, 20, 25, 25, 65561, 262169, 458765, 786436, 1179648, 1638400),
        (786432, 786432, 786432, 786688, 786944, 787456, 787968, 788992, 658432, 265216, 68608, 3072, 2048, 769, 4, 10, 12, 12, 12, 131084, 196614, 393218, 589824, 786432),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/pride-16.png
   :height: 2em

.. code-block:: python
    
    pride = (
        (16711680, 16712448, 16717056, 16727808, 16747264, 16776960, 4259584, 261888, 35843, 5440, 255, 262399, 1769727, 4915340, 9699349, 16711680),
        (11730944, 11731456, 11734528, 11742208, 11755776, 11776768, 2994944, 176896, 25090, 3885, 179, 131251, 1245363, 3407970, 6815759, 11730944),
        (8388608, 8388864, 8391168, 8396544, 8406272, 8421376, 2129920, 98304, 17921, 2592, 128, 131200, 852096, 2424902, 4849674, 8388608),
        (4980736, 4980736, 4982272, 4985600, 4991232, 5000192, 1264640, 19456, 10752, 1555, 76, 65612, 524364, 1441834, 2883590, 4980736),
        (1638400, 1638400, 1638912, 1639936, 1641728, 1644800, 399616, 6400, 3584, 518, 25, 25, 131097, 458766, 917506, 1638400),
        (786432, 786432, 786688, 787200, 787968, 789504, 199680, 3072, 1792, 259, 12, 12, 65548, 196615, 458753, 786432),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/pride-10.png
   :height: 2em

.. code-block:: python
    
    pride = (
        (16711680, 16715008, 16733440, 16776960, 917248, 21773, 255, 1048831, 6291541, 16711680),
        (11730944, 11733248, 11746048, 11776768, 635648, 15113, 179, 721075, 4390971, 11730944),
        (8388608, 8390144, 8399360, 8421376, 425984, 10758, 128, 524416, 3145770, 8388608),
        (4980736, 4981504, 4987136, 5000192, 216064, 6403, 76, 262220, 1835033, 4980736),
        (1638400, 1638656, 1640448, 1644800, 71936, 2049, 25, 65561, 589832, 1638400),
        (786432, 786432, 787456, 789504, 3072, 1024, 12, 12, 262148, 786432),
    )

Halloween
---------
The unofficial colors of the night before All Saint's Day are orange and purple. Due to the wavelengths involved in making blue light, the :code:`VIOLET` color looks almost like ultra-violet, like black velvet illuminated by a black light. Spooky!

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/halloween-24.png
   :height: 2em

.. code-block:: python

    halloween = (
        (16721408, 15015424, 13375234, 11931910, 10488846, 9242651, 8062252, 6947651, 5964128, 5111940, 4260015, 3539171, 3539171, 4260015, 5111940, 5964128, 6947651, 8062252, 9242651, 10488846, 11931910, 13375234, 15015424, 16721408),
        (11737856, 10491136, 9375745, 8326148, 7342090, 6423826, 5636894, 4850222, 4194627, 3539036, 3014778, 2490526, 2490526, 3014778, 3539036, 4194627, 4850222, 5636894, 6423826, 7342090, 8326148, 9375745, 10491136, 11737856),
        (8393472, 7474944, 6687489, 5965827, 5244423, 4588557, 3998230, 3473697, 2949168, 2555970, 2097239, 1769585, 1769585, 2097239, 2555970, 2949168, 3473697, 3998230, 4588557, 5244423, 5965827, 6687489, 7474944, 8393472),
        (4983552, 4458752, 3999232, 3540226, 3146500, 2753032, 2359565, 2097172, 1769500, 1507367, 1245236, 1048644, 1048644, 1245236, 1507367, 1769500, 2097172, 2359565, 2753032, 3146500, 3540226, 3999232, 4458752, 4983552),
        (1639168, 1442560, 1311232, 1179904, 1048833, 917506, 786436, 655366, 589833, 458765, 393233, 327702, 327702, 393233, 458765, 589833, 655366, 786436, 917506, 1048833, 1179904, 1311232, 1442560, 1639168),
        (786688, 721152, 655616, 589824, 524288, 458753, 393218, 327683, 262148, 196614, 196616, 131083, 131083, 196616, 196614, 262148, 327683, 393218, 458753, 524288, 589824, 655616, 721152, 786688),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/halloween-16.png
   :height: 2em

.. code-block:: python

    halloween = (
        (16721408, 14162433, 11800583, 9701653, 7865390, 6292053, 4915340, 3735764, 3735764, 4915340, 6292053, 7865390, 9701653, 11800583, 14162433, 16721408),
        (11737856, 9900544, 8260357, 6817295, 5505824, 4391227, 3407970, 2621588, 2621588, 3407970, 4391227, 5505824, 6817295, 8260357, 9900544, 11737856),
        (8393472, 7081216, 5900291, 4850698, 3932695, 3146026, 2424902, 1835114, 1835114, 2424902, 3146026, 3932695, 4850698, 5900291, 7081216, 8393472),
        (4983552, 4196096, 3540226, 2884102, 2359566, 1835033, 1441834, 1114175, 1114175, 1441834, 1835033, 2359566, 2884102, 3540226, 4196096, 4983552),
        (1639168, 1376768, 1179904, 917506, 786436, 589832, 458766, 327701, 327701, 458766, 589832, 786436, 917506, 1179904, 1376768, 1639168),
        (786688, 655616, 589824, 458753, 393218, 262148, 196615, 131082, 131082, 196615, 262148, 393218, 458753, 589824, 655616, 786688),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/halloween-10.png
   :height: 2em

.. code-block:: python

    halloween = (
        (16721408, 12522244, 9111324, 6292053, 4128954, 4128954, 6292053, 9111324, 12522244, 16721408),
        (11737856, 8785155, 6358292, 4391227, 2883714, 2883714, 4391227, 6358292, 8785155, 11737856),
        (8393472, 6228226, 4522766, 3146026, 2031709, 2031709, 3146026, 4522766, 6228226, 8393472),
        (4983552, 3736833, 2687496, 1835033, 1179703, 1179703, 1835033, 2687496, 3736833, 4983552),
        (1639168, 1245440, 851970, 589832, 393234, 393234, 589832, 851970, 1245440, 1639168),
        (786688, 589824, 393217, 262148, 196617, 196617, 262148, 393217, 589824, 786688),
    )

Anna Howard Shaw
----------------
A nod to an episode of a favorite TV comedy of mine, `30 Rock <https://en.wikipedia.org/wiki/Anna_Howard_Shaw_Day>`__. The main character, Liz Lemon, chooses to celebrate the birthday of pioneering suffragette and physician Anna Howard Shaw, instead of St. Valentine's day. A blend of red, white and pink to reflect the holiday (whichever you choose to celebrate!)

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/anna_howard_shaw-24.png
   :height: 2em

.. code-block:: python
    
    anna_howard_shaw = (
        (16711680, 16712194, 16715278, 16722988, 16736352, 16756655, 16773617, 16759739, 16747917, 16738151, 16730441, 16724016, 16724016, 16730441, 16738151, 16747917, 16759739, 16773617, 16756655, 16736352, 16722988, 16715278, 16712194, 16711680),
        (11730944, 11731201, 11733514, 11738654, 11748163, 11762298, 11774120, 11764611, 11756387, 11749448, 11744051, 11739682, 11739682, 11744051, 11749448, 11756387, 11764611, 11774120, 11762298, 11748163, 11738654, 11733514, 11731201, 11730944),
        (8388608, 8388865, 8390407, 8394262, 8400944, 8410967, 8419448, 8412509, 8406598, 8401715, 8397860, 8394776, 8394776, 8397860, 8401715, 8406598, 8412509, 8419448, 8410967, 8400944, 8394262, 8390407, 8388865, 8388608),
        (4980736, 4980736, 4981764, 4984077, 4987932, 4994100, 4999240, 4995128, 4991530, 4988703, 4986133, 4984334, 4984334, 4986133, 4988703, 4991530, 4995128, 4999240, 4994100, 4987932, 4984077, 4981764, 4980736, 4980736),
        (1638400, 1638400, 1638657, 1639428, 1640713, 1642769, 1644568, 1643026, 1641998, 1640970, 1640199, 1639428, 1639428, 1640199, 1640970, 1641998, 1643026, 1644568, 1642769, 1640713, 1639428, 1638657, 1638400, 1638400),
        (786432, 786432, 786432, 786946, 787460, 788488, 789516, 788745, 788231, 787717, 787203, 786946, 786946, 787203, 787717, 788231, 788745, 789516, 788488, 787460, 786946, 786432, 786432, 786432),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/anna_howard_shaw-16.png
   :height: 2em

.. code-block:: python
    
    anna_howard_shaw = (
        (16711680, 16713479, 16723502, 16747660, 16771561, 16751772, 16736609, 16725558, 16725558, 16736609, 16751772, 16771561, 16747660, 16723502, 16713479, 16711680),
        (11730944, 11732229, 11739168, 11756130, 11772835, 11758957, 11748420, 11740710, 11740710, 11748420, 11758957, 11772835, 11756130, 11739168, 11732229, 11730944),
        (8388608, 8389379, 8394519, 8406598, 8418420, 8408654, 8400944, 8395547, 8395547, 8400944, 8408654, 8418420, 8406598, 8394519, 8389379, 8388608),
        (4980736, 4981250, 4984334, 4991530, 4998726, 4992558, 4988189, 4984848, 4984848, 4988189, 4992558, 4998726, 4991530, 4984334, 4981250, 4980736),
        (1638400, 1638400, 1639428, 1641998, 1644311, 1642255, 1640713, 1639685, 1639685, 1640713, 1642255, 1644311, 1641998, 1639428, 1638400, 1638400),
        (786432, 786432, 786946, 788231, 789259, 788231, 787460, 786946, 786946, 787460, 788231, 789259, 788231, 786946, 786432, 786432),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/anna_howard_shaw-10.png
   :height: 2em

.. code-block:: python
    
    anna_howard_shaw = (
        (16711680, 16718876, 16759482, 16751772, 16728899, 16728899, 16751772, 16759482, 16718876, 16711680),
        (11730944, 11736084, 11764354, 11758957, 11743023, 11743023, 11758957, 11764354, 11736084, 11730944),
        (8388608, 8392206, 8412509, 8408654, 8397089, 8397089, 8408654, 8412509, 8392206, 8388608),
        (4980736, 4982792, 4994871, 4992558, 4985876, 4985876, 4992558, 4994871, 4982792, 4980736),
        (1638400, 1638914, 1643026, 1642255, 1639942, 1639942, 1642255, 1643026, 1638914, 1638400),
        (786432, 786689, 788745, 788231, 787203, 787203, 788231, 788745, 786689, 786432),
    )

Pastels
-------
Evoking the softer colors of spring, this gradient features pastels common during the Easter holiday. Perfect for your egg-shaped lighting projects.

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/pastels-24.png
   :height: 2em

.. code-block:: python

    pastels = (
        (16721446, 16730441, 16742777, 16759739, 15859697, 10747811, 6815591, 3997500, 3211056, 5766999, 9305997, 14024661, 14013951, 9276927, 5724159, 3158271, 3947775, 6776831, 10724351, 15856127, 16759739, 16742777, 16730441, 16721446),
        (11737883, 11744051, 11752789, 11764611, 11056040, 7517042, 4764488, 2798378, 2274082, 4043581, 6533987, 9810837, 9803187, 6513587, 4013491, 2237107, 2763443, 4737203, 7500467, 11053235, 11764611, 11752789, 11744051, 11737883),
        (8393491, 8397860, 8404028, 8412509, 7897208, 5341265, 3375155, 1998878, 1605656, 2850859, 4620358, 6979690, 6974080, 4605568, 2829184, 1579136, 1973888, 3355520, 5329280, 7895168, 8412509, 8404028, 8397860, 8393491),
        (4983563, 4986133, 4989988, 4995128, 4738120, 3230769, 2051103, 1199122, 936974, 1723418, 2772010, 4148287, 4144972, 2763340, 1710668, 921164, 1184332, 2039628, 3223884, 4737100, 4995128, 4989988, 4986133, 4983563),
        (1639171, 1640199, 1641484, 1643026, 1579288, 1054992, 661770, 399622, 268548, 530696, 923918, 1382677, 1381657, 921113, 526361, 263193, 394777, 657945, 1052697, 1579033, 1643026, 1641484, 1640199, 1639171),
        (786689, 787203, 787974, 788745, 789516, 527368, 330757, 199683, 134146, 265220, 461831, 658442, 657932, 460556, 263180, 131596, 197388, 328972, 526348, 789516, 788745, 787974, 787203, 786689),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/pastels-16.png
   :height: 2em

.. code-block:: python

    pastels = (
        (16721446, 16736609, 16761024, 12648384, 6422369, 2555686, 6422369, 12648384, 12632319, 6382079, 2500351, 6382079, 12632319, 16761024, 16736609, 16721446),
        (11737883, 11748420, 11765382, 8827782, 4502340, 1815323, 4502340, 8827782, 8816307, 4474035, 1776563, 4474035, 8816307, 11765382, 11748420, 11737883),
        (8393491, 8400944, 8413280, 6324320, 3178544, 1277971, 3178544, 6324320, 6316160, 3158144, 1250176, 3158144, 6316160, 8413280, 8400944, 8393491),
        (4983563, 4988189, 4995385, 3755065, 1920029, 740363, 1920029, 3755065, 3750220, 1908044, 723788, 1908044, 3750220, 4995385, 4988189, 4983563),
        (1639171, 1640713, 1643283, 1251603, 596233, 203011, 596233, 1251603, 1250073, 592153, 197401, 592153, 1250073, 1643283, 1640713, 1639171),
        (786689, 787460, 788745, 592905, 265220, 68609, 265220, 592905, 592140, 263180, 65804, 263180, 592140, 788745, 787460, 786689),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/pastels-10.png
   :height: 2em

.. code-block:: python

    pastels = (
        (16721446, 16751772, 10289052, 2555686, 10289052, 10263807, 2500351, 10263807, 16751772, 16721446),
        (11737883, 11758957, 7189357, 1815323, 7189357, 7171507, 1776563, 7171507, 11758957, 11737883),
        (8393491, 8408654, 5144654, 1277971, 5144654, 5131904, 1250176, 5131904, 8408654, 8393491),
        (4983563, 4992558, 3034158, 740363, 3034158, 3026508, 723788, 3026508, 4992558, 4983563),
        (1639171, 1642255, 989455, 203011, 989455, 986905, 197401, 986905, 1642255, 1639171),
        (786689, 788231, 461831, 68609, 461831, 460556, 65804, 460556, 788231, 786689),
    )


RGB
---
The standard colors used to make up all other colors. A symbol of additive color mixing and representative of the internal anatomy of the human eye.

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/rgb-24.png
   :height: 2em

.. code-block:: python

    rgb = (
        (16711680, 11469056, 7407104, 4396032, 2239488, 937984, 295936, 51200, 58112, 38914, 24586, 13851, 6966, 2656, 664, 227, 200, 262276, 917584, 2228268, 4390932, 7405574, 11468801, 16711680),
        (11730944, 7995392, 5178368, 3018240, 1580544, 669696, 154624, 35840, 40448, 27137, 17159, 9746, 4646, 1859, 362, 158, 140, 131164, 655416, 1572894, 3014670, 5177348, 7995392, 11730944),
        (8388608, 5701632, 3670784, 2165248, 1119744, 468992, 147968, 25600, 28928, 19457, 12293, 6925, 3355, 1328, 332, 113, 100, 131138, 458792, 1114134, 2162698, 3670019, 5701632, 8388608),
        (4980736, 3407872, 2163200, 1312256, 658688, 268288, 75520, 15360, 17408, 11520, 7171, 4104, 2064, 796, 45, 68, 60, 65575, 262168, 655373, 1310726, 2162690, 3407872, 4980736),
        (1638400, 1114112, 720896, 393728, 197632, 67584, 3328, 5120, 5632, 3840, 2305, 1282, 517, 265, 15, 22, 20, 13, 65544, 196612, 393218, 720896, 1114112, 1638400),
        (786432, 524288, 327680, 196864, 66048, 1024, 1536, 2560, 2816, 1792, 1024, 513, 258, 4, 7, 11, 10, 6, 4, 65538, 196609, 327680, 524288, 786432),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/rgb-16.png
   :height: 2em

.. code-block:: python

    rgb = (
        (16711680, 9175808, 4199680, 1392640, 232448, 65280, 35843, 16405, 5440, 908, 255, 196748, 1376320, 4194325, 9175043, 16711680),
        (11730944, 6423040, 2952960, 994560, 156160, 45824, 25090, 11535, 3885, 610, 179, 131170, 983085, 2949135, 6422530, 11730944),
        (8388608, 4587776, 2099712, 663552, 83456, 32768, 17921, 8202, 2592, 326, 128, 65606, 655392, 2097162, 4587521, 8388608),
        (4980736, 2752512, 1246720, 398080, 10752, 19456, 10752, 4870, 1555, 42, 76, 42, 393235, 1245190, 2752512, 4980736),
        (1638400, 917504, 393728, 132608, 3584, 6400, 3584, 1538, 518, 14, 25, 14, 131078, 393218, 917504, 1638400),
        (786432, 458752, 196864, 66304, 1792, 3072, 1792, 769, 259, 7, 12, 7, 65539, 196609, 458752, 786432),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/rgb-10.png
   :height: 2em

.. code-block:: python

    rgb = (
        (16711680, 5573888, 873728, 65280, 21773, 3413, 255, 852053, 5570573, 16711680),
        (11730944, 3868928, 604928, 45824, 15113, 2363, 179, 589883, 3866633, 11730944),
        (8388608, 2754048, 403968, 32768, 10758, 1578, 128, 393258, 2752518, 8388608),
        (4980736, 1639168, 203008, 19456, 6403, 793, 76, 196633, 1638403, 4980736),
        (1638400, 524544, 67584, 6400, 2049, 264, 25, 65544, 524289, 1638400),
        (786432, 262144, 1024, 3072, 1024, 4, 12, 4, 262144, 786432),
    )


July 4th
--------
In the US, July 4th is celebrated as Independence Day. A swath of red, white and blue that represents the stars and stripes of the US flag. Works for Puerto Rico too. Can be reversed for authentic French flag colors.

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/july4-24.png
   :height: 2em

.. code-block:: python

    july4 = (
        (16711680, 16712194, 16715278, 16722988, 16736352, 16756655, 16777215, 16777215, 16777215, 16777215, 16777215, 16777215, 13158655, 7434751, 3553023, 1316095, 263423, 255, 65711, 655456, 2228268, 5242894, 9961474, 16711680),
        (11730944, 11731201, 11733514, 11738654, 11748163, 11762298, 11776947, 11776947, 11776947, 11776947, 11776947, 11776947, 9211059, 5197747, 2500275, 921267, 131763, 179, 122, 458819, 1572894, 3670026, 6946817, 11730944),
        (8388608, 8388865, 8390407, 8394262, 8400944, 8410967, 8421504, 8421504, 8421504, 8421504, 8421504, 8421504, 6579328, 3684480, 1776512, 658048, 131712, 128, 87, 327728, 1114134, 2621447, 4980737, 8388608),
        (4980736, 4980736, 4981764, 4984077, 4987932, 4994100, 5000268, 5000268, 5000268, 5000268, 5000268, 5000268, 3947596, 2171212, 1052748, 394828, 65868, 76, 52, 196636, 655373, 1572868, 2949120, 4980736),
        (1638400, 1638400, 1638657, 1639428, 1640713, 1642769, 1644825, 1644825, 1644825, 1644825, 1644825, 1644825, 1315865, 723737, 328985, 131609, 25, 25, 17, 65545, 196612, 524289, 983040, 1638400),
        (786432, 786432, 786432, 786946, 787460, 788488, 789516, 789516, 789516, 789516, 789516, 789516, 657932, 328972, 131596, 65804, 12, 12, 8, 4, 65538, 262144, 458752, 786432),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/july4-16.png
   :height: 2em

.. code-block:: python

    july4 = (
        (16711680, 16713479, 16723502, 16747660, 16777215, 16777215, 16777215, 16777215, 11382271, 4210943, 855551, 255, 196748, 2097198, 7208967, 16711680),
        (11730944, 11732229, 11739168, 11756130, 11776947, 11776947, 11776947, 11776947, 7961011, 2960819, 592307, 179, 131170, 1441824, 5046277, 11730944),
        (8388608, 8389379, 8394519, 8406598, 8421504, 8421504, 8421504, 8421504, 5658240, 2105472, 394880, 128, 65606, 1048599, 3604483, 8388608),
        (4980736, 4981250, 4984334, 4991530, 5000268, 5000268, 5000268, 5000268, 3421260, 1250124, 197452, 76, 42, 589838, 2162690, 4980736),
        (1638400, 1638400, 1639428, 1641998, 1644825, 1644825, 1644825, 1644825, 1118489, 394777, 65817, 25, 14, 196612, 720896, 1638400),
        (786432, 786432, 786946, 788231, 789516, 789516, 789516, 789516, 526348, 197388, 12, 12, 7, 65538, 327680, 786432),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/july4-10.png
   :height: 2em

.. code-block:: python

    july4 = (
        (16711680, 16718876, 16759482, 16777215, 16777215, 8487423, 855551, 186, 3407900, 16711680),
        (11730944, 11736084, 11764354, 11776947, 11776947, 5921459, 592307, 130, 2359316, 11730944),
        (8388608, 8392206, 8412509, 8421504, 8421504, 4210816, 394880, 93, 1703950, 8388608),
        (4980736, 4982792, 4994871, 5000268, 5000268, 2500172, 197452, 55, 983048, 4980736),
        (1638400, 1638914, 1643026, 1644825, 1644825, 789529, 65817, 18, 327682, 1638400),
        (786432, 786689, 788745, 789516, 789516, 394764, 12, 9, 131073, 786432),
    )


Ireland
-------
The colors of the Irish national flag. In the US, it reminds us of St. Patrick's day, celebrated in March. Green, White and Orange.

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/ireland-24.png
   :height: 2em

.. code-block:: python

    ireland = (
        (65280, 130817, 458502, 1376020, 2948908, 5308240, 8716164, 13172680, 16773603, 16763032, 16753504, 16745270, 16738075, 16732170, 16727042, 16722688, 13119488, 8667648, 5265152, 2912256, 1346816, 438016, 120064, 65280),
        (45824, 45824, 307972, 963342, 2011934, 3715896, 6075228, 9221004, 11774110, 11766890, 11760195, 11754534, 11749394, 11745287, 11741697, 11738624, 9183744, 6041088, 3685632, 1986048, 942848, 293376, 38144, 45824),
        (32768, 32768, 229379, 688138, 1474582, 2654248, 4358210, 6586468, 8419441, 8414284, 8409392, 8405275, 8401677, 8398853, 8396289, 8393984, 6559744, 4333824, 2632448, 1456128, 673280, 218880, 27136, 32768),
        (19456, 19456, 150530, 412678, 871437, 1592344, 2575399, 3951676, 4999236, 4996141, 4993308, 4990736, 4988680, 4986883, 4985344, 4984064, 3935744, 2560768, 1579520, 860416, 403968, 144384, 16128, 19456),
        (6400, 6400, 6400, 137474, 268548, 530696, 858381, 1317140, 1644566, 1643535, 1642505, 1641733, 1640962, 1640449, 1639936, 1639424, 1311744, 853504, 526336, 264960, 134656, 4352, 5376, 6400),
        (3072, 3072, 3072, 68609, 134146, 265220, 396294, 658442, 789515, 788999, 788484, 787970, 787713, 787456, 787200, 786944, 655872, 393984, 263168, 132352, 67328, 2048, 2560, 3072),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/ireland-16.png
   :height: 2em

.. code-block:: python

    ireland = (
        (65280, 261891, 1441557, 4259648, 9240460, 16777215, 16760972, 16747328, 16736533, 16727811, 16721408, 9191168, 4219136, 1411840, 245760, 65280),
        (45824, 176898, 1028879, 2994989, 6468450, 11776947, 11765346, 11755821, 11748367, 11742210, 11737856, 6433792, 2966528, 1007872, 165376, 45824),
        (32768, 98305, 688138, 2129952, 4620358, 8421504, 8413254, 8406304, 8400906, 8396545, 8393472, 4595456, 2109440, 673024, 90112, 32768),
        (19456, 19456, 412678, 1264659, 2772010, 5000268, 4995370, 4991251, 4988166, 4985600, 4983552, 2757376, 1252608, 403712, 14592, 19456),
        (6400, 6400, 137474, 399622, 923918, 1644825, 1643278, 1641734, 1640706, 1639936, 1639168, 919040, 395520, 134400, 4864, 6400),
        (3072, 3072, 68609, 199683, 461831, 789516, 788743, 787971, 787457, 787200, 786688, 459520, 197632, 67072, 2304, 3072),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/ireland-10.png
   :height: 2em

.. code-block:: python

    ireland = (
        (65280, 917261, 5635925, 16777215, 16751701, 16733453, 16721408, 5592320, 891904, 65280),
        (45824, 635657, 3912507, 11776947, 11758907, 11746057, 11737856, 3881728, 617728, 45824),
        (32768, 425990, 2785322, 8421504, 8408618, 8399366, 8393472, 2763264, 413184, 32768),
        (19456, 216067, 1657881, 5000268, 4992537, 4987139, 4983552, 1644800, 208384, 19456),
        (6400, 71937, 530696, 1644825, 1642248, 1640449, 1639168, 526336, 69376, 6400),
        (3072, 3072, 265220, 789516, 788228, 787456, 786688, 263168, 1792, 3072),
    )

Icy
---
An experimental winter gradient, meant to imply the flash of lights twinkling off of ice and snow, grey skies and warm feelings of the broader holiday season. Also `golden age Batman <https://en.wikipedia.org/wiki/Batman#Golden_age>`__.

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/icy-24.png
   :height: 2em

.. code-block:: python

    icy = (
        (255, 131839, 921343, 2829311, 6250495, 11513855, 16777160, 16777014, 16776964, 14013696, 7960837, 3947543, 1513276, 329081, 213, 255, 526591, 1974015, 4803071, 9276927, 15856127, 16777215, 16777215, 16777215),
        (179, 65971, 658099, 1973939, 4342451, 8026803, 11776908, 11776806, 11776770, 9803008, 5592323, 2763280, 1052714, 197461, 149, 179, 329139, 1381811, 3355571, 6513587, 11053235, 11776947, 11776947, 11776947),
        (128, 65920, 460672, 1381760, 3092352, 5724032, 8421476, 8421403, 8421378, 6973952, 3947522, 1973771, 723742, 131644, 106, 128, 263296, 987008, 2368640, 4605568, 7895168, 8421504, 8421504, 8421504),
        (76, 76, 263244, 855372, 1842252, 3421260, 5000252, 5000208, 5000193, 4144896, 2368513, 1184262, 394770, 65828, 63, 76, 131660, 592204, 1381708, 2763340, 4737100, 5000268, 5000268, 5000268),
        (25, 25, 65817, 263193, 592153, 1118489, 1644820, 1644805, 1644800, 1381632, 789504, 394754, 131590, 12, 21, 25, 25, 197401, 460569, 921113, 1579033, 1644825, 1644825, 1644825),
        (12, 12, 12, 131596, 263180, 526348, 789514, 789506, 789504, 657920, 394752, 197377, 65795, 6, 10, 12, 12, 65804, 197388, 460556, 789516, 789516, 789516, 789516),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/icy-16.png
   :height: 2em

.. code-block:: python

    icy = (
        (255, 460799, 3026687, 9145343, 16777133, 16776973, 12632064, 4868624, 1052746, 192, 131839, 1710847, 6382079, 15329791, 16777215, 16777215),
        (179, 263347, 2105523, 6382003, 11776889, 11776777, 8816128, 3355403, 723763, 134, 65971, 1184435, 4474035, 10724275, 11776947, 11776947),
        (128, 197504, 1513344, 4539776, 8421462, 8421382, 6316032, 2434312, 526373, 96, 65920, 855424, 3158144, 7632000, 8421504, 8421504),
        (76, 131660, 855372, 2697548, 5000244, 5000195, 3750144, 1447429, 328982, 57, 76, 460620, 1908044, 4605516, 5000268, 5000268),
        (25, 25, 263193, 855321, 1644817, 1644801, 1250048, 460545, 65799, 19, 25, 131609, 592153, 1513241, 1644825, 1644825),
        (12, 12, 131596, 394764, 789512, 789504, 592128, 197376, 3, 9, 12, 65804, 263180, 723724, 789516, 789516),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/icy-10.png
   :height: 2em

.. code-block:: python

    icy = (
        (255, 1842431, 12237567, 16776973, 6908167, 460649, 131839, 4408319, 16777215, 16777215),
        (179, 1250227, 8553139, 11776777, 4868613, 329034, 65971, 3092403, 11776947, 11776947),
        (128, 921216, 6118784, 8421382, 3421187, 197428, 65920, 2171264, 8421504, 8421504),
        (76, 526412, 3618636, 5000195, 2039554, 131615, 76, 1315916, 5000268, 5000268),
        (25, 131609, 1184281, 1644801, 657920, 10, 25, 394777, 1644825, 1644825),
        (12, 65804, 592140, 789504, 328960, 5, 12, 197388, 789516, 789516),
    )


Gray
----
Shades of Gray. 

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/gray-24.png
   :height: 2em

.. code-block:: python

    gray = (
        (16777215, 12303291, 8618883, 5723991, 3552822, 1973790, 921102, 328965, 65793, 0, 0, 197379, 657930, 1513239, 2829099, 4802889, 7368816, 10724259, 14869218, 16777215, 16777215, 16777215, 16777215, 16777215),
        (11776947, 8618883, 6052956, 4013373, 2500134, 1381653, 657930, 197379, 0, 0, 0, 131586, 460551, 1052688, 1973790, 3355443, 5131854, 7500402, 10395294, 11776947, 11776947, 11776947, 11776947, 11776947),
        (8421504, 6118749, 4276545, 2829099, 1776411, 986895, 460551, 131586, 0, 0, 0, 65793, 328965, 723723, 1381653, 2368548, 3684408, 5329233, 7434609, 8421504, 8421504, 8421504, 8421504, 8421504),
        (5000268, 3684408, 2565927, 1710618, 1052688, 592137, 263172, 65793, 0, 0, 0, 0, 197379, 394758, 855309, 1381653, 2171169, 3223857, 4473924, 5000268, 5000268, 5000268, 5000268, 5000268),
        (1644825, 1184274, 855309, 526344, 328965, 197379, 65793, 0, 0, 0, 0, 0, 65793, 131586, 263172, 460551, 723723, 1052688, 1447446, 1644825, 1644825, 1644825, 1644825, 1644825),
        (789516, 592137, 394758, 263172, 131586, 65793, 0, 0, 0, 0, 0, 0, 0, 65793, 131586, 197379, 328965, 526344, 723723, 789516, 789516, 789516, 789516, 789516),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/gray-16.png
   :height: 2em

.. code-block:: python

    gray = (
        (16777215, 10263708, 5592405, 2500134, 855309, 131586, 0, 131586, 855309, 2500134, 5592405, 10263708, 16777215, 16777215, 16777215, 16777215),
        (11776947, 7171437, 3881787, 1776411, 592137, 65793, 0, 65793, 592137, 1776411, 3881787, 7171437, 11776947, 11776947, 11776947, 11776947),
        (8421504, 5131854, 2763306, 1250067, 394758, 65793, 0, 65793, 394758, 1250067, 2763306, 5131854, 8421504, 8421504, 8421504, 8421504),
        (5000268, 3026478, 1644825, 723723, 197379, 0, 0, 0, 197379, 723723, 1644825, 3026478, 5000268, 5000268, 5000268, 5000268),
        (1644825, 986895, 526344, 197379, 65793, 0, 0, 0, 65793, 197379, 526344, 986895, 1644825, 1644825, 1644825, 1644825),
        (789516, 460551, 263172, 65793, 0, 0, 0, 0, 0, 65793, 263172, 460551, 789516, 789516, 789516, 789516),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/gray-10.png
   :height: 2em

.. code-block:: python

    gray = (
        (16777215, 6908265, 1842204, 131586, 0, 1250067, 5592405, 14408667, 16777215, 16777215),
        (11776947, 4868682, 1250067, 65793, 0, 855309, 3881787, 10066329, 11776947, 11776947),
        (8421504, 3421236, 921102, 65793, 0, 592137, 2763306, 7171437, 8421504, 8421504),
        (5000268, 2039583, 526344, 0, 0, 328965, 1644825, 4276545, 5000268, 5000268),
        (1644825, 657930, 131586, 0, 0, 65793, 526344, 1381653, 1644825, 1644825),
        (789516, 328965, 65793, 0, 0, 0, 263172, 657930, 789516, 789516),
    )

White To Off
------------
A descending gradient from full white, down to black (off). Nice for a gentle transition from "on" to "off". 100% white, fades to black. On RGBW neopixels, the white pixel will typically be used.

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/white_to_off-24.png
   :height: 2em

.. code-block:: python

    white_to_off = (
        (16777215, 13158600, 10000536, 7434609, 5263440, 3552822, 2236962, 1315860, 657930, 263172, 65793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (11776947, 9211020, 6974058, 5197647, 3684408, 2500134, 1579032, 921102, 460551, 131586, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (8421504, 6579300, 5000268, 3684408, 2631720, 1776411, 1118481, 657930, 328965, 131586, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (5000268, 3947580, 2960685, 2171169, 1579032, 1052688, 657930, 394758, 197379, 65793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (1644825, 1315860, 986895, 723723, 526344, 328965, 197379, 131586, 65793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (789516, 657930, 460551, 328965, 263172, 131586, 65793, 65793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/white_to_off-16.png
   :height: 2em

.. code-block:: python

    white_to_off = (
        (16777215, 11382189, 7237230, 4210752, 2105376, 855309, 197379, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (11776947, 7960953, 5066061, 2960685, 1447446, 592137, 131586, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (8421504, 5658198, 3618615, 2105376, 1052688, 394758, 65793, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (5000268, 3421236, 2171169, 1250067, 592137, 197379, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (1644825, 1118481, 723723, 394758, 197379, 65793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (789516, 526344, 328965, 197379, 65793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/white_to_off-10.png
   :height: 2em

.. code-block:: python

    white_to_off = (
        (16777215, 8487297, 3421236, 855309, 0, 0, 0, 0, 0, 0),
        (11776947, 5921370, 2368548, 592137, 0, 0, 0, 0, 0, 0),
        (8421504, 4210752, 1710618, 394758, 0, 0, 0, 0, 0, 0),
        (5000268, 2500134, 986895, 197379, 0, 0, 0, 0, 0, 0),
        (1644825, 789516, 328965, 65793, 0, 0, 0, 0, 0, 0),
        (789516, 394758, 131586, 0, 0, 0, 0, 0, 0, 0),
    )


Green To Off
------------
A descending gradient from full green, down to black (off) Nice for a gentle transition from "on" to "off". 100% green, fades to black.

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/green_to_off-24.png
   :height: 2em

.. code-block:: python

    green_to_off = (
        (65280, 51200, 38912, 28928, 20480, 13824, 8704, 5120, 2560, 1024, 256, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (45824, 35840, 27136, 20224, 14336, 9728, 6144, 3584, 1792, 512, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (32768, 25600, 19456, 14336, 10240, 6912, 4352, 2560, 1280, 512, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (19456, 15360, 11520, 8448, 6144, 4096, 2560, 1536, 768, 256, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (6400, 5120, 3840, 2816, 2048, 1280, 768, 512, 256, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (3072, 2560, 1792, 1280, 1024, 512, 256, 256, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/green_to_off-16.png
   :height: 2em

.. code-block:: python

    green_to_off = (
        (65280, 44288, 28160, 16384, 8192, 3328, 768, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (45824, 30976, 19712, 11520, 5632, 2304, 512, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (32768, 22016, 14080, 8192, 4096, 1536, 256, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (19456, 13312, 8448, 4864, 2304, 768, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (6400, 4352, 2816, 1536, 768, 256, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (3072, 2048, 1280, 768, 256, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/green_to_off-10.png
   :height: 2em

.. code-block:: python

    green_to_off = (
        (65280, 33024, 13312, 3328, 0, 0, 0, 0, 0, 0),
        (45824, 23040, 9216, 2304, 0, 0, 0, 0, 0, 0),
        (32768, 16384, 6656, 1536, 0, 0, 0, 0, 0, 0),
        (19456, 9728, 3840, 768, 0, 0, 0, 0, 0, 0),
        (6400, 3072, 1280, 256, 0, 0, 0, 0, 0, 0),
        (3072, 1536, 512, 0, 0, 0, 0, 0, 0, 0),
    )


Red To Off
------------
A descending gradient from full red, down to black (off) Nice for a gentle transition from "on" to "off". 100% red, fades to black

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/red_to_off-24.png
   :height: 2em

.. code-block:: python

    red_to_off = (
        (16711680, 13107200, 9961472, 7405568, 5242880, 3538944, 2228224, 1310720, 655360, 262144, 65536, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (11730944, 9175040, 6946816, 5177344, 3670016, 2490368, 1572864, 917504, 458752, 131072, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (8388608, 6553600, 4980736, 3670016, 2621440, 1769472, 1114112, 655360, 327680, 131072, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (4980736, 3932160, 2949120, 2162688, 1572864, 1048576, 655360, 393216, 196608, 65536, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (1638400, 1310720, 983040, 720896, 524288, 327680, 196608, 131072, 65536, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (786432, 655360, 458752, 327680, 262144, 131072, 65536, 65536, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/red_to_off-16.png
   :height: 2em

.. code-block:: python

    red_to_off = (
        (16711680, 11337728, 7208960, 4194304, 2097152, 851968, 196608, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (11730944, 7929856, 5046272, 2949120, 1441792, 589824, 131072, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (8388608, 5636096, 3604480, 2097152, 1048576, 393216, 65536, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (4980736, 3407872, 2162688, 1245184, 589824, 196608, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (1638400, 1114112, 720896, 393216, 196608, 65536, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (786432, 524288, 327680, 196608, 65536, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/red_to_off-10.png
   :height: 2em

.. code-block:: python

    red_to_off = (
        (16711680, 8454144, 3407872, 851968, 0, 0, 0, 0, 0, 0),
        (11730944, 5898240, 2359296, 589824, 0, 0, 0, 0, 0, 0),
        (8388608, 4194304, 1703936, 393216, 0, 0, 0, 0, 0, 0),
        (4980736, 2490368, 983040, 196608, 0, 0, 0, 0, 0, 0),
        (1638400, 786432, 327680, 65536, 0, 0, 0, 0, 0, 0),
        (786432, 393216, 131072, 0, 0, 0, 0, 0, 0, 0),
    )


Blue To Off
------------
A descending gradient from full blue, down to black (off) Nice for a gentle transition from "on" to "off". 100% blue, fades to black

24 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/blue_to_off-24.png
   :height: 2em

.. code-block:: python

    blue_to_off = (
        (255, 200, 152, 113, 80, 54, 34, 20, 10, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (179, 140, 106, 79, 56, 38, 24, 14, 7, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (128, 100, 76, 56, 40, 27, 17, 10, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (76, 60, 45, 33, 24, 16, 10, 6, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (25, 20, 15, 11, 8, 5, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (12, 10, 7, 5, 4, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    )

16 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/blue_to_off-16.png
   :height: 2em

.. code-block:: python

    blue_to_off = (
        (255, 173, 110, 64, 32, 13, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (179, 121, 77, 45, 22, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (128, 86, 55, 32, 16, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (76, 52, 33, 19, 9, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (25, 17, 11, 6, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (12, 8, 5, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    )

10 Steps
~~~~~~~~
.. image:: {static}/images/time-based-fading/blue_to_off-10.png
   :height: 2em

.. code-block:: python

    blue_to_off = (
        (255, 129, 52, 13, 0, 0, 0, 0, 0, 0),
        (179, 90, 36, 9, 0, 0, 0, 0, 0, 0),
        (128, 64, 26, 6, 0, 0, 0, 0, 0, 0),
        (76, 38, 15, 3, 0, 0, 0, 0, 0, 0),
        (25, 12, 5, 1, 0, 0, 0, 0, 0, 0),
        (12, 6, 2, 0, 0, 0, 0, 0, 0, 0),
    )