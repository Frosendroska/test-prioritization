from src.shared.base_models import TestOccurrencesFilter


class SimpleTestFilter(TestOccurrencesFilter):
    RUN_THRESHOLD = 0.5
    FAILED_THRESHOLD = 0.8
    IGNORED_THRESHOLD = 0.5

    def test_ok(self, test, test_info):
        test_name = test["name"]
        if test_info.all_runs == 0 or test_info.num_runs.get(test_name, 0) == 0:
            return True

        run = test_info.num_runs.get(test_name, 0)
        failed = test_info.num_failed.get(test_name, 0)
        ignored = test_info.num_ignored.get(test_name, 0)
        all_runs = test_info.all_runs

        return (
            run / all_runs >= self.RUN_THRESHOLD
            and failed / all_runs < self.FAILED_THRESHOLD
            and ignored / all_runs < self.IGNORED_THRESHOLD
        )

    def filter(self, test_occurrences, test_info):
        return list(filter(lambda test: self.test_ok(test, test_info), test_occurrences))
