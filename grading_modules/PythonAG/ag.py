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
