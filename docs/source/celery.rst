.. _celery-setup::

===========================
Celery/RabbitMQ Setup Guide
===========================

Installation
============

This will explain how to install Celery/RabbitMQ

1.  Install RabbitMQ using your package manager, for example::

        $ sudo apt-get install rabbitmq-server

2.  For the Celery set up step, activate your virtualenv::

        $ workon tokeniz

3.  Install celery (this step has probably already been completed)::

        $ pip install celery==3.0.1

4.  Run the celery migrations if needed::

        $ django-admin.py migrate djcelery

Configuration
=============

If you followed the installation instructions, you will not need to do any 
configuration, the guest user will work.  However, if you do need do use
a custom username and password, you can change these settings by overriding 
*BROKER_URL* in your local settings file.

Running
=======

For development, you can start a celery worker with the celery worker management
command::

    $ django-admin.py celery worker -E --loglevel=info

In order for the management monitor to work (in the Django admin), you also have
to start the celery cam::

    $ django-admin.py celerycam


