import numpy as np

class BGeneratorC2D3():

    def __init__(self, nodes):
        self.nodes = nodes

    def BJ(self, p, q):

        J     = self.__J(p, q)
        J_inv = J.I

        DN1Dx = J_inv[0, 0] * (-1) + J_inv[0, 1] * (-1)
        DN2Dx = J_inv[0, 0]
        DN3Dx = J_inv[0, 1]

        DN1Dy = J_inv[1, 0] * (-1) + J_inv[1, 1] * (-1)
        DN2Dy = J_inv[1, 0]
        DN3Dy = J_inv[1, 1]

        B =  np.matrix([[DN1Dx,   0.0, DN2Dx,   0.0, DN3Dx,   0.0],
                        [  0.0, DN1Dy,   0.0, DN2Dy,   0.0, DN3Dy],
                        [DN1Dy, DN1Dx, DN2Dy, DN2Dx, DN3Dy, DN3Dx]])

        return (B, J)


    def __J(self, p, q):

        node1 = self.nodes[0]
        node2 = self.nodes[1]
        node3 = self.nodes[2]

        DxDp = -node1.x + node2.x
        DyDp = -node1.y + node2.y
        DxDq = -node1.x + node3.x
        DyDq = -node1.y + node3.y

        return np.matrix([[DxDp, DyDp],
                          [DxDq, DyDq]])

class BGeneratorC2D4():
    
    def __init__(self, nodes):
        self.nodes = nodes

    def BJ(self, p, q):

        J     = self.__J(p, q)
        J_inv = J.I

        DN1Dx = J_inv[0, 0] * ( 1 + q) / 4 + J_inv[0, 1] * ( 1 + p) / 4
        DN2Dx = J_inv[0, 0] * (-1 - q) / 4 + J_inv[0, 1] * ( 1 - p) / 4
        DN3Dx = J_inv[0, 0] * (-1 + q) / 4 + J_inv[0, 1] * (-1 + p) / 4
        DN4Dx = J_inv[0, 0] * ( 1 - q) / 4 + J_inv[0, 1] * (-1 - p) / 4

        DN1Dy = J_inv[1, 0] * ( 1 + q) / 4 + J_inv[1, 1] * ( 1 + p) / 4
        DN2Dy = J_inv[1, 0] * (-1 - q) / 4 + J_inv[1, 1] * ( 1 - p) / 4
        DN3Dy = J_inv[1, 0] * (-1 + q) / 4 + J_inv[1, 1] * (-1 + p) / 4
        DN4Dy = J_inv[1, 0] * ( 1 - q) / 4 + J_inv[1, 1] * (-1 - p) / 4

        B =  np.matrix([[DN1Dx,   0.0, DN2Dx,   0.0, DN3Dx,   0.0, DN4Dx,   0.0],
                        [  0.0, DN1Dy,   0.0, DN2Dy,   0.0, DN3Dy,   0.0, DN4Dy],
                        [DN1Dy, DN1Dx, DN2Dy, DN2Dx, DN3Dy, DN3Dx, DN4Dy, DN4Dx]])

        return (B, J)

    def __J(self, p, q):

        node1 = self.nodes[0]
        node2 = self.nodes[1]
        node3 = self.nodes[2]
        node4 = self.nodes[3]

        DxDp = (node1.x - node2.x - node3.x + node4.x) / 4 + (node1.x - node2.x + node3.x - node4.x) / 4 * q
        DyDp = (node1.y - node2.y - node3.y + node4.y) / 4 + (node1.y - node2.y + node3.y - node4.y) / 4 * q
        DxDq = (node1.x + node2.x - node3.x - node4.x) / 4 + (node1.x - node2.x + node3.x - node4.x) / 4 * p
        DyDq = (node1.y + node2.y - node3.y - node4.y) / 4 + (node1.y - node2.y + node3.y - node4.y) / 4 * p

        return np.matrix([[DxDp, DyDp],
                          [DxDq, DyDq]])

