Programming Style Guide
===============================

The focus of this style guide is to keep consistency among developers
team. Most of the style guide will be inherited from Python's style guide,
`PEP-8 <http://www.python.org/dev/peps/pep-0008/>`_,
`Django's Coding Style <http://tinyurl.com/6753zmc>`_ and
`Google's Python Coding Style Guide <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>`_.

PEP-8
-----
This is a highlight of the important pieces of the PEP-8 document. You should
still read the whole document to familiarize yourself with all rules.
`PEP-8 <http://www.python.org/dev/peps/pep-0008/>`_ and
`Google's Python Coding Style Guide <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>`_

- Two good reasons to break a particular rule:
    - When applying the rule would make the code less readable, even for
      someone who is used to reading code that follows the rules.
    - To be consistent with surrounding code that also breaks it (maybe for
      historic reasons) -- although this is also an opportunity to clean up
      someone else's mess.
- Use 4 spaces per indentation level. **Not a tab character**.
- Limit all lines to a **maximum** of 79 characters.
- Imports should usually be on separate lines.
- Avoid extraneous whitespace in the following situations:
    - Immediately inside parentheses, brackets or braces.
    - Immediately before a comma, semicolon, or colon.
    - Immediately before the open parenthesis that starts the argument list
      of a function call.
    - Immediately before the open parenthesis that starts an indexing or
      slicing.
- Use spaces around arithmetic, comparison and binary operators.
- Do not use spaces when around the assignment operator '=' when used to
  indicate a keyword argument or a default parameter value.
- Compound statements (multiple statements on the same line) are generally
  discouraged.

Django's Coding Style
---------------------
This is a highlight of the important pieces of the Django Coding Style. You
should still read the whole document to familiarize yourself with all rules.
`Django's Coding Style <http://tinyurl.com/6753zmc>`_

- In Django template code, put one (and only one) space between the curly
  brackets and the tag contents.
- In Django views, the first parameter in a view function should be called
  request.
- Field names should be all lowercase, using underscores instead of camelCase.

Tokeniz-specific Coding Style
-----------------------------
In-line documentation is not necessary as long as you've followed all style guidlines.
The nature of the Python language lends itself to readability.

No white-space directly before end of line. Including empty lines of code. At
least one empty line at the end of a file.

Tokeniz-specific Django Style
-----------------------------
Templates directly related to an app should be in their respective
app's template directory. For example, a template specific to a "clients" app
should be in the following directory, { app }/templates/{ app }

URL Routing
-----------
Name every URL route in Django. You should always be able to run reverse
routing on the name of the URL.

Use hyphens to separate words for the URL routes (including namespace routes).
Use underscores to represent the same separation in route and namespace names.
For example, the URL r"^my-clients/$" should have the name "my_clients". Match
the routes and their names as close as possible like the example. This will
make it so if that my clients example was in the common app, someone
would expect to be able to use the reverse name of "common:my_clients"
to get to "/common/my-clients".

If you have an ID or slug in URL route, just skip that section in the naming
of the route. For example, r'^(?P<slug>[\w\-]+)/edit/$' should map to "edit".
However, in cases where there is nothing after the ID or slug,
r'^(?P<slug>[\w\-]+)/$' needs to map to something. In this case, it is usually
labeled a "view" page, this one would make sense to call it "view".

Each application should use Django URL namespaces to scope their urls.

If managing models, create namespaces for each model. For example, in the
common app, a Client model should have it's own namespace for managing
Client in the common namespace (i.e. common:client:index).

Within model routing, the following is the standard structure for working with
those URL routes. It is close to RESTful routing, with a few differences.

