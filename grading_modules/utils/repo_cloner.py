import os
import shutil
# For each student, download the appropriate repository to a given location
# Each repo for each student/week has unique name


# example:  student_code/student_github/test_set
# example student_code/clara-mctc/week_1

#       minneapolis-edu    JAG_2            student_code
#       bobStudent  asignment-1-bobStudent  student_code
def clone(github_id, repo_name, download_dir):


    # Todo test if download_dir is present

    try:
        os.mkdir(download_dir)  # no error if already exists
    except:
        pass # no problem


    # delete if exists already; get a fresh copy

    directory = os.path.join(download_dir, repo_name)
    print(directory)
    try:
        shutil.rmtree(directory)
        pass
    except Exception as e:
        print('code does not exist already or error. ', e)

    # git clone URL dirname e.g.
    # command = 'git clone git://github.com/%s/%s %s/%s/%s' % (github_id, repo_name, download_dir, github_id, test_set)

    repo_url = 'https://github.com/%s/%s' % (github_id, repo_name)
    print(repo_url)

    command = 'git clone --recursive https://github.com/%s/%s %s/%s' % (github_id, repo_name, download_dir, repo_name)
    os.system(command)


    # Does directory exist?

    print("The repo exists?, is there is something at " + directory )
    print(os.path.exists(directory))

    return os.path.exists(directory)

    # TODO test for and handle errors e.g code is already downloaded
    # TODO repo may not exist
