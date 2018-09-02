Boot: Getting Started With Clojure In < 10 Minutes
##################################################
:date: 2018-08-01 11:41
:author: jjmojojjmojo
:category: tutorials
:tags: boot, clojure
:slug: boot-getting-started-with-clojure-in-10-minutes
:status: published

With the power of `boot <http://boot-clj.com/>`__, it's possible to go from "never used java before" to budding `Clojure <http://clojure.org/>`__-ist cranking out jars like a pickle factory in record time. This post walks you through the process, and provides some post-'hello world' examples, with pointers to more information.

.. PELICAN_END_SUMMARY

Overview For The Unititated
===========================
For those who are absolute Clojure beginners, here are a few clarifying terms and concepts.

Clojure is a *functional programming language* in the style of Common Lisp. "Functional" in this sense means that functions are first-class objects; code and data are peers. Data is *immutable* - as values change, objects are replaced, not manipulated. Code structures and language features common to most other types of languages are not present. Instead, they are implemented as functions or are simply not necessary. 

Functional languages, especially in the Lisp-style are *expressive* and, linguistically speaking, *simple*. The original Lisp, invented in 1958 by John McCarthy at M.I.T., was expressed in seven functions and two special forms - the language, in total, contained just *nine elements*, and was fully Touring-complete. By comparison, the current version (3.5) of Python has 30+ keywords, plus special elements such as mathematical operators and colons - and that's merely the language itself, that doesn't include idioms or conventions.

What this adds up to is a vast reduction in "incidental complexity" - complexities that creep into code because of the limitations, or expectations, of our languages. Contrast incidental complexity with "essential complexity", or complexities that our code would not function without. Lisp-like languages stay out of your way.

In terms of Clojure, we are blessed with a very concise, easy to reason about syntax that gives us incredible flexibility. We are also provided with a robust standard library. 

Clojure was designed with concurrency in mind, from its inception. This makes advanced use of threads and multiple processes simple and quite accessible, not to mention *safe*. 

Clojure is a general language specification. It has been implemented for the Java Virtual Machine (JVM), JavaScript, and 
the Microsoft .Net Common Languge Runtime (CLR). There are platform-specific nuances, but the core language and library is the same - as you move from a Java environment  to a .Net one or onto front-end browser development, your Clojure skills will convey.

This tutorial focuses on using Clojure with the JVM. This requires the installation of a Java Development Kit (JDK). It's really the only hard prerequisite. 

Java applications are typically distributed as JAR files - simple Zipped archives of compiled source code. We will be using Boot to compile and package some example applications.

About Boot
----------

Boot is a relatively new build tool for Clojure. It succeeds where others have been found wanting. This is because it embodies core Clojure philosophies, in particular the aforementioned reduction in *incidental complexity*. 

If you have read some other Clojure tutorials or books, you will likely have been introduced to Leiningen. Leiningen is the defacto standard Clojure build tool. Its functionality overlaps with Boot's, but the approach is very different.

Leiningen provides some special conventions and a domain-specific language (DSL) to drive the build and development processes. Boot, on the other hand, is purely functional. With the exception of some isolation mechanisms implemented under the hood, Boot works just like any other Clojure library. Extending Boot is as simple as writing any other Clojure code. Leiningen requires that you implement some complex APIs to extend it.

My personal favorite feature of Boot, which I believe makes it not only a superior build tool, but an all-around killer utility even outside the build problem space, is *scripting*. Clojure is a compiled language, so the concept of Clojure scripts is not baked in. However, Boot, using the same conventions as you would use to manage a build process, gives us the ability to write scripts.

These scripts work just like shell scripts, with a few key exceptions:

- They are written entirely in Clojure.
- They can have dependencies on Clojure libraries that are resolved at runtime.

This means you can distribute Boot scripts in the same manner as Python or Bash scripts - except dependencies are handled automatically.

This concept is explored in the sister post to this one, `Boot: Getting Started With Clojure In 10 Minutes <{filename}boot-getting-started-with-clojure-in-10-minutes.rst>`__

Installation/Development Setup
------------------------------
The command-line examples assume a unix-like environment, and are to be run within a terminal. The bash shell was used. Examples have been tested on Ubuntu Linux and MacOs. 

However, the principals should be transferable to any Linux, BSD or similar operating system.

.. note::
   
   Clojure is supported in the Microsoft Windows operating system. The author hopes to expand this tutorial to cover Windows sometime in the future.

Clojure doesn't need to be installed, in the typical sense. Clojure is distributed as a JAR file, and so Boot is able to download it and use it as its standard operating procedure. 

Behind the scenes, `Maven <https://maven.apache.org/>`__ is used to manage JARs. The public maven repositories are utilized for Java dependencies, and `clojars <http://clojars.org/>`__ is used for clojure ones.

Conventions
-----------
See `Site-wide Conventions Explained <{filename}/pages/conventions.rst>`__.


Prerequisites
=============

You will need the following: 

- *A JDK installed*. 

Really, that's it. `Sun's JDK <http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html>`__ or `OpenJDK <http://openjdk.java.net/>`__ will work. Use the newest version. 

In addition, you'll need a way to download things. Feel free to use your browser. The examples below use `wget <https://www.gnu.org/software/wget/>`__. 

If you're on Linux or Mac OS, you'll also need root access via `sudo <http://www.sudo.ws/>`__ - this is not a hard requirement but allows you to install boot for everyone on your machine to use. 

There's an expectation that you know basic `Clojure <http://clojure.org/>`__, and examples try not to be too clever. For a good introduction, check out `Clojure For The Brave and True <http://www.braveclojure.com>`__, specifically `Do Things: a Clojure Crash Course <http://www.braveclojure.com/do-things/>`__. If you need help with specific forms used, the `Clojure Community Documentation <http://clojure.org/documentation>`__ is extremely helpful, especially the `Clojure Cheat Sheet <http://clojure.org/cheatsheet>`__. 

It may be helpful to give the `boot readme <https://github.com/boot-clj/boot>`__ and `wiki documentation <https://github.com/boot-clj/boot/wiki>`__ a read. 

