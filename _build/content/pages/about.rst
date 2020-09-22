About This Site
###############
:slug: about
:tags: about
:status: published

.. include:: ../../emojis.rst

Everything you ever wanted to know about this website *and more*.

.. PELICAN_END_SUMMARY

What Are All These *WORDS*?
===========================

This website is a creative outlet of **Josh Johnson**: writer, programmer, technology enthusiast... and |unicorn| *iconoclast* |unicorn|? 

This site contains articles, tutorials and light-hearted philosophical ramblings. It's generally geared toward other tech enthusiasts, but Josh tries to write for everyone. The tone is generally light, but *thorough*. Brevity is not Josh's strongest suit. Subjects typically revolve around technology, but may veer into other territories. 

If you have comments about, suggestions for, problems with, or just deep personal feelings about this site, please `contact Josh <{filename}/pages/contact.rst>`__.

.. note::
    
    Josh is not super comfortable writing in the third person. This makes him feel a bit odd. He's going to stop it now.
    

About The Author
================
.. figure:: {static}/images/about/josh-johnson-artists-rendering.png
   :align: right
   :figwidth: 20%
   :width: 100%
   
   Josh Johnson in 2018. Artist's rendering.

My name is Josh Johnson. I've been involved in tech professionally since 1999, and had my fair share of dabbling prior to that.



I have extensive experience with programming (Python, PHP, Perl, Javascript, Clojure), particularly web programming, systems automation, systems engineering, development and deployment pipelines (aka DevOps) and general technology. 

I really enjoy programming. I am a big fan of functional paradigms, but embraced OOP very early on in my journey, so it's second nature. 

I'm big on aesthetics. My style tends to be minimalistic, but I like colors and patterns. When it comes to my work, I know how to make things look nice. I am comfortable with creative tools. I'm well versed with commercial and open-source tools (I know most of the Adobe suite well, can do great things with MS Office, but I also know The Gimp, Inkscape, and LibreOffice).

I don't believe anything is beyond my understanding. If I want to do something *it happens*. If I don't have a skill, *I will develop it*. I'm an autodidact, so I've been doing this my entire life. I've built my career on technologies that I had to learn, often on the fly, on a deadline. But where I differ from a lot of my self-taught colleagues is that I can't live with just a superficial understanding. I have an innate need to dig deeper, to know more. More is never enough.

I conduct myself in a methodical fashion. I work deliberately. I like organization. I've studied many development methodologies like SCRUM, and have really embraced the idea of planning *just enough* to be able to build working software. 

When I'm not doing tech stuff, I love nature and art and all sorts of soft squishy things. |sparkleheart| I'm very tactile. I also enjoy music; my tastes are varied, sometimes esoteric, but vast - there's probably some artist we both like. 

I like to *make* things. I have a few recipes I know well. I craft, I paint, I assist my wife in her art photography. I build things with microcontrollers. 

Overall I just really enjoy the things I do. Otherwise, I wouldn't bother. |thinking|.

About The Site
==============
Philosophy
----------
This site's goals include:

* Providing high-quality content.
* Making content useful to as many people as possible. This means the site should be responsive, as light-weight as possible, and accessible.
* Looking good without detracting from the first two goals.
* Serving a wide audience while being as cost-effective as possible.

I really want the site to go against the grain of typical blogs. I want to find the "holy grail" of having a widely popular site that doesn't have to resort to intrusive ads, sponsored content, or any other revenue streams that tend to bum users out. 

I also don't want you to have to log in to read something, or break your browser.

Further, I don't want my content to be beholden to some company. I want to be able to deploy it freely so I can change hosts at will as I need to scale. 

This is a creative outlet for me, so I don't mind paying to keep it up - it's just tough when I see content becoming less and less useful as the userbase of a site goes up and up. And content producers make less and less money! I think its possible to be popular, maintain a high level of usability, and not have to constantly be strapped for cash.

So to start, this site, at its core, will always be strictly static. I've worked with many CMS systems over the years (`Plone <https://plone.org/>`__ is still my favorite), and find them all useless for a blog like mine.

