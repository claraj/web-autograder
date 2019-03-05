# Installs 

git:  
- sudo apt install git 
Java 11: 
- https://askubuntu.com/questions/508546/howto-upgrade-java-on-ubuntu-14-04-lts 
Maven: 
- sudo apt install maven
- set JAVA_HOME, possibly /usr/bin/java
node
- sudo apt install node npm
Python
- use pyenv
- https://github.com/pyenv/pyenv 
- install a bunch of other dependencies first https://bugs.python.org/issue31652 

Clone repo
- git clone https://github.com/claraj/web-autograder 

Set up database
- python manage.py migrate

Install dependencies
- pip install -r requirements.txt

Install Vue dependencies 
- cd grader_client
- npm i 


# Github

Create a auth token, save to machine

# Running 

Run server, from root 
- python manage.py qcluster 
- python manage.py runserver 

Run client from grader_client
- npm start 

(or run go_grader script. Copy it to /usr/local/bin to avoid ./go_grader)

Site at 127.0.0.0:3000/spa