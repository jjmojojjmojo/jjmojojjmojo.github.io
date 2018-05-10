Boot: Getting Started With Clojure In < 10 Minutes
##################################################
:date: 2015-01-17 11:41
:author: lionfacelemonface
:category: tutorials
:tags: boot, clojure
:slug: boot-getting-started-with-clojure-in-10-minutes

With the power of `boot <http://boot-clj.com/>`__, it's possible to go from "never used java before" to budding `Clojure <http://clojure.org/>`__-ist cranking out jars like a pickle factory in record time. This post walks you through the process, and provides some post-'hello world' examples, with pointers to more information.

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
   

*¡Dales la Bota!* (Give 'em The *Boot*!)
========================================

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
   
   The :code:`boot.user=>` prompt tells us that we are in a special namespace, set up for us by boot.
   
   On line 15, we're doing a simple addition of some integers. When you press enter after typing some code, the result is printed below.
   
   On line 17, we illustrate what happens when there is a java exception. If you'd like to see the full stacktrace, you can use the :code:`(pst)` `form <https://clojuredocs.org/clojure.repl/pst>`__:
   
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
      
   
   


Here's a simple Clojure function that prints the `fibonacci sequence <http://www.mathsisfun.com/numbers/fibonacci-sequence.html>`__ to a given number of digits:

.. code-block:: clojure
    
    (defn fib
      ([n]
        (fib [0 1] n))
      ([pair, n]
        (print (first pair) " ")
        (if (> n 0)
          (fib [(second pair) (apply + pair)] (- n 1))
          (println))))

.. explanation:: Discussion
   
   Boo.



You can paste this into your REPL and try it out:

.. code-block:: clojure
    
    boot.user=> (defn fib
       #_=>   ([n]
       #_=>     (fib [0 1] n))
       #_=>   ([pair, n]
       #_=>     (print (first pair) " ")
       #_=>     (if (> n 0)
       #_=>       (fib [(second pair) (apply + pair)] (- n 1))
       #_=>       (println))))
    #'boot.user/fib
    boot.user=> (fib 10)
    0 1 1 2 3 5 8 13 21 34 55
    nil
    boot.user=> exit
    Bye for now!



Boot also works as a `scripting platform <https://github.com/boot-clj/boot/wiki/Scripts>`__ - you can construct applications, specifying dependencies, and parse command-line arguments. 

We can transform that function into a command-line tool using the power of boot scripting. Assume this file is called :code:`fib.boot`:




.. code-block:: clojure
    
    #!/usr/bin/env boot
    
    (defn fib
       ([n]
         (fib [0 1] n))
       ([pair, n]
         (print (first pair) " ")
         (if (> n 0)
           (fib [(second pair) (apply + pair)] (- n 1))
           (println))))
     
    (defn -main [& args]
       (let [limit (first args)]
         (println "Printing fibonacci sequence up to " limit "numbers")
         (fib (Integer/parseInt limit))))

Make the script executable:

.. code-block:: console
    
    
    $ chmod u+x fib.boot

Now you can run the script:

.. code-block:: console
    
    
    $ ./fib.boot 10
    Printing fibonacci sequence up to 10 numbers
    0 1 1 2 3 5 8 13 21 34

The script can declare dependencies, which will be downloaded as needed when the script is run. Here, we'll show the use of an external dependency: we can write a new fibonacci sequence that utilizes the fact that numbers in the sequence are related to each other by approximately the `golden ratio <http://en.wikipedia.org/wiki/Golden_ratio>`__ (ca 1.62). Rounding makes it all work, but rounding isn't "baked in" to Clojure, so we'll use an external library to do it for us, called `math.numeric-tower <https://github.com/clojure/math.numeric-tower>`__. 

.. note::
    
    In actuality, the required functionality is present, you just need to use some `existing Java libraries <http://stackoverflow.com/a/25098576>`__ to make it work. I admit this is a bit of a strain, but it illustrates the use of external dependencies in boot.

.. code-block:: clojure
    
    #!/usr/bin/env boot
    
    (set-env! :dependencies '[[org.clojure/math.numeric-tower "0.0.4"]])
     (require '[clojure.math.numeric-tower :refer [floor ceil round]])
    
    (defn fib
       [n]
       (loop [counter 0 x 0]
         (if (= counter 0)
           (do (print 0 " " 1 " " 1 " ")
             (recur 3 1))
           (let [y (round (* x 1.62))]
             (print y " ")
             (if (< counter 9)
               (recur (+ counter 1) y))))))
    
    (defn -main [& args]
       (let [limit (first args)]
         (println "Printing fibonacci sequence up to" limit "numbers")
         (fib (Integer/parseInt limit))
         (println)))
         

When you run this code the first time, you'll notice boot tells you that it has downloaded some new jars:

.. code-block:: console
    
    $ ./fib.boot 10
    Retrieving clojure-1.4.0.jar from http://clojars.org/repo/
    Retrieving math.numeric-tower-0.0.4.jar from http://repo1.maven.org/maven2/
    Printing fibonacci sequence up to 10 numbers
    0 1 1 2 3 5 8 13 21 34

The syntax to define our ``-main`` function and parse our command line options can be a bit tedious. Luckily, we can borrow a macro from boot.core that lets us specify CLI options using a robust syntax. For the full syntax, check out `the documentation <https://github.com/boot-clj/boot/wiki/Task-Options-DSL>`__. 

Here, we'll let the user choose which implementation they'd like to use, and utilize the task `DSL <http://martinfowler.com/books/dsl.html>`__ to do some simple command line options:

.. code-block:: clojure
    
    #!/usr/bin/env boot
    
    (set-env! :dependencies '[[org.clojure/math.numeric-tower "0.0.4"]])
    
    (require '[clojure.math.numeric-tower :refer [floor ceil round]])
    (require '[boot.cli :as cli])
    
    (defn fib
       ([n]
         (fib [0 1] n))
       ([pair, n]
          (print (first pair) " ")
          (if (> n 1)
            (fib [(second pair) (apply + pair)] (- n 1)))))
    
    (defn fibgolden
       [n]
       (loop [counter 0 x 0]
         (if (= counter 0)
           (do (print (str 0 "  " 1 "  " 1 "  "))
             (recur 3 1))
         (let [y (round (* x 1.62))]
           (print y " ")
           (if (< counter 9)
             (recur (+ counter 1) y))))))
    
    (cli/defclifn -main
       "Print a fibonacci sequence to stdout using one of two algorithms."
       [g golden bool "Use the golden mean to calculate"
        n number NUMBER int "Quantity of numbers to generate. Defaults to 10"]
       (let [n (:number *opts* 10)
             note (if golden "[golden]" "[recursive]")]
         (println note "Printing fibonacci sequence up to" n "numbers:")
         (if golden
           (fibgolden n)
           (fib n)))
         (println))
         


Now you can see what options are available, tell the script what to do:

.. code-block:: console
    
    $ boot fib.boot -h
    Print a fibonacci sequence to stdout using one of two algorithms.
    
    Options:
     -h, --help Print this help info.
     -g, --golden Use the golden mean to calculate
     -n, --number NUMBER Set quantity of numbers to generate. Defaults to 10 to NUMBER.
    
    $ boot fib.boot
     [recursive] Printing fibonacci sequence up to 10 numbers:
     0 1 1 2 3 5 8 13 21 34
    
    $ boot fib.boot -g -n 20
     [golden] Printing fibonacci sequence up to 20 numbers:
     0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181

Working At The Pickle Factory (Packing Java Jars and More Complex Projects)
---------------------------------------------------------------------------

Now that we've got a basic feel for Clojure and using boot, we can build a project, that creates a library with an entry point that we can use and distribute as a jar file. This opens the doors to being able to deploy web applications, build libraries to share, and distribute standalone applications. First, we need to create a project structure. This will help us keep things organized, and fit in with the way Clojure handles namespaces and files. We'll put our source code in ``src``, and create a new namespace, called ``fib.core``:

.. code-block:: console
    
    $ mkdir -p src/fib

In ``src/fib/core.clj``, we'll declare our new namespace:

.. code-block:: clojure
    
    (ns fib.core
       (:require [clojure.math.numeric-tower :refer [floor ceil round]]
                 [boot.cli :as cli])
       (:gen-class))
    
    (defn fib
       ([n]
         (fib [0 1] n))
       ([pair, n]
         (print (first pair) " ")
         (if (> n 1)
           (fib [(second pair) (apply + pair)] (- n 1)))))
    
    (defn fibgolden
       [n]
       (loop [counter 0 x 0]
         (if (= counter 0)
           (do (print (str 0 "  " 1 "  " 1 "  "))
               (recur 3 1))
         (let [y (round (* x 1.62))]
           (print y " ")
           (if (< counter 9)
             (recur (+ counter 1) y))))))
    
    (cli/defclifn -main
       "Print a fibonacci sequence to stdout using one of two algorithms."
       [g golden bool "Use the golden mean to calculate"
        n number NUMBER int "Quantity of numbers to generate. Defaults to 10"]
       (let [n (if number number 10)
             note (if golden "[golden]" "[recursive]")]
         (println note "Printing fibonacci sequence up to" n "numbers:")
         (if golden
           (fibgolden n)
           (fib n)))
         (println))
         


To build our jar, there are a handful of steps:

#. Download our dependencies.
#. Compile our clojure code ahead of time (aka `AOT <http://clojure.org/compilation>`__).
#. Add a `POM <http://maven.apache.org/pom.html>`__ file describing our project and the version.
#. Scan all of our dependencies and add them to the fileset to be put into the jar.
#. Build the jar, specifying a module containing a -main function to run when the jar is invoked.

Helpfully, boot provides built-in functionality to do this for us. Each step is implemented as a boot `*task* <https://github.com/boot-clj/boot/wiki/Tasks>`__. Tasks act as a pipeline: the result of each can influence the next. 

.. code-block:: console
    
    $ boot -d org.clojure/clojure \
           -d boot/core \
           -d org.clojure/math.numeric-tower:0.0.4 \
           -s src/ \
           aot -a \
           pom -p fib -v 1.0.0 \
           uber \
           jar -m fib.core \
           target

A brief explanation of each task and command line options:

    **Line 1-3:** the ``-d`` option specifies a dependency. Here we list   Clojure itself, ``boot.core``, and ``math.numeric-tower``.

    **Line 4:** ``-s`` specifies a source directory to look into for ``.clj`` files.

    **Line 5:** this is the AOT task, that compiles all of the ``.clj`` files for us. The ``-a`` flag tells the task to compile everything it finds.

    **Line 6:** the POM task. This task adds project information to the jar. The ``-p`` option specifies the project name, ``-v`` is the version.

    **Line 7:** the uber task collects the dependencies so they can be baked into the jar file. This makes the jar big (huge really), but it ends up being self-contained.

    **Line 8:** the jar task. This is the task that actually generates the jar file. The ``-m`` option specifies which module has the ``-main`` function.
    
    **Line 9:** the :code:`target` task. This task writes out the product of the other tasks to the target directory (:code:`./target` by default).
    
    
Running the above command, produces output something like this:

.. code-block:: consoleshell
    
     
    $ boot -d "org.clojure/clojure" \
           -d "boot/core" \
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

You can send this file to a friend, and they can use it too.


Introducing build.boot
----------------------

At this point we have a project and can build a standalone jar file from it. This is great, but long command lines are prone to error. Boot provides a mechanism for defining your own tasks and setting the command line options in a single file, named build.boot. Here's a ``build.boot`` that configures boot in a manner equivalent to the command line switches above:

.. code-block:: clojure
    
    (set-env! :dependencies '[[org.clojure/math.numeric-tower "0.0.4"]
                               [boot/core "LATEST"]
                               [org.clojure/clojure "LATEST"]]
       :source-paths #{"src/"})
    
    (task-options!
      pom {:project 'fib 
           :version "1.0.0"}
      jar {:main 'fib.core}
      aot {:all true})
      


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
                               [boot/core "LATEST"]
                               [org.clojure/clojure "LATEST"]]
       :source-paths #{"src/"})
    
    (task-options!
      pom {:project 'fib 
           :version "1.0.0"}
      jar {:main 'fib.core}
      aot {:all true})
    
    (deftask build
     "Create a standalone jar file that computes fibonacci sequences."
     []
     (comp (aot) (pom) (uber) (jar) (target)))

Now, we can just run ``boot build`` to make our standalone jar file. You'll also see your task show up in the help output:

.. code-block:: console
    
    $ boot -h
    ...
    build Create a standalone jar file that computes fibonacci sequences.
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

Install For All Users
---------------------

Install Via Homebrew
--------------------