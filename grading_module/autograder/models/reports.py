from dataclasses import dataclass, field

"""

A Question has 1 or more testfiles associated with it.
Each testfile results in one report file.
A report file contains one or more TestSuite objects, and the parser will wrap them all into a TestSuites object.

TestSuites contain TestSuite objects
TestSuite objects contain TestCase objects - one TestCase is one test.

Would like a TestFileReport to contain


Filename: tests.xml
TestSuites
    TestSuite name:suite1
      TestCase name:test1 passed
      TestCase name:test2 errored with message whoops
      TestCase name:test3 failed with message crashy crash
    TestSuite name:suite2
      TestCase name:test21 passed
      TestCase name:test23 failed with message yuck

Question Report can contain 1+ TestFileReport, also question number, number of points


"""



@dataclass
class TestFileReport:
    filename: str
    tests: int = 0
    passed: int = 0
    message: str = ''
    testsuites: list = field(init=False, default_factory=list)


@dataclass
class QuestionReport:
    question: str
    source_file: str
    points_available: float
    report_files: list = field(default_factory=list)
    points_earned: float = 0
    points_earned: int = 0
    tests: int = 0
    passes: int = 0
    testsuites: list = field(init=False, default_factory=list)
    fraction_passed: float = 0

    def calc_grade(self):

        # sum tests, and passes from all testsuites
        self.tests = sum( [tss.tests for tss in self.testsuites ] )
        self.passes = sum( [tss.passes for tss in self.testsuites] )

        if self.tests == 0:
            self.fraction_passed = 0
        else:
            self.fraction_passed = self.passes / self.tests

        points = self.fraction_passed * self.points_available
        self.points_earned = points
        return self.points_earned


    def __str__(self):

        msg_sep = '\n'
        return f'Q: {self.question}, file {self.source_file}, reports {self.report_files}, pts {self.points_available}, earned {self.points_earned}, \nMessages: { msg_sep.join(self.messages)}'


@dataclass
class AssignmentReport:
    question_reports: list = field(init=False, default_factory=list)
    total_points_available: int = 0
    total_points_earned: int = 0

    def add_question_report(self, question_report):
        self.question_reports.append(question_report)
        self.total_points_earned = sum( [ qr.points_earned for qr in self.question_reports] )
