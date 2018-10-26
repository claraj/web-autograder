from git import Repo, GitCommandError
import os
from .exceptions import CloneError

# token = os.environ['GITHUB_AUTOGRADER_ACCESS_TOKEN']

# This just works if you are authenticated to GitHub, like have a token saved.


def clone_or_pull_latest(repo_url, target_dir, repo_dir):

    """ Clone the given repo to location target_dir/repo_dir.
    If the dir already exists, attempt to git pull to get latest code.
    Error if directory already exists and it's remote origin is not the same URL as repo_url
    Error if repo not found. """

    print(target_dir, repo_dir)

    repo_target_dir = os.path.join(target_dir, repo_dir)

    try:
        repo = Repo.clone_from(repo_url, os.path.join(target_dir, repo_dir))
        return repo_target_dir, 'clone', get_latest_commit_sha(repo)

    except GitCommandError as e:
        if 'remote: Repository not found.' in e.stderr:
            # The URL isn't a repo
            raise CloneError(f'The URL {repo_url} was not found or not a git repository.')

        elif 'already exists and is not an empty directory' in e.stderr:
            # repo already exists. Is it the one we wanted to download? If so, pull latest
            # print('something already exists at location', target_dir, repo_dir)
            repo = Repo(repo_target_dir)

            try:
                origin = repo.remote('origin')
            except ValueError:
                raise CloneError(f'There is no origin remote for the contents of {repo_target_dir} to pull. Is this directory a git repository?')
                # this directory has something in it, but it's not a git repo

            if origin.url == repo_url:
                # this is the repo and it's already downloaded. Pull any changes
                try:
                    origin.pull()
                    return repo_target_dir, 'pull', get_latest_commit_sha(repo)
                except GitCommandError as e:
                    #Error pulling code - e.g. the remote history doesn't match the local history.
                    # raise CloneError(f'Error pulling code. The remote history may be different to local? Error: {e.stderr}')

                    # Or, aonther process is trying to clone this repo e.g. more than one task
                    # trying to clone the instructor repo.

                    # " Another git process seems to be running in this repository, e.g.
                    # an editor opened by 'git commit'. Please make sure all processes
                    # are terminated then try again. If it still fails, a git process
                    # may have crashed in this repository earlier: "

                    # TODO warn instead of crash.
                    print(f'error pulling code because {e.stderr}, continuing anyway')
                    return repo_target_dir, 'pull', get_latest_commit_sha(repo)

            else:
                raise CloneError(f'error cloning {repo_url} into {repo_target_dir} because {e.stderr}')
                # something else went wrong, throw the error

        else:
            # Some other error, throw
            raise CloneError(f'error cloning {repo_url} into {repo_target_dir} because {e.stderr}')



def get_latest_commit_sha(repo):
    head = repo.commit('HEAD')
    sha = head.hexsha
    return sha


if __name__ == '__main__':
    ex_repo_url = 'https://github.com/minneapolis-edu/temp'
    ex_dir = '/Users/admin/TEMP/repos/'
    err = clone_or_pull_latest(ex_repo_url, ex_dir, 'tempsdfsdf')
    print('is there an error?', err)
