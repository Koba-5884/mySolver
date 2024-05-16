from ..Entity import Entity

class Elem(Entity):

    def __init__(self, ID, nodes, section):

        super().__init__(ID)

        self.nodes   = nodes
        self.section = section
