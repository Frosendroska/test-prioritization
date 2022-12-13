from shared.pipelines import Pipelines
from shared.statistics import generate_report
from shared.test_info import TestInfo
from src.metrics.duration_metrics import *
from src.metrics.failed_position_metrics import *
from src.models.history_based.history_based_test_rank import HistoryBasedTestRank
from src.models.bayes.bayes_test_rank import BayesTestRank
from src.models.basic.identity_rank import IdentityTestRank
from src.models.basic.random_rank import RandomTestRank
from src.util.util import parse_projects_file


def main():
    """
    To get data run scripts/download_data.py
    :print: statistics for data to the results/
    """
    projects = parse_projects_file()

    gamma = 0.8
    test_info = TestInfo(gamma)
    test_rank_history_based = HistoryBasedTestRank()
    test_rank_bayes_based = BayesTestRank()
    test_rank_identity_based = IdentityTestRank()
    test_rank_random_based = RandomTestRank()

    test_metrics = [
        FirstFailedPosition(),
        FirstFailedPositionRankedRatio(),
        AverageFailedPosition(show_graph=True),
        AverageFailedPositionRankedRatio(show_graph=True),
        LastFailedPosition(),
        LastFailedPositionRankedRatio(),
        FirstFailureDurationRatio(),
        FirstFailureDurationDifference(show_graph=True),
        LastFailureDurationRatio(),
        LastFailureDurationDifference(show_graph=True),
        AverageFailureDurationRatio(show_graph=True),
        AverageFailureDurationDifference(show_graph=True),
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
            generate_report(project_reports,
                            output_file_name=f"{pipelines[i].test_rank.name}-for-{project}-rank-report.html")


if __name__ == "__main__":
    main()
