import docker
from docker.types import Mount

import os
import json
'''
Need dockerfile location, from instructor repo

'''

def run_code_in_container():

    instructor_code = '/Users/admin/Development/python/django_autograder/grader/grading_modules/example_java_assignment/JavaAutoGraderWeek3'
    student_code = '/Users/admin/Development/python/django_autograder/grader/grading_modules/example_java_assignment_docker/JAG_3_mock_student_code'

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

    container = client.containers.run(image, stderr=True,  **config)

    # container = client.containers.run(\
    # image, \
    # mem_limit='512M', \
    # mounts=[maven_cache_mount, the_filesystem_mount], \
    # name='replace-with-better-name-maybe', \
    # remove=True, \
    # )


    return container

if __name__ == '__main__':
    run_code_in_container()

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
