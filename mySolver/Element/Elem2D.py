import numpy as np

from .Element    import Elem
from .BGenerator import BGeneratorC2D3, BGeneratorC2D4, BGeneratorC2D6, BGeneratorC2D8, BGeneratorC2D4I
from .DGenerator import DGeneratorCPS, DGeneratorCPE
from .IntPoint   import IntPointTri1, IntPointTri3, IntPoint2x2, IntPoint3x3

class C2D(Elem):

    def compute_Ke(self):

        P = self.IntP.P
        W = self.IntP.W

        self.B = []
        self.J = []

        for p in P:

            (B, J) = self.Bgen.BJ(*p)

            self.B.append(B)
            self.J.append(J)

        self.D = self.Dgen.D()

        detJ = [np.linalg.det(J) for J in self.J]

        self.Ke = sum([B.T * self.D * B * detJ * W for B, detJ, W in zip(self.B, detJ, W)]) * self.section.T


class C2D4I(Elem):

    def compute_Ke(self):

        P = self.IntP.P
        W = self.IntP.W

        self.B1 = []
        self.B2 = []
        self.J  = []

        for p in P:

            (B1, B2, J) = self.Bgen.BJ(*p)

            self.B1.append(B1)
            self.B2.append(B2)
            self.J.append(J)

        self.D = self.Dgen.D()

        detJ = [np.linalg.det(J) for J in self.J]

        V   = sum([detJ * W for detJ, W in zip(detJ, W)])
        B2_ = sum([B2 * detJ * W for B2, detJ, W in zip(self.B2, detJ, W)]) / V

        self.B2 = [B2 - B2_ for B2 in self.B2]

        K11 = sum([B1.T * self.D * B1 * detJ * W for B1, detJ, W in zip(self.B1, detJ, W)])
        K22 = sum([B2.T * self.D * B2 * detJ * W for B2, detJ, W in zip(self.B2, detJ, W)])
        K12 = sum([B1.T * self.D * B2 * detJ * W for B1, B2, detJ, W in zip(self.B1, self.B2, detJ, W)])

        self.Ke = (K11 - K12 * K22.I * K12.T) * self.section.T

class CPS3(C2D):

    def __init__(self, ID, nodes, section):

        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D3(self.nodes)
        self.Dgen = DGeneratorCPS(self.section)
        self.IntP = IntPointTri1()

class CPE3(C2D):

    def __init__(self, ID, nodes, section):

        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D3(self.nodes)
        self.Dgen = DGeneratorCPE(self.section)
        self.IntP = IntPointTri1()

class CPS4(C2D):

    def __init__(self, ID, nodes, section):

        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D4(self.nodes)
        self.Dgen = DGeneratorCPS(self.section)
        self.IntP = IntPoint2x2()
    
class CPE4(C2D):
    
    def __init__(self, ID, nodes, section):

        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D4(self.nodes)
        self.Dgen = DGeneratorCPE(self.section)
        self.IntP = IntPoint2x2()

class CPS6(C2D):

    def __init__(self, ID, nodes, section):

        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D6(self.nodes)
        self.Dgen = DGeneratorCPS(self.section)
        self.IntP = IntPointTri3()

class CPE6(C2D):

    def __init__(self, ID, nodes, section):

        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D6(self.nodes)
        self.Dgen = DGeneratorCPE(self.section)
        self.IntP = IntPointTri3()

class CPS8(C2D):

    def __init__(self, ID, nodes, section):

        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D8(self.nodes)
        self.Dgen = DGeneratorCPS(self.section)
        self.IntP = IntPoint3x3()

class CPE8(C2D):

    def __init__(self, ID, nodes, section):

        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D8(self.nodes)
        self.Dgen = DGeneratorCPE(self.section)
        self.IntP = IntPoint3x3()

class CPS8R(C2D):

    def __init__(self, ID, nodes, section):

        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D8(self.nodes)
        self.Dgen = DGeneratorCPS(self.section)
        self.IntP = IntPoint2x2()

class CPE8R(C2D):

    def __init__(self, ID, nodes, section):

        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D8(self.nodes)
        self.Dgen = DGeneratorCPE(self.section)
        self.IntP = IntPoint2x2()

class CPS4I(C2D4I):

    def __init__(self, ID, nodes, section):
        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D4I(self.nodes)
        self.Dgen = DGeneratorCPS(self.section)
        self.IntP = IntPoint2x2()

class CPE4I(C2D4I):

    def __init__(self, ID, nodes, section):
        super().__init__(ID, nodes, section)

        self.Bgen = BGeneratorC2D4I(self.nodes)
        self.Dgen = DGeneratorCPE(self.section)
        self.IntP = IntPoint2x2()
