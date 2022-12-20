from src.util.util import OrderType


class TestOccurrencesMetric:

    def __init__(self, order_type: OrderType = OrderType.BOTH, description="", show_graph=True):
        self.show_graph = show_graph
        self.description = description
        self.order_type = order_type

    def measure(self, test_ranked, test_occurrences):
        raise NotImplementedError("TestOccurrencesMetric.measure")
