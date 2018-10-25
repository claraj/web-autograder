from ..junitparser.parse import parse as juparse
from ..models.reports import AssignmentReport, QuestionReport
# from .autograder.junitparser.parse import parse as juparse
import os
from collections import namedtuple


"""
A project will have a number (1+) files with names in the format TEST-testfilename.xml.
These files are located in the

The grade_scheme.json has an attribute "questions" which is a describes a list of question objects in the format
    {
      "question" : 3,
      "source_file": "Question_3_Agile_Or_Waterfall",
      "test_files": ["week_3.Question_3_Agile_Or_WaterfallTest", "week_3.Question_3_Another_Test"],
      "points": 3.5
     }

The procedure to grade is:


For each question:
  identify points available
  For each test_file:
    find report
    count total tests, passing tests
  sum total tests for all file, sum total passing tests for all files
  question points are adjusted by fraction of tests passed
  add points for question to total
  add messages to output

  # points earned = fraction of tests passed (for all the tests in all the files), multiplied by points available
  # e.g. 5 tests, 3 passes. Question is worth 10 points
  # 5/3 * 10 = 6 points

"""


def grade(report_path, scheme):

    questions = scheme['questions']

    total_points = 0
    assignment_report = AssignmentReport()

    for question in questions:

        question_tests = 0
        question_test_passes = 0

        question_report = initialize_report(question)

        for report_file in question_report.report_files:

            filename = f'TEST-{report_file}.xml'
            report_file_path = os.path.join(report_path, filename)
            testsuites, tests, passes = grade_report_file(report_file_path)

            question_report.testsuites.append(testsuites)
            question_report.tests += tests
            question_report.passes += passes

        question_report.calc_grade()

        assignment_report.add_question_report(question_report)
        # reports.total_points += question_report.points_earned

        # print('One report messages', question_report.messages)

    return assignment_report  # Has a list of questionreports, which have a list of testsuites, and total points earned


def initialize_report(question):
    question_id = question['question']
    available_points = question['points']
    source_file = question['source_file']
    report_files = question['test_files']

    return QuestionReport(question=question, source_file=source_file, \
        points_available=available_points, report_files=report_files)


def grade_report_file(report_file):
    points = 0
    messages = []

    try:
        testsuites = juparse.parse(report_file)
    except FileNotFoundError:
        return f'error file {report_file} not found', 0, 0  # Ignore. # TODO this will break.

    total_tests = testsuites.tests
    total_passes = testsuites.passes

    print('MESSAGES FROM FILE ARE', messages)
    # return '\n\n'.join(messages), points
    return testsuites, total_tests, total_passes
