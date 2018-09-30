Advice For New Programmers
##########################
:date: 2018-09-29 15:07
:author: jjmojojjmojo
:category: musings
:tags: advice, programming
:slug: advice-for-new-programmers
:status: published

.. include:: ../emojis.rst

I am a proud **autodidact**. That means I am *entirely* self taught. |thinking| |mortarboard| |heart| People like myself are not uncommon in the tech industry, but we have always been in the minority. Autodidacts represent *industry outsiders*, because we've diverged from the typical learning path: a degree at a four-year college. With the advent of "let's code" initiatives, coding boot camps, better programming curriculum at 2-year colleges, and easier self-lead study, the number and varieties of outsiders is growing every day. We need to stick together.

We are a constant stream of new programmers, often without any sort of support system to help us along after we complete our training. Getting into this industry can be scary. So, for my fellow outsiders, I've put together some thoughts that will help you thrive and excel. I've based this on on what helped me, and my personal observations over the years.

However, I've realized that the difficulty of getting established is real, even for people with a typical education. There's a sort of *innocence* that is impressed onto new graduates, and there aren't a lot of resources for them either. So college grads, this is for you too.

.. PELICAN_END_SUMMARY

Expectation Management
======================

| People are lusty, excitable creatures. We are prone to fantastical elaborations and tend to see the world through rose-colored glasses.

Well, that's a bit extreme, but illustrative of the point - one of the best things we can do, and this is especially important working in tech, is learn how to *manage expectations*. 

This has two primary applications, one is outward facing, the other, inward. 

When you boil things down to core interactions, tech is ultimately a service industry. There's always a customer, or some sort of stake holder. There's always someone asking us to do what we do, relying on us to perform. It might be a coworker, a colleague in another department, a user, etc.

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


Learn Testing, Profiling And Debugging
======================================
| This can not be stressed enough: **you have to know how to know what's wrong**.

It sounds a bit funny, but what I'm talking about is *profiling*, *debugging* and *testing*. 

**Profiling** is a way of analyzing code as it executes to determine the most resource intensive parts.  

**Debugging** involves finding errors and fixing them. Debuggers are specialized tools that allow you to peek into the execution of your code, so you can see what's going on. You can pause execution and look at the state of variables and follow the execution stack. 

**Testing** gives you piece of mind. Well written test suites provide confidence: as long as the tests are passing, you can make radical changes to the code without worry. They also make you think critically about how your APIs are built - a good rule of thumb is that if code is hard to test, it's probably written poorly. Testing teaches better isolation of code units, better encapsulation, and better API construction. Tests can be manual or automated. Automated tests are absolutely *critical* when working on large, fast-moving codebases with lots of different developers.

The combination of automated tests and using the debugger gives you incredible insight into your application. You won't have to guess why code doesn't do what you think it should. This makes asking for help more productive, if you can't isolate the issue on your own - once you peel back the veneer of frameworks and libraries, you can really get to understand how they work - and see where they fail. 

Profiling provides definitive answers to performance questions. It's essential for scaling. You will most certainly run into many performance issues in your career. Having the skills you need to assess what's actually going on are requisite for solving these sorts of issues.

So, if you haven't dug into the profiling, testing and debugging tools for your chosen language and application stack, do this as soon as you can. In fact, stop reading this post and *go look them up right now*. 

If I were putting together a programming curriculum, I'd make testing and debugging the first thing my students would learn after basic syntax. Profiling would come later (once we have some complex, possibly poorly optimized code to work with), but would still be taught early. This is essential stuff that is often left out.

Learn The Scientific Method
===========================

| A methodical approach is key to writing good software.

You don't have to be a scientist to write programs. But when making technical decisions it's best to take a scientific approach. This is especially true when there's ambiguity, or you're isolating bugs. 

There's nuance to the process, and much has been written about it, but here's a brief summary of the `scientific method <https://en.wikipedia.org/wiki/Scientific_method>`__:

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
* Sometimes it's a good idea to build a contrived "toy" implementation to test, instead of trying to pull apart an existing application.

