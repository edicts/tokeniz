import coverage
import shutil

from django_nose import NoseTestSuiteRunner
from django.conf import settings

EXCLUDED_APPS = getattr(settings, 'TEST_EXCLUDE', [])


class TokenizTestSuiteRunner(NoseTestSuiteRunner):
    """
    Runs testing suite and adds code coverage report.
    """
    def __init__(self, *args, **kwargs):
        super(TokenizTestSuiteRunner, self).__init__(*args, **kwargs)
        self.coverage = coverage.coverage()
        self.coverage.use_cache(0)  # don't use caching with coverage.py

    def build_suite(self, *args, **kwargs):
        suite = super(TokenizTestSuiteRunner, self).build_suite(
            *args, **kwargs)
        # Filter out tests from EXCLUDED_APPS
        # Hacky code borrowed from http://djangosnippets.org/snippets/2211/
        tests = []
        for case in suite:
            pkg = case.__class__.__module__.split('.')[0]
            if pkg not in EXCLUDED_APPS:
                tests.append(case)
        suite._tests = tests

        return suite

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        test_coverage = hasattr(settings, "COVERAGE_MODULES") and \
            not test_labels

        if test_coverage:
            self.coverage.start()

        test_results = super(TokenizTestSuiteRunner, self)\
            .run_tests(test_labels, extra_tests, **kwargs)

        if test_coverage:
            self.coverage.stop()
            if test_results < 1:
                self._print_coverage()

        shutil.rmtree(settings.MEDIA_ROOT)
        return test_results

    def _print_coverage(self):
        print ''
        print '-' * 46
        print "Unit Test Coverage Results"
        print '-' * 46

        # Report the metrics
        coverage_modules = []
        for module in settings.COVERAGE_MODULES:
            coverage_modules.append(
                __import__(module, globals(), locals(), ['']))

        self.coverage.report(coverage_modules, show_missing=1)

        print '-' * 46

