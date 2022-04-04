import numpy as np

from src.shared.base_models import TestOccurrencesMetric


def first_failed_position(test_occurrences):
    for i in range(len(test_occurrences)):
        if test_occurrences[i]["status"] == "FAILURE":
            return i / len(test_occurrences)
    return None


def average_failed_position(test_occurrences):
    pos = []
    for i in range(len(test_occurrences)):
        if test_occurrences[i]["status"] == "FAILURE":
            pos.append(i / len(test_occurrences))
    return None if len(pos) == 0 else np.mean(pos)


def last_failed_position(test_occurrences):
    for i in range(len(test_occurrences))[::-1]:
        if test_occurrences[i]["status"] == "FAILURE":
            return i / len(test_occurrences)
    return None


def compare_metric_with_other_order(metric, test_ranked, test_occurrences):
    metric_before = metric(test_occurrences)
    metric_ranked = metric(test_ranked)
    return None if metric_before is None or metric_before == 0 else metric_ranked / metric_before


class FirstFailedPosition(TestOccurrencesMetric):
    description = "First failed position"

    def measure(self, test_ranked, test_occurrences):
        return first_failed_position(test_ranked)


class FirstFailedPositionRankedRatio(TestOccurrencesMetric):
    description = "First failed position / teamcity order"

    def measure(self, test_ranked, test_occurrences):
        return compare_metric_with_other_order(first_failed_position, test_ranked, test_occurrences)


class AverageFailedPosition(TestOccurrencesMetric):
    description = "Average failed position"

    def measure(self, test_ranked, test_occurrences):
        return average_failed_position(test_ranked)


class AverageFailedPositionRankedRatio(TestOccurrencesMetric):
    description = "Average failed position / teamcity order"

    def measure(self, test_ranked, test_occurrences):
        return compare_metric_with_other_order(average_failed_position, test_ranked, test_occurrences)


class LastFailedPosition(TestOccurrencesMetric):
    description = "Last failed position"

    def measure(self, test_ranked, test_occurrences):
        return last_failed_position(test_ranked)


class LastFailedPositionRankedRatio(TestOccurrencesMetric):
    description = "Last failed position / teamcity order"

    def measure(self, test_ranked, test_occurrences):
        return compare_metric_with_other_order(last_failed_position, test_ranked, test_occurrences)
