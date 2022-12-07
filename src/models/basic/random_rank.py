from src.models.models import TestOccurrencesRank
import random
import sys


class RandomTestRank(TestOccurrencesRank):
    """
     Sort randomly.
    """

    name = "random"

    def key(self, test, test_info):
        return random.randint(0, sys.maxsize - 1)

    def rank(self, test_occurrences, test_info):
        return sorted(test_occurrences, key=lambda test: self.key(test, test_info))
