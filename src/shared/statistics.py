from base64 import b64encode
from io import BytesIO

from domonic.html import br, div, hr, html, img, render
from matplotlib import pyplot as plt
import numpy as np


def generate_report(projects_statistics, output_file_name="report.html"):
    document = html(*projects_statistics)
    render(f"{document}", output_file_name)


class Statistics:
    def __init__(self, project, num_tests, metrics, flaky_test_stats, num_failures, builds_with_changes):
        self.project = project
        self.num_tests = num_tests
        self.metrics = metrics
        self.flaky_test_stats = flaky_test_stats
        self.num_failures = num_failures
        self.builds_with_changes = builds_with_changes

    def __pyplot_to_img(self):
        tmp_image = BytesIO()
        plt.savefig(tmp_image, format="png")
        image_base64 = b64encode(tmp_image.getvalue()).decode("utf-8")
        return img() >> {"_src": f"data:image/png;base64,{image_base64}"}

    def create_project_report(self):
        metrics_to_show = []
        metric_plots = []
        num_builds = None
        for metric_class, metric_result in self.metrics:
            num_builds = len(metric_result)
            metrics = [[], []]
            x = [[], []]
            for i in range(len(metric_result)):
                m, changed = metric_result[i], self.builds_with_changes[i]
                metrics[changed].append(m)
                x[changed].append(i + 1)

            if metric_class.show_graph:
                plt.figure(figsize=(6, 4), constrained_layout=True)
                plt.scatter(x[0], metrics[0], s=3, color="#1F77B4")
                plt.scatter(x[1], metrics[1], s=3, color="#E7363A")
                plt.title(metric_class.description)
                plt.xlabel("# test")
                plt.ylabel("value")
                metric_plots.append(self.__pyplot_to_img())
                plt.close()

            metrics_to_show.append(f"{metric_class.description}: mean = {np.round(np.mean(metric_result), 2)}")

        failed_to_run_fractions, flaky_counts = self.flaky_test_stats
        plt.figure(figsize=(6, 4), constrained_layout=True)
        plt.plot(failed_to_run_fractions, flaky_counts)
        plt.title("fraction of tests: failed / run >= x")
        plt.xlabel("x")
        plt.yscale('log')
        flaky_counts_img = self.__pyplot_to_img()
        plt.close()

        indices = list(range(self.num_tests))
        num_failures_list = [self.num_failures.get(i, 0) for i in indices]
        plt.figure(figsize=(6, 4), constrained_layout=True)
        plt.scatter(indices, num_failures_list, s=2)
        plt.title("# test fails on position i")
        plt.xlabel("i")
        plt.yscale('log')
        num_failures_img = self.__pyplot_to_img()
        plt.close()

        return div(
            div(self.project, _style="font-size:20px;font-weight:bold;"),
            div(f"{num_builds} builds with failing tests."),
            div(f"{self.num_tests} tests on average."),
            div(f"{br()}".join(metrics_to_show)),
            *metric_plots,
            flaky_counts_img,
            num_failures_img,
            hr(),
        )
