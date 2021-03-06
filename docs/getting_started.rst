Getting Started
===============

Setup
-----

Install Salmon from PyPI::

    $ pip install [--user] salmon-mail

Now run the ``gen`` command to create the basic layout of your first project::

    $ salmon gen myproject

Then change directory to ``myproject``

.. warning:: Users of older versions of Salmon should note that the project
   template now uses LMPTReceiver as its default

Handlers
--------

Handlers are how your application will process incoming mail. Open
``app/handlers/sample.py`` and you'll see the following:

.. literalinclude:: ../salmon/data/prototype/app/handlers/sample.py
   :language: python

Each handler returns the next handler for that sender. ``START`` is the default
handler for senders that Salmon doesn't know about. This `state` is stored in
memory by default.

Let's start up a server and see how it all works::

    $ salmon start
    $ salmon status
    Salmon running with PID 4557

If you look at ``logs/salmon.log``, you'll see various start-up messages from Salmon.

Now send an email to our server::

    $ telnet localhost 8823
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    220 localhost Salmon Mail router LMTPD, version 3
    MAIL FROM: sender@example.com
    250 Ok
    RCPT TO: rcpt@example.com
    250 Ok
    DATA
    354 End data with <CR><LF>.<CR><LF>
    Hello
    .
    250 Ok
    QUIT
    221 Bye
    Connection closed by foreign host.

Check ``logs/salmon.log`` and you'll see the following lines::

    2016-01-11 00:49:49,947 - root - DEBUG - Message received from Peer: ('127.0.0.1', 38150), From: 'sender@example.com', to To ['rcpt@example.com'].
    2016-01-11 01:00:49,949 - routing - DEBUG - Matched 'rcpt@example.com' against START.
    2016-01-11 01:00:49,949 - sample_app - INFO - START: rcpt@example.com
    2016-01-11 01:00:49,950 - routing - DEBUG - Message to rcpt@example.com was handled by app.handlers.sample.START

If you send the message again you'll see this::

    2016-01-11 01:01:36,486 - root - DEBUG - Message received from Peer: ('127.0.0.1', 54628), From: 'sender@example.com', to To ['rcpt@example.com'].
    2016-01-11 01:01:36,487 - routing - DEBUG - Matched 'rcpt@example.com' against NEW_USER.
    2016-01-11 01:01:36,488 - routing - DEBUG - Message to rcpt@example.com was handled by app.handlers.sample.NEW_USER

As the ``NEW_USER`` handler returns itself, every message from "sender@example" will now be processed by ``NEW_USER``

Once you're done, stop the server::

    $ salmon stop
    Stopping processes with the following PID files: ['./run/stmp.pid']
    Attempting to stop salmon at pid 4557

Configuration
-------------

By deafult, all configuration happens in ``config/``

``boot.py``
^^^^^^^^^^^

This file is used by Salmon during start-up to configure the daemon with
various things, such as starting the ``LMTPReceiver``. It's a bit like the
``wsgi.py`` file that Python web apps have. If you want to use a different boot
module, you can specify it with the ``--boot`` argument. E.g. to use
``myapp/othermodule.py``, do::

    salmon start --boot myapp.othermodule

``testing.py``
^^^^^^^^^^^^^^

Just like ``boot.py``, except for testing. You can specify ``--boot
config.testing`` when starting Salmon to try it out.

``logging.conf`` and ``test_logging.conf``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Standard Python logging configuration files. See Python's documentation for more
details.

``settings.py``
^^^^^^^^^^^^^^^

This file contains generic settings used by the rest of your application, e.g.
which port the receiver should listen to. The default settings module is ``config.settings``

You can specify a different settings module via the environment variable
``SALMON_SETTINGS_MODULE``::

    SALMON_SETTINGS_MODULE="myapp.othersettings" salmon start
