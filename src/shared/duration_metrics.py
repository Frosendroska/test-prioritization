import numpy as np

from src.shared.base_models import TestOccurrencesMetric


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


def metric_ratio_with_other_order(metric, test_ranked, test_occurrences):
    time_before = metric(test_occurrences)
    time_ranked = metric(test_ranked)
    return None if time_before == 0 else time_ranked / time_before


def metric_difference_with_other_order(metric, test_ranked, test_occurrences):
    time_before = metric(test_occurrences)
    time_ranked = metric(test_ranked)
    return (time_ranked - time_before) / 1000  # seconds


class FirstFailureDurationRatio(TestOccurrencesMetric):
    description = "Duration until first failed test / teamcity order"

    def measure(self, test_ranked, test_occurrences):
        return metric_ratio_with_other_order(time_until_first_failure, test_ranked, test_occurrences)


class FirstFailureDurationDifference(TestOccurrencesMetric):
    description = "Duration until first failed test - teamcity order(in seconds)"

    def measure(self, test_ranked, test_occurrences):
        return metric_difference_with_other_order(time_until_first_failure, test_ranked, test_occurrences)


class AverageFailureDurationRatio(TestOccurrencesMetric):
    description = "Average duration until failed test / teamcity order"

    def measure(self, test_ranked, test_occurrences):
        return metric_ratio_with_other_order(average_time_until_failure, test_ranked, test_occurrences)


class AverageFailureDurationDifference(TestOccurrencesMetric):
    description = "Average duration until failed test - teamcity order(in seconds)"

    def measure(self, test_ranked, test_occurrences):
        return metric_difference_with_other_order(average_time_until_failure, test_ranked, test_occurrences)


class LastFailureDurationRatio(TestOccurrencesMetric):
    description = "Duration until last failed test / teamcity order"

    def measure(self, test_ranked, test_occurrences):
        return metric_ratio_with_other_order(time_until_last_failure, test_ranked, test_occurrences)


class LastFailureDurationDifference(TestOccurrencesMetric):
    description = "Duration until last failed test - teamcity order(in seconds)"

    def measure(self, test_ranked, test_occurrences):
        return metric_difference_with_other_order(time_until_last_failure, test_ranked, test_occurrences)
