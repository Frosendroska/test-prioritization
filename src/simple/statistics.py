from base64 import b64encode
from io import BytesIO

from domonic.html import *
from matplotlib import pyplot as plt
import numpy as np


def generate_report(projects_statistics, output_file_name="report.html"):
    document = html(*projects_statistics)
    render(f"{document}", output_file_name)


class Statistics:
    def __init__(self, project, metrics, flaky_test_stats):
        self.project = project
        self.metrics = metrics
        self.flaky_test_stats = flaky_test_stats

    def __pyplot_to_img(self):
        tmp_image = BytesIO()
        plt.savefig(tmp_image, format="png")
        image_base64 = b64encode(tmp_image.getvalue()).decode("utf-8")
        return img() >> {"_src": f"data:image/png;base64,{image_base64}"}

    def create_project_report(self):
        metrics_to_show = []
        metric_plots = []
        for metric_name, metric_result in self.metrics:
            nonnull = list(filter(lambda x: x is not None, metric_result))

            plt.figure(figsize=(6, 4))
            plt.plot(range(1, len(nonnull) + 1), nonnull)
            plt.title(metric_name)
            plt.xlabel("# test")
            plt.ylabel("value")
            metric_plots.append(self.__pyplot_to_img())

            metrics_to_show.append(f"{metric_name} mean = {np.mean(nonnull)}")

        failed_to_run_fractions, flaky_counts = self.flaky_test_stats
        plt.figure(figsize=(6, 4))
        plt.plot(failed_to_run_fractions, flaky_counts)
        plt.title(self.project)
        plt.xlabel("x")
        plt.ylabel("fraction of tests: failed / run >= x")
        plot_img = self.__pyplot_to_img()

        return div(
            div(self.project, _style="font-size:20px;font-weight:bold;"),
            div(f"{br()}".join(metrics_to_show)),
            *metric_plots,
            plot_img,
            hr(),
        )
