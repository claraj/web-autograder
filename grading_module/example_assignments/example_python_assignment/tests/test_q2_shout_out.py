# DO NOT MODIFY THIS FILE

from unittest import TestCase

from lab_questions import q2_shout_out as q2


class Q2ShoutTest(TestCase):

    def test_shouting_lowercase(self):

        msg = 'When called with "%s", shout() should return "%s" '

        name = 'beyonce'
        name_shout = 'BEYONCE!!!'
        self.assertEqual(name_shout, q2.shout(name), msg=msg % (name, name_shout))

        name = 'yoda'
        name_shout = 'YODA!!!'
        self.assertEqual(name_shout, q2.shout(name), msg=msg % (name, name_shout))


    def test_shouting_uppercase(self):

        msg = 'When called with "%s", shout() should return "%s" '

        name = 'PIZZA'
        name_shout = 'PIZZA!!!'
        self.assertEqual(name_shout, q2.shout(name), msg=msg % (name, name_shout))


        name = 'VELOCIRAPTOR'
        name_shout = 'VELOCIRAPTOR!!!'
        self.assertEqual(name_shout, q2.shout(name), msg=msg % (name, name_shout))
