Release Cycle
====================

No development cycle exists. All the development work that is approved will be pushed live.


Branches
--------

"dev" is the branch with everything that is currently available for the next
release.

"master" is the branch with everything that should be live as of now.


Hot-fixes
---------

In between main release cycle, features and bugs may be addressed as
"hot-fixes". These are intended to be business needs that are of a high
priority. These fixes should *not* be merged to the "dev" branch, first.
However, they should be approved to be merged to "master". When the hot-fix is
merged to "master", it should immediately be tagged, pushed to live and merged
back to dev by the person pushing to live.


Tagging
-------

Each release will be tagged in our main Git repo for historical reference. If
we have a critical problem with one release, then we will be able to push the
HEAD of our last functioning tag to restore live until the problem is fixed.

The syntax for tagging is as follows::

    { major version }.{ two-digit year }.{ non-zero month }.{ month release number }

For example, a first release occurrence for August 3rd, 2013 would have the following tag::

    1.13.8.1

Presumably, the next release occurrence, say on September 16th, 2013, should have::

    1.13.9.1

Hot-fixes are given an extra minor number for tagging::

    { major version }.{ two-digit year }.{ non-zero month }.{ month release number }.{ hot-fix release number }

If we had a hot-fix after our first release occurrence and before the second
release occurrence, the tag should be::

    1.13.8.1.1


Pushing to Live
---------------

To push to live, you will need sudo/root access on web servers and worker
servers. We have a fab script used for deploying at { tokeniz root }/deploy.py.
The basic usage of this file is to run two fabric commands: deploy.web and
deploy.worker. These two commands are meant to pull the latest of origin/master
and make respective updates and reloads on their server. To get more
information, run `fab -l` in the command line from { tokeniz root }, or check
out the deploy.py file for comments.

