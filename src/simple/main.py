import json

import matplotlib.pyplot as plt
from tqdm import tqdm
from pathlib import Path

from simple_test_info import SimpleTestOccurrencesInfo
from src.simple.simple_test_filter import SimpleTestOccurrencesFilter
from src.simple.average_failed_position import AverageFailedPosition
from src.simple.simple_test_rank import SimpleTestOccurrencesRank
from src.util import downloaded
import numpy as np

DATA_DIRECTORY = Path("..") / Path("..") / Path("data")


def get_test_occurrences(project, build_id):
    project_dir = DATA_DIRECTORY / Path(f"{project}")
    filename = project_dir / Path("testOccurrences") / Path(f"{build_id}.json")
    with open(filename) as file:
        return json.load(file)


def num_flaky(test_info, failed_to_run):
    count = 0
    all_tests = 0
    for test_name, run in test_info.numRun.items():
        all_tests += 1
        failed = test_info.numFailed.get(test_name, 0)
        if failed / run >= failed_to_run:
            count += 1
    return count / all_tests


def show_stats(project, test_info):
    failed_to_run_fractions = np.linspace(0, 1, 100)
    plt.figure(figsize=(12, 8))
    flaky_counts = [num_flaky(test_info, fraction) for fraction in failed_to_run_fractions]
    plt.plot(failed_to_run_fractions, flaky_counts)
    plt.title(project)
    plt.xlabel("x")
    plt.ylabel("fraction of tests: failed / run >= x")
    plt.show()


def calc_metric(project, builds):
    test_info = SimpleTestOccurrencesInfo()
    test_filter = SimpleTestOccurrencesFilter()
    test_rank = SimpleTestOccurrencesRank()
    test_metric = AverageFailedPosition()

    metric = []
    all_tests = []
    for build_id in tqdm(builds):
        test_occurrences = get_test_occurrences(project, build_id)
        all_tests.append(test_occurrences)
        if not test_occurrences:
            continue

        # tests_filtered = test_filter.filter(test_occurrences, test_info)
        tests_ranked = test_rank.rank(test_occurrences, test_info)
        metric.append(test_metric.measure(tests_ranked))

        test_info.update(test_occurrences)
    show_stats(project, test_info)
    return metric


def calc(project):
    project_dir = DATA_DIRECTORY / Path(f"{project}")
    with open(project_dir / Path("builds_info.json")) as file:
        builds_info = json.load(file)
        builds = builds_info[::-1]  # chronological order
        print('# builds =', len(builds))
        return calc_metric(project, builds)


def main():
    projects = downloaded
    # projects = []
    for project in projects:
        print(project)
        metric = calc(project)
        nonnull = list(filter(lambda x: x is not None, metric))
        # print(nonnull)
        print('metric mean = ', np.mean(nonnull), end="\n\n")


if __name__ == "__main__":
    main()
