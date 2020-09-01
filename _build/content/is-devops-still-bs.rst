Is DevOps Still Bullshit?
#########################
:date: 2018-09-17 15:07
:author: jjmojojjmojo
:category: opinion
:tags: culture, devops, updates, engineering
:slug: is-devops-still-bullshit
:status: draft

.. include:: ../emojis.rst

A few years ago, I wrote a blog post that got a lot of attention, called "DevOps Is Bullshit: Why One Programmer Doesn't Do It Anymore". In this post, I reflect on the response to my previous post, on the years since, and on the current state of so-called DevOps. 

.. PELICAN_END_SUMMARY

The Original Post
=================
On March 8th, 2015 I published a my most popular blog post. It was on the front page of Hacker News. It peaked at about 50,000 views. It sparked a lot of discussion, and I learned why people are always complaining about the tone of Reddit users.

Since time has passed and my situation has changed, I feel like I can give a little more background on what was going on back then. There were circumstances that prompted the composition of this "classic" piece.

Lets go back to 2011. I took a job at a company where I was given the option to choose between four different teams. 

Fun fact about me: I'm from the mid-west (Iowa to be precise). There's something about some folks from that part of the US that makes us just bad at careers. Hard working, dedicated, but not not very career-minded. 

I'm not sure what it is exactly, but for people like me ambition is often difficult to muster. We see jobs as long-term investments in service, not stepping stones on a path to what we really want out of life.

.. image:: {static}/images/is-devops-still-bs/you-gotta-do-what-you-gotta-do.jpg
   :width: 80%
   :align: center

I wouldn't generalize but I've seen it in my relatives and extended family. It could be genetic, I don't know. 

Anyway, my midwesternness caused me to be so thrilled to feel wanted that I played it cool and said "hey, you put me wherever you think I'll do the best work". This is how I ended up on the so-called DevOps team. 

It wasn't a bad decision on my employer's part. Even though I've always been a programmer first, I have a knack for systems. At the job I was leaving, I had single-handedly built (with inspiration from a good friend and colleague) my own virtualization cluster with hot failover, what you might call a "private cloud". For years prior, I was always building my own servers. I always got along well with sysadmins and infrastructure folks. I shouldn't have been surprised, but I was. I remained cautiously optimistic, but I was ready for a new challenge and went into my new DevOps Engineer role with my standard (often excessive) enthusiasm.

However, I got disappointed pretty quickly. There was a deep cultural and political divide at the company between the Engineering and Infrastructure Departments. At this company, Engineering encompassed all of the programmers. Infrastructure included the systems engineers and database admins as well as desktop support and office infrastructure. 

We didn't have any of our own infrastructure. Everything had to be set up for us by the other department. Our deadlines and priorities were completely different, and often at odds.

As "the DevOps team", at best we should have been the bridge between the two groups, but since we were beholden to the Engineering group, we were hamstrung and hindered a lot.

But that was only part of the problem. We had a basic issue with semantics. I've come to realize that "DevOps" can be interpreted in different ways. The movement defines it essentially as "Developers (Doing) Operations (Too)", but I think this particular company saw it more as "Operations (for) Developers", in the sense of "operations activities that directly help developers". 

This was evidenced early on by the tasks we were given. We were in charge of transitioning the legacy code base from SVN to git. We were handed the JIRA installation. We were asked to set up code review processes, branching strategies, and continuous integration. We set up monitors that showed the build status. We were told "red is dead".

This was all patently wrong. *We* had nothing at stake, since we didn't touch the actual code base, or even interact with the actual infrastructure. All of the things we did should have been lead by the developers with full support of the operations team, but we were just the people making the changes, separate from the rest of the group. It's a bit awkward when you're dictating branching strategies and insisting on adequate test coverage when you have no authority over, or even camaraderie with, the engineers who are supposed to comply. 

Red was not dead. Nothing stopped when the tests failed. This was partially because the tests didn't work from the beginning. We were building continuous integration infrastructure for a group of developers who had no edict to update their broken tests. Seriously. 

The release cycle was fixed, so even the idea of stopping everything when the tests failed was a pipe dream. We scrambled to set up all of this infrastructure, drive all of this better culture on a short timeline that was beholden to, but not directly affected by, the developers we were supposed to be helping.

It seemed that management decided that if we just pushed hard enough, if the DevOps team just lead by example, everyone would just jump on the DevOps bandwagon and we'd become a modern, super-awesome highly efficient engineering culture. Their heart was in the right place, but you can't build such things without servers to deploy it to.  

I had just wasted my time, yet again, with a recruiter from a large company that shall not be named (let's just say having worked there would look good on my resume). I was pretty happy where I was working at the time, but I noticed that I was sliding into becoming the "devops guy". 

I had come off of a failed attempt at moving to New York City to work on a systems team playing "devops", and a brief and frustrating week trying to help a consultancy bring their practices into the modern era (two stories for another time, preferably under the influence).

I failed embracing the devops. I failed trying to fix culture. At this point, I just wanted to program, and if I had to scale a system or build a server, fine, but I didn't want that to be *my job*.

.. image:: {static}/images/is-devops-still-bs/what-is-my-purpose.jpg
   :width: 80%
   :align: center
   
That unnamed recruiter wasted my time *hard*. They were trying harder to sell me on their position and company than they were trying to see if I was a good fit. I felt like I was being sold a bill of goods so the recruiter could keep me on the hook long enough to pad their numbers. They were nice, and I caught some of their enthusiasm for what they were offering, but it just wasn't what I was looking for.

I know recruiters hate it when you try to take them off book, but after wasting an hour talking with them on the phone, I proposed a test.

I sent a link to the Johnson Pyramid Of Programmer Greatness, and asked the recruiter to show it to the hiring manager. If they still wanted to talk to me, I'd be interested in moving forward. I figured if they saw something that represented my approach to my work and liked it, it was a good sign. If they didn't, we could stop wasting time. The recruiter agreed to this, so I left the interaction with a pretty optimistic feeling about it.

The next week, the recruiter and I reconnected, and I politely waited for them to relay the reaction. It never happened. Another hour lost, and pressure to "move on to the next step". If you've been through the gauntlet of a technical interview, especially at certain high-recognition companies, you know what that meant: at least a day out of work for more screens, and then if I did well, another day (at least) of on-site interviews. The risk was just too high. I had a job, a good job that payed well and had great benefits. 

The reality was that I knew I wasn't what they were looking for. I had a chance with trying to connect to the hiring manager. But I knew what this position required, and I knew I didn't have those qualifications. This recruiter was not doing their job.

I was sick of being jerked around - DevOps was in high demand, so I was being targeted for jobs I wasn't really qualified for. This wasn't the first time, either. The recruiter was just using me, but I couldn't blame them. They have their own job to do, quotas to meet; it's not easy. But as much as I'm sympathetic to the realities of their job, I need to be protective of my work, my career, my free time. I was mad. What was wrong with me? What was wrong with this industry? Where did I take the wrong turns?

I looked back over my career and remembered how many times I'd turn to a coworker after a bad collab with a dev, or a counterproductive edict from managers who were more political than practical, and they'd say, half-jokingly, "DevOps is bullshit."

That got me thinking, and that weekend I sat down and expressed my exasperation.

The Response
============