The content is maintained as lightweight markup that is processed into static HTML for deployment (more about this below). This is the fundamental aspect of the site that will allow all of the goals to be achieved. Starting with lightweight markup means the code can live in a git repo, which keeps it autonomous. I can host my git repo on github (as I do currently), or I can host it in my own infrastructure. 

Because it's all static, I don't require any scripting runtimes or platforms for my site to function - I can host it literally anywhere, and even in multiple places. Free hosting, paid hosting, self hosting in S3, or all of the above with a load balancer attached to my domain name, even multiple domain names - *it doesn't matter because it's static*.

That relieves a huge cost, compared to hosting a dynamic blog. Using lightweight markup means I can change the look and feel easily, and have that consistency in the way the content is presented, much like a CMS. It's the best of all worlds.

Features
--------
This site has a few user features that are designed to enhance the overall utility of the site. 

First, I've added "explanation" sections liberally throughout the site. They look like this:

.. explanation::
    
    This part explains some stuff.
    
The book icon |OPEN_BOOK_ICON| is clickable - if you click it, the explanation is hidden. You can click the |CLOSED_BOOK_ICON| icon to open it back up.

The state of each explanation is stored in your browser, if its supported. You can control the data stored, as well as close or open all explanations on the `settings page </pages/settings.html>`__. You can get there quickly on any page in the site by clicking the gear icon in the right side of the header.

.. |CLOSED_BOOK_ICON| image:: {static}/images/book.svg
   :align: middle

.. |OPEN_BOOK_ICON| image:: {static}/images/book-open.svg
   :align: middle
   
Code samples are syntax-highlighted for easier readability. They are rendered using my favorite terminal font, `Inconsolata <http://levien.com/type/myfonts/inconsolata.html>`__. Here's an example of some random code:

.. code-block:: python
    
    def some_function(arg1, arg2, **kwargs):
        print(arg1)
        print(arg2)
        for key in kwargs:
            print("%s: %s" % (key, kwargs[key]))
            
    
If you would like to use different colors for the highlighting, you can also change the style sheet over in the `settings page </pages/settings.html>`__. 

.. tip::
    
    Please `let me know <{filename}/pages/contact.rst>`__ if you have any trouble with the code examples, especially with regards to the font choice or syntax highlighting. I'm happy to add options to change fonts and additional style sheets to accomodate your needs.

Technology
----------
This site is built using the `Pelican <ahttp://docs.getpelican.com/en/latest/>`__ site generator. The pages are mostly written in `RestructuredText <http://docutils.sourceforge.net/rst.html>`__.

All scripts and plugins were written in `Python <https://www.python.org/>`__.

The little bit of front-end functionality was written using `Jquery <https://jquery.com/>`__. 

You can see the source code on `github <https://github.com/jjmojojjmojo/jjmojojjmojo.github.io>`__. Pull requests with bug fixes or corrections are welcome!

.. note::
    
    I hope to write a detailed blog post about how this site works behind the scenes, stay tuned!
    
Copyright, License, Etc
=======================
Copyright
---------
All contents are |copyright| 2020 Josh Johnson. All rights are reserved.

I keep a listing of content from 3rd parties on `my media sources page <{filename}/pages/image-sources.rst>`__.


License
-------
Again, all rights are reserved.

License to the content of this site (code, media, text, and so on) is granted for personal, private use. You can view the code, download it, run it, be inspired by it, but you cannot use it in commercial products and you cannot use it in educational materials.

Please do not redistribute it, use it for teaching purposes, or any commercial purposes without asking for permission. You can `reach out to me <{filename}/pages/contact.rst>`__ to obtain permission. I promise it won't be hard. |sparkleheart|

Linking to this content is permitted (and encouraged), just don't be sneaky about it.

Warranty
--------
All code and information is provided *as is*, without warranty. You are using it at your own risk. So be careful!

Want To Use Content For Something?
==================================
If you are interested in using the content provided in this website for any purpose, please `contact Josh Johnson <{filename}/pages/contact.rst>`__. I'm very open to licensing my content or working with you to create new content for your purposes. 

I have a preference toward licensing content for open-source organizations and folks doing public good. If you fall under that heading, I encourage you to reach out.
