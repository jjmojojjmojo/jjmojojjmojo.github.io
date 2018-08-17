Raspberry Pi Build Environment In No Time At All
################################################
:date: 2015-04-18 18:07
:author: lionfacelemonface
:category: arch, linux, raspberrypi, tutorials, ubuntu
:slug: raspberry-pi-build-environment-in-no-time-at-all
:status: draft

Leveraging `PRoot <http://proot.me/>`__ and `qemu <www.qemu.org>`__,
it's easy to configure Raspberry Pi's, build and install packages,
without the need to do so on physical hardware. It's especially nice if
you have to work with many disk images at once, create specialized
distributions, reset passwords, or install/customize
applications that aren't yet in the official repositories.

I've recently dug in to building apps and doing fun things with the
`Raspberry Pi <https://www.raspberrypi.org/>`__. With the recent release
of the `Raspberry Pi 2 <https://www.raspberrypi.org/blog/page/6/#raspberry-pi-2-on-sale>`__,
its an even more exciting platform. I've documented what I've been using
to make my workflow more productive.

Table Of Contents
-----------------

.. contents::

Setup
-----

We'll use a Linux machine. Below are setup instructions for
`Ubuntu <http://www.ubuntu.com/>`__ and
`Arch <https://www.archlinux.org/>`__. I prefer Arch for desktop and
personal work, I use `Debian <https://www.debian.org/>`__ or Ubuntu for
production deployments.

Arch Linux is a great "tinkerer's" distribution - if you haven't used it
before it's worth checking out. It's `great on the Raspberry Pi <http://archlinuxarm.org/>`__.

Debian and Ubuntu have some differences, but share the same base and use
the same package management system
(`apt <http://en.wikipedia.org/wiki/Advanced_Packaging_Tool>`__). I've
included instructions for Ubuntu in particular, since it's the most
similar to `Raspbian <http://www.raspbian.org/>`__, the
default Raspberry Pi operating system, and folks may be more familiar
with that environment.

Generally speaking, you'll need the following things:

-  A physical computer or virtual machine running some version of Linux
   (setup instructions are provided for the latest Arch and Ubuntu, but
   any Linux should work).
-  `Installation files for the Raspberry Pi. <https://www.raspberrypi.org/downloads/>`__
-  SD cards `suitable for whatever Raspberry Pi you have <https://www.raspberrypi.org/documentation/installation/sd-cards.md>`__.
   We'll learn how to work with raw disk images and how to copy disk images to SD cards.
-  `QEMU <http://www.qemu.org>`__, an emulator system, and it's `ARM processor <http://en.wikipedia.org/wiki/ARM_architecture>`__ support (the Raspberry Pi uses an ARM processor).
-  `PRoot <http://proot.me/>`__ - a convenience tool that makes it
   easy to mount a "foreign" filesystem and run commands inside of it
   without booting.
-  A way to create disk images, and mount them like physical devices.

Once the packages are installed, the commands and processes for building
and working with Raspberry Pi boot disks are the same.

.. note::
   We assume you have `sudo <http://en.wikipedia.org/wiki/Sudo>`__ installed and configured.

Virtual Machine Notes
~~~~~~~~~~~~~~~~~~~~~

If you're using an Apple (Mac OS X) computer or Windows, the easiest way
to work with Linux systems is via virtualization.
`VirtualBox <https://www.virtualbox.org/>`__ is available for most
platforms and is easy to work with.

The virtualbox documentation can walk you through the `installation of VirtualBox and creating your first virtual machine <https://www.virtualbox.org/manual/ch01.html>`__.

When working with an SD card, you'll might want to follow instructions for "`Access to entire physical hard disk <https://www.virtualbox.org/manual/ch09.html#rawdisk>`__" to make
the card accessible to the virtual machine. As an alternative, you could
use a USB SD card reader, and `usb pass-thru <https://www.virtualbox.org/manual/ch03.html#settings-usb>`__ to
present not the disk to the virtual machine, but the entire USB device,
and let the virtual machine deal with mounting it.

Both of these approaches can be (very) error prone, but provide the most
"native" way of working.

Instead I'd recommend installing `guest additions <https://www.virtualbox.org/manual/ch04.html>`__. With guest
additions installed in your virtual machine, you can use the `shared folders feature <https://www.virtualbox.org/manual/ch04.html#sharedfolders>`__
of VirtualBox. This makes it easy to copy disk images created in your
virtual machine to your host machine, and then you can use the standard
instructions for
`Windows <https://www.raspberrypi.org/documentation/installation/installing-images/windows.md>`__
and `Mac OS <https://www.raspberrypi.org/documentation/installation/installing-images/mac.md>`__ to
copy the disks images to your SD cards.

Advanced Usage Note
~~~~~~~~~~~~~~~~~~~
Personally, my usual method of operations with
VirtualBox VMs is to set up `Samba <https://www.samba.org/>`__ in my
virtual machine and share a folder over a `host-only network <https://www.virtualbox.org/manual/ch06.html#network_hostonly>`__
(or I'll use `bridged networking <https://www.virtualbox.org/manual/ch06.html#network_bridged>`__ so
I can connect to it from any machine on my LAN) - I'd consider this a
more "advanced" approach but I've had more consistent results for
day-to-day work than using guest additions or mounting host disks.
However, for the simple task of just copying disk images back and forth
to the virtual machine, the shared folders feature should suffice.

Arch Linux
~~~~~~~~~~

We'll use `pacman <https://wiki.archlinux.org/index.php/Pacman>`__ and
`wget <https://www.gnu.org/software/wget/>`__ to procure and install
most of the tools we need:

.. code-block:: shell-session
   
   $ sudo pacman -S dosfstools wget qemu unzip pv
   $ wget http://static.proot.me/proot-x86\_64
   $ chmod +x proot-x86\_64
   $ sudo mv proot-x86\_64 /usr/local/bin/proot
   



First, we install the following packages:

dosfstools
    Gives us the ability to create FAT filesystems, required for making
    a disk bootable on the RaspberryPi.
wget
    General purpose file grabber - used for downloading installation
    files and PRoot
qemu
    QEMU emulator - allows us to run RaspberryPi executables
unzip
    Decompresses ZIP archives.
pv
    Pipeline middleware that shows a progress bar (we'll be using it to
    make copying disk images with ``dd`` a little easier for the
    impatient)

Then we download PRoot, make the file executable, and copy it to a
common location for global executable that everyone on a machine can
access, ``/usr/local/bin``. This location is just a suggestion - to
follow along with the examples in this article, you just need to put the
``proot`` executable somewhere on your
`$PATH <http://en.wikipedia.org/wiki/PATH_%28variable%29>`__.

Finally, we'll use an `AUR <https://aur.archlinux.org/>`__ package to
obtain the ``kpartx`` tool.

kpartx wraps a handful of tasks required for creating loopback devices
into a single action.

