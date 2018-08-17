Centralized Ansible Management With Knockd + Auto-provisioning with AWS
#######################################################################
:date: 2014-04-23 06:47
:author: lionfacelemonface
:category: Uncategorized
:tags: amazon web services, ansible, aws, knockd, port knocking, python
:slug: centralized-ansible-management-with-knockd-auto-provisioning-with-aws
:attachments: 2014/04/user-data-screen-shot.png, 2014/04/security-group-config.png
:status: draft

Ansible is a great tool. We've been using it at my job with a fair
amount of success. When it was chosen, we didn't have a requirement for
supporting Auto scaling groups in AWS. This offers a unique problem - we
need machines to be able to essentially provision themselves when AWS
brings them up. This has interesting implications outside of AWS as
well. This article covers using the Ansible API to build just enough of
a custom playbook runner to target a single machine at a time, and
discusses how to wire it up to knockd, a "port knocking" server and
client, and finally how to use user data in AWS to execute this at boot
- or any reboot.

Ansible - A "Push" Model
========================

Ansible is a configuration management tool used in orchestration of
large pieces of infrastructure. It's structured as a simple layer above
SSH - but it's a very sophisticated piece of software. Bottom line, it
uses SSH to "push" configuration out to remote servers - this differs
from some other popular approaches (like Chef, Puppet and CFEngine)
where an agent is run on each machine, and a centralized server manages
communication with the agents. Check out `How Ansible
Works <http://www.ansible.com/how-ansible-works>`__ for a bit more
detail.

Every approach has it's advantages and disadvantages - discussing the
nuances is beyond the scope of this article, but the primary
disadvantage that Ansible has is one of it's strongest advantages: it's
decentralized and doesn't require agent installation. The problem arises
when you don't know your inventory (Ansible-speak for "list of all your
machines") beforehand. This can be mitigated with `inventory
plugins <http://docs.ansible.com/intro_dynamic_inventory.html>`__.
However, when you have to configure machines that are being spun up
dynamically, that need to be configured quickly, the push model starts
to break down.

Luckily, Ansible is highly compatible with automation, and provides a
very useful python API for specialized cases.

Port Knocking For Fun And Profit
================================

`Port knocking <http://portknocking.org/>`__ is a novel way of invoking
code. It involves listening to the network at a very low level, and
listening for *attempted* connections to a specific sequence of ports.
No ports are opened. It has its roots in network security, where it's
used to temporarily open up firewalls. You knock, then you connect, then
you knock again to close the door behind you. It's very cool tech.

The standard implementation of port knocking is
`knockd <http://www.zeroflux.org/projects/knock>`__, included with  most
major linux distributions. It's extremely light weight, and uses a
simple configuration file. It supports some interesting features, such
as limiting the number of times a client can invoke the knock sequence,
by commenting out lines in a flat file.

User Data In EC2
================

EC2 has a really cool feature called `user
data <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html>`__,
that allows you to add some information to an instance upon boot. It
works with `cloud-init <http://cloudinit.readthedocs.org/en/latest/>`__
(installed on most AMIs) to perform tasks and run scripts when the
machine is first booted, or rebooted.

Auto Scalling
=============

EC2 provides a mechanism for spinning up instances based on need (or
really any arbitrary event). The `AWS
documentation <http://docs.aws.amazon.com/AutoScaling/latest/DeveloperGuide/WhatIsAutoScaling.html>`__
gives a detailed overview of how it works. It's useful for responding to
sudden spikes in demand, or contracting your running instances during
low-demand periods.

Ansilbe + Knockd = Centralized, On-Demand Configuration
=======================================================

As mentioned earlier, Ansible provides a fairly robust API for use in
your own scripts. Knockd can be used to invoke any shell command. Here's
how I tied the two together.

Prerequisites
-------------

All of my experimentation was done in EC2, using the Ubuntu 12.04 LTS
AMI.

