import os
import requests
import logging
logger = logging.getLogger(__name__)


def findFile(repo_url, file):

    """ file might be a regular filename 'code.java' or a package+file 'package.code.java' or just the name without extension 'code' """

    if not repo_url or not file:
        logger.info('Provide file and repository URL. Can\'t search')
        return None

    TOKEN = os.environ.get('GITHUB_TOKEN', None)
    if TOKEN == None:
        logger.warning('No Github token, can\'t guess Github URLs')
        return None

    headers = {'Authorization': f'token {TOKEN}'}
    print('repo_url', repo_url)
    repo_parts = repo_url.split('/')[-2:]
    repo = '/'.join(repo_parts)
    print('repo name', repo)

    # params = {'q': f'repo:{repo}+filename:{file}'}   # Nope
    params = {'q': f'{file}+repo:{repo}'}

    print(params)

    # for some reason, the filename:hello query does not work. Search by name and filter out unlikely results.
    r = requests.get('https://api.github.com/search/code', params=params, headers=headers)
    response = r.json()
    print(r.url)

    if 'items' in response:
        name_path = { item['path']: item['name'] for item in response['items']}
        print(name_path)
        name_path = { item['path']: item['name'] for item in response['items'] if is_likely(item, file)}
        print('names and paths', name_path)

        if name_path:
            # Generate full URL and return first thing in dictionary
            for path, name in name_path.items():
                full_url = f'{repo_url}/blob/master/{path}'
                print(full_url)
                return(full_url)

    else:
        return None


def is_likely(item, search_name):
    name = item['name'].lower()
    path = item['path'].lower()
    search_name = search_name.lower()

    print(name, path, search_name)

    if 'test' not in search_name and ('test' in path or 'test' in name):
        return False

    not_student_code = ['pom.xml', 'workspace.xml', 'grade_scheme.json', 'readme.md']
    if name in not_student_code:
        return False

    extension = name.split('.')[-1:]
    print(extension)

    not_student_code_extensions = ['json', 'xml', 'md', 'jpg', 'jpeg', 'png', 'gradle']
    if extension in not_student_code_extensions:
        return False

    return True

# Testing....
if __name__ == '__main__':
    findFile('https://github.com/mctc-itec/python-week-5-dictionaries-achrastek',  'hello')
