# Question 2 - Is your name longer than 6 letters?


def main():

    # You don't need to modify this function.

    name = input('Please enter your name: ')

    # Call function to check if your name is longer than 6 letters, or not.

    longer_than_6_letters = is_longer_than_6_letters(name)

    if longer_than_6_letters:
        print('Your name, {}, is longer than 6 letters.'.format(name))
    else:
        print('Your name, {}, is 6 letters or shorter'.format(name))


def is_longer_than_6_letters(name):

    # TODO return True if the name is longer than 6 letters
    # TODO return False if the name is exactly 6 letters, or if it is shorter than 6 letters.

    pass  # TODO replace this with your code


# You don't need to modify the following code.
if __name__ == "__main__":
    main()