class BGeneratorC2D6():

    def __init__(self, nodes):
        self.nodes = nodes

    def BJ(self, p, q):

        J     = self.__J(p, q)
        J_inv = J.I

        DN1Dx = J_inv[0, 0] * (-3 + 4 * p + 4 * q) + J_inv[0, 1] * (-3 + 4 * p + 4 * q)
        DN2Dx = J_inv[0, 0] *         (-1 + 4 * p)
        DN3Dx =                                      J_inv[0, 1] *         (-1 + 4 * q)
        DN4Dx = J_inv[0, 0] *  (4 - 8 * p - 4 * q) + J_inv[0, 1] *             (-4 * p)
        DN5Dx = J_inv[0, 0] *              (4 * q) + J_inv[0, 1] *              (4 * p)
        DN6Dx = J_inv[0, 0] *             (-4 * q) + J_inv[0, 1] *  (4 - 4 * p - 8 * q)

        DN1Dy = J_inv[1, 0] * (-3 + 4 * p + 4 * q) + J_inv[1, 1] * (-3 + 4 * p + 4 * q)
        DN2Dy = J_inv[1, 0] *         (-1 + 4 * p)
        DN3Dy =                                      J_inv[1, 1] *         (-1 + 4 * q)
        DN4Dy = J_inv[1, 0] *  (4 - 8 * p - 4 * q) + J_inv[1, 1] *             (-4 * p)
        DN5Dy = J_inv[1, 0] *              (4 * q) + J_inv[1, 1] *              (4 * p)
        DN6Dy = J_inv[1, 0] *             (-4 * q) + J_inv[1, 1] *  (4 - 4 * p - 8 * q)

        B =  np.matrix([[DN1Dx,   0.0, DN2Dx,   0.0, DN3Dx,   0.0, DN4Dx,   0.0, DN5Dx,   0.0, DN6Dx,   0.0],
                        [  0.0, DN1Dy,   0.0, DN2Dy,   0.0, DN3Dy,   0.0, DN4Dy,   0.0, DN5Dy,   0.0, DN6Dy],
                        [DN1Dy, DN1Dx, DN2Dy, DN2Dx, DN3Dy, DN3Dx, DN4Dy, DN4Dx, DN5Dy, DN5Dx, DN6Dy, DN6Dx]])

        return (B, J)


    def __J(self, p, q):

        node1 = self.nodes[0]
        node2 = self.nodes[1]
        node3 = self.nodes[2]
        node4 = self.nodes[3]
        node5 = self.nodes[4]
        node6 = self.nodes[5]

        DxDp = (-3 * node1.x - node2.x + 4 * node4.x) + (node1.x + node2.x - 2 * node4.x) * 4 * p + (node1.x - node4.x + node5.x - node6.x) * 4 * q
        DyDp = (-3 * node1.y - node2.y + 4 * node4.y) + (node1.y + node2.y - 2 * node4.y) * 4 * p + (node1.y - node4.y + node5.y - node6.y) * 4 * q

        DxDq = (-3 * node1.x - node3.x + 4 * node6.x) + (node1.x - node4.x + node5.x - node6.x) * 4 * p + (node1.x + node3.x - 2 * node6.x) * 4 * q
        DyDq = (-3 * node1.y - node3.y + 4 * node6.y) + (node1.y - node4.y + node5.y - node6.y) * 4 * p + (node1.y + node3.y - 2 * node6.y) * 4 * q

        return np.matrix([[DxDp, DyDp],
                          [DxDq, DyDq]])


