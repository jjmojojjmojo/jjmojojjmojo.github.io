Purely Python: LSB-Compliant Init Scripts
#########################################
:date: 2009-12-29 08:44
:author: lionfacelemonface
:category: python
:tags: init script, lsb, python
:slug: python-init-scripts
:status: draft

I've recently been writing a large number of Linux
`Sys-V <http://en.wikipedia.org/wiki/UNIX_System_V>`__ style init
scripts, to control how services are started upon system boot (or
terminated upon shutdown).

I've chosen Python over shell script as my language of choice. I've dug
into the tools, conventions and standards behind init scripts, and I'm
documenting what I've found, and what I've done.

*If you're not interested in the background details, you can check out
my `google code
repository <http://code.google.com/p/lionfacelemonface/source/browse/trunk/initscript/>`__
for this article, or jump right to my `init script
skeleton <http://lionfacelemonface.wordpress.com/2009/12/29/python-init-scripts/#code-skeleton>`__,
or `a real-world
example <http://lionfacelemonface.wordpress.com/2009/12/29/python-init-scripts/#aoe-init>`__.*

Background
----------

Over the past few months, I've building a large hardware infrastructure.
It's based on `Red Hat Enterprise Linux
5 <http://www.redhat.com/rhel/server/>`__, and will make heavy use of
`KVM virtualization <http://www.linux-kvm.org/page/Main_Page>`__.

I've established a
`DRBD <http://www.drbd.org/>`__\ +\ `OCFS2 <http://oss.oracle.com/projects/ocfs2/>`__
cluster between two heavy-duty servers serving as virtual machine hosts.

I'm using
`ATA-Over-Ethernet <http://en.wikipedia.org/wiki/ATA_over_Ethernet>`__
(AoE)-based SAN hardware from `Coraid, Inc. <http://www.coraid.com/>`__
for mass-storage and backups.

I'll be running multiple virtual machine guests, mostly Debian based
(`Ubuntu <http://www.ubuntu.com/>`__).

All of these features rely on various services. I got into the business
of writing my own init scripts and the nuts and bolts of the
`init <http://en.wikipedia.org/wiki/Init>`__ system because of a need to
aggregate multiple services under one control script, to ensure they are
started properly.

I was also drawn into init script development due to the lack of a
useful init script from Coraid. Getting the exported drive space to
mount requires a bit of finesse, and my general assessment of `Coraid's
documentation on the
matter <http://www.coraid.com/site/co-files/FAQ.html#ss5.14>`__ is that
they feel that it's up to the individual implementing the SAN to handle
that maneuvering.

There's also an emerging benefit of writing my own control scripts:
consistency across upgrades.

One way to control the order that scripts are executed during
startup/shutdown is to manipulate the LSB Info Blocks and chckconfig
comments (see `Script Requirements <#script-requirements>`__ below for
an explanation).

This is fairly simple to do and highly affective (if not a little
annoying), but this becomes problematic when you go to upgrade your
packages. Either the upgrade will over-wright the modified scripts,
breaking your established order, or possibly worse, the init scripts
that you've modified won't be upgraded.

With your own script, even if it's quite simplistic and just running
other init scripts, you can ensure that the proper order will be
maintained, and your script will be safe from manipulation from package
updates.

So Why Python?
--------------

I chose Python as the scripting language here for a couple of reasons:

#. Python is readily available on both my host machines (RHEL depends
   heavily on Python 2.4) and my guests (Python 2.5 is installed on a
   minimal VM installation of Ubuntu)
#. Python is the primary language that all of my applications will be
   written in. I felt it was best to keep the language consistent if
   possible so that I can hand off future tweaks and bug fixes to any of
   my developers (no sysadmin or shell expert needed).

Python is well-equipped for shell scripting; the
`sys <http://docs.python.org/library/sys.html>`__ and
`os <http://docs.python.org/library/os.html>`__ modules handle most of
the basic shell commands, and the
`subprocess <http://docs.python.org/library/subprocess.html>`__ module
handles process control.

Granted, there are some negative aspects to doing things this way.

Problems arise from the simple differences between a general-purpose
language like Python and a shell automation language like sh or bash.
Depending on your perspective,

::

    if [-e /some/file]; then
         echo "Hey you guys!" 1>&2
    fi

Might be easier to deal with than,

::

    import os, sys

    if os.path.exists('/some/file'):
         print >> sys.stderr, "Hey you guys!"
     

Or, this

::

    import os, sys

    if sys.argv[1] == 'start':
        print "Starting..."
    elif sys.argv[1] == 'stop':
        print "Stopping..."
    elif sys.argv[1] == 'restart':
        print "Restarting..."
    else:
        print "Usage: %s [start|stop|restart]" % (sys.argv[0])

Verses this:

::

    case "$1" in
           'start')
           echo "Starting..."
    ;;
           'stop')
           echo "Stopping..."
    ;;
           'restart')
           echo "Restarting..."
    ;;
           *)
           echo "Usage: $0 [start|stop|restart]"
    ;;
    esac

*Sarcasm implied.* I'm sure I could find many examples where something
is easier to do in Bash than in Python, but you get the idea.

There's a risk of alienating any system administrators that may come
after me, who don't know Python.

`Perl <http://www.perl.org/>`__ is really better suited for this anyway,
right?

Bottom line: I'm not terribly worried about any of this. Python is a
really great language for this purpose, and the process has proven to be
relatively painless.

Concepts
--------

