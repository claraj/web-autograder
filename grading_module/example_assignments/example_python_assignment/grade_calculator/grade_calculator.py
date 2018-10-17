# STUDENTS: you DON'T need to modify this file!

# This program read in the lab's JSON file, run tests, figure out points.
# Instructor: remember to edit the grades.json file to assign appropriate points for each lab question.
#  (Students, note that the instructor's copy of grades.json is used for grading :)

# Credit to helpful stack overflow.
# https://stackoverflow.com/questions/14282783/call-a-python-unittest-from-another-script-and-export-all-the-error-messages

import json
import os
import unittest
import importlib
import inspect
import sys

# Add one directory up to python path so can run this script from command line.
script_loc = sys.path[0]
sys.path.append(os.path.join(script_loc, '..'))

grade_json_file = 'grades.json'  # Modify this if the filename with points and test files is changed
test_out_file = 'test_report.txt'
round_grades_to = 2  # how many decimal places?  Unused at the moment.
report_directory = 'reports'


def calc():

    """ Run tests in a lab package (directory) and calculate grade from grades.json
    """

    # Read in the grades.json from grades.json
    # This does some verification of the JSON, including that the points per assignment sum sensibly.
    assignment = read_grade_json()

    total_points = assignment.total_points

    print('Total points for this assignment:', total_points)

    messages = []

    points_earned = 0

    for question in assignment.questions:

        print()

        test_file = question['test_file']
        question_points = question['points']
        question_name = question['name']

        print('Points available for question %s:' % question_name, question_points)

        results = run_test(test_file)

        if not results:
            print('No tests found in test file %s, skipping, no points assigned' % test_file)
            continue

        total_tests_run = 0
        total_fails = 0
        total_errors = 0

        for result in results:

            total_tests_run += result.testsRun
            total_fails += len(result.failures)
            total_errors += len(result.errors)

            for err in result.errors:
                messages.append(err)

            for fail in result.failures:
                messages.append(fail)

            # For debugging, remove after testing
            print('Result: total points %s total tests %s total fails %s total errors %s' % (question_points, total_tests_run, total_fails, total_errors))

        # Points proportional to number of passing tests
        # So if there are 10 points for the question, and 3 out of 5 tests pass,
        # the assignment receives 6 points.

        passing_tests = total_tests_run - (total_errors + total_fails)

        if passing_tests == 0:
            points_for_question = 0  # Avoid divide by zero errors
        else:
            points_for_question = (passing_tests / total_tests_run) * question_points

        print('points earned for question %s' % question_name, points_for_question)
        points_earned += points_for_question


    return points_earned, messages


def run_test(test_file):

    """
    :param lab: name of directory containing the lab materials
    :param test_file: the test file name, read from JSON. The module/package is assumed
    :return: test results.
    """

    test_file = 'tests.%s' % test_file

    try:
        test_package = importlib.import_module(test_file)
    except ModuleNotFoundError as err:
        sys.exit('Unable to calculate grades. Please report this to the instructor.', err)

    objects = [m[1] for m in inspect.getmembers(test_package) if inspect.isclass(m[1])]
    #print('objects', objects)

    results = []

    for obj in objects:

        # Create test runner
        # Dump test output into text file to not clutter console output.
        # test_out_file is human-readable, may be used for debugging


        # Skip the superclass TestCase
        if 'unittest.case.TestCase' in str(obj):
            continue

        report_file = os.path.join(script_loc, report_directory, test_file + '_report.txt')

        with open(report_file, 'w') as stream:
            runner = unittest.TextTestRunner(stream)

            result = runner.run(unittest.makeSuite(obj))
            #print('this many tests were run', result.testsRun)

            results.append(result)


    return results



class GradeData:
    def __init__(self, gradejson):
        self.__dict__ = json.loads(gradejson)


def read_grade_json():

    filename = os.path.join(script_loc, '..', grade_json_file)

    with open(filename) as f:
        grade_json = f.read()
        assignment = GradeData(grade_json)

    # Verify that the total points == sum of individual assignments

    total_points = assignment.total_points
    question_points = 0

    for question in assignment.questions:
        question_points += question['points']

    assert question_points == total_points, 'Total points for each question in ' + filename \
                                            + ' must sum to the same value as total_points.'
    assert question_points > 0

    return assignment


# test

# Make report directory
os.makedirs(os.path.join(script_loc, report_directory), exist_ok=True)

pts, msgs = calc()
print('\nSUMMARY\n')
print('TOTAL POINTS:', pts)
# print('MESSAGES', msgs)   # TODO replace with user-friendly message
print('Full test results in the files in this directory: ' + os.path.join(os.getcwd(), report_directory))
