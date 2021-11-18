from src.base_models import TestOccurrencesInfo


class SimpleTestOccurrencesInfo(TestOccurrencesInfo):
    def __init__(self):
        self.all_runs = 0
        self.num_runs = {}
        self.num_success = {}
        self.num_failed = {}
        self.num_ignored = {}

    def update(self, test_occurrences):
        self.all_runs += 1
        for test in test_occurrences:
            test_name = test["name"]
            self.num_runs[test_name] = self.num_runs.get(test_name, 0) + 1

            if test["status"] == "SUCCESS":
                self.num_success[test_name] = self.num_success.get(test_name, 0) + 1
            if test["status"] == "FAILURE":
                self.num_failed[test_name] = self.num_failed.get(test_name, 0) + 1
            if test.get("ignored"):
                self.num_ignored[test_name] = self.num_ignored.get(test_name, 0) + 1
