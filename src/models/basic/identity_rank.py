from src.models.models import TestOccurrencesRank


class IdentityTestRank(TestOccurrencesRank):
    """
     Sort identicly.
    """

    name = "identity"

    def key(self, test, test_info):
        pass

    def rank(self, test_occurrences, test_info):
        return test_occurrences
