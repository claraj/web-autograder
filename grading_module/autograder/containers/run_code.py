import docker
from docker.types import Mount

import os
import json
import xml.etree.ElementTree as ET
'''

Need dockerfile location, from instructor repo

'''

instructor_code = '/Users/admin/Development/python/django_autograder/grader/grading_modules/example_java_assignment/JavaAutoGraderWeek3INSTRUCTOR'
student_code = '/Users/admin/Development/python/django_autograder/grader/grading_modules/example_java_assignment_docker/JAG_3_mock_student_code'

def grade():

    # student code should have target/surefire-reports/stuff.xml with names like
    #/Users/admin/Development/python/django_autograder/grader/grading_modules/example_java_assignment_docker/JAG_3_mock_student_code/target/surefire-reports/TEST-week_3.Question_2_Wear_A_HatTest.xml
    # File names are TEST-package.testfilename.xml

    # Parse some JSON, Parse some XML. How about some CSV and some YAML for fun?

    package, questions = grade_schema(instructor_code)

    points = 0

    for question in questions:
        points, messages = grade_question(question, package)
        print(points, messages)


def grade_question(question, package):
    test_files = question['test_file']

    messages = []
    # todo close file
    for test_file in test_files:
        # test_file is the filename of the Java junit tests
        xml_report = f'TEST-{package}.{test_file}.xml'
        xml = ET.parse(os.path.join(student_code, 'target', 'surefire-reports', xml_report))
        testsuite = xml.getroot()  # testsuite
        tests = int(testsuite.get('tests'))      # get gets attributes
        fails = int(testsuite.get('failures'))
        errors = int(testsuite.get('errors'))
        skipped = int(testsuite.get('skipped'))
        passes = tests - (fails+errors+skipped)

        for testcase in testsuite:   # iterate over children
            classname = testcase.get('classname')
            testname = testcase.get('name')
            failure = testcase.find('failure')  # find returns first matching child
            # print(failure)
            if failure is not None:  # elements with no children are considered false, so have to explicitly test if None
                # print(failure.text)  # The stack trace
                failmessage = failure.get('message')
            else:
                failmessage = 'Passed!'
            report = f'In the test class {classname}, for the test with name = {testname}, pass/fail/error {failmessage}'
            messages.append(report)

        return 0, messages





def grade_schema(location):
    data = json.load(open(os.path.join(location,'grades', 'week_3.json'), 'r'))
    return data['package'], data['questions']


def run_code_in_container():

    config = from_config_file(os.path.join(instructor_code, 'grades', 'config.json'), student_code)
    dockerfile_location = os.path.join(instructor_code, 'grades')

    tag = config['tag']
    config.pop('tag', None)
    image, logs = build_image(dockerfile_location, tag)
    print('the image is:' , image)
    print(type(image))
    print(image.id)
    print(image.tags)
    container_output = run_image(image.tags[0], config)

    print(container_output)


def from_config_file(path, student_code_dir):
    config_data = json.load(open(path, 'r'))
    print(config_data)
    docker_config = config_data['docker_config']
    mounts = docker_config['mounts']
    mounts_list = []
    if mounts:
        for mount in mounts:
            src = student_code_dir if mount['source'] == '$PWD' else mount['source']
            target = mount['target']
            type = mount['type'] if mount['type'] else 'volume'
            mounts_list.append(Mount(target, src, type=mount['type']))
    docker_config['mounts'] = mounts_list
    # docker_config.pop('tag', None)
    return docker_config


def build_image(dockerfile_location, tag):
    client = docker.from_env()
    image = client.images.build(path=dockerfile_location, tag=tag)
    return image


def run_image(image, config):

    client = docker.from_env()

    # pwd = '/Users/admin/Development/python/django_autograder/grader/grading_modules/example_java_assignment/JavaAutoGraderWeek3'
    # maven_cache_mount = Mount('/root/.m2', 'maven-repo', type='volume')
    # the_filesystem_mount = Mount('/usr/src/mymaven', pwd, type='bind')

    print('config will be', config, 'image is ', image)

    try:
        container = client.containers.run(image, stderr=True,  **config)
    except docker.errors.ContainerError as err:
        print('container error', err)  # if the java code won't compile, the mvn test command will error.
        return None
    # container = client.containers.run(\
    # image, \
    # mem_limit='512M', \
    # mounts=[maven_cache_mount, the_filesystem_mount], \
    # name='replace-with-better-name-maybe', \
    # remove=True, \
    # )


    return container

if __name__ == '__main__':
    # run_code_in_container()
    grade()


# container = client.containers.run('maven:3.5.4-jdk-10', \
# 'mvn clean test', \
# mem_limit='512M', \
# mounts=[maven_cache_mount, the_filesystem_mount], \
# name='replace-with-better-name-maybe', \
# remove=True, \
# tty=True, \
# working_dir='/usr/src/mymaven' \
# )

# docker build from instructor dockerfile will give the name of the image

# Using config from dockerfile

# The surefire reports are in the local code dir


# Example
'''
# Works with no dockerfile
docker run -it --rm --name my-maven-project --memory 512M -v maven-repo:/root/.m2 -v "$(pwd)":/usr/src/mymaven -w /usr/src/mymaven maven:3.5.4-jdk-10 mvn test

docker run -it --rm --name my-maven-project --memory 512M -v maven-repo:/root/.m2 -v "$(pwd)":/usr/src/mymaven -w /usr/src/mymaven maven-autograder:latest mvn test

docker run --rm --name my-maven-project --memory 512M -v maven-repo:/root/.m2 -v "$(pwd)":/usr/src/mymaven mvn-ag:latest

docker
run
-it
--rm
--name my-maven-project
--network none   // boo, have to get dependencies from mvn central
--memory 512M
-v maven-repo:/root/.m2
-v "$(pwd)":/usr/src/mymaven
-w /usr/src/mymaven
maven:3.5.4-jdk-10
mvn test

'''

# Surefire reports written to HOST filesystem but code runs in docker.