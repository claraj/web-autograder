import test_artifacts
from test_artifacts import Failure, TestError, TestSuite, TestSuites

from json_encoders import TestItemEncoder#TestCaseEncoder, FailureEncoder, TestErrorEncoder, TestSuiteEncoder, TestSuitesEncoder
import unittest
import json

class TestEncodeTestArtifacts(unittest.TestCase):

    def test_encode_failure(self):
        f = Failure('boo', 'oops')
        # f_json = json.dumps(f, cls=FailureEncoder)
        f_json = json.dumps(f, cls=TestItemEncoder)
        self.assertEqual('{"message": "boo", "fulltext": "oops"}', f_json)

        f = Failure(None, None)
        # f_json = json.dumps(f, cls=FailureEncoder)
        f_json = json.dumps(f, cls=TestItemEncoder)
        self.assertEqual('{"message": null, "fulltext": null}', f_json)

        f = None
        # f_json = json.dumps(f, cls=FailureEncoder)
        f_json = json.dumps(f, cls=TestItemEncoder)
        self.assertEqual('null', f_json)


    def test_encode_error(self):
        e = TestError('err', 'noooo')
        e_json = json.dumps(e, cls=TestItemEncoder)
        self.assertEqual('{"message": "err", "fulltext": "noooo"}', e_json)

        e = TestError(None, None)
        e_json = json.dumps(e, cls=TestItemEncoder)
        self.assertEqual('{"message": null, "fulltext": null}', e_json)

        e = None
        e_json = json.dumps(e, cls=TestItemEncoder)
        self.assertEqual('null', e_json)


    def test_encode_testcase(self):
        tc = test_artifacts.TestCase('the_name', 'doThing')
        tc_json = json.dumps(tc, cls=TestItemEncoder, sort_keys=True)
        tc_dict = json.loads(tc_json)
        self.assertDictEqual({"name": "the_name", "classname": "doThing", "failure": None, "error": None, "passed": True}, tc_dict)


        tc = test_artifacts.TestCase('the_name', 'doThing', failure=Failure('err', 'noo'))
        tc_json = json.dumps(tc, cls=TestItemEncoder, sort_keys=True)
        tc_dict = json.loads(tc_json)
        self.assertDictEqual({"name": "the_name", "classname": "doThing", "failure": {"message": "err", "fulltext": "noo"}, "error": None, "passed": False}, tc_dict)

        tc = test_artifacts.TestCase('the_name', 'doThing', error=TestError('err', 'noo'))
        tc_json = json.dumps(tc, cls=TestItemEncoder, sort_keys=True)
        tc_dict = json.loads(tc_json)
        self.assertDictEqual({"name": "the_name", "classname": "doThing", "error": {"message": "err", "fulltext": "noo"}, "failure": None, "passed": False}, tc_dict)


    def test_encode_testsuite(self):
        tc1 = test_artifacts.TestCase('tc1', 'tcc1', error=TestError('oop', 'ug'))
        tc2 = test_artifacts.TestCase('tc2', 'tcc2', failure=Failure('oops', 'ugs'))

        ts = TestSuite('name', 0, 0)
        ts_json = json.dumps(ts, cls=TestItemEncoder)
        ts_dict = json.loads(ts_json)
        self.assertDictEqual( {"name":"name", "tests": 0, "errors": 0, "failures":0, "skipped": 0, "filename": None, "testcases": [], "passes": 0},  ts_dict)


        ts = TestSuite('name', 2, 1, errors=1, filename='code.py')
        ts.add_testcase(tc1)
        ts.add_testcase(tc2)

        ts_json = json.dumps(ts, cls=TestItemEncoder, sort_keys=True)
        ts_dict = json.loads(ts_json)

        self.maxDiff = None

        self.assertDictEqual({"name":"name", "tests": 2, "errors": 1, "failures":1, "skipped": 0, "passes": 0, "filename": 'code.py', \
        "testcases": [ {"name": "tc1", "classname": "tcc1", "error": {"message": "oop", "fulltext": "ug"}, "failure": None, "passed": False}, \
        {"name": "tc2", "classname": "tcc2",  "failure": {"message": "oops", "fulltext": "ugs"} , "error": None, "passed": False} ], "passes": 0}, ts_dict)


    def test_encode_testsuites(self):

        tc1 = test_artifacts.TestCase('tc1', 'tcc1', error=TestError('oop', 'ug'))
        tc2 = test_artifacts.TestCase('tc2', 'tcc2', failure=TestError('oops', 'ugs'))

        ts1 = TestSuite('name', 0, 0)
        ts2 = TestSuite('name', 2, 1, errors=1, filename='code.py')

        ts2.add_testcase(tc1)
        ts2.add_testcase(tc2)

        tss = TestSuites('suites', tests=2, errors=1, failures=1)
        tss.add_testsuite(ts1)
        tss.add_testsuite(ts2)

        tss_json = json.dumps(tss, cls=TestItemEncoder, sort_keys=True)
        tss_dict = json.loads(tss_json)


        print('\ACTUAL JSON', '\n')

        import pprint
        pprint.pprint(tss_dict)  # Actual

        self.maxDiff = None

        ts1_dict = {"name": "name", "tests":0, "errors": 0, "passes": 0, "failures":0, "skipped": 0, 'filename':None, "testcases": []}
        ts2_dict = {"name":"name", "tests": 2, "errors": 1, "passes": 0, "failures":1, "skipped": 0, "filename": 'code.py', \
        "testcases": [ {"name": "tc1", "classname": "tcc1", "error": {"message": "oop", "fulltext": "ug"}, "failure": None, "passed": False}, \
        {"name": "tc2", "classname": "tcc2",  "failure": {"message": "oops", "fulltext": "ugs"} , "error": None, "passed": False} ], "passes": 0}

        expected_tss_dict = {'name': 'suites', 'skipped': 0, 'errors':1, 'failures':1, 'passes':0, 'tests': 2, "testsuites": [ts1_dict, ts2_dict]}

        print('\nEXPECTED', '\n')
        pprint.pprint(expected_tss_dict)

        self.assertDictEqual(expected_tss_dict, tss_dict)


if __name__ == '__main__':
    unittest.main()
