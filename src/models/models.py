class TestOccurrencesFilter:
    def filter(self, test_occurrences, test_info):
        raise NotImplementedError("TestOccurrencesFilter.filter")


class TestOccurrencesRank:
    name = None

    def rank(self, test_occurrences, test_info):
        raise NotImplementedError("TestOccurrencesRank.rank")
