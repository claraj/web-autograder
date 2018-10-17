# DO NOT MODIFY THIS FILE

from unittest import TestCase

from lab_questions import q1_length_of_name as q1


class Q2LengthTest(TestCase):

    def test_check_length_of_name_longer_than_6(self):

        msg = 'When called with "%s", is_longer_than_6_letters() should return True"'
        name = 'Beyonce'  # 7 letters
        self.assertTrue(q1.is_longer_than_6_letters(name), msg=msg % name)

        name = 'Jacqueline Lee Kennedy Onassis'  # Way more than 6 letters
        self.assertTrue(q1.is_longer_than_6_letters(name), msg=msg % name)


    def test_check_length_of_name_6_letters(self):

        msg = 'When called with "%s", is_longer_than_6_letters() should return False"'

        name = 'Barack'  # 6 letters
        self.assertFalse(q1.is_longer_than_6_letters(name), msg=msg % name)
        self.assertIsNotNone(q1.is_longer_than_6_letters(name), msg=msg % name)


        name = 'Gisele'  # 6 letters
        self.assertFalse(q1.is_longer_than_6_letters(name), msg=msg % name)
        self.assertIsNotNone(q1.is_longer_than_6_letters(name), msg=msg % name)


    def test_check_length_of_name_6_or_less(self):

        msg = 'When called with "%s", is_longer_than_6_letters() should return False"'

        name = 'Kanye'  # less than 6 letters
        self.assertFalse(q1.is_longer_than_6_letters(name), msg=msg % name)
        self.assertIsNotNone(q1.is_longer_than_6_letters(name), msg=msg % name)

        name = 'Mia'  # less than 6 letters
        self.assertFalse(q1.is_longer_than_6_letters(name), msg=msg % name)
        self.assertIsNotNone(q1.is_longer_than_6_letters(name), msg=msg % name)
