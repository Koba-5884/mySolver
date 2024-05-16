import numpy as np

class DGeneratorCPS():

    def __init__(self, section):
        self.section = section

    def D(self):

        E  = self.section.material.E
        nu = self.section.material.nu

        return E / (1 - nu ** 2) * np.matrix([[1.0,  nu,          0.0],
                                              [ nu, 1.0,          0.0],
                                              [0.0, 0.0, (1 - nu) / 2]])


class DGeneratorCPE():

    def __init__(self, section):
        self.section = section

    def D(self):

        E  = self.section.material.E
        nu = self.section.material.nu

        return E / ((1 + nu) * (1 - 2 * nu)) * np.matrix([[1 - nu,     nu,              0.0],
                                                          [    nu, 1 - nu,              0.0],
                                                          [   0.0,    0.0, (1 - 2 * nu) / 2]])
