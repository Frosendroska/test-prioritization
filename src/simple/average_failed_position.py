from src.base_models import TestOccurrencesMetric
import numpy as np


class AverageFailedPosition(TestOccurrencesMetric):
    def measure(self, test_occurrences):
        pos = []
        for i in range(len(test_occurrences)):
            if test_occurrences[i]["status"] == "FAILURE":
                pos.append(i / len(test_occurrences))
        return None if len(pos) == 0 else np.mean(pos)
