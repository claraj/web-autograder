
import db
import repo_cloner as cloner
import grader
import tester
#import add_extra_credit
import os
import pwd
import sys
import json

import config

download_dir = config.download_student_code_dir

## TODO CHANGE THESE THINGS TO GRADE A DIFFERENT WEEK

#original_repo = "git://github.com/minneapolis-edu/JAG_2"
#original_repo = config.my_original_repo   # unused?

#grade_json = "grades"
#test_set = 'week_1'

#my_repo = 'JAG_2'
my_repo = config.my_repo_name

test_set = config.test_set

#An optimistic name. The manager of grading one week.

def autograde(lab_base_name, week_name, download):

    # Which set of tests to run? or all?

    #test_sets = which_tests()  # TODO return to this, but chance are, grade all.

    # load student data

    student_data = db.load_student_data(config.student_data_file)

    print(student_data)


    # Week 1 repo is called JAG_1

    #for test_set in test_sets:
    #print('\n\n**** TESTING TEST SET ' + test_set + " ****\n\n")

    #student_repos = db.get_repo_list()

    # Get my stuff from git, has original tests etc.

    if download[0]:
        cloner.clone('minneapolis-edu', my_repo, download_dir)

    grade_json_file = os.path.join(download_dir, my_repo, 'grades', test_set + '.json')

    grade_scheme = json.load(open(grade_json_file))
    print('Grade scheme used will be ' + str(grade_scheme))



    for student in student_data:


        print('\n\n**** Grading Student ' + student[1] + " " + student[0] + ' *****\n\n')
        student_github_id = student[1]

        their_repo = lab_base_name + '-' + student_github_id

        # Comment these lines to NOT overwrite student code

        if download[1]:
            repo_fetched = cloner.clone('mctc-itec', their_repo, download_dir)  # download_dir = student_code
        else:
            repo_fetched = True  # ummmmmmm....TODO check if exists

        if not repo_fetched:
            print("The repo " + their_repo + " was not found. Skipping this student.")
            continue

        tester.fetch_tests(download_dir, their_repo, my_repo)

        # TODO Check if code builds?  Student needs to fix build errors before any grading happens

        # Run tests
        if tester.test(download_dir, their_repo) == 'build error':
            total = 0
            results = {}

        else:
            # Grade
            print('down', download_dir)
            print('their repo', their_repo)
            print('test', test_set)

            results, total = grader.grade(os.path.join(download_dir, their_repo), test_set, grade_scheme)

            if not results or not total:
                print("ERROR no results generated for " + student[0] + " " + student[1] + "Check for surefile reports generated, does student code compile?")
                continue


            # Find extra credit tokens for this student
            week_number = int(week_name.replace('week_', ''))
            #extra_credit_tokens = add_extra_credit.token_search(student_name, week_number, len(results))

            # save to DB as entry in grade table
            #if extra_credit_tokens:
                # name, week_1, [3, 4]   <- list of questions to add a point
                #db.save_extra_credit(student[0], test_set, extra_credit_tokens)


        print('\n\nResults for student ' + student[2] + "\n" + str(results) + "\nTotal points: " + str(total) + '\n\n')

        db.save_results(student[0], test_set, results, total) # starID, week_1, dictionary of results, total points




    # Print a summary

    print("SUMMARY OF LAB: " + week_name)

    for student in student_data:
        print(student[0], db.grade_for_lab(student[0], week_name))





def which_tests():

    args = sys.argv[1:]
    if not args:
        all_tests = input("all the tests? are you sure? \nPress y to run all, anything else to quit: ")
        if all_tests == "y":
            args = db.get_all_test_names('test_sets.txt')
        else:
            print('quit. Try running with names of test sets, e.g. python jag.py week_1 week_3')
            sys.exit()


    # TODO  check for valid test_set names
    return args
