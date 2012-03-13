from json import load
import os
from src.parser.IntrepidRASParser import IntrepidRASParser

__author__ = 'jon'

import unittest

class IntrepidRASParserTest(unittest.TestCase):
    """
      Unit tests for the IntrepidRASParser class
    """

    # The expected empty summarized log
    emptySummarizedLog = {
        'RECID': None,
        'MSG_ID': [],
        'COMPONENT': [],
        'SUBCOMPONENT': [],
        'ERRCODE': [],
        'SEVERITY': [],
        'EVENT_TIME': None,
        'FLAGS': [],
        'PROCESSOR': [],
        'NODE': [],
        'BLOCK': [],
        'LOCATION': [],
        'SERIALNUMBER': [],
        'ECID': [],
        'MESSAGE': []
    }


    def setUp(self):
        """
          Setup before each test, creating a new parser
        """

        self.projectRoot = os.environ['PROJECT_ROOT']
        self.parser = IntrepidRASParser()


    def testIsNumberWithIntegers(self):
        """
          Test that 'isNumber' works with explicit and implicit positive and negative integers
        """

        self.assertTrue(self.parser.isNumber('10'))
        self.assertTrue(self.parser.isNumber('-10'))
        self.assertTrue(self.parser.isNumber('+20'))
        self.assertTrue(self.parser.isNumber('-60'))


    def testIsNumberWithFloats(self):
        """
          Test that 'isNumber' works with explicit and implicit positive and negative floats
        """

        self.assertTrue(self.parser.isNumber('1.0'))
        self.assertTrue(self.parser.isNumber('-1.0'))
        self.assertTrue(self.parser.isNumber('+2.0'))
        self.assertTrue(self.parser.isNumber('-6.0'))


    def testParseEmpty(self):
        """
          Test that parsing an empty log results in empty summarized and log data
        """

        self.parser.logPath = self.projectRoot + '/test/parser/intrepid/log/SampleEmptyLog'

        parsedData = self.parser.parse()
        summarizedData = self.parser.summarize()

        self.assertEqual([], parsedData)
        self.assertEqual(IntrepidRASParserTest.emptySummarizedLog, summarizedData)


    def testParseInvalid(self):
        """
          Test that parsing an invalid log results in empty summarized and log data
        """

        self.parser.logPath = self.projectRoot + '/test/parser/intrepid/log/SampleInvalidLog'

        parsedData = self.parser.parse()
        summarizedData = self.parser.summarize()

        self.assertEqual([], parsedData)
        self.assertEqual(IntrepidRASParserTest.emptySummarizedLog, summarizedData)


    def testParseValidLog(self):
        """
          Test that parsing the 'SampleLog' file results in the expected log data
        """

        # Setup
        expectedSummarizedLog = load(open(self.projectRoot + '/test/parser/intrepid/json/ExpectedSummarizedLog.json'))
        expectedParsedLog = load(open(self.projectRoot + '/test/parser/intrepid/json/ExpectedParsedLog.json'))
        self.parser.logPath = self.projectRoot + '/test/parser/intrepid/log/SampleLog'
        self.maxDiff = 2000

        # Test
        parsedLog = self.parser.parse()
        summarizedLog = self.parser.summarize()

        # Verify
        self.assertEqual(expectedSummarizedLog, summarizedLog)
        self.assertEqual(expectedParsedLog, parsedLog)


if __name__ == '__main__':
    unittest.main()
