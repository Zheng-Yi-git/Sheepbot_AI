from Sheep import Node


class SheepdogBot(Node):
    # Sheepdog bot object

    # neighbors held in list
    neighbors = []

    def __init__(self, row, col):
        super().__init__(row, col)