If you haven't used the AUR before, `check out the documentation first <https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_package>`__
for an overview of the process, and to install prerequisites.

.. code-block:: shell-session
   
   $ wget
  https://aur.archlinux.org/packages/mu/multipath-tools/multipath-tools.tar.gz
   $ tar -zxvf multipath-tools.tar.gz
   $ cd multipath-tools
   $ makepkg
   $ sudo pacman -U sudo pacman -U multipath-tools-\*.pkg.tar.xz
   



Ubuntu
~~~~~~

Ubuntu Desktop comes with most of the tools we need (in particular,
``wget``, the ability to mount dos file systems, and ``unzip``). As
such, the process of getting set up for using PRoot is a bit simpler,
compared to Arch.

Ubuntu uses
`apt-get <http://en.wikipedia.org/wiki/Advanced_Packaging_Tool>`__ for
package installation.

.. code-block:: shell-session
   
   $ sudo apt-get install qemu kpartx pv
   $ wget http://static.proot.me/proot-x86\_64
   $ chmod +x proot-x86\_64
   $ sudo mv proot-x86\_64 /usr/local/bin/proot
   



First, we install the following packages:

qemu
    QEMU emulator – allows us to run RaspberryPi executables
kpartx
    Helper tool that wraps a handful of tasks required for creating
    loopback devices into a single action.
pv
    Pipeline middleware that shows a progress bar (we’ll be using it to
    make copying disk images with dd a little easier for the impatient)

Then, we install PRoot by downloading the binary from
`proot.me <http://proot.me>`__, making it executable, and putting it
somewhere on our `$PATH <http://en.wikipedia.org/wiki/PATH_%28variable%29>`__,
``/usr/local/bin``, making it available to all users on the system. This
location is merely a suggestion, but putting the ``proot`` executable
somewhere on your $PATH will make it easier to follow along with the
examples below.

Working With A Disk Image
-------------------------

A disk (in the Raspberry Pi's case, we're talking about an SD card) is
just an arrangement of blocks for data storage. On top of those blocks
is a description of how files are represented in those blocks, or a
*filesystem* (for more detail, see the Wikipedia articles on `Disk Storage <http://en.wikipedia.org/wiki/Disk_storage>`__ and `File System <http://en.wikipedia.org/wiki/File_system>`__).

Disks can exist in the physical world, or can be represented by a
special file, called a disk image. We can download pre-made images with
Raspbian already installed from the official `Raspberry Pi downloads page <https://www.raspberrypi.org/downloads/>`__.

.. code-block:: shell-session
   
   $ wget http://downloads.raspberrypi.org/raspbian\_latest -O
  rasbian\_latest.img.zip
   $ unzip rasbian\_latest.img.zip
   Archive: raspbian\_latest.zip
   inflating: 2015-02-16-raspbian-wheezy.img
   



Take note of the name of the img file - it will vary depending on the
current release of Raspbian at the time.

At this point we have a disk image we can mount by creating a loopback
device. Once we have it mounted, we can use QEMU and PRoot to run
commands within it without fully booting it.

We'll use kpartx to set up a loopback device for each partition in the
disk image:

.. code-block:: shell-session
   
   $ sudo kpartx -a -v 2015-02-16-raspbian-wheezy.img
   add map loop0p1 (254:0): 0 114688 linear /dev/loop0 8192
   add map loop0p2 (254:1): 0 6277120 linear /dev/loop0 122880
   



The ``-a`` command line switch tells kpartx to \ *create *\ new loopback
devices. The ``-v`` switch asks kpartx to be more \ *verbose* and print
out what it's doing.

We can do a dry-run and inspect the disk image using the ``-l`` switch:

.. code-block:: shell-session
   
   $ sudo kpartx -l 2015-02-16-raspbian-wheezy.img
   loop0p1 : 0 114688 /dev/loop0 8192
   loop0p2 : 0 6277120 /dev/loop0 122880
   loop deleted : /dev/loop0
   



We can see the partitions to be sure, using ``fdisk -l``

.. code-block:: shell-session
   
   $ sudo fdisk -l /dev/loop0

   Disk /dev/loop0: 3.1 GiB, 3276800000 bytes, 6400000 sectors
   Units: sectors of 1 \* 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disklabel type: dos
   Disk identifier: 0x0009bf4f

   Device Boot Start End Sectors Size Id Type
   /dev/loop0p1 8192 122879 114688 56M c W95 FAT32 (LBA)
   /dev/loop0p2 122880 6399999 6277120 3G 83 Linux
   



We can also see them using ``lsblk``:

.. code-block:: shell-session
   
   $ lsblk
   NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
   sda 8:0 0 14.9G 0 disk
   └─sda1 8:1 0 14.9G 0 part /
   sdc 8:32 0 29.8G 0 disk
   └─sdc1 8:33 0 29.8G 0 part /run/media/jj/STEALTH
   loop0 7:0 0 3.1G 0 loop
   ├─loop0p1 254:0 0 56M 0 part
   └─loop0p2 254:1 0 3G 0 part
   



Generally speaking, the first, smaller partition will be the boot
partition, and the others will hold data. It's typical with RaspberryPi
distributions to use a simple 2-partition scheme like this.

The new partitions will end up in ``/dev/mapper``:

.. code-block:: shell-session
   
   $ ls /dev/mapper
   control loop0p1 loop0p2
   



Now we can mount our partitions. We'll first make a couple of
descriptive directories for mount points:

.. code-block:: shell-session
   
   $ mkdir raspbian-boot raspbian-root
   $ sudo mount /dev/mapper/loop0p1 raspbian-boot
   $ sudo mount /dev/mapper/loop0p2 raspbian-root
   



At this point we can go to the next section where we will run PRoot and
start doing things "inside" the disk image.

Working With An Existing Disk
-----------------------------

We can use PRoot with an existing disk (SD card) as well. The first step
is to insert the disk into your computer. Your operating system will
likely automatically boot it. We also need to find out which device the
disk is registered as.

``lsblk`` can answer both questions for us:

.. code-block:: shell-session
   
   $ lsblk
   NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
   sda 8:0 0 14.9G 0 disk
   └─sda1 8:1 0 14.9G 0 part /
   sdb 8:16 1 14.9G 0 disk
   ├─sdb1 8:17 1 56M 0 part /run/media/jj/boot
   └─sdb2 8:18 1 3G 0 part
  /run/media/jj/f24a4949-f4b2-4cad-a780-a138695079ec
   sdc 8:32 0 29.8G 0 disk
   └─sdc1 8:33 0 29.8G 0 part /run/media/jj/STEALTH
   



On my system, the SD card I inserted (a Raspbian disk I pulled out of a
Raspberry Pi) came up as ``/dev/sdb``. It has two paritions, ``sdb1``
and ``sdb2``. Both partitions were automatically mounted, to
``/run/media/jj/boot`` and
``/run/media/jj/f24a4949-f4b2-4cad-a780-a138695079ec``, respectively.

