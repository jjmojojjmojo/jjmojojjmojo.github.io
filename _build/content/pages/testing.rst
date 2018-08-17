Testing!
########
:date: 2018-06-11 15:07
:author: lionfacelemonface
:category: testing
:tags: testing
:slug: testing
:status: draft

.. include:: ../../emojis.rst

This page exists for testing the style and post-processing of the site outside of actual content.

.. PELICAN_END_SUMMARY

Emojis
======
I've experimented with using various emojis in my text. Here's what they look like:

|grin| - general smile

|heartbreak| - broken heart

|thinking| - thinking face

|winking| - winking face

|rainbow| - rainbow

|unicorn| - unicorn

|crying| - crying face

|mouse| - mouse face

|trademark| - trademark - should be right up against text |trademark|.

|sparkleheart| - sparkling heart

Admonitions
===========

.. warning::
   This is a warning. 
   
.. tip::
   This is a helpful tip.
   
.. note::
   This is a note.
   
   
Code/Explanation
================
.. code-block:: python
    
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
   
   This explains the above code. 
   
   .. note::
      This is a note inside of the explanation.
      
   .. tip::
      This is a tip inside of the explanation.
      
   .. warning::
      This is a warning inside of the explanation.

Images
======
These images should be responsive. We can link to the original PNG version, and a bunch of responsive variants will be made, and the HTML will be replaced with the proper responsive image HTML. The image should also link to a full-sized version.

Images in a container
---------------------
.. container:: centered
   
   .. image:: {filename}/images/circuitplayground-express-closeup-neopixel-marked.png
      :width: 20%
      
   .. image:: {filename}/images/itsybitsy-m0-express-closeup-dotstar-marked.png
      :width: 20%
      
   .. image:: {filename}/images/trinket-m0-closeup-dotstar-marked.png
      :width: 20%
      
   .. image:: {filename}/images/gemma-m0-closeup-dotstar-marked.png
      :width: 20%
   
Images on their own
-------------------
.. image:: {filename}/images/aligator-clips.png
   :width: 80%
   :align: center
   
.. image:: {filename}/images/nonblocking-lengths-of-wire.png
   :width: 50%
   :align: center
   
Figures
-------

.. figure:: {filename}/images/basic-button-event-logic.png
   :figwidth: 80%
   
   This is the caption for this figure.
    
   
Line Blocks
===========

| this is a line block

| this is a multiple line line block
| isn't it *nice?*
| so cool
| |unicorn|

Nested Line Block
-----------------

| Line one is here.
|    line two is nested.
|    Line three is too.
| Line four is not.
| Line five is blah.