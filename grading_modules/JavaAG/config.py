
import json
### Per-lab stuff

# Info about the repository used.
# TODO important! Make sure this syncs with grade_item_url or you'll post grades in the wrong place
#lab_base_name = "assignment-2-loops-and-arrays"
week_name = "week_2"

download_mine = True
download_student = True
download = (download_mine, download_student)   # Whether to re-download ( my repo, student repos ) TEST MEEE!!

labs_data_file = 'class_data/github_classroom_assignment_names.json'
lab_info = json.load(open(labs_data_file))

print('lab info', lab_info)


# The URL of the grade all items for this week in D2L. See list in classdata/d2l_links
# d2l_grade_item_url = "https://minneapolis.ims.mnscu.edu/d2l/lms/grades/admin/enter/grade_item_edit.d2l?objectId=14229002&ou=3696835"
d2l_grade_item_url = lab_info[week_name]['d2l_url']
print('d2l grade item ', d2l_grade_item_url)

lab_base_name = lab_info[week_name]['lab_base_name']
print('lab base', lab_base_name)

my_original_repo = lab_info[week_name]['original_repo']

my_repo_name = my_original_repo.split('/')[-1]
print('my repo', my_repo_name)

test_set = week_name
print('test set aka week number', test_set)


### Global stuff

# File path with student name,github,id list
student_data_file = 'class_data/class_data.py'  # sigh

# Whether to download a new copy of student code from GitHub and copy my tests in
# Currently unused
clean_code = True

# All grades in SQLIte database with this file name
db_file = "db_jag.sqlite"

# Where to save student repos. Each has unique name.
download_student_code_dir = "student_code"
