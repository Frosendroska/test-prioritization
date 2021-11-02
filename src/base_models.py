class TestOccurrencesInfo:
    def update(self, test_occurrences):
        raise NotImplementedError("TestOccurrencesInfo.update")


class TestOccurrencesMetric:
    def measure(self, test_occurrences):
        raise NotImplementedError("TestOccurrencesMetric.measure")


class TestOccurrencesFilter:
    def filter(self, test_occurrences, test_info):
        raise NotImplementedError("TestOccurrencesFilter.filter")


class TestOccurrencesRank:
    def rank(self, test_occurrences, test_info):
        raise NotImplementedError("TestOccurrencesRank.rank")
