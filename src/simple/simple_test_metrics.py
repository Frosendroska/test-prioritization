from src.base_models import TestOccurrencesMetric
import numpy as np


class AverageFailedPosition(TestOccurrencesMetric):
    def measure(self, test_ranked, test_occurrences):
        pos = []
        for i in range(len(test_occurrences)):
            if test_occurrences[i]["status"] == "FAILURE":
                pos.append(i / len(test_occurrences))
        return None if len(pos) == 0 else np.mean(pos)


class RankedDurationRatio(TestOccurrencesMetric):
    def __time_until_last_failure(self, test_occurrences):
        start = False
        time = 0
        for i in range(len(test_occurrences) - 1, 0, -1):
            if test_occurrences[i]["status"] == "FAILURE":
                start = True
            if start:
                time += test_occurrences[i]["duration"]
        return time

    def measure(self, test_ranked, test_occurrences):
        time_before = self.__time_until_last_failure(test_occurrences)
        time_ranked = self.__time_until_last_failure(test_ranked)
        return None if time_before == 0 else time_ranked / time_before
