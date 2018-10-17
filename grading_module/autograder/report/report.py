# from .. import junitparser
from autograder.junitparser.parse import parse as juparse
import os
from collections import namedtuple
from autograder.models.reports import TestSuiteReport as Report

def grade(project_location, config, scheme):

    report_location = config['report_location']
    questions = scheme['questions']

    report_path = os.path.join(project_location, report_location)

    total_points = 0
    reports = []

    for question in questions:

        question_report = initialize_report(question)

        total_points_for_question = 0

        for report_file in question_report.report_files:
            filename = f'TEST-{report_file}.xml'
            report_file_path = os.path.join(report_path, filename)
            messages, points_earned = grade_report_file(report_file_path)
            total_points += points_earned
            messages.append(messages)

        question_report.points_earned = total_points_for_question
        question_report.messages = messages
        reports.append(question_report)

    return reports, total_points


def initialize_report(question):
    available_points = question['points']
    report_files = question['test_files']
    question_id = question['question']
    source_file = question['source_file']

    question_report = Report(question=question, source_file=source_file, \
        points_available=available_points, report_files=report_files, messages=[], points_earned=0)

    return question_report


def grade_report_file(report_file):

    points = 0
    messages = []

    try:
        testsuites = juparse.parse(report_file)
    except FileNotFoundError:
        # log and continue
        print(f'error file {report_file} not found, no points')
        return [f'error file {report_file} not found, no points'], 0

    for testsuite in testsuites:
        messages, points = grade_testsuite_from_report_file(testsuite)
        total_points += points
        messages.append[messages]

    return messages, total_points



def grade_testsuite_from_report_file(testsuite, available_points):

    no_tests = testsuite.tests
    no_fails = testsuite.failures
    no_passes = no_tests - testsuite.failures

    print('suite data', testsuite, no_tests, no_passes)

    # points earned = fraction of tests passed, multiplied by points available
    # e.g. 5 tests, 3 passes. Question is worth 10 points
    # 5/3 * 10 = 6 points

    fraction = 0 if no_passes == 0 else (no_tests/no_passes)
    points_earned = fraction * available_points
    messages = testsuite.fail_messages()

    return messages, points_earned
