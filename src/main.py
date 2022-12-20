from shared.pipelines import Pipelines
from shared.statistics import generate_report
from shared.test_info import TestInfo
from src.util.util import parse_projects_file
import metrics
import models


def main():
    """
    To get data run scripts/download_data.py
    :print: statistics for data to the results/
    """
    projects = parse_projects_file()

    gamma = 0.8
    test_info = TestInfo(gamma)
    test_rank_history_based = models.HistoryBasedTestRank()
    test_rank_bayes_based = models.BayesTestRank()
    test_rank_identity_based = models.IdentityTestRank()
    test_rank_random_based = models.RandomTestRank()

    test_metrics = [
        metrics.FirstFailedPosition(),
        metrics.FirstFailedPositionRatio(),
        metrics.AverageFailedPosition(show_graph=True),
        metrics.AverageFailedPositionRatio(show_graph=True),
        metrics.LastFailedPosition(),
        metrics.LastFailedPositionRatio(),
        metrics.FirstFailureDurationRatio(),
        metrics.FirstFailureDurationDifference(show_graph=True),
        metrics.LastFailureDurationRatio(),
        metrics.LastFailureDurationDifference(show_graph=True),
        metrics.AverageFailureDurationRatio(show_graph=True),
        metrics.AverageFailureDurationDifference(show_graph=True),
    ]

    pipelines = [Pipelines(test_info, test_rank_history_based),
                 Pipelines(test_info, test_rank_bayes_based),
                 Pipelines(test_info, test_rank_identity_based),
                 Pipelines(test_info, test_rank_random_based)]

    for i in range(len(pipelines)):
        for project in projects:
            project_reports = []
            print(project)
            statistics = pipelines[i].run_all_with_metrics(project, test_metrics)
            project_reports.append(statistics.create_project_report())
            generate_report(project_reports,
                            output_file_name=f"{project}-{pipelines[i].test_rank.name}-rank-report.html")


if __name__ == "__main__":
    main()
