Advanced Boot Scripting
#######################
:date: 2015-04-11 15:07
:author: lionfacelemonface
:category: tutorial
:slug: advanced-boot-scripting

`As covered in a previous post <{filename}boot-getting-started-with-clojure-in-10-minutes.rst>`__,
`boot <https://github.com/boot-clj/boot>`__ is an all-around useful tool
for building clojure applications, but one feature in particular has
proven a *adjuncti finalum*\*: boot lets you do `clojure
scripting <https://github.com/boot-clj/boot/wiki/Scripts>`__. This
elevates clojure to the same high productivity of scripting languages
(like my personal favorite, Python), but bakes in dependency management
and other goodies. This allows the user to build complexity iteratively,
in a straight-forward manner (verses generating a bunch of boiler plate
project code and building a package). This article explores boot
scripting further, illustrating how boot can be used to quickly and
easily develop and distribute applications and tools. There's also
discussion about getting your jars into
`Clojars <http://clojars.org>`__, and setting up a simple bare-minimum
`Maven <http://maven.apache.org/index.html>`__ repository.

.. admonition:: Edit
    
    I originally had "*interfectorem pluma*\ " to represent "killer
    feature" in Latin, however thanks to danielsmulewicz in #hoplon
    reminding me how stupid Google Translate can be, I consulted a
    Latin->English dictionary and Wikipedia to attempt an uneducated, but
    better Latin equivalent. I mention it here because it's all extremely
    funny, as *interfectorem pluma* literally translates to something like
    "feather murderer". In my amateur approach *adjuncti finalum* literally
    translates to something like "characteristic of the ultimate goal",
    which, if even remotely correct, is pretty accurate.

Setup
-----

`As I've covered before <{filename}boot-getting-started-with-clojure-in-10-minutes.rst>`__,
boot is easy to install. All you need is a JDK and the `boot executable <https://github.com/boot-clj/boot/releases>`__. Here's arecap for the Linux and OSX crowd, just to get you going (we'll assume you already have a JDK set up, have wget, and have sudo privileges):

.. code-block:: console
   :linenos: none
   
   $ wget https://github.com/boot-clj/boot-bin/releases/download/latest/boot.sh
   $ mv boot.sh boot && chmod a+x boot && sudo mv boot /usr/local/bin
   $ boot -u
   


Note that we are also instructing boot to update itself. This is useful if you've used boot in the past - the executable and the core boot libraries are distributed separately.

Making Boot Faster
------------------

Adding the following to your environment will speed boot startup by a vast amount. You can either run this command in your terminal, or make it permanent by putting this line into ``~/.bash_profile`` or similar other files for your particular shell. See the `JVM-Options <https://github.com/boot-clj/boot/wiki/JVM-Options>`__ page in the boot documentation for details, and other ways to incorporate these settings into your projects:

.. code-block:: console
   :linenos: none
   
   export BOOT_JVM_OPTIONS="-client -XX:+TieredCompilation XX:TieredStopAtLevel=1 -Xverify:none"
   

A Simple Script
---------------

For this article, we'll start with an example of a useful application that grabs the most recent tweet from the `Nihilist Arby's <https://twitter.com/nihilist_arbys>`__ twitter feed. A great addition to your `MOTD <http://en.wikipedia.org/wiki/Motd_%28Unix%29>`__ to de-motivate users overzealous about the fact that they have SSH privileges to your machine.

Twitter API Tokens
------------------
Before we begin, set up an application and `obtain a consumer key <https://dev.twitter.com/oauth/overview/application-owner-access-tokens>`__ using a twitter account for which you have the username and password. For the sake of security, you may want to limit the application's access to read only. The tokens can be used to read anything in the account, and any private feeds the account has access to, so be careful. 

Quick Note: Development Deviations
----------------------------------
Since we're not building anything right now, or utilizing the task infrastructure, we don't need a ``build.boot`` file. However, to make prototyping a bit easier, it's useful to create one that will load our dependencies or libraries we're playing with, when we run ``boot repl``: 

