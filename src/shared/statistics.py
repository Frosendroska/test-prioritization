from base64 import b64encode
from io import BytesIO

from domonic.html import br, div, hr, html, img, render, p, tr, th, style, td, table
from matplotlib import pyplot as plt
import numpy as np

from src.util.util import RESULTS_PATH, BUILD_HTML_COLOR, MARKED_HTML_COLOR, HTML_FRONT, BEAUTIFUL_TABLE


def generate_report(projects_statistics, output_file_name, results_path=RESULTS_PATH):
    document = html(*projects_statistics)
    results_path.mkdir(parents=True, exist_ok=True)
    render(f"{document}", results_path / output_file_name)


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

    def __flaky_counts_img(self):
        failed_to_run_fractions, flaky_counts = self.flaky_test_stats
        plt.figure(figsize=(6, 4), constrained_layout=True)
        plt.plot(failed_to_run_fractions, flaky_counts)
        plt.title("fraction of tests: failed / run >= x")
        plt.xlabel("x")
        plt.yscale('log')
        flaky_counts_img = self.__pyplot_to_img()
        plt.close()
        return flaky_counts_img

    def __num_failures_img(self):
        indices = list(range(self.num_tests))
        num_failures_list = [self.num_failures.get(i, 0) for i in indices]
        plt.figure(figsize=(6, 4), constrained_layout=True)
        plt.scatter(indices, num_failures_list, s=2)
        plt.title("# test fails on position i")
        plt.xlabel("i")
        plt.yscale('log')
        num_failures_img = self.__pyplot_to_img()
        plt.close()
        return num_failures_img

    def __general_project_report(self, num_builds):
        return div(self.project, _style="font-size:25px;font-weight:bold;"), p(
            div(f"Builds with failing tests: {num_builds}", _style="font-weight:bold;"),
            div(f"Tests on average: {self.num_tests}", _style="font-weight:bold;")
        )

    def __general_metric_report(self, metrics_to_show):
        strings = [": mean = ".join(s) for s in metrics_to_show]
        return div(br(), f"{br()}".join(strings))  # TODO

    def __general_metric_report_table(self, metrics_to_show):
        rows = [tr(td(s[0]), td(s[1])) for s in metrics_to_show]
        return p(
            style(HTML_FRONT + BEAUTIFUL_TABLE),
            table(tr(th("metrics"), th("mean")), *rows),
        )

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
                plt.scatter(x[0], metrics[0], s=3, color=BUILD_HTML_COLOR)
                plt.scatter(x[1], metrics[1], s=3, color=MARKED_HTML_COLOR)
                plt.title(metric_class.description)
                plt.xlabel("# test")
                plt.ylabel("value")
                metric_plots.append(self.__pyplot_to_img())
                plt.close()

            metrics_to_show.append([f"{metric_class.description}", f"{np.round(np.mean(metric_result), 2)}"])

        flaky_counts_img = self.__flaky_counts_img()
        num_failures_img = self.__num_failures_img()

        return div(
            *self.__general_project_report(num_builds),
            self.__general_metric_report_table(metrics_to_show),
            *metric_plots,
            flaky_counts_img,
            num_failures_img,
            hr(),
        )
