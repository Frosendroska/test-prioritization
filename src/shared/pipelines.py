import json
from pathlib import Path
import sys

import numpy as np
from tqdm import tqdm

from src.shared.statistics import Statistics

DATA_DIRECTORY = Path("..") / Path("data")


def get_test_occurrences(project, build_id):
    project_dir = DATA_DIRECTORY / Path(f"{project}")
    filename = project_dir / Path("testOccurrences") / Path(f"{build_id}.json")
    with open(filename, "r") as file:
        return json.load(file)


def get_changed_files(project, build_id):
    project_dir = DATA_DIRECTORY / Path(f"{project}")
    filename = project_dir / Path("builds") / Path(f"{build_id}.json")
    with open(filename, "r") as file:
        return set(json.load(file)["changed_files"])


def num_flaky(test_info, failed_to_run_fraction):
    count = 0
    all_tests = 0
    for test_name, run in test_info.num_runs.items():
        all_tests += 1
        failed = test_info.num_failed.get(test_name, 0)
        if failed / run >= failed_to_run_fraction:
            count += 1
    return count / all_tests


def calc_flaky_count(test_info):
    if test_info.num_runs is None or test_info.num_failed is None:
        return None
    failed_to_run_fractions = np.linspace(0, 1, 100)
    num_flakys = [num_flaky(test_info, fraction) for fraction in failed_to_run_fractions]
    return failed_to_run_fractions, num_flakys


class Pipelines:
    def __init__(self, test_info, test_rank):
        self.test_info = test_info
        self.test_rank = test_rank

    def __calc_metric(self, project, builds, test_metrics):
        metric_results = []
        num_tests = []
        builds_with_changes = []
        num_failures = {}

        for build_id in tqdm(builds, file=sys.stdout):
            changed_files = get_changed_files(project, build_id)
            test_occurrences = get_test_occurrences(project, build_id)
            if not test_occurrences:
                continue

            self.test_info.changed_files = changed_files
            num_tests.append(len(test_occurrences))
            tests_ranked = self.test_rank.rank(test_occurrences, self.test_info)
            cur_build_metrics = [test_metric.measure(tests_ranked, test_occurrences) for test_metric in test_metrics]
            self.test_info.update(test_occurrences)

            for i, test in enumerate(tests_ranked):
                if test["status"] == "FAILURE":
                    num_failures[i] = num_failures.get(i, 0) + 1

            ok = True
            for m in cur_build_metrics:
                ok &= m is not None
            if ok:
                builds_with_changes.append(len(changed_files) > 0)
                metric_results.append(cur_build_metrics)

        flaky_test_stats = calc_flaky_count(self.test_info)
        metrics = zip(test_metrics, np.transpose(metric_results))
        return Statistics(
            project, int(np.mean(num_tests)), metrics, flaky_test_stats, num_failures, builds_with_changes
        )

    def run_all_with_metrics(self, project, test_metrics):
        project_dir = DATA_DIRECTORY / Path(f"{project}")
        with open(project_dir / Path("builds_info.json"), "r") as file:
            builds_info = json.load(file)
            builds = sorted(builds_info)  # chronological order
            print("# builds =", len(builds))
            return self.__calc_metric(project, builds, test_metrics)
