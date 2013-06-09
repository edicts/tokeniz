Testing
=======
Testing is an important part of the maintainability moving forward.
We focus on building automated testing for models, forms and other classes with
commonly-used and/or vital interfaces for the functions. With these
efforts, we strive to keep as close as we can to 100% code coverage in these
tested areas.

In Tokeniz
---------
.. warning::
    These guides assume that you have already created and activated your
    virtualenv.  If you do not activate your virtualenv, the python
    libraries will be installed globally (not good).

We use Django's test commands to execute tests. There is only one
adjustment that needs to be made to the standard command; Use the test settings
included in the repository.::

    $ django-admin.py test --settings=tokeniz.settings.test

This will test all apps within Tokeniz. However usually as you are developing,
you will want to be specific to the app you modifying. Through Django's test
command, you can also define the specific app to test with the following
command.::

    $ django-admin.py test common --settings=tokeniz.settings.test

Once tests have passed and you've verified proper coverage you should run a
PEP8 check with the following command and fix any suggestions given by
the output.::

    $pep8 --first --show-source --show-pep8 --count --ignore=W391 --exclude=urls.py,README.md,REQUIREMENTS.pip *


Notes
-----
We require that tests be ran before pushing code live. If you push code that
breaks tests, this will most likely cause other developers to stall their
changes until they can fully test their changes.

We do have a couple exceptions for testing. Templates and Views in Django are
not necessary to test. Both of these areas have often changing interfaces that
really hamper development.

There are exceptions for PEP8 standards.  Just because the output suggests a
change doesn't necessarily mean you should make the change.  Use your best
judgement.  If you don't know what to do you should err on the side of
caution or ask another developer for their opinion.
