import tempfile

from __init__ import *

DEBUG = True
TEMPLATE_DEBUG = True

ADMIN_MEDIA_PREFIX = '/media/admin-media/'
MEDIA_ROOT = tempfile.mkdtemp()
MEDIA_URL = '/test/media/'

DBINFO = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'test_tokeniz.sqlite3',
}

for item in ('default', 'read'):
    DATABASES[item].update(DBINFO)

USE_POSTGRESHSTORE = False

INSTALLED_APPS += ('django_nose',)

# Define configuration for testing with coverage output
TEST_RUNNER = 'tokeniz.tests.TokenizTestSuiteRunner'
COVERAGE_MODULES = [
    # common
    'common.mixins', 'common.models', 'common.forms', 'common.managers',

    # relationships
    'relationships.models',

    # api
    'api.
]

# The following apps won't be tested by the testrunner.
TEST_EXCLUDE = [
    'django',
    'south',
]

try:
    from test_local import *
except ImportError:
    pass

# vim: foldmethod=marker
