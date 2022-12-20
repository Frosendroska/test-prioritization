import numpy as np

from src.metrics.metrics import TestOccurrencesMetric
from src.util.util import OrderType


def time_until_first_failure(test_occurrences):
    time = 0
    for test in test_occurrences:
        if test["status"] == "FAILURE":
            return time
        time += test["duration"]
    return 0


def average_time_until_failure(test_occurrences):
    times = []
    time = 0
    for test in test_occurrences:
        if test["status"] == "FAILURE":
            times.append(time)
        time += test["duration"]
    return 0 if len(times) == 0 else np.mean(times)


def time_until_last_failure(test_occurrences):
    start = False
    time = 0
    for test in test_occurrences[::-1]:
        if test["status"] == "FAILURE":
            start = True
        if start:
            time += test["duration"]
    return time


def metric_difference_with_other_order(metric, test_ranked, test_occurrences):
    time_before = metric(test_occurrences)
    time_ranked = metric(test_ranked)
    return (time_ranked - time_before) / 1000  # seconds


def metric_ratio_with_other_order(metric, test_ranked, test_occurrences):
    time_before = metric(test_occurrences)
    time_ranked = metric(test_ranked)
    return None if time_before == 0 else time_ranked / time_before


class FirstFailureDurationRatio(TestOccurrencesMetric):

    def __init__(self, order_type: OrderType = OrderType.BOTH, description="", show_graph=True):
        super().__init__(order_type, description, show_graph)
        self.description = "Duration until first failed test ratio"

    def measure(self, test_ranked, test_occurrences):
        if self.order_type == OrderType.BOTH:
            return metric_ratio_with_other_order(time_until_first_failure, test_ranked, test_occurrences)
        else:
            raise AttributeError("This metric is for different type of order")


class FirstFailureDurationDifference(TestOccurrencesMetric):
    description = "Duration until first failed test - teamcity order(in seconds)"

    def measure(self, test_ranked, test_occurrences):
        return metric_difference_with_other_order(time_until_first_failure, test_ranked, test_occurrences)


class AverageFailureDurationRatio(TestOccurrencesMetric):

    def __init__(self, order_type: OrderType = OrderType.BOTH, description="", show_graph=True):
        super().__init__(order_type, description, show_graph)
        self.description = "Average duration until failed test ratio"

    def measure(self, test_ranked, test_occurrences):
        if self.order_type == OrderType.BOTH:
            return metric_ratio_with_other_order(average_time_until_failure, test_ranked, test_occurrences)
        else:
            raise AttributeError("This metric is for different type of order")


class AverageFailureDurationDifference(TestOccurrencesMetric):
    description = "Average duration until failed test - teamcity order(in seconds)"

    def measure(self, test_ranked, test_occurrences):
        return metric_difference_with_other_order(average_time_until_failure, test_ranked, test_occurrences)


class LastFailureDurationRatio(TestOccurrencesMetric):

    def __init__(self, order_type: OrderType = OrderType.BOTH, description="", show_graph=True):
        super().__init__(order_type, description, show_graph)
        self.description = "Duration until last failed test ratio"

    def measure(self, test_ranked, test_occurrences):
        if self.order_type == OrderType.BOTH:
            return metric_ratio_with_other_order(time_until_last_failure, test_ranked, test_occurrences)
        else:
            raise AttributeError("This metric is for different type of order")


class LastFailureDurationDifference(TestOccurrencesMetric):
    description = "Duration until last failed test - teamcity order(in seconds)"

    def measure(self, test_ranked, test_occurrences):
        return metric_difference_with_other_order(time_until_last_failure, test_ranked, test_occurrences)
