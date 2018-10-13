# Read the JSON file with grades

# Assume test and grades/file are correct
#

import json
import os
import re

'''
Example schema: test_file might be an array OR single string (barf, fixme)

{ "week" : 9 ,
  "questions" : [
    {
      "question" : 1,
      "java_file": "TicketProgram.java",
      "test_file": "TicketTest.java",
      "points": 5
    },

    {
      "question" : 2,
      "java_file": "AnotherProgram.java",
      "test_file": ["SomeTicketTests.java", "YetMoreTests.java"]
      "points": 15
    },

  ]
}


'''


# scheme == json.load(grade_json_file)
def grade(project_location, test_set, scheme):  # test set e.g. week_1
    # Expect to have a file grages/week_1.json IN MY REPO NOT STUDENT REPO

    #filename = os.path.join(project_location, 'grades', test_set_name + '.json')

    # grade_json_file = os.path.join(project_location, 'grades', test_set + '.json')
    # scheme = json.load(open(grade_json_file))

    print('scheme is', scheme)


    # surefile report filenames look like this
    # test_package.testfile.txt
    # test_week_1.Test_Mail_Prices.txt

    # Open each file in the /target/surefire-reports dir

    '''

    -------------------------------------------------------------------------------
    Test set: week_1.TestNASAAstronaut
    -------------------------------------------------------------------------------
    Tests run: 1, Failures: 1, Errors: 0, Skipped: 0, Time elapsed: 0 s <<< FAILURE! - in test_week_1.TestNASAAstronaut
    testAstronautQualifications(week_1.TestNASAAstronaut)  Time elapsed: 0 s  <<< FAILURE!
    java.lang.AssertionError: Height = 60, swim = 75 should return true
    	at test_week_1.TestNASAAstronaut.testAstronautQualifications(TestNASAAstronaut.java:41)


    '''


    # Compare to filenames in json

    results = {}

    total_points = 0

    for item in scheme["questions"]:

        test_filenames = item['test_file']    # This is either a String or list. Ensure it is list
        java_filename = item['java_file']

        if type(test_filenames) is str:
            test_filename_list = [ test_filenames ]
        else:
            test_filename_list = test_filenames

        points_avail = item['points']

        run = 0
        passing_tests = 0
        errors = 0
        failures = 0
        # Find this report
        print(test_filenames)

        for test_filename in test_filename_list:

            try:
                report_filename = '%s.%s.txt' % (test_set, test_filename)
                print(report_filename)
                report_location = os.path.join(project_location, 'target', 'surefire-reports', report_filename)
                print(report_location)

                with open(report_location) as f:
                    report = f.readlines()
                    q_run, q_errors, q_failures = extract(report[3]) # ugh
                    print('test file results: Points %d, run %d , errors %d, fails %d' % (points_avail, q_run, q_errors, q_failures))
                    # So question is worth e.g. 5 points. 3 tests, 1 fails. Student gets 5/3 * 2 points for this

            except IOError:
                print("Can't find the test report file. " + report_location + " Either the tests haven't run, or there's a build error for this project. Returning None " + report_filename)
                #return None, None
                # just be zeros
                q_run, q_errors, q_failures = (0, 0, 0) # ugh


                # Either the name in week_1.json is wrong
                # Or, a MVN build error. TODO check for MVN build errors. One hacky way to to see if target/classes has anything in or not.
                # If the tests haven't run, this file doesn't exist. Caller should check for this being none.

            run = run + q_run
            errors = errors + q_errors
            failures = failures + q_failures

            print('after adding test file results: Points %d, run %d , errors %d, fails %d' % (points_avail, run, errors, failures))


        # For all tests for this question,
        passing_tests = run - (errors + failures)
        print("passing tests for this question", passing_tests)
        if run == 0:
            points_for_question = 0
        else:
            points_for_question = ( points_avail / run ) * passing_tests
        print('points earned for this question', points_for_question )
        total_points += points_for_question
        print('total points now ', total_points)
        results[java_filename] = points_for_question


    print('RESULTS', results, total_points)
    return results, total_points




def extract(line) :

    run = re.search('(?<=Tests run: )\d+', line).group(0)
    errors = re.search('(?<=Failures: )\d+', line).group(0)
    failures = re.search('(?<=Errors: )\d+', line).group(0)
    #print(run,errors, failures)
    return int(run), int(errors), int(failures)