I won't go into deep detail here, since these concepts are better
explained elsewhere, but here's a rundown of the concepts we're dealing
with when creating Python-based init scripts:

-  `System V Init <http://en.wikipedia.org/wiki/Init#SysV-style>`__ -
   the style of init that both of my target OS' use, or are compatible
   with (RHEL and Ubuntu).

   -  `Runlevels <http://en.wikipedia.org/wiki/Runlevel>`__
   -  `/etc/rc.d <http://www.netbsd.org/docs/guide/en/chap-rc.html>`__
   -  `chkconfig (man page) <http://ss64.com/bash/chkconfig.html>`__,
      and `more detail in an old
      article <http://www.linuxjournal.com/article/4445>`__

-  `The Linux Standards Base
   (LSB) <http://www.linuxfoundation.org/collaborate/workgroups/lsb>`__,
   and specifically, its `standards for init
   scripts <http://dev.linux-foundation.org/betaspecs/booksets/LSB-Core-generic/LSB-Core-generic/sysinit.html>`__

Essentially, here's what we need to do:

#. We put an executable script into ``/etc/init.d``
#. We follow the LSB standard to ensure:

   #. the script works with LSB-compliant distros.
   #. dependant services are started/shutdown in the proper order.

#. use ``chkconfig`` to register the service.

This will create a bunch of symlinks to our script in
``/etc/rc.d/rcX.d`` (where ``X`` is each runlevel we specified). One
will be prefixed with an S, indicating a *startup* script, and another
will be prefixed with K, for the *kill* or shutdown script.

The links will also be prefixed with numbers so that they can be sorted
by the init system. This ensures they will start or shutdown in the
proper order.

Script Requirements
-------------------

Because of common convention, LSB standards, and the nuance of the
chkconfig command, any init script we write will have to meet the
following requirements:

#. It must be executable on the command-line.
#. It must support the following command-line options (actions):

   -  **start** - start the service, called during boot
   -  **stop** - stop the service, called during shutdown
   -  **restart** - stop and then start the service; start it if it's
      not running.
   -  **force-reload** - reload configuration, but only if that is
      supported, otherwise, restart the service if it's running
   -  **status** - print the status of the service

   | 
   |  And optionally support the following actions:

   -  **reload** - reload configuration information
   -  **try-restart** - restart the service \*only\* if it's already
      running

#. It must be placed into ``/etc/init.d``. (Not sure if a symlink will
   work)
#. It must contain 2 comments indicating the requested start/shutdown
   order and the description (these are specified by the ```chkconfig``
   man page <http://ss64.com/bash/chkconfig.html>`__):

   ::

                # chkconfig: 345 20 70
                # description: My service that rocks \
                # socks
                

   There must be a space between the hash mark and the
   ``chkconfig``/``description`` field name.

   The ``chkconfig:`` field indicates 3 space-separated values:

   #. what runlevels you want the service to run at (no spaces; a single
      dash means "don't start by default in any runlevels")
   #. What order you'd like the service to *start*
   #. What order you'd like the service to *shut down*

   Note the orders are just *requests*, the LSB block (defined below)
   and other dependencies will dictate the final start/shutdown order.

   .. raw:: html

      <p>

   The ``description:`` field describes what the service is. It can span
   multiple lines if you add a backslash before the carriage return, as
   illustrated above.

#. | It must contain an `LSB info
     block <http://dev.linux-foundation.org/betaspecs/booksets/LSB-Core-generic/LSB-Core-generic/initscrcomconv.html>`__,
     with at least the ``Description``, and ``Provides`` fields.

   ::

                ### BEGIN INIT INFO
                # Provides: myservice
                # Description: A service of mine that rocks socks 
                ### END INIT INFO
                

   The ``Description`` serves the same purpose as the ``chkconfig``
   description (and they can be the same text).

   The ``Provides`` field lists all of the "boot facilities" that this
   service provides. This is used to set dependencies.

   Listing more than one can be useful if you are controlling multiple
   services, or replacing the standard init scripts (so you can specify
   ``cluster ocfs2 drbd``, and any other drbd or ocfs2-dependant
   services will not need to be altered).

   However, it's most likely you'll want to also add the
   ``Required-Start`` and ``Required-Stop`` fields as well. These fields
   list "boot facilities" that your service requires during startup and
   shutdown.

   ::

                ### BEGIN INIT INFO
                # Provides: myservice
                # Description: A service of mine that rocks socks
                # Required-Start: nfs ntpd
                # Required-Stop: nfs
                ### END INIT INFO
                

   In this example, we're telling ``chkconfig`` that our service mustn't
   start before nfs *and* ntpd have started.

   .. raw:: html

      <p>

   | There are also `some "facilities" that are
     in-specific <http://dev.linux-foundation.org/betaspecs/booksets/LSB-Core-generic/LSB-Core-generic/facilname.html>`__,
     and prefixed with a dollar sign. These include ``$network`` and
     ``$local_fs``,
   |  which represent "the network is up" and "all local file systems
     are mounted", respectively.

#. The script must write a file with the same name as the service to
   ``/var/lock/subsys``.

   .. raw:: html

      </p>

   I'm having trouble finding concrete explanation as to why this is a
   requirement. All I've been able to find is a `Red Hat "tips and
   tricks"
   entry <http://www.redhat.com/magazine/008jun05/departments/tips_tricks/>`__
   (scroll down).

   .. raw:: html

      <p>

   So I'm not sure if this is a hard requirement, a Red Hat requirement,
   or what, but it was part of `Coraid's init script
   shell <http://www.coraid.com/site/co-files/FAQ.html#ss5.14>`__, and I
   don't see any harm, so I've included it here.

