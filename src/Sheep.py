from typing import List, Tuple


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Key:
    def __init__(self, key1: Tuple[int, int], key2: Tuple[int, int]):
        self.key1 = key1
        self.key2 = key2

    def __eq__(self, other):
        if not isinstance(other, Key):
            return False
        return (
            other.key1[0] == self.key1[0]
            and other.key1[1] == self.key1[1]
            and other.key2[0] == self.key2[0]
            and other.key2[1] == self.key2[1]
        )

    def __hash__(self):
        PRIME = 31
        result = 1
        result = PRIME * result + hash(self.key1) + hash(self.key2)
        return result


class Node:
    # Node is comprised of variables x and y which represent location on the grid
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = 0
        self.blocked = False


class Sheep(Node):
    def __init__(self, row: int, col: int):
        super().__init__(row, col)
        self.view: List[Node] = []
        self.neighbors: List[Node] = []
