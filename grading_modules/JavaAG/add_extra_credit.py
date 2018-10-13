from extra_credit import token_gen
import subprocess

## For the current lab, for this student generate all the valid tokens
## search for each
## return a list of points


## One token == 1 point. NO EXCEPTIONS!!

def token_search(student_name, lab_number, total_questions, code_directory):
    tokens = []

    for q in range(total_questions):

        token_text = token_gen(student_name, lab_number, q)

        if find_in_code(token_text, code_directory):
            tokens.add(q)

    return tokens


def find_in_code(text, root_dir):

    result = subprocess.run('grep -r "%s" %s' % (text, root_dir), shell=True, stdout=subprocess.PIPE)

    #print(result.stdout)


    if result.stdout:
        print('*******' , text , " WAS found in a file at location ", root_dir)
        return True

    print(text , " was not found in a file at location: ", root_dir)
    return False

    # result = subprocess.run(command, stdout=subprocess.PIPE)
    # print(result)


if __name__ == '__main__':
    # just testing
    find_in_code('TODO', 'student_code/assignment-2-loops-and-arrays-ag5300cm')
    find_in_code('TOthisiinotherehsdfsdfsfdDO', 'student_code/assignment-2-loops-and-arrays-ag5300cm')
