from src.shared.base_models import TestOccurrencesRank


class BayesTestRank(TestOccurrencesRank):
    def key(self, test, test_info):
        test_name = test["name"]
        if test_info.num_failed.get(test_name, 0) == 0:
            return 1
        if test_info.num_runs.get(test_name, 0) == 0:
            return 0

        runs = test_info.num_runs[test_name]
        freq_fail = test_info.num_failed[test_name] / runs
        alpha = 10

        prod_changed = 1
        for filename in test_info.changed_files:
            key = (filename, test_name)
            prod_changed *= test_info.file_changed_test_failed.get(key, 0) + alpha * freq_fail
            prod_changed /= test_info.num_failed[test_name] + alpha

        p_fail = freq_fail * prod_changed
        return 1 - p_fail

    def rank(self, test_occurrences, test_info):
        return sorted(test_occurrences, key=lambda test: self.key(test, test_info))
