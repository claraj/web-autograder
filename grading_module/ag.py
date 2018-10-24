"""
This module will be given a student, an assignment, and then:

- Download the instructor code. git pull if it already exists .
- Download the student code (git pull if it already exists. )
- Do any copying/editing to student code dir and make new copy of code
     -- look in instructorrepo/grades/config for list of student dirs to copy into a copy of the instructor repo.
- Instructor repo should have Dockerfile with any pre-test installs and test command in.
- Create volume and mount at test result location. Test results are expected to be written to the volume
- Create docker image and start container which will run tests. Test result file(s) should end up in the volume
- Copy report(s) out of volume
- delete volume & container (OR prefix all reports with unique name and use one volume?)
- Figure out score from reports and grades.json
- return text of reports and score
"""

## To run this file by itself.... python -m grading_module.ag  from dir above grading_module

import sys
import traceback
import os
import json
from tempfile import TemporaryDirectory

from . import settings

from .autograder.github import clone
from .autograder.container import runner
from .autograder.jsonparser import parser
from .autograder.directory import combine
from .autograder.report import report
from .autograder.models.json_encoders import TestItemEncoder

# import settings
#
# from autograder.github import clone
# from autograder.container import runner
# from autograder.jsonparser import parser
# from autograder.directory import combine
# from autograder.report import report
# from autograder.models.json_encoders import TestItemEncoder

'''
All of these steps can error.
Let them, ensure exceptions have useful error message,
and caller can deal with problem.
'''

# temp for testing
class A:
    def __init__(self, in_repo, base, org):
        self.instructor_repo = in_repo
        self.github_base = base
        self.github_org = org

class S:
    def __init__(self, gh_id):
        self.github_id = gh_id

def example():

    # Java example
    # assignment = A('https://github.com/minneapolis-edu/JAG_3', 'assignment-3-methods', 'mctc-itec')
    # student = S('minneapolis-edu')

     # Python example
    assignment = A('https://github.com/minneapolis-edu/PAG_5', 'python-week-5-dictionaries', 'mctc-itec')
    student = S('minneapolis-edu')

    result = grade(assignment, student)
    print(result)


def grade(assignment, student):

    try:

        instructor_code = fetch_instructor_code(assignment.instructor_repo)

        try:
            student_code, err = fetch_student_code(assignment.github_base, assignment.github_org, student.github_id)
        except Exception as e:
            return { 'success': True, 'result': (f'Error fetching student code, {e}', 0) }

        project_config = get_config(instructor_code)
        grade_scheme = get_grade_scheme(instructor_code)

        with TemporaryDirectory(dir=settings.COMBINED_CODE_LOCATION) as temp_student_code_dir:
            combined = combine_code(instructor_code, student_code, project_config, temp_student_code_dir)
            try:
                run_code_in_container(combined, project_config)
            except Exception as e:
                # Could be compile errors, code crashed etc.
                t, e, tb = sys.exc_info()
                print(traceback.print_tb(tb))

                return { 'success': True, 'result': (f'Error running tests on student code, {e}', 0) }

            try:
                report, score = generate_grade_report(combined, project_config, grade_scheme)
            except Exception as e:
                t, e, tb = sys.exc_info()
                print(traceback.print_tb(tb))
                
                return { 'success': True, 'result': (f'Error reading test report files from student code, {e}', 0) }

            # input('done. press a key')

        return { 'success': True, 'result': (report, score) }

    except Exception as e:

        # These are most likely errors that I have caused, or from modifications of the project structure between student and instructor.
        t, e, tb = sys.exc_info()
        print(traceback.print_tb(tb))
        return { 'success': False, 'error': e }


def fetch_student_code(base, org, student_id):

    url = f'https://github.com/{org}/{base}-{student_id}'
    repo_name = f'{base}-{student_id}'

    student_code_location, mode = clone.clone_or_pull_latest(url, os.path.join(settings.CODE_STORE, settings.STUDENT_CODE_LOCATION), repo_name)
    print('got student code by: ', mode)
    return student_code_location, None



def fetch_instructor_code(repo_url):
    repo_name = repo_url.split('/').pop()
    instructor_code_location, mode = clone.clone_or_pull_latest(repo_url, os.path.join(settings.CODE_STORE, settings.INSTRUCTOR_CODE_LOCATION), repo_name)
    print('got code by: ', mode)
    return instructor_code_location


def get_config(path):
    config_dir = os.path.join(path, settings.GRADE_CONFIG_LOCATION, settings.CONFIG_FILENAME)
    config = parser.parse(config_dir)
    return config


def get_grade_scheme(path):
    config_dir = os.path.join(path, settings.GRADE_CONFIG_LOCATION, settings.GRADE_SCHEME_FILENAME)
    config = parser.parse(config_dir)
    return config


def combine_code(instructor_code, student_code, config, combined_location):
    # combined_location = student_code + settings.STUDENT_COMBINED_SUFFIX
    # paths to overwrite are in config.student_code_locations
    code = os.path.join(combined_location, 'code')
    combine.combine(instructor_code, student_code, config['student_code_locations'], code)
    return code


def run_code_in_container(path, config):
    runner.run_in_container(path, config)


def generate_grade_report(location, config, scheme):
    reports_dir = config['report_location']
    test_report_location = os.path.join(location, reports_dir)
    print(test_report_location)
    grade_report_list, score = report.grade(test_report_location, scheme)  # report could be CSV (probably) or some other organized text format.
    for r in grade_report_list:
        print('REPORT IS', r)

    strr = [str(r) for r in grade_report_list]
    print('STRR', strr)

    return '\n'.join( [str(r) for r in grade_report_list] ), score


if __name__ == '__main__':
    example()
