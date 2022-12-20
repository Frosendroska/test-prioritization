import numpy as np

from src.metrics.metrics import TestOccurrencesMetric
from src.util.util import OrderType


def first_failed_position(test_occurrences):
    for i in range(len(test_occurrences)):
        if test_occurrences[i]["status"] == "FAILURE":
            return i / len(test_occurrences)
    return None


def average_failed_position(test_occurrences):
    pos = []
    for i in range(len(test_occurrences)):
        if test_occurrences[i]["status"] == "FAILURE":
            pos.append(i / len(test_occurrences))
    return None if len(pos) == 0 else np.mean(pos)


def last_failed_position(test_occurrences):
    for i in range(len(test_occurrences))[::-1]:
        if test_occurrences[i]["status"] == "FAILURE":
            return i / len(test_occurrences)
    return None


def compare_metric_with_other_order(metric, test_ranked, test_occurrences):
    metric_before = metric(test_occurrences)
    metric_ranked = metric(test_ranked)
    return None if metric_before is None or metric_before == 0 else metric_ranked / metric_before


class FirstFailedPosition(TestOccurrencesMetric):
    def __init__(self, order_type: OrderType = OrderType.BOTH, description="", show_graph=True):
        super().__init__(order_type, description, show_graph)
        self.description = "First failed position of " + order_type.value

    def measure(self, test_ranked, test_occurrences):
        if self.order_type == OrderType.RANKED:
            return first_failed_position(test_ranked)
        elif self.order_type == OrderType.INITIAL:
            return first_failed_position(test_occurrences)
        else:
            raise AttributeError("This metric is for different type of order")


class FirstFailedPositionRatio(TestOccurrencesMetric):
    def __init__(self, order_type: OrderType = OrderType.BOTH, description="", show_graph=True):
        super().__init__(order_type, description, show_graph)
        self.description = "First failed position ratio"

    def measure(self, test_ranked, test_occurrences):
        if self.order_type == OrderType.BOTH:
            return compare_metric_with_other_order(first_failed_position, test_ranked, test_occurrences)
        else:
            raise AttributeError("This metric is for different type of order")


class AverageFailedPosition(TestOccurrencesMetric):
    def __init__(self, order_type: OrderType = OrderType.BOTH, description="", show_graph=True):
        super().__init__(order_type, description, show_graph)
        self.description = "Average failed position of " + order_type.value

    def measure(self, test_ranked, test_occurrences):
        if self.order_type == OrderType.RANKED:
            return average_failed_position(test_ranked)
        elif self.order_type == OrderType.INITIAL:
            return average_failed_position(test_occurrences)
        else:
            raise AttributeError("This metric is for different type of order")


class AverageFailedPositionRatio(TestOccurrencesMetric):
    def __init__(self, order_type: OrderType = OrderType.BOTH, description="", show_graph=True):
        super().__init__(order_type, description, show_graph)
        self.description = "Average failed position ratio"

    def measure(self, test_ranked, test_occurrences):
        if self.order_type == OrderType.BOTH:
            return compare_metric_with_other_order(average_failed_position, test_ranked, test_occurrences)
        else:
            raise AttributeError("This metric is for different type of order")


class LastFailedPosition(TestOccurrencesMetric):
    def __init__(self, order_type: OrderType = OrderType.BOTH, description="", show_graph=True):
        super().__init__(order_type, description, show_graph)
        self.description = "Last failed position of " + order_type.value

    def measure(self, test_ranked, test_occurrences):
        if self.order_type == OrderType.RANKED:
            return last_failed_position(test_ranked)
        elif self.order_type == OrderType.INITIAL:
            return last_failed_position(test_occurrences)
        else:
            raise AttributeError("This metric is for different type of order")


class LastFailedPositionRatio(TestOccurrencesMetric):
    def __init__(self, order_type: OrderType = OrderType.BOTH, description="", show_graph=True):
        super().__init__(order_type, description, show_graph)
        self.description = "Last failed position ratio"

    def measure(self, test_ranked, test_occurrences):
        if self.order_type == OrderType.BOTH:
            return compare_metric_with_other_order(last_failed_position, test_ranked, test_occurrences)
        else:
            raise AttributeError("This metric is for different type of order")