.. code-block:: clojure
   
   #!/usr/bin/env boot
   (set-env! :dependencies '[[twitter-api "0.7.8"]])
   

Alternatively, we can pre-load dependencies on the command line when we run the repl task:

.. code-block:: console
   :linenos: none
   
   $ boot -d twitter-api:0.7.8 repl
   

The Script: Version 1
---------------------

For the first pass of the script, we will hard-code our credentials, and not bother taking any command-line arguments. This illustrates what a bare-minimum boot script looks like.

.. code-block:: clojure
   
   #!/usr/bin/env boot
   (set-env! :dependencies '[[twitter-api "0.7.8"]])
    
   (use '[twitter.oauth]
        '[twitter.api.restful]
        '[twitter.callbacks]
        '[twitter.callbacks.handlers])
   
   (import '(twitter.callbacks.protocols SyncSingleCallback))
   
   (defn printer
     [response]
       (println (:text (second response))))

   (defn -main
      []
      (statuses-user-timeline
        :oauth-creds
          (make-oauth-creds
            "[YOUR API KEY ID]"
            "[YOUR API KEY]")
        :callbacks (SyncSingleCallback.
                    (comp printer response-return-body)
                    exception-print
                    exception-print)
        :params
          {:screen-name "nihilist\_arbys"
           :count 2}))
    
   


Making this script executable, it can be run on the command line. The
result will be the last tweet. I named my script ``downer``, but you can
name it however you'd like:

.. code-block:: console
   :linenos: none
   
   $ chmod +x downer
   $ ./downer
   Rip it to shreds. Put it on a bun. Slather it in horsey sauce. Watch them line up to gorge. Feeding pigs to pigs. Arbys: a flat circle.
   
   


You may see some output on stderr about some missing logging libraries. For now, these can be ignored.

Lets take a quick look at the script's main components:

-  The first 2 lines are what make this a boot script. The ``set-env!`` function and general information about environments can be found in the `boot documentation <https://github.com/boot-clj/boot/wiki/Boot-Environment>`__.
   
   First we have the "`shebang <http://en.wikipedia.org/wiki/Shebang_%28Unix%29>`__\ " line, which tells the operating system what interpreter to use to run the script. In this case, we're taking advantage of the convention of having ``/bin/env`` available in the same location on most systems, to figure out where boot is. Then we declare our sole dependency on `twitter-api <https://github.com/adamwynne/twitter-api>`__.
   

-  lines 4-9 are typical use/import statements. In a boot script, a special namespace is created, called ``boot.user``. You can alternatively load external code using the ``ns`` form. The example code could be replaced thusly:

.. code-block:: clojure
   
   (ns boot.user
   (:use [twitter.oauth]
   [twitter.api.restful]
   [twitter.callbacks]
   [twitter.callbacks.handlers])
   
   (:import [twitter.callbacks.protocols SyncSingleCallback]))
   
   

-  Lines 11-28 are the "meat" of the program. Boot will execute the first  ``-main`` function that it finds in a script. For details about what the code is doing, see the `twitter-api <https://github.com/adamwynne/twitter-api>`__ and the `twitter restful api <https://dev.twitter.com/rest/reference/get/statuses/user_timeline>`__    documentation. In essence, the app makes a RESTful call to the twitter API, providing an API key and the necessary parameters. We then use a special callback to print the message from the result of that call.

Distribution/Installation: Mark 1
---------------------------------

The real beauty of this boot script we have, is that it is a self-contained entity. We can send it to anyone who has boot and a JDK installed. They can place the script anywhere they like. Dependencies are automatically downloaded the first time its run.

A Not-So-Simple Script
----------------------

Boot scripting provides a natural progression from "just a script" to "full-blown application".

Boot scripts contain all of the functions needed to run, but this poses some problems:

-  as functionality grows, the script can quickly become unruly
-  because of the way boot encapsulates the running code, it can be difficult to debug.

The solution to both of these problems is to move code into other files, and use the ``-main`` function in your boot script to invoke that code.

This is handled quite simply by utilizing boot's ``:source-paths`` environment option, and a little refactoring.

We'll construct a directory named ``src``, and create a ``last_tweet.clj`` file. In it, we'll declare a new namespace, last-tweet, and move the code there.

``src/last_tweet.clj``:

.. code-block:: clojure
   
   (ns last-tweet
   (:use [twitter.oauth]
   [twitter.api.restful]
   [twitter.callbacks]
   [twitter.callbacks.handlers])
   (:import [twitter.callbacks.protocols SyncSingleCallback]))
   
   (defn printer
     [response]
     (println (:text (first response))))
   
   (defn last-tweet
     []
     (statuses-user-timeline
     :oauth-creds
        (make-oauth-creds
          "[YOUR API KEY ID]"
          "[YOUR API KEY]")
    :callbacks (SyncSingleCallback. 
                (comp printer response-return-body)
                    exception-print
                    exception-print)
    :params {:screen-name "nihilist_arbys"
             :count 1}))
   
   

This code is copied from the original boot script, almost verbatim. We've just made use of our own namespace, and renamed ``-main`` to ``last-tweet``.

Here is the new ``downer`` script:

.. code-block:: clojure
   
   #!/usr/bin/env boot
   (set-env!
     :dependencies '[[twitter-api "0.7.8"]]
     :source-paths #{"src"})
   
   (require '[last-tweet :refer [last-tweet]])
   
   (defn -main
     []
     (last-tweet))
   
   

This greatly simplifies our script, and does a better job of separating our concerns. We've segregated the application logic from the user interface. We've set ourselves up for some additional refactoring to make things more flexible.

We can add many namespaces to the ``src`` directory. We can also add other source paths - the ``:source-paths`` directive is a `hash set <http://clojure.org/data_structures#toc24>`__.

Now we can refactor the \ ``last-tweet/last-tweet`` function to take credentials and the twitter account to get a tweet from as arguments:

.. code-block:: clojure
   
   (defn last-tweet
     "Print the last tweet from a given twitter account"
     [account secret-id secret-key]
     (let [creds (make-oauth-creds secret-id secret-key)
           callback (SyncSingleCallback.
                      (comp printer response-return-body)
                      exception-print
                      exception-print)]
       (statuses-user-timeline
         :oauth-creds creds
         :callbacks callback
         :params
           {:screen-name account
            :count 1})))
   
   

We've gone from a hard-coded function to one that is more general-purpose.

Now we can utilize boot's extremely useful ``defclifn`` macro and boot's `task option DSL <https://github.com/boot-clj/boot/wiki/Task-Options-DSL>`__ to wrap our function, allowing the user to provide the values on the command-line, creating a proper user interface.

.. code-block:: clojure
   
   #!/usr/bin/env boot
   (set-env!
     :dependencies '[[twitter-api "0.7.8"]]
     :source-paths #{"src"})
   
   (require
     '[last-tweet :refer [last-tweet]]
     '[boot.cli :as cli])
   
   (cli/defclifn -main
     "Prints the last tweet from the given account. Requires twitter user app
     authentication tokens. The authentication tokens can be set using the
     command-line options below, or in the TWITTER_KEY and TWITTER_KEY_ID
     environment variables.
     
     USAGE: downer [options] [twitter account]"
     
     [k secret-key KEY str "Secret key from Twitter"
      i secret-key-id KEYID str "Secret key id from Twitter"]
     (let [account (get *args* 0 "nihilist_arbys")
           secret-key (or (System/getenv "TWITTER_KEY") (:secret-key *opts*))
           secret-key-id (or (System/getenv "TWITTER_KEY_ID") (:secret-key-id *opts*))]
   
       (if (or (nil? secret-key) (nil? secret-key-id))
         (println "ERROR: you must provide twitter credentials. Try -h")
         (last-tweet
           account
           secret-key-id
           secret-key))))
   
   
A few notes:

-  The docstring for the function is used as the "usage" message when the user passes the ``-h`` flag.

-  The task option DSL allows for `a pre-processing step <https://github.com/boot-clj/boot/wiki/Task-Options-DSL#types>`__ to be defined for each value. In this case, we used ``str``, which treats each argument as a string. This can be changed to one of many very useful options, including keywords, symbols, files (which take a path and return a java.io object) and many more, including `complex compound values <https://github.com/boot-clj/boot/wiki/Task-Options-DSL#complex-options>`__.

-  There are two special variables that are provided by the ``defclifn``   macro: ``*opts*`` and ``*args*``. ``*opts*`` contains all of the processed options as defined in the argument list, in the form of a map. ``*args*`` contains all other values passed on the command line, as a vector. We use the ``*args*`` variable to allow the user an intuitive way to override the default twitter account.

-  The use of environment variables as alternatives to CLI options is  illustrated here. It's very useful for deployment of more complex    applications, and keeps sensitive information out of the process list.

-  We've added some error handling to give the user a nice message if they neglect to set their credentials.

Now we can see command-line output:

.. code-block:: console
   :linenos: none
   
   $ ./downer
   ERROR: you must provide twitter credentials. Try -h
   
   

The output of ``./downer -h``:

.. code-block:: console
   :linenos: none
   
   $ ./downer -h
   Prints the last tweet from the given account. Requires twitter user app authentication tokens.

   The authentication tokens can be set using the command-line options below, or in the TWITTER_KEY and TWITTER_KEY_ID environment variables.
   
   
   USAGE: downer [options] [twitter account]
   
   Options:
    -h, --help Print this help info.
    -k, --secret-key KEY Set secret key from Twitter to KEY.
    -i, --secret-key-id KEYID Set secret key id from Twitter to KEYID.
    
   

We set the environment variables, and try getting the last post from a different, possibly more depressing account:

.. code-block:: console
   :linenos: none
   
   $ export TWITTER\_KEY\_ID="XXXXXXXXXXXXXXXXX"
   $ export TWITTER\_KEY="YYYYYYYYYYYYYYYYYYYYYYYYY"
   $ ./downer jjmojojjmojo
   FINALLY... this just makes getting the sweet, sweet carrot dogs that much easier... http://t.co/TWYer14JH4 @adzerk
   
   


Distribution/Installation, Mark 2
---------------------------------

Pulling some of the code out into a separate file has made our little script cleaner, but now distributing the file is slightly more complicated, since we have to provide the script access to the code we factored out.

There are several ways to handle this:

-  Distribute the source code via git, or a tarball. The ``:source-paths`` environment parameter can be changed if needed to point to a proper location such as ``/opt/downer``, or ``/usr/local/lib/downer``.

-  Build a library jar file. The jar file can be installed into a local maven repository, or a public one like `clojars <https://clojars.org/>`__.

The first option is sub-optimal. It can be made somewhat easier with help from `fpm <https://github.com/jordansissel/fpm>`__, but it's still a bit cumbersome. The real beauty of boot scripting is we don't have to bother with complex installation procedures.

We can leverage the power of java jar files (which are just zip files under the hood) to contain our source code and other artifacts.

This makes the jar file the best path. Once the jar is installed into a maven repository the script can reach, the script can once again be distributed as a simple stand-alone text file.

We can use boot for this. *That's what it does.*

Compiling A Library Jar
~~~~~~~~~~~~~~~~~~~~~~~
For a jar file to be installable via maven (which is what boot and the clojure ecosystem uses under the hood), it must contain a pom.xml file. This file will declare the project version, the dependencies and other metadata.

We can construct a jar file from our source code just using the command line, or we can `wrap it up in a build.boot file in a custom task. <https://lionfacelemonface.wordpress.com/2015/01/17/boot-getting-started-with-clojure-in-10-minutes/#build.boot>`__

Here's the basic command to get our last tweet jar:

.. code-block:: console 
   
   $ boot -d org.clojure/clojure:1.6.0 \
          -d boot/core:2.0.0-rc12 \
          -d twitter-api:0.7.8 \
          -s src/ \
          aot -a \
          pom -p last-tweet -v 1.0.0 \
          jar
   
   


Looking in the ``target`` directory, we can see our jar file:

.. code-block:: console
   :linenos: none
   
   $ ls target/*.jar
   last-tweet-1.0.0.jar
   


We have several options for distribution, now that we have a jar file, each one takes advantage of the `Apache Maven <https://maven.apache.org/>`__ ecosystem:

#. We can send the jar file along with the script to the user, and they
   can install it with boot.
#. We can set up our own maven repository and upload the jar to that,
   then provide access to the user.
#. We can send the jar file to a public repository like
   `clojars <https://clojars.org/>`__.
#. We can upload the file to S3, and provide credentials to our user.

Wait, Why Not Distribute A Self-Contained Jar?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We could move the CLI logic into our last-tweet namespace, and get rid of the boot script altogether. We could add the "uber" task and bundle all of our dependencies into a single, stand-alone, self-contained jar file that could be distributed (via maven as described above) without any external dependencies besides a JVM (the user won't even need boot or clojure).

This process is covered in some detail `here  <{filename}boot-getting-started-with-clojure-in-10-minutes.rst>`__.

There's nothing inherently wrong with this practice. In fact, it's a good idea to seriously consider it when deciding how to deploy an application.

But when writing boot scripts, it can be very useful to allow the user to change things in the script, or encourage them to write new scripts that use the underlying code in new ways.

It helps to start looking at a boot script much like we would any other shell script - consider *composing* calls to external code instead of implementing and containing it internally.

This concept coupled with the "it just works" approach of boot makes distributing core code as library dependencies of particular interest.
You can make changes to your library code and distribute it once, and when your users run their boot script it will automatically update. 

On the other side of that coin, you have less worry about breaking existing scripts "in the wild".  Users can pin the version of your library to a specific number and avoid automatic updates altogether.

It amounts to an extremely elegant way of constructing tools.

Script Modifications
~~~~~~~~~~~~~~~~~~~~

To use an external jar instead of our bundled-in code, we just need to omit the ``:source-paths`` environment directive, and add our jar into the ``:dependencies`` list.

Here are the changes to the ``(set-env!)`` call:

.. code-block:: clojure
   
   (set-env!
     :dependencies '[[twitter-api "0.7.8"]
     [last-tweet "LATEST"]])
   

Note that we're not pinning the version to a particular release, instead specifying the special keyword ``LATEST`` to signal that we always want the latest. This is helpful when distributing jar files that are updated frequently while the boot script is not.

However, be careful not to rely on this too heavily. If the API in the library falls too far out of sync with the script, users will get errors.

Installing A Jar With Boot
~~~~~~~~~~~~~~~~~~~~~~~~~~
Boot provides the install task, which can install jars built with a pipeline of tasks, or a specific jar with the -f option.

.. code-block:: console
   :linenos: none
   
   $ boot install -f target/last-tweet-1.0.0.jar
   

Now we can run our script and it will use the locally installed jar:

.. code-block:: console
   :linenos: none
   
   $ ./downer jjmojojjmojo
   RT @adzerk: 3 ways for vendors to keep mobile ad tech lean - "be easy to work with" should be a no brainer http://t.co/P3yrKH74WW @blp101 v…
   
   

This is the easiest way to get jars working with boot, but it's the least flexible. Every time you make a change to your code, you need to create a new version of your jar and distribute it to all of your users, and they will need to install it.

Uploading To Clojars
~~~~~~~~~~~~~~~~~~~~

`Clojars <https://clojars.org/>`__ provides a public maven repository for the greater Clojure community.

There isn't much in the way of documentation for using boot with clojars, but there is a `tutorial <https://github.com/ato/clojars-web/wiki/tutorial>`__, and a handy tool called `bootlaces <https://github.com/adzerk-oss/bootlaces>`__ that provides a couple of wrapper boot tasks to make the process more seamless.

Alas, neither of these things goes far enough to help the brand new boot user who wants to make use of clojars for their libraries. Very little is explained, and the tutorial is leiningen-centric.

.. note::
   
   There is also an excellent write up of the process (also linegien-centric but it covers GPG and signing your jars) by Michael Peterson over at `ThornyDev <http://thornydev.blogspot.com/2013/03/signing-and-promoting-your-clojure.html>`__ including links to the rationale for signing packages.
   

So lets go over the process in detail, from the ground up. Admittedly, this is probably best left for a separate blog post, but as clojars is a great service and something any clojurist should be equipped to participate in - once you've got a handle on how it works "the hard way", you are free to use bootlaces or derive your own workflow. It slots in nicely with the next section, where we build our own maven repository.

In preparation for pushing your jar to clojars, you'll first need to install `GPG <https://www.gnupg.org/>`__.

GPG will be used to sign jar files to ensure they are not tampered with by malicious third parties.

.. note::
   
   For a comprehensive introduction, see `The GPG Mini HOWTO <http://www.dewinter.com/gnupg_howto/english/GPGMiniHowto.html>`__.*
   


GPG can be installed via the downloads located at `gnupg.org <https://www.gnupg.org/download/index.html>`__, or using your preferred package manager.

MacOs users can use homebrew (``brew install gpg``), or MacPorts (``sudo port install gpg``).

We'll need to generate our key, if we've never used GPG before:

.. code-block:: console
   :linenos: none
   
   $ gpg --gen-key
   

You will be asked many questions. For most, you can specify the default suggested by gpg (press ENTER). Take note of the e-mail address that you use for your key, it will be the identifier for your new key in your keyring.

.. note::
   
   It's a good idea to specify a pass-phrase. If you decide not to, you can just enter an empty pass-phrase when prompted.
   

Now that we've generated our key, we can see it using ``gpg --list-keys``:

.. code-block:: console 
   
   $ gpg --list-keys
   /Users/jj/.gnupg/pubring.gpg
   ----------------------------
   pub 2048R/5A36EA7C 2015-05-21
   uid Josh Johnson <[THE EMAIL YOU PROVIDED]>
   sub 2048R/6C662B47 2015-05-21
   

Next, we need to `sign up for a clojars account. <https://clojars.org/register>`__ Ignore the SSH key entry. We will need to generate a text-based "ASCII-armored" version of our public GPG key to paste into the corresponding text box in the form. This is accomplished with the ``gpg`` command:

.. code-block:: console
   :linenos: none
   
   $ gpg --armor --export [THE EMAIL YOU PROVIDED] code
   -----BEGIN PGP PUBLIC KEY BLOCK-----
   [KEY CONTENT HERE]
   -----END PGP PUBLIC KEY BLOCK-----
   

Copy everything from ``-----BEGIN PGP PUBLIC KEY BLOCK-----`` to ``-----END PGP PUBLIC KEY BLOCK-----``, *inclusive*.

Once you have your account set up, the next thing to do is set up a new repository in our ``build.boot`` file:

.. code-block:: clojure
   
   (set-env! :dependencies '[[twitter-api "0.7.8"]]
             :repositories
                #(conj % 
                  ["clojars-upload" {:url "https://clojars.org/repo"
                                     :username "[YOUR USERNAME]"
                                     :password "[YOUR PASSWORD]"}]))
   
   

**WARNING:** *You will want to source your username and password from an environment variable, or some other place, like a local config file. We're putting them here for the sake of simplicity, but this is not a sound practice!*

We've provided a *function* to set the environment property ``:repositories``. This allows us to update the list of repositories instead of replacing it.

We're ready to upload our jar. This can be done, as before, with use ``push`` boot task:

.. code-block:: console
   :linenos: none
   
   $ boot push -f target/last-tweet-1.0.0.jar -g -k [THE EMAIL FOR YOUR KEY] -r clojars-upload
   
   

Taking a look at clojars, we will see our new jar file has been uploaded!

However, it's missing a lot of key information - things that weren't so important when we were building a jar for our own use, but are **very** important when distributing software to a public repository.

In the next section, we'll fix this, but also use the power of boot to make our workflow easier.

Adding better metatdata, fleshing out our ``build.boot``
--------------------------------------------------------

We've constructed a library jar, and have successfully uploaded it to clojars. However, at this point we cannot build and distribute boot scripts that depend on our library. Clojars has a "promotion" process that protects users from seeing jars that do not have essential metadata.

Let's rebuild our jar with a URL, a license, and a proper description:

.. code-block:: console
   :linenos: none
   
   $ boot -d org.clojure/clojure:1.6.0 \
          -d boot/core:2.0.0-rc12 \
          -d twitter-api:0.7.8 \
          -s src/ \
          aot -a \
          pom -p last-tweet\
          -v 1.0.0 \
          -u "https://lionfacelemonface.wordpress.com/2015/04/11/advanced-boot-scripting/"\
          -d "Demo project for advanced boot scripting blog post"\
          jar
   

Now, this is getting a bit (more) unwieldy. It's better if we put this information into our ``build.boot`` file. We'll still use the command line for now, as opposed to building our own boot tasks, but we'll set these properties as default options. This way, we are free to construct our build pipeline as we see fit, but we don't have to specify all of these lengthy parameters on the command line.

We will be able to override these values if we desire, using command line arguments as before.

.. code-block:: clojure
   
   (set-env! 
     :dependencies
       '[[twitter-api "0.7.8"]
         [org.clojure/clojure "1.6.0"]
         [boot/core "2.0.0"]]
     :source-dirs #{"src/"}
     :repositories
        #(conj % ["clojars-upload"
                  {:url "https://clojars.org/repo"
                   :username "[YOUR USERNAME]"
                   :password "[YOUR PASSWORD]"}]))
   
   (task-options!
     pom {:project 'last-tweet
          :url "https://lionfacelemonface.wordpress.com/2015/04/11/advanced-boot-scripting/"
          :version "1.0.1"
          :description "Demo project for advanced boot scripting blog post."
          :license {"MIT License" "http://opensource.org/licenses/mit-license.php"}}
     aot {:all true}
     push {:gpg-sign true
           :repo "clojars-upload"
           :gpg-user-id "[EMAIL ASSOCIATED WITH YOUR KEY]"
           :gpg-passphrase "[YOUR PASSPHRASE]"})
   
   

This is a lot of stuff, so lets walk through the new concepts line by line:

Lines 1-4 invokes the ``set-env!`` function to declare the dependencies we require to be included in our jar. These correspond to the ``-d`` options in the command line we used earlier.

Line 5 specifies the source directories. We previously specified our source directory with the ``-s`` command-line option.

Lines 6-10 update the repositories list with our clojars destination and credentials, as we implemented earlier.

For general explanation of these environment modifying lines, check out `Boot Environment <https://github.com/boot-clj/boot/wiki/Boot-Environment>`__, in the Boot Wiki.

The rest of the file represents settings that are passed to boot tasks.

Generally speaking, these correspond 1:1 with the command line options, but are expected to be pre-processed into clojure data objects.

You can figure out the exact key to set for each value using the ``-h`` switch. For example, the help text for the ``pom`` task, looks like this:

.. code-block:: console
   :linenos: none
   
   $ boot pom -h
   Create project pom.xml file.
   
   The project and version must be specified to make a pom.xml.
   
   Options:
    -h, --help Print this help info.
    -p, --project SYM Set the project id (eg. foo/bar) to SYM.
    -v, --version VER Set the project version to VER.
    -d, --description DESC Set the project description to DESC.
    -u, --url URL Set the project homepage url to URL.
    -l, --license NAME:URL Conj [NAME URL] onto the project license map.
    -s, --scm KEY=VAL Conj [KEY VAL] onto the project scm map (KEY in url, tag).
   

And we can see that the ``-d`` command line option corresponds to the``:description`` key passed to ``task-options!``.

Of particular interest to us are the ``--project`` and ``--license`` options - these are not specified as simple strings.

The ``--project`` option is converted to a clojure *symbol*, as hinted at by the ``SYM`` placeholder variable. To verify this, we need to look at the `source for the task <https://github.com/boot-clj/boot/blob/master/boot/core/src/boot/task/built_in.clj#L27>`__, and read the task-option DSL:

.. code-block:: clojure
   
   "Create project pom.xml file.
   The project and version must be specified to make a pom.xml."
   
   [p project SYM sym "The project id (eg. foo/bar)."
    v version VER str "The project version."
    d description DESC str "The project description."
    u url URL str "The project homepage url."
    l license NAME:URL {str str} "The project license map."
    s scm KEY=VAL {kw str} "The project scm map (KEY in url, tag)."]
   

Here we see in the 4th column, the handling directive for each command line option. In the case of the ``--project`` option, the ``sym`` specification casts the value from the command line into a symbol.

The ``--license`` is specificed as ``{str str}``, indicating it is a *mapping*. On the command line, a colon is used to separate the key of the map from its value. Additional ``--license`` command line options will conjoin into a single map. As such, in ``task-options!``, a map is expected.

.. note::
   
   For a comprehensive explanation of the various options, see the `Task Options DSL <https://github.com/boot-clj/boot/wiki/Task-Options-DSL>`__ page in the Boot Wiki. 
   

The rest of the options are simply strings. A few, such as the ``-a``, or ``:all`` parameter to the ``aot`` task, are flags, and are specified with a boolean value. 

One last note: the version of our project has to be incremented every time that we change the metadata in our jar file. This is important to note since the output jar will be named differently. If you try to upload a jar with the same version as a previous upload, it will fail with an "Access Denied" error.

Now we can rebuild and redeploy our jar. Since we're chaining the boot tasks, the ``push`` task knows to look for jar files to upload in the working file set, so we don't have to specify the path.

.. code-block:: console
   :linenos: none
   
   $ boot aot pom jar push
   

These tasks can be simply composed into a custom boot task. This is left as an exercise for the reader, but with the following caveat:

*Once you've uploaded a jar to clojars, there's no automatic or simple way to get it removed.*

You can open an issue in github to ask for a deletion (details `here <https://github.com/ato/clojars-web/wiki/Contact>`__), but it's considered bad form.

As such, *please be careful what you upload!*. Make sure that you're running tests, and doing verifications on your jar files before you push them out for mass consumption.

It's a good idea to work those sorts of checks into any custom tasks that you put together.

Building Your Own Maven Repository
----------------------------------

Maven handles resolving dependencies in the Java ecosystem. In maven terms, a repository is where you store artifacts, chiefly jar files. It's what boot uses under the hood to resolve and store dependencies.

Maven repositories are relatively simple. If you've been using boot, you already have one, located in ``~/.m2``.

If you take a look you'll see how the files are laid out:

.. code-block:: console
   :linenos: none
   
   $ ls -la ~/.m2/repository/
   total 0
   drwxr-xr-x 41 jj staff 1394 Apr 5 10:50 .
   drwxr-xr-x 3 jj staff 102 Apr 1 09:46 ..
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 alandipert
   drwxr-xr-x 7 jj staff 238 Apr 1 09:46 boot
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 byte-streams
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 cheshire
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 clj-http
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 clj-http-lite
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 clj-jgit
   drwxr-xr-x 3 jj staff 102 Apr 1 10:49 clj-oauth
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 clj-stacktrace
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 clj-tuple
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 clj-yaml
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 clojure-complete
   drwxr-xr-x 7 jj staff 238 Apr 1 10:49 com
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 commons-codec
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 commons-fileupload
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 commons-io
   drwxr-xr-x 3 jj staff 102 Apr 1 09:46 commons-logging
   drwxr-xr-x 3 jj staff 102 Apr 1 10:49 crouton
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 fs
   drwxr-xr-x 3 jj staff 102 Apr 1 10:49 http
   drwxr-xr-x 4 jj staff 136 Apr 1 12:46 io
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 javax
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 javazoom
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 jline
   drwxr-xr-x 3 jj staff 102 Apr 5 10:50 last-tweet
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 mvxcvi
   drwxr-xr-x 4 jj staff 136 Apr 1 09:47 net
   drwxr-xr-x 3 jj staff 102 Apr 3 08:20 opencv
   drwxr-xr-x 3 jj staff 102 Apr 3 09:52 opencv-native
   drwxr-xr-x 14 jj staff 476 Apr 1 10:49 org
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 potemkin
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 primitive-math
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 reply
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 riddley
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 ring
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 slingshot
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 tigris
   drwxr-xr-x 3 jj staff 102 Apr 1 09:47 trptcolin
   drwxr-xr-x 3 jj staff 102 Apr 1 10:49 twitter-api
   

Note the ``last-tweet`` directory - this is where boot put our jar file when we installed it in the last section.

A maven repository is this directory structure, accessible from one of a plethora of different protocols. This includes the file system, HTTP, WebDAV, even directly from S3.

We'll build a repository that we use the file system to write to (we could also use SFTP if this were a remote system), and provide HTTP access for a read-only use.

Boot doesn't currently contain any tools to do this sort of work, so we'll need to install maven.

This is fairly simple, we just need to download the tarball, and unzip it. We can then put its ``bin`` directory into our $PATH so it's available (note this will need to go into your ``.bash_profile`` or similar location to make the change "stick"):

.. code-block:: consolr
   
   $ wget   http://apache.mirrors.hoobly.com/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz
   $ tar -xvf apache-maven-3.3.3-bin.tar.gz
   $ export PATH="$PWD/apache-maven-3.3.3/bin:$PATH"
   $ which mvn
   ...path to the mvn executable
   
   
*See `the download page <https://maven.apache.org/download.cgi>`__ for alternative mirrors and formats.*

If you are using OS X, you can install maven via homebrew:

.. code-block:: console
   :linenos: none
   
   $ brew install maven
   
   

To construct a new maven repository, we just need to install our jar to it:

.. code-block:: console
   :linenos: none
   
   $ mvn deploy:deploy-file \
    -DpomFile=target/META-INF/maven/last-tweet/last-tweet/pom.xml \
    -Dfile=target/last-tweet-1.0.0.jar \
    -DrepositoryId=local-repo \
    -Durl="file:///$PWD/my-maven-repo"
   

As a first pass, we can use the ``file://`` protocol to load the jar from our new repository. We'll need to remove the file from our local repository first:

.. code-block:: console
   :linenos: none
   
   $ rm -rf ~/.m2/repository/last-tweet
   

Then we can add the new repository to our ``downer`` script:

.. code-block:: clojure
   
   (set-env!
    :dependencies '[[twitter-api "0.7.8"]
                    [last-tweet "LATEST"]]
    :repositories #(conj % '["my-maven-repo" {:url "file://[full-path-to-your-repo]"}]))
   
   

We use ``conj`` here to preserve the baked-in defaults.

When we run ``downer`` now, we'll see an ever-so-slight pause and a blank line to indicate the jar is being found and copied. We can then verify that it was used by checking ``~/.m2/repository``:

.. code-block:: console
   :linenos: none
   
   $ ./downer
   $ ls -l ~/.m2/repository
   ...
   last-tweet
   ...
   

To share this repository, we have many options, but we're going to do the simplest for our introductory purposes: set up `nginx <http://nginx.org/>`__ to serve our repository to the public.

.. note::
   
   Any web server will work, as long as it generates directory listings.
   

First, we need to install nginx. There are `packages available for most operating systems <http://nginx.org/en/download.html>`__, and it's in `homebrew for folks using OS X <http://learnaholic.me/2012/10/10/installing-nginx-in-mac-os-x-mountain-lion/>`__.

Since the location of the nginx configuration is variable depending on what operating system you're using, we'll make a bare-minimum configuration and pass it to nginx, called ``nginx.conf``:

.. code-block:: nginx
   
   events {
      worker_connections 1024;
   }
   
   http {
      default_type application/octet-stream;
      server {
        listen 8080;
        location / {
            root [FULL PATH TO YOUR REPOSITORY];
            autoindex on;
        }
      }
   }
    
   


.. note::
   
   You will want to better fine-tune the web server in a "production" deployment, this is just a bare-minimum example to get you going.
   

We can then start up nginx:

.. code-block:: console
   :linenos: none
   
   $ nginx -c nginx.conf
   
   

Nginx will run in the background. Now you can open a browser to http://localhost:8080/, and see your repository.

We can now configure the boot script to use this repository in the same manner we used the file path earlier:

.. code-block:: clojure
   
   (set-env!
     :dependencies '[[twitter-api "0.7.8"]
                     [last-tweet "LATEST"]]
     :repositories #(conj % '["my-maven-repo" {:url "http://localhost:8080"}]))
   
   

And we can test it in the same way as before:

.. code-block:: console
   :linenos: none
   
   $ rm -rf ~/.m2/repository/last-tweet
   $ ./downer
   $ ls -l ~/.m2/repository
   ...
   last-tweet
   ...
    
   

To shut down nginx, we use the ``-s`` switch:

.. code-block:: console
   :linenos: none
   
   $ nginx -s stop
   


From here, you can construct fairly complex maven systems. Maven supports HTTP authentication, so you can present your repository to the world and limit access. You can use WebDAV to make the HTTP-side of the repository read and write.

Outside of the HTTP front-end, you can settle on the ``file://`` protocol and put the repository on a shared drive, and ensure each user has it mounted to the same location.

SFTP is an option for read/write of a remote system, using SSH for authentication (works with keys).
