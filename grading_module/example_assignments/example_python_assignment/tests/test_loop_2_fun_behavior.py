# DO NOT MODIFY THIS FILE!!!

from unittest import TestCase
from unittest.mock import patch
from threading import Thread

from .print_util import print_calls_contain_output
from lab_questions import Loop2fun as l2


# Checks if the required functions are created
# Checks for expected output, given example input, for the program as a whole.
# Instructor should examine student code for appropriate structure.

class PrintNumbersLoopFunTest(TestCase):

    # Mocks are only used to consume input, otherwise test would hang waiting for input.
    @patch('builtins.print')
    @patch('builtins.input')
    def test_function_with_correct_params_created(self, mock_input, mock_print):

        error = ''

        expected_functions = \
            {
                l2.main: tuple(),              # no args - empty tuple
                l2.inputNumbers: tuple(),
                l2.processing: (1, 2),         # example valid input, anything valid is fine
                l2.outputAnswer: (1, 2, 3)
            }

        for fn, args in expected_functions.items():
            try:
                fn(*args)
            except AttributeError:
                error = f'You need to create a function with the name "{fn}". Make sure your spelling is correct.'
            except TypeError:
                error = f'Check the arguments the function "{fn}" takes.'

            if error:
                self.fail(error)



    @patch('builtins.print')
    @patch('builtins.input')
    def test_behavior_valid_input(self, mock_input, mock_print):

        expected_input = ['3', '6']    # sum = 3 + 4 + 5 + 6 = 18
        mock_input.side_effect = expected_input

        expected_output = ['3', '4', '5', '6', '18']   # Things in the output, in this order

        l2.main()

        self.assertTrue(*print_calls_contain_output(mock_print, expected_output))


    @patch('builtins.print')
    @patch('builtins.input')
    def test_behavior_invalid_input(self, mock_input, mock_print):

        # This is hard to test since there's no definition of how the program should
        # gather input and how it should be validated.

        # This test just makes input() return bad input to the program, and then fails if the code errors.

        # Wrap in a timeout. Fail if the timeout expires.

        exceptions = []

        def run_program(invalid_input):
            mock_input.return_value = invalid_input
            try:
                l2.main()
            except ValueError as e:
                exceptions.append(e)

        bad_inputs = ['0.7', '-12345.asdasd', 'pizza', '123.45']

        for bad_input in bad_inputs:

            test_program = Thread(target=run_program, args=(bad_input,), daemon=True)
            test_program.start()
            test_program.join(1.0)  # Wait for program to complete or error, up to 1 second.

            # It doesn't matter if the program doesn't finish. All this test checks for
            # is whether it crashes or not when given bad input.

            if exceptions:
                self.fail('Your program crashed when given bad input with these error(s)' + str(exceptions))



