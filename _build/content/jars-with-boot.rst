Making And Distributing Jars With Boot
######################################
:date: 2015-04-11 15:07
:author: jjmojojjmojo
:category: tutorial
:slug: making-jars-with-boot
:status: draft

This post covers using boot to build and distribute your applications. We'll dive deep into packing up our clojure code, publishing to clojars, as well as considering other self-hosted distribution options.

We'll do all of this with boot. Because it rocks.

A Simple Application
--------------------
For use in this post, we'll borrow the "last tweet" app from `Advanced Boot Scripting <{filename}advanced-boot-scripting.rst>`__.

Picking up from the end of that article, our directory structure looks something like this:

.. code-block:: console
   :linenos: none
   
   $ ls -lR
   total 8
   -rw-r--r--  1 jj  staff  1060 May 20 08:54 downer
   drwxr-xr-x  3 jj  staff  102 May 20 08:49 src
   
   ./src:
   total 8
   -rw-r--r--  1 jj  staff  651 May 20 08:49 last_tweet.clj
   
We have two files:

* ``downer``, a boot script that provides a simple command-line interface to our application.
* ``src\last_tweet.clj``, our clojure source code - provides the ``last-tweet`` namespace.

.. explanation::
   
   This application uses the `twitter-api <https://clojars.org/twitter-api>`__ library to grab the last tweet from a given account. 
   
   As explained in `Advanced Boot Scripting <{filename}advanced-boot-scripting.rst>`__, to use it, you must set up a developer account for twitter, and generate API credentials.
   
   The CLI script is called ``downer`` because it defaults to displaying the last tweet from the `Nihilist Arbys <https://twitter.com/nihilist_arbys>`__ twitter account. 
   
   This setup is a nice example of general boot scripting, and how you can build pretty robust applications without compiling anything. 
   
   It's also nice groundwork for this post, since it has all of the elements we need to build and distribute jar files.
   
   
Here is the source code for ``last_tweet.clj``:

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
     [account consumer-id consumer-secret]
     (statuses-user-timeline
       :oauth-creds
          (make-oauth-creds
            consumer-id
            consumer-secret)
       :callbacks (SyncSingleCallback.
                    (comp printer response-return-body)
                    exception-print
                    exception-print)
       :params {:screen-name account
                :count 1}))
                
.. explanation:: 
   
   The ``last-tweet`` namespace and its ``last-tweet`` function are fairly self-explanatory. For more information, see `Advanced Boot Scripting <{filename}advanced-boot-scripting.rst>`__, and `the twitter-api github <https://github.com/adamwynne/twitter-api>`__.
   
And the source of ``downer``:

.. code-block:: clojure
    
    #!/usr/bin/env boot
    (set-env!
      :dependencies '[[twitter-api "1.8.0"]
                      [org.slf4j/slf4j-nop "1.7.25"]]
      :source-paths #{"src"})

    (require
      '[last-tweet :refer [last-tweet]]
      '[boot.cli :as cli])
    
    (cli/defclifn -main
      "Prints the last tweet from the given account. Requires twitter user app
      authentication tokens. The authentication tokens can be set using the
      command-line options below, or in the TWITTER_ID and TWITTER_SECRET
      environment variables.
    
      USAGE: downer [options] [twitter account]"
    
      [k consumer-id ID str "Consumer id from Twitter"
       i consumer-secret SECRET str "Consumer secret from Twitter"]
      (let [account (nth *args* 0 "nihilist_arbys")
            consumer-id (or (System/getenv "TWITTER_ID") (:consumer-id *opts*))
            consumer-secret (or (System/getenv "TWITTER_SECRET") (:consumer-secret *opts*))]
    
        (if (or (nil? consumer-id) (nil? consumer-secret))
          (println "ERROR: you must provide twitter credentials. Try -h")
          (last-tweet
            account
            consumer-id
            consumer-secret))))
            
    
.. explanation::
   
   This boot script is covered in detail in `Advanced Boot Scripting <{filename}advanced-boot-scripting.rst>`__. 
   
   We've also included the "SLF4J fix" discussed `here <{filename}advanced-boot-scripting.rst#appendix-getting-rid-of-log4j-notices>`__

Overview Of Our Options
-----------------------
Given we have this application code, we have several ways of putting it together for release:

#. We can put all the code into a boot script, as initially outlined in `Advanced Boot Scripting <{filename}advanced-boot-scripting.rst>`__. It can then be distributed like any other file.

#. We can distribute our code (with or without a boot script) as a tarball or zip file. We could also use system package - slick tool like FPM can make that super easy.

#. We can package our application as a Java jar file, and:
   
   #. Distribute it manually, via e-mail, FTP, file sharing, etc.
   
   #. Distribute it by uploading it to clojars.
   
   #. Distribute it using a private Maven repository.
   

With the last option, we have two approaches we can take:

* We can package our application code, our CLI interface (currently living in the ``downer`` script), and all of our dependencies into what is known as an "uber" jar. 
* We can just pack our application code and CLI interface into a jar meant to be used as a libary.

In this article, we will cover both approaches. Then, we'll cover running our own Maven repository, and uploading to Clojars.

Compiling A Library Jar
-----------------------

For a jar file to be installable via maven (which is what boot and the clojure ecosystem uses under the hood), it must contain a pom.xml file. This file will declare the project version, the dependencies and other metadata.

We can construct a jar file from our source code just using the command line. This is a good practice when first pinning down your build pipeline.

Here's the basic command to get our last tweet jar:

.. code-block:: console 
   :linenos: none
   
   $ boot -d org.clojure/clojure:1.8.0 \
          -d boot/core:2.7.2 \
          -d twitter-api:1.8.0 \
          -s src/ \
          aot -a \
          pom -p last-tweet -v 1.0.0 \
          jar \ 
          target
   

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
----------------------------------------------

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
--------------------

To use an external jar instead of our bundled-in code, we just need to omit the ``:source-paths`` environment directive, and add our jar into the ``:dependencies`` list.

Here are the changes to the ``(set-env!)`` call:

.. code-block:: clojure
   
   (set-env!
     :dependencies '[[twitter-api "0.7.8"]
     [last-tweet "LATEST"]])
   

Note that we're not pinning the version to a particular release, instead specifying the special keyword ``LATEST`` to signal that we always want the latest. This is helpful when distributing jar files that are updated frequently while the boot script is not.

However, be careful not to rely on this too heavily. If the API in the library falls too far out of sync with the script, users will get errors.

Installing A Jar With Boot
--------------------------

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
--------------------

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
   
   

.. warning:: 
   
   You will want to source your username and password from an environment variable, or some other place, like a local config file. We're putting them here for the sake of simplicity, but this is not a sound practice!
   

We've provided a *function* to set the environment property ``:repositories``. This allows us to update the list of repositories instead of replacing it.

We're ready to upload our jar. This can be done, as before, with use ``push`` boot task:

.. code-block:: console
   :linenos: none
   
   $ boot push -f target/last-tweet-1.0.0.jar -g -k [THE EMAIL FOR YOUR KEY] -r clojars-upload
   
   

Taking a look at clojars, we will see our new jar file has been uploaded!

However, it's missing a lot of key information - things that weren't so important when we were building a jar for our own use, but are **very** important when distributing software to a public repository.

In the next section, we'll fix this, but also use the power of boot to make our workflow easier.

Adding better metatdata, fleshing out our ``build.boot``
========================================================

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
==================================

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
   
   
.. tip::
   
   See `the download page <https://maven.apache.org/download.cgi>`__ for alternative mirrors and formats.
   

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
