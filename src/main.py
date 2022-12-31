from shared.pipelines import Pipelines
from shared.statistics import generate_report
from shared.test_info import TestInfo
from src.util.util import parse_projects_file
import metrics
import models
from src.util.util import OrderType


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
        metrics.FirstFailedPosition(OrderType.INITIAL),
        metrics.FirstFailedPosition(OrderType.RANKED),
        metrics.FirstFailedPositionRatio(),
        metrics.AverageFailedPosition(OrderType.INITIAL),
        metrics.AverageFailedPosition(OrderType.RANKED),
        metrics.AverageFailedPositionRatio(),
        metrics.LastFailedPosition(OrderType.INITIAL),
        metrics.LastFailedPosition(OrderType.RANKED),
        metrics.LastFailedPositionRatio(),

        metrics.FirstFailureDurationRatio(),
        metrics.FirstFailureDurationDifference(),
        metrics.LastFailureDurationRatio(),
        metrics.LastFailureDurationDifference(),
        metrics.AverageFailureDurationRatio(),
        metrics.AverageFailureDurationDifference(),
    ]

    pipelines = [Pipelines(test_info, test_rank_history_based),
                 Pipelines(test_info, test_rank_bayes_based),
                 Pipelines(test_info, test_rank_identity_based),
                 Pipelines(test_info, test_rank_random_based)]

    for i in range(len(pipelines)):
        project_reports = []
        for project in projects:
            print(project)
            statistics = pipelines[i].run_all_with_metrics(project, test_metrics)
            project_reports.append(statistics.create_project_report())
        generate_report(project_reports, f"{pipelines[i].test_rank.name}-rank-report.html")


if __name__ == "__main__":
    main()