Some other things to keep in mind:

-  Best practice dictates that we put functions and such in external
   modules. This is difficult in the service/init script environment.
   The best thing to do is create an egg of your special dependancies
   and install it into your system python.

   *There is a potential for putting the init script into an egg
   itself.* I haven't explored this yet, but it would allow for easy
   inclusion of local libraries, allow you to keep the init script
   simple, segregate tests from the script itself, and automatically
   install any external resources.

-  Root will be executing this script, so be careful!

-  This script is intended to *control* a separate application. It's not
   an application in itself.

   The script is expected to exit after spawning the controlled
   application and return a relevant status code.

-  Unit testing can be problematic. I've come up with a relatively
   cleaver way of dealing with that, which I will describe below.

Code Skeleton
-------------

Taking the above requirements into account, I've developed a code
skeleton that contains all of the bits and pieces, plus an easy to use
"switchboard" to control the whole thing.

::

    #!/usr/bin/python
    #
    # Init script skeleton for Python-based service control scripts
    #
    # chkconfig: 123456 1 99
    # description: My service
    #
    # Author: Josh Johnson 
    #
    #
    ### BEGIN INIT INFO
    # Provides: my-service
    # Required-Start: 
    # Required-Stop: 
    # Default-Start:  123456
    # Default-Stop:  123456
    # Short-Description: My service
    # Description: My service
    ### END INIT INFO

    import sys, os, subprocess, re, time

    def lock():
        """
        Create the /var/lock/subsys file
        """
        open('/var/lock/subsys/my-service', 'w').close()
        
    def locked():
        """
        Return True if the lock file exists
        """
        return os.path.exists('/var/lock/subsys/my-service')
        
    def unlock():
        """
        Remove the /var/lock/subsys file
        """
        os.remove('/var/lock/subsys/my-service')

    def start():
        """
        Do whatever needs to be done.. this is where you start any applications,
        mount filesystems, etc.
        """

    def stop():
        """
        Shut everything down, clean up.
        """
        
    def restart():
        """
        Stop and then start
        """
        stop()
        lock()
        start()
        
    def status():
        """
        Print any relevant status info, and return a status code, an integer:
        
        0         program is running or service is OK
        1         program is dead and /var/run pid file exists
        2         program is dead and /var/lock lock file exists
        3         program is not running
        4         program or service status is unknown
        5-99      reserved for future LSB use
        100-149   reserved for distribution use
        150-199   reserved for application use
        200-254   reserved
        
        @see: http://dev.linux-foundation.org/betaspecs/booksets/LSB-Core-generic/LSB-Core-generic/iniscrptact.html
        """
        if not locked():
            # this is dubious! if you're controlling another process, you should check its
            # PID file or use some other means.. consider this an example
            print "STATUS: Program isn't running"
            return 3
        else:
            print "STATUS: Everything is A-OK"
            return 0

    def test():
        """
        This is my way of "unit testing" the script. This function
        calls each of actions, mimicking the switchboard below. 
        
        It then verifies that the functions did what they were supposed to, 
        and reports any problems to stderr.
        
        @TODO: this could be used to inspect the system (e.g. open a web page if this is
        a web server control script) instead of the script.
        
        @TODO: you'll need to also check for PID files and running processes!
        """
        # Since this will turn off the system when its complete, 
        # I want to warn the user and give them the chance to opt out if they 
        # chose this option by accident.
        
        ok = raw_input("""
    ******************
    TESTING MY SERVICE
    ******************

    This will TURN OFF my-service after all the tests.

    This should only be done for testing and debugging purposes.

    Are you sure you want to do this? [Y/N]: """
        ).lower()
        
        if ok != 'y':
            print >> sys.stderr, "Aborting..."
            return
            
        print "Writing Lock File..."
        lock()
        print "Verifying lock file..."
        if os.path.exists('/var/lock/subsys/my-service'):
            print "Lock file written..."
        else:
            print >> sys.stderr, "ERROR: Lock file was NOT written"
        
        print "Starting..."
        start()
        # Do stuff to check the start() function     
        #
        # 
        
        # we call status a couple of times so we can test if it's returning the right
        # output under different circumstances
        status()
            
        print "Stopping..."
        stop()
        # Do stuff to check the stop() function     
        #
        # 
            
        print "Removing lock file..."
        unlock()
        
        if os.path.exists('/var/lock/subsys/my-service'):
            print >> sys.stderr, "ERROR: Could not remove lock file"
        else:
            print "Lock file removed successfully"
        
        # one more time to see what it looks like when the service off
        status()


    # Main program switchboard - wrap everything in a try block to
    # ensure the right return code is sent to the shell, and keep things tidy.
    # 
    # @TODO: need to raise custom exception instead of ValueError, and 
    #        handle other exceptions better. 
    #
    # @TODO: put lock/unlock calls inside of start/stop?
    if __name__ == '__main__':
        try:
            # if there's fewer than 2 options on the command line 
            # (sys.argv[0] is the program name)
            if len(sys.argv) == 1:
                raise ValueError;  
                
            action = str(sys.argv[1]).strip().lower()
            
            if action == 'start':
                lock()
                start()
                sys.exit(0)
            elif action == 'stop':
                stop()
                unlock()
                sys.exit(0)
            elif action == 'restart' or action == 'force-reload':
                restart()
                sys.exit(0)
            elif action == 'status':
                OK = status()
                sys.exit(OK)
            elif action == 'test':
                test()
                sys.exit(0)
            else:
                raise ValueError
        
        except (SystemExit):
            # calls to sys.exit() raise this error :(
            pass
        except (ValueError):
            print >> sys.stderr, "Usage: my-service [start|stop|restart|force-reload|status|test]"
            # return 2 for "bad command line option"
            sys.exit(2)
        except:
            # all other exceptions get caught here
            extype, value = sys.exc_info()[:2]
            print >> sys.stderr, "ERROR: %s (%s)" % (extype, value)
            # return 1 for "general error"
            sys.exit(1)

            