Mentor Every Day
================

| The best way to really learn something is to teach it to someone else.

Mentorship is a great way to maintain personal connections with fellow techies and "pay forward" the help you may have gotten from teachers, coworkers and friends.

As your career advances, it becomes an essential function of your job, even if you aren't interested in getting into management.

Here are a couple of ideas that I've leaned that have helped me be a better mentor.

Learn By Documenting
--------------------
Documentation is a hard practice for some programmers to get into. We get hyper-focused on code and functionality and we forget that sometimes the code isn't as obvious (or, *self-documenting*) as we might think.

So the first thing you can do to get a mentoring mind-set is **write documentation for your code**. Pretend that you are a new programmer and think about what you'd need to know to add a new feature or run the tests. It doesn't have to be a full-fledged technical manual, but the more detail you can get into the better. Just remember that your audience is probably as skilled as you are, so you don't have to explain basic concepts about the language or platform.

As you get better at it, the process will expose blind spots in your knowledge or implementation. There might be an edge case that will only come to mind when you are writing the docs. You may expose design, UI or API issues: if something is hard to talk about, there's a good chance its not well engineered.

Another thing that I've found really helpful, especially when I'm learning some new tech or concept, is to **write tutorials**. After I've gotten my head wrapped around the subject, maybe built a few things with it, I'll sit down and write a tutorial that walks someone who's new through what I learned, and publish it on my blog. 

It's a great way to help with that mentor mind-set, generate original content, fill in gaps in available knowledge on a subject, and contribute back to open-source projects. If you find you have a real knack for it, you can also find interesting career opportunities in technical writing, training or developer evangelism.

But for me, the biggest benefit I've found is that writing a tutorial forces me to **think about the subject in the abstract**. I have to strip down the complexities of the problem I'm trying to solve with it, so I can explain it to someone else. It really helps solidify what I've learned.


Help People
-----------
A great way to learn and practice mentoring skills is to get involved with helping other developers. It also builds your network and reputation.

Some tips on how to be a good helper:

* Be **paitent**, especially when others are too busy to really sit down and explain something to someone.
* Never forget how hard it was when you were learning. **Be empathetic** toward people who need your help.
* **Think about how to ask a good question**. It will help you get the most out of your interactions. There's a `classic document <http://www.catb.org/esr/faqs/smart-questions.html>`__ that has a lot of great discussion to get you started.
* Remember that people with problems are still *people* and have feelings and lives outside of programming. But so do you, so **be firm, but kind**.
* Make sure you really understand the problem. **Ask questions**, draw the person out if they are having trouble asking.
* Sometimes, even if you can't help, *just listening* is enough to help someone out. **Be available to listen**. 
* **Get to know subject matter experts**. Understand what questions they get asked a lot, and offer to triage problems for them. 

Tips on how to find opportunities to help:

* Keep an eye out for other devs struggling at work, and offer to help. Especially look out for junior devs and new hires. Eventually people will start to come to you.
* Participate in support for your platform, your company, or your applications. Getting to see how different kinds of people struggle to use tech builds empathy and can open your eyes to better ways of building things.
* Get involved in user groups and meetups. Think creatively about which ones to join, there are groups beyond the typical language and problem-domain focused ones that might be a source of people to help.
* Monitor communication channels (IRC, mailing lists, chat rooms, github issues, stack overflow) for people who need help. *You* can learn a lot too.

Learn A New Language
====================
| There's a lot to be gained by going through the process of learning a new language, besides adding a new skill to your resume. 

Languages have many commonalities, but where they diverge is where you can find some serious insight into computer science. It really can make you a more thoughtful programmer, more of a real, literal, **software engineer**. 

Further, you'll start to better learn **how to learn** languages, and it will make it easier for you to change things up in your career. It happens a lot more than you might think, given the way that job postings seem to be obsessed with specific technologies. Often you'll run into legacy systems written in "classic" languages, have to integrate with code from external entities, or business needs will change and you'll find yourself having to work outside of your primary language. There's also the ebb and flow of what's popular: job opportunities are constantly shifting from one technology to the next. Knowing how to change direction quickly is a huge asset to your career. It can keep you employed when there's a sea change at your place of employment, and it can find you work between jobs.

