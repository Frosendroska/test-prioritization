from src.shared.base_models import TestOccurrencesRank


class HistoryBasedTestRank(TestOccurrencesRank):
    """
    Sort based on the priority, which is the percentage of the fall of this test on past runs.
    """
    name = "history-based"

    def key(self, test, test_info):
        test_name = test["name"]
        run = test_info.num_runs.get(test_name, 0)
        failed = test_info.num_failed.get(test_name, 0)
        return 1 - failed / run if run > 0 else 0

    def rank(self, test_occurrences, test_info):
        return sorted(test_occurrences, key=lambda test: self.key(test, test_info))
