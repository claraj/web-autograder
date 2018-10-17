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


import settings

# from autograder import container, directory, github, report, jsonparser
# from github import clone

from autograder.github import clone
from autograder.container import runner
from autograder.jsonparser import parser
from autograder.directory import combine
from autograder.report import report

from tempfile import TemporaryDirectory

import os

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
    assignment = A('https://github.com/minneapolis-edu/JAG_3', 'assignment-3-methods', 'mctc-itec')
    student = S('minneapolis-edu')
    r, s = grade(assignment, student)
    print(r, s)



def grade(assignment, student):
    instructor_code = fetch_instructor_code(assignment.instructor_repo)
    student_code = fetch_student_code(assignment.github_base, assignment.github_org, student.github_id)
    project_config = get_config(instructor_code)

    with TemporaryDirectory() as temp_student_code_dir:
        combine_code(instructor_code, student_code, project_config, temp_student_code_dir)
        run_code_in_container(temp_student_code_dir, project_config)
        report, score = generate_grade_report(temp_student_code_dir)

    return report, score


def fetch_student_code(base, org, student_id):
    url = f'https://github.com/{org}/{base}-{student_id}'
    repo_name = f'{base}-{student_id}'
    student_code_location, mode = clone.clone_or_pull_latest(url, os.path.join(settings.CODE_STORE, settings.STUDENT_CODE_LOCATION), repo_name)
    print('got student code by: ', mode)
    return student_code_location


def fetch_instructor_code(repo_url):
    repo_name = repo_url.split('/').pop()
    instructor_code_location, mode = clone.clone_or_pull_latest(repo_url, os.path.join(settings.CODE_STORE, settings.INSTRUCTOR_CODE_LOCATION), repo_name)
    print('got code by: ', mode)
    return instructor_code_location


def get_config(path):
    print('GET CONFIG', path,settings.GRADE_CONFIG_LOCATION, settings.CONFIG_FILENAME )
    config_dir = os.path.join(path, settings.GRADE_CONFIG_LOCATION, settings.CONFIG_FILENAME)
    config = parser.parse(config_dir)
    return config


def combine_code(instructor_code, student_code, config, combined_location):
    # combined_location = student_code + settings.STUDENT_COMBINED_SUFFIX
    # paths to overwrite are in config.student_code_locations
    combine.combine(instructor_code, student_code, config['student_code_locations'], combined_location+'COMB')


def run_code_in_container(path, config):
    runner.run_in_container(path, config)


def generate_grade_report(location):
    grade_report, score = report.create_report(location)  # report is CSV (probably) or some other organized text format.
    return grade_report, score


if __name__ == '__main__':
    example()

