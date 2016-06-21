Lambda processor for event sources
===================================

.. |Build Status| image:: https://travis-ci.org/humilis/humilis-lambda-processor.svg?branch=master
   :target: https://travis-ci.org/humilis/humilis-lambda-processor
.. |PyPI| image:: https://img.shields.io/pypi/v/humilis-s3-processor.svg?style=flat
   :target: https://pypi.python.org/pypi/humilis-s3-processor

|Build Status| |PyPI|

A `humilis <https://github.com/humilis/humilis>`__ plugin to deploy a
`Lambda <https://aws.amazon.com/documentation/lambda/>`__ function that
processes event notification from any of the `event sources`_ supported by 
AWS.

.. _event sources: http://docs.aws.amazon.com/lambda/latest/dg/eventsources.html


Installation
------------

::

    pip install humilis-lambda-processor

Development
-----------

Assuming you have
`virtualenv <https://virtualenv.readthedocs.org/en/latest/>`__ installed:

::

    make develop

Configure humilis:

::

    .env/bin/humilis configure --local


You can crate a development deployment (on a deployment stage called `DEV`) of
the Lambda function using:

.. code:: bash

    make create STAGE=DEV

The command above will also create additional resources (such as a S3 bucket)
needed to produce a self-contained deployment that you can play with. You
can destroy the `DEV` deployment using:

.. code:: bash

    make delete STAGE=DEV


Testing
-------

To run the local test suite::

    make test

To run the integration test suite:

::

    make testi


Note that the command above will deploy the processor to a deployment stage 
called `TEST`. All deployed resources will be deleted after tests have 
completed but if you want to make sure that you are not leaving any
(cost-incurring) infrastructure behind you may want to also run:

.. code:: bash

    make delete STAGE=TEST


Deployment secrets
------------------

The S3 event processor supports `Sentry <https://getsentry.com/welcome/>`_
monitoring out of the box. To activate it you just need to store your Sentry
DSN in your local keychain. Using Python's `keyring <https://pypi.python.org/pypi/keyring>`_
module::

    keyring set humilis-lambda-processor:[STAGE] sentry.dsn [SENTRY_DSN]


Alternatively you can set environment variable ``SENTRY_DSN``



More information
----------------

See `humilis <https://github.com/humilis/humilis>`__ documentation.


Contact
-------

If you have questions, bug reports, suggestions, etc. please create an issue on
the `GitHub project page <http://github.com/humilis/humilis-lambda-processor>`_.

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

See `License file <https://github.com/humilis/humilis-lambda-processor/blob/master/LICENSE.txt>`_


© 2016 German Gomez-Herrero, FindHotel and others.