Typically, the first, smaller partition will be the boot partition. To
verify this, we'll again use ``fdisk -l``:

.. code-block:: shell-session
   
   $ sudo fdisk -l /dev/sdb
   Disk /dev/sdb: 14.9 GiB, 16021192704 bytes, 31291392 sectors
   Units: sectors of 1 \* 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disklabel type: dos
   Disk identifier: 0x0009bf4f

   Device Boot Start End Sectors Size Id Type
   /dev/sdb1 8192 122879 114688 56M c W95 FAT32 (LBA)
   /dev/sdb2 122880 6399999 6277120 3G 83 Linux
   



Here we see that ``/dev/sdb1`` is 56 megabytes in size, and is of type
"W95 FAT32 (LBA)". This is typically indicative of a RasbperryPi boot
partition, so ``/dev/sdb1`` is our boot partition, and ``/dev/sdb2`` is
our root partition.

We can use the existing mounts that the operating system set up
automatically for us, if we want, but it's a bit easier to un-mount the
partitions and mount them somewhere more descriptive, like
``raspbian-boot`` and ``raspbian-boot``:

.. code-block:: shell-session
   
   $ sudo umount /dev/sdb1 /dev/sdb2
   $ mkdir -p raspbian-boot raspbian-root
   $ sudo mount /dev/sdb1 raspbian-boot
   $ sudo mount /dev/sdb2 raspbian-root
   



.. note::
   The ``-p`` switch to ``mkdir`` causes ``mkdir`` to ignore
   already-exsiting directories. We've added it here in case you were
   following along in the previous section and already have these
   directories handy.

A call to ``lsblk`` will confirm that we've mounted things as we
expected:

.. code-block:: shell-session
   
   $ lsblk
   NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
   sda 8:0 0 14.9G 0 disk
   └─sda1 8:1 0 14.9G 0 part /
   sdb 8:16 1 14.9G 0 disk
   ├─sdb1 8:17 1 56M 0 part /run/media/jj/STEALTH/raspbian-boot
   └─sdb2 8:18 1 3G 0 part /run/media/jj/STEALTH/raspbian-root
   sdc 8:32 0 29.8G 0 disk
   └─sdc1 8:33 0 29.8G 0 part /run/media/jj/STEALTH
   



Now we can proceed to the next section, and run the same PRoot command
to configure, compile and/or install things - but this time we'll be
working directly on the SD card instead of inside of a disk image.

Basic Configuration/Package Installation
----------------------------------------

Now that we've got either a disk image or a physical disk mounted, we
can run commands within those filesystems using PRoot.

.. note::
   
   The following command line switches worked for me, but took some experimentation to figure out. Please take some time to read `the PRoot documentation <http://proot.me/>`__ so you understand exactly what the switches mean.
   

We can run any command directly (like say, ``apt-get``) but it's useful
to be able to "log in" to the disk image (run a shell), and then perform
our tasks:

.. code-block:: shell-session
   
   $ sudo proot -q qemu-arm -S raspbian-root -b raspbian-boot:/boot
  /bin/bash
   



This mode of PRoot forces the root user inside of the disk image. The
``-q`` switch wraps every command in the ``qemu-arm`` emulator program,
making it possible to run code compiled for the RaspberryPi's ARM
processor. The ``-S`` parameter sets the directory that will be the
"root" - essentially that means that ``raspbian-root`` will map to
``/``. ``-S`` also fakes the root user (id 0), and adds some protections
for us in the event we've mixed in files from our host system that we
don't want the disk image code to modify. ``-b`` splices in additional
directories - we add the ``/boot`` partition, since that's where new
kernel images and other boot-related stuff gets installed. This isn't
entirely necessary, but its useful for system upgrades and making
changes to boot settings. Finally, we tell PRoot which command to run,
in this case, ``/bin/bash``, the BASH shell.

Now that we're "in" the disk image, we can update and install new
packages.

Since root is not a "normal" user in the default Rasbian installation,
the path needs to be adjusted:

.. code-block:: shell-session
   
   # export PATH=$PATH:/usr/sbin:/sbin:/bin:/usr/local/sbin
   



Now we can do the update/upgrade, and install any additional packages we
might want (for example, the samba file sharing server):

.. code-block:: shell-session
   
   # apt-get update
   # apt-get upgrade
   # apt-get install samba
   



Check out the man page for apt-get for full details (type
``man apt-get`` at a shell prompt).

You will likely see a lot of warnings and possibly errors when
installing packages - these can usually be ignored, but make note of
them - there may be some environmental tweaks that need to be made.

We can do almost anything in the PRoot environment that we could do
logged into a running Raspberry Pi.

We can edit config.txt and change settings (for an explanation of the
settings, see `the documentation <https://www.raspberrypi.org/documentation/configuration/config-txt.md>`__):

.. code-block:: shell-session
   
   # vi /boot/config.txt
   



We can add a new user:

.. code-block:: shell-session
   
   # adduser jj
   Adding user `jj' ...
   Adding new group `jj' (1004) ...
   Adding new user `jj' (1001) with group `jj' ...
   Creating home directory `/home/jj' ...
   Copying files from `/etc/skel' ...
   Enter new UNIX password:
   Retype new UNIX password:
   passwd: password updated successfully
   Changing the user information for jj
   Enter the new value, or press ENTER for the default
   Full Name []: Josh Johnson
   Room Number []:
   Work Phone []:
   Home Phone []:
   Other []:
   



We can grant a user sudo privileges (the default sudo configuration
allows anyone in the ``sudo`` group to run commands as root via sudo):

.. code-block:: shell-session
   
   # usermod -a -G sudo jj
   # groups jj
   jj : jj sudo
   



You can reset someone's password, or change the password of the default
``pi`` user:

.. code-block:: shell-session
   
   # passwd pi
   Enter new UNIX password:
   Retype new UNIX password:
   passwd: password updated successfully
   



The possibilities here are endless, with a few exceptions:

-  Running code that relies on the GPIO pins or drivers loaded into the
   kernel will not work.
-  Configuring devices (like, say, a wifi adapter) may work, but device
   information will likely be wrong.
-  Testing startup/shutdown scripts - since we're not booting the disk
   image, these scripts aren't run.

Compiling For The RPi
---------------------

Raspbian comes with most of the tools we'll need (in particular, the
``build-essential`` package). Lets build and install the `nginx web server <http://nginx.org/>`__ - a relatively easy to build package.

If you've never compiled software on Linux before, most (but not
all!) source code packages are provided as tarballs, and include some
scripts that help you build the software in what's known as the
"configure, make, make install" (or CMMI) procedure.

.. note::
   For a great explanation (with examples you can follow to
   build your own CMMI package), `George Brocklehurst <https://twitter.com/georgebrock>`__ wrote an excellent
   article explaining the details behind CMMI called "`The magic behind configure, make, make install <https://robots.thoughtbot.com/the-magic-behind-configure-make-make-install>`__".

