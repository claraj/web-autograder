from dataclasses import dataclass, field

@dataclass
class TestSuites:

    name: str = 'Unnamed Test Suite'
    tests: int = 0
    failures: int = 0
    errors: int = 0
    skipped: int = 0
    testsuites: list = field(init=False, default_factory=list)
    passes: int = field(init=False, default=0)


    def __post_init__(self):
        self.passes = self.tests - (self.failures + self.errors + self.skipped)
        print("HELLO! this is tss post init ")


    def add_testsuite(self, ts):
        self.testsuites.append(ts)
        self.tests = sum( [ts.tests for test in self.testsuites] )
        self.failures = sum( [ts.failures for test in self.testsuites] )
        self.errors = sum( [ts.errors for test in self.testsuites] )
        self.skipped = sum( [ts.skipped for test in self.testsuites] )
        self.passes = sum( [ts.passes for test in self.testsuites] )


    def __len__(self):
        return len(self.testsuites)


    def __getitem__(self, index):
        return self.testsuites[index]


    def fail_error_messages(self):
        return [ ts.fail_error_messages() for ts in self.testsuites ]



@dataclass
class TestSuite:
    """
    Has a name,
    number of tests, number of failures, number of errors, number of skipped
    Contains a list of TestCase objects
    """
    name: str
    tests: int
    failures: int = 0
    errors: int = 0
    skipped: int = 0
    filename: str = None
    testcases: list = field(init=False, default_factory=list)
    passes: int = field(init=False)


    def __post_init__(self):
        self.passes = self.tests - (self.failures + self.errors + self.skipped)
        print("HELLO! this is ts post init ", self.passes)


    def add_testcase(self, testcase):
        self.testcases.append(testcase)


    def __len__(self):
        return len(self.testcases)


    def __getitem__(self, index):
        return self.testcases[index]


    def fail_error_messages(self):
        return [t.failure.message + ', ' + t.failure.fulltext for t in self.testcases if t.failure] + [t.error.message + ', ' + t.error.fulltext for t in self.testcases if t.error]


@dataclass
class Failure:

    message: str
    fulltext: str


@dataclass
class TestError:

    message: str
    fulltext: str


@dataclass
class TestCase:
    """
    One test - it passes or fails. ( or errors or is skipped. )
    Has a name - the method name in JUnit, the message in it('sdfsf') in Karma
    A classname - the class in Junit, the describe('sdfsf') in Karma
    A failure, if the test failed, None if it passed
    An error if the test errored, None otherwise
    A test is considered to be a pass if it did not fail or error.
    """

    name: str
    classname: str
    failure: Failure = None
    error: TestError = None
    passed: bool = field(init=False)

    def __post_init__(self):
        self.passed = self.failure == None and self.error == None
