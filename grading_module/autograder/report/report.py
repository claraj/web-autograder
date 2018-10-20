from ..junitparser.parse import parse as juparse
from ..models.reports import TestSuiteReport as Report

# from .autograder.junitparser.parse import parse as juparse
import os
from collections import namedtuple


"""
A project will have a number (1+) files with names in the format TEST-testfilename.xml.
These files are located in the

The scheme json has an attribute "questions" which is a describes a list of question objects in the format
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



  # points earned = fraction of tests passed, multiplied by points available
  # e.g. 5 tests, 3 passes. Question is worth 10 points
  # 5/3 * 10 = 6 points
"""


def grade(report_path, scheme):
    questions = scheme['questions']

    total_points = 0
    reports = []

    for question in questions:

        question_report = initialize_report(question)

        for report_file in question_report.report_files:
            report_file_path = os.path.join(report_path, f'TEST-{report_file}.xml')
            messages, points_earned = grade_report_file(report_file_path, question_report.points_available)
            print('points:', report_file, question_report.points_earned, points_earned)
            question_report.points_earned += points_earned
            question_report.messages.append(messages)

        reports.append(question_report)
        total_points += question_report.points_earned

    return reports, total_points


def initialize_report(question):
    question_id = question['question']
    available_points = question['points']
    source_file = question['source_file']
    report_files = question['test_files']

    return Report(question=question, source_file=source_file, \
        points_available=available_points, report_files=report_files, messages=[], points_earned=0)


def grade_report_file(report_file, points_available):
    points = 0
    messages = []

    try:
        testsuites = juparse.parse(report_file)
    except FileNotFoundError:
        return [f'error file {report_file} not found'], 0  # Ignore.

    for testsuite in testsuites:
        messages, fraction = extract_data(testsuite)
        points_earned = fraction * points_available
        points += points_earned
        print(f'maths: fraction {fraction}, points earned {points_earned}, available {points_available}')
        messages.append(messages)

    return messages, points


def extract_data(testsuite):
    no_tests = testsuite.tests
    no_passes = testsuite.passes

    fraction_passed = 0 if no_passes == 0 else (no_passes/no_tests)

    print('fraction passed', fraction_passed, no_tests, no_passes)
    messages = testsuite.fail_error_messages()

    return messages, fraction_passed
