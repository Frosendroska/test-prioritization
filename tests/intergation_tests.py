import pytest

from src.shared.pipelines import Pipelines
from src.shared.statistics import generate_report
from src.shared.test_info import TestInfo
from src.util.util import parse_small_projects_file
import src.metrics as metrics
import src.models as models
from pathlib import Path


@pytest.mark.integtest
def test_integration():
    projects = parse_small_projects_file("../src")
    gamma = 0.8
    test_info = TestInfo(gamma)

    test_rank_history_based = models.HistoryBasedTestRank()
    test_rank_bayes_based = models.BayesTestRank()
    test_rank_identity_based = models.IdentityTestRank()
    test_rank_random_based = models.RandomTestRank()

    test_metrics = [
        metrics.FirstFailedPosition(),
        metrics.FirstFailedPositionRankedRatio(),
        metrics.AverageFailedPosition(show_graph=True),
        metrics.AverageFailedPositionRankedRatio(show_graph=True),
        metrics.LastFailedPosition(),
        metrics.LastFailedPositionRankedRatio(),
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
                            f"{project}-{pipelines[i].test_rank.name}-rank-report.html",
                            Path("..") / Path("results-test"))
