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

.. PELICAN_END_SUMMARY

Expectation Management
======================

| People are lusty, excitable creatures. We are prone to fantastical elaborations and tend to see the world through rose-colored glasses.

Well, that's a bit extreme, but illustrative of the point - one of the best things we can do, and this is especially important working in tech, is learn how to *manage expectations*. 

This has two primary applications, one is outward facing, the other, inward. 

When you boil things down to core interactions, tech is ultimately a service industry. There's always a customer, a stake holder. There's always someone asking us to do what we do, relying on us to perform. It might be a coworker, a colleague in another department, a user, etc.

Our customers' expectations often don't reconcile with the realities of our work. If you don't experience this yourself, you'll hear the stories.

To best align expectations with reality, the thing to do is *communicate*. Some general tips:

* Break down problems into manageable pieces - discuss the components with your customers.
* Establish a minimum viable product, and commit to that first.
* Sell people on the idea of quick iterations.
* Don't be afraid to say "no". 

Personal expectations are an entirely different matter. The tech industry holds an immense potential. We have resources at our disposal to do anything, and what we lack, we can build. This is why this work is so enticing. It doesn't hurt that our income potential is high as well.  

It's easy to delude ourselves into thinking this work isn't really *work*. It's especially easy if we're coming from other industries where creativity is less important. From the outside, we see people making obscene amounts of money to sit around and type. They have free food, great benefits. They can work from home! They set their own hours! Look at that ping-pong table, it must be so much *fun* to be a programmer!

What you miss, looking from the outside, is *why* we have these things. Tech work can be extremely demanding, and the market is very competitive. So companies do what they can to attract and retain talent. And often that means giving them things to do to make their day-to-day less arduous. 

Because this work, regardless of your position, can be *extremely* arduous. The hardest work in tech isn't (usually) physically taxing. The hardest work in tech is (usually) *mentally* and *emotionally* taxing. Few, if any, bootcamps and training programs prepare you for just how bad it can be. 

So when I see companies touting their in-office showers, game rooms, free-flowing beer and catered food - I see the reality. A company is providing an *escape* from the job. Working from home allows people the ability to basically work *all the time*. "Unlimited" time off can easily become *no* time off. 

This is what I mean about keeping personal expectations managed. It's important not to delude yourself. It *will* get difficult, and when it does, it's helpful to be firmly rooted in reality. 

Perspective is gained by looking at things the right way.


Learn Testing, Profiling And Debugging
======================================
| This can not be stressed enough: **you have to know how to know what's wrong**.

It sounds a bit funny, but what I'm talking about is *profiling*, *debugging* and *testing*. 

Profiling is a way of analyzing code as it executes to determine the most resource intensive parts.  

Debuggers allow you to peek into the execution of your code, so you can see what's going on. You can pause execution and look at the state of variables and follow the execution stack. 

Testing gives you piece of mind. Well written test suites provide confidence: as long as the tests are passing, you can make radical changes to the code without worry. They also make you think critically about how your APIs are built - a good rule of thumb is that if code is hard to test, it's probably written poorly. Testing teaches better isolation of code units, better encapsulation, and better API construction.

The combination of automated tests and using the debugger gives you great insight. You won't have to guess why code doesn't do what you think it should. This makes asking for help more productive, if you can't isolate the issue on your own - once you peel back the veneer of frameworks and libraries, you can really get to understand how they work - and see where they fail. 

Profiling provides definitive answers to performance questions. It's essential for scaling. You will most certainly run into many performance issues in your career. Having the skills you need to assess what's actually going on are requisite for solving these sorts of issues.

So, if you haven't dug into the profiling, testing and debugging tools for your chosen language and application stack, do this as soon as you can. In fact, stop reading this post and *go look them up right now*. 

If I were putting together a programming curriculum, I'd make testing and debugging the first thing my students would learn after basic syntax. Profiling would come later (once we have some complex, possibly poorly optimized code to work with), but would still be taught early.

Learn The Scientific Method
===========================

| Being methodical is key to writing good software.

You don't have to be a scientist to write programs. But when making technical decisions it's best to take a scientific approach. This is especially true when there's ambiguity, or you're isolating bugs. 

There's nuance to the process, and much has been written about it, but here's a brief summary of the steps:

#. Question - what is wrong?
#. Hypothesis - why do you *think* it might be wrong? 
#. Prediction - what are some possible solutions that will satisfy the hypothesis?
#. Testing - construct experimental processes that will test the hypothesis, and verify the predictions.
#. Analysis - what does it all mean?

This reiterates the previous recommendation for learning profilers, debuggers, and writing tests. Good tests and profilers are your experimental methodology. Debuggers help with ensuring the methodology is sound.

Some related tips:

* Reproduce your results on multiple platforms.
* Reduce variability by isolating units. When testing a hypothesis, make sure you are dealing with as *little* code as possible.
* Limit the variables. 
* When appropriate, make sure you are adding enough data and load to make the experimentation realistic.

Mentor Every Day
================

| The best way to really learn something is to teach it to someone else.

Learn By Documenting
--------------------
* Write tutorials after you learn something new.

Help People
-----------
* Keep an eye out for other devs struggling, and be helpful. Especially junior devs and new hires.
* Participate in support for your platform, your company, your applications.
* Monitor the communication channels (IRC, mailing lists, chat rooms, github issues), and watch for people having problems - and do whatever you can to help them.

