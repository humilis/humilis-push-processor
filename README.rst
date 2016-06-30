Lambda processor for push event sources
=======================================

.. |Build Status| image:: https://travis-ci.org/humilis/humilis-push-processor.svg?branch=master
   :target: https://travis-ci.org/humilis/humilis-push-processor
.. |PyPI| image:: https://img.shields.io/pypi/v/humilis-push-processor.svg?style=flat
   :target: https://pypi.python.org/pypi/humilis-push-processor

|Build Status| |PyPI|

A `humilis <https://github.com/humilis/humilis>`__ plugin to deploy a
`Lambda <https://aws.amazon.com/documentation/lambda/>`__ function that
processes event notification from an `event sources`_ that pushes events to
Lambda (e.g. S3 or SNS, as opposed to Kinesis).

.. _event sources: http://docs.aws.amazon.com/lambda/latest/dg/eventsources.html


Installation
------------

::

    pip install humilis-push-processor

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

    make testi STAGE=[STAGE] DESTROY=[yes|no]


Note that the command above will deploy the processor to the specified
deployment stage. If a deployment stage is not specified then `TEST` will be
used. If ``DESTROY`` is set to ``yes`` all deployed resources will be deleted
after tests have completed (this is also the default behaviour if the
``DESTROY`` parameter is not provided). You can manually destroy the test
infrastructure with:

.. code:: bash

    make delete STAGE=[STAGE]


Deployment secrets
------------------

The S3 event processor supports `Sentry <https://getsentry.com/welcome/>`_
monitoring out of the box. To activate it you just need to store your Sentry
DSN in your local keychain. Using Python's `keyring <https://pypi.python.org/pypi/keyring>`_
module::

    keyring set humilis-push-processor:[STAGE] sentry.dsn [SENTRY_DSN]


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
