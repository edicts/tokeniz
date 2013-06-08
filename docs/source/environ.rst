==========================
Environment Setup
==========================

This guide will help you set up your development environment in order to start
working on tokeniz.  It may also be of use in setting up a production server.

Linux Installation (Ubuntu/Debian)
==================================

By following these steps, you can easily have a working installation of the 
tokeniz development environment.

.. note::

   The following will assume you are cloning the tokeniz sourcecode to
   **~/Projects/tokeniz**.  If you are cloning to a different location, you
   will need to adjust these instructions accordingly.

.. note::

   A dollar sign ($) indicates a terminal prompt, as your user, not root.

1.  Clone the source::

        $ cd ~/Projects
        $ git clone git@github.com:edicts/tokeniz.git

2a. Install some required packages::
    
        $ sudo apt-get install python python-dev python-pip build-essential

2b. NOTE for Ubuntu: Check to see if you have the following symbolic links::
    
        $ /usr/lib/libfreetype.so -> /usr/lib/x86_64-linux-gnu/libfreetype.so
        $ /usr/lib/libz.so -> /usr/lib/x86_64-linux-gnu/libz.so
        $ /usr/lib/libjpeg.so -> /usr/lib/x86_64-linux-gnu/libjpeg.so
    
    If not, ensure you have the following packages::
    
        $ sudo apt-get install libfreetype6-dev libjpeg8-dev zlib1g-dev
    
    Then create the symbolic links manually if the system did not do it for you.
    
3.  Install virtualenv and virtualenvwrapper::

        $ pip install virtualenv
        $ pip install virtualenvwrapper

4.  Add the following to the end of your **~/.bashrc** file (or **~/.zshrc**)::

        source /usr/local/bin/virtualenvwrapper.sh

5.  Type the following::

        $ source /usr/local/bin/virtualenvwrapper.sh

6.  Create your tokeniz virtualenv and deactivate it::

        $ mkvirtualenv tokeniz
        $ deactivate

7.  Add the following to the end of the file
    **~/.virtualenvs/tokeniz/bin/activate**::

        export DJANGO_SETTINGS_MODULE=tokeniz.settings.dev
        export PYTHONPATH=$PYTHONPATH:~/Projects/tokeniz/tokeniz/apps

8.  Activate the virtualenv::

        $ workon tokeniz

9.  Install the required python libraries::

        $ pip install -r ~/Projects/tokeniz/REQUIREMENTS.pip

10. :ref:`Configure your database <ref-database-configuration>`.  

11. Prepare the database (and add yourself a superuser)::

        $ django-admin.py syncdb
        $ django-admin.py migrate

12. Collect the static files::
    
        $ django-admin.py collectstatic

13. Run the Django development server::

        $ django-admin.py runserver

