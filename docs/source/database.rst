.. _ref-database-configuration:

====================
Database Configuration
====================

This guide will help you to set up and configure your database.

.. warning::
    
    These guides assume that you have already created and activated your
    virtualenv.  If you do not activate your virtualenv, the python
    libraries will be installed globally (not good).

PostgreSQL Installation/Configuration (Ubuntu/Debian)
=====================================================

1.  Use your package manager to install the postgres server::

        $ sudo apt-get install postgresql postgresql-contrib libpq-dev

2.  Become the postgresql user, and create a tokeniz user and database.::

        .. note::
            
            When it asks if this user should be a superuser, say yes.

        $ sudo su - postgres
        $ createuser <tokeniz_db_username>
        $ createdb -O <tokeniz_db_username> <tokeniz_db_name>
        $ psql <tokeniz_db_name>
        <tokenize_db_username>=# create extension hstore;
        <tokenize_db_username>=# \q


3.  Edit the file **/etc/postgresql/9.1/main/pg_hba.conf** and add the
    following to the bottom of the file (this file is space sensative)::

        local   <tokeniz_db_username>          <tokenize_db_name>    trust
        local   test_<tokeniz_db_username>     <tokenize_db_name>    trust

4.  Reload postgres::
    
        sudo service postgresql reload

5.  Activate your virtualenv and install the required python libraries
    (this should already be installed)::

        $ pip install psycopg2==2.4.5
