from src.base_models import TestOccurrencesMetric


class SimpleTestOccurrencesMetric(TestOccurrencesMetric):
    def measure(self, test_occurrences):
        for i in range(len(test_occurrences)):
            if test_occurrences[i]["status"] == "FAILURE":
                return i / len(test_occurrences)
        return None
