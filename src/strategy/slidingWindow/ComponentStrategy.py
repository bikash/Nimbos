from src.strategy.SlidingWindowStrategy import SlidingWindowStrategy

__author__ = 'jon'

class ComponentStrategy(SlidingWindowStrategy):
    """
      Class that holds prediction strategies based on a sliding window of log events. Specifically, this strategy
        uses SVM based on the sliding windows of intervals of several hours. Based on features of the last 4 windows,
        this will predict whether or not there will be a fatal error.
      Specifically, the features we consider in this strategy are (for each window, all of these):
        - number of INFO events
        - number of WARN events
        - number of ERROR events
        - number of FATAL events
        - number of events associated with each component
        - number of events associated with each sub-component
    """

    def parseWindowedLogData(self, windowedLogData):
        # TODO: Implement me!
        super(ComponentStrategy, self).parseWindowedLogData(windowedLogData)

    def learn(self, examples):
        # TODO: Implement me!
        super(ComponentStrategy, self).learn(examples)

    def predict(self, features):
        # TODO: Implement me!
        super(ComponentStrategy, self).predict(features)
