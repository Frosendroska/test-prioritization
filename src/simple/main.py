import json
from simple_test_info import SimpleTestOccurrencesInfo
from src.simple.simple_test_filter import SimpleTestOccurrencesFilter
from src.simple.simple_test_metric import SimpleTestOccurrencesMetric
from src.simple.simple_test_rank import SimpleTestOccurrencesRank
from src.util import downloaded
import numpy as np


def get_test_occurrences(project_dir, build_id):
    filename = project_dir + "testOccurrences/" + str(build_id) + ".json"
    with open(filename) as file:
        return json.load(file)


def calc_metric(project_dir, builds):
    test_info = SimpleTestOccurrencesInfo()
    test_filter = SimpleTestOccurrencesFilter()
    test_rank = SimpleTestOccurrencesRank()
    test_metric = SimpleTestOccurrencesMetric()

    metric = []
    for build_id in builds:
        test_occurrences = get_test_occurrences(project_dir, build_id)
        if not test_occurrences:
            continue

        tests_filtered = test_filter.filter(test_occurrences, test_info)
        tests_ranked = test_rank.rank(tests_filtered, test_info)
        metric.append(test_metric.measure(tests_ranked))

        test_info.update(test_occurrences)
    return metric


def calc(project):
    project_dir = "../../data/" + project + "/"
    with open(project_dir + "builds_info.json") as file:
        builds_info = json.load(file)
        builds = builds_info[::-1]  # chronological order
        return calc_metric(project_dir, builds)


def main():
    # projects = downloaded
    projects = ["Kotlin_dev_GradleIntegrationTests"]
    for project in projects:
        print(project)
        metric = calc(project)
        nonnull = list(filter(lambda x: x is not None, metric))
        print(metric)
        print(nonnull)
        print('mean = ', np.mean(nonnull))
        print()
        print()


if __name__ == "__main__":
    main()
