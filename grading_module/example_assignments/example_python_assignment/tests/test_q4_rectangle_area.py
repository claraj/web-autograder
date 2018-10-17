# DO NOT MODIFY THIS FILE!!!

from unittest import TestCase
from unittest.mock import patch

from lab_questions import q4_calculate_rectangle_area as q4


class Q4Test(TestCase):

    def test_function_with_correct_params_created(self):

        error = ''

        try:
            q4.rectangle_area(3, 4)
        except AttributeError:
            error = 'You need to create a function with the name rectangle_area. Make sure your spelling is correct.'
        except TypeError:
            error = 'The rectangle_area function should take exactly two arguments, for the width and height.'

        if error:
            self.fail(error)


    def test_rectangle_area_calculations(self):

        error = ''

        try:
            area = q4.rectangle_area(3, 4)
            self.assertEqual(12, area, 'The area of a triangle with width = 3 and height = 4 should be 12. '
                                       'Your function returned %f' % area)

            area = q4.rectangle_area(100, 4.5)
            self.assertEqual(450, area, 'The area of a triangle with width = 100 and height = 4.5 should be 450. '
                                       'Your function returned %f' % area)

        except (AttributeError, TypeError) as err:
            error = 'Error calling rectangle_area function. Did you create this function, ' \
                    'with the correct name, and parameters?'
            print(err)

        if error:
            self.fail(error)


    @patch('builtins.print')
    @patch('builtins.input')
    def test_answer_printed_from_main(self, mock_input, mock_print):

        # call rectangle_area, verify print was not called

        error = ''

        try:
            area = q4.rectangle_area(2, 3)
            mock_print.assert_not_called()
        except (AttributeError, TypeError) as err:
            error = 'Error calling rectangle_area function. Did you create this function, ' \
                    'with the correct name, and parameters?'

        if error:
            self.fail(error)


        # call main, verify print was called and it includes the correct answer

        mock_input.side_effect = ['4.5', '3.6']
        q4.main()

        found_output = False
        for call in mock_print.call_args_list:
            if call and str(4.5 * 3.6) in str(call[0]):
                found_output = True

        self.assertTrue(found_output, 'Print the area of the rectangle that rectangle_area returns, from the main method.')