I've put this code skeleton into my `google code
repository <http://code.google.com/p/lionfacelemonface/source/browse/trunk/initscript/>`__.
Check there for the latest version as well as a fully unit tested
version.

What the script does, in esscence, is take an action from the command
line, and then call a function that performs that action. Everything is
wrapped in a ``try... except`` block, so that any exceptions are caught,
the user is notified via `standard
error <http://en.wikipedia.org/wiki/Stderr#Standard_error_.28stderr.29>`__
(so if errors appear during boot, they'll get logged somewhere like
``/var/log/messages``), and the appropriate error code is returned.

I intentionally throw a ``ValueError`` if the user provides a bad
option. This is due to the requirement that we must return a different
error code when a bad command line option is supplied (code 2; this is
also a general Unix convention), and to follow the best practice of
gently reminding the user of proper syntax when they make a mistake.

I should probably write a custom exception class instead, but this is
adequate for now.

I had to do a blanket-pass for when ``sys.exit(0)`` is called, since it
raises a ``SystemExit`` exception. I'm not happy about this. I'm not
100% sure, but I believe that this and all the calls to ``sys.exit()``
when the return value should be 0 could be removed, since Python
normally returns 0 upon successful completion of a script (I need to
check up on this).

This script will run as-is. You can install it like this:

::

    $ cd ~
    $ svn co https://lionfacelemonface.googlecode.com/svn/trunk/initscript
    $ cd initscript
    $ sudo cp init_skeleton.py /etc/init.d/my-service
    $ sudo chkconfig --add my-service
    $ sudo chkconfig my-service on

At this point, the service is installed, and will run at all runlevels.
You can verify this by peeking at ``/etc/rc.d``:

::

    $ ls -la /etc/rc.d/rc5.d | grep my-service
    lrwxrwxrwx  1 root root   20 Dec 28 15:05 S01my-service -> ../init.d/my-service

I'm not 100% sure why there isn't a kill script there. I need to look
into that further.

Getting Fancy
-------------

Pretty Status
~~~~~~~~~~~~~

The LSB specs call for a "library" of sorts that contains useful
functions that help simplify init script creation. Most Linux
distributions (or, at least the ones I'm dealing with here) include a
variant, installed at ``/etc/init.d/functions``.

At some point I'd like to emulate that entire library in python (or see
if someone else already has), but there's one bit in there that I really
like, which would make these python-based init scripts look much more
authentic.

When you send a command via ``/sbin/service servicename``, or call the
script using ``/etc/init.d/servicename``, most distributions print a
little colorized ``[  OK  ]`` once a task has completed successfully (or
``[FAILED]`` upon failure). I think its worth the trouble to emulate
that idea.

This is accomplished with a couple of new functions, named after shell
functions I found in ``/etc/init.d/functions`` (on a RHEL5 machine).

To get the cursor movement and colors, we'll use `ANSI escape
codes <http://en.wikipedia.org/wiki/ANSI_escape_code>`__. I've defined
them as variables (using all caps as an homage to the shell script
convention)

::

    # ANSI codes
    MOVE_CURSOR = '33[60G'
    FAILURE_COLOR = '33[1;31m'
    SUCCESS_COLOR = '33[1;32m'
    NO_COLOR = '33[0m'

    def echo_success():
        """
        Port of standard RHEL function, echos pretty colorized "[  OK  ]" after 
        output
        """
        print "%s[  %sOK%s  ]" % (MOVE_CURSOR, SUCCESS_COLOR, NO_COLOR)

    def echo_failure():
        """
        Port of standard RHEL function, echos pretty colorized "[FAILED]" after 
        output
        """
        print "%s[%sFAILED%s]" % (MOVE_CURSOR, FAILURE_COLOR, NO_COLOR)

Here's how they're used:

::

    import sys

    def start():
        print "Starting...",
        # do stuff...
        echo_success()
        
    try:
       start()
    except:
       echo_failure()
       extype, value = sys.exc_info()[:2]
       print >> sys.stderr, "ERROR: %s (%s)" % (extype, value)
       # return 1 for "general error"
       sys.exit(1) 

Essentially, we're using the "don't print a newline" syntax for
``print``, and relying on the ``echo_*`` functions to handle printing
the newlines for us.

If any exception is raised, the code immediately goes to the except
clause, finishing the line with the "FAILED" notice, and then printing
the nature of the error to standard error.

"Real" Unit Testing
~~~~~~~~~~~~~~~~~~~

My first full-blown init script involved mounting AoE LUNs on my SAN. I
had trouble mounting them using the standard ``fstab`` methods (even
with ``_netdev`` specified).

What `Coraid
provided <http://www.coraid.com/site/co-files/FAQ.html#ss5.14>`__ was
fairly lacking, and quite hard for a non-shell expert to really
understand, so I took a cue from a colleague of mine who had done
something similar as a Debian shell script, and wrote my own mounting
and parsing init script.

