# mvn test for each student repository to populate the test reports.

# mvn -f path/to/place/with/pom.xml test

import os
import shutil

### TODO handle tests hanging. Build in a timeout.

def test(download_dir, student_repo_name):

    # Install maven dependencies NO DONT DO THIS NEED CACHE OF dependencies ?

    project_dir = os.path.join(download_dir, student_repo_name)


    # -q supresses [INFO] messages
    # -f which pom file to use


    # This builds the project too
    #mvn_install_command = 'mvn -f %s/%s/%s install' % (download_dir, student_github_id, repo_name)
    mvn_install_command = 'mvn -q -f %s install' % project_dir

    print('\nInstalling project dependencies\n')

    os.system(mvn_install_command)


    classes_dir = os.path.join(project_dir, 'target', 'classes')
    try:
        classes_files = os.listdir(classes_dir)
    except OSError:
        return 'build error'
    if not classes_files:
        return 'build error'



    # test_command = 'mvn -f %s/%s/%s test' % (download_dir, student_github_id, repo_name)
    test_command = 'mvn -q -f %s test' % project_dir

    os.system(test_command)

    # TODO handle errors

    # TODO if the build failed then target/classes will be empty. Report error to caller.




#              student_code     week-1-variables-bob      JAG_1
def fetch_tests(download_dir, student_github_directory, source_repo_name):
    # Copy tests from MY repo to student repo. Overwrite any tests that may have been changed.

    # Delete tests from student repo

    student_project = os.path.join(download_dir, student_github_directory)
    print('student project dir', student_project)

    student_test_path = os.path.join(student_project, 'src')  # the /src/test dir
    student_test_dir = os.path.join(student_project, 'src', 'test')  # the /src/test dir

    student_grade_scheme = os.path.join(student_project, 'grades')


    #print(student_test_dir)

    # Verify this works - this could destroy a lot of stuff!
    shutil.rmtree(student_test_dir)
    shutil.rmtree(student_grade_scheme)


    # Copy in the original repo tests

    original_project = os.path.join(download_dir, source_repo_name)

    original_tests_path = os.path.join(original_project, 'src', 'test')

    original_grade_scheme_dir = os.path.join(original_project, 'grades')


    shutil.copytree(original_tests_path, student_test_dir)

    # Copy in the original JSON grade rubric
    #print(original_grade_scheme_dir)
    #print(student_project)
    shutil.copytree(original_grade_scheme_dir, student_grade_scheme)
