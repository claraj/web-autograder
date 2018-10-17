class TestSuites:

    def __init__(self, name='', tests=0, failures=0):
        self.name = name
        self._tests = tests
        self._failures = failures
        self.testsuites = []

    def set_tests(self):
        self.tests = sum(ts.tests for ts in self.testsuites)

    def set_failures(self):
        self.failures = sum(ts.failures for ts in self.testsuites)

    def add_testsuite(self, ts):
        self.testsuites.append(ts)
        self.set_tests()
        self.set_failures()

    def __len__(self):
        return len(self.testsuites)

    def __getitem__(self, index):
        return self.testsuites[index]


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


class TestCase:
    """
    One test - it passes or fails. ( or errors or is skipped. )
    Has a name - the method name in JUnit, the message in it('sdfsf') in Karma
    A classname - the class in Junit, the describe('sdfsf') in Karma
    A failure, if the test failed, None if it passed
    """

    def __init__(self, name, classname, failure=None):
        self.name = name;
        self.classname = classname
        self.failure = failure
        self.passed = (failure == None)


    def __repr__(self):
        passfail = 'Passed' if self.failure is None else ('Failed because ' + self.failure.message)
        return f'{self.name} for class {self.classname}. {passfail}'


class Failure:
    def __init__(self, message, text):
        self.message = message
        self.fulltext = text

    def __repr__(self):
        return f'Failed with message {self.message}, text starts with {self.fulltext[:50]}'