Take a close look at what kind of language(s) you already know, and seek out languages that represent other paradigms, or have different workflows.

If your primary language is interpreted, look into something compiled. If you usually use something procedural, look into event driven or functional languages.

For example, my primary experience is with Python ("duck-typed", procedural and interpreted), but I found that learning Clojure (dynamically typed, functional and compiled, runs on the JVM) really made me an overall better programmer. I'm currently learning Haskell - it's a departure from both, since it's functional and compiled, but it's strongly typed and runs on the "native" hardware.

Choosing which languages or paradigms to learn can be hard. There's a book called `"Seven Languages In Seven Weeks" <https://pragprog.com/book/btlang/seven-languages-in-seven-weeks>`__ by Bruce A. Tate that is a great starting point if you have trouble identifying languages to try on your own. 

Work For Free - With Conditions
===============================
| A great way to establish yourself and gain real-life experience is to do volunteer work. But don't let people take advantage of you. 

Look for community organizations, home owner's associations, churches, charities, animal rescues, user groups, etc. that need a website, or some other programming work, and volunteer to take it on. Start with groups you are an active member of, or have an interest in. It's a great way to give back.

.. tip::
    
    This doesn't always mean working for free - non-profits are often hard pressed to find good people to help them achieve their development goals due to budget restraints, and they're willing to pay, just maybe not as much as you could make elsewhere.
    

When you are going to work for free, be sure to clearly outline what you are agreeing to do before you commit. There's something odd about free work - in spite of the fact that your "customer" knows your time is valuable, there's a tendency to ask for too much, take up an unreasonable amount of your time, or micromanage the process. So it's imperative that you set realistic expectations, establish attainable time lines and set clear goals.

One tact I take is borrowed from Duff Goldman, the "Ace Of Cakes". He's a baker and cake decorator from Baltimore, MD, often credited with launching the modern cake decorating era. In his reality show, he tells his friends that he will make and decorate cakes for them at no cost. However, there's a catch: *Duff's friend is not allowed to have any input on what Duff makes.*

This concept is a stroke of genius for several reasons. 

First, it's a rare opportunity for Duff to have total creative freedom. He can experiment, push the envelope, and see his vision come to life without outside interference. 

Second, it sets a very clear boundary. The customer understands without ambiguity that they need to stay out of the creative process.

Next, there's no chance of a monetary dispute between friends. 

Finally, Duff has a chance to do something really special for a friend, since the cake is technically a gift. 

This approach is great for tech projects for all the same reasons, especially for friends and family. You get to do something nice, have fun and do something intellectually interesting, without risk of straining a relationship or the whole thing turning into a chore. So I always take this approach when a cousin I forgot I had comes out of the woodwork asking me to fix their website |grin|.


.. tip::
    
    There's another benefit for tech projects: establishing this sort of arrangement will deter most people who might try to take advantage of your good will. There's something about giving up control that turns off people who will tend to waste your time. I hate to have to even think about this, but it's happened to me and plenty of people I know. It's just too easy to take advantage. We enjoy this work so much we'll do it for free, and certain types of folks just can't resist pushing boundaries and extracting as much as they can from someone's good will. 
    
    The "Duff Methodology" is a great way to avoid unhealthy relationships when working for free.
    


Know How Servers And Virtualization Work
========================================

| Deploying, running, and scaling your application is not someone else's problem. Even when it is.

If you are new to programming right now in 2018, you might have only ever run your applications in `Docker <https://www.docker.com/>`__ or deployed them to a service like `Heroku <https://www.heroku.com/>`__. These tools are great for basic functionality, but it will greatly benefit your career if you dig a bit deeper and learn how to build your own servers and run things on the cloud.

Here are some reasons why this is helpful:

