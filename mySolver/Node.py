from .Entity import Entity

class Node(Entity):

    def __init__(self, ID, index):
        
        super().__init__(ID)

        self.index = index

class Node2D(Node):

    def __init__(self, ID, index, x, y):

        super().__init__(ID, index)

        self.x = x
        self.y = y

class Node3D(Node):

    def __init__(self, ID, index, x, y, z):

        super().__init__(ID, index)

        self.x = x
        self.y = y
        self.z = z


