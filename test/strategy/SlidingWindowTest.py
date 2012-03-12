from datetime import timedelta
from json import load
import unittest
from src.strategy.SlidingWindow import SlidingWindow

__author__ = 'jon'

class SlidingWindowTest(unittest.TestCase):
    """
      Unit tests for the SlidingWindow class
    """

    # Should have complicated split pattern with 5 hour default interval and 5 sub-windows
    mockLogData = load(open('slidingWindow/json/MockLogData.json'))


    def setUp(self):
        """
          Reconstruct a new sliding window strategy object each iteration
        """
        self.slidingWindowStrategy = SlidingWindow()
        self.maxDiff = 2000


    def testParseTrainingDataWithEmptyData(self):
        try:
            self.slidingWindowStrategy.parseTrainingData([])
            self.fail("Should have thrown an assertion error")
        except AssertionError, error:
            self.assertEqual(error.message, 'Training data for SlidingWindow must be non-empty!')


    def testParseTrainingDataWithNoData(self):
        try:
            self.slidingWindowStrategy.parseTrainingData(None)
            self.fail("Should have thrown an assertion error")
        except AssertionError, error:
            self.assertEqual(error.message, 'Training data for SlidingWindow must be non-empty!')


    def testParseLogWindows(self):
        """
          Tests that SlidingWindow correctly categorizes 5 adjacent sub-windows
        """

        # Setup

        # Expected data split by windows. The sub-window dividing lines are:
        #   1) 2009-08-31-01.00.00.000000
        #   2) 2009-08-31-06.00.00.000000
        #   3) 2009-08-31-11.00.00.000000
        #   4) 2009-08-31-16.00.00.000000
        #   5) 2009-08-31-21.00.00.000000
        #   6) 2009-09-01-01.00.00.000000
        expectedWindowedData = load(open('slidingWindow/json/ExpectedWindowedData.json'))

        # Test
        actualWindowedData = self.slidingWindowStrategy.parseLogWindows(SlidingWindowTest.mockLogData[:-1])

        # Verify
        self.assertEqual(expectedWindowedData, actualWindowedData)


    def testParseExtendedLogWindows(self):
        """
          Tests that SlidingWindow correctly categorizes 6 adjacent sub-windows
        """

        # Setup

        # Expected data split by windows. The sub-window dividing lines are:
        #   1.1) 2009-08-31-01.00.00.000000
        #   1.2) 2009-08-31-06.00.00.000000
        #   1.3) 2009-08-31-11.00.00.000000
        #   1.4) 2009-08-31-16.00.00.000000
        #   1.5) 2009-08-31-21.00.00.000000
        #   2.1) 2009-09-01-01.00.00.000000
        expectedWindowedData = load(open('slidingWindow/json/ExpectedExtendedLogWindows.json'))

        # Test
        actualWindowedData = self.slidingWindowStrategy.parseLogWindows(SlidingWindowTest.mockLogData)

        # Verify
        self.assertEqual(expectedWindowedData, actualWindowedData)


    def testParseExtendedModifiedIntervalLogWindows(self):
        """
          Tests that SlidingWindow correctly categorizes 6 adjacent sub-windows
        """

        # Setup
        self.slidingWindowStrategy.windowDelta = timedelta(hours=4)

        # Expected data split by windows. The sub-window dividing lines are:
        #   1.1) 2009-08-31-01.00.00.000000
        #   1.2) 2009-08-31-05.00.00.000000
        #   1.3) 2009-08-31-09.00.00.000000
        #   1.4) 2009-08-31-13.00.00.000000
        #   1.5) 2009-08-31-17.00.00.000000
        #   2.1) 2009-08-31-21.00.00.000000
        #   2.2) 2009-09-01-01.00.00.000000
        #   2.3) 2009-09-01-05.00.00.000000
        #   2.4) 2009-09-01-07.00.00.000000 (the last entry)
        expectedWindowedData = load(open('slidingWindow/json/ExpectedExtendedModifiedIntervalLogWindows.json'))

        # Test
        actualWindowedData = self.slidingWindowStrategy.parseLogWindows(SlidingWindowTest.mockLogData)

        # Verify
        self.assertEqual(expectedWindowedData, actualWindowedData)


    def testParseExtendedModifiedIntervalAndSubWindowsLogWindows(self):
        """
          Tests that SlidingWindow correctly categorizes 6 adjacent sub-windows
        """

        # Setup
        self.slidingWindowStrategy.windowDelta = timedelta(hours=4)
        self.slidingWindowStrategy.numberOfSubWindows = 6

        # Expected data split by windows. The sub-window dividing lines are:
        #   1.1) 2009-08-31-01.00.00.000000
        #   1.2) 2009-08-31-05.00.00.000000
        #   1.3) 2009-08-31-09.00.00.000000
        #   1.4) 2009-08-31-13.00.00.000000
        #   1.5) 2009-08-31-17.00.00.000000
        #   1.6) 2009-08-31-21.00.00.000000
        #   2.1) 2009-09-01-01.00.00.000000
        #   2.2) 2009-09-01-05.00.00.000000
        #   2.3) 2009-09-01-07.00.00.000000 (the last entry)
        expectedWindowedData = load(
            open('slidingWindow/json/ExpectedExtendedModifiedIntervalAndSubWindowsLogWindows.json'))

        # Test
        actualWindowedData = self.slidingWindowStrategy.parseLogWindows(SlidingWindowTest.mockLogData)

        # Verify
        self.assertEqual(expectedWindowedData, actualWindowedData)
