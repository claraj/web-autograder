
import getpass
from selenium import webdriver
import time
import db
import config
import sys

### TODO handle students who have dropped.

d2l_home = 'https://minneapolis.learn.minnstate.edu'

big_warning_message = "IMPORTANT!! THESE ARE PROVISIONAL GRADES GENERATED AND PUBLISHED BY A COMPUTER. THEY MAY CHANGE (like, increase OR decrease) WHEN CLARA HAS REVIEWED YOUR WORK"

def post_grades(grade_item, grade_data):

	browser = webdriver.Firefox()
	browser.implicitly_wait(3)

	students = get_student_name_list()


	try:
		# D2L Homepage
		username = "we4954cp"
		password = getpass.getpass("enter d2l password: ")

		login(browser, username, password)

		navigateToGrades(browser, students)

		inputGrades(browser)

	except Exception as e:
		print('An exception happened.')
		print(e)
		browser.quit()



def login(browser, username, password):


	browser.get(d2l_home)

	login_form = browser.find_element_by_name("processLogonForm")

	login_box = browser.find_element_by_id("Username")
	login_box.send_keys(username)

	password_box = browser.find_element_by_id("Password")
	password_box.send_keys(password)

	login_form.submit()


def navigateToGrades(browser, students):

	#java_grades_home_url = 'https://minneapolis.ims.mnscu.edu/d2l/lms/grades/admin/enter/user_list_view.d2l?ou=3696835'

	# TODO avoid hard-coding

	# Find the lab to be graded

	time.sleep(2)  # implicitly_wait doesn't seem to hold long enough... waiting for login? time.sleep() is hacky but simple... and only needs to be done once.
	# Can also poll the page until the the login process has completed?

	# Either make a list of this URLs or figure out how to navigate through the mass of JS and clicks needed to get there manually.
	# Would need a list of the grades' objectId from D2L.

	#java_wk1 = 'https://minneapolis.ims.mnscu.edu/d2l/lms/grades/admin/enter/grade_item_edit.d2l?objectId=14229002&ou=3696835'
	#d2l_grade_item_url = 'https://minneapolis.ims.mnscu.edu/d2l/lms/grades/admin/enter/grade_item_edit.d2l?objectId=14229003&ou=3696835'
	d2l_grade_item_url = config.d2l_grade_item_url

	browser.get(d2l_grade_item_url)

	lab_assignment = config.week_name

	time.sleep(2) # ugh

	# overall_comments = browser.find_element_by_id('overallComments')
	# print('overall comments:', overall_comments)
	# overall_comments.send_keys(big_warning_message)  # This does not work, but doesn't crash either....

	try:
		browser.switch_to_frame('overallComments$html_ifr')
		time.sleep(1)
		html = browser.find_element_by_id('tinymce')

		print('current text = ', html.text)
		if not big_warning_message in html.text:
			html.send_keys(big_warning_message)

	except Exception as e:
		print('typing error', e)

	browser.switch_to_default_content()

	time.sleep(1)


	#exampleStudentTitle = "Grade for John Zika"


	for student_name in students:

		#e.g. student_name = "Bob Student"

		grade = db.grade_for_lab(student_name, lab_assignment)
		grade_str = '%.1f' % grade
		print(grade_str)

		try:
			gradeBox = browser.find_element_by_xpath('//*[@title="Grade for %s"]' % student_name)
		except:
			print('Error finding grade for ', student_name, ' have they dropped or did you spell their name wrong? Or name change? \nSkipping');
			continue

		oldgrade = 0


		try:
			print(gradeBox.text)
			print('existing grade is ', gradeBox.get_attribute('value'))
			oldgrade = float (gradeBox.get_attribute('value'))
		except:
			print('err reading old grade as number' , gradeBox.text)

		if (grade >= oldgrade):
			gradeBox.clear()  ## Remove old grade

			#gradeBox.send_keys('20')
			gradeBox.send_keys(grade_str)
		else:
			print(student_name, 'old grade is', oldgrade, 'new grade is lower', grade , 'IGNORING'  )

		# Repeat for all the student names and grades

	# Submit button id = 'z_a' for some reason.
	submitbtn = browser.find_element_by_id('z_a')
	submitbtn.click()

	# Now have to click "Yes" in popup

	time.sleep(1)  # just in case - needed?

	buttons = browser.find_elements_by_tag_name('button')
	#print(buttons)
	for button in buttons:
		#print(button, button.text)
		if button.text == 'Yes':
			button.click()   # Srsly?  Well, it works.





def get_student_name_list():

	student_file = config.student_data_file
	all_data = db.load_student_data(student_file)
	just_names = [ student[0] for student in all_data]
	print(just_names)
	return(just_names)


def inputGrades(browser):
	pass




def show_grades():

	students = get_student_name_list()

	print('All grades graded for assignment ', config.week_name)

	for student_name in students:

		#e.g. student_name = "Bob Student"

		grade = db.grade_for_lab(student_name, config.week_name)
		grade_str = '%-30s%.1f' % (student_name, grade)
		print(grade_str)





if __name__ == '__main__':

	args = ['post', 'show']

	if len(sys.argv) < 2 or sys.argv[1] not in args:
		print('python grade_publisher.py post\nor\npython grade_publisher.py show')

	arg = sys.argv[1]

	if arg == 'post':
		post_grades(None, None)  # For testing...

	elif arg == 'show':

		show_grades()