So I had python functions that were parsing a standin fstab file, the
output of the ``mount`` command and various other shell commands.

This made unit testing problematic. I had to find a way to simulate some
of the shell commands, without actually executing them.

I also needed to test certain exceptions being raised. I didn't (and
still don't) know how to accurately simulate an exception in a doctest.

Then I had trouble getting my doctests to actually run. The usual
``if __name__ == '__main__':`` idiom was already being used by the
"switchboard" for the init script. This meant that the standard way of
invoking the doctest module wouldn't work.

I mucked around a bit and settled on adding another action to the
script, called "unittest". Using the `doctest
API <http://docs.python.org/library/doctest.html>`__, I was able to run
all the doctests, so that worked out well.

When it came to overcoming the other problems, I was able to do so by
running all of my system calls through a central function, I called
``run()``, and setting up some globals to switch on and off the "test
mode" when the unittest action is called.

``run()`` takes several arguments, and works with two global registries
that establish test output and exceptions depending on what function is
calling the ``run()`` function. My unittest action sets up those globals
dynamically when it runs. I don't think its ideal, but it seems to work.

To see it in action, see `aoe-init: A Real-World Example <#aoe-init>`__
below.

aoe-init: A Real-World Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As part of the process of developing the code skeleton above, I wrote my
first init script to mount my AoE SAN.

I'm displaying it here to show how I've done the unit testing. I need to
rework the script to use the skeleton, and work the unit testing bits
into the skeleton, but I think it's a good example of what a
Python-based init script can look like, and I don't mind getting other
pythonista's opinions of how it could be improved.

Keep an eye on my `google code
repository <http://code.google.com/p/lionfacelemonface/source/browse/trunk/initscript/>`__.
The code is there and I'll be tracking my changes as the script is
refactored (it should probably be its own project, but that's an
exercise for another time... but I could of course be persuaded... if
you're interested, drop me a line at lionface dot lemonface at gmail dot
com)

