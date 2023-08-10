from typing import Tuple

class Key:
    # Uses object Key which is comprised of two Point object, key1: which hold the
    # x,y values for the sheep and key2: which hold the x,y values for the
    # sheepdogbot
    def __init__(self, key1: Tuple[int, int], key2: Tuple[int, int]):
        self.key1 = key1
        self.key2 = key2

    # Overrode the equals and hashCode method of Object Key to allow for simple
    # search in HashMap, enabling me to create a key object of the same state to
    # use for simple lookup
    # instead of traversing through all possible keys in HashMap before lookup
    def __eq__(self, other):
        if not isinstance(other, Key):
            return False
        return (other.key1[0] == self.key1[0] and other.key1[1] == self.key1[1] and other.key2[0] == self.key2[0]
                and other.key2[1] == self.key2[1])

    def __hash__(self):
        PRIME = 31
        result = 1
        result = PRIME * result + hash(self.key1) + hash(self.key2)
        return result