Learn A New Language
====================
| There's a lot to be gained by going through the process of learning a new language, besides adding a new skill to your resume. 

Languages have many commonalities, but where they diverge is where you can find some serious insight into computer science. It really can make you a more thoughtful programmer, more of a real, literal, *software engineer*. 

Further, you'll start to better learn *how to learn* languages, and it will make it easier for you to change things up in your career. It happens a lot more than you might think, given the way that job postings seem to be obsessed with specific technologies. Often you'll run into legacy systems written in "classic" languages, have to integrate with code from external entities, or business needs will change and you'll find yourself having to work outside of your primary language. There's also the ebb and flow of what's popular - job opportunities are constantly shifting from one technology to the next.  Knowing how to change direction quickly is a huge asset to your career. It can keep you employed when there's a sea change at your place of employment, and it can find you work between jobs.

Take a look at what kind of language(s) you already know, and seek out languages that represent other paradigms, or have different workflows.

For example, if you're primary language is interpreted, look into something compiled. If you usually use something procedural, look into event driven or functional languages. 

My primary experience is with Python (procedural and interpreted), but I found that learning Clojure (functional and compiled) really made me an overall better programmer. I'm currently learning Haskell - it's a departure from both, since it's strongly typed and compiled to machine code (as opposed to JVM bytecode).

There's a great book called `"Seven Languages In Seven Weeks" <https://pragprog.com/book/btlang/seven-languages-in-seven-weeks>`__ by Bruce A. Tate that is a great starting point if you have trouble identifying languages to try on your own. 

Work For Free - With Conditions
===============================
| A great way to establish yourself and gain real-life experience is to do volunteer work. But don't let people take advantage of you. 

Look for community organizations, home owner's associations, churches, charities, animal rescues, user groups, etc. Start with groups you are an active member of, or have an interest in. It's a great way to give back.

.. tip::
    
    This doesn't always mean working for free - non-profits are often hard pressed to find good people to help them achieve their development goals due to budget restraints, and they're willing to pay, just maybe not as much as you could make elsewhere.
    

But when you are going to work for free, be sure to clearly outline what you are agreeing to do before you commit. There's something odd about free work - in spite of the fact that your "customer" knows your time is valuable, there's a tendency to ask for too much, take up an unreasonable amount of time, or micromanage. So it's imperative that you set realistic expectations, establish attainable time lines and set clear goals.

One tact I take is borrowed from Duff Goldman, the "Ace Of Cakes". He's a baker and cake decorator from Baltimore, MD, often credited with launching the modern cake decorating era. In his reality show, he tells his friends that he will make and decorate cakes for them at no cost. However, there's a catch: *Duff's friend is not allowed to have any input on what Duff makes.*

This concept is a stroke of genius for several reasons. 

First, it's a rare opportunity for Duff to have total creative freedom. He can experiment, push the envelope, and see his vision come to life without outside interference. 

Second, it sets a very clear boundary. The customer understands without ambiguity that they need to stay out of the creative process.

Next, there's no chance of a monetary dispute between friends. 

Finally, Duff has a chance to do something really special, since the cake is technically a gift. 

This approach is great for tech projects for all the same reasons. And especially with tech projects, establishing this sort of arrangement will deter most people who might try to take advantage of your good will. There's something about giving up control that turns off people who will tend to waste your time.

Know How Servers And Virtualization Work
========================================

| Deploying, running, and scaling your application is not someone else's problem. Even when it is.

* Your app is more than just your code
* You will need to be able to harden and secure your work
* Sometimes optimizations need to happen in the OS layer
* How to get started
* You need to know when to say "this isn't my code's fault"


Never Stop Having Fun
=====================

| When this work stops being fun, you need to adjust your perspective.

To really make it in this industry, you have to **enjoy** what you do. That doesn't mean you have to live and breathe programming, it doesn't mean you have to be all smiles and nerdgasms and "go-team". 

I'm talking about true, simple joy. 

It comes from unexpected places. A sense of accomplishment, connecting with a user, feeling like your a part of something, sure. But also having an epiphany at 2AM that solves a problem you spackled over because of time constraints 3 years ago. It comes from looking at a piece of tech and not being able to stop smiling because you know how it works, or it's just plain *beautiful*. It's finding colleagues that really seem to *get* you. It's being twitter friends with the gal that invented that thing everyone uses, or that guy that made the thing everybody in your industry uses but nobody's heard of outside.

It's your first cup of coffee in the morning. It's walking out of a meeting feeling like you really accomplished something.

That's all really about perspective, and not so much about *fun*. The thing is, you shouldn't take this work too seriously. Even when we build applications that actually do affect life and death, if we stop having fun, the quality of our code suffers. 

If the joy leaves, if programming doesn't "do it" for you anymore, you have to seriously look at your life and make changes. They may have to be drastic. 

If you happen to find yourself in a soul-crushing job that just can't make you happy, and you can't leave it, have fun in other ways. Take up a hobby, especially one that lets you flex your technological muscles. 

Build an app that solves some stupid problem in your life. It doesn't have to make money, it doesn't have to be elegant or refined, just let it all go and *code stuff*.