To get the machine running ansible configured, I ran the following
commands:

| [code]
|  $ sudo apt-get update
|  $ sudo apt-get install python-dev python-pip knockd
|  $ sudo pip install ansible
|  [/code]

Note: its important that you install the ``python-dev`` package *before*
you install ansible. This will provide the proper headers so that the
c-based SSH library will be compiled, which is faster than the
pure-python version installed when the headers are not available.

You'll notice some information from the knockd package regarding how to
enable it. Take note of this for final deployment, but we'll be running
knockd manually during this proof-of-concept exercise.

On the "client" machine, the one who is asking to be configured, you
need only install knockd. Again, the service isn't enabled by default,
but the package provides the ``knock`` command.

EC2 Setup
---------

We require a few things to be done in the EC2 console for this all to
work.

First, I created a keypair for use by the tool. I called "bootstrap". I
downloaded it onto a freshly set up instance I designated for this
purpose.

NOTE: It's important to set the permissions of the private key
correctly. They **must** be set to ``0600``.

I then needed to create a special security group. The point of the group
is to allow *all* ports from within the current subnet. This gives us
maximum flexibility when assigning port knock sequences.

Here's what it looks like:

|image0|\ Depending on our circumstances, we would need to also open up
UDP traffic as well (port knocks can be TCP or UDP based, or a
combination within a sequence).

For the sake of security, a limited range of a specific type of
connection is advised, but since we're only communicating over our
internal subnet, the risk here is minimal.

Note that I've also opened SSH traffic to the world. This is not
advisable as standard practice, but it's necessary for me since I do not
have a fixed IP address on my connection.

Making It Work
--------------

I wrote a simple python script that runs a given playbook against a
given IP address:

| [code language="python"]
|  """
|  Script to run a given playbook against a specific host
|  """

| import ansible.playbook
|  from ansible import callbacks
|  from ansible import utils

| import argparse
|  import os, sys

| parser = argparse.ArgumentParser(
|  description="Run an ansible playbook against a specific host."
|  )

| parser.add\_argument(
|  'host',
|  help="The IP address or hostname of the machine to run the playbook
  against."
|  )

| parser.add\_argument(
|  "-p",
|  "--playbook",
|  default="default.yml",
|  metavar="PLAY\_BOOK",
|  help="Specify path to a specific playbook to run."
|  )

| parser.add\_argument(
|  "-c",
|  "--config\_file",
|  metavar="CONFIG\_FILE",
|  default="./config.ini",
|  help="Specify path to a config file. Defaults to %(default)s."
|  )

| def run\_playbook(host, playbook, user, key\_file):
|  """
|  Run a given playbook against a specific host, with the given username
|  and private key file.
|  """
|  stats = callbacks.AggregateStats()
|  playbook\_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
|  runner\_cb = callbacks.PlaybookRunnerCallbacks(stats,
  verbose=utils.VERBOSITY)

| pb = ansible.playbook.PlayBook(
|  host\_list=[host,],
|  playbook=playbook,
|  forks=1,
|  remote\_user=user,
|  private\_key\_file=key\_file,
|  runner\_callbacks=runner\_cb,
|  callbacks=playbook\_cb,
|  stats=stats
|  )

pb.run()

options = parser.parse\_args()

playbook = os.path.abspath("./playbooks/%s" % options.playbook)

| run\_playbook(options.host, playbook, 'ubuntu', "./bootstrap.pem")
|  [/code]

Most of the script is user-interface code, using
`argparse <https://docs.python.org/2/library/argparse.html?highlight=argparse#argparse>`__
to bring in configuration options. One unimplemented feature is using an
INI file to specify things like the default playbook, pem key, user,
etc. These things are just hard coded in the call to run\_playbook for
this proof-of-concept implementation.

The real heart of the script is the run\_playbook function. Given a host
(IP or hostname), a path to a playbook file (assumed to be relative to a
"playbooks" directory), a user and a private key, it uses the Ansible
API to run the playbook.

