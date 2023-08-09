from Node import Node
from typing import List

class AngrySheep(Node):
	def __init__(self, row: int, col: int):
		super().__init__(row, col)
		self.view: List[Node] = []
		self.neighbors: List[Node] = []