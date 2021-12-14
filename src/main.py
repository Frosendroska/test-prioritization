from shared.pipelines import Pipelines
from shared.statistics import generate_report
from shared.test_info import TestInfo
from shared.test_metrics import *
from simple.simple_test_rank import SimpleTestRank
from src.bayes.bayes_test_rank import BayesTestRank
from src.util.util import parse_projects_file


def main():
    projects = parse_projects_file()

    test_info = TestInfo()
    test_rank = SimpleTestRank()
    test_metrics = [
        AverageFailedPosition(),
        AverageFailedPositionRankedRatio(),
        RankedDurationRatio(),
        RankedDurationDifference(),
    ]

    pipelines = Pipelines(test_info, test_rank)

    project_reports = []
    for project in projects:
        print(project)
        statistics = pipelines.run_all_with_metrics(project, test_metrics)
        project_reports.append(statistics.create_project_report())
    generate_report(project_reports)


if __name__ == "__main__":
    main()
