from unittest import TestCase
from parse import parse
import sys
import os

class TestJUnitParser(TestCase):

    def test_junit_file_all_pass(self):
        filename = os.path.join('test', 'example_junit_pass.xml')
        testsuites = parse.parse(filename)
        self.assertEqual(1, len(testsuites))
        ts = testsuites[0]
        self.assertEqual('week_3.Question_1_MPGTest', ts.name)
        self.assertEqual(1, ts.tests)
        self.assertEqual(0, ts.errors)
        self.assertEqual(0, ts.skipped)
        self.assertEqual(0, ts.failures)
        self.assertEqual(1, ts.passes)

        self.assertEqual(1, len(ts.testcases))
        tc = ts.testcases[0]
        self.assertEqual('testMPGCalculations', tc.name)
        self.assertEqual('week_3.Question_1_MPGTest', tc.classname)
        self.assertIsNone(tc.failure)
        self.assertTrue(tc.passed)


    def test_junit_file_some_pass_some_fail(self):
        filename = os.path.join('test', 'example_junit_pass_and_fail.xml')
        testsuites = parse.parse(filename)
        self.assertEqual(1, len(testsuites))
        ts = testsuites[0]
        self.assertEqual('week_3.Question_2_Wear_A_HatTest', ts.name)
        self.assertEqual(3, ts.tests)
        self.assertEqual(0, ts.errors)
        self.assertEqual(0, ts.skipped)
        self.assertEqual(1, ts.failures)
        self.assertEqual(2, ts.passes)

        self.assertEqual(3, len(ts.testcases))
        tc_fail = ts.testcases[0]
        self.assertEqual('doYouNeedAHatTodayAbove40', tc_fail.name)
        self.assertEqual('week_3.Question_2_Wear_A_HatTest', tc_fail.classname)
        self.assertIsNotNone(tc_fail.failure)
        self.assertFalse(tc_fail.passed)
        self.assertEqual("Your doYouNeedAHat method, called with the temperature '40.0000001' is expected to return false.  expected:<false> but was:<true>", tc_fail.failure.message)


        tc_pass = ts.testcases[2]
        self.assertEqual('doYouNeedAHatTodayBelow40', tc_pass.name)
        self.assertEqual('week_3.Question_2_Wear_A_HatTest', tc_pass.classname)
        self.assertIsNone(tc_pass.failure)
        self.assertTrue(tc_pass.passed)



    def test_junit_file_all_fail(self):
        filename = os.path.join('test', 'example_junit_all_fail.xml')
        testsuites = parse.parse(filename)
        self.assertEqual(1, len(testsuites))
        ts = testsuites[0]
        self.assertEqual('week_3.Question_2_Wear_A_HatTest', ts.name)
        self.assertEqual(3, ts.tests)
        self.assertEqual(0, ts.errors)
        self.assertEqual(0, ts.skipped)
        self.assertEqual(3, ts.failures)
        self.assertEqual(0, ts.passes)

        self.assertEqual(3, len(ts.testcases))
        tc = ts.testcases[1]
        self.assertEqual('doYouNeedAHatTodayAt40', tc.name)
        self.assertEqual('week_3.Question_2_Wear_A_HatTest', tc.classname)
        self.assertIsNotNone(tc.failure)
        self.assertFalse(tc.passed)
        fail = tc.failure
        self.assertEqual("When called with the double '40.0' your method threw a class java.lang.RuntimeException, crash!", fail.message)
        self.assertTrue(fail.fulltext.startswith('''java.lang.AssertionError: When called with the double '40.0' your method threw a class java.lang.RuntimeException, crash!\n	at org.junit.Assert.fail(Assert.java:88)\n	at week_3.Question_2_Wear_A_HatTest.findAndInvokeHatMethod(Question_2_Wear_A_HatTest.java:53)\n	at week_3.Question_2_Wear_A_HatTest.doYouNeedAHatTodayAt40(Question_2_Wear_A_HatTest.java:23)'''))


if __name__ == '__main__':
    unittest.main()