.. tip::
   **For questions about boot or clojure,** `The Clojurians Slack <http://clojurians.net/>`__ **is the defacto place to go to converse with clojure rockstars and other newbs alike.**
   
   **If slack isn't your jam,** `IRC <http://en.wikipedia.org/wiki/Internet_Relay_Chat>`__ **is another great way to get in touch with clojure folks. Come join us on** `freenode <https://freenode.net/>`__, **in #hoplon.**
   

*¡Dales la Bota!* (Give 'em The *Boot*!) - *Installation*
=========================================================

`Boot <http://boot-clj.com/>`__ is '`installed <https://github.com/boot-clj/boot#install>`__' by simply downloading an `executable file <https://github.com/boot-clj/boot/releases>`__ and putting it somewhere where you can execute it. 

.. note::
   
   For more options, see `Appendix: Alternative Install Methods`_.
   

   
In our case, we'll use our home directory:
 
.. code-block:: console
    
    
    $ wget https://github.com/boot-clj/boot-bin/releases/download/latest/boot.sh
    $ mkdir -p ~/bin
    $ mv boot.sh boot && chmod a+x boot && mv boot ~/bin/
    

.. explanation::

   First we need to download the boot executable script. The .sh extension indicates it's a shell script.
   
   Then a directory is created with :code:`mkdir` for personal executables (binaries, hence :code:`bin`). We use the :code:`-p` flag to tell :code:`mkdir` that any intermediary directories should be created. :code:`-p` also silences any errors for already-existing directories. 
   
   The tilde :code:`~` is an alias for the current user's home directory. We use it here because the specific path for home is variable depending on both the user, and the operating system. For example, if my log in is jjmojojjmojo, on Linux, my home directory is likely :code:`/home/jjmojojjmojo`. But on some systems, it will be :code:`/var/users/jjmojojjmojo`. On MacOS, home directories are in :code:`/Users`. See `this wikipedia article <https://en.wikipedia.org/wiki/Home_directory>`__ for more information.
   
   Finally, we string a few commands together using :code:`&&`. :code:`&&` will execute the following command if the preceding one succeeds (has a 0 return value). Here's what each part does:
   
   #. We rename (move) the :code:`boot.sh` to :code:`boot`. This way we can type :code:`boot` instead of :code:`boot.sh` to execute boot commands later on.
   #. We change the *mode* of the :code:`boot` script to include *execute* for the group, owner, and other bits. This allows the script to be executed like any other command - and by anyone who can read it. Using this approach (as opposed to, say :code:`chmod 755`) only modifies the execute bit for each class. `More info <http://mason.gmu.edu/~montecin/UNIXpermiss.htm>`__. 
   #. Finally, we move the :code:`boot` script to our personal :code:`~/bin` directory, so the shell can find it when we set that up in the next step.
    
Then we need to update our :code:`$PATH` environment variable so the shell can find our new executable boot:
    
.. code-block:: console
   :linenos: none
   
   $ echo "export PATH=\$PATH:\$HOME/bin" >> ~/.bash_profile
   $ export PATH=$PATH:$HOME/bin
   

.. explanation::
   
   The shell looks for executables in a variable called :code:`$PATH`. :code:`$PATH` is a list of directories, that are searched in sequential order. 
   
   We can get the shell to find our :code:`boot` script by adding our personal bin directory to the end of that variable. `More info <https://en.wikipedia.org/wiki/PATH_(variable)>`__.
   
   By adding an :code:`export` command to the end of our :code:`~/.bash_profile`, we can ensure this modification to our shell happens every time we log in, or start our terminal app. Other environments, and shells have different files that are used this way.
   
   We accomplish this by using the :code:`echo` command. :code:`echo` sends data to the terminal output (stdout). We redirect that output to be appended to :code:`~/.bash_profile`, using two greater-than symbols (:code:`>>`). `More info <http://www.tldp.org/LDP/abs/html/io-redirection.html>`__.
   
   Note that we escape the dollar signs in the :code:`$PATH` and :code:`$HOME` variables. This prevents the shell from expanding the current value for those variables before adding the :code:`export` to :code:`~/.bash_profile`.
   
   Finally, we make the change take effect in our current shell by running the export (without the escaped dollar signs). 
   
   

   
.. note::
   
   Depending on your distribution, and shell, the way to make this change permanent may be different. Most shells read a special file in your home directory. Look for files like :code:`~/.bashrc`, :code:`~/.profile`, etc.  
   

The real magic happens when boot is run. Boot sets everything up in a ``.boot`` directory in your home folder. Without having any code to execute yet, you can trigger this by simply asking boot for help: 

.. code-block:: console
   :linenos: none
   
   $ boot -h
   Downloading https://github.com/boot-clj/boot/releases/download/2.7.2/boot.jar...
   Running for the first time, BOOT_VERSION not set: updating to latest.
   Retrieving clojure-1.8.0.pom from https://repo1.maven.org/maven2/ (8k)
   Retrieving oss-parent-7.pom from https://repo1.maven.org/maven2/ (5k)
   Retrieving maven-metadata.xml from https://repo.clojars.org/
   Retrieving boot-2.7.2.pom from https://repo.clojars.org/ (2k)
   Retrieving boot-2.7.2.jar from https://repo.clojars.org/ (3k)
   Retrieving clojure-1.8.0.jar from https://repo1.maven.org/maven2/ (3538k)
   #http://boot-clj.com
   #Wed May 09 20:19:27 EDT 2018
   BOOT_CLOJURE_NAME=org.clojure/clojure
   BOOT_VERSION=2.7.2
   BOOT_CLOJURE_VERSION=1.8.0
   

.. note::
   
   If you have previously installed boot, it's a good idea to run boot's self-update (:code:`boot -u`) before continuing:
   
   .. code-block:: console
      :linenos: none
      
      $ boot -u
      Retrieving boot-2.7.0.jar from https://clojars.org/repo/
      #http://boot-clj.com
      #Wed Dec 14 11:53:20 EST 2016
      BOOT_CLOJURE_NAME=org.clojure/clojure
      BOOT_CLOJURE_VERSION=1.7.0
      BOOT_VERSION=2.7.0
      


Let's Play With Clojure
-----------------------

The REPL
~~~~~~~~

Clojure utilizes a concept called a `REPL <http://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop>`__ (**R**\ ead, **E**\ valuate, **P**\ rint, **L**\ oop). REPLs allow you to interactively run code and experiment.

.. code-block:: console
    
    $ boot repl

.. tip::
   
   Boot's ``repl`` task downloads a bunch of dependencies. Don't be alarmed if a bunch of text scrolls by the first time you run ``boot repl``.
    
Boot then provides you with a prompt, where you can play around:

.. code-block:: clojure
   
   nREPL server started on port 62443 on host 127.0.0.1 - nrepl://127.0.0.1:62443
   REPL-y 0.3.7, nREPL 0.2.12
   Clojure 1.8.0
   Java HotSpot(TM) 64-Bit Server VM 1.8.0_92-b14
           Exit: Control+D or (exit) or (quit)
       Commands: (user/help)
           Docs: (doc function-name-here)
                 (find-doc "part-of-name-here")
   Find by Name: (find-name "part-of-name-here")
         Source: (source function-name-here)
        Javadoc: (javadoc java-object-or-class-here)
       Examples from clojuredocs.org: [clojuredocs or cdoc]
                 (user/clojuredocs name-here)
                 (user/clojuredocs "ns-here" "name-here")
   boot.user=> (+ 1 2 3 4 5)
   15
   boot.user=> (/ 10 0)
   
   java.lang.ArithmeticException: Divide by zero
   

.. explanation::
   
   The first few lines provide some basic information:
   
   * Line 1: `nREPL <https://github.com/clojure/tools.nrepl>`__ is a service that allows you to connect to a repl using a remote client.
   * Line 2: `REPL-y <https://github.com/trptcolin/reply>`__ is an alternative to the built-in REPL that has some nice features.
   * Line 3: We're using Clojure 1.8.
   * Line 4: This is the particular JVM in use. 
   
   Line's 5 through 14 are some helpful forms and functions you can use inside the REPL.
   
   The :code:`boot.user=>` prompt tells us that we are in a special `namespace <https://clojure.org/reference/namespaces>`__, set up for us by boot.
   
   On line 15, we're doing a simple addition of some integers. When you press enter after typing some code, the result is printed below.
   
   On line 17, we illustrate what happens when there is a java exception. If you'd like to see the full stacktrace, you can use the `pst <https://clojuredocs.org/clojure.repl/pst>`__ (*print stack trace*) form:
   
   .. code-block:: clojure
      
      boot.user=> (/ 10 0)
      
      java.lang.ArithmeticException: Divide by zero
      
      boot.user=> (pst)
       clojure.core/eval                          core.clj: 3105
               ...
      boot.user/eval1532  boot.user3203296763858150787.clj:    1
               ...
      java.lang.ArithmeticException: Divide by zero
      nil
      
   
   
A Simple Clojure Function
~~~~~~~~~~~~~~~~~~~~~~~~~

Here's a simple Clojure function that prints the `Fibonacci sequence <http://www.mathsisfun.com/numbers/fibonacci-sequence.html>`__ to a given number of digits:

.. code-block:: clojure
    
    (defn fib
      ([n]
        (fib [0 1] n))
      ([pair, n]
        (print (first pair) " ")
        (if (> n 1)
          (fib [(second pair) (apply + pair)] (- n 1))
          (println))))

.. explanation:: 
   
   This is a basic clojure function definition. It uses `multiple airties <http://clojure-doc.org/articles/language/functions.html#multi-arity-functions>`__. This is how you provide multiple different ways to call the same function. 
   
   Note how on line 2 and line 4 we specify two different argument lists. The first is for calling the function the typical way (providing the maximum number of levels), the second is used for recursion - the ``pair`` argument is a sequence containing the previous and current number in the sequence.
   
   * Line 1: The opening of the function definition.
   * Line 2: The first airty - one single argument named ``n``. The maximum number of levels.
   * Line 3: Recursion - if only one argument is passed, call ``fib`` again, but with 0 and 1 (the first numbers in the Fibonacci sequence) to get things started.
   * Line 4: The second airty - two argunments: ``pair`` a sequence containin two integers representing the previous and current numbers in the sequence, and ``n``, the maximum number of levels.
   * Line 5: print the previous number to `standard out <https://en.wikipedia.org/wiki/Standard_streams#Standard_output_(stdout)>`__. We're using the `print <https://clojuredocs.org/clojure.core/print>`__ function here to avoid adding a line break after the number so they'll all print to the console on the same line.
   * Line 6: the `if <https://clojuredocs.org/clojure.core/if>`__ form  is used to check if we've hit the maximum number of levels yet. We subtract one from ``n`` every iteration, so when it's equal to 1, it's time to stop.
   * Line 7: *True condition.* Recurse, this time passing a vector containing the current number, and the sum of the current and previous number. The second parameter is the maximum level minus one.
   * Line 8: *False condition.* The end of the requested sequence. Use the `println <https://clojuredocs.org/clojure.core/println>`__ function with no arguments to print a final line break.
   
   



You can paste this into your REPL and try it out:

.. code-block:: clojure
    
    boot.user=> (defn fib
       #_=>   ([n]
       #_=>     (fib [0 1] n))
       #_=>   ([pair, n]
       #_=>     (print (first pair) " ")
       #_=>     (if (> n 1)
       #_=>       (fib [(second pair) (apply + pair)] (- n 1))
       #_=>       (println))))
    #'boot.user/fib
    boot.user=> (fib 10)
    0 1 1 2 3 5 8 13 21 34 55
    nil
    boot.user=> exit
    Bye for now!

.. tip::
   
   You can copy the prompts along with the code, the REPL will ignore them.
   

Boot Scripts
~~~~~~~~~~~~
   
Boot also works as a `scripting platform <https://github.com/boot-clj/boot/wiki/Scripts>`__ - you can construct applications, specifying dependencies, and parse command-line arguments. 

We can transform that function into a command-line tool using the power of boot scripting. Assume this file is called :code:`fib.boot`:

.. code-block:: clojure
    
    #!/usr/bin/env boot
    
    (defn fib
       ([n]
         (fib [0 1] n))
       ([pair, n]
         (print (str (first pair) " "))
         (if (> n 1)
           (fib [(second pair) (apply + pair)] (- n 1))
           (println))))
     
    (defn -main [& args]
       (let [limit (first args)]
         (println "Printing fibonacci sequence up to " limit "numbers")
         (fib (Integer/parseInt limit))))
     
.. explanation:: 
   
   The primary differences betweent a boot script and the bare boot function we wrote earlier:
   
   * A boot script is a shell script, and so it needs a line to indicate which interpreter is required to parse the contents. This is known as a `shebang <https://en.wikipedia.org/wiki/Shebang_(Unix)>`__ or 'hashbang' line. (Line 1.)
   
   * A boot script requires a ``-main`` function to be defined. This function is invoked by boot when the script is run. (Line 12.) 
   
   The shebang line has to be a 'full' path (not relative) to the executable. 
   
   In our shebang line, on line 1, we're using a (mostly) ubiquitous tool called ``env``, that looks for the given argument (``boot``) in the directories specified in the ``$PATH`` environment variable of the current user. This way, we don't have to hard code the location of the boot tool, since it can vary. 
   
   For example,  in this article we've installed boot in ``~/bin``. In my case that expands to ``/Users/jj/bin``, but in yours, it might be ``/home/joecool/bin`` or ``/var/home/bethrulz``. The location for home directories varies by operating system and more often than not, we will have different user names.  
   
   .. note::
      
      The ``~`` shortcut for ``$HOME`` is not expanded in shebang lines.
      
   
   Or, you may have installed boot globally into ``/usr/local/bin`` or any number of other possible system locations depending on a lot of factors. Using ``env`` is a handy way to remove that complexity. 
   
   Lines 3-10 are the same Fibonacci sequence we used before. 
   
   Line 12 provides an *entry point*, a function that boot will invoke when the script is run. The name ``-main`` is required by boot. The argument list uses the ``&`` special form to collect a variable number of arguments into a single sequence named ``args`` (a function that does this is called a `variadic function <http://clojure-doc.org/articles/language/functions.html#variadic-functions>`__). 
   
   Boot passes the function a variable number of strings . Each string is text that was provided by the user in the console while invoking the script (typically referred to 'command-line arguments' or 'command-line options'). 
   
   For example, if an imaginary command-line tool called ``boo`` is executed with "hello world, welcome to the thunder dome", like this:
   
   .. code-block:: console
      :linenos: none
      
      $ boo hello world, welcome to the thunder dome
      
   The content of ``args`` will be
   
   .. code-block:: clojure 
      :linenos: none
      
      ["hello" "world," "welcome" "to" "the" "thunder" "dome"]
      
   This is something the shell does. It can be avoided by surrounding the arguments with double quotes, like this:
   
   .. code-block:: console
      :linenos: none
      
      $ boo "hello world, welcome" "to the thunder dome"
      
   In this case, ``args`` is a vector containing two elements:
   
   .. code-block:: clojure 
      :linenos: none
      
      ["hello world, welcome" "to the thunder dome"]
      
   It's important to note that the shell can do other things with arguments that may be unexpected. The ins and outs of shells are outside the scope of this tutorial (and can vary from shell to shell), but here are a couple of common ones that might be useful or trip you up:
   
   * **Glob Expansion.** Shells help you out by replacing special patterns with matching filenames, so you can pass a bunch of paths to a command line tool without having to type them all out. `More info <https://en.wikipedia.org/wiki/Glob_(programming)>`__.
   * **Environment Variable Expansion.** Shells understand inline variables and will expand them before running your command line tool. Common useful environment variables include ``$HOME``, ``$PATH``, ``$SHELL``, and ``$PWD``.  
   * **Subshell Execution.** Shells can execute commands for you and pass the results on to your command line script.
   
   Because of these things, it's good to be conscious of which characters are used to make use of these special features, and how to escape them so you don't get unexpected arguments passed to your scripts. This will vary depending on your shell - `take a look at a chapter from a book on learning bash <https://www.safaribooksonline.com/library/view/learning-the-bash/1565923472/ch01s09.html>`__ to get an idea of what you need to look out for.
   
   On line 13, we extract the first member of ``args`` to pass as the maximum number of Fibonacci iterations. 
   
   Line 14 prints some informatio to the user to let them know what's going on.
   
   On line 15, the ``fib`` is finally executed, passing the limit provided by the user on the command line. 
   
   We need to convert the limit to an integer for use by our ``fib`` function. This is accomplished using the Java ``Integer.ParseInt()`` function. 
   
   It may seem odd that we invoke a Java function here, but this is common practice in Clojure, since we are usually running on the JVM. It's referred to as `Java interop <https://clojure.org/reference/java_interop>`__.

Next, we make the script executable:

.. code-block:: console
   :linenos: none
   
   $ chmod u+x fib.boot
   

.. explanation:: 
   
   We're again utilizing the ``chmod`` command to make a file executable. Here, we use the shorthand mode specification (see the man page `online <https://linux.die.net/man/1/chmod>`__ or you can type ``man chmod`` in your console for specifics), instead of using octal numbers (like ``755``). 
   
   ``u+x`` means "*add* whatever bits are necessary to allow the **u**\ser to e\ **x**\ ecute this file". This leaves any other bits untouched.
   

Now you can run the script:

.. code-block:: console
    
    
    $ ./fib.boot 10
    Printing fibonacci sequence up to 10 numbers
    0 1 1 2 3 5 8 13 21 34


Dependencies
~~~~~~~~~~~~
    
The script can declare dependencies, which will be downloaded as needed when the script is run. Here, we'll show the use of an external dependency: we can write a new Fibonacci sequence that exploits an the fact that numbers in the sequence are related to each other by approximately the `golden ratio <http://en.wikipedia.org/wiki/Golden_ratio>`__ (ca 1.62), as noted by Kepler, and derived from `Binets Formula <https://en.wikipedia.org/wiki/Fibonacci_number#Binet's_formula>`__. 

.. note::
   
   I'm not a maths scholar, so I may have the specifics and credit a bit wrong. The `Wikipedia page <https://en.wikipedia.org/wiki/Fibonacci_number#Relation_to_the_golden_ratio>`__ is a bit thin on specific references for the use of the golden ratio and rounding to calculate one Fibonacci number using another. 
   
   If you happen upon this and can shed some light on the subject, please `drop me a line <{filename}pages/contact.rst>`__!
   
   

Rounding makes it all work, but rounding isn't "baked in" to Clojure, so we'll use an external library to do it for us, called `math.numeric-tower <https://github.com/clojure/math.numeric-tower>`__. 

.. note::
    
    In actuality, the required functionality is present, you just need to use some `existing Java libraries <http://stackoverflow.com/a/25098576>`__ to make it work. I admit this is a bit of a strain, but it illustrates the use of external dependencies in boot.

.. code-block:: clojure
    
    #!/usr/bin/env boot
    
    (set-env! :dependencies '[[org.clojure/math.numeric-tower "0.0.4"]])
    
    (require '[clojure.math.numeric-tower :refer [round sqrt expt]])
    
    (def phi (/ (+ (sqrt 5) 1) 2))
    
    (defn fibgolden
       [n]
       (loop [counter 0]
         (if (= counter 0)
           (do 
             (print (str 0 " " 1 " " 1 " "))
             (recur 3))
         (let [f (round (/ (expt phi counter) (sqrt 5)))]
           (print (str f " "))
           (if (< counter (- n 1))
             (recur (+ counter 1)))))))
    
    (defn -main [& args]
       (let [cli-arg (first args)
             limit (if (empty? cli-arg) 10 (Integer/parseInt cli-arg))]
         (println "Printing Fibonacci sequence up to" limit "numbers")
         (fib limit)
         (println)))
                 
    
    

.. explanation::
   
   Line 3 illustrates how to add a dependency to a boot script. 
   
   Boot has the concept of an `environment <https://github.com/boot-clj/boot/wiki/Boot-Environment>`__. The environment represents the current working environment of the JVM during the execution of boot scripts or tasks.
   
   On Line 3 we manipulate the environment using the ``set-env!`` function. 
   
   Note that this function ends with an exclamation point (!), or *bang*. Data structures in Clojure are not normally *mutable* (they can't be changed, only transformed into new ones). But in some cases it's required. So clojurists have established a convention to suffix a function name with an exclamation point to indicate that the function mutates data, or otherwise has side effects. 
   
   The environment is represented as a mapping, and so we use symbols to access and change its members. The ``:dependencies`` key tells boot which libraries to look for. 
   
   Dependencies are first sourced from `clojars <https://clojars.org/>`__, then the `Maven central repository <https://maven.apache.org/repository/>`__. 
   
   The format for specifying dependencies is the same that `Leiningen <https://leiningen.org/>`__ uses - a vector containing a package specifier (often containing an organizational part, like ``org.clojure`` in our script), and a version. Clojars uses `semantic versioning <https://semver.org/>`__, so there are 3 numbers: a major revision (breaks existing APIs), a feature revision (API stays the same), and patch revision (for non-breaking bug fixes).
   
   Note that the list of dependencies is behind a `var quote <https://clojure.org/guides/weird_characters#__code_code_var_quote>`__. 
   
   On line 5, the library is brought into our namespace using `require <https://clojuredocs.org/clojure.core/require>`__. (For more information about namespaces and libraries, *Clojure For The Brave and True*'s `organization <https://www.braveclojure.com/organization/>`__ chapter goes into some great detail. We've used the ``:refer`` parameter to just import one function, ``round``.
   
   On line 7, we pre-calculate the golden ratio and define a variable named ``phi`` (the greek letter phi [φ] is used to represent the golden ratio in equations).
   
   Lines 9-19 define our new, golden ratio-based Fibonacci sequence function. It performs basically the same way, except that it's single-airity. 
   
   Some interesting concepts introduced in this new function:
   
   * This is not a recursive function in the usual sense. Instead, we use the ``loop`` function and ``recur`` macro. This is the way looping (like you'd use ``for`` or ``while`` in other languages) works in Clojure. For more details on how they work, check out `this ClojureBridge article <https://clojurebridge.github.io/community-docs/docs/clojure/recur/>`__. 
   
   * On line 11, we use ``do`` to group multiple expressions (printing and recursing) into a single branch of an ``if``. This comes in handy a lot, but be careful not to overuse it - if you are doing too much in a conditional branch, it may be better to factor that code out into its own function.
   
   * On line 14 and 17, we use ``str`` to concatenate our Fibonacci numbers and some spaces. Core Clojure doesn't have string "math" or interpolation features.
   
   On lines 22 and 23, we process the command line argument. Variables that are unpacked by ``let`` are processed in order, so we can refer to them right away. We take advantage of this to first extract the argument on line 22, then provide a sane default (10) in the event that the user didn't provide a value. We also go ahead and convert the argument to an integer using Java interop as we did in the previous version.
   
.. tip::
   
   We've added a sane default for the single command-line argument, but otherwise aren't doing any input validation. We'll address this in a shallow way in the next section, when we use Boot's `argument DSL <https://github.com/boot-clj/boot/wiki/Task-Options-DSL>`__, but it's always something to keep in mind. 
   
   As such, the current script doesn't handle:
   
      * Negative numbers (it stops after the initial iteration)
      
      * Large numbers - Java's ``Integer`` has a maximum size (the exact size varies by platform). After fairly few iterations it will hit this number and stop getting larger (it used to throw a stack trace for me, so YMMV). On the computer I'm using at the time of writing, I get repeating values if I pass anything larger than 94 to ``fib.boot``. 
      
      * Non-integers. If you pass a float (say, 2.45), or anything that ``Integer/parseInt`` can't work with, it will throw an exception. 
   
   

When you run this code the first time, you'll notice boot tells you that it has downloaded some new jars:

.. code-block:: console
    
    $ ./fib.boot 10
    Retrieving clojure-1.4.0.jar from http://clojars.org/repo/
    Retrieving math.numeric-tower-0.0.4.jar from http://repo1.maven.org/maven2/
    Printing fibonacci sequence up to 10 numbers
    0 1 1 2 3 5 8 13 21 34

The syntax to parse our command line options can be a bit tedious and we will often run into the same patterns over and over, like "flags" (true/false toggles like ``-n`` or ``--without-module-x``), collected values (like passing ``-vvv`` to increase verbosity), even complex subcommands (like ``git merge``). 

Luckily, we can borrow a macro from boot.core that lets us specify CLI options using a robust syntax. For the full syntax, check out `the documentation <https://github.com/boot-clj/boot/wiki/Task-Options-DSL>`__. 

Here, we'll let the user choose which implementation they'd like to use, and utilize the task `DSL <http://martinfowler.com/books/dsl.html>`__ to do some simple command line options:

.. code-block:: clojure
    
    #!/usr/bin/env boot
    
    (set-env! :dependencies '[[org.clojure/math.numeric-tower "0.0.4"]])
    
    (require '[clojure.math.numeric-tower :refer [expt round sqrt]])
    (require '[boot.cli :as cli])
    
    (def phi (/ (+ (sqrt 5) 1) 2))
    
    (defn fib
       ([n]
         (fib [0 1] n))
       ([pair, n]
          (print (str (first pair) " "))
          (if (> n 1)
            (fib [(second pair) (apply + pair)] (- n 1)))))
    
    (defn fibgolden
       [n]
       (loop [counter 0]
         (if (= counter 0)
           (do 
             (print (str 0 " " 1 " " 1 " "))
             (recur 3))
         (let [f (round (/ (expt phi counter) (sqrt 5)))]
           (print (str f " "))
           (if (< counter (- n 1))
             (recur (+ counter 1)))))))
    
    (cli/defclifn -main
       "Print a Fibonacci sequence to stdout using one of two algorithms."
       [g golden bool "Use the golden mean to calculate"
        n number NUMBER int "Quantity of numbers to generate. Defaults to 10"]
       (let [n (:number *opts* 10)
             note (if golden "[golden]" "[recursive]")]
         (println note "Printing Fibonacci sequence up to" n "numbers:")
         (if golden
           (fibgolden n)
           (fib n)))
         (println))         
    
    

.. explanation::
   
   This version of the script splices together what we've done in previous examples. We have the recursive ``fib`` function on lines 10-16, and the golden ratio-based function on lines 18-28. We've renamed the golden ration-based function to ``fibgolden``.
   
   On line 6, we require the boot command line utility ``boot.cli``. We pass the ``:as`` parameter to ``require`` in order to give the library a different name in our namespace. We do this just to keep things a bit more tidy (and illustrate this feature!).
   
   The ``-main`` function on line 30 is chiefly the same, except that we use the ``defclifn`` macro from ``boot.cli`` instead of the special ``defn`` form. 
   
   The string on line 31 will be used in the usage description when the user provides the ``-h`` command line argument.
   
   The major difference besides using the macro, is in the argument specification on lines 32 and 33. This is the "option DSL" that is discussed in `the documentation  <https://github.com/boot-clj/boot/wiki/Task-Options-DSL>`__. 
   
   The command line arguments are extracted and used to populate a special ``*opts*`` map that will be automatically in scope of your function.
   
   Line 32 defines a *boolean* command line argument, or a *flag*. If the argument is provided, the value will be ``true``, otherwise, it will be ``false``. We are using this argument to let the user change algorithms used to generate their requested Fibonacci sequence.
   
   The first value is the "short form" of the option, ``-g``. The second is the "long form" ``--golden`` and also the name of the argument in the ``*opts*`` map (without the dashes). Next we specify the type of the argument, ``bool``, short for *boolean*, or a true/false value. The ``defclifn`` macro will convert the string value from the command line arguments into a boolean. Finally, we provide a string that will be used to tell the user what sort of value we're expecting in the usage output.
   
   On the next line, we define another command-line option, this time one that takes a value. This is how the user will tell us how many numbers to generate.
   
   .. note::
      
      Due to how boot uses the CLI macro, it does not support *positional* arguments, like we used in our earlier scripts. 
      
      However another tool, like `tools.cli <https://github.com/clojure/tools.cli>`__ serves a similar purpose and has positional argument support, but is not as nice of an interface. 
      
   In this case, we use ``-n`` as the short form, ``--number`` as the name/long form, and ``int`` as the type. The next form is used as the placeholder when printing the usage information.
   
   The last differences of note are on line 34 and 35.
   
   On line 34, we set a default for the number of Fibonacci numbers to generate, by utilizing a special feature of symbols - you can use them as a function, passing a map as the first parameter. This looks up the value for that symbol in the mapping. You can pass a second parameter, which will be returned if the symbol isn't a key in the map - essentially a default value.
   
   Finally, line 35 sets a variable called ``note`` using the ``if`` form - if the user has passed ``-g`` and ``golden`` is true, then we'll print ``[golden]`` to indicate the golden ratio-based function is in use. Otherwise, we'll print ``[recursive]`` to indicate the standard recursive function is in use.
   


Now you can see what options are available, and tell the script what to do:

.. code-block:: console
   :linenos: none
   
   $ ./fib.boot -h
   Print a fibonacci sequence to stdout using one of two algorithms.
   
   Options:
    -h, --help Print this help info.
    -g, --golden Use the golden mean to calculate
    -n, --number NUMBER Set quantity of numbers to generate. Defaults to 10.
   
   $ ./fib.boot
    [recursive] Printing fibonacci sequence up to 10 numbers:
    0 1 1 2 3 5 8 13 21 34
   
   $ ./fib.boot -g -n 20
    [golden] Printing fibonacci sequence up to 20 numbers:
    0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 611 990 1604 2598 4209

Working At The Pickle Factory (Packing Java Jars and More Complex Projects)
---------------------------------------------------------------------------

Now that we've got a basic feel for Clojure and using boot, we can build a project, that creates a library with an entry point that we can use and distribute as a jar file. This opens the doors to being able to deploy web applications, build libraries to share, and distribute standalone application bundles. 

Project Structure
~~~~~~~~~~~~~~~~~

First, we need to create a project structure. This will help us keep things organized, and fit in with the way Clojure handles namespaces and files. We'll put our source code in ``src``, and create a new namespace, called ``fib.core``:

.. code-block:: console
    
    $ mkdir -p src/fib

In ``src/fib/core.clj``, we'll declare our new namespace:

.. code-block:: clojure
    
    (ns fib.core
       (:require [clojure.math.numeric-tower :refer [expt round sqrt]]
                 [boot.cli :as cli])
       (:gen-class))
    
    (def phi (/ (+ (sqrt 5) 1) 2))
    
    (defn fib
       ([n]
         (fib [0 1] n))
       ([pair, n]
          (print (str (first pair) " "))
          (if (> n 1)
            (fib [(second pair) (apply + pair)] (- n 1)))))
    
    (defn fibgolden
       [n]
       (loop [counter 0]
         (if (= counter 0)
           (do 
             (print (str 0 " " 1 " " 1 " "))
             (recur 3))
         (let [f (round (/ (expt phi counter) (sqrt 5)))]
           (print (str f " "))
           (if (< counter (- n 1))
             (recur (+ counter 1)))))))
    
    (cli/defclifn -main
       "Print a Fibonacci sequence to stdout using one of two algorithms."
       [g golden bool "Use the golden mean to calculate"
        n number NUMBER int "Quantity of numbers to generate. Defaults to 10"]
       (let [n (:number *opts* 10)
             note (if golden "[golden]" "[recursive]")]
         (println note "Printing Fibonacci sequence up to" n "numbers:")
         (if golden
           (fibgolden n)
           (fib n)))
         (println))
         
    
.. explanation:: 
   
   Our module is identical to our boot script, except for the following:
   
   * On line 1 we declare a `namespace <https://clojure.org/reference/namespaces>`__ (`more info <https://www.braveclojure.com/organization/>`__). ``ns`` allows us to bring in libraries using the ``:require`` parameter (line 2). The syntax is just like the ``require`` function, except that you don't have to prefix the module name with a `var quote <https://clojure.org/guides/weird_characters#__code_code_var_quote>`__. 
   
   We use the ``:gen-class`` parameter to tell clojure to generate proper Java classes for our namespace when compiling. This allows us to use our compiled jar file like any old Java jar. `More info <https://clojure.org/reference/compilation>`__.
   

To build our jar, there are a handful of steps:

#. Download our dependencies.
#. Compile our clojure code ahead of time (aka `AOT <http://clojure.org/compilation>`__).
#. Add a `POM <http://maven.apache.org/pom.html>`__ file describing our project and the version.
#. Scan all of our dependencies and add them to the fileset to be put into the jar.
#. Build the jar, specifying a module containing a -main function to run when the jar is invoked.

Helpfully, boot provides built-in functionality to do this for us. Each step is implemented as a boot `task <https://github.com/boot-clj/boot/wiki/Tasks>`__. Tasks act as a pipeline: the result of each can influence the next. 

.. code-block:: console
    
    $ boot -d org.clojure/clojure \
           -d boot/core \
           -d boot/base \
           -d org.clojure/math.numeric-tower:0.0.4 \
           -s src/ \
           aot -a \
           pom -p fib -v 1.0.0 \
           uber \
           jar -m fib.core \
           target

A brief explanation of each task and command line options:

    **Line 1-4:** the ``-d`` option specifies a dependency. Here we list   Clojure itself, ``boot.core``, ``boot.base`` and ``math.numeric-tower``.

    **Line 5:** ``-s`` specifies a source directory to look into for ``.clj`` files.

    **Line 6:** this is the AOT task, that compiles all of the ``.clj`` files for us. The ``-a`` flag tells the task to compile everything it finds.

    **Line 7:** the POM task. This task adds project information to the jar. The ``-p`` option specifies the project name, ``-v`` is the version.

    **Line 8:** the uber task collects the dependencies so they can be baked into the jar file. This makes the jar big (huge really), but it ends up being self-contained.

    **Line 9:** the jar task. This is the task that actually generates the jar file. The ``-m`` option specifies which module has the ``-main`` function.
    
    **Line 10:** the :code:`target` task. This task writes out the product of the other tasks to the target directory (:code:`./target` by default).
    
    
    
    
Running the above command, produces output something like this:

.. code-block:: consoleshell
    :linenos: none
     
    $ boot -d "org.clojure/clojure" \
           -d "boot/core" \
           -d "boot/base" \
           -d "org.clojure/math.numeric-tower:0.0.4" \
           -s src/ \
           aot -a \
           pom -p fib -v 1.0.0 \
           uber \
           jar -m fib.core \
           target
    
    Retrieving core-2.0.0-rc8.pom from https://repo.clojars.org/ (3k)
    Retrieving pod-2.0.0-rc8.pom from https://repo.clojars.org/ (4k)
    Retrieving core-2.0.0-rc8.jar from https://repo.clojars.org/ (671k)
    Retrieving pod-2.0.0-rc8.jar from https://repo.clojars.org/ (878k)
    Classpath conflict: org.clojure/clojure version 1.7.0 already loaded, NOT loading version 1.6.0
    Compiling 1/1 fib.core...
    Adding uberjar entries...
    Writing fib-1.0.0.jar...
    Writing target dir(s)...


At this point, there is a file named ``fib-1.0.0.jar`` in the ``target`` directory. We can use the ``java`` command to run it:

.. code-block:: console
    
    $ java -jar target/fib-1.0.0.jar
    [recursive] Printing fibonacci sequence up to 10 numbers:
    0 1 1 2 3 5 8 13 21 34
    $ java -jar target/fib-1.0.0.jar -g -n 20
    [golden] Printing Fibonacci sequence up to 20 numbers:
    0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181
    

You can send this file to a friend, and they can use it too.

.. note::
   
   At time of writing, the ``-h`` flag, that usually displays help info, is not working in the jar file. I think it's because the ``java`` command is "swallowing" it.
   

Introducing build.boot
----------------------

At this point we have a project and can build a standalone jar file from it. This is great, but long command lines are prone to error. Boot provides a mechanism for defining your own tasks and setting the command line options in a single file, named ``build.boot``. Here's a ``build.boot`` that configures boot in a manner equivalent to the command line switches above:

.. code-block:: clojure
    
    (set-env! :dependencies '[[org.clojure/math.numeric-tower "0.0.4"]
                               [boot/core "2.7.2"]
                               [boot/base "2.7.2"]
                               [org.clojure/clojure "1.8.0"]]
              :source-paths #{"src/"})
    
    (task-options!
      pom {:project 'fib 
           :version "1.0.0"}
      jar {:main 'fib.core}
      aot {:all true})
      
   
.. explanation::
   
   ``build.boot`` is analogous to a ``Makefile`` or `Apache Ant <https://ant.apache.org/>`__ build file - it acts a a robust configuration file with declarative syntax that tells the build tools what to do. 
   
   ``set-env!`` was introduced earlier, here's the new concepts introduced:
   
   * We have to specify the precise versions of our dependencies here - this might seem tedious, but it's best to *always* do this, even with things we take for granted like clojure itself and boot. This way, our code will always be explicitly telling any users which versions its compatible with, and we won't get any surprises. 
   
     Most of the time, you'll know the version number you're using from clojars, but for boot and clojure itself, it might have been a while since you isntalled, and you may not remember. 
     
     To find out the boot and clojure version number, we can ask ``boot``:
     
     .. code-block:: console
        :linenos: none
        
        $ boot -V
        #http://boot-clj.com
        #Tue May 15 14:27:28 EDT 2018
        BOOT_CLOJURE_NAME=org.clojure/clojure
        BOOT_CLOJURE_VERSION=1.8.0
        BOOT_VERSION=2.7.2
        
     
     
   
   
   * The ``:source-paths`` setting is using a neat built-in data structure called a `hash set <https://clojure.org/reference/data_structures#Sets>`__. It's a clever way of handling a sequence of values that come from multiple sources but need to be unique - the data structure handles duplicates transparently so you don't have to think about it. This comes at a slight performance cost in most cases (compared to a hashmap or "dumb" sequence like an array or vector), but it also adds some interesting features like efficient unions and diffs.
   
   * On line 7, we use the ``task-options!`` macro to take the place of specifying task options on the command line. The keys for each setting correspond to the "long form" of the given option. You can see these using the built-in help:
       
       .. code-block:: console
          :linenos: none
          
          $ boot pom -h
          
          Create project pom.xml file.
          
          The project and version must be specified to make a pom.xml.
          
          Options:
            -h, --help                   Print this help info.
            -p, --project SYM            SYM sets the project id (eg. foo/bar).
            -v, --version VER            VER sets the project version.
            -d, --description DESC       DESC sets the project description.
            -c, --classifier STR         STR sets the project classifier.
            -P, --packaging STR          STR sets the project packaging type, i.e. war, pom.
            -u, --url URL                URL sets the project homepage url.
            -s, --scm KEY=VAL            Conj [KEY VAL] onto the project scm map (KEY is one of url, tag, connection, developerConnection).
            -l, --license NAME:URL       Conj [NAME URL] onto the map {name url} of project licenses.
            -o, --developers NAME:EMAIL  Conj [NAME EMAIL] onto the map {name email} of project developers.
            -D, --dependencies SYM:VER   Conj [SYM VER] onto the project dependencies vector (overrides boot env dependencies).
   
       
       As you can see, the ``-v`` parameter corresponds to ``--version``, and ``-p`` to ``--project``. Hence we use ``:version`` and ``:project`` in ``task-options!``. 
       
       You will have to use a little intutition to figure out what *data type* the command wants, or you can always look at `the source <https://github.com/boot-clj/boot/blob/de1b9876b4485b23b25614dd4b4a528d0931ccda/boot/core/src/boot/task/built_in.clj#L534>`__:
       
       .. code-block:: clojure
          
          ...
          (core/deftask pom
            "Create project pom.xml file.
            The project and version must be specified to make a pom.xml.
            Note that if you want to install some other artifact along with the main one,
            for instance the classic sources or javadoc artifact, you have to add the
            classifier to your pom.xml, which translates to adding :classifier to this
            task."
            
            [p project SYM           sym           "The project id (eg. foo/bar)."
             v version VER           str           "The project version."
             d description DESC      str           "The project description."
             c classifier STR        str           "The project classifier."
             P packaging STR         str           "The project packaging type, i.e. war, pom"
             u url URL               str           "The project homepage url."
             s scm KEY=VAL           {kw str}      "The project scm map (KEY is one of url, tag, connection, developerConnection)."
             l license NAME:URL      {str str}     "The map {name url} of project licenses."
             o developers NAME:EMAIL {str str}     "The map {name email} of project developers."
             D dependencies SYM:VER  [[sym str]]   "The project dependencies vector (overrides boot env dependencies)."
             a parent SYM:VER=PATH [sym str str] "The project dependency vector of the parent project, path included."]
          ...
       
       On line 9, we see that the ``project`` argument is a symbol - this is why we prefix it with a var quote in ``build.boot``.
   
   

With ``build.boot`` in the current directory, you can now run the tasks like this:

.. code-block:: console
    
    $ boot aot pom uber jar target
    Compiling fib.core...
    Writing pom.xml and pom.properties...
    Adding uberjar entries...
    Writing fib-1.0.0.jar...
    Writing target dir(s)...

The convenience of ``build.boot`` one step further, we can chain the tasks we want to use into our own task, using the ``deftask`` macro:

.. code-block:: clojure
    
    (set-env! :dependencies '[[org.clojure/math.numeric-tower "0.0.4"]
                               [boot/core "2.7.2"]
                               [boot/base "2.7.2"]
                               [org.clojure/clojure "1.8.0"]]
              :source-paths #{"src/"})
    
    (task-options!
      pom {:project 'fib 
           :version "1.0.0"}
      jar {:main 'fib.core}
      aot {:all true})
    
    (deftask build
     "Create a standalone jar file that computes Fibonacci sequences."
     []
     (comp (aot) (pom) (uber) (jar) (target)))

Now, we can just run ``boot build`` to make our standalone jar file. You'll also see your task show up in the help output:

.. code-block:: console
    
    $ boot -h
    ...
    build Create a standalone jar file that computes Fibonacci sequences.
    ...
    $ boot build
    Compiling fib.core...
    Writing pom.xml and pom.properties...
    Adding uberjar entries...
    Writing fib-1.0.0.jar...
    Writing target dir(s)...

Where To Go From Here
---------------------

At this point we've touched most of the awesomeness that boot gives us. With these basic tools, there's all sorts of interesting things we can do next. Here are some ideas:

-  Use boot instead of a "typical" scripting language for systems automation.
-  Distribute single :code:`.boot` files containing entire applications.
-  Build WAR files and use other `boot tasks provided by the community <https://github.com/boot-clj/boot/wiki/Community-Tasks>`__\ to do all sorts of cool things, like `compile SASS     templates <https://github.com/mathias/boot-sassc>`__ and `deploy to Amazon Elastic Beanstalk <https://github.com/adzerk/boot-beanstalk>`__.
-  Write your own, specialized tasks to help streamline complex build     processes - boot can replace (or augment) tools like     `ant <http://ant.apache.org/>`__ and     `make <http://www.gnu.org/software/make/>`__.

Appendix: Alternative Install Methods
=====================================
Recent versions of boot are now available for homebrew, nix, and docker. More details `here <https://github.com/boot-clj/boot#install>`__.