class BGeneratorC2D8():
    
    def __init__(self, nodes):
        self.nodes = nodes

    def BJ(self, p, q):

        J     = self.__J(p, q)
        J_inv = J.I

        DN1Dx = J_inv[0, 0] * (2 * p + q + 2 * p * q + q ** 2) / 4 + J_inv[0, 1] * ( p + 2 * q + p ** 2 + 2 * p * q) / 4
        DN2Dx = J_inv[0, 0] * (2 * p - q + 2 * p * q - q ** 2) / 4 + J_inv[0, 1] * (-p + 2 * q + p ** 2 - 2 * p * q) / 4
        DN3Dx = J_inv[0, 0] * (2 * p + q - 2 * p * q - q ** 2) / 4 + J_inv[0, 1] * ( p + 2 * q - p ** 2 - 2 * p * q) / 4
        DN4Dx = J_inv[0, 0] * (2 * p - q - 2 * p * q + q ** 2) / 4 + J_inv[0, 1] * (-p + 2 * q - p ** 2 + 2 * p * q) / 4
        DN5Dx = J_inv[0, 0] *             (-2 * p - 2 * p * q) / 2 + J_inv[0, 1] *                     ( 1 - p ** 2) / 2
        DN6Dx = J_inv[0, 0] *                    (-1 + q ** 2) / 2 + J_inv[0, 1] *              (-2 * q + 2 * p * q) / 2
        DN7Dx = J_inv[0, 0] *             (-2 * p + 2 * p * q) / 2 + J_inv[0, 1] *                     (-1 + p ** 2) / 2
        DN8Dx = J_inv[0, 0] *                    ( 1 - q ** 2) / 2 + J_inv[0, 1] *              (-2 * q - 2 * p * q) / 2

        DN1Dy = J_inv[1, 0] * (2 * p + q + 2 * p * q + q ** 2) / 4 + J_inv[1, 1] * ( p + 2 * q + p ** 2 + 2 * p * q) / 4
        DN2Dy = J_inv[1, 0] * (2 * p - q + 2 * p * q - q ** 2) / 4 + J_inv[1, 1] * (-p + 2 * q + p ** 2 - 2 * p * q) / 4
        DN3Dy = J_inv[1, 0] * (2 * p + q - 2 * p * q - q ** 2) / 4 + J_inv[1, 1] * ( p + 2 * q - p ** 2 - 2 * p * q) / 4
        DN4Dy = J_inv[1, 0] * (2 * p - q - 2 * p * q + q ** 2) / 4 + J_inv[1, 1] * (-p + 2 * q - p ** 2 + 2 * p * q) / 4
        DN5Dy = J_inv[1, 0] *             (-2 * p - 2 * p * q) / 2 + J_inv[1, 1] *                     ( 1 - p ** 2) / 2
        DN6Dy = J_inv[1, 0] *                    (-1 + q ** 2) / 2 + J_inv[1, 1] *              (-2 * q + 2 * p * q) / 2
        DN7Dy = J_inv[1, 0] *             (-2 * p + 2 * p * q) / 2 + J_inv[1, 1] *                     (-1 + p ** 2) / 2
        DN8Dy = J_inv[1, 0] *                    ( 1 - q ** 2) / 2 + J_inv[1, 1] *              (-2 * q - 2 * p * q) / 2

        B =  np.matrix([[DN1Dx,   0.0, DN2Dx,   0.0, DN3Dx,   0.0, DN4Dx,   0.0, DN5Dx,   0.0, DN6Dx,   0.0, DN7Dx,   0.0, DN8Dx,   0.0],
                        [  0.0, DN1Dy,   0.0, DN2Dy,   0.0, DN3Dy,   0.0, DN4Dy,   0.0, DN5Dy,   0.0, DN6Dy,   0.0, DN7Dy,   0.0, DN8Dy],
                        [DN1Dy, DN1Dx, DN2Dy, DN2Dx, DN3Dy, DN3Dx, DN4Dy, DN4Dx, DN5Dy, DN5Dx, DN6Dy, DN6Dx, DN7Dy, DN7Dx, DN8Dy, DN8Dx]])

        return (B, J)

    def __J(self, p, q):

        node1 = self.nodes[0]
        node2 = self.nodes[1]
        node3 = self.nodes[2]
        node4 = self.nodes[3]
        node5 = self.nodes[4]
        node6 = self.nodes[5]
        node7 = self.nodes[6]
        node8 = self.nodes[7]

        DxDp = (-node6.x + node8.x) / 2 + (node1.x + node2.x + node3.x + node4.x - 2 * node5.x - 2 * node7.x) / 2 * p + ( node1.x - node2.x + node3.x - node4.x) / 4 * q + (node1.x + node2.x - node3.x - node4.x - 2 * node5.x + 2 * node7.x) / 2 * p * q + (node1.x - node2.x - node3.x + node4.x + 2 * node6.x - 2 * node8.x) / 4 * q ** 2
        DyDp = (-node6.y + node8.y) / 2 + (node1.y + node2.y + node3.y + node4.y - 2 * node5.y - 2 * node7.y) / 2 * p + ( node1.y - node2.y + node3.y - node4.y) / 4 * q + (node1.y + node2.y - node3.y - node4.y - 2 * node5.y + 2 * node7.y) / 2 * p * q + (node1.y - node2.y - node3.y + node4.y + 2 * node6.y - 2 * node8.y) / 4 * q ** 2

        DxDq = ( node5.x - node7.x) / 2 + ( node1.x - node2.x + node3.x - node4.x) / 4 * p + (node1.x + node2.x + node3.x + node4.x - 2 * node6.x - 2 * node8.x) / 2 * q + (node1.x - node2.x - node3.x + node4.x + 2 * node6.x - 2 * node8.x) / 2 * p * q + (node1.x + node2.x - node3.x - node4.x - 2 * node5.x + 2 * node7.x) / 4 * p ** 2
        DyDq = ( node5.y - node7.y) / 2 + ( node1.y - node2.y + node3.y - node4.y) / 4 * p + (node1.y + node2.y + node3.y + node4.y - 2 * node6.y - 2 * node8.y) / 2 * q + (node1.y - node2.y - node3.y + node4.y + 2 * node6.y - 2 * node8.y) / 2 * p * q + (node1.y + node2.y - node3.y - node4.y - 2 * node5.y + 2 * node7.y) / 4 * p ** 2

        return np.matrix([[DxDp, DyDp],
                          [DxDq, DyDq]])

class BGeneratorC2D4I():

    def __init__(self, nodes):

        self.nodes = nodes

    def BJ(self, p, q):

        Bgen = BGeneratorC2D4(self.nodes)

        (B1, J) = Bgen.BJ(p, q)
        J_inv = J.I

        DM1Dx = J_inv[0, 0] * (-2 * p)
        DM2Dx = J_inv[0, 1] * (-2 * q)

        DM1Dy = J_inv[1, 0] * (-2 * p)
        DM2Dy = J_inv[1, 1] * (-2 * q)

        B2 =  np.matrix([[DM1Dx,   0.0, DM2Dx,   0.0],
                         [  0.0, DM1Dy,   0.0, DM2Dy],
                         [DM1Dy, DM1Dx, DM2Dy, DM2Dx]])

        return (B1, B2, J)

