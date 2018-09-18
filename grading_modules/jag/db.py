import sqlite3
import csv

import config

# Student info DB



db = config.db_file

# Name, starID, GitHub URL

def create():

    con = sqlite3.connect(db)

    cur = con.cursor()

    cur.execute('''CREATE TABLE if not exists students (name text, starid text, github text)''')

    cur.execute('''CREATE TABLE if not exists question_results (starid text, test_set text, question text, points real)''')
    cur.execute('''CREATE TABLE if not exists lab_results (starid text, test_set text, points real)''')

    cur.execute(""" INSERT INTO students values ('clara', 'we4954cp', 'clara-mctc') """)



    con.commit()

    con.close()






def grade_for_lab(student_name, lab_name):

    con = sqlite3.connect(db)
    cur = con.cursor()

    # example sql = """ select total(points) from question_results where starid='Vu Tran' and test_set='week_2' """
    sql = """select total(points) from question_results where starid=? and test_set=?"""

    total = cur.execute(sql, (student_name, lab_name)).fetchall()

    #print(total[0][0])
    return total[0][0]


def save_extra_credit(student_name, test_set, extra_credit_tokens):
    print("YOU HAVE NOT WRITTEN THIS FUNCTION YET")



def save_results(starID, test_set, results, total):

    con = sqlite3.connect(db)
    cur = con.cursor()

    # Example SQL to add a new row if student + test_set not in DB
    # Update points column current row if student+test_set does exist



    con.commit()


    # Save individual points for assignment to question_results
    # These will always be the highest score so far - so if student fixes thing and then break it, they'll have the higher grade.

    for question in results.keys():

        points = results[question]

        current_question_points = cur.execute('select * from question_results where starID = ? and test_set = ? and question = ?', (starID, test_set, question)).fetchone()

        if current_question_points == None:
            cur.execute('insert into question_results values (?, ?, ?, ?)', (starID, test_set, question, points))
        elif points > current_question_points[3]:
            cur.execute('update question_results set points = ? where starID = ? and test_set = ? and question= ?', (points, starID, test_set, question))
        else:
            pass #

    con.commit()


    # The total points will not be accurate if student gets something working and then breaks it.
    # But if student breaks their code, should they get points? Or should their points go down?

    #total_points = cur.execute('select sum(points) from question_results where starID = ? and test_set = ? ')


    current_points_res = cur.execute('select * from lab_results where starID = ? and test_set = ?', (starID, test_set)).fetchone()

    if current_points_res == None:
        cur.execute('insert into lab_results values (?, ?, ?)', (starID, test_set, total))
    elif total > current_points_res[2]:
        cur.execute('update lab_results set points = ? where starID = ? and test_set = ?', (total, starID, test_set))
    else:
        pass # Student's score is lower than current score in DB.



    con.close()





def get_repo_list():
    con = sqlite3.connect(db)
    cur = con.cursor()

    res = cur.execute("select * from students")
    return res.fetchall()

    con.close()


def get_all_test_names(filename):

    ## TODO replace with SQLite (?)

    with open(filename) as f:
        sets = f.readlines()

    print(sets)

    test_sets = [ line.strip() for line in sets ]

    return test_sets


def load_student_data(filename):

    students = []

    with open(filename) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            print(row[0][0])
            if row[0][0] != "#":   # Skip lines starting with #
                students.append(row)

    return students
