import numpy as np

from src.base_models import TestOccurrencesMetric


def average_failed_position(test_occurrences):
    pos = []
    for i in range(len(test_occurrences)):
        if test_occurrences[i]["status"] == "FAILURE":
            pos.append(i / len(test_occurrences))
    return None if len(pos) == 0 else np.mean(pos)


class AverageFailedPosition(TestOccurrencesMetric):
    description = "Average failed position"

    def measure(self, test_ranked, test_occurrences):
        return average_failed_position(test_ranked)


class AverageFailedPositionRankedRatio(TestOccurrencesMetric):
    description = "Average failed position / teamcity order"

    def measure(self, test_ranked, test_occurrences):
        metric_before = average_failed_position(test_occurrences)
        metric_ranked = average_failed_position(test_ranked)
        return None if metric_before is None or metric_before == 0 else metric_ranked / metric_before


def time_until_last_failure(test_occurrences):
    start = False
    time = 0
    for test in test_occurrences[::-1]:
        if test["status"] == "FAILURE":
            start = True
        if start:
            time += test["duration"]
    return time


class RankedDurationRatio(TestOccurrencesMetric):
    description = "Duration until last failed test / teamcity order"

    def measure(self, test_ranked, test_occurrences):
        time_before = time_until_last_failure(test_occurrences)
        time_ranked = time_until_last_failure(test_ranked)
        return None if time_before == 0 else time_ranked / time_before


class RankedDurationDifference(TestOccurrencesMetric):
    description = "Duration until last failed test - teamcity order"

    def measure(self, test_ranked, test_occurrences):
        time_before = time_until_last_failure(test_occurrences)
        time_ranked = time_until_last_failure(test_ranked)
        return time_ranked - time_before