First we'll need to obtain the nginx tarball:

.. code-block:: shell-session
   
   # wget http://nginx.org/download/nginx-1.7.12.tar.gz
   # tar -zxvf nginx-1.7.12.tar.gz
   



Next we'll look for a README or INSTALL file, to check for any extra
build dependencies:

.. code-block:: shell-session
   
   # cd nginx-1.7.12
   # ls -l
   total 660
   -rw-r--r-- 1 jj indiecity 249016 Apr 7 15:35 CHANGES
   -rw-r--r-- 1 jj indiecity 378885 Apr 7 15:35 CHANGES.ru
   -rw-r--r-- 1 jj indiecity 1397 Apr 7 15:35 LICENSE
   -rw-r--r-- 1 root root 46 Apr 18 10:21 Makefile
   -rw-r--r-- 1 jj indiecity 49 Apr 7 15:35 README
   drwxr-xr-x 6 jj indiecity 4096 Apr 18 10:21 auto
   drwxr-xr-x 2 jj indiecity 4096 Apr 18 10:21 conf
   -rwxr-xr-x 1 jj indiecity 2478 Apr 7 15:35 configure
   drwxr-xr-x 4 jj indiecity 4096 Apr 18 10:21 contrib
   drwxr-xr-x 2 jj indiecity 4096 Apr 18 10:21 html
   drwxr-xr-x 2 jj indiecity 4096 Apr 18 10:21 man
   drwxr-xr-x 2 root root 4096 Apr 18 10:23 objs
   drwxr-xr-x 8 jj indiecity 4096 Apr 18 10:21 src
   # view README
   



We'll note that, helpfully (*cue eye roll*) that nginx has put into the README:

.. code-block:: shell-session
   
   
   Documentation is available at http://nginx.org
   
   

A more `direct link <http://nginx.org/en/docs/configure.html>`__ gives
us a little more useful information. Scanning this, there aren't any
obvious dependencies or features we want to add/enable, so we can
proceed.

We can also find out which options are available by running
``./configure --help``.

.. note::
   There are several configuration options that control where
   files are put when the compiled code is installed - they may be of use,
   in particular the standard ``--PREFIX``. This can help segregate
   multiple versions of the same application on a system, for example if
   you need to install a newer/older version and already have one installed
   via the apt package. It is also useful to build self-contained directory
   structures that you can easily copy from one system to another.

Run ``./configure``, note any warnings or errors. There may be some
modules or other things ``not found`` - that's typically OK, but can
help explain why an eventual error happened toward the end of the
configure script or during compilation:

.. code-block:: shell-session
   
   # cd nginx-1.7.12
   # ./configure
   ...
   checking for PCRE library ... not found
   checking for PCRE library in /usr/local/ ... not found
   checking for PCRE library in /usr/include/pcre/ ... not found
   checking for PCRE library in /usr/pkg/ ... not found
   checking for PCRE library in /opt/local/ ... not found
   ...

   ./configure: error: the HTTP rewrite module requires the PCRE library.
   You can either disable the module by using
  --without-http\_rewrite\_module
   option, or install the PCRE library into the system, or build the
  PCRE library
   statically from the source with nginx by using
  --with-pcre=&lt;path&gt; option.
   



Whoa, we ran into a problem! For our use case (just showing off how to
do a CMMI build in a PRoot environment) we probably don't need the
rewrite module, so we can re-run ``./configure`` with the
``--without-http_rewrite_module`` switch.

However, it's useful to understand how to track down dependencies like
this, and rewriting is a pretty killer feature of any http server, so
lets install the dependency.

The configure script mentions the "PCRE library". PCRE stands for "Perl
Compatible Regular Expressions". `Perl <http://www.perl.org/>`__ is a
classical systems language that has hard-core text processing
capabilities. It's particularly known for its `regular expression <http://en.wikipedia.org/wiki/Regular_expression>`__ support
and syntax. The Perl regular expression syntax is so useful in fact,
that `some folks built a library allowing other programmers to use it without having to use Perl itself <http://www.pcre.org/>`__.

.. note::
   
   This information can be found by using your favorite search engine!
   

There are two ways libraries like PCRE are installed. The first, and
easiest, is that a system package will be available with the library
pre-compiled and ready to go. The second will require the same steps
we're following to install nginx - download a tarball, extract, and
configure, make, make install.

To find a package, you can use ``apt-cache search`` or
``aptitude search``.

I prefer ``aptitude``, since it will tell us what packages are already
installed:

.. code-block:: shell-session
   
   # aptitude search pcre
   v apertium-pcre2 -
   p cl-ppcre - Portable Regular Express Library for Common Lisp
   p clisp-module-pcre - clisp module that adds libpcre support
   p gambas3-gb-pcre - Gambas regexp component
   p haskell-pcre-light-doc - transitional dummy package
   p libghc-pcre-light-dev - Haskell library for Perl 5-compatible
  regular expressions
   v libghc-pcre-light-dev-0.4-4f534 -
   p libghc-pcre-light-doc - library documentation for pcre-light
   p libghc-pcre-light-prof - pcre-light library with profiling enabled
   v libghc-pcre-light-prof-0.4-4f534 -
   p libghc-regex-pcre-dev - Perl-compatible regular expressions
   v libghc-regex-pcre-dev-0.94.2-49128 -
   p libghc-regex-pcre-doc - Perl-compatible regular expressions;
  documentation
   p libghc-regex-pcre-prof - Perl-compatible regular expressions;
  profiling libraries
   v libghc-regex-pcre-prof-0.94.2-49128 -
   p libghc6-pcre-light-dev - transitional dummy package
   p libghc6-pcre-light-doc - transitional dummy package
   p libghc6-pcre-light-prof - transitional dummy package
   p liblua5.1-rex-pcre-dev - Transitional package for lua-rex-pcre-dev
   p liblua5.1-rex-pcre0 - Transitional package for lua-rex-pcre
   p libpcre++-dev - C++ wrapper class for pcre (development)
   p libpcre++0 - C++ wrapper class for pcre (runtime)
   p libpcre-ocaml - OCaml bindings for PCRE (runtime)
   p libpcre-ocaml-dev - OCaml bindings for PCRE (Perl Compatible
  Regular Expression)
   v libpcre-ocaml-dev-werc3 -
   v libpcre-ocaml-werc3 -
   i libpcre3 - Perl 5 Compatible Regular Expression Library - runtime
  files
   p libpcre3-dbg - Perl 5 Compatible Regular Expression Library - debug
  symbols
   p libpcre3-dev - Perl 5 Compatible Regular Expression Library -
  development f
   p libpcrecpp0 - Perl 5 Compatible Regular Expression Library - C++
  runtime f
   p lua-rex-pcre - Perl regular expressions library for the Lua
  language
   p lua-rex-pcre-dev - PCRE development files for the Lua language
   v lua5.1-rex-pcre -
   v lua5.1-rex-pcre-dev -
   v lua5.2-rex-pcre -
   v lua5.2-rex-pcre-dev -
   p pcregrep - grep utility that uses perl 5 compatible regexes.
   p pike7.8-pcre - PCRE module for Pike
   p postfix-pcre - PCRE map support for Postfix
   



