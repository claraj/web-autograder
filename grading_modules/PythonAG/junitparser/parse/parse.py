import xml.etree.ElementTree as ET
from .models import TestCase, TestSuite, Failure

def parse(filepath):
    """ returns a list of testsuites from the file """
    xml = ET.parse(filepath)
    testobj = xml.getroot()  # May be a testsuite or a testsuites
    testsuites = []

    print(testobj.tag)

    if testobj.tag == 'testsuites':
        for testsuite in testobj:
            ts = parse_testsuite(testsuite)
            testsuites.append(ts)

    elif testobj.tag == 'testsuite':
        ts = parse_testsuite(testobj)
        testsuites.append(ts)

    else:
        raise JUnitParseException(f'The root element of the file {filepath} is expected to be either testsuite or testsuites')

    return testsuites


def parse_testsuite(xml_testsuite):
    """ Extract testcases """
    name = xml_testsuite.get('name')
    tests = int(xml_testsuite.get('tests'), 0)
    failures = int(xml_testsuite.get('failures'))
    errors = int(xml_testsuite.get('errors'), 0)
    skipped = int(xml_testsuite.get('skipped'), 0)

    testsuite = TestSuite(name, tests, failures, errors, skipped)

    for testcase in xml_testsuite:
        if testcase.tag == 'testcase':
            tc = make_testcase(testcase)
            print('making testcase', testcase, tc)
            testsuite.add_testcase(tc)

    return testsuite


def make_testcase(xml_testcase):
    name = xml_testcase.get('name')
    classname = xml_testcase.get('classname')
    xml_failure = xml_testcase.find('failure')
    failure = make_failure(xml_failure)

    testcase = TestCase(name, classname, failure)
    return testcase


def make_failure(xml_failure):
    if xml_failure is None:
        return None
    message = xml_failure.get('message')
    text = xml_failure.text
    return Failure(message, text)


def parsedir(dirpath):
    # parse all the files found, treat each as a testsuite
    pass
