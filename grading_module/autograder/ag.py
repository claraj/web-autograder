# """
# This module will be given a student, an assignment, and then:
#
# - Download the instructor code. git pull if it already exists .
# - Download the student code (git pull if it already exists. )
# - Do any copying/editing to student code dir and make new copy of code
#      -- look in instructorrepo/grades/config for list of student dirs to copy into a copy of the instructor repo.
# - Instructor repo should have Dockerfile with any pre-test installs and test command in.
# - Create volume and mount at test result location. Test results are expected to be written to the volume
# - Create docker image and start container which will run tests. Test result file(s) should end up in the volume
# - Copy report(s) out of volume
# - delete volume & container (OR prefix all reports with unique name and use one volume?)
# - Figure out score from reports and grades.json
# - return text of reports and score
# """
#
#
# import settings
# from githuboperations.ops import clone_or_pull_latest
# from containers import run_code
# from files import combine
# from grade_calc import report
#
#
# '''
# All of these steps can error. Let them, ensure exceptions have useful error message,
# and caller can deal with problem.
# '''
#
#
# def grade(assignment, student):
#     instructor_code = fetch_instructor_code(assignment.instructor_repo)
#     student_code = fetch_student_code(assignment.github_base, assignment.github_org, student.github_id)
#     project_to_grade = combine_code(student_code, instructor_code)
#     run_code_in_container(project_to_grade)
#     report, score = generate_grade_report(project_to_grade)
#     return report, score
#
#
# def fetch_student_code(base, org, student_id):
#     url = f'https://github.com/{org}/{base}-{student_id}'
#     repo_name = f'{base}-{student_id}'
#     clone_or_pull_latest(url, os.path.join(settings.CODE_STORE, settings.STUDENT_DIR), repo_name)
#
#
# def fetch_instructor_code(repo_url):
#     repo_name = repo_url.split['/'][:-1]
#     clone_or_pull_latest(repo_url, os.path.join(settings.CODE_STORE, settings.INSTRUCTOR_DIR), repo_name)
#
#
# def combine_code(student_code, instructor_code):
#     combined_location = combine.combine_projects(student_code, instructor_code)
#     return combined_location
#
#
# def run_code_in_container(location):
#     run_code.run_in_container(location)
#
#
# def generate_grade_report(location):
#     report, score = report.create_report(location)  # report is CSV (probably) or some other organized text format.
#     return report, score