See ``man aptitude`` for full details, but the gist is that ``p`` means
the package is available but not installed, ``v`` is a virtual package
that points to other packages, and ``i`` means the package is installed.

What we want is a package with header files and modules we can compile
against - these are usually named ``lib[SOMETHING]-dev``.

Scanning the list, we see a package named ``libpcre3-dev`` - this is
probably what we want, we can find out by installing it:

.. code-block:: shell-session
   
   # apt-get install libpcre3-dev
   



Now we can re-run ``./configure`` and see if it works:

.. code-block:: shell-session
   
   # ./configure
   ...
   checking for PCRE library ... found
   ...
   Configuration summary
   + using system PCRE library
   + OpenSSL library is not used
   + using builtin md5 code
   + sha1 library is not found
   + using system zlib library

   nginx path prefix: "/usr/local/nginx"
   nginx binary file: "/usr/local/nginx/sbin/nginx"
   nginx configuration prefix: "/usr/local/nginx/conf"
   nginx configuration file: "/usr/local/nginx/conf/nginx.conf"
   nginx pid file: "/usr/local/nginx/logs/nginx.pid"
   nginx error log file: "/usr/local/nginx/logs/error.log"
   nginx http access log file: "/usr/local/nginx/logs/access.log"
   nginx http client request body temporary files: "client\_body\_temp"
   nginx http proxy temporary files: "proxy\_temp"
   nginx http fastcgi temporary files: "fastcgi\_temp"
   nginx http uwsgi temporary files: "uwsgi\_temp"
   nginx http scgi temporary files: "scgi\_temp"
   



The library was found, the error is gone, and so now we can proceed with
compilation.

To build nginx, we simply run ``make``:

.. code-block:: shell-session
   
   # make
   



If all goes well, then you can isntall it:

.. code-block:: shell-session
   
   # make install
   



This same basic process can be used to build custom applications written
in C/C++, to build applications that aren't yet in the package
repository, or build applications with specific features or
optimizations enabled that the standard packages might not have.

Using Apt To Install Build Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One more useful thing that apt-get can do for us: it can install
the *build* dependencies for any given package in the repository. This
allows us to get most, if not all, potentially missing dependencies to
build a known application.

We could have started off with our nginx exploration by first installing
it's build dependencies:

.. code-block:: shell-session
   
   # apt-get build-dep nginx
   



This won't solve every dependency issue, but it's a useful tool in
getting all of your ducks in a row for building, especially for more
complex things like desktop applications.

Be careful with build-dep - it can bring in a *lot* of things, some
you may not really need. In our case it's not really a problem, but be
aware of space limitations.

Umount and Clean Up
-------------------

Once we've gotten our disk image configured as we like, we need to
un-mount it.

First, we need to exit the bash shell we started with PRoot, then we'll
call ``sync`` to ensure all data is flushed to any disks:

.. code-block:: shell-session
   
   # exit
   $ sync
   