* Your app is more than just your code - the infrastructure it runs on directly affects how it performs. Understanding the infrastructure helps you understand your app and make it better.
* There are lots of opportunities at places where they don't have dedicated systems engineers. Being able to build your own servers can open doors for you.
* When there are dedicated systems people, knowing how to do it yourself helps you communicate more effectively with them. Communicating with systems engineers can be the difference between shipping on time or failing to meet a commitment, so it's a big deal.
* You need to know when to say "this isn't my code's fault". Even if you can't fix an infrastructure problem because it's not your jurisdiction, it's critical to be able to identify and communicate solutions to the people who *can* fix it.
* You will need to be able to harden and secure your work. Relying on a service or tool to do it for you will never be completely adequate. In order to do this, you have to understand what's going on under the hood.
* Sometimes optimizations need to happen in the OS or platform layer. This is just a fact. There are some settings and libraries you have to adjust in the operating system, or the VM/container host. Knowing when this is happening is a huge benefit, and being able to fix it yourself is even better |unicorn|
* There's a whole tech movement (and lots of jobs) for so-called `DevOps <https://en.wikipedia.org/wiki/DevOps>`__. Being an adept programmer who can also work with servers opens up that realm to you.

To get started, try installing a virtualization platform like `VirtualBox <https://www.virtualbox.org/>`__. Find a `linux <https://en.wikipedia.org/wiki/List_of_Linux_distributions>`__ or `BSD <https://en.wikipedia.org/wiki/List_of_BSD_operating_systems>`__ distribution you like, and install it in a VM. 

Study some resources for using `the command line <https://www.davidbaumgold.com/tutorials/command-line/>`__, particularly the `Bash shell <https://www.tldp.org/LDP/Bash-Beginners-Guide/html/>`__. There are books you can get too (too many to recommend any in particular).

Then look at `configuration management <https://en.wikipedia.org/wiki/Configuration_management>`__ tools like `Ansible <https://www.ansible.com/>`__ or `Chef <https://www.chef.io/>`__. 

Read up on the `package manager <https://en.wikipedia.org/wiki/Package_manager>`__ for your chosen distribution. Install what you need to run your app. Deploy your app to your VM and make sure it works. 

Write an Ansible playbook or Chef recipe to automate the setup and deployment of your application to your VM. 

Find out how to write startup and shutdown scripts for your application, and make sure it starts up when you restart the VM. Figure out how you can read system logs, and schedule scripts to run at various times. 

This is just scratching the surface, but it will expose you to a lot of what it takes to run software in production, and set you up for deeper dives into systems engineering.

As you proceed, take note of concepts and terms that are new to you, or that you're not totally clear on. Later on, research them further. Find people who already know Linux or BSD really well and lean on them for help when you get stuck.

.. tip::
    
    There are user groups all over the world for both Linux and BSD. Here are some helpful lists!
    
    * `Linux User Groups <http://lugslist.com/>`__
    * `OpenBSD <https://www.openbsd.org/groups.html>`__
    * `NetBSD <https://www.netbsd.org/community/groups.html>`__ 
    * `FreeBSD <https://www.freebsd.org/usergroups.html>`__ 

Before you know it, you'll have some confidence and be able to get the most out of Docker and the cloud... and become best buds with the systems folks. |unicorn|

