from IN import INT_MAX
from datetime import timedelta
from json import load
import os
import unittest
from src.strategy.StrategyError import StrategyError
from src.strategy.slidingWindow.IBMPaperStrategy import IBMPaperStrategy

__author__ = 'jon'

class IBMPaperStrategyTest(unittest.TestCase):
    """
      Unit tests for the SlidingWindow class
    """

    def setUp(self):
        self.eventLevelSlidingWindowStrategy = IBMPaperStrategy('TestData', subWindowIntervalDelta=timedelta(hours=5))
        self.eventLevelSlidingWindowStrategy6 = IBMPaperStrategy('TestData', numberOfSubWindows=6, subWindowIntervalDelta=timedelta(hours=1))

        # Parsed training data for five sub-window example
        self.fiveSubWindowTrainingData = [
            (
                # Event level counts for sub-windows
                (2, 0, 1, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0),

                # Total event level counts
                3, 3, 2, 0,

                # Event level counts for sub-window intervals (each sub-window is 1 hour interval
                (
                    (2, 0, 1, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0)
                ),

                # Event level count means
                (0.75, 0.75, 0.50, 0.00),

                # Event level count standard deviations
                (0.83, 1.30, 0.50, 0.00),

                # Number of intervals since last fatal event
                INT_MAX,

                True
            ),
            (
                # Event level counts for sub-windows
                (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1),

                # Total event level counts
                2, 3, 1, 1,

                # Event level counts for sub-window intervals (each sub-window is 1 hour interval
                (
                    (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1)
                ),

                # Event level count means
                (0.50, 0.75, 0.25, 0.25),

                # Event level count standard deviations
                (0.50, 1.30, 0.43, 0.43),

                # Number of intervals since last fatal event
                1,

                False
            ),
            (
                # Event level counts for sub-windows
                (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0),

                # Total event level counts
                1, 3, 0, 1,

                # Event level counts for sub-window intervals (each sub-window is 1 hour interval
                (
                    (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0)
                ),

                # Event level count means
                (0.25, 0.75, 0.00, 0.25),

                # Event level count standard deviations
                (0.43, 1.30, 0.00, 0.43),

                # Number of intervals since last fatal event
                2,

                False
            )
        ]

        # Parsed training data for six sub-window example
        self.sixSubWindowTrainingData = [
            (
                # Event level counts for sub-windows
                (2, 0, 1, 0), (0, 0, 0, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0),

                # Total event level counts
                3, 3, 2, 0,

                # Event level counts for sub-window intervals (each sub-window is 1 hour interval
                (
                    (1,0,0,0), (0,0,1,0), (1,0,0,0), (0,0,0,0), # Hours 1-4
                    (0,0,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0), # Hours 5-8
                    (0,0,0,0), (0,0,0,0), (0,0,1,0), (1,0,0,0), # Hours 9-12
                    (0,3,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0), # Hours 13-16
                    (0,0,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0), # Hours 17-20
                ),

                # Event level count means
                (0.15, 0.15, 0.10, 0.00),

                # Event level count standard deviations
                (0.36, 0.65, 0.30, 0.00),

                # Number of intervals since last fatal event
                INT_MAX,

                True
            ),
            (
                # Event level counts for sub-windows
                (0, 0, 0, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1),

                # Total event level counts
                2, 3, 1, 1,

                # Event level counts for sub-window intervals (each sub-window is 1 hour interval
                (
                    (0,0,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0), # Hours 5-8
                    (0,0,0,0), (0,0,0,0), (0,0,1,0), (1,0,0,0), # Hours 9-12
                    (0,3,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0), # Hours 13-16
                    (0,0,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0), # Hours 17-20
                    (0,0,0,0), (0,0,0,1), (0,0,0,0), (1,0,0,0), # Hours 21-0 (next day)
                ),

                # Event level count means
                (0.10, 0.15, 0.05, 0.05),

                # Event level count standard deviations
                (0.30, 0.65, 0.22, 0.22),

                # Number of intervals since last fatal event
                1,

                False
            ),
            (
                # Event level counts for sub-windows
                (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0),

                # Total event level counts
                2, 3, 1, 1,

                # Event level counts for sub-window intervals (each sub-window is 1 hour interval
                (
                    (0,0,0,0), (0,0,0,0), (0,0,1,0), (1,0,0,0), # Hours 9-12
                    (0,3,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0), # Hours 13-16
                    (0,0,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0), # Hours 17-20
                    (0,0,0,0), (0,0,0,1), (0,0,0,0), (1,0,0,0), # Hours 21-0 (next day)
                    (0,0,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0), # Hours 1-4 (next day)
                ),

                # Event level count means
                (0.10, 0.15, 0.05, 0.05),

                # Event level count standard deviations
                (0.30, 0.65, 0.22, 0.22),

                # Number of intervals since last fatal event
                2,

                False
            )
        ]
        self.projectRoot = os.environ['PROJECT_ROOT']


    def testParseTrainingDataEmpty(self):
        """
          Tests that no training data is returned when passed an empty log
        """

        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData([], [])

        self.assertEqual([], actualTrainingData)


    def testParseTrainingDataNone(self):
        """
          Tests that no training data is returned when passed a null log
        """

        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(None, None)

        self.assertEqual([], actualTrainingData)


    def testParseTrainingDataUnevenSplit(self):
        """
          Tests that the training data fails to parse if the sub-window intervals do not divide evenly into the sub-windows
        """

        try:
            invalidStrategy = IBMPaperStrategy('TestData', subWindowIntervalDelta=timedelta(hours=4))
            self.fail('Trying to construct an invalid strategy should have thrown an exception!')
        except StrategyError, error:
            self.assertEqual('Error parsing windowed log data, cannot divide sub-windows into smaller intervals evenly!', error.message)


    def testParseTrainingDataInvalid(self):
        """
          Tests that no training data is returned when passed an invalid log
        """

        try:
            self.eventLevelSlidingWindowStrategy.parseWindowedLogData([[]], [])
            self.fail('Trying to parse an invalid log should have thrown an exception!')
        except StrategyError, error:
            self.assertEqual('Error parsing windowed log data!', error.message)

        try:
            self.eventLevelSlidingWindowStrategy.parseWindowedLogData([[[{}]]], [])
            self.fail('Trying to parse an invalid log should have thrown an exception!')
        except StrategyError, error:
            self.assertEqual('Error parsing windowed log data!', error.message)

        try:
            self.eventLevelSlidingWindowStrategy.parseWindowedLogData([[[{}, {}], [], []]], [])
            self.fail('Trying to parse an invalid log should have thrown an exception!')
        except StrategyError, error:
            self.assertEqual('Error parsing windowed log data!', error.message)


    def testParseTrainingDataFiveSubWindows(self):
        """
          Tests that the training data for the event level sliding window strategy is generated correctly for 5
            sub-window length windows
        """

        # Setup
        mockWindowedLogData = load(open(self.projectRoot + '/test/strategy/ibmPaperStrategy/parsedLog/FiveSubWindows.json'))
        mockIntervalWindowedLogData = load(open(self.projectRoot + '/test/strategy/ibmPaperStrategy/parsedLog/FiveSubIntervalWindows.json'))
        expectedTrainingData = self.fiveSubWindowTrainingData

        # Test
        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(mockWindowedLogData, mockIntervalWindowedLogData)

        # Verify
        self.assertEqual(expectedTrainingData, actualTrainingData)


    def testParseTrainingDataSixSubWindows(self):
        """
          Tests that the training data for the event level sliding window strategy is generated correctly for 6
            sub-window length windows
        """

        # Setup
        mockWindowedLogData = load(open(self.projectRoot + '/test/strategy/ibmPaperStrategy/parsedLog/SixSubWindows.json'))
        mockIntervalWindowedLogData = load(open(self.projectRoot + '/test/strategy/ibmPaperStrategy/parsedLog/SixSubIntervalWindows.json'))
        expectedTrainingData = self.sixSubWindowTrainingData

        # Test
        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(mockWindowedLogData, mockIntervalWindowedLogData)

        # Verify
        self.assertEqual(expectedTrainingData, actualTrainingData)


    def testBuildTrainingFileContentNone(self):

        try:
            self.eventLevelSlidingWindowStrategy.buildDataFileContent(None)
            self.fail('Should have thrown a StrategyError given None for training data!')
        except StrategyError, error:
            self.assertEqual('Error building training file content: no examples given!', error.message)


    def testBuildTrainingFileContentEmpty(self):

        try:
            self.eventLevelSlidingWindowStrategy.buildDataFileContent([])
            self.fail('Should have thrown a StrategyError given empty training data!')
        except StrategyError, error:
            self.assertEqual('Error building training file content: no examples given!', error.message)


    def testBuildTrainingFileContentInvalid(self):

        invalidTrainingData1 = [
            ((2, 0, 1, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), False),
            ((0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0), False)
        ]
        invalidTrainingData2 = [
            ((2, 0, 1, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0), False),
            ((0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0), False)
        ]

        try:
            self.eventLevelSlidingWindowStrategy.buildDataFileContent(invalidTrainingData1)
            self.fail('Should have thrown a StrategyError given invalid training data!')
        except StrategyError, error:
            self.assertEqual('Error building training file content: Invalid training data!', error.message)

        try:
            self.eventLevelSlidingWindowStrategy.buildDataFileContent(invalidTrainingData2)
            self.fail('Should have thrown a StrategyError given invalid training data!')
        except StrategyError, error:
            self.assertEqual('Error building training file content: Invalid training data!', error.message)


    def testBuildTrainingFileContentFiveWindow(self):

        # Setup
        trainingData = self.fiveSubWindowTrainingData
        expectedTrainingFileContent = open(self.projectRoot + '/test/strategy/ibmPaperStrategy/trainingFile/FiveSubWindows').read()

        # Test
        actualTrainingFileContent = self.eventLevelSlidingWindowStrategy.buildDataFileContent(trainingData)

        # Verify
        self.assertEqual(expectedTrainingFileContent, actualTrainingFileContent)


    def testBuildTrainingFileContentSixWindow(self):

        # Setup
        trainingData = self.sixSubWindowTrainingData
        expectedTrainingFileContent = open(self.projectRoot + '/test/strategy/ibmPaperStrategy/trainingFile/SixSubWindows').read()

        # Test
        actualTrainingFileContent = self.eventLevelSlidingWindowStrategy6.buildDataFileContent(trainingData)

        # Verify
        self.assertEqual(expectedTrainingFileContent, actualTrainingFileContent)