This function represents the bare-minimum code required to apply a
playbook to one or more hosts. It's surprisingly simple - and I've only
scratched the surface here of what can be done. With custom callbacks,
instead of the ones used by the ansible-playbook runner, we can fine
tune how we collect information about each run.

The playbook I used for testing this implementation is very simplistic
(see `the Ansible playbook
documentation <http://docs.ansible.com/playbooks.html>`__ for an
explaination of the playbook syntax):

| [code]
|  ---
|  - hosts: all
|  sudo: yes
|  tasks:
|  - name: ensure apache is at the latest version
|  apt: update\_cache=yes pkg=apache2 state=latest
|  - name: drop an arbitrary file just so we know something happened
|  copy: src=it\_ran.txt dest=/tmp/ mode=0777
|  [/code]

It just installs and starts apache, does an ``apt-get update``, and
drops a file into /tmp to give me a clue that it ran.

Note that the ``hosts:`` setting is set to "all" - this means that this
playbook will run regardless of the role or class of the machine. This
is essential, since, again, the machines are unknown when they invoke
this script.

For the sake of simplicity, and to set a necessary environment variable,
I wrapped the call to my script in a shell script:

| [code language="bash"]
|  #!/bin/bash
|  export ANSIBLE\_HOST\_KEY\_CHECKING=False
|  cd /home/ubuntu
|  /usr/bin/python /home/ubuntu/run\_playbook.py $1 >> $1.log 2>&1
|  [/code]

The ``$ANSIBLE_HOST_KEY_CHECKING`` environment variable here is
necessary, short of futzing with the ssh configuration for the ubuntu
user, to tell Ansible to not bother verifying host keys. This is
required in this situation because the machines it talks to are unknown
to it, since the script will be used to configure newly launched
machines. We're also running the playbook unattended, so there's no one
to say "yes" to accepting a new key.

The script also does some very rudimentary logging of all output from
the playbook run - it creates logs for each host that it services, for
easy debugging.

Finally, the following configuration in ``knockd.conf`` makes it all
work:

| [code]
|  [options]
|  UseSyslog

| [ansible]
|  sequence = 9000, 9999
|  seq\_timeout = 5
|  Command = /home/ubuntu/run.sh %IP%
|  [/code]

The first configuration section ``[options]``, is special to knockd -
its used to configure the server. Here we're just asking knockd to log
message to the system log (e.g. /var/log/messages).

The ``[ansible]`` section sets up the knock sequence for an machine that
wants Ansible to configure it. The sequence set here (it can be anything
- any port number and any number of ports >= 2) is 9000, 9999. There's a
5 second timeout - in the event that the client doing the knocking takes
longer than 5 seconds to complete the sequence, nothing happens.

Finally, the command to run is specified. The special ``%IP%`` variable
is replaced when the command is executed by the IP address of the
machine that knocked.

At this point, we can test the setup by running knockd. We can use the
``-vD`` options to output lots of useful information.

We just need to then do the knocking from a machine that's been
provisioned with the bootstrap keypair.

Here's what it looks like (these are all Ubuntu 12.04 LTS instances):

On the "server" machine, the one with the ansible script:

::

    $  sudo knockd -vD
    config: new section: 'options'
    config: usesyslog
    config: new section: 'ansible'
    config: ansible: sequence: 9000:tcp,9999:tcp
    config: ansible: seq_timeout: 5
    config: ansible: start_command: /home/ubuntu/run.sh %IP%
    ethernet interface detected
    Local IP: 172.31.31.48
    listening on eth0...

On the "client" machine, the one that wants to be provisioned:

::

    $ knock 172.31.31.48 9000 9999

Back on the server machine, we'll see some output upon successful knock:

