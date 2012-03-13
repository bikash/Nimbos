from datetime import timedelta
from src.strategy.SlidingWindow import SlidingWindow
from src.strategy.StrategyError import StrategyError

__author__ = 'jon'

class EventLevelSlidingWindow(SlidingWindow):
    """
      Class that holds prediction strategies based on a sliding window of log events. Specifically, this strategy
        uses SVM based on the sliding windows of intervals of several hours. Based on features of the last 4 windows,
        this will predict whether or not there will be a fatal error.
      Specifically, the features we consider in this strategy are (for each window, all of these):
        - number of INFO events
        - number of WARN events
        - number of ERROR events
        - number of FATAL events
    """

    def __init__(self, windowDelta=timedelta(hours=5), numberOfSubWindows=5, severities=None, severityKeyword=None):
        super(EventLevelSlidingWindow, self).__init__(windowDelta, numberOfSubWindows)

        self.severities = severities or ['INFO', 'WARN', 'ERROR', 'FATAL']
        self.severityKey = severityKeyword or 'SEVERITY'


    def parseWindowedLogData(self, windowedLogData):
        """
          Helper function to parse the windowed log data (log data properly divided into sliding windows for learning)
            into training examples.

            @param  windowedLogData The log data divided into sliding window format
        """




        # Handle case of invalid windowed log data
        if windowedLogData is None or len(windowedLogData) <= 0:

            return []

        else:

            trainingData = []

            # Iterate through each window, each of which will consist of a training example
            for window in windowedLogData:
                # Throw an exception if there is 1 or 0 sub-windows in a window --  the strategy doesn't make sense
                if len(window) <= 1:
                    raise StrategyError(
                        'Error parsing windowed log data, found window with %d sub-windows!' % len(window))

                # Iterate through each sub-window, skipping the last window (since the last is used for classification)
                subWindowData = []
                for subWindowIndex in xrange(0, len(window) - 1):
                    subWindow = window[subWindowIndex]

                    # Counts the number of events of each severity
                    eventCounts = {
                        self.severities[0]: 0,
                        self.severities[1]: 0,
                        self.severities[2]: 0,
                        self.severities[3]: 0
                    }

                    for logEvent in subWindow:

                        # Fail to parse the log data if it's invalid (in that it doesn't contain the expected 'SEVERITY' field)
                        if self.severityKey not in logEvent:
                            raise  StrategyError(
                                'Error parsing windowed log data, could not find %s field!' % self.severityKey)

                        # Tally an event of this severity
                        eventCounts[logEvent[self.severityKey]] += 1

                    # Append the counts for this sub-window
                    subWindowData.append(
                        (eventCounts[self.severities[0]], eventCounts[self.severities[1]],
                         eventCounts[self.severities[2]], eventCounts[self.severities[3]]))

                # Look for 'FATAL' events in the last window
                foundFatalEvent = False
                for logEvent in window[-1]:
                    if logEvent[self.severityKey] == self.severities[3]:
                        foundFatalEvent = True
                        break

                # Add the training example
                trainingData.append(tuple(subWindowData) + (foundFatalEvent,))

            return trainingData


    def train(self, examples):
        # TODO: Implement me!
        super(EventLevelSlidingWindow, self).train(examples)


    def predict(self, features):
        # TODO: Implement me!
        super(EventLevelSlidingWindow, self).predict(features)
