from src.shared.base_models import TestOccurrencesInfo


class TestInfo(TestOccurrencesInfo):
    def __init__(self):
        self.num_runs = {}
        self.num_failed = {}
        self.num_success = {}
        self.file_changed_test_failed = {}
        self.changed_files = None

    def update(self, test_occurrences, changed_files):
        self.changed_files = changed_files
        for test in test_occurrences:
            if test.get("ignored"):
                continue
            test_name = test["name"]
            self.num_runs[test_name] = self.num_runs.get(test_name, 0) + 1

            if test["status"] == "SUCCESS":
                self.num_success[test_name] = self.num_success.get(test_name, 0) + 1
            elif test["status"] == "FAILURE":
                self.num_failed[test_name] = self.num_failed.get(test_name, 0) + 1
                for filename in changed_files:
                    key = (filename, test_name)
                    self.file_changed_test_failed[key] = self.file_changed_test_failed.get(key, 0) + 1
