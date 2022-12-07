import numpy as np

from src.shared.base_models import TestOccurrencesRank


class BayesTestRank(TestOccurrencesRank):
    """
    Sort based on the priority, which is the probability of falling using the
    naive-bayes formula (with the assumption of independence).
    """
    name = "naive-bayes"

    def key(self, test, test_info):
        test_name = test["name"]
        runs = test_info.num_runs.get(test_name, 0)
        failed = test_info.num_failed.get(test_name, 0)
        if len(test_info.changed_files) == 0:
            return 1 - failed / runs if runs > 0 else 0

        if runs == 0:
            return 0
        if failed == 0:
            return np.inf

        freq_fail = failed / runs
        alpha, beta = 3, 0.75

        prod_changed_log = 0
        for filename in test_info.changed_files:
            key = (filename, test_name)
            changed_and_failed = test_info.file_changed_test_failed.get(key, 0)
            prod_changed_log += np.log(changed_and_failed + alpha * freq_fail)

        prod_changed_log -= len(test_info.changed_files) * np.log(test_info.num_failed[test_name] + alpha)

        p_fail = beta * np.log(freq_fail) + (1 - beta) * prod_changed_log
        return -p_fail

    def rank(self, test_occurrences, test_info):
        return sorted(test_occurrences, key=lambda test: self.key(test, test_info))