::

    #!/usr/bin/python
    # aoe-init - example init script for ATA over Ethernet storage
    #
    # NOTE: add required aoe mounts to /etc/fstab-aoe
    #
    # Author: Josh Johnson 
    #
    # TODO: support LVM mounts, RAID arrays of etherd devices (may need to do other stuff before mounting)
    # TODO: add "live test" that parses the fstab-aoe, and verifies all the mounts
    # TODO: replace sys.stderr.write with print >> sys.stderr
    # TODO: add "reload" action that refreshes and revalidates the aoe targets (and remounts mounted ones?)
    # 
    # chkconfig: - 99 01
    # description: Mount AoE targets at boot.
    #
    ### BEGIN INIT INFO
    # Provides: aoe-init
    # Required-Start: $network 
    # Required-Stop: 
    # X-UnitedLinux-Should-Start:
    # X-UnitedLinux-Should-Stop:
    # Default-Start:  2 3 5
    # Default-Stop:
    # Short-Description: Mount AoE targets at boot.
    # Description:  Mount AoE targets at boot.
    ### END INIT INFO

    import sys, os, subprocess, re, time

    ####### Settings used for testing purposes ############################
    testing = False
    myfstab = '/etc/fstab-aoe'


    def parse_fstab(path=""):
        """
        Parse the /etc/fstab-aoe file, return a structure.
        
        @TODO: parse options into a list?
        
        >>> mounts = parse_fstab()
        >>> mounts[0]['file-system']
        '/dev/etherd/e99.68'
        >>> mounts[2]['fs-type']
        'ext3'
        >>> mounts[4]['options']
        'defaults,_netdev,noatime,bubba,data=journal'
        """
        
        if not path:
            path = myfstab
        
        fstab = open(path)
        
        data = fstab.readlines()
        
        _fstab = []
            
        for line in data:
            line = line.strip()
            
            # skip comments/empty lines
            if line == '' or line.startswith("#"):
                continue
            
            info = {}
            cols = re.split("\s+", line)
            
            info['file-system'] = cols[0]
            info['mount-point'] = cols[1]
            info['fs-type'] = cols[2]
            info['options'] = cols[3]
            info['dump'] = cols[4]
            info['pass'] = cols[5]
            
            _fstab.append(info)

        fstab.close()
        
        return _fstab

    def run(command, usetest='unknown', bypass_test=False, test_except=False):
        """
        Execute a command and return the output.
        
        If the global testing variable is set, the command isn't executed, just printed to stdout 
        (no newline)
        
        @param command: list, the command and any arguments you want to pass
        @param usetest: string, used in conjunction with the global testing variable, 
                        by the test() function below. Used as a reference for what fake output 
                        you'd like to return.
        @param bypass_test: boolean, if True, still execute the command, even if testing is True
        @param test_except: boolean, set to True if you'd like to use the _except hash to test an exception  
        
        @TODO: should we always strip? maybe add as an option?
        @TODO: should we always split the command?
        
        
        
        >>> run(['uname'], bypass_test=True)
        'Linux'
        >>> run(['uname', '-r'])
        uname -r
        >>> run(['uname', '-r'], 'run', test_except=True)
        Traceback (most recent call last):
        ...
        KeyError
        """
        # little bit of code to help in unit testing
        if testing and not bypass_test:
            print " ".join(command)
            if usetest != 'unknown':
                if test_except:
                    raise _except[usetest]
                    
                return _test[usetest]
            else:
                return
        
        result = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0].strip()
        
        return result
        


    def load(interfaces=['eth1', 'eth0']):
        """
        Load the aoe module.
        
        @TODO: test for module prescence?
        @TODO: set some sort of timeout in the loop
        
        >>> load()
        /sbin/modprobe aoe aoe_iflist="eth1 eth0"
        >>> load(['eth1'])
        /sbin/modprobe aoe aoe_iflist="eth1"
        """
        chk = run(['lsmod'])
        
        if re.search('^aoe', chk, re.MULTILINE):
            print >> sys.stderr, "Module already loaded" 
            return
        
        run(['/sbin/modprobe',  'aoe', 'aoe_iflist="%s"' % ' '.join(interfaces)])
        
        # don't return until it's loaded (/dev/etherd/discover exists)
        
        if not testing:
            print "Waiting for module to come up..."
            while not os.path.exists('/dev/etherd/discover'):
                pass
            print "Module up."
            

    def unload():
        """
        Unload the aoe module
        
        @TODO: set some sort of timeout in the loop
        
        >>> unload()
        /sbin/rmmod aoe
        """
        chk = run(['lsmod'])
        
        if not re.search('^aoe', chk, re.MULTILINE):
            print >> sys.stderr, "Module not loaded" 
            return
        
        run(['/sbin/rmmod', 'aoe'])
        
        # don't return until it's unloaded (/dev/etherd/discover dissapears)
        
        if not testing:
            print "Waiting for module to come down..."
            while os.path.exists('/dev/etherd/discover'):
                pass
            print "Module down."
        

    def mount():
        """
        Mount all of the entries in /etc/fstab-aoe
        
        @TODO: verify mount points/etherd devices?
        
        >>> import sys
        >>> # capture stderr so we can test the exceptions too
        >>> sys.stderr = sys.stdout
        >>> mount()
        mount -t ext3 -o defaults,_netdev,noatime,data=journal /dev/etherd/e99.68 /var/shares/ccbc-admin
        Unable to mount aoe target /dev/etherd/e99.68 to /var/shares/ccbc-admin
        mount -t ext3 -o defaults,_netdev,noatime,data=journal /dev/etherd/e99.130 /var/backup/ccbc-admin
        Unable to mount aoe target /dev/etherd/e99.130 to /var/backup/ccbc-admin
        mount -t ext3 -o defaults,_netdev,noatime,data=journal /dev/etherd/e99.51 /var/shares/patterson-lab
        Unable to mount aoe target /dev/etherd/e99.51 to /var/shares/patterson-lab
        mount -t ext3 -o defaults,_netdev,noatime,data=journal /dev/etherd/e99.131 /var/backup/patterson-lab
        Unable to mount aoe target /dev/etherd/e99.131 to /var/backup/patterson-lab
        mount -t ext3 -o defaults,_netdev,noatime,bubba,data=journal /dev/etherd/e99.52 /var/shares/miller-lab
        Unable to mount aoe target /dev/etherd/e99.52 to /var/shares/miller-lab
        mount -t ext3 -o defaults,_netdev,noatime,data=journal /dev/etherd/e99.132 /var/backup/miller-lab
        Unable to mount aoe target /dev/etherd/e99.132 to /var/backup/miller-lab
        """
        mounts = parse_fstab()
        
        for mount in mounts:
            try:
                command = ['mount', '-t', mount['fs-type'], '-o', mount['options'], mount['file-system'], mount['mount-point']]
                
                #turning on exception testing if testing is True
                run(command, 'mount', test_except=testing)
                
            except OSError:
                sys.stderr.write("Unable to mount aoe target %(file-system)s to %(mount-point)s\n" % mount)
            
            


    def unmount():
        """
        Un-mount all of the entries in /etc/fstab-aoe
        
        @TODO: only unmount mounted entries?
        
        >>> import sys
        >>> # capture stderr so we can test the exceptions too
        >>> sys.stderr = sys.stdout
        >>> unmount()
        umount /dev/etherd/e99.68
        Unable to unmount aoe target /dev/etherd/e99.68 from /var/shares/ccbc-admin
        umount /dev/etherd/e99.130
        Unable to unmount aoe target /dev/etherd/e99.130 from /var/backup/ccbc-admin
        umount /dev/etherd/e99.51
        Unable to unmount aoe target /dev/etherd/e99.51 from /var/shares/patterson-lab
        umount /dev/etherd/e99.131
        Unable to unmount aoe target /dev/etherd/e99.131 from /var/backup/patterson-lab
        umount /dev/etherd/e99.52
        Unable to unmount aoe target /dev/etherd/e99.52 from /var/shares/miller-lab
        umount /dev/etherd/e99.132
        Unable to unmount aoe target /dev/etherd/e99.132 from /var/backup/miller-lab
        """
        mounts = parse_fstab()
        
        for mount in mounts:
            try:
                command = ('umount', mount['file-system'])
                
                run(command, 'unmount', test_except=testing)
                
            except OSError:
                sys.stderr.write("Unable to unmount aoe target %(file-system)s from %(mount-point)s\n" % mount)
            
         

    def lock():
        """
        Create the /var/lock/subsys/aoe-init file
        
        @TODO: catch exceptions
        
        >>> lock()
        >>> import os
        >>> os.path.exists('/var/lock/subsys/aoe-init')
        True
        >>> os.remove('/var/lock/subsys/aoe-init')
        
        """
        open('/var/lock/subsys/aoe-init', 'w').close()

    def unlock():
        """
        Remove the /var/lock/subsys/aoe-init file
        
        @TODO: catch exceptions
        
        >>> lock()
        >>> unlock()
        >>> import os
        >>> os.path.exists('/var/lock/subsys/aoe-init')
        False
        """
        os.remove('/var/lock/subsys/aoe-init')
        

    def aoe_stat():
        """
        Get the current list of available aoe targets
        """
        return run(['/usr/sbin/aoe-stat'], 'aoe_stat')

    def aoe_version():
        """
        Get the current AoE driver and tools versions
        """
        return run(['/usr/sbin/aoe-version'], 'aoe_version')

    def aoe_discover():
        """
        Probe the SAN network for AoE targets
        """
        run(['/usr/sbin/aoe-discover'])
        
        # give aoe-discover a chance to do it's thing
        time.sleep(5)

    def mounted():
        """
        Return any mount entries for mounted AoE targets
        
        @TODO: parse mounts into structure
        
        >>> mounted()
        /bin/mount
        ['/dev/etherd/e99.2 on /media/test type ext3 (rw,_netdev,noatime)']
        """
        mounts = run(['/bin/mount'], 'mounted').split("\n")
        
        aoe_mounts = []
        
        for mount in mounts:
            if "dev/etherd" in mount:
                aoe_mounts.append(mount.strip())
        
        return aoe_mounts

    def status():
        """
        Check for the lock file, call the aoe version command, etc
        
        >>> import sys
        >>> # capture stderr so we can test the error messages
        >>> sys.stderr = sys.stdout
        >>> status()
        Lock file not found. Status uknown
        >>> lock()
        >>> status() #doctest: +NORMALIZE_WHITESPACE
        AoE Version Information:
        /usr/sbin/aoe-version
        
                          aoetools: 30
              installed aoe driver: 73
                running aoe driver: 73
        
        
        Available AoE Targets:
        /usr/sbin/aoe-stat
            e99.2        32.212GB  eth1,eth0 1024  up
        
        Mounted AoE Targets:
        /bin/mount
        /dev/etherd/e99.2 on /media/test type ext3 (rw,_netdev,noatime)
        >>> unlock()
        """
        locked = os.path.exists('/var/lock/subsys/aoe-init')
        
        if not locked:
            sys.stderr.write("WARNING: Lock file not found. Init script may not be functioning properly\n")
        
        print "AoE Version Information:"
        print aoe_version()
        print 
        print "Available AoE Targets:"
        print aoe_stat()
        print
        print "Mounted AoE Targets:"
        
        mounts = mounted()
        
        for mount in mounts:
            print mount
                

    def unittest():
        """
        Run unit tests on this file.
        """
        import tempfile
        import doctest
        
        this_module = __import__(__name__)
        
        tmp = tempfile.NamedTemporaryFile()
        
        this_module.myfstab = tmp.name
        
        tmp.write('''
            # /etc/fstab-aoe: AoE filesystems mount-points   -*-conf-*-
            #
            #                
            #
            #/dev/etherd/e99.0      /mnt/aoe_trial  ext3  defaults,_netdev,noatime,data=journal     1 2
            /dev/etherd/e99.68      /var/shares/ccbc-admin  ext3    defaults,_netdev,noatime,data=journal   1 2
            /dev/etherd/e99.130     /var/backup/ccbc-admin  ext3    defaults,_netdev,noatime,data=journal   1 2
            /dev/etherd/e99.51      /var/shares/patterson-lab       ext3    defaults,_netdev,noatime,data=journal   1 2
            /dev/etherd/e99.131     /var/backup/patterson-lab       ext3    defaults,_netdev,noatime,data=journal   1 2
            /dev/etherd/e99.52      /var/shares/miller-lab  ext3    defaults,_netdev,noatime,bubba,data=journal   1 2
            /dev/etherd/e99.132     /var/backup/miller-lab  ext3    defaults,_netdev,noatime,data=journal   1 2'''
        )
        
        tmp.seek(0)
        
        # test output for parsing functions
        _test = {}
        _test['mounted'] = """
        /dev/mapper/Primary-Root on / type ext3 (rw)
        proc on /proc type proc (rw)
        sysfs on /sys type sysfs (rw)
        devpts on /dev/pts type devpts (rw,gid=5,mode=620)
        /dev/mapper/Primary-Home on /home type ext3 (rw)
        /dev/mapper/Primary-Temp on /tmp type ext3 (rw)
        /dev/mapper/Primary-Logs on /var/log type ext3 (rw)
        /dev/md0 on /boot type ext3 (rw)
        tmpfs on /dev/shm type tmpfs (rw)
        none on /proc/sys/fs/binfmt_misc type binfmt_misc (rw)
        sunrpc on /var/lib/nfs/rpc_pipefs type rpc_pipefs (rw)
        configfs on /sys/kernel/config type configfs (rw)
        ocfs2_dlmfs on /dlm type ocfs2_dlmfs (rw)
        /dev/drbd1 on /vm type ocfs2 (rw,_netdev,noatime,heartbeat=local)
        /dev/etherd/e99.2 on /media/test type ext3 (rw,_netdev,noatime)
        """
        
        _test['load'] = ""
        _test['unload'] = ""
        _test['mount'] = ""
        _test['unmount'] = ""
        _test['lock'] = ""
        _test['aoe_stat'] = "\te99.2        32.212GB  eth1,eth0 1024  up"
        _test['aoe_version'] = """
                      aoetools: 30
          installed aoe driver: 73
            running aoe driver: 73
        """
        _test['unknown'] = ""
        
        # exceptions to test
        _except = {}
        _except['mount'] = OSError
        _except['unmount'] = OSError
        _except['run'] = KeyError
        
        this_module.testing = True
        this_module._test = _test
        this_module._except = _except
        
        print "Running unit tests for this init script..."
        
        doctest.testmod(this_module)
        
        print 
        print "No output means the tests were successful. For more detail, call `aoe-init test -v`"
        
        tmp.close()


    def test():
        """
        Do a sanity check to make sure we can load the module, parse the /etc/fstab-aoe
        file, mount the contents, then run the shutdown procedure.
        
        @TODO: unit test for this?
        """
        
        ok = raw_input("\n*******************\nTESTING AOE SETUP\n*******************\n\nThis will turn off the aoe driver in your system.\n\nThis should only be done for testing and debugging purposes.\n\nAre you sure you want to do this? [Y/N]: ").lower()
        
        if ok != 'y':
            sys.stderr.write("Aborting...\n")
            return
        
        # check if there's an /etc/fstab-aoe
        if not os.path.exists('/etc/fstab-aoe'):
            sys.stderr.write("ERROR: No /etc/fstab-aoe file found\n")
            return
            
        # try parsing it and check the entries
        fstab = parse_fstab('/etc/fstab-aoe')
        
        if len(fstab) == 0:
            sys.stderr.write("ERROR: /etc/fstab-aoe doesn't contain any un-commented entries\n")
            return
            
        
        unload()
        load()
        aoe_discover()
        
        for _mount in fstab:
            # check for common errors
            if not os.path.exists(_mount['mount-point']):
                sys.stderr.write("WARNING: %s does not exist\n" % (_mount['mount-point']))
                
            if not os.path.exists(_mount['file-system']):
                sys.stderr.write("WARNING: %s is not an existing device\n" % (_mount['file-system']))
        
        
        mount()
        lock()
        status()
        unmount()
        unload()
        status()
        
        print "Testing /var/lock/subsys lock file..." 
        
        if not os.path.exists("/var/lock/subsys/aoe-init"):
            print >> sys.stderr, "ERROR: Lock file was NOT written"
        else:
            print "Lock file written."
            
        unlock()
        
        if os.path.exists("/var/lock/subsys/aoe-init"):
            print >> sys.stderr, "ERROR: Lock file was NOT deleted"
        else:
            print "Lock file deleted."    
        

    def refresh():
        """
        Attempt to reload and re-validate all of the aoe mounts on the system.
        
        @TODO: actually write this :)
        """
        

    # Main program switchboard
    if __name__ == '__main__':
        try:
            if len(sys.argv) == 0:
                raise ValueError;
                
            action = str(sys.argv[1]).strip().lower()
            
            if action == 'start':
                load()
                aoe_discover()
                lock()
                mount()
            elif action == 'stop':
                unmount()
                unload()
                unlock()
            elif action == 'status':
                status()
            elif action == 'unittest':
                unittest()
            elif action == 'test':
                test() 
            elif action == 'refresh':
                print "Not currently implemented."
            else:
                raise ValueError
            
             
        except (ValueError, IndexError):
            sys.stderr.write("Usage: aoe-init [start|stop|status|refresh|test|unittest]\n")
        

