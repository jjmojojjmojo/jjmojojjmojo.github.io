Application Of State: A CircuitPlayground Express Sound Meter
#############################################################
:date: 2019-03-26 13:15:00
:author: jjmojojjmojo
:category: tutorial
:tags: python; circuitplayground express; circuitpython
:slug: cpx-sound-meter
:status: draft

.. include:: ../emojis.rst

In this tutorial, we'll build a *sound meter* using the never-boring `Circuit Playground Express <https://www.adafruit.com/product/3333>`__. Building on the `example in the CircuitPlayground Express docs <https://learn.adafruit.com/adafruit-circuit-playground-express/playground-sound-meter>`__, we'll improve the overall performance in a few key ways, and use an event-driven approach based on state management.

.. PELICAN_END_SUMMARY

Author's Note
=============

.. tip:: 
    
    Feel free to skip this section! |unicorn|
    

In putting together `State And Events In CircuitPython <{filename}/pages/circuitpython-state.rst>`__ in 2018, I found myself in a bit of a quagmire. I initially wrote the series as one very, very long article early in the year, and as I broke things up, the scope of the series expanded quite a bit.

At the same time, "life stuff" got in the way, and I had to make some tough decisions about where I'd put my effort. As such, the series languished a bit. 

I did manage to synthesize what I had already written, along with what I had planned near-term into a presentation I gave to TriPython in December of 2018.

**TODO: link to finished HTML conversion of the presentation**

Overview
========

Our Inspiration
===============

Materials/Setup
===============

In contrast to previous posts this article is written directly for the CircuitPlayground Express. 

Because of this, the only materials you need to follow along are:

* A CircuitPlayground Express board.
* A micro-USB cable.
* A computer.

I'd highly suggest using the mu editor as well.

.. note::
    
    If you'd like to see walk-throughs of building equivalent circuits using a different board and separate components, please reach out to the author.
    

Update The Firmware
-------------------

This tutorial was written using CircuitPython ﻿4.0.2. You should always use the latest available firmware.

.. note::
    
    Please contact the author if you have any trouble with later versions of CircuitPython.
    
To update, follow the instructions at `Adafruit's CPX Page <https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-quickstart>`__.

Basics Of The Components We're Using
====================================

NeoPixels
---------

MEMs Micropohone
----------------

Theory
======

Proof Of Concept
================
Now that we're comfortable with the hardware and APIs involved, lets apply our theory to a quick prototypical project.

To keep things simple, lets 