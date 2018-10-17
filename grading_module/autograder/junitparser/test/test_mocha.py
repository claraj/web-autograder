from unittest import TestCase
from parse import parse
import sys
import os

class TestMochaParser(TestCase):

    def test_mocha_file_pass_and_fail(self):

        filename = os.path.join('test', 'example_mocha_pass_fail.xml')
        testsuites = parse.parse(filename)

        self.assertEqual(5, testsuites.tests)
        self.assertEqual(1, testsuites.failures)

        self.assertEqual(4, len(testsuites))
        ts_root = testsuites[0]

        # Empty testsuite, no tests
        self.assertEqual(0, ts_root.tests)
        self.assertEqual('Root Suite', ts_root.name)

        # Testsuite with two testcases, with two passsing tests
        ts_has_testcases = testsuites[2]
        self.assertEqual('api crud tests with no data in DB', ts_has_testcases.name)
        self.assertEqual(2, ts_has_testcases.tests)
        self.assertEqual(2, len(ts_has_testcases))

        for tc in ts_has_testcases.testcases:
            self.assertTrue(tc.passed)

        # Testsuite with one pass, one fail testcase

        ts_has_fail = testsuites[3]
        self.assertEqual("api crud tests with test data in DB", ts_has_fail.name)

        self.assertEqual(3, ts_has_fail.tests)
        self.assertEqual(1, ts_has_fail.failures)
        self.assertEqual(2, ts_has_fail.passes)

        self.assertEqual('/Users/admin/Development/node/AllOfTheWebLabs/Server_Week_1/test/api_test.js', ts_has_fail.filename)
        tc_fail = ts_has_fail[0]
        self.assertFalse(tc_fail.passed)
        self.assertIsNotNone(tc_fail.failure)
        self.assertEqual('expected [ Array(3) ] to have a length of 30000 but got 3', tc_fail.failure.message)

        expected = 'AssertionError: expected [ Array(3) ] to have a length of 30000 but got 3\n    at chai_server.get.end (test/api_test.js:108:32)\n    at Test.Request.callback (node_modules/superagent/lib/node/index.js:716:12)'
        self.assertTrue(tc_fail.failure.fulltext.startswith(expected))
