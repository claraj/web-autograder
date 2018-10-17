# DO NOT MODIFY THIS FILE!!!

from unittest import TestCase
from unittest.mock import patch

from .print_util import print_calls_contain_output

from lab_questions import Loop2fun as l2


class PrintNumbersLoopFunTest(TestCase):

    @patch('builtins.input')
    def test_input_numbers_valid(self, mock_input):
        mock_input.side_effect = ['2', '4']
        data = l2.inputNumbers()
        self.assertEqual( data, (2, 4))


    @patch('builtins.input')
    def test_input_numbers_invalid(self, mock_input):

        mock_input.side_effect = ['pizza', '34.34', '2', '4']  # bad, bad, good, good,
        # Expect program to reject pizza and 34.34 and return 2, 4
        data = l2.inputNumbers()
        self.assertEqual(data, (2, 4))


    def test_processing(self):
        sum = l2.processing(20, 23)
        self.assertEqual(86, sum)

        sum = l2.processing(3, 6)
        self.assertEqual(18, sum)


    @patch('builtins.print')
    def test_outputAnswer(self, mock_print):

        l2.outputAnswer(14, 2, 5)   # 2+3+4+5 = 14
        expected_output = [ '2', '3', '4', '5', '14']   # Expect all the numbers and then the total.
        self.assertTrue(*print_calls_contain_output(mock_print, expected_output))
