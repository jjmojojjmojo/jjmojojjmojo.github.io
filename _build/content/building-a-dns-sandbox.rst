Building A DNS Sandbox
######################
:date: 2013-12-26 13:53
:author: lionfacelemonface
:category: Uncategorized
:slug: building-a-dns-sandbox
:status: published

I'm developing some automation around DNS. Its imperative that I don't
break anything that might impact any users. This post documents the
process I went through to build a DNS sandbox, and serves as a
crash-course in DNS, which is, like most technology that's been around
since the dawn of time, a lot simpler than it seems at first glance.

Use Case
========

When a new machine is brought up, I need to register it with my internal
DNS server. The DNS server doesn't allow remote updating, and there's no
DHCP server in play (for the record, I'm bringing up machines in AWS). I
have access to the machine via SSH, so I can edit the zone files
directly. As SOP, we use `hostdb <http://code.google.com/p/hostdb/>`__
and a git repository. This works really well for manual updates, but
it's a bit clunky to automate, and has one fatal flaw: there can be
parity between what's in DNS and what's in the git repo. My hope is to
eliminate this by using the DNS server as the single source of truth,
using other mechanisms for auditing and change-management.

So the point of the DNS sandbox is to make testing/debugging of hostdb
easier and to facilitate rapid development of new tools.

.. warning::
    
    Please be aware that this setup is designed strictly for experimentation
    and testing - it's not secure, or terribly useful outside of *basic* DNS
    functionality. Please take the time to really understand what it takes
    to run a DNS server before you try to set something like this up outside
    of a laboratory setting.
    


Coming Soon
===========

There are a lot of features of DNS that this setup doesn't take into
account. I'm planning on following up this post as I add the following
to my sandbox setup (suggestions for other things are welcome!)

-  Remote updates (being able to speak DNS directly to the server from a
   script)
-  Chrooting the bind installation for security.
-  DNS Security (DNSSEC) - makes remote updates secure.
-  Slaves - DNS can be configured so that when one server is updated,
   the changes propagate to *n* number of servers.

Server Setup
============

I started with stock Ubuntu 12.04 server instance.

I installed bind9 using apt, and created a couple of directories for log
and zone files.

.. code-block:: console
   :linenos: none
   
   $ sudo apt-get install bind9
   $ sudo mkdir -p /var/log/named
   $ sudo chown bind:bind /var/log/named
   $ sudo mkdir /etc/bind/zones

Zone Files
==========

Basics
------

See: http://www.zytrax.com/books/dns/ch8

-  Zone files have a header section called the SOA
-  Fully-qualified domain names end with a period (e.g. my.domain.com.),
   subdomains relative to an FDQN do not (e.g. my, www).
-  Zone files have an *origin* - a base added to every name in the file.
   The origin is defined using the $ORIGIN directive (see:
   http://www.zytrax.com/books/dns/ch8/#directives)
-  The @ symbol is used as a shortcut for $ORIGIN.
-  Each zone file is referenced in the named.conf file (see
   `Configuration <#configuration>`__ below for details)
-  The name of the file itself is immaterial - there are many standards
   in the wild - I'm opting to keep them consistent with the name of the
   zone in named.conf.
-  Zone files have a *serial number*, which consists of the current date
   and an increment number. Example: 20131226000 (YYYYMMDDXXX). This
   number must be incremented every time you make a change to a zone
   file, or bind will ignore the changes.
-  Comments start with a semi-colon (;) and run to the end of the line.

DNS lookups can happen in two directions: *forward* and *reverse*.
Forward lookups resolve a doman name to an IP address (``my.domain.com``
-> ``192.168.0.1``). Reverse lookups resolve an IP address to a domain
name (``192.168.0.1`` -> ``my.domain.name``). Each type of lookup is
controlled from a separate zone file, with different types of records.

See http://www.zytrax.com/books/dns/ch8/#types for details about the
different types of records. This post only deals with **SOA**, **NS**,
**A**, **CNAME** and **PTR** records.

Note that reverse lookup is not required for a functioning DNS setup,
but is recommended.

Forward Lookup
--------------

Filename:
    ``/etc/bind/zones/example.test``
Reference:
    http://www.zytrax.com/books/dns/ch8/

Our domain name is *example.test*.

| [code language="text"]
|  $ORIGIN example.test.
|  $TTL 1h

| @ IN SOA ns.example.test. hostmaster.example.test. (
|  20131226000 ; serial number
|  1d ; refresh
|  2h ; update retry
|  4w ; expiry
|  1h ; minimum
|  )

@ NS ns

| ns A 127.0.0.1
|  box1 A 192.168.0.1
|  alt CNAME box1

[/code]

.. raw:: html

   <ul>
   <li>

Line 1 sets the origin. All entries will be a subdomain of example.test.
You can put whatever you want in this stanza, but keep it consistent in
the other areas.

.. raw:: html

   </li>
   <li>

Line 2 sets the Time To Live for records in this zone.

.. raw:: html

   </li>
   <li>

Lines 4-10 are the
`SOA <http://www.zytrax.com/books/dns/ch8/soa.html>`__.

.. raw:: html

   </li>
   <li>

On line 5, We use @ to stand in for the $ORIGIN directive defined on
line 1. We specifify the authoritative server (``ns.example.test.``),
which we will define in an A record later. Finally, we specify the
e-mail address of a person responsible for this zone, replacing the at
symbol (@) with a period.

.. raw:: html

   </li>
   <li>

Line 5 contains the serial number. This will need to be incremented
every time we make a change. In this example, I'm starting with the
current date and 000, so we'll get 999 updates before we have to
increment the date.

.. raw:: html

   </li>
   <li>

Line 12 is a requirement of Bind - we must specify at least one NS
record for our DNS server. The @ symbol is used again here to avoid
typing the origin again. The hostname for the NS record is ``ns``, which
means ``ns.example.test``, defined in an A record on line 14.

.. raw:: html

   </li>
   <li>

Line 14 defines our DNS server for the NS record on line 12. We're using
localhost here to point back to the default setup we got from using the
ubuntu packages.

.. raw:: html

   </li>
   <li>

Line 15 is an example of another A record, for a box named
``box1.example.test``. Its IP address is ``192.168.0.1``. Note that the
actual IP addresses here do not need to be routable to the DNS server;
all it's doing is translating a hostname to an IP address. For testing
purposes, this can be anything. Just be aware that reverse lookups are
scoped to a given address range, so things will need to be consistent
across the two zones.

.. raw:: html

   </li>
   <li>

Finally on line 16, we have an example of a CNAME record. This aliases
the name ``alt.example.test`` to ``box1.example.test``, and ultimately
resolves to ``192.168.0.1``.

.. raw:: html

   </li>

Reverse Lookup
--------------

Filename:
    ``/etc/bind/zones/0.168.192.in-addr.arpa``
Reference:
    http://www.zytrax.com/books/dns/ch3/

We're setting up reverse lookups for the 192.168.0.x subnet (CIDR
192.168.0.0/24).

| [code language="text"]
|  $ORIGIN 0.168.192.in-addr.arpa.
|  $TTL 1h

| @ IN SOA ns.example.test hostmaster.example.test (
|  20131226000 ; serial number
|  1d ; refresh
|  2h ; update retry
|  4w ; expiry
|  1h ; minimum
|  )

| IN NS ns.example.test.
|  1 IN PTR box1.example.test
|  [/code]

-  Lines 1-10 are the SOA, and are formatted the exact same way as in
   our forward zone file.

   Note that the ``$ORIGIN`` is now ``0.168.192.in-addr.arpa.``. The
   ``in-addr.arpa`` domain is special; used for reverse lookups. The
   numbers before the top level domain are simply the subnet octets,
   reversed (``192.168.0`` becomes ``0.168.192``).

   .. raw:: html

      <p>

   Remember, this serves as shorthand for defining the entry records
   below the SOA.

-  Line 12 is the required NS record, pointing at the one that we set up
   an A record for in the forward zone file.
-  Finally, line 13 is a typical PTR record. It associates
   ``192.168.0.1`` with ``box1.example.test``.

Configuration
=============

In the default ubuntu setup, local configuration is handled in
``/etc/bind/named.conf.local`` (this is just simply included into
``/etc/bind/named.conf``).

See http://www.zytrax.com/books/dns/ch7/ for details about the
``named.conf`` format and what the directives mean.

| [code language="text"]
|  zone "example.test." {
|  type master;
|  file "/etc/bind/zones/example.test";
|  allow-update { none; };
|  };

| zone "0.168.192.in-addr.arpa." {
|  type master;
|  file "/etc/bind/zones/0.168.192.in-addr.arpa";
|  allow-update { none; };
|  };

| logging{
|  channel simple\_log {
|  file "/var/log/named/bind.log" versions 3 size 5m;
|  severity debug;
|  print-time yes;
|  print-severity yes;
|  print-category yes;
|  };
|  category default{
|  simple\_log;
|  };
|  };
|  [/code]

-  Lines 1-5 set up our forward zone "example.test.". Note that
   ``allow-update`` is set to ``none``. This simplifies our
   configuration and prevents updates to this zone from other servers.
-  Lines 7-11 set up the reverse zone "0.168.192.in-addr.arpa.".
-  Lines 13-24 set up simple (and verbose) logging to
   ``/var/log/named/bind.log``. See
   http://www.zytrax.com/books/dns/ch7/logging.html for details about
   the setting here.

Testing
=======

Configuration Syntax Check
--------------------------

We can use the ``named-checkzone`` utility to verify our zone file
syntax before reloading the configuration.

You specify the name of the zone and then the filename (the ``-k fail``
parameter causes it to return a failed return code when an error is
found, useful for automated scripts):

::

    $ named-checkzone -k fail example.test /etc/bind/zones/example.test
    zone example.test/IN: loaded serial 2951356816
    OK

In the case of a reverse zone file:

::

    $ named-checkzone -k fail 0.168.192.in-addr.arpa /etc/bind/zones/0.168.192.in-addr.arpa
    zone 0.168.192.in-addr.arpa/IN: loaded serial 2951356817
    OK

Reloading Config
----------------

Configuraiton can be reloaded with the ``rndc reload`` command.

::

    $ sudo rndc reload

It's helpful to run ``tail -f /var/log/named/bind.log`` in another
terminal window during testing.

Testing DNS Queries
-------------------

The definitive tool is ``dig``. ``nslookup`` is also useful for basic
queries.

With both tools, its possible to specify a specific DNS server to query.
In this case, it's assumed that we're logged in to the sandbox DNS
server, so we'll use 127.0.0.1 for the server to query.

With dig
~~~~~~~~

Note: remove the ``+short`` parameter from the end of the query to get
more info.

Forward Lookup
^^^^^^^^^^^^^^

The A record:

::

    $ dig @127.0.0.1 box1.example.test +short
    192.168.0.1

The CNAME:

::

    $ dig @127.0.0.1 alt.example.test +short
    192.168.0.1

Reverse Lookup
^^^^^^^^^^^^^^

::

    $ dig @127.0.0.1 -x 192.168.0.1 +short
    box1.example.test.0.168.192.in-addr.arpa.

With nslookup
~~~~~~~~~~~~~

Forward Lookup
^^^^^^^^^^^^^^

The A record:

::

    $ nslookup box1.example.test 127.0.0.1
    Server:     127.0.0.1
    Address:    127.0.0.1#53

    Name:   box1.example.test
    Address: 192.168.0.1

The CNAME:

::

    $ nslookup alt.example.test 127.0.0.1
    Server:     127.0.0.1
    Address:    127.0.0.1#53

    alt.example.test    canonical name = box1.example.test.
    Name:   box1.example.test
    Address: 192.168.0.1

Reverse Lookup
^^^^^^^^^^^^^^

::

    $ nslookup 192.168.0.1 127.0.0.1
    Server:     127.0.0.1
    Address:    127.0.0.1#53

    1.0.168.192.in-addr.arpa    name = box1.example.test.0.168.192.in-addr.arpa.

Using Your Sandbox
==================

| Now that the DNS sandbox is built and working correctly, you may want
  to add it
|  to your list of DNS servers.

| This process will vary depending on what operating system you use, and
  is an
|  exercise best left to the user. However, here are some pointers:

| Note: depending on your setup, you will likely need to put your
  sandbox DNS server
|  *first* in the list.

Mac OS X:
https://www.plus.net/support/software/dns/changing\_dns\_mac.shtml

Ubuntu:
http://www.cyberciti.biz/faq/ubuntu-linux-configure-dns-nameserver-ip-address/
