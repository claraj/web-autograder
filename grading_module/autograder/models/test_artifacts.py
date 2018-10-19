class TestSuites:

    def __init__(self, name='', tests=0, failures=0, errors=0, skipped=0):
        self.name = name
        self.tests = tests
        self.failures = failures
        self.errors = errors
        self.skipped = 0
        self.testsuites = []
        self.passes = self.tests - self.failures


    # def _set_tests(self):
    #     self.tests = sum(ts.tests for ts in self.testsuites)
    #
    #
    # def _set_failures(self):
    #     self.failures = sum(ts.failures for ts in self.testsuites)
    #
    #
    # def _set_errors(self):
    #     self.errors = sum(ts.errors for ts in self.testsuites)
    #
    #
    # def _set_passes(self):
    #     self.passes = self.tests - ( self.failures + self.errors + self.skipped )


    def add_testsuite(self, ts):
        self.testsuites.append(ts)
        # self._set_tests()
        # self._set_failures()
        # self._set_errors()
        # self._set_passes()


    def __len__(self):
        return len(self.testsuites)


    def __getitem__(self, index):
        return self.testsuites[index]


    def fail_error_messages(self):
        return [ ts.fail_error_messages() for ts in self.testsuites ]


class TestSuite:
    """
    Has a name,
    number of tests, number of failures, number of errors, number of skipped
    Contains a list of TestCase objects
    """

    def __init__(self, name, tests, failures, errors=0, skipped=0, filename=None):
        self.name = name
        self.tests = tests
        self.failures = failures
        self.errors = errors
        self.skipped = skipped
        self.filename = filename
        self.testcases = []
        self.passes = self.tests - (self.failures + self.errors + self.skipped)


    def add_testcase(self, testcase):
        self.testcases.append(testcase)


    def __len__(self):
        return len(self.testcases)


    def __repr__(self):
        return f'{self.name}, {self.tests} tests, {self.failures} failures, {self.errors} errors, {self.skipped} skipped, {self.passes} passed.'


    def __getitem__(self, index):
        return self.testcases[index]


    def fail_error_messages(self):
        return [t.failure.message for t in self.testcases if t.failure] + [t.error.message for t in self.testcases if t.error]


class TestCase:
    """
    One test - it passes or fails. ( or errors or is skipped. )
    Has a name - the method name in JUnit, the message in it('sdfsf') in Karma
    A classname - the class in Junit, the describe('sdfsf') in Karma
    A failure, if the test failed, None if it passed
    An error if the test errored, None otherwise
    A test is considered to be a pass if it did not fail or error.
    """

    def __init__(self, name, classname, failure=None, error=None):
        self.name = name;
        self.classname = classname
        self.failure = failure
        self.error = error
        self.passed = (failure == None and error == None)

    def __repr__(self):

        if self.error:
            passfailerror = str(self.error)
        elif self.failure:
            passfailerror = str(self.failure)
        else:
            passfailerror = 'Passed'

        return f'{self.name} for class {self.classname}. {passfailerror}'


class Failure:
    def __init__(self, message, text):
        self.message = message
        self.fulltext = text

    def __str__(self):
        return f'Failed with message {self.message}, text starts with {self.fulltext[:50]}'


class TestError:
    def __init__(self, message, text):
        self.message = message
        self.fulltext = text

    def __str__(self):
        return f'Errored with message {self.message}, text starts with {self.fulltext[:50]}'
