State And Events In CircuitPython
#################################
:date: 2018-06-11 15:07
:author: jjmojojjmojo
:category: tutorial
:tags: tutorial; circuitpython; hardware; state;
:slug: circuitpython-state
:status: published

This page collects links to all of the pages in the "State And Events In CircuitPython" series.

* `Part 1: Setup <{filename}/circuitpython-state-1.rst>`__. 

  In the first installment, we discuss the platform we're using (both CircuitPython and the Adafruit M0/M4 boards that support it), and build a simple circuit for demonstration purposes. We'll also talk a bit about abstraction.
  
* `Part 2: Exploring State And Debouncing The World <{filename}/circuitpython-state-2.rst>`__. 

  In part two of the series, we really dig into what state actually is, using analogies from real life. We then look at how we might model real-life state using Python data structures.

  But first, we discuss a common problem that all budding electronics engineers have to deal with at some point: "noisy" buttons and how to make them "un-noisy", commonly referred to as "debouncing".

  We talk about fixing the problem in the worst, but maybe easiest way: by blocking. We also talk about why it's bad.
  
* `Part 3: State And Microcontrollers And Events (Oh My!) <{filename}/circuitpython-state-3.rst>`__.
  
  Part three shows us how to debounce buttons without blocking, and explores the concept of events.
  
  It uses the testing code from Part 1 as a subject, refactoring it to be non-blocking, and enhancing it to add a new feature.