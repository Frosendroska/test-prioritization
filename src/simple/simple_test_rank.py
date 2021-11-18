from src.base_models import TestOccurrencesRank


class SimpleTestOccurrencesRank(TestOccurrencesRank):
    def key(self, test, test_info):
        test_name = test["name"]
        run = test_info.num_runs.get(test_name, 0)
        success = test_info.num_success.get(test_name, 0)
        return success / run if run > 0 else 0

    def rank(self, test_occurrences, test_info):
        return sorted(test_occurrences, key=lambda test: self.key(test, test_info))
