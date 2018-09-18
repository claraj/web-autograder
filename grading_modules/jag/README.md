This program should run as the autograder user
Autograder doesn't have permission to modify anything that it doesn't own.

su autograder

cd /Users/autograder/Autograder


jag.py is the main entry point to this application.


cache git credentials

git config --global credential.helper cache


security create-keychain

open -a atom .    // open as logged in user?

## TODO

Make keychain for autograder user

OR download as minneapolis-edu, test (like delete) as Autograder. Publish as either minneapolis-edu or Autograder

Be able to re-run tests on student repo that I have edited - don't redownload, don't re-replace test  (Can do with Maven)

Autogen a snippet to post in D2L with report of test fails


grade_publisher - what if calc grade is 12 but there is an already published grade? Warn and don't overwrite. Need to pull value attr from input. Why not work?



Handle errors.
* Empty repository,
* No repository
* no code in repo
* Code does not compile
* test hangs, gets stuck in loop

- Need to get a timeout for tests that run forever


Maven dependencies, download once and put in shared location, not for each repo
Consider copying student code to my project?? But that could miss other files.

Creating a text file of student info student_data.txt to fetch, once students have configured their GitHubs  

Reading the SQLlite database and uploading to D2L -> wait until D2L new design launches and have done Java class setup so know names of elements and things to find.

Comment analyzer

Deal with non-compiling code?

Deal with grades/week_X.json not adding up to 20

Extra credit tokens

Am copying grades folder with JSON over  - yes, am using


Print better report

Figure out the github keychain for autograder user. maybe another github account with permissions just for this project?  

Delete permissions for donwloaded code, project can't delete right now, no x permission on dirs downloaded?


Atom plugin to 'comment' and uncomment .txt files


# TODO

ignore test files that pass when students get code.
just don't list them in grades.json.