Now we can un-mount the partitions (the command is the same whether
we're using a disk image or an SD card):

.. code-block:: shell-session
   
   $ sudo umount raspbian-root rasbian-boot
   



We can double-check that the disk is no longer mounted by calling
``mount`` without any additional parameters, or using ``lsblk``

.. code-block:: shell-session
   
   $ mount
   ...
   



With ``lsblk``, we'll still see the disks (or loopback devices) present,
but not mounted:

.. code-block:: shell-session
   
   $ lsblk
   NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
   sda 8:0 0 14.9G 0 disk
   └─sda1 8:1 0 14.9G 0 part /
   sdc 8:32 0 29.8G 0 disk
   └─sdc1 8:33 0 29.8G 0 part /run/media/jj/STEALTH
   loop0 7:0 0 3.1G 0 loop
   ├─loop0p1 254:0 0 56M 0 part
   └─loop0p2 254:1 0 3G 0 part
   



If we're using a disk image, we'll want to destroy the loopback devices.
This is accomplished with ``kpartx -d``:

.. code-block:: shell-session
   
   $ sudo kpartx -d 2015-02-16-raspbian-wheezy.img
   



We can verify that it's gone using ``lsblk`` again:

.. code-block:: shell-session
   
   $ lsblk
   sda 8:0 0 14.9G 0 disk
   └─sda1 8:1 0 14.9G 0 part /
   sdc 8:32 0 29.8G 0 disk
   └─sdc1 8:33 0 29.8G 0 part /run/media/jj/STEALTH
   



At this point we can write the disk image to an SD card, or eject the SD
card and insert it into a Raspberry Pi.

Writing a Disk Image to an SD Card
----------------------------------

We'll use the ``dd`` command, which writes raw blocks of data from one
block device to another, to copy the disk image we made into an SD card.

.. note::
   
   The SD card you use will be COMPLETELY erased. Proceed with caution.
   

First, insert the SD card into your computer (or card reader, etc).
Depending on your system, it may be automatically mounted. We can find
out the device name and if its mounted using ``lsblk``:

.. code-block:: shell-session
   
   $ lsblk
   NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
   sda 8:0 0 14.9G 0 disk
   └─sda1 8:1 0 14.9G 0 part /
   sdb 8:16 1 14.9G 0 disk
   ├─sdb1 8:17 1 114.3M 0 part
   ├─sdb2 8:18 1 1K 0 part
   └─sdb3 8:19 1 32M 0 part /run/media/jj/SETTINGS
   sdc 8:32 0 29.8G 0 disk
   └─sdc1 8:33 0 29.8G 0 part /run/media/jj/STEALTH
   



We can see the new disk came up as ``sdb``. It has three partitions,
``sdb1``, ``sdb2``, and ``sdb3``. Looking at the ``MOUNTPOINT`` column,
we can tell that my operating system auto-mounted ``sdb3`` into the
``/run/media/jj/SETTINGS`` directory.

.. note::
   The partition layout may vary depending on what was on the SD
   card before you inserted it. My SD card had a fresh copy of
   `NOOBS <https://www.raspberrypi.org/introducing-noobs/>`__ that hadn't
   yet installed an OS.

We can double-check that ``sdb`` is the right disk with ``fdisk``:

.. code-block:: shell-session
   
   $ sudo fdisk -l /dev/sdb
   Disk /dev/sdb: 14.9 GiB, 16021192704 bytes, 31291392 sectors
   Units: sectors of 1 \* 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disklabel type: dos
   Disk identifier: 0x000cb53d

   Device Boot Start End Sectors Size Id Type
   /dev/sdb1 8192 242187 233996 114.3M e W95 FAT16 (LBA)
   /dev/sdb2 245760 31225855 30980096 14.8G 85 Linux extended
   /dev/sdb3 31225856 31291391 65536 32M 83 Linux
   



``fdisk`` tells us that this is a 16GB drive. The exact amount cited by
some drive manufacturers is not in "real" gigabytes, an exponent of
2[`\* <#gb>`__\ ] but in billions of bytes - note the byte count:
16,021,192,704.

We can see the three partitions, and what format they are in. The small
`FAT <http://en.wikipedia.org/wiki/File_Allocation_Table>`__ filesystem
is a good indication that this is a bootable Raspberry Pi disk.

With a fresh SD card, the call to ``fdisk`` may look more like this:

.. code-block:: shell-session
   
   Disk /dev/sdb: 14.9 GiB, 16021192704 bytes, 31291392 sectors
   Units: sectors of 1 \* 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disklabel type: dos
   Disk identifier: 0x00000000

   Device Boot Start End Sectors Size Id Type
   /dev/sdb1 8192 31291391 31283200 14.9G c W95 FAT32 (LBA)
   



Most SD cards are pre-formatted with a single partition containing a
`FAT32 <http://en.wikipedia.org/wiki/File_Allocation_Table#FAT32>`__
filesystem.

It's important to be able to differentiate between your system drives
and the target for copying over your disk image - if you point ``dd`` at
the wrong place, you can destroy important things, like your operating
system!

Now that we're sure that ``/dev/sdb`` is our SD card, we can proceed.

Since ``lsblk`` indicated that at least one of the partitions was
mounted (``sdb3``), we will fist need to un-mount it:

.. code-block:: shell-session
   
   $ sudo umount /dev/sdb3
   



Now we can verify it's indeed not mounted:

.. code-block:: shell-session
   
   $ lsblk
   NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
   sda 8:0 0 14.9G 0 disk
   └─sda1 8:1 0 14.9G 0 part /
   sdb 8:16 1 14.9G 0 disk
   ├─sdb1 8:17 1 114.3M 0 part
   ├─sdb2 8:18 1 1K 0 part
   └─sdb3 8:19 1 32M 0 part
   sdc 8:32 0 29.8G 0 disk
   └─sdc1 8:33 0 29.8G 0 part /run/media/jj/STEALTH
   



And copy the disk image:

.. code-block:: shell-session
   
   $ sudo dd if=2015-02-16-raspbian-wheezy.img of=/dev/sdb bs=4M
   781+1 records in
   781+1 records out
   3276800000 bytes (3.3 GB) copied, 318.934 s, 10.3 MB/s
   



This will take some time, and ``dd`` gives no output until it's
finished. Be patient.

``dd`` has a fairly simple interface. The ``if`` option indicates the
*in file*, or the disk (or disk image in our case) that is being copied.
The ``of`` option sets the *out file*, or the disk to write to. ``bs``
sets the *block size*, which indicates how big of a piece of data to
write at a time.

The ``bs`` value can be tweaked to get faster or more reliable
performance in various situations - we're using ``4M`` (four megabytes)
as `recommended by raspberrypi.org <https://www.raspberrypi.org/documentation/installation/installing-images/linux.md>`__.
The larger the value, the faster ``dd`` will run, but there are physical
limits to what your system can handle, so it's best to stick with the
recommended value.

So ``dd`` gives us no output until it's completed. This is kind of an
annoying thing about ``dd`` `but it can be remedied <http://askubuntu.com/questions/215505/how-do-you-monitor-the-progress-of-dd>`__.
The easiest way is to install a tool called \ ``pv``, and split the
command - ``pv`` acts as an intermediary between two commands and
displays a progress bar as it moves along. ``dd`` can read and write
data to a pipe
(`details <http://en.wikipedia.org/wiki/Pipeline_%28Unix%29>`__). So we
can use two ``dd`` commands, put ``pv`` in the middle, and get a nice
progress bar.

Here's the same copy as before, but using ``pv``:

.. note::
   Here we're using ``sh -c`` to wrap the command pipeline in
   quotes. This allows us to provide the entire pipeline as a single unit.
   If we didn't, the shell would interpret the first pipe in the pipeline
   as part of the call to sudo, and not what we want to run as root.

.. code-block:: shell-session
   
   $ ls -l 2015-02-16-raspbian-wheezy.img
   -rw-r--r-- 1 jj jj 3276800000 Apr 18 07:58
  2015-02-16-raspbian-wheezy.img
   $ sudo sh -c "dd if=2015-02-16-raspbian-wheezy.img bs=4M \   pv
  --size=3276800000 \   dd of=/dev/sdb"
   613MiB 0:02:31 [4.22MiB/s] [===========> ] 19% ETA 0:10:04
   # exit
   



We pass ``pv`` a ``--size`` argument to give it an idea of how big the
file is, so it can provide accurate progress. We found out the size of
our disk image using ``ls -l.``, which shows the size of the file
in *bytes*.

If we run ``lsblk`` again, we'll see the different partition arrangement
now on ``sdb``:

.. code-block:: shell-session
   
   $ lsblk
   NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
   sda 8:0 0 14.9G 0 disk
   └─sda1 8:1 0 14.9G 0 part /
   sdb 8:16 1 14.9G 0 disk
   ├─sdb1 8:17 1 56M 0 part
   └─sdb2 8:18 1 3G 0 part
   sdc 8:32 0 29.8G 0 disk
   └─sdc1 8:33 0 29.8G 0 part /run/media/jj/STEALTH
   



``fdisk -l`` gives a bit more detail:

.. code-block:: shell-session
   
   $ sudo fdisk -l /dev/sdb
   Disk /dev/sdb: 14.9 GiB, 16021192704 bytes, 31291392 sectors
   Units: sectors of 1 \* 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disklabel type: dos
   Disk identifier: 0x0009bf4f

   Device Boot Start End Sectors Size Id Type
   /dev/sdb1 8192 122879 114688 56M c W95 FAT32 (LBA)
   /dev/sdb2 122880 6399999 6277120 3G 83 Linux
   



Now we can ``sync`` the disks:

.. code-block:: shell-session
   
   $ sync
   



At this point we have an SD card we can put into a Raspberry Pi and
boot.

[\*] *(1GB = 1 byte \* 1024 (kilobyte) \* 1024 (megabyte) \* 1024, or
1,073,741,824 bytes)*

Extra Credit: Making our own disk image
---------------------------------------

Some distributions, such as Arch, don't distribute disk images, but
instead distribute tarballs of files. They let you set up the disk
however you want, then copy the files over to install the operating
system.

We can create our own disk images using ``fallocate``, and then use
``fdisk`` or ```parted`` <http://www.gnu.org/software/parted/>`__ (or if
you prefer a GUI, `gparted <http://gparted.org/>`__) to partition the
disk.

We'll create a disk image for the latest `Arch Linux ARM distribution for the Raspberry Pi 2 <http://archlinuxarm.org/platforms/armv7/broadcom/raspberry-pi-2>`__.

.. note::
   You must create the disk image file on a compatible
   filesystem, such as ext4, for this to work. This is the default system
   disk filesystem for most modern Linux distributions, including Arch and
   Ubuntu, so for most people this isn't a problem. The implication is that
   this will not work on, say, an external hard drive formatted in an
   incompatible format, such as FAT32.

First we'll create an 8 gigabyte empty disk image:

.. code-block:: shell-session
   
   $ fallocate -l 8G arch-latest-rpi2.img
   



We'll use ``fdisk`` to partition the disk. We need two partitions. The
first will be 100 megabytes, formatted as
`FAT32 <http://en.wikipedia.org/wiki/File_Allocation_Table#FAT32>`__.
We'll need to set the partition's `*system id* <http://en.wikipedia.org/wiki/Partition_type>`__ to correspond to
FAT32 with `LBA <http://en.wikipedia.org/wiki/Logical_block_addressing>`__ so that the Raspberry Pi's BIOS knows how to read it.

..note::
   
   I've had trouble finding documentation as to exactly why FAT + LBA is required, the assumption is it has something to do with how the ARM processor loads the operating system in the earliest boot stages; if anyone knows more detail or can point me to the documentation about this, it would be greatly appreciated!
   

The offset for the partition will be 2048 blocks - this is the default
that ``fdisk`` will suggest (and what the Arch installation instructions
tell us to do).

.. note::
   This seems to work well- however, there is some confusion
   about partition alignment. The Raspbian disk images use a 8192 block
   offset, and there is a lot of information available explaining how a bad
   alignment can cause quicker SD card degradation and hurt write
   performance. I'm still trying to figure out the best way to address
   this, this is another area where community help would be appreciated :)
   Here are a few links that dig into the issue:
   http://wiki.laptop.org/go/How_to_Damage_a_FLASH_Storage_Device,
   http://thunk.org/tytso/blog/2009/02/20/aligning-filesystems-to-an-ssds-erase-block-size/,
   http://3gfp.com/wp/2014/07/formatting-sd-cards-for-speed-and-lifetime/.