# import docker
# from docker.types import Mount
#
# import os
# import json
# import xml.etree.ElementTree as ET
# '''
#
# Need dockerfile location, from instructor repo
#
# '''
#
# instructor_code = '/Users/admin/Development/python/django_autograder/grader/grading_modules/example_java_assignment/JavaAutoGraderWeek3INSTRUCTOR'
# student_code = '/Users/admin/Development/python/django_autograder/grader/grading_modules/example_java_assignment_docker/JAG_3_mock_student_code'
#
# def grade():
#
#     # student code should have target/surefire-reports/stuff.xml with names like
#     #/Users/admin/Development/python/django_autograder/grader/grading_modules/example_java_assignment_docker/JAG_3_mock_student_code/target/surefire-reports/TEST-week_3.Question_2_Wear_A_HatTest.xml
#     # File names are TEST-package.testfilename.xml
#
#     # Parse some JSON, Parse some XML. How about some CSV and some YAML for fun?
#
#     package, questions = grade_schema(instructor_code)
#
#     points = 0
#
#     for question in questions:
#         points, messages = grade_question(question, package)
#         print(points, messages)
#
#
# def grade_question(question, package):
#     test_files = question['test_file']
#
#     messages = []
#     # todo close file
#     for test_file in test_files:
#         # test_file is the filename of the Java junit tests
#         xml_report = f'TEST-{package}.{test_file}.xml'
#         xml = ET.parse(os.path.join(student_code, 'target', 'surefire-reports', xml_report))
#         testsuite = xml.getroot()  # testsuite
#         tests = int(testsuite.get('tests'))      # get gets attributes
#         fails = int(testsuite.get('failures'))
#         errors = int(testsuite.get('errors'))
#         skipped = int(testsuite.get('skipped'))
#         passes = tests - (fails+errors+skipped)
#
#         for testcase in testsuite:   # iterate over children
#             classname = testcase.get('classname')
#             testname = testcase.get('name')
#             failure = testcase.find('failure')  # find returns first matching child
#             # print(failure)
#             if failure is not None:  # elements with no children are considered false, so have to explicitly test if None
#                 # print(failure.text)  # The stack trace
#                 failmessage = failure.get('message')
#             else:
#                 failmessage = 'Passed!'
#             report = f'In the test class {classname}, for the test with name = {testname}, pass/fail/error {failmessage}'
#             messages.append(report)
#
#         return 0, messages
#
#
#
#
#
# def grade_schema(location):
#     data = json.load(open(os.path.join(location,'grades', 'week_3.json'), 'r'))
#     return data['package'], data['questions']
#
#
# def run_code_in_container():
#
#     config = from_config_file(os.path.join(instructor_code, 'grades', 'config.json'), student_code)
#     dockerfile_location = os.path.join(instructor_code, 'grades')
#
#     tag = config['tag']
#     config.pop('tag', None)
#     image, logs = build_image(dockerfile_location, tag)
#     print('the image is:' , image)
#     print(type(image))
#     print(image.id)
#     print(image.tags)
#     container_output = run_image(image.tags[0], config)
#
#     print(container_output)
#
#
# def from_config_file(path, student_code_dir):
#     config_data = json.load(open(path, 'r'))
#     print(config_data)
#     docker_config = config_data['docker_config']
#     mounts = docker_config['mounts']
#     mounts_list = []
#     if mounts:
#         for mount in mounts:
#             src = student_code_dir if mount['source'] == '$PWD' else mount['source']
#             target = mount['target']
#             type = mount['type'] if mount['type'] else 'volume'
#             mounts_list.append(Mount(target, src, type=mount['type']))
#     docker_config['mounts'] = mounts_list
#     # docker_config.pop('tag', None)
#     return docker_config
#
#
# def build_image(dockerfile_location, tag):
#     client = docker.from_env()
#     image = client.images.build(path=dockerfile_location, tag=tag)
#     return image
#
#
# def run_image(image, config):
#
#     client = docker.from_env()
#
#     # pwd = '/Users/admin/Development/python/django_autograder/grader/grading_modules/example_java_assignment/JavaAutoGraderWeek3'
#     # maven_cache_mount = Mount('/root/.m2', 'maven-repo', type='volume')
#     # the_filesystem_mount = Mount('/usr/src/mymaven', pwd, type='bind')
#
#     print('config will be', config, 'image is ', image)
#
#     try:
#         container = client.containers.run(image, stderr=True,  **config)
#     except docker.errors.ContainerError as err:
#         print('container error', err)  # if the java code won't compile, the mvn test command will error.
#         return None
#     # container = client.containers.run(\
#     # image, \
#     # mem_limit='512M', \
#     # mounts=[maven_cache_mount, the_filesystem_mount], \
#     # name='replace-with-better-name-maybe', \
#     # remove=True, \
#     # )
#
#
#     return container
#
# if __name__ == '__main__':
#     # run_code_in_container()
#     grade()
#
#
# # container = client.containers.run('maven:3.5.4-jdk-10', \
# # 'mvn clean test', \
# # mem_limit='512M', \
# # mounts=[maven_cache_mount, the_filesystem_mount], \
# # name='replace-with-better-name-maybe', \
# # remove=True, \
# # tty=True, \
# # working_dir='/usr/src/mymaven' \
# # )
#
# # docker build from instructor dockerfile will give the name of the image
#
# # Using config from dockerfile
#
# # The surefire reports are in the local code dir
#
#
# # Example
# '''
# # Works with no dockerfile
# docker run -it --rm --name my-maven-project --memory 512M -v maven-repo:/root/.m2 -v "$(pwd)":/usr/src/mymaven -w /usr/src/mymaven maven:3.5.4-jdk-10 mvn test
#
# docker run -it --rm --name my-maven-project --memory 512M -v maven-repo:/root/.m2 -v "$(pwd)":/usr/src/mymaven -w /usr/src/mymaven maven-autograder:latest mvn test
#
# docker run --rm --name my-maven-project --memory 512M -v maven-repo:/root/.m2 -v "$(pwd)":/usr/src/mymaven mvn-ag:latest
#
# docker
# run
# -it
# --rm
# --name my-maven-project
# --network none   // boo, have to get dependencies from mvn central
# --memory 512M
# -v maven-repo:/root/.m2
# -v "$(pwd)":/usr/src/mymaven
# -w /usr/src/mymaven
# maven:3.5.4-jdk-10
# mvn test
#
# '''
#
# # Surefire reports written to HOST filesystem but code runs in docker.
