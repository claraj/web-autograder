# Question 1: if-else in a function. Which number is larger?


def main():

    # You don't need to modify this function.

    a = input('Enter one number: ')
    b = input('Enter another number: ')

    compare = which_number_is_larger(a, b)

    if compare == 'same':
        print('The two numbers are the same')
    else:
        print('The {} number is larger'.format(compare))



def which_number_is_larger(first, second):

    pass  # TODO delete this line and replace this with your code

    # TODO if the first number is larger, return the string 'first'
    # TODO if the second number is larger, return the string 'second'
    # TODO if the numbers are the same, return the string 'same'


# You don't need to modify the following code.
if __name__ == "__main__":
    main()
