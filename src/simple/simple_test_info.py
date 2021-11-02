from src.base_models import TestOccurrencesInfo


class SimpleTestOccurrencesInfo(TestOccurrencesInfo):
    def __init__(self):
        self.allRuns = 0
        self.numRun = {}
        self.numSuccess = {}
        self.numFailed = {}
        self.numIgnored = {}

    def update(self, test_occurrences):
        self.allRuns += 1
        for test in test_occurrences:
            test_name = test["name"]
            self.numRun[test_name] = self.numRun.get(test_name, 0) + 1

            if test["status"] == "SUCCESS":
                self.numSuccess[test_name] = self.numSuccess.get(test_name, 0) + 1
            if test["status"] == "FAILURE":
                self.numFailed[test_name] = self.numFailed.get(test_name, 0) + 1
            if test.get("ignored"):
                self.numIgnored[test_name] = self.numIgnored.get(test_name, 0) + 1