Moving Forward
--------------

There are a handful of items on my TODO list that I'd like to document
here

-  I haven't actually written anything that *controls* a process; I've
   only written init scripts that load kernel modules, mount
   filesystems, and kick off other init scripts.

   I'd like to delve into process control and monitoring more in the
   future.

-  I've ported two very small and simple pieces of common functionality
   from the standard init script function libraries. I'd like to expand
   that. (this will become more necessary as I proceed with the last
   item)

-  Verification could be handled better. I don't *really* know what the
   state of a process is; in the ``aoe-init`` script, I checked things
   like the output of ``aoe-stat``, a tool that comes with the AoE
   driver, and the standard ``mount`` command.

-  My unit testing setup is kind of convoluted. I really don't like the
   level of complexity in my ``run()`` function. I need to collect the
   testing bits into something more concrete and transparent.

-  The more I think about it, the more I feel I need to figure out how
   to put my init scripts into proper eggs. As things get more complex,
   I may need external dependencies, and I'd like to let the
   `setuptools <http://pypi.python.org/pypi/setuptools>`__
   infrastructure handle that for me.

   Also, an egg package would afford me lots of leeway for creating
   tests. I could move most of the doctests into a central file and move
   the testing code (the ``unittest`` action) into a setup.py action.

-  The code skeleton doesn't handle a common use case: if you call the
   stop action when the serivce isn't running, the whole script fails.
   This is due to the lock file not existing since the ``lock()``
   function never wrote it, since the ``start()`` function hadn't been
   called.

   I'm not sure exactly how to handle this. I see a couple of
   possiblites:

   #. Check for the file's existence, and if it's not there, just
      quietly don't do anything.
   #. Check for the file's existence, and if it's not there, don't call
      ``unlock()``, but still proceed with shutdown procedures.
   #. Continue failing.

   I think that in a real process-control application, you'd need to do
   more than just look for a lock file. You'd check the status of the
   process itself by getting the PID and looking for a running process,
   then proceed in a application-specific manner.

   So you may want to fail if the process isn't running, or maybe there
   is still some cleanup that you need to do even if was never started.

   We also have to take into consideration that the process may have
   actually died as opposed to never been started.

   So generally speaking, I think the skeleton is OK the way it is, but
   I may "fix" this just so the end use isn't caught off guard by it.
