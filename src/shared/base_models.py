class TestOccurrencesInfo:
    def update(self, test_occurrences):
        raise NotImplementedError("TestOccurrencesInfo.update")


class TestOccurrencesMetric:
    description = None

    def __init__(self, show_graph=False):
        self.show_graph = show_graph

    def measure(self, test_ranked, test_occurrences):
        raise NotImplementedError("TestOccurrencesMetric.measure")


class TestOccurrencesFilter:
    def filter(self, test_occurrences, test_info):
        raise NotImplementedError("TestOccurrencesFilter.filter")


class TestOccurrencesRank:
    name = None

    def rank(self, test_occurrences, test_info):
        raise NotImplementedError("TestOccurrencesRank.rank")
