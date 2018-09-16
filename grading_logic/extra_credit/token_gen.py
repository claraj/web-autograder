# Generate token from

# hash (vsecret + student full name + lab number + question number )


import hashlib
#from . import secret
print('fix the imports here.')
import secret   # Srsly, fix this

import sys

def main():

    if len(sys.argv) < 4:
        print('''Provide 3 arguments. lab number, question number, Student name in title case (and same as D2L name)\n
        Example Lab 1, Question 2, Lady Gaga\n
        python token_gen.py 1 2 Lady Gaga
        ''')

        return


    lab = sys.argv[1]
    question = sys.argv[2]
    name = " ".join(sys.argv[3:])

    cont = input('Generate a token for student |%s| for lab %s, question %s?  \nY to continue\t' % (name, lab, question) )

    if not cont.lower().startswith('y'):
        print('run program again to generate token, check data')
        return



    # token = generate_token_with_bytes(b'clara james11')
    # print(token)
    #
    # token = generate_token_with_student_data('clara james', 1, 1)
    # print(token)

    full_token = generate_token_with_student_data(name, lab, question)
    print(full_token)

    short_token = short_token_student_data(name, lab, question)
    print(short_token)

    comment = "/* EXTRA_CREDIT_CODE_%s Paste this line anywhere in your project code for 1 extra credit point for reporting a bug or issue with Lab %s Question %s */" % (short_token, lab, question)

    print(comment)




'''Fifteen character token to paste into code '''
def short_token_student_data(name, lab_no, question_no):
    byte_string = bytes(name + str(lab_no) + str(question_no), 'utf-8')
    full_token = generate_token_with_bytes(byte_string)
    return full_token[-15:]


def generate_token_with_student_data(name, lab_no, question_no):
    byte_string = bytes(name + str(lab_no) + str(question_no), 'utf-8')
    return generate_token_with_bytes(byte_string)


def generate_token_with_bytes(student_bytes):

    byte_string = secret.secret['key'] + student_bytes

    return hashlib.sha256(byte_string).hexdigest()




if __name__ =='__main__':
    main()
