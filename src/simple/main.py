from pathlib import Path

import numpy as np

from simple_test_info import SimpleTestOccurrencesInfo
from src.simple.simple_test_metrics import AverageFailedPosition, RankedDurationRatio
from src.simple.Pipelines import Pipelines
from src.simple.simple_test_filter import SimpleTestOccurrencesFilter
from src.simple.simple_test_rank import SimpleTestOccurrencesRank
from src.util import parse_projects_file


def main():
    projects = parse_projects_file(prefix=Path(".."))

    test_info = SimpleTestOccurrencesInfo()
    test_filter = SimpleTestOccurrencesFilter()
    test_rank = SimpleTestOccurrencesRank()
    test_metrics = [AverageFailedPosition()]

    pipelines = Pipelines(test_info, test_filter, test_rank)

    for project in projects:
        print(project)
        metric = pipelines.run_all_with_metrics(project, test_metrics)
        transposed = np.transpose(metric)
        for i, metric in enumerate(transposed):
            nonnull = list(filter(lambda x: x is not None, metric))
            print(f"metric {i} mean = ", np.mean(nonnull))
        print()


if __name__ == "__main__":
    main()
