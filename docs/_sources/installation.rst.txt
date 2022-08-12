.. highlight:: shell

Installation
============


.. Stable release
.. --------------

.. To install MPIM Ice-Lab Routines, run this command in your terminal:

.. .. code-block:: console

..     $ pip install mpim-icelab

.. This is the preferred method to install MPIM Ice-Lab Routines, as it will always install the most recent stable release.

.. If you don't have `pip`_ installed, this `Python installation guide`_ can guide
.. you through the process.

.. .. _pip: https://pip.pypa.io
.. .. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for MPIM Ice-Lab Routines can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/markusritschel/mpim-icelab

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/markusritschel/mpim-icelab/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


Changes on the code
-------------------
If you plan on making changes to the code, you can install the package in developer mode, which would mirror all your
changes to the installed package such that all your changes are immediately reflected in the installed version.

.. code-block:: console

    $ python setup.py develop


.. _Github repo: https://github.com/markusritschel/mpim-icelab
.. _tarball: https://github.com/markusritschel/mpim-icelab/tarball/master
