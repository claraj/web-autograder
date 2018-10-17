# Python
# not Java
# I like Python
# Java is ok too

'''

Original, starter code with grades/week_1.json and tests at (example)
https://github.com/minneapolis-edu/JAG_1/
or on this computer


Student setup:
  1. Create repo through GitHub classroom
  2. Work with repo with URL of the form
https://github.com/mctc-itec/assignment-1-variables-and-conditional-statements-zoomeko
https://github.com/mctc-itec/githubAssignmentName-studentGitHubName


Steps to autograde

1. Have DB of student names, and IDs, GitHub IDs  (s)
2. For each weekly lab, have a JSON or text file with the points for each assignment
3. Use surefire plugin to run test report

For each week...

  For each student repo....

    0. figure out git repo name
    1. git clone the code. Save location somewhere
    2. mvn test    <- generates surefire .txt and .xml reports
    3. Read surefire reports, probably as .txt, compare to rubric and calculate grade
    4. Save grade to db  [ starID, code_location, week, grade ]

  Once all grades for a week are done,
    1. Use selenium to log into D2L
    2. Navigate to grade entry area
    2. Enter grades for each student and save.


'''



import grade_one_week
import os, pwd
import sys

import config


def main():

    # if len(sys.argv) <= 2:
    #     week = sys.argv[1]
    #

    lab_base_name = config.lab_base_name
    week_name = config.week_name
    download = config.download



    grade_one_week.autograde(lab_base_name, week_name, download)


if __name__ == '__main__':

    # Ensure are running as autograder user. No deleting things as su!

    print(os.getenv('USERNAME'))
    print(os.getlogin())  # admin?

    process_owner = pwd.getpwuid(os.getuid())[0]

    print('The process owner is ' + process_owner)
    assert(process_owner == 'autograder')

    main()
