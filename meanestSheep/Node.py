class Node:
	# Node is comprised of variables x and y which represent location on the grid
	def __init__(self, row, col):
		self.row = row
		self.col = col
		self.x = 0
		self.blocked = False