+--------+--------------------+--------+-----------------------------------+
| Type   | URL                | Method | Description                       |
+========+====================+========+===================================+
| index  | /                  | GET    | Lists model records               |
+--------+--------------------+--------+-----------------------------------+
| new    | /new/              | GET    | Shows form to create model record |
+--------+--------------------+--------+-----------------------------------+
| create | /new/              | POST   | Creates model record              |
+--------+--------------------+--------+-----------------------------------+
| view   | /(id|slug)/        | GET    | Views model record                |
+--------+--------------------+--------+-----------------------------------+
| edit   | /(id|slug)/edit/   | GET    | Shows form to edit model record   |
+--------+--------------------+--------+-----------------------------------+
| update | /(id|slug)/edit/   | POST   | Updates model record              |
+--------+--------------------+--------+-----------------------------------+
| delete | /(id|slug)/delete/ | POST   | Deletes model record              |
+--------+--------------------+--------+-----------------------------------+

If you are adding extra pages/view to model routes, just create them for
"/(id|slug)/(new route)/". For example, if you are within the client namespace
and want to show all the contacts for one client, use this full route
"/common/client/{ client slug }/contacts/".

Git usage
---------
Master branch is always considered live. Never push to master, if it is
not ready for live at that moment.

Create your own remote branch on your github repo for all commits. Then create
a Pull Request on github to the respective branch on the edicts github repo.

*RECOMMENDATION*: Use local branches for most feature requests locally, just
to get used to branches.

Make sure to prune the origin from time-to-time, to clean up your
remote branch tracker.

Be explicit with the name of the branch in our main repo. It always sucks to
run across a branch that you have no idea what it means.

*RECOMMENDATION*: If the remote branch is related to a ticket, the branch name
could just be the referenced ticket name (e.g. S3-123).

Test-driven development
-----------------------
Anytime you are building a test-required implementation, tests should be built
first to replicate the intended implementation. Then you should build code
to pass the tests.

Test-required Implementations are for the following file types:
- forms.py
- generic.py
- managers.py
- mixins.py
- models.py
- utils.py
- other python files

Each class being tested should include tests for each condition in each method.
(This should include 100% coverage for the above file types).

Module-level functions should be tested in these files, as well.

Try to keep these methods and functions as specific (within reason) to it's
purpose. If the functionality starts getting north of 10 lines of code, then
some refactoring may need to be in store. This will keep the tests simple to
write and maintain.

Should never push code to the master git branch where any of these required
tests are failing.

If a bug is found, you should first build a test to replicate the cause of
the bug. Then, write the code to pass that test, therefore fixing the bug.

Database
--------
Should stick to SQL standards when building queries. Should not introduce
queries that will not work in PostgreSQL, MySQL or SQLite.

When drafting/implementing data models, we will follow the Django's imposed
conventions of tables, columns, indexes, etc. Here are some highlights of those
imposed conventions:

- Database table name: { app name }_{ model name }
- Primary key: id
- Foreign key: { foreign model name }_id
- Character Set: utf8
- Collation: utf8_general_ci
- Timestamps: Use for every model, unless specific reason not to.
    - Create: created_at
    - Update: updated_at

Models
------
If a field is required, should define the default value as well.

Every model should have a __unicode__ method.

Settings
--------
Generic project-wide settings should be set in settings/__init__.py and should
be committed to the git repository. Settings that are specific to one of our
defined environments should be included in the repo under there specified name
in the settings directory. System-specific settings or sensitive data should
not be commit to the repo. However, they can optionally be defined under a
local settings files in the settings directory.

Some examples of where settings should go in the settings directory:

- __init__.py
    - Project directory paths.
    - I18n and L10n settings.
    - Middleware settings.
    - Generic database config.

- dev.py
    - Some setting overrides from __init__.py that generically apply to dev
      environments.
    - Imports local_dev.py if exists. Therefore, can override system-specific
      dev settings with local_dev.py

- test.py
    - Some setting overrides from __init__.py that generically apply to test
      environments.
    - Imports local_test.py if exists. Therefore, can override system-specific
      test settings with local_test.py

- production.py
    - Some setting overrides from __init__.py that generically apply to
      production environments.
    - Imports local_production.py if exists. Therefore, can override
      system-specific production settings with local_production.py

- each {environment}_local.py
    - Database config overrides for the system and environment.
    - API Keys for the system and environment.
    - Passwords for the system and environment.
    - Directory overrides for the system and environment.