The second partition will be ext4, and use the rest of the the available
disk space.

We'll start fdisk and get the initial prompt. No changes will be saved
until we instruct ``fdisk`` to do so:

.. code-block:: shell-session
   
   $ fdisk arch-latest-rpi2.img
   Device contains neither a valid DOS partition table, nor Sun, SGI or
  OSF disklabel
   Building a new DOS disklabel with disk identifier 0x152a22d4.
   Changes will remain in memory only, until you decide to write them.
   After that, of course, the previous content won't be recoverable.

Warning: invalid flag 0x0000 of partition table 4 will be corrected by
w(rite)

   Command (m for help):
   



Most of the information here is just telling us that this is a block
device with no partitions. If you need help, as indicated, you can type
``m``:

.. code-block:: shell-session
   
   Command (m for help): m
   Command action
   a toggle a bootable flag
   b edit bsd disklabel
   c toggle the dos compatibility flag
   d delete a partition
   l list known partition types
   m print this menu
   n add a new partition
   o create a new empty DOS partition table
   p print the partition table
   q quit without saving changes
   s create a new empty Sun disklabel
   t change a partition's system id
   u change display/entry units
   v verify the partition table
   w write table to disk and exit
   x extra functionality (experts only)
   



First, we need to create a new disk *partition table*. This is done by
entering ``o``:

.. code-block:: shell-session
   
   Command (m for help): o
   Building a new DOS disklabel with disk identifier 0xa8e8538a.
   Changes will remain in memory only, until you decide to write them.
   After that, of course, the previous content won't be recoverable.

   Warning: invalid flag 0x0000 of partition table 4 will be corrected by
  w(rite)
   



Next, we'll create our first *primary* partition, the boot partition, at
2048 blocks offset, 100MB in size.

.. code-block:: shell-session
   
   Command (m for help): n
   Partition type:
   p primary (0 primary, 0 extended, 4 free)
   e extended
   Select (default p): p
   Partition number (1-4, default 1): 1
   First sector (2048-16777215, default 2048): 2048
   Last sector, +sectors or +size{K,M,G} (2048-16777215, default
  16777215): +100M
   



By using the relative number ``+100M``, we save ourselves some trouble
of having to do math to figure out how many sectors we need.

We can see what we have so far, by using the ``p`` command:

.. code-block:: shell-session
   
   Command (m for help): p

   Disk arch-latest-rpi2.img: 8589 MB, 8589934592 bytes
   255 heads, 63 sectors/track, 1044 cylinders, total 16777216 sectors
   Units = sectors of 1 \* 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disk identifier: 0xa8e8538a

   Device Boot Start End Blocks Id System
   arch-latest-rpi2.img1 2048 206847 102400 83 Linux
   



Next, we need to set the partition type (system id) by entering ``t``:

.. code-block:: shell-session
   
   Command (m for help): t
   Selected partition 1
   Hex code (type L to list codes): L

   0 Empty 24 NEC DOS 81 Minix / old Lin bf Solaris
   1 FAT12 27 Hidden NTFS Win 82 Linux swap / So c1 DRDOS/sec (FAT-
   2 XENIX root 39 Plan 9 83 Linux c4 DRDOS/sec (FAT-
   3 XENIX usr 3c PartitionMagic 84 OS/2 hidden C: c6 DRDOS/sec (FAT-
   4 FAT16 <32M 40 Venix 80286 85 Linux extended c7 Syrinx
   5 Extended 41 PPC PReP Boot 86 NTFS volume set da Non-FS data
   6 FAT16 42 SFS 87 NTFS volume set db CP/M / CTOS / .
   7 HPFS/NTFS/exFAT 4d QNX4.x 88 Linux plaintext de Dell Utility
   8 AIX 4e QNX4.x 2nd part 8e Linux LVM df BootIt
   9 AIX bootable 4f QNX4.x 3rd part 93 Amoeba e1 DOS access
   a OS/2 Boot Manag 50 OnTrack DM 94 Amoeba BBT e3 DOS R/O
   b W95 FAT32 51 OnTrack DM6 Aux 9f BSD/OS e4 SpeedStor
   c W95 FAT32 (LBA) 52 CP/M a0 IBM Thinkpad hi eb BeOS fs
   e W95 FAT16 (LBA) 53 OnTrack DM6 Aux a5 FreeBSD ee GPT
   f W95 Ext'd (LBA) 54 OnTrackDM6 a6 OpenBSD ef EFI (FAT-12/16/
   10 OPUS 55 EZ-Drive a7 NeXTSTEP f0 Linux/PA-RISC b
   11 Hidden FAT12 56 Golden Bow a8 Darwin UFS f1 SpeedStor
   12 Compaq diagnost 5c Priam Edisk a9 NetBSD f4 SpeedStor
   14 Hidden FAT16 <3 61 SpeedStor ab Darwin boot f2 DOS secondary
   16 Hidden FAT16 63 GNU HURD or Sys af HFS / HFS+ fb VMware VMFS
   17 Hidden HPFS/NTF 64 Novell Netware b7 BSDI fs fc VMware VMKCORE
   18 AST SmartSleep 65 Novell Netware b8 BSDI swap fd Linux raid auto
   1b Hidden W95 FAT3 70 DiskSecure Mult bb Boot Wizard hid fe LANstep
   1c Hidden W95 FAT3 75 PC/IX be Solaris boot ff BBT
   1e Hidden W95 FAT1 80 Old Minix
   Hex code (type L to list codes): c
   Changed system type of partition 1 to c (W95 FAT32 (LBA))
   



After the ``t`` command, we opted to enter ``L`` to see the list of
possible codes. We then see that ``W95 FAT32 (LBA)`` corresponds to the
code ``c``.

Now we can make our second primary partition for data storage, utilizing
the rest of the disk. We again use the ``n`` command:

.. code-block:: shell-session
   
   Command (m for help): n
   Partition type:
   p primary (1 primary, 0 extended, 3 free)
   e extended
   Select (default p): p
   Partition number (1-4, default 2): 2
   First sector (206848-16777215, default 206848):
   Using default value 206848
   Last sector, +sectors or +size{K,M,G} (206848-16777215, default
  16777215):
   Using default value 16777215
   



We accepted the defaults for all of the prompts.

Now, entering ``p`` again, we can see the state of the partition table:

.. code-block:: shell-session
   
   Command (m for help): p

   Disk arch-latest-rpi2.img: 8589 MB, 8589934592 bytes
   255 heads, 63 sectors/track, 1044 cylinders, total 16777216 sectors
   Units = sectors of 1 \* 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disk identifier: 0xa8e8538a

   Device Boot Start End Blocks Id System
   arch-latest-rpi2.img1 2048 206847 102400 c W95 FAT32 (LBA)
   arch-latest-rpi2.img2 206848 16777215 8285184 83 Linux
   



Now we can write out the table (``w``), which will exit ``fdisk``:

.. code-block:: shell-session
   
   Command (m for help): w
   The partition table has been altered!

   WARNING: If you have created or modified any DOS 6.x
   partitions, please see the fdisk manual page for additional
   information.
   Syncing disks.
   



Now we need to format the partitions. We'll use ``kpartx`` to create
block devices for us that we can format:

.. code-block:: shell-session
   
   $ sudo kpartx -av arch-latest-rpi2.img
   add map loop0p1 (252:0): 0 204800 linear /dev/loop0 2048
   add map loop0p2 (252:1): 0 16570368 linear /dev/loop0 206848
   



As we saw earilier, the devices will show up in ``/dev/mapper``, as
``/dev/mapper/loop0p1`` and ``/dev/mapper/loop0p2``.

First we'll format the boot partition ``loop0p1``, as :

.. code-block:: shell-session
   
   $ sudo mkfs.vfat /dev/mapper/loop0p1
   mkfs.fat 3.0.26 (2014-03-07)
   unable to get drive geometry, using default 255/63
   



Next the data partition, in ext4 format:

.. code-block:: shell-session
   
   $ sudo mkfs.ext4 /dev/mapper/loop0p2
   mke2fs 1.42.9 (4-Feb-2014)
   Discarding device blocks: done
   Filesystem label=
   OS type: Linux
   Block size=4096 (log=2)
   Fragment size=4096 (log=2)
   Stride=0 blocks, Stripe width=0 blocks
   518144 inodes, 2071296 blocks
   103564 blocks (5.00%) reserved for the super user
   First data block=0
   Maximum filesystem blocks=2122317824
   64 block groups
   32768 blocks per group, 32768 fragments per group
   8096 inodes per group
   Superblock backups stored on blocks:
   32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632

   Allocating group tables: done
   Writing inode tables: done
   Creating journal (32768 blocks): done
   Writing superblocks and filesystem accounting information: done
   



At this point we just need to mount the new filesystems, download the
installation tarball and use ``tar`` to extract and copy the files:

First we'll grab the installation files:

.. code-block:: shell-session
   
   $ wget http://archlinuxarm.org/os/ArchLinuxARM-rpi-2-latest.tar.gz
   



   Next we'll mount the new filesystems:
.. code-block:: shell-session
   
   $ mkdir arch-root arch-boot
   $ sudo mount /dev/mapper/loop0p1 arch-boot
   $ sudo mount /dev/mapper/loop0p2 arch-root
   



And finally populate the disk image with the system files, and move the
``boot`` directory to the boot partition:

.. code-block:: shell-session
   
   $ sudo tar -xpf ArchLinuxARM-rpi-2-latest.tar.gz -C arch-root
   $ sync
   $ sudo mv arch-root/boot/\* arch-boot/
   



We're using a few somewhat less common parameters for ``tar``. Typically
we'll use ``-xvf`` to tell ``tar`` to extract (``-x``), be verbose
(``-v``) and specify the file (``-f``). We've added the ``-p`` switch to
preserve permissions. This is especially important with system files.

The ``-C`` switch tells ``tar`` to change to the ``arch-root`` directory
before extraction, effectively extracting the files directly to the root
filesystem.

*You may see some warnings about extended header keywords, these can be
ignored.*

Now we just need to clean up (unmount, remove the loopback devs):

.. code-block:: shell-session
   
   $ sudo umount arch-root arch-boot
   $ sudo kpartx -d arch-latest-rpi2.img
   



Now we've got our own Arch disk image we can distribute, or copy onto SD
cards. We can also mount it on the loopback and use PRoot to further
configure it, as we did above with Raspbian.

Where To Go From Here
---------------------

With this basic workflow, we can do all sorts of interesting things. A
few ideas:

-  Distribute disk images pre-configured with applications we created.
-  Pre-configure images and SD cards for use in classrooms, meetups,
   demos, etc.
-  Set up a `cron <http://en.wikipedia.org/wiki/Cron>`__ job that runs
   nightly and creates a disk image with the latest packages.
-  Build our own packages (either just create tarballs or use a tool
   like `FPM <https://github.com/jordansissel/fpm>`__ and build deb
   packages) for drivers and other software and save other folks the
   hassle of doing this themselves.
-  Create rudimentary disk duplication setups for putting one image on a
   bunch of SD cards.
-  Fix broken installs.
-  Construct build and testing systems; integrate with tools like
   `Jenkins <https://jenkins-ci.org/>`__.

So there we go - now you can customize the Raspberry Pi operating system
with impunity, on your favorite workstation or laptop machine. If you
have any questions, corrections, or suggestions for ways to streamline
the process, please leave a comment!
