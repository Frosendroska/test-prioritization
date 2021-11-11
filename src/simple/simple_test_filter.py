from src.base_models import TestOccurrencesFilter


class SimpleTestOccurrencesFilter(TestOccurrencesFilter):
    RUN_THRESHOLD = 0.5
    FAILED_THRESHOLD = 0.8
    IGNORED_THRESHOLD = 0.5

    def test_ok(self, test, test_info):
        test_name = test["name"]
        if test_info.allRuns == 0:
            return False
        if test_info.numRun.get(test_name, 0) == 0:
            return True

        run = test_info.numRun.get(test_name, 0)
        failed = test_info.numFailed.get(test_name, 0)
        ignored = test_info.numIgnored.get(test_name, 0)
        all_runs = test_info.allRuns

        return run / all_runs >= self.RUN_THRESHOLD and \
               failed / all_runs < self.FAILED_THRESHOLD and \
               ignored / all_runs < self.IGNORED_THRESHOLD

    def filter(self, test_occurrences, test_info):
        return list(filter(lambda test: self.test_ok(test, test_info), test_occurrences))
