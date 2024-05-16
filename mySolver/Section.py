from .Entity import Entity

class Section(Entity):

    def __init__(self, ID, material):

        super().__init__(ID)

        self.material = material

class ShellSection(Section):

    def __init__(self, ID, material, T):
        
        super().__init__(ID, material)

        self.T = T

class SolidSection(Section):

    def __init__(self, ID, mat):

        super().__init__(ID, material)


