class TestOccurrencesMetric:
    description = None

    def __init__(self, show_graph=False):
        self.show_graph = show_graph

    def measure(self, test_ranked, test_occurrences):
        raise NotImplementedError("TestOccurrencesMetric.measure")