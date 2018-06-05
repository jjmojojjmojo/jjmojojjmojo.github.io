Advice For New Programmers
##########################
:date: 2018-06-15 15:07
:author: lionfacelemonface
:category: tutorial
:slug: advice-for-new-programmers
:status: draft

I am a proud autodidact. I am *entirely* self taught. People like myself are not uncommon in the tech industry, but we have always been in the minority. Autodidacts represent industry outsiders. We are outsiders in contrast to the usual path: a computer science degree at a 4-year university. With the advent of coding bootcamps, better programming curriculum at 2-year colleges, and self-lead study, the number of outsiders is growing. While autodidacts have unique problems, other outsiders share a lot of our struggle. 

Further, there is a constant stream of new programmers, often without any sort of support system to help them along after they complete their training. Getting into this industry can be scary. So, I've put together some thoughts on what can help you get a good foothold, and excel. I've based this on on what helped me, and my personal observations over the years.

As an aside, I've realized that the difficulty of getting established is real, even for traditionally trained folks. There's a sort of *innocence* that is impressed onto new graduates, and there aren't a lot of resources for them either. So this is for them too.

Expectation Management
======================

People are lusty, excitable creatures. We are prone to fantastical elaborations and tend to see the world through rose-colored glasses.

Well, that's a bit extreme, but illustrative of the point - one of the best things we can do, and this is especially important working in tech, is learn how to *manage expectations*. 

This has two primary applications, one is outward facing, the other, inward. 

When you boil things down to core interactions, tech is ultimately a service industry. There's always a customer, a stake holder. There's always someone asking us to do what we do, relying on us to perform. 

Our customers' expecations often don't reconcile with the realies of our work. If you don't experience this yourself, you'll hear the stories.

To best align expectations with reality, the best thing to do is communicate. Some general tips:

* Break down problems into managable pieces - discuss the components with your customers.
* Establish a minimum viable product, and commit to that first.
* Sell people on the idea of quick iterations.
* Don't be afraid to say "no". 

Personal expectations are an entirely different matter. The tech industry holds an immense potential. We have resources at our disposal to do anything, and what we lack, we can build. This is why this work is so enticing. It doesn't hurt that our income potential is high as well.  

It's easy to dilute ourselves into thinking this work isn't really *work*. It's especially easy if we're coming from other industries where creativity is less important. From the outside, we see people making obscene amounts of money to sit around and type. They have free food, great benefits. They can work from home! They set their own hours! Look at that ping-pong table, it must be so much *fun* to be a programmer!

What you miss, looking from the outside, is *why* we have these things. Tech work can be extremely demanding, and the market is very competitive. So companies do what they can to attract and retain talent. And often that means giving them things to do to make their day-to-day less arduous. 

Because this work, even at a low level, can be extremely arduous. The hardest work in tech isn't (usually) physically taxing. The hardest work is *mentally* and *emotionally* taxing. Few, if any, bootcamps and training programs prepare you for just how bad it can be. 

So when I see companies touting their in-office showers, game rooms, free-flowing beer and catered food - I see the reality. A company is providing an *escape* from the job. Working from home allows people the ability to basically work *all the time*. "Unlimited" time off can easily become *no* time off. 

This is what I mean about keeping personal expectations managed. It's important not to delude yourself. It *will* get difficult, and when it does, if you are dealing with the fact that you thought it wouldn't be, you will be less likely to adequately adapt.


Learn Testing, Profiling And Debugging
======================================
I can not stress this enough: *you have to know how to know what's wrong*.

It sounds a bit funny, but what I'm talking about is profiling, debugging and testing. 

Profiling is a way of analyzing code as it executes to determine the most resource intensive parts.  

Debuggers allow you to peek into the execution of your code, so you can see what's going on. You can pause execution and look at the state of variables and follow the execution stack. 

Testing gives you piece of mind. Well written test suites provide confidence: as long as the tests are passing, you can make radical changes to the code without worry. They also make you think critically about how your APIs are built - a good rule of thumb is that if code is hard to test, it's probably written poorly. Testing teaches better isolation of code units, better encapsulation, and better API construction.

The combination of automated tests and using the debugger gives you great insight. You won't have to guess why code doesn't do what you think it should. This makes asking for help more productive, if you can't isolate the issue on your own - once you peel back the vineer of frameworks and libraries, you can really get to understand how they work - and see where they fail. 

Profiling provides definitive answers to performance questions. It's essential for scaling. You will likely run into many performance issues in your career, and having good information about why helps you decide the best course of action.

So, if you haven't dug into the profiling, testing and debugging tools for your chosen language and application stack, do this as soon as you can. 

If I were putting together a programming curriculum, I'd make testing and debugging the first thing my students would learn after basic syntax. Profiling would come later (once we have some complex, possibly poorly optimized code to work with), but would be a key part as well.


Learn The Scientific Method
===========================
You don't have to be a scientist to write programs. But when making technical decisions, especially when things are ambiguous, or you are isolating bugs, it's best to take a scientific approach.

There's nuance and much has been written about it, but here's a brief summary of the process:

#. Question - what is wrong?
#. Hypothesis - why do you *think* it might be wrong? 
#. Prediction - what are some possible solutions that will satisfy the hypothesis?
#. Testing - construct experimental processes that will test the hypothesis, and verify the predictions.
#. Analysis - what does it all mean?

This reiterates the previous recommendation for learning profilers, debuggers, and writing tests. Good tests and profilers are your experimental methodology. Debuggers help with ensuring the methodology is sound.

Some related tips:

* Reproduce your results on multiple platforms to ensure they are sound.
* When appropriate, make sure you are adding enough data and load to make the experimentation realistic.
* Isolate variables. When testing a hypothesis, make sure you are dealing with as little code as possible.

Mentor Every Day
================

Work For Free - With Conditions
===============================

[The Duff]

Know How Servers And Virtualization Work
========================================
* Your app is more than just your code
* You will need to be able to harden and secure your work
* Sometimes optimizations need to happen in the OS layer
* How to get started
* You need to know when to say "this isn't my code's fault"