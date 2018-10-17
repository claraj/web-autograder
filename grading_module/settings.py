import os

# The directory that contains this settings.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CODE_STORE = 'code_store'

# Where instructor code is cloned to
INSTRUCTOR_DIR = 'instructor_code'

# Where student code is cloned to
STUDENT_DIR = 'student_code'

STUDENT_INSTRUCTOR_COMBINED = 'temp_combined'

CODE_STORE_LOCATION = os.path.join(BASE_DIR, CODE_STORE)

INSTRUCTOR_CODE_LOCATION = os.path.join(CODE_STORE_LOCATION, INSTRUCTOR_DIR)
STUDENT_CODE_LOCATION = os.path.join(CODE_STORE_LOCATION, STUDENT_DIR)

# Directory suffix for combined code
COMBINED_CODE_LOCATION = os.path.join(CODE_STORE_LOCATION, STUDENT_INSTRUCTOR_COMBINED)


# Location of config.json and grades.json files in a assignment repository
GRADE_CONFIG_LOCATION = 'grades'

# Assignment configuration filename
CONFIG_FILENAME = 'config.json'

# Filename with grade schema.
GRADE_SCHEME_FILENAME = 'grades.json'

# Container configuration file location in an assignment repository
CONTAINER_CONFIGURATION_LOCATION = '/'
