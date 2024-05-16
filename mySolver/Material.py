from .Entity import Entity

class Material(Entity):

    def __init__(self, ID, E, nu):

        super().__init__(ID)

        self.E  = E
        self.nu = nu
        self.G  = E / (2 * (1 + nu))
