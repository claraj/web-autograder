import os.path


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

CODE_STORE = 'code_store'

# Where instructor code is cloned to
INSTRUCTOR_DIR = 'instructor_code'

# Where student code is cloned to
STUDENT_DIR = 'student_code'

CODE_STORE_LOCATION = os.path.join(BASE_DIR, CODE_STORE)

INSTRUCTOR_CODE_LOCATION = os.path.join(CODE_STORE_LOCATION, INSTRUCTOR_DIR)
STUDENT_CODE_LOCATION = os.path.join(CODE_STORE_LOCATION, STUDENT_DIR)

# Directory suffix for combined code
COMBINED_SUFFIX = '_combined'

# Location of config and grades.json files in a assignment repository
ASSIGNMENT_GRADE_CONFIG_LOCATION = 'grades'

# Container configuration file location in an assignment repository
CONTAINER_CONFIGURATION_LOCATION = '/'