::

    2014-03-23 10:32:02: tcp: 172.31.24.211:44362 -> 172.31.31.48:9000 74 bytes
    172.31.24.211: ansible: Stage 1
    2014-03-23 10:32:02: tcp: 172.31.24.211:55882 -> 172.31.31.48:9999 74 bytes
    172.31.24.211: ansible: Stage 2
    172.31.24.211: ansible: OPEN SESAME
    ansible: running command: /home/ubuntu/run.sh 172.31.24.211

 

Making It Automatic With User Data
==================================

Now that we have a way to configure machines on demand - the knock could
happen at any time, from a cron job, executed via a distributed SSH
client (like `fabric <http://docs.fabfile.org/en/1.8/>`__), etc - we can
use the user data feature of EC2 with cloud-init to do the knock at
boot, and every reboot.

Here is the user data that I used, which is technically *cloud config*
code (`more examples
here <http://cloudinit.readthedocs.org/en/latest/topics/examples.html>`__):

| [code]
|  #cloud-config
|  packages:
|  - knockd

| runcmd:
|  - knock 172.31.31.48 9000 9999
|  [/code]

User data can be edited at any time as long as an EC2 instance is in the
"stopped" state. When launching a new instance, the field is hidden in
Step 3, under "Advanced Details":

|User Data Field|\ Once this is established, you can use the "launch
more like this" feature of the AWS console to replicate the user data.

This is also a prime use case for writing your own provisioning scripts
(using something like `boto <http://boto.readthedocs.org/en/latest/>`__)
or using something a bit higher level, like
`CloudFormation <https://aws.amazon.com/cloudformation/>`__.

Auto Scaling And User Data
==========================

Auto Scaling is controlled via "auto scaling groups" and "launch
configuration". If you're not familiar these can sound like foreign
concepts, but they're quite simple.

Auto Scaling Groups define how many instances will be maintained, and
set up the events to scale up or down the number of instances in the
group.

Launch Configurations are nearly identical to the basic settings used
when launching an EC2 instance, including user data. In fact, user data
is entered in on Step 3 of the process, in the "Advanced Details"
section, just like when spinning up a new EC2 instance.

In this way, we can automatically configure machines that come up via
auto scaling.

Conclusions And Next Steps
==========================

This proof of concept presents an exciting opportunity for people who
use Ansible and have use cases that benefit from a "pull" model -
without really changing anything about their setup.

Here are a few miscellaneous notes, and some things to consider:

-  There are many implementations of port knocking, beyond knockd. There
   is a `huge amount of information available <http://portknocking.org/view/resources>`__ to dig into the
   concept itself, and it's various implementations.
-  The way the script is implemented, it's possible to have different
   knock sequences execute different playbooks. A "poor-man's" method of
   differentiating hosts.
-  The Ansible script could be coupled the AWS API to get more
   information about the particular host it's servicing. Imagine using a
   tag to set the "class" or "role" of the machine. The API could be
   used to look up that information about the host, and apply playbooks
   accordingly. This could also be done with variables - the values that
   are "punched in" when a playbook is run. This means one source of
   truth for configuration - just add the relevant bits to the right
   tags, and it just works.
-  I tested this approach with an auto scaling group, but I've used a
   trivial playbook and only launched 10 machines at a time - it would
   be a good idea to test this approach with hundreds of machines and
   more complex plays - my "free tier" t1.micro instance handled this
   "stampeding herd" without a blink, but it's unclear how this really
   scales. **If anyone gives this a try, please let me know how it went.**
-  Custom callbacks could be used to enhance the script to send
   notifications when machines were launched, as well as more detailed
   logging.

.. |image0| image:: http://lionfacelemonface.files.wordpress.com/2014/04/security-group-config.png?w=640
   :target: http://lionfacelemonface.files.wordpress.com/2014/04/security-group-config.png
.. |User Data Field| image:: http://lionfacelemonface.files.wordpress.com/2014/04/user-data-screen-shot.png?w=640
   :target: http://lionfacelemonface.files.wordpress.com/2014/04/user-data-screen-shot.png
