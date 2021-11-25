from pathlib import Path

from simple_test_info import SimpleTestOccurrencesInfo
from src.simple.pipelines import Pipelines
from src.simple.simple_test_filter import SimpleTestOccurrencesFilter
from src.simple.simple_test_metrics import *
from src.simple.simple_test_rank import SimpleTestOccurrencesRank
from src.simple.statistics import generate_report
from src.util import parse_projects_file


def main():
    projects = parse_projects_file(prefix=Path(".."))

    test_info = SimpleTestOccurrencesInfo()
    test_filter = SimpleTestOccurrencesFilter()
    test_rank = SimpleTestOccurrencesRank()
    test_metrics = [AverageFailedPosition(),
                    AverageFailedPositionRankedRatio(),
                    RankedDurationRatio(),
                    RankedDurationDifference()]

    pipelines = Pipelines(test_info, test_filter, test_rank)

    project_reports = []
    for project in projects:
        print(project)
        statistics = pipelines.run_all_with_metrics(project, test_metrics)
        project_reports.append(statistics.create_project_report())
    generate_report(project_reports)


if __name__ == "__main__":
    main()
