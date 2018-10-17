"""
NOTE Chapter 3 lab (Lab 6) & Homework assignments are redesigns of previous programs, to follow the new IPO structure.​

Use the code from the Loop-2 program from last time

You will create functions called main(), inputNumbers(), processing(), and outputAnswer().

The old program and new program will have a similar feel when run:
 - ask the user for a small number.
 - Then, ask the user for a larger number.​

Your program should display all the numbers in the range,
add up all the numbers in the range, and display the total.​

So if your user enters 20 and 23, the program should display the
numbers in that range, and calculate 20+21+22+23 = 86.​

Add exception handling in main() and test with bad inputs. ​

Add validations and your own touches.

"""

# TODO your code here.


def inputNumbers():
    # Validation should go here?
    # Check that data is an integer and the first number is smaller than the seconds.
    while True:
        try:
            firstNum = int(input('Enter a small number: '))
            secondNum = int(input(f'Enter another number that is larger than {firstNum}: '))
            if firstNum > secondNum:
                print('The second number should be larger than the first number.')
                continue
            return firstNum, secondNum
        except ValueError:
            print('Make sure you enter an integer number.')


def processing(n1, n2):
    # math
    total = 0
    for n in range(n1, n2+1):
        total += n
    return total


def outputAnswer(total, n1, n2):

    print(f'All the numbers in the range {n1} to {n2} are:')
    for n in range(n1, n2+1):
        print(n)
    print(f'The total is {total}')


def main():
    n1, n2 = inputNumbers()
    total = processing(n1, n2)
    outputAnswer(total, n1, n2)


# It is important that you call main in this way,
# or all the code will run when this is imported into
# the test file, including input statements, which
# will confuse the tests.
if __name__ == '__main__':
    main()
