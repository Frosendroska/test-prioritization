import json
from simple_test_info import SimpleTestOccurrencesInfo
from src.simple.simple_test_filter import SimpleTestOccurrencesFilter
from src.simple.simple_test_metric import SimpleTestOccurrencesMetric
from src.simple.simple_test_rank import SimpleTestOccurrencesRank


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
    for build in builds:
        test_occurrences = get_test_occurrences(project_dir, build["id"])
        if not test_occurrences:
            continue

        tests_filtered = test_filter.filter(test_occurrences, test_info)
        tests_ranked = test_rank.rank(tests_filtered, test_info)
        metric.append(test_metric.measure(tests_ranked))

        test_info.update(test_occurrences)
    return metric


def calc(project):
    project_dir = "data/" + project + "/"
    with open(project_dir + "builds_info.json") as file:
        builds_info = json.load(file)
        builds = builds_info["build"][::-1]  # chronological order
        metric = calc_metric(project_dir, builds)
        print(metric)


def main():
    projects = ["KotlinTools_Exposed_Build",
                "Kotlin_TypeScriptDeclarationToKotlinConverter_DukatBuild",
                "KotlinTools_KotlinFrontendPlugin_Build"]
    for project in projects:
        print(project + ":", end=" ")
        calc(project)


if __name__ == "__main__":
    main()