.. tip::
    
    If you're having trouble choosing a operating system to install, first look at what's being used at work, the cloud provider you use, or the Docker image you base your deployments on. It's a good idea to get comfortable with what you work with day-to-day.
    
    I'd recommend starting with a `Debian <https://www.debian.org/>`__ variant. `Ubuntu <https://www.ubuntu.com/>`__ is considered to be pretty friendly to newcomers. 
    
    I really like `Arch <https://www.archlinux.org/>`__, but I don't recommend it to newcomers. That is, unless they really want to learn the ins and outs of Linux. Arch starts you off with the absolute minimum you need to say you are running Linux. Nothing more. That can be really scary for people who are new to the OS. However, the Arch docs are *impeccable* - there has not been one thing I couldn't find out from their docs. In fact, I've used them a lot for other distributions too. If you try Arch, by the time you get to the point where you can run your application, you will have learned a whole lot about computers and Linux, and probably yourself. |heart|
    
    Another great way to get into systems things is to pick up a `Raspberry Pi <https://www.raspberrypi.org/>`__ (I'd suggest buying a kit that includes a case and power supply), use the default `Raspian Linux <https://www.raspberrypi.org/documentation/raspbian/>`__, and install your application on that. You can use Ansible or other configuration management tools to automate the process too.
    
    I like the Raspberry Pi because it has a really great community that is oriented toward absolute beginners. It's probably the most gentle way to get into Linux and messing with systems I can think of. And as a bonus, you can  dig into electronics and build `Internet-of-things <https://en.wikipedia.org/wiki/Internet_of_things>`__ projects!
    


Never Stop Having Fun
=====================

| When this work stops being fun, you need to adjust your perspective, or maybe just GTFO.

To really make it in this industry, you have to **enjoy** what you do. People say that about all work. Personally, I don't think it's universally true, *except in tech*.

Now, that doesn't mean you have to live and breathe programming. It doesn't mean you have to be all smiles and "nerdgasms" and "go-team", *while you're struggling to get some stupid project you hate finished at 11PM because sales are a bunch of jerks and your boss promised things he knew you couldn't deliver and you have this pain in your side that the doctor says is nothing but you're sure its something and your kids need braces and Slack is down and I don't know what to do...* |grin| 

I'm talking about true, simple joy. And finding it in out of the way places.

It can be simple, or quite complex. Things like a sense of accomplishment, connecting with a user, feeling like you're a part of something, sure. But also having an epiphany at 2AM that solves a problem you spackled over because of time constraints 3 years ago. 

It can come from looking at a piece of tech and not being able to stop smiling because you know how it works. Maybe you find it's just a *beautiful* engineering achievement. 

The joy can be in finding colleagues that really seem to *get* you. The work might suck but sometimes the people you work with make it worth it.

Maybe it's the smug feeling you get being twitter friends with the gal that invented "that thing" everyone uses, or having beers with that guy that made the thing everybody in your industry relies on but nobody at the family reunion has ever heard of.

It's the joy of your first cup of coffee in the morning. Eating the last donut. It's walking out of a meeting feeling like you really accomplished something. It's helping a coworker solve a problem. It's hearing a client really liked that feature you built. 

It could be the freedom you have to work from home. The walk from your office to the bathroom. Looking forward to the next office Mario Kart tournament. Being able to spend $300 on a custom mechanical keyboard, or being able to build one.

It's all about having the right perspective. You have to see the good in what we do, and be open when the good finds you.

If you happen to find yourself in a soul-crushing job that just can't make you happy, and you can't just leave it, change your perspective to find the fun in other ways. Take up a hobby, especially one that lets you flex your technological muscles. Buy a raspberry pi or an Arduino and make some LEDs flash. Get into 3d printing. Take up photography. 

`Take some time to help people <Help People_>`__. Give back to the community. Contribute to an open-source project.

Build an app that solves some stupid problem in your life. It doesn't have to make money, it doesn't have to be elegant or refined, just let it all go and *code stuff*.

The point is that this work isn't for everyone, and sometimes you have to just admit you made a mistake, and change direction. But maybe it's not so bad, maybe there's other things you can do to find that joy again. Don't give up!

But there is a time when you have to be honest with yourself. There's so much variation and opportunity in this field, that if you just can't find some way to have fun with it, you really should find another line of work. |heartbreak|

Interviewing: Work The Coding Challenges
========================================

| Sometimes you have to play the game to get by, even when you know its rigged.

Hiring managers have a tough job. It's often been the case in the past 30 years or so, but especially today: tech is an "employees' market". There are too many jobs and not enough applicants. 

In spite of this, managers and recruiters are inundated with applicants for any tech-related position that gets posted. They often report being overwhelmed, particularly with applicants who aren't qualified for the job.

And then there is the idea of the "meritocracy" - in tech, you get jobs and advance because you *have merit*. It doesn't happen because you have experience, or education, or other things that usually make a difference.

So we have tech managers, who are technical people, trying to apply logic and reason to filtering applicants. Some say it's in an effort to be fair, because they really believe in the meritocracy. For others, its a bit more dubious. 

.. tip::
   
   I could (and probably will some day) write about my feelings and experiences on this subject, but that's would be very long diversion from the topic at hand. You need to get your career going already, not sit here listening to me rant about hiring practices. |winking|
   

One of the most common methods for "fairly" filtering applicants is the so called "coding challenge". They're sometimes called "technical screens", or "coding tests", "assignments", "evaluations" or "assessments". But they all have the same function: make the applicant write some code, and if it's *meritorious* enough, they are allowed to proceed in the interview process. Otherwise, the process usually ends and both parties move on to other opportunities. 

In my opinion, from being an applicant and participating in the hiring process from the employer's side, this is a flawed system. However, it's something that is so prevalent in the industry that it's essential that you at the very least know what you're getting into. It's especially important when you don't have much practical experience to fall back on. 

How experienced new programmers are with these coding challenges depends entirely on how they got into programming. Some colleges and bootcamps spend time on interviewing, so you may have gotten some coaching. Chances are you probably didn't. Being an autodicact, I was totally blindsided the first time I saw one in the wild.

In any case, the process can feel absolutely *brutal*, especially at first. 

|rainbow| The best advice I can give is: **Don't get discouraged!** I can't say anyone *deserves* any particular job, but if you've finished a bootcamp, or built an app, or gotten a degree, *you have value to this industry*. You've accomplished something most people can't. **You are a programmer.** Don't let some arbitrary process throw you off your game. Keep at it, and you *will* find a job where you can get past the nonsense and **you will shine!** |sparkleheart|

There are as many different styles of tests and particular coding problems as there are companies and jobs. However it does tend to follow trends and you will notice patterns emerge when you're out interviewing.

The main thing to remember is that you typically won't see the challenge before it's administered. You have to be ready for anything. 

The challenges have two main styles: the "live coding" type, and the "take home" type. Live coding is often done over the phone, in a video chat, with screen sharing, a "shared editor" tool, or sometimes in person. Some companies use an online service, and you won't usually be talking to someone when taking the test. 

Live challenges tend to be very short, usually not longer than an hour. The subjects tend to be very specific problems, and often involve standard data types and/or algorithms. There is an expectation that you can just *do it*, perform on the spot.

Take home challenges are usually longer form and tend to be higher level, but not always. The main difference is that you can do them on your own time. Some have hard time limits, others do not. Time limits are typically measured in days, as opposed to minutes.

.. tip::
    
    Don't be afraid to ask for information about the challenges beforehand! Interviewers, recruiters, and HR people might not volunteer the information, but they will often tell you a lot if you just ask. 
    
    Get as much information as you can, but focus on asking about things like:
        
        * What language you are expected to use (most are pretty flexible, but sometimes you are limited to one language or a small number of options).
        * How much time you will have.
        * What kind of test it is (take-home, live coding, white board, etc).
        * The general problem domain.
        

I've seen really fun take-home projects. I've done live coding of interesting design questions where I get to solve a real-life problem in front of a room of peers (something like "If you were building Twitter, how would you design it?"). These are my favorites. |unicorn|

I've also been asked to solve some pretty complex equations, given "brain teasers", asked to decipher some cryptic word problems, remember multiple implementations of algorithms that are well-solved by smarter people than me, and write algorithms where you are at a disadvantage if you don't know the "trick". I'm not a fan of these. |heartbreak|

But even when things are especially challenging or frustrating, the biggest thing you can do is *keep going*. Quitting in the middle of the challenge is almost always the same as failing, but you will usually get points for trying, especially if you keep your cool.

Here's some things you can do to prepare:

* Understand `complexity theory <https://en.wikipedia.org/wiki/Computational_complexity_theory>`__.
* Read up on basic `data structures <https://www.geeksforgeeks.org/data-structures/>`__ and `algorithms <https://www.geeksforgeeks.org/fundamentals-of-algorithms/>`__. You may want to get a book that shows you how to implement them in your favorite language.
* `Brush up on college-level maths <https://www.edx.org/course/subject/math>`__. Geometry, algebra, calculus. Linear algebra, trigonometry.
* Understand `design patterns <https://en.wikipedia.org/wiki/Software_design_pattern>`__. I highly recommend the "Gang of Four" book, *Design Patterns: Elements of Reusable Object-Oriented Software*. There are other, simpler books, but this is the definitive reference. Try to find one in your preferred language.
* Do some puzzles and brain teasers to keep your mind limber (I'm really bad at these, so you'll have to find ones you like) |thinking|.
* Get an "interview questions" book. There are many of these, you will want to try a couple and see which one illustrates the concepts the best, and gives you the right kind of questions. Again, consider a book that has problems in your preferred language. 
* Read through some online repositories of interview questions. If you search for "interview questions" you will find many github repos and websites. It takes some time to sort through them, and they vary a lot in quality. It would be best to use these as a last resort. However they can be really useful if you are unable to obtain any books on the subject.

.. tip::
    
    Don't look at the "cracking the coding interview"-type book or lists of problems as giving you the answers (aka "cheating"). Everyone is aware of the existence of these resources, so there is little chance you will be given the exact problem you see in one of the books.
    
    Treat them as a resource for practice, and a trove of leads for new study subjects. 
    
    There's likely some areas of computer science or programming that you are weak in, or haven't studied yet. These questions will give you the keywords and concepts so you can really dig in and level up. |thinking|
    
But above all, **practice**. You can think of ways to do this off-line, like starting a study group, or having an experienced friend give you mock interviews.

But here's a list of online sites that will give you lots of challenges that are typical of what's being used. As a bonus, a lot of them act as training sites, and some are connected to hiring pipelines at major companies! It's a great way to get past HR departments or recruiters that might see your lack of experience or atypical background as a blocker.

* https://www.interviewbit.com/
* https://www.hackerrank.com/
* https://triplebyte.com/
* https://exercism.io/

.. note::
    
    I'm not affiliated or endorsing any of these sites. I suggest them because I've looked through them or used them myself, and at least on the surface they look really good. 
    
    Please `let me know <{filename}/pages/contact.rst>`__ if they turn out to be spammy, scammy, or are otherwise bad news. 
    
    **You should never have to pay for access to one of these sites, or to get interviews!**
    

Be sure to do some research about the company where you're interviewing, and pay attention to the job posting. You want to know what tools and problems they are solving. If it's not clear, ask the interviewer or recruiter before they give you the coding challenge. A lot of companies make coding challenges based on actual problems they've had to solve, so you can get a leg up if you start reading about algorithms and the like that are specific to that domain.

One last tip, and this is the hardest truth about this process. **You will have to make time to practice and work on these challenges**. It can be really hard when you have a family, other obligations in life, already have a job, or just have a lot going on. But if you don't practice, or rush through the take-home tests, you will miss opportunities that would otherwise be a great fit for you.

And as an new programmer, experience is so critical at this time in your career, you have to do whatever you can to get your foot in the door. 

People are reasonable, though! Be up front with recruiters and interviewers about areas where you lack expertise. They might give you a more appropriate challenge for your background.

Ask if you can do a take-home test instead of live coding or timed evaluations. It may not always be an option, but it doesn't hurt to ask. 

People want to hire you, as much as it may seem otherwise. They will work with you. And honestly, if they won't, it's probably a red flag. There's a good chance that if they wont show flexibility in interviewing, they won't show it when you're hired. And if you have family and other life obligations, that doesn't change when you get an offer.

So it's ok to be mindful of your time, and pass on some jobs. Remember you are in an employees' market, and you will find other opportunities.

Conculsion
==========
So here's what I would tell (and have told |grin| ) a new programmer. Please `let me know <{filename}/pages/contact.rst>`__ if you have any thing to add, or if I'm totally off base about something!

I hope to expand on this post over time, so your feedback is greatly appreciated |heart